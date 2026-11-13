# Understanding, speech-to-text, object storage, and the asset library

Behaviour and gotchas for `seed_understand`, `seed_audio_understand`,
`speech_to_text`, `media_upload`, `media_presign`, and the `ark_asset_*` tools.
For parameters see the tool schema and
[API reference](https://byteplus-sa.github.io/ark-mcp/api-reference/). Per-model limits:
[models-and-limits.md](models-and-limits.md); env vars:
[environment.md](environment.md); submitting and polling background work:
[workflows.md](workflows.md), [polling-and-artifacts.md](polling-and-artifacts.md).

## Execution mode at a glance

| Tool | Mode | Needs |
|---|---|---|
| `seed_understand`, `seed_audio_understand` | background required (`ark_job_submit`) | `BYTEPLUS_MODELARK_API_KEY` |
| `speech_to_text` | background required | `BYTEPLUS_SEED_SPEECH_API_KEY` |
| `media_upload` | background required | object storage (TOS or S3) |
| `media_presign` | foreground | object storage |
| `ark_asset_*` | foreground (`ark_asset_create` and `ark_asset_verification_result` may also run in the background) | AK/SK |

**Never work around a client timeout by shortening the prompt or calling a
background-required tool in the foreground**: submit with `ark_job_submit` and
poll `ark_job_get`. `save_to` inside a job needs `OUTPUT_ROOTS` on the server
(a worker has no MCP roots) and is otherwise rejected before billing; see
[background-job-output.md](background-job-output.md).

## Understanding (`seed_understand`, `seed_audio_understand`)

Both tools use ModelArk Chat Completions with **deep thinking always on** and
return **only the final answer** (the trace is never returned or saved). Depth is `reasoning_effort`: `low` for simple OCR or lookups,
`medium` default, `high` for deep reviews; cost shows in `usage.reasoning_tokens`.
Do not pass `thinking` (ignored).

### Choosing the model

- **`seed_understand`**: pick the model from `ark_list_models(kind='understanding')`
  (exact IDs; omit for the default). Per-model limits are in
  [models-and-limits.md](models-and-limits.md); a request outside them fails
  locally before billing.
- **`seed_audio_understand` has no `model` argument.** The server fixes the
  model (`SEED_AUDIO_UNDERSTANDING_MODEL`); `ark_list_models` shows which.

### Media inputs

- **Videos are HTTPS URLs only** (no Base64). Page or platform links (YouTube,
  TikTok, Instagram), auth-gated URLs, and anything that is not a directly
  fetchable video file fail: download locally, `media_upload`, and pass the
  returned URL. Do not substitute transcripts when the task is about visuals.
- **Images**: URL or Base64; upload local files with `media_upload` first.
- **Audio**: 1-8 clips in order; URL preferred. Base64 must be raw (no `data:`
  prefix), at most 10 MB decoded, with `mime_type` one of `audio/wav`,
  `audio/mpeg`, `audio/flac`, `audio/aac`, `audio/mp4`. **Base64 Ogg/Opus/PCM is
  rejected: upload and pass a URL.**
- **Large audio / video soundtracks:** `seed_audio_understand.delivery` is
  `auto` (default), `direct`, or `files_api`. Automatic delivery retries one
  audio-related 400 rejection through Files API; explicit delivery uploads
  first. Files API supports up to 512 MB versus the default model's 25 MiB
  direct URL limit. Base64 stays inline. Video uses its soundtrack plus
  frames sampled at 0.2 fps, which also consume tokens. Outputs report
  `audio_delivery` per input and `delivery_fallback_reason`. Uploads are
  deleted best-effort after the call and otherwise expire after roughly a day.
  Malformed upload successes return `INVALID_RESPONSE` with
  `ambiguous_completion=true`, not a safe retry. Cleanup uses a recoverable,
  validated file ID; without one, the upload must expire.

### Shaping and saving the answer

- **Enforce structure with `response_format`, not prompt wording.** Pass a
  template's JSON Schema verbatim as `type: "json_schema"`; the parsed value is
  in `choices[0].parsed` and is returned even when `return_content` is
  `summary` or `none`. **Always check `choices[0].schema_violation` before
  trusting `parsed`.**
- **`json_retry` (0-2) costs extra billed attempts** and is skipped when
  `finish_reason="length"`: raise `max_tokens` instead (it includes thinking
  tokens). If a retry call itself fails, the earlier billed answer is kept.
- **Keep large answers out of context** with `save_to` plus
  `return_content="none"` (or `"summary"`: first 2,000 characters). `save_to` is
  an absolute path inside an allowed output root (stdio only), validated before
  billing; replacing a different existing file needs `overwrite=true`. If the
  write fails after billing the call still succeeds with `saved_path=null` and
  the full answer inline.
- Ask for timestamps when referencing video moments; name the languages for OCR.

### Timeouts and cost

A chat timeout returns `TIMEOUT` (`retryable=true`) but the server **does not
retry it**: a second full thinking run doubles the cost (429 and 5xx are
retried). Raise `SEED_UNDERSTANDING_TIMEOUT_MS` for long video analysis and size
the job TTL to match. Output is text only.

### Audio understanding vs speech-to-text

- **`seed_audio_understand`** answers questions about audio: translation,
  speaker count/gender/emotion, summaries and minutes, music and sound events.
- **Prefer `speech_to_text` for plain or long-form transcription**, and whenever
  you need word-level timestamps, utterances, or speaker labels.
- **Structured output:** the default audio model enforces `json_schema` but not
  `json_object`; use `json_schema` when you need JSON.

## Speech-to-text (`speech_to_text`)

Seed Speech ASR. One background job submits, polls, and returns the full
transcript; there is no separate provider task ID. Capped by
`SEED_SPEECH_ASR_POLL_MAX_SECONDS` (default 600 s).

- **Input:** exactly one of `audio_url` (HTTPS), `audio_data` (Base64), or
  `audio_file_path` (absolute path, **stdio only**), each up to **200 MB**, plus
  a required `audio_format` (`wav`, `mp3`, `ogg`, `raw`, `flac`). `options.language`
  defaults to `en-US`; set the real language for non-English audio.
- **Output:** `result.text`, `result.utterances` (**word-level timings**, speaker
  labels), `duration_ms`. Text only.
- **Status `20000003` (silent audio)** is terminal and non-retryable ("query
  failed with status code 20000003"): no speech detected. Check the audio has
  speech and matches `audio_format`; for `wav`/`raw` the gateway assumes 16 kHz,
  16-bit, mono PCM, and a mismatch decodes to silence. Re-submit corrected audio.

## Object storage (`media_upload`, `media_presign`)

Needed whenever a tool takes media as a URL only (Seedance video/audio
references, understanding videos, VOD sources). TOS or S3 makes no difference
to tool behaviour.

### `media_upload`

Uploads 1-50 items (Base64 `data` or stdio-only `file_path`) and returns a
presigned GET `url` and an `object_key` per item, in request order.

- **Items fail independently** and the call still succeeds: **always check
  `failed` and each `items[].error`**; re-upload only `retryable=true` items and
  fix the input of the rest.
- **Only an over-size request fails the whole call.** The total decoded size is
  checked before anything uploads against `MEDIA_UPLOAD_BATCH_MAX_BYTES`
  (default 500 MiB): split into smaller calls. Per-item size limits (video
  200 MiB) fail just that item.
- **`mime_type`** is required for `data` items and inferred from the extension
  for `file_path` items; if inference fails that item errors, so set it for
  unusual extensions.
- **Use a long `expires_in_seconds` (at least 3600) for `vod_*` sources**: VOD
  fetches asynchronously and a default-TTL URL can expire first. It applies to
  every item in the call.
- **The returned `object_key`** feeds `media_presign` and `ark_asset_create`.

### `media_presign`

Mints fresh URLs for 1-100 `object_keys` without re-uploading. Read-only,
foreground. **Only keys you uploaded work**, and each key fails on its own, so
check `failed` and per-key `code`:

| `code` | Meaning and fix |
|---|---|
| `INVALID_KEY` | Malformed key; use it exactly as `media_upload` returned it |
| `NOT_OWNED` | Not uploaded by this caller; re-upload |
| `INTERNAL` | Unexpected server error; retry |
| provider code | TOS/S3 rejected it (object missing, credentials); see `error`, `request_id` |

### Presign-reuse pattern

Presigned URLs expire (default 30 minutes; `TOS_PRESIGN_TTL_SECONDS` /
`S3_PRESIGN_TTL_SECONDS`). When the same references (character sheets, a music
bed) feed many shots, **upload once, then presign per shot**:

1. Upload all references in one `media_upload` call, check `failed`, and store
   each `object_key` in the project's reference registry.
2. Right before each submission, `media_presign` the keys that shot needs, check
   per-key `code`, and submit immediately while the URLs are valid.

## Private asset library (`ark_asset_*`)

Lets Seedance use real people, your own virtual characters, and copyright IP
(Advanced Creation Rights). Operator guide: [Assets](https://byteplus-sa.github.io/ark-mcp/assets/).

### Prerequisites and rules

- **AK/SK are required** (`BYTEPLUS_MODELARK_ACCESS_KEY` +
  `BYTEPLUS_MODELARK_SECRET_KEY`, independent of the API key); without them no
  `ark_asset_*` tool is registered. **`ark_asset_delete` is the eighth tool and
  exists only with `BYTEPLUS_MODELARK_ASSETS_ALLOW_DELETE=true`.**
- **`asset://<id>` references are for Seedance only** (`images`, `videos`,
  `audios`). Seedream and Seed Audio reject them unless the operator set
  `BYTEPLUS_MODELARK_ASSET_REFERENCE_MODE=resolve`, which experimentally swaps in
  the asset's temporary download URL.
- **Only `Active` assets are usable.** Seedance preflights `asset://` references
  and stops before billing when one is `Processing` or `Failed`
  (`asset_not_active`). Unreadable references, such as console-authorized
  real-human or copyright IP assets from another account, do not block.
- **Assets only work within one `project_name`**; keep it consistent.
- In the Seedance prompt, refer to references by position ("Image 1",
  "Video 1"), never by asset ID or name. Image references are verified live with
  Seedance 2.5; video/audio references and Seedance 2.0 are unvalidated.
- Asset calls hold the `modelark-openapi` rate-limit slot **only per provider
  request**, so waits and polling never block a Seedance `asset://` preflight.

### One subject per group

**Never mix people or characters in one group.** Path by subject:

| Subject | Path |
|---|---|
| Fictional character or product | `ark_asset_create(subject=...)` (or `ark_asset_group_ensure`) |
| Real person | `ark_asset_verification_start` -> `ark_asset_verification_result` -> `ark_asset_create(group_id=...)` |
| Copyright IP | Copy the asset ID from the console Copyright Library |

- **AIGC groups** (virtual portraits): `ark_asset_group_ensure(subject=...)`
  returns the one group named exactly that and creates it if absent; it is
  idempotent. `ark_asset_create(subject=...)` does the same while adding assets.
  AIGC assets must not resemble any real person. Several groups with the same
  name fail with `ambiguous_asset_group` (IDs listed): pass `group_id` instead.
- **Subject lookup is serialized within one server process only.** Across
  servers or replicas, pre-create the group and pass its `group_id`. More than
  20 pages of name matches fails with `asset_group_scan_incomplete`.
- **Real people need consent and liveness.** `ark_asset_verification_start`
  returns an `h5_link` (temporary credentials: send it only to that person, never
  verify anyone without consent) and a `verification_token` valid about 30
  minutes. `ark_asset_verification_result` stays `pending` until they pass, then
  returns `verified` with the `LivenessFace` `group_id` (`wait_seconds` polls;
  0 is a single check). A failed attempt invalidates the link: start again. Upload
  only that person's media to that group. `callback_url` must be HTTPS (or set
  `BYTEPLUS_MODELARK_ASSET_VERIFY_CALLBACK_URL`).

### Creating assets (`ark_asset_create`)

- **Sources** are public HTTPS `url`s or `media_upload` `object_key`s. For local
  files, run one `media_upload` call first, check `failed`, then pass each
  `object_key` (a presigned URL is minted automatically). Best portrait set:
  a front-facing close-up plus a full-body shot, portrait orientation.
  `asset_type` is inferred from the extension or key; if it cannot be, the call
  fails and you must set `Image`, `Video`, or `Audio`.
- **One call, one subject, 1-20 sources.** It waits by default
  (`wait_until_active`); read `all_active`, then check each `items[].error` and
  `status`. **Sources fail individually**; `Failed` means preprocessing or
  content review rejected it.
- **`group_created_empty: true`**: this call created the subject's group but every
  source failed. Deleting it with `ark_asset_delete(group_id=..., confirm=true)`
  **works only when delete is enabled**; otherwise leave it and reuse it next time.
- CreateAsset is rate-limited client-side (`BYTEPLUS_MODELARK_ASSET_CREATE_QPM`,
  default 3 per minute), so large batches take longer: prefer the background form.

### Reading and renaming

- Both list tools also read 1-20 items by ID (`group_ids` of any type;
  `asset_ids` as plain IDs or `asset://` refs). `group_type` defaults to `AIGC`;
  use `LivenessFace` for verified people. Assets authorized from another account
  are not listed but are usable by ID.
- **ID lookups exclude the list filters** (`name`, `next_token`, `sort_order`,
  plus `group_ids`/`statuses` for assets); duplicate IDs are de-duplicated.
- **Unreadable IDs do not fail the call.** Each is reported in `errors[]` as
  `{id, code, message}` (for example `NotFound.Asset`); check `errors` before
  assuming every ID was found. `preview_url` is a temporary (~12 h) viewing link,
  not a generation input: pass `asset_uri`.
- `ark_asset_update` renames; `description` works only with `group_id`.

### Deleting (`ark_asset_delete`)

Irreversible, and only available with the flag above. Inspect the exact target
first (`ark_asset_list(asset_ids=[...])`, `ark_asset_group_list(group_ids=[...])`,
or `ark_asset_list(group_ids=[...])` for a group's members).

- Exactly one of `asset_id` / `group_id`, and **`confirm: true`** is mandatory.
- **Deleting a group also deletes its assets.** A non-empty group is refused with
  `asset_group_not_empty` unless `cascade=true` (default `false`); delete the
  assets first, or get the user's agreement to cascade.
- After a timeout or 5xx, read the target again before retrying (ambiguous).
