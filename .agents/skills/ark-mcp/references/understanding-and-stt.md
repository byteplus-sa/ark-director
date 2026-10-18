# Understanding and speech-to-text

Load this when you analyse images or video (`seed_understand`), analyse audio
(`seed_audio_understand`), or need a word-timed transcript (`speech_to_text`).

All three tools require background execution through `ark_job_submit`; poll at
the server-recommended two-second interval. Do not call them in the foreground
or shorten the prompt to dodge a client timeout.

## Which tool

| Need | Tool |
|---|---|
| OCR, scene or motion analysis, video review, visual reasoning sub-agent | `seed_understand` |
| Summary, translation, speaker or emotion notes, Q&A about what is heard | `seed_audio_understand` |
| Exact words with word-level timestamps and speakers | `speech_to_text` (the authority for words) |

`seed_audio_understand` cannot judge accent or pronunciation reliably and can
mislabel music; accent verdicts need a native listener.

## `seed_understand`

Requires `BYTEPLUS_MODELARK_API_KEY`; scope `understanding:read`. Default model
`dola-seed-2-1-turbo-260628` (Seed 2.1 Turbo). `dola-seed-evolving` (Pro tier)
is a recognized built-in: set `SEED_UNDERSTANDING_DEFAULT_MODEL` to opt in.
Other IDs need `SEED_UNDERSTANDING_MODEL_BINDINGS`.

Deep thinking is **always on** (depth via `reasoning_effort`); only the final
answer is returned. Do not pass `thinking` (deprecated no-op) and do not look
for `reasoning_content` (removed).

**Video inputs are HTTPS URLs only.** Prefer a public HTTPS URL the provider
can already fetch as video. For local files, `media_upload` first. For
page/platform links (video sharing sites, social posts), auth-gated URLs, or
any link that is not a usable video input, download locally, then upload. Do
not analyse cited footage from transcripts or article text when the task is
visual or motion grammar.

| Parameter | Type | Notes |
|---|---|---|
| `prompt` | `str` | 1–32,000 characters; required |
| `images` | list | Up to 32 (URL or Base64) |
| `videos` | list | Up to 32 (URL only); images + videos ≤ 32 parts |
| `system` | `str` | Optional, ≤ 32,000 characters |
| `model` | `str` | Override the configured model |
| `reasoning_effort` | `low` \| `medium` \| `high` | Default `medium` |
| `response_format` | object | `{type: text \| json_object \| json_schema, json_schema?: {name, schema, description?, strict=true}}`; provider-enforced |
| `json_retry` | `int` | 0–2 extra **billed** attempts on invalid JSON; skipped when `finish_reason="length"` |
| `save_to` | `str` | Absolute path inside an output root (stdio); validated before billing |
| `overwrite` | `bool` | Default `false` |
| `return_content` | `full` \| `summary` \| `none` | Inline everything, the first 2,000 characters, or nothing |
| `temperature`, `top_p`, `repetition_penalty` | `float` | 0–2, 0–1, 0–2 |
| `max_tokens` | `int` | 1–32768, **including thinking tokens** |

Returns `model`, `completion_id`, `choices`, `usage` (with `reasoning_tokens`
when reported, summed over attempts), `attempts`, `saved_path`,
`saved_bytes`, `request_id`. Each choice has `content`, `content_chars`,
`content_truncated`, `parsed` (returned even with `summary`/`none`),
`schema_violation`, and `finish_reason`. If `save_to` fails after billing, the
call still succeeds with `saved_path=null` and the answer inline.

Chat timeouts return `TIMEOUT` (`retryable=true`,
`ambiguous_completion=false`) but the server does not retry them, because a
second thinking run doubles cost; raise `SEED_UNDERSTANDING_TIMEOUT_MS` for
long analyses. 429/5xx are retried.

Inside `ark_job_submit`, `save_to` can fail with "session is not available".
Omit it and read the answer from `result.structured_content`; see
[Background-job output](background-job-output.md).

### Reasoning depth

| `reasoning_effort` | Use |
|---|---|
| `low` | Quick checks, simple OCR, basic descriptions |
| `medium` | Balanced analysis, moderate comparisons |
| `high` | Deep video review, complex reasoning |

### Prompting tips

- Enforce structure with `response_format` `json_schema` (pass a template's
  schema verbatim) rather than asking for JSON in prose; set `json_retry: 1`.
- Keep large answers out of context with `return_content: "none"` or
  `"summary"` and read `choices[0].parsed`; check `schema_violation` first.
- Put role and constraints in `system`.
- Split complex work into focused calls (extract, then analyse, then
  summarize).
- Ask for timestamps when you need specific video moments; name expected
  languages for multilingual OCR.

### Example: schema-enforced video review

```json
{"tool_name": "seed_understand",
 "arguments": {"input": {
   "prompt": "Review this ad against the template. Return the beats with start/end seconds.",
   "videos": [{"kind": "url", "url": "https://cdn.example.com/ad.mp4"}],
   "reasoning_effort": "high",
   "response_format": {"type": "json_schema", "json_schema": {
     "name": "ad_review",
     "schema": {"type": "object", "required": ["beats"], "properties": {
       "beats": {"type": "array", "items": {"type": "object",
         "required": ["label", "start", "end"],
         "properties": {"label": {"type": "string"},
                        "start": {"type": "number"},
                        "end": {"type": "number"}}}}}}}},
   "json_retry": 1,
   "return_content": "summary"}}}
```

Image comparison as a reasoning sub-agent:

```json
{"prompt": "Compare the UI in screenshot 1 with the design spec in screenshot 2. List all differences in spacing, color, and typography.",
 "images": [{"kind": "url", "url": "https://cdn.example.com/screenshot.png"},
            {"kind": "url", "url": "https://cdn.example.com/design-spec.png"}],
 "system": "You are a meticulous UI reviewer. Be specific about pixel-level differences.",
 "reasoning_effort": "low"}
```

Limitations: no video Base64, no streaming, no artifact persistence (text
only; use `save_to`), no reasoning trace.

## `seed_audio_understand`

Requires `BYTEPLUS_MODELARK_API_KEY`; scope `understanding:read`. The model is
set server-side by `SEED_AUDIO_UNDERSTANDING_MODEL` (default
`seed-2-0-lite-260428`, an interim choice); there is no per-call `model`
argument and no capability pre-validation.

| Parameter | Notes |
|---|---|
| `prompt` | 1–32,000 characters |
| `audios` | 1–8 clips, sent in order |
| `system`, `reasoning_effort`, `response_format`, `json_retry`, `save_to`, `overwrite`, `return_content`, `temperature`, `max_tokens`, `top_p`, `repetition_penalty` | Same as `seed_understand` |

Audio inputs:

- `{"kind": "url", "url": "https://..."}` (preferred; `media_upload` local
  files first).
- `{"kind": "base64", "data": "<raw base64>", "mime_type": "audio/wav"}`: at
  most 10 MB decoded, no `data:` prefix; `mime_type` is required and must be
  `audio/wav`, `audio/mpeg`, `audio/flac`, `audio/aac`, or `audio/mp4`.
  Base64 Ogg/Opus/PCM is rejected; use a URL.

With the default model, `json_schema` is enforced but `json_object` is not.

```json
{"prompt": "Transcribe the speech and describe the speaker's emotion.",
 "audios": [{"kind": "url", "url": "https://cdn.example.com/clip.mp3"}],
 "reasoning_effort": "low",
 "response_format": {"type": "json_schema", "json_schema": {
   "name": "speech_analysis",
   "schema": {"type": "object", "additionalProperties": false,
              "required": ["transcript", "emotion"],
              "properties": {"transcript": {"type": "string"},
                             "emotion": {"type": "string"}}}}}}
```

## `speech_to_text`

Requires `BYTEPLUS_SEED_SPEECH_API_KEY`; scope `seed:asr:transcribe`. Seed
Speech ASR runs inside the background job: the tool submits, polls internally
(capped by `SEED_SPEECH_ASR_POLL_MAX_SECONDS`, default 600 s), and returns the
full transcript. There is no separate provider task ID. A timeout yields no
partial result.

`audio` takes exactly one of:

| Field | Notes |
|---|---|
| `audio_file_path` | Absolute local path; stdio only. **Preferred.** |
| `audio_data` | Base64 bytes |
| `audio_url` | HTTPS URL |
| `audio_format` | Required: `wav`, `mp3`, `ogg`, `raw`, `flac` |

Presigned object-storage URLs (S3/TOS) are rejected as an untrusted host.
Pass a local file path. Extract a clip's audio first (for example 16 kHz mono
16-bit WAV with FFmpeg).

`options`: `language` (BCP-47, default `en-US`), `enable_punc`, `enable_itn`.

```json
{"tool_name": "speech_to_text",
 "arguments": {"input": {
   "audio": {"audio_file_path": "/abs/path/clip.wav", "audio_format": "wav"},
   "options": {"language": "en-US", "enable_punc": true}}}}
```

Returns `result` (`text`, `utterances` / `words` with word-level timestamps
and speaker labels, `duration_ms`) and optional `log_id`. Text only; nothing to persist.

**Error `20000003` (silent audio).** ASR state comes in `X-Api-Status-Code`:
`20000000` success, `20000001` / `20000002` processing, `20000003` terminal
"no speech detected" (`retryable=false`). Check that the audio contains speech
and matches `audio_format`; for `wav`/`raw` the gateway assumes 16 kHz, 16-bit,
mono PCM, and a mismatch decodes to silence. Resubmit corrected audio.
