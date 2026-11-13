# Create-tool reference

Per-product behaviour of the create tools that the tool schemas do not spell out: flows, cross-field rules, gotchas, and recovery. Parameters, ranges and output fields are in each tool's schema (also [API reference](https://byteplus-sa.github.io/ark-mcp/api-reference/)); per-model limits are in [models-and-limits.md](models-and-limits.md); polling, persistence and artifact handling are in [polling-and-artifacts.md](polling-and-artifacts.md); background-job mechanics are in [workflows.md](workflows.md).

**Universal rules for every create tool below:** run it through `ark_job_submit` (or native task augmentation), read the task IDs from the job result, and poll those IDs. **Never resubmit a create tool to poll or to retry an ambiguous failure: every submit is billed and none is idempotent.** Take exact model IDs from `ark_list_models`; `model` accepts exact IDs only.

- [Variations and dry runs](#variations-and-dry-runs)
- [Seedance](#seedance)
- [Seedream](#seedream)
- [Seed Audio](#seed-audio)
- [Seed 3D](#seed-3d-hyper3d-and-hitem3d)
- [OmniHuman](#omnihuman)
- [VOD AI MediaKit](#vod-ai-mediakit)

## Variations and dry runs

**There are no separate variation tools.** Set `variations` on the create tool.

| Tool | `variations` | Seeds | Where results land |
|---|---|---|---|
| `seedance_create_task` | 1-5, each a separate billed task | none | `tasks[]` with `task_id` or `error`; `submitted` / `failed` |
| `seedream_generate_image` | 1-10, one provider call each | base `seed` | `summary` (`VariationSummary`) |
| `seed_audio_generate` | 1-5 | none (Seed Audio has no seed) | `summary` (`VariationSummary`) |

- **Partial failure is normal.** Each variation is independent; 4 of 5 can succeed and the call still returns 4 results plus 1 error. Read every `error` before concluding.
- **No per-variation timeout.** Queue wait never counts; one batch deadline bounds the call. A deadline or storage failure sets `error.phase`: `queued` (`QUEUE_TIMEOUT`, safe to retry), `generating` (may have completed, **do not retry blindly**), `persisting` (billed output not stored; the provider URL may still be in the result).
- **`variation_prompts`** must have exactly `variations` entries and replaces `prompt` (and satisfies "prompt required").
- **Local export:** image and audio variations need an `output_path` directory ending in `/`. Video variations are polled together with **one** `gen_task_get` call over all non-null `task_id`s.
- **`dry_run: true`** (Seedance and Seedream only) runs all validation and returns `preview` (provider request bodies with media URLs reduced to scheme and host, Base64 reduced to its size) plus `estimated_cost_usd`. **Nothing is submitted or billed**; the cost is an estimate, not billing or a provider quote. Seedream adds `price_source`: `catalog` for a fresh cached image rate, otherwise `builtin`. Dry runs finish on the first `ark_job_get`. Remove `dry_run` to run for real.
- **Runtime validation reports everything at once.** Per-model limits are checked from the capability registry before any provider call, and all violations come back in one error ending with `Call ark_list_models(kind=...) for per-model limits.` Fix them together.

## Seedance

Needs `BYTEPLUS_MODELARK_API_KEY`. Video is **asynchronous**: `seedance_create_task` returns `tasks[].task_id`; poll with `gen_task_get` ([polling-and-artifacts.md](polling-and-artifacts.md)). States: `queued -> running -> succeeded | failed | cancelled | expired`.

### Model selection

**One tool covers every Seedance model**: 2.0 (Standard, Fast, Mini), regular 2.5, and 2.5 Flash. `ark_list_models(kind='video')` lists the exact `model_id`s, their limits, and which are bound. Omit `model` for the default (`SEEDANCE_DEFAULT_MODEL`, regular Seedance 2.5 unless changed).

- **2.5**: up to 30 s single pass, including 4K through `resolution="4k"` on the same model; richer references, structured editing and native extension (`omni_reference_task_type`), `mov` output, Draft mode, audio-only input. No extra feature flag or model.
- **2.5 Flash**: select `dreamina-seedance-2-5-flash-261115` on the same tool for
  480p/720p reference/edit/extend generation, with the same reference limits
  and formats but no Draft. It is included when bindings are empty; add it
  explicitly to custom binding lists as `seedance_2_5_flash`. Listing it is
  not an account-activation check. Costs use the static 2.5 fallback, not a
  token-based provider quote.
- **2.0 family**: 4K on Standard, Fast/Mini for speed and cost, 15 s maximum, no Draft, no task types, no `output_format`, audio needs an image or video alongside it.

Family limits (resolutions, durations, reference counts, Draft final resolution): [models-and-limits.md](models-and-limits.md).

### Inputs and media rules

- **At least one of `prompt`, `images`, `videos`, `audios`** is required (except with `draft_task_id`). Text-only is valid text-to-video; audio-only works on regular 2.5 and Flash.
- **Media is URL-only for video.** Every video reference must be an HTTPS URL or `asset://<asset_id>`. Images and audio also accept inline Base64 (size- and MIME-checked), but prefer URLs; local files go through `media_upload` first ([understanding-media-assets.md](understanding-media-assets.md)).
- **Private and link-local hosts are rejected** (SSRF policy); the URL must be publicly fetchable by the provider while the task is queued.
- **`asset://<asset_id>`** references the private asset library and is the only way to use AIGC virtual portraits, verified real people, and copyright IP. The asset must be `Active`. When AK/SK are configured and `SEEDANCE_ASSET_PREFLIGHT` is on, the server checks references before submitting (dry runs included): `Processing` or `Failed` assets fail fast with `asset_not_active`; a not-found lookup does **not** block, because console-authorized and copyright IP assets belong to other accounts.
- **Image roles:** `first_frame`, `last_frame`, `reference_image` (default for bare URLs). Videos and audios have a fixed role.
- **Prompt length:** schema max 32,000 characters; ModelArk recommends staying near 1,000 English words.

### Task types and auto-locked parameters

On regular 2.5 and Flash, `omni_reference_task_type` (`auto`, `reference`, `edit`, `extend`) forces the task type when auto-detection is ambiguous. **Write the prompt to match the type**, otherwise the provider fails the task with `TaskTypeMismatch`.

| Task | Aspect ratio | Duration |
|---|---|---|
| Video editing (`edit`) | Locked to the input video | Locked to the input video (about +/-0.3 s) |
| Video extension (`extend`) | Locked to the input video | Free |
| First or first/last-frame generation | Locked to the first image | Free |
| Text-to-video, standard reference | Free | Free (or `-1` for auto) |

**Server-side rejections** (instead of letting the provider fail with `InvalidParameter.TaskTypeConstraint` after billing a slot):

- `edit` and `extend` need at least one reference video, and `ratio` omitted or `adaptive`.
- `edit` also needs `duration` omitted or `-1`.
- Any request with `first_frame` / `last_frame` images needs `ratio` omitted or `adaptive`.
- 2.0 models reject `omni_reference_task_type` entirely.

### Draft mode (regular 2.5 only)

A cheap 480p preview, then a 1080p final render of the one you like. 4K is supported for ordinary generation, not Draft promotion. Each step is billed separately (the Draft as a normal 480p video). Static video cost previews do not account for resolution or duration.

1. `draft: true` with `resolution` omitted or `480p`. Combine with `variations` for several candidates.
2. Poll with `gen_task_get` until a Draft succeeds (`draft: true` in the result) and review it.
3. Call again with **only** `draft_task_id` (plus optional overrides below). It must be a succeeded Draft task **you own**, at most **7 days old**, and `variations` stays 1 with no `variation_prompts`.

**Reused from the Draft, so omit them (rejected even when identical):** `prompt`, `images`, `videos`, `audios`, `duration`, `ratio`, `generate_audio`, `omni_reference_task_type`. The model is also reused (omit `model`; a different one is rejected), as is the Draft's seed. `resolution` must be omitted or the model's Draft final resolution (the default). Still settable on the final call: `return_last_frame`, `watermark`, `execution_expires_after`, `priority`, `safety_identifier`, `output_format`.

`draft` and `draft_task_id` are mutually exclusive. On a model without Draft support (2.0 or Flash) both are rejected.

```json
{ "prompt": "A cinematic 20-second chase through a night market", "duration": 20, "draft": true, "variations": 3 }
```

```json
{ "draft_task_id": "<succeeded draft task_id>" }
```

### Output handling

- `recommended_poll_after_ms` is the delay before the first `gen_task_get`; it is `null` for dry runs.
- A single task and a variations batch return the same shape; check `failed` and each `tasks[].error` (`retryable`, `ambiguous_completion`, `phase`) before resubmitting only the failed indices.
- `output_format: mov` (regular 2.5 and Flash) is H.264 4:4:4 with PCM audio for post-production; some players cannot play it.
- Provider video URLs expire in about 24 hours; persist from the poller, see [polling-and-artifacts.md](polling-and-artifacts.md).

## Seedream

Needs `BYTEPLUS_MODELARK_API_KEY`. **`seedream_generate_image` is the only Seedream tool**: text-to-image, image-to-image, reference editing, point/box edits, provider batches (`max_images`), parallel `variations`, and dry runs. A foreground direct call is rejected; run it through `ark_job_submit`.

### Prompt and edit rules

- **`prompt` is 1-4000 characters including any markup the tool adds**; with `images` it is the edit instruction. Optional only when `variation_prompts` is set.
- **Point and box edits** target the **first** image and require `images`. Pass structured `point` / `bbox`; **do not write the markup into the prompt**. The tool prepends `Image 1<bbox>x1 y1 x2 y2</bbox>` and/or `Image 1<point>x y</point>` (bbox first when both) to **every** variation prompt, which counts against the 4000 characters.
- Coordinates are normalized, top-left `0,0`, bottom-right `999,999`: `normalized = min(999, round(pixel / dimension * 1000))`.
- Reference limits and `size` / `output_format` sets differ per family; see [models-and-limits.md](models-and-limits.md).

### `max_images` versus `variations`

- **`max_images`** is one provider call returning up to 15 images: one request, one `usage`, results in `artifacts` and `item_errors`. Only on batch-capable families (Lite, 4.x); **Seedream 5.5 and 5.0 Pro do not support it**.
- **`variations`** is separate parallel calls: works on every model, supports `variation_prompts` and per-variation seeds, results in `summary` (`artifacts` and `usage` stay empty).
- **They cannot be combined** (`variations > 1` with `max_images > 1` is rejected). On 5.5 and Pro, use `variations`.

### Seeds

A fixed `seed` reproduces request settings, not guaranteed identical pixels. Single-call `-1` or omitted seed remains provider randomness, not a recovered actual seed. With `variations > 1`, `seed` is the **base seed**:

| `seed` | Per-variation seeds |
|---|---|
| omitted | Provider randomizes each; seed **not recorded** in `summary` |
| `-1` | Client picks a random seed per variation; **recorded** |
| `N` | `N, N+1, N+2, ...` wrapped modulo 2147483648; recorded |

### Transparent background

`background="transparent"` requires `output_format` omitted or `png`.
Seedream 5.5 (default) accepts text-only prompts and reference images
without alpha. It defaults to PNG even for ordinary generation.
`prompt_optimization="standard"` is accepted (provider default); `fast` is rejected.
`background="auto"` is the 5.5 default and follows the prompt; JPEG is always opaque.

Use 5.5 size tiers `1K`, `1.5K`, `2K` (default), or positive `WIDTHxHEIGHT`
with 921600-4624220 pixels and width/height ratio 1/16-16, inclusive.
Optional `safety_identifier` on 5.5/Pro must be a stable hashed user ID,
1-64 non-space printable ASCII characters. Previews and logs redact it.
`generations` preserves per-call usage, identifier echo, and provider-reported
image size, format and actual background, with image/variation indices and
matching artifact IDs. Missing values stay null; successful provider metadata
survives partial variation failures. Decomposition/OCR inputs are rejected.

On Seedream 5.0 Pro, transparency **edits exactly one PNG input that already has
transparent pixels**. It does not remove an opaque background. Non-PNG Base64
input is rejected locally; an opaque PNG fails at the provider with HTTP 400.
The following example selects Pro, which must be bound by the operator:

```json
{
  "model": "dola-seedream-5-0-pro-260628",
  "prompt": "Turn the circle into a glossy ceramic button, keep the background transparent",
  "images": [{ "kind": "url", "url": "https://cdn.example.com/circle-rgba.png" }],
  "background": "transparent",
  "output_format": "png"
}
```

### Persistence and local export

- `persist=true` (default) stores each image as a durable artifact. **A storage failure never drops a billed image**: the result carries the 24-hour provider URL (id `provider-url`) with `persistence_error`, or, for Base64 output, `fallback_data` inline up to `ARTIFACT_INLINE_FALLBACK_MAX_BYTES`. Check each artifact's `persistence_error` and download from `source_url`/`uri` before it expires. Details: [polling-and-artifacts.md](polling-and-artifacts.md).
- `persist=false` returns provider-URL references only.
- Explicit `response_format="b64_json"` with `persist=false` is rejected before
  submission, even for dry runs. Missing output yields `NO_OUTPUT`; unexpected
  Base64-only delivery without persistence yields `NO_DELIVERABLE_OUTPUT`.
- `generations` includes single/variation request IDs, submitted seeds,
  final-prompt hashes and allowlisted options excluding private media and
  identifiers. `images[].inspection` independently measures decoded format,
  dimensions and actual alpha: `verified`, `mismatch`, `invalid`, `unavailable`,
  or null for URL-only delivery. It preserves artifacts, never overwrites
  provider reports, and does not establish visual quality or trigger paid retries.
- Use the bounded [review/edit workflow](workflows.md#seedream-generate-review-edit)
  before accepting text, counts or geometry; publishing previews are a separate check.
- `output_path` (stdio local export) needs `persist=true` and **must be a directory ending in `/`** when `variations > 1` or `max_images > 1`.
- `asset://` references are **not** accepted by Seedream natively: rejected unless `BYTEPLUS_MODELARK_ASSET_REFERENCE_MODE=resolve` (experimental; sends the asset's temporary download URL and only works for assets this account can look up).
- Dry-run cost covers `variations x max_images` images.

## Seed Audio

Needs `BYTEPLUS_SEED_SPEECH_API_KEY`. `seed_audio_generate` produces a full-scene clip (speech, ambience, music, effects) from a text prompt; **run it through `ark_job_submit`**. The provider URL expires after 2 hours, so keep `persist=true` (default).

- **References: one kind only.** `audio_references` (up to 3: `speaker` ID, `url`, or `base64`) steer voice or scene; `image_reference` gives visual context. **Passing both is rejected.**
- **Base64 reference audio** is checked against the media limit (30 s by default for WAV) and the audio size cap before submission; prefer a URL for longer material.
- **`asset://` references** are rejected by default and follow `BYTEPLUS_MODELARK_ASSET_REFERENCE_MODE` like Seedream (see above); only Seedance uses them natively.
- **`text_prompt` is 1-3000 characters**; a line such as `Max duration: 20 seconds` in the prompt is only used for the cost estimate, not enforced.
- **Subtitles** (`output.subtitle`, `subtitle_type` `utterance` or `word`) are returned on the single-call result only.
- **Variations:** no seed exists, so variations differ only by sampling. With `variations > 1`, `artifact`, `duration_seconds`, `billing_duration_seconds` and `subtitle` are **null**; everything is in `summary` (`total`, `succeeded`, `failed`, per-variation `artifact` or `error`). `output_path` must then be a directory ending in `/`.
- `billing_duration_seconds` can differ from the actual `duration_seconds`.

## Seed 3D (Hyper3D and Hitem3d)

Needs `BYTEPLUS_MODELARK_3D_ENABLED=true` and the ModelArk key. **Check availability first**: if `ark_list_models` reports `seed3d` disabled or the create tools are absent, report 3D unavailable; configuration docs alone prove nothing about the running server.

**Choosing:** `hyper3d_create_task` for text-to-3D or image-to-3D (prompt and/or up to 5 images; seed, PBR/Shaded/All/None materials, Raw/Quad meshes, HD textures, T-pose, bounding box). `hitem3d_create_task` for image-to-3D only (1-4 images; resolution, face count, geometry-only versus textured, multi-view bitmap). Both return `task_id` with `status="queued"`; **both are polled, cancelled and deleted with `gen_task_get` / `gen_task_cancel_or_delete`**, same lifecycle as Seedance.

- A model ID from the other family is rejected with a pointer to the right tool. `model` comes from `ark_list_models(kind='3d')`; omit for the configured default.
- **Hyper3D:** `prompt` is English, max 400 characters, and required when no images are given. `subdivision_level` is ignored when `quality_override` is set. `quality_override` ranges differ by mesh mode (Raw 500-1M, Quad 1000-200K). `file_format` defaults to `glb`.
- **Hitem3d:** `multi_images_bit` marks which views are present in front/back/left/right order and may contain only `0` and `1` (`"1010"` = front + left). `file_format` defaults to `obj`; `request_type` 3 (default) is geometry plus texture.
- Input images accept URLs or Base64; no `asset://`.
- The finished `model_file` output is a **zip package** whose provider URL lasts about 24 hours; persist it from `gen_task_get` with `persist_output=true` in the background ([polling-and-artifacts.md](polling-and-artifacts.md)).

### 3D delivery contract

**Provider success delivers a generated package, not a Blender-ready or approved asset.** Before handing a result to a DCC workflow:

- Retain the immutable package and record provider family and model, request and reference hashes, the Ark job ID and the provider task ID as separate values, artifact ID, byte size, SHA-256, requested format, material/topology settings, usage, and source URL expiry.
- Prefer GLB for a first Blender handoff (mesh, hierarchy, materials and textures travel together). Extract into a new bounded directory, reject absolute paths and parent traversal, and never overwrite the provider archive.
- Import into a quarantine collection, then normalize units, scale, axes, origin, transforms, geometry, normals, UVs, materials, textures and rig readiness. Record the normalized working-copy hash and viewport review separately from the provider package.
- **A 3D asset supplies structure and appearance, not motion.** It becomes Seedance motion authority only after an animated video render is deliberately selected and bound for a supported video-reference mode. Keep 3D generation, Blender normalization, previz rendering and Seedance generation as distinct operations with their own task IDs, costs, statuses and review evidence.

## OmniHuman

Needs `BYTEPLUS_OMNIHUMAN_ENABLED=true` and `BYTEPLUS_CV_API_KEY` (a Vision AI key, separate from the ModelArk key); disabled by default. One portrait image plus one audio clip (plus an optional prompt) becomes a talking or performing avatar video.

- **`omnihuman_create_task` submits one task and is never retried automatically.** It returns `status="accepted"` and `task_id`; poll with `omnihuman_get_task` (cancel with `omnihuman_cancel_task`). Its poller defaults to persisting the finished video, because the provider URL lasts only about **one hour**; see [polling-and-artifacts.md](polling-and-artifacts.md).
- **Sources:** `image` and `audio` are public HTTPS URLs or `seed-media://artifacts/<id>`. Image limits: common formats (jpeg, png, webp, bmp, tiff, gif, heic, heif), under 30 MB, aspect 0.4-2.5, each side 300-6000 px. Audio: wav or mp3, under 15 MB, 4-300 s. **The video length follows the audio.**
- **`seed-media://` inputs need `ARTIFACT_BACKEND=object_storage`** so the server can presign them (1-hour URL). Otherwise `media_upload` the file and pass the presigned URL. The artifact's media type, MIME type and size are checked and reported as safe errors.
- `prompt` is optional scene, motion and camera guidance (max 2000 characters; zh, en, ja, ko, es-MX, id). `watermark` defaults to `true`.

## VOD AI MediaKit

Needs `BYTEPLUS_VOD_MEDIAKIT_API_KEY`. Five submit tools (`vod_enhance_video`, `vod_transcode_video`, `vod_add_subtitles`, `vod_remove_subtitles`, `vod_separate_audio`) share one poller, **`vod_get_task`**.

### Submit-then-poll contract

- **Read `task_id` and `operation` from the submit result and pass both to `vod_get_task`.** The echoed `operation` is `enhance`, `transcode`, `add_subtitles`, `remove_subtitles` or `separate_audio`; a task cannot be read with a different `operation`.
- **Every submit is a non-idempotent, open-world mutation and is never retried automatically.** A timeout or 5xx may mean the provider already started work (ambiguous completion). Do not resubmit blindly.
- `vod_add_subtitles` and `vod_remove_subtitles` accept a **`client_token`** (1-64 printable ASCII characters): reuse the same token to reconcile an ambiguous submission instead of creating a duplicate. The other three submit tools have no token, so confirm with the user before re-submitting after an ambiguous failure.
- `vod_get_task` defaults to `persist_output=false` (foreground poll). `persist_output=true` copies finished outputs into the artifact store once per task and requires background execution; provider URLs are preserved in the result even when persistence is skipped or fails. See [polling-and-artifacts.md](polling-and-artifacts.md).
- Submit results are `status="accepted"` with `recommended_poll_after_ms` (a heuristic).

### Source URL rules

**All sources must be public HTTPS URLs; private and link-local hosts are rejected.** The provider downloads the source asynchronously after submission, so **the URL must stay fetchable until the provider has it**. A presigned URL can expire first (default TTL 1800 s, configurable 60-604800 s via `TOS_PRESIGN_TTL_SECONDS` / `S3_PRESIGN_TTL_SECONDS`) and fail the task. For local files, upload with `media_upload` and `expires_in_seconds` of about 3600, check `failed` and `items[].error`, and pass the item's `url`; or use a stable public URL.

### Per-operation notes

- **`vod_enhance_video`**: tiers `fast` (latency, input up to 2K, output up to 4K), `standard` (balanced; honors `scene`), `professional` (highest quality and cost, the default). `resolution` and `resolution_limit` are mutually exclusive (default `4k`). `scene` applies only to `standard`; `enhance_style` is not supported by `fast`; `fps` above the source interpolates (stay within 4x), `null` keeps the source rate. **The result may be `accepted` (poll it) or `succeeded` directly** with `source_url`; `persistence` (`not_applicable`, `not_requested`, `persisted`, `failed`) reports the best-effort durable copy, which is capped at 200 MiB, so **retain `source_url` even when the copy fails**. `estimated_cost_usd` is always null.
- **`vod_transcode_video`**: the defaults reproduce a portrait-to-720x720 letterbox profile (h264, CRF 25, `scale_type=2`). Set `video.scale_type`/`scale_mode` explicitly for other targets; width/height apply only with `scale_type=2`, short/long side only with `scale_type=1`. `fps_mode` matters only when `fps` is set; HDR is converted to SDR unless `is_hdr_to_sdr=false`.
- **`vod_add_subtitles`**: burns an SRT/VTT/ASS file (`subtitle_url`, wins if both are given) or inline cues into the video; at least one is required. Cues need nonblank text, a nonnegative `start_time` and a later `end_time`. Output is an MP4.
- **`vod_remove_subtitles`**: default `subtitle` mode erases recognized dialogue subtitles; **`text` mode is broader and also erases titles, labels and watermarks**. Normalized rectangles, time segments and OCR thresholds narrow the work. `project` and `model_version` are legacy extensions, omitted by default.
- **`vod_separate_audio`**: exactly one of `audio_url` or `video_url`. `scene` `Audio` / `Music` yields voice plus background; `Drama` / `Narrate` yields voice, music and sfx. Typically tens of seconds but can take minutes: **keep polling until a terminal state** rather than giving up on the first `processing`. A provider `failed` with `AbilityProcessingError` or `InternalError` has been transient in practice: re-submit the same source before concluding the input is bad. `output_path` for the poller must be a directory ending in `/` (several tracks).
