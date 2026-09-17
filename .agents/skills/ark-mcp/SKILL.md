---
name: ark-mcp
description: Guide for using the Ark Seed Multimodal MCP server to generate or edit images, audio, video, and 3D models (including Seedance 2.5, Hyper3D, Hitem3d, BytePlus VOD AI MediaKit enhancement, transcoding, subtitle burn-in/removal, and voice/background audio separation), understand images and videos through Seed 2.1, transcribe speech to text, manage native or ordinary-tool background jobs, upload reference media, and fetch persisted artifacts. Use when Codex, Cursor, or another client rejects task-augmented execution and must route the same work through ark_job_capabilities, ark_job_submit, ark_job_get, and ark_job_cancel.
---

# Ark Seed Multimodal MCP Server

The Ark Seed MCP server exposes BytePlus multimodal generation through a typed,
safe MCP tool surface. It wraps multiple BytePlus AI product families behind
one server, including products served through ModelArk:

- **Seedream** — image generation and editing (text-to-image, reference-based
  editing, batch generation).
- **Seed Audio** — full-scene audio generation with voice cloning, subtitles,
  and watermarking.
- **Seedance** — asynchronous video generation with task-based lifecycle
  (create, poll, list, cancel/delete). Supports two model generations: 2.5
  (default, 30s, 30/10/10 refs, 480p/720p/1080p) and 2.0 (legacy, 15s, 9/3/3
  refs, 480p–4K, Fast/Mini variants).
- **Seed 3D** — asynchronous 3D model generation through ModelArk. Hyper3D
  (text-to-3D and image-to-3D, up to 5 images, GLB/OBJ/USDZ/FBX/STL output)
  and Hitem3d (image-to-3D only, 1–4 images, OBJ/GLB/STL/FBX/USDZ output).
  Gated by `BYTEPLUS_MODELARK_3D_ENABLED`; disabled by default.
- **Seed 2.1 Understanding** — multimodal video/image understanding and
  reasoning through ModelArk Chat Completions; supports deep-thinking mode.
  Use for OCR, scene analysis, content review, and as a visual reasoning
  sub-agent.
- **Speech-to-Text** — background audio transcription via Seed Speech ASR;
  retrieve the completed transcript from the native or compatibility result.
- **VOD AI MediaKit** — asynchronous video enhancement using the exact
  common/professional/4K/high/24-fps profile with task polling and download,
  asynchronous video transcoding
  (codec, container, resolution, bitrate, frame rate) via a submit-then-poll
  tool pair, subtitle burn-in and precision subtitle/text erasure via two
  submit-then-poll pairs, and voice + background (or voice + music + sfx)
  audio separation via a submit-then-poll tool pair.
- **Artifacts** — durable media access after provider URLs expire.
- **Object storage upload** — presigned URL generation for URL-only media
  workflows such as Seedance video references.

The server is built on FastMCP v4 and runs locally via `stdio` or as a
deployable Streamable HTTP service. Generated media is persisted to a local
artifact store with stable `seed-media://` resource URIs that survive provider
URL expiry (2 hours for audio, 24 hours for ModelArk image/video/3D and MediaKit
outputs). MediaKit durable copies are best-effort.

## When To Use

Invoke this skill when the user wants to:

- generate or edit an image;
- generate audio, voice-clone from references, or request several variations;
- create, poll, list, cancel, or delete Seedance video tasks (Seedance 2.0 and 2.5);
- create, poll, list, cancel, or delete Hyper3D and Hitem3d 3D generation tasks (requires the 3D feature flag);
- understand images or videos (OCR, scene analysis, content review), or use a
  multimodal reasoning sub-agent;
- transcribe audio or video into timestamped, speaker-diarized text;
- enhance a public HTTPS video with the supported VOD AI MediaKit profile;
- transcode a public HTTPS video (codec, container, resolution, bitrate, frame
  rate) with the VOD AI MediaKit submit-then-poll tool pair;
- burn an SRT/VTT/ASS file or inline timed subtitle cues into a public HTTPS
  video, or remove hardcoded subtitles/on-screen text with MediaKit;
- separate voice from background audio (or voice + music + sfx) for a public
  HTTPS audio or video URL using the VOD AI MediaKit tool pair;
- fetch a previously persisted artifact by ID;
- locate or copy a previously persisted artifact to a local path without
  streaming Base64 through the context window;
- upload local or Base64 media to object storage (TOS or S3) to obtain a
  presigned HTTPS URL;
- verify which products are configured on the running server.

## Registration Model

Do not assume a fixed tool count. Registration is conditional on environment
variables. Tools for a product appear only when its API key is set; the server
gracefully degrades to whatever is configured.

### Always registered

- `seed_media_get_artifact`
- `seed_media_export_artifact`
- `ark_job_capabilities`
- `ark_job_submit`
- `ark_job_get`
- `ark_job_cancel`
- `seed-health://status` resource

### Requires `BYTEPLUS_SEED_SPEECH_API_KEY`

- `seed_audio_generate`
- `seed_audio_generate_variations`
- `speech_to_text`

### Requires `BYTEPLUS_VOD_MEDIAKIT_API_KEY`

- `vod_enhance_video`
- `vod_get_enhancement_task`
- `vod_transcode_video`
- `vod_get_transcode_task`
- `vod_add_subtitles`
- `vod_get_subtitle_addition_task`
- `vod_remove_subtitles`
- `vod_get_subtitle_removal_task`
- `vod_separate_audio`
- `vod_get_audio_separation`

### Requires `BYTEPLUS_MODELARK_API_KEY`

- `seedream_generate_image`
- `seedream_edit_image`
- `seedream_generate_image_variations`
- `seedance_create_task`
- `seedance_create_task_variations`
- `seedance_get_task`               # shared: retrieves both 2.0 and 2.5 tasks
- `seedance_list_tasks`             # shared: lists both 2.0 and 2.5 tasks
- `seedance_cancel_or_delete_task`  # shared: acts on both 2.0 and 2.5 tasks
- `seedance_2_5_create_task`
- `seedance_2_5_create_task_variations`
- `seed_understand`

### Requires `BYTEPLUS_MODELARK_3D_ENABLED=true` (and `BYTEPLUS_MODELARK_API_KEY`)

- `hyper3d_create_task`
- `hyper3d_get_task`
- `hyper3d_list_tasks`
- `hyper3d_cancel_or_delete_task`
- `hitem3d_create_task`
- `hitem3d_get_task`
- `hitem3d_list_tasks`
- `hitem3d_cancel_or_delete_task`

3D generation is **disabled by default**; it reuses the ModelArk API key and
base URL but is gated by its own feature flag so it stays off unless
explicitly enabled.

### Requires object storage credentials (TOS or S3)

- `media_upload`
- `media_presign`
- `media_presign_batch`

### Background Task Execution

Native task execution uses MCP `2026-07-28` and the
`io.modelcontextprotocol/tasks` extension. FastMCP 4.0.x is tested; a desktop
client discovering tools does not by itself prove native task execution support.

The following long-running calls require background execution. Their direct
tool contracts advertise MCP task augmentation as required with a two-second
polling interval:

- `media_upload`
- `seed_audio_generate`
- `seed_audio_generate_variations`
- `speech_to_text`
- `seedream_generate_image`
- `seedream_edit_image`
- `seedream_generate_image_variations`
- `seedance_create_task`
- `seedance_create_task_variations`
- `seedance_2_5_create_task`
- `seedance_2_5_create_task_variations`
- `hyper3d_create_task`
- `hitem3d_create_task`
- `seed_understand`
- `vod_enhance_video`
- `vod_transcode_video`
- `vod_separate_audio`
- `vod_add_subtitles`
- `vod_remove_subtitles`

On a task-capable client, call them with MCP task metadata, retain the returned
MCP task ID, and poll `tasks/get` until terminal. Foreground direct calls are
rejected before the provider is contacted. For Seedance, Seed 3D, and MediaKit
create/submit tools, the returned tool result contains the provider task ID to
poll with the corresponding get tool.

The Seedance, Seed 3D, and MediaKit get tools support optional background
execution. Use foreground calls with `persist_output=false` for quick status
polling; once a task succeeds, run the get tool in the background with
`persist_output=true` so completed-media download and persistence cannot exhaust
the client deadline. List, presign, artifact-read, and cancel/delete tools
remain foreground operations.

Clients that reject task augmentation, including affected Codex or Cursor
transports, must use the ordinary compatibility tools. This still runs the
selected tool in the same background worker:

1. Call `ark_job_capabilities` and select a listed target.
2. Call `ark_job_submit` with `{"input": {"tool_name": name,
   "arguments": original_arguments}}`; `original_arguments` is normally
   `{"input": {...}}` for the selected target.
3. Retain the returned Ark `job_id` and poll `ark_job_get` no faster than
   `poll_after_ms`.
4. At terminal status, read the original tool result from `result`; its
   `structured_content` contains any Seedance, Seed 3D, or VOD provider task ID.
5. Call `ark_job_cancel` only when cooperative local cancellation is intended.

In the rest of this skill, **run in the background** means either a native
task-augmented call or `ark_job_submit`, depending on client capability.
**Background result** means the terminal `tasks/get` response on the native
path or the original tool result under terminal `ark_job_get.result` on the
compatibility path. Use `result.structured_content` to read the typed payload
on the compatibility path.

Never confuse the Ark job ID with a provider task ID, and never resubmit merely
because a submit response was lost. Retry a direct required-tool call through
`ark_job_submit` only after the explicit unsupported-task-capability rejection,
which occurs before provider execution. Do not retry after a timeout,
disconnect, or ambiguous provider error. `ark_job_capabilities` is filtered by
configured providers and the caller's scopes. Unknown or unauthorized targets
must be treated as unavailable.

Native MCP task and ordinary Ark job operations enforce the same configured
tenant and principal ownership as provider tasks. Required-task execution is
claimed once in the runtime database: an interrupted task cannot silently
replay paid work. Retain the local MCP task or Ark job ID plus any provider ID,
and reconcile ambiguous provider outcomes before submitting again. The smoke
scripts save provider IDs before polling.

JWT-authenticated Redis tasks require `FASTMCP_TASKS_ENCRYPTION_KEY`; keep the
runtime database, queue and encryption key together. Redis does not remove the
single-replica limitation. Snapshot encryption protects stored auth context;
backend access controls must also protect task arguments and results. See the
repository deployment and security documentation for recovery constraints.

---

## Quick Start

### Prerequisites

- Python 3.12+
- `uv` package manager
- BytePlus API keys for the products you intend to use

### Environment Variables

Copy `.env.example` to `.env` and configure at minimum:

```bash
BYTEPLUS_MODELARK_API_KEY=your-modelark-key   # required for Seedream + Seedance
BYTEPLUS_SEED_SPEECH_API_KEY=your-speech-key  # required for Seed Audio + Speech-to-Text
BYTEPLUS_VOD_MEDIAKIT_API_KEY=your-mediakit-key # required for VOD enhancement, transcoding, and audio separation
```

Optional object storage upload support (TOS default, S3 alternative):

```bash
# TOS backend (default)
TOS_ACCESS_KEY=your-ak
TOS_SECRET_KEY=your-sk
TOS_BUCKET=your-private-bucket

# S3 backend
S3_ACCESS_KEY=your-ak
S3_SECRET_KEY=your-sk
S3_BUCKET=your-private-bucket
OBJECT_STORAGE_BACKEND=s3
```

### Running

```bash
uv run python -m ark_mcp          # stdio transport (default, for local MCP clients)
MCP_TRANSPORT=http uv run python -m ark_mcp  # Streamable HTTP on 127.0.0.1:3000
```

Verify with the `seed-health://status` resource or the `/health`, `/ready`, or
`/metrics` HTTP endpoints.

---

## Tool Reference

All tools are Pydantic-validated and return structured outputs. Below is the
complete reference organized by product.

### Artifact Access

#### `seed_media_get_artifact`

Retrieve a persisted media artifact by its UUID as inline Base64 content. Use
when the client needs the artifact data directly rather than reading the
resource URI. Read-only, idempotent, ownership-checked. Requires
`artifacts:read` scope in JWT mode.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `artifact_id` | `str` | Yes | Artifact UUID from a previous generation call |

Returns `SeedMediaGetArtifactOutput` with `artifact_id`, `media_type`,
`mime_type`, `sha256`, `bytes`, optional `expires_at`, and Base64 `data`.

#### `seed_media_export_artifact`

Locate or copy a persisted artifact on the local filesystem. Returns the
absolute on-disk path instead of streaming Base64 through the context window.
Stdio transport only — the client and server must share a filesystem. Requires
`artifacts:read` scope in JWT mode.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `artifact_id` | `str` | Yes | Artifact UUID from a previous generation call |
| `destination_path` | `str` | No | Absolute path where the server writes an atomic copy; omit to return the canonical store path |

Returns `SeedMediaExportArtifactOutput` with `artifact_id`, `path`,
`media_type`, `mime_type`, `bytes`, `sha256`, and `copied`. `copied=false`
means `path` is the canonical store location (filesystem backend); `copied=true`
means the artifact was copied to `destination_path`.

---

### VOD AI MediaKit

Requires `BYTEPLUS_VOD_MEDIAKIT_API_KEY`. Auth scopes: `vod:enhance`,
`vod:transcode`, `vod:subtitle:add`, `vod:subtitle:remove`, `vod:extract`,
and `vod:read`.

#### `vod_enhance_video`

Enhance a public HTTPS video using the exact currently supported profile. The
operation is asynchronous, mutating, non-idempotent, and open-world. Do
not retry it automatically: a timeout may be ambiguous after provider work has
started. Run it in the background, then pass the provider `task_id` from its
background result to `vod_get_enhancement_task`.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `video_url` | URL | Yes | Public HTTPS source; private/link-local targets rejected |
| `scene` | `"common"` | No | Fixed current scene profile |
| `tool_version` | `"professional"` | No | Fixed current enhancement profile |
| `resolution` | `"4k"` | No | Fixed current output resolution |
| `bitrate_level` | `"high"` | No | Fixed current bitrate profile |
| `fps` | `24` | No | Fixed current frame rate |
| `project` | string | No | Defaults to `default`; sent upstream as `Project` |
| `input_duration_seconds` | number | No | Reserved; no price estimate is currently produced |
| `persist` | boolean | No | Best-effort durable artifact copy; default `true` |

The verified response is `status="accepted"` inside the background result. Use
the provider `task_id` from that result and poll that exact ID with
`vod_get_enhancement_task`; do not substitute the transcode or
audio-separation poll tools for enhancement results.
If a completed response supplies `source_url`, retain it even when the best-effort
copy fails. `persistence` is `not_applicable`, `persisted`, `failed`, or `not_requested`; durable
video copies are capped at 200 MiB. `estimated_cost_usd` remains null until
convenience-endpoint pricing and billing-unit mapping are confirmed.

#### `vod_get_enhancement_task`

Read-only poll of an enhancement task (`vod:read`). Requires the provider
`task_id` from the background result of `vod_enhance_video`. Maps provider `running`→`processing`,
`completed`→`succeeded`, and `failed`→`failed`, while requiring
`task_type="enhance-video"`. On success, returns the 24-hour `source_url`,
duration, resolution, frame rate, enhancement tier, and normalized timestamps.
With `persist_output=true` (default), concurrent first polls share one durable
artifact copy under the 200 MiB limit and cache it by task ID. Cache failures
emit safe warnings without discarding an artifact that was already created.

#### `vod_transcode_video`

Submit an asynchronous video transcoding task. Mutating, non-idempotent,
open-world. Do not retry the POST automatically (a timeout may be ambiguous).
The request body and `video` object enums are verified from the official AI
MediaKit API reference. Defaults reproduce the verified portrait-to-720x720
letterbox profile (`scale_type=2`, `scale_width=720`, `scale_height=720`,
`scale_mode=2`).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `video_url` | URL | Yes | Public HTTPS source; private/link-local targets rejected |
| `container_format` | `"MP4"` \| `"FLV"` \| `"MPEGTS"` | No | Output container format; default `MP4` |
| `video` | object | No | See fields below |
| `persist` | boolean | No | Best-effort durable copy on later poll; default `true` |

`video` fields: `codec` (`h264`/`h265`, default `h264`); `scale_type` (`0`/`1`/`2`,
default `2`); `scale_mode` (`0`/`1`/`2`, default `2`); `scale_width`/`scale_height`
(px [0,4320], only when `scale_type=2`, default 720); `scale_short`/`scale_long`
(px [0,4320], only when `scale_type=1`); `bitrate_mode` (`crf`/`abr`/`cbr`, default
`crf`); `bitrate_crf` ([0,51], default 25); `bitrate_kbps` (kbps [10,50000],
default 2000); `fps_mode` (`vfr`/`cfr`, default `vfr`); `fps` ([1,240], unset keeps
source rate); `is_hdr_to_sdr` (default `true`).

Returns `status="accepted"` plus `task_id` and a heuristic
`recommended_poll_after_ms` from the background result; pass that provider
`task_id` to `vod_get_transcode_task`.

#### `vod_get_transcode_task`

Read-only poll of a transcode task (`vod:read`). Requires the provider `task_id`
from the background result of `vod_transcode_video`. Maps provider `running`→`processing`,
`completed`→`succeeded`, `failed`→`failed` (the provider documents no
queued/expired/cancelled statuses). On success, returns `source_url` (24-hour
lifetime) plus optional `duration_seconds`/`resolution`/`video_codec` and
normalized ISO-8601 `created_at`/`finished_at`/`source_expires_at`. With
`persist_output=true` (default), the completed output is copied once into the
durable artifact store (200 MiB cap) and cached by task ID so repeated polls do
not re-download; a persistence failure never erases provider success. On
failure, `error` carries the safe provider detail.

#### `vod_add_subtitles` / `vod_get_subtitle_addition_task`

Burn an SRT/VTT/ASS subtitle file or inline timed cues into a public HTTPS
video. At least one of `subtitle_url` or `subtitles` is required; the file URL
takes priority if both are present. Inline cues require nonblank
`subtitle_text`, a nonnegative `start_time`, and a later `end_time`. Optional
position, font size, RGBA color, and font identifier fields control styling.
Submit with `vod:subtitle:add`, retrieve the provider `task_id` through
the background result, then poll with `vod:read`.
The poller requires `task_type="add-subtitle-to-video"` and can best-effort
persist the completed MP4 when `persist_output=true`.

#### `vod_remove_subtitles` / `vod_get_subtitle_removal_task`

Use precision erasure on a public HTTPS video. The default `subtitle` mode
targets dialogue subtitles; `text` mode is broader and may erase titles,
labels, or watermarks. Optional normalized rectangles, selected/skipped time
segments, and OCR subtitle thresholds constrain processing. Submit with
`vod:subtitle:remove`, retrieve the provider `task_id` from the background result,
then poll with `vod:read`. The
poller requires `task_type="erase-video-subtitle-pro"` and shares the subtitle
addition persistence contract.

Both submission tools are non-idempotent mutations and are never retried after
ambiguous transport failures. Use a stable `client_token` to reconcile such a
submission. Callback and queue fields are supported. `project` and removal
`model_version` are optional legacy endpoint extensions and are omitted by
default. Completed provider URLs are always preserved when persistence is
skipped or fails.

---

### VOD AI MediaKit audio separation

Requires `BYTEPLUS_VOD_MEDIAKIT_API_KEY` (same Bearer key as enhancement and
transcoding). Auth scopes: `vod:extract` (submit) and `vod:read` (poll).

#### `vod_separate_audio`

Submit an asynchronous voice and background audio separation task
(`POST /api/v1/tools/separate-voice`). Mutating, non-idempotent, open-world —
do not retry the POST automatically (timeout/5xx means ambiguous completion).
The source is a public HTTPS URL (audio or video), exactly one of the two.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `audio_url` | URL | Exactly one of `audio_url`/`video_url` | Public HTTPS audio URL (mp3, m4a, wav) |
| `video_url` | URL | Exactly one of `audio_url`/`video_url` | Public HTTPS video URL (mp4, flv, ts, avi, mov, wmv, mkv) |
| `scene` | `"Audio"` \| `"Music"` \| `"Drama"` \| `"Narrate"` | No | Default `Audio`. `Audio`/`Music` = 2-track; `Drama`/`Narrate` = 3-track |
| `output_format` | `"aac"` \| `"mp3"` \| `"wav"` \| `"m4a"` \| `"flac"` | No | Default `aac` |

Returns `status="accepted"` plus `task_id`, `request_id`, and
`provider_log_id` from the background result. Poll the provider `task_id` with
`vod_get_audio_separation`.

**Source URL liveness.** The provider downloads `audio_url`/`video_url`
asynchronously after submission, so the URL must stay fetchable until the
provider has downloaded it. A presigned URL (default 1800s / 30 min,
configurable 60–604800s via `TOS_PRESIGN_TTL_SECONDS`/`S3_PRESIGN_TTL_SECONDS`)
may expire before the provider fetches it, causing the task to fail. For VOD
inputs, upload via `media_upload` with `expires_in_seconds` (e.g. 3600) or use
a stable public URL.

#### `vod_get_audio_separation`

Read-only poll of a separation task (`vod:read`). Requires the provider
`task_id` from the background result of `vod_separate_audio`. Maps provider `running`→`processing`,
`completed`→`succeeded`, `failed`→`failed`. On success, `voice`, `background`,
`music`, and `sfx` each carry the track's expiring `source_url` (24-hour
lifetime) and, with `persist_output=true` (default), a durable `artifact`
reference copied once and cached by task ID. A persistence failure never erases
provider success. On failure, `error` carries the safe provider detail.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `task_id` | string | Yes | Provider task ID from the background result of `vod_separate_audio` |
| `persist_output` | boolean | No | Best-effort durable copy on first successful poll; default `true` (requires background execution) |

**Latency and transient failures.** A completed separation typically takes
tens of seconds but can take minutes; keep polling until a terminal state
rather than giving up after the first `processing` response. A provider
`failed` result with `error.code` `AbilityProcessingError` /
`InternalError` is usually transient — re-submit the same source rather than
treating the input as invalid.

---

### Seed Audio Tools

Requires `BYTEPLUS_SEED_SPEECH_API_KEY`. Auth scope: `seed:audio:generate`.

#### `seed_audio_generate`

Generate a full-scene audio clip from a text prompt. Supports voice cloning via
audio references, optional image input for context-aware audio, subtitle
generation, and watermarking.

**Constraint:** `audio_references` and `image_reference` are mutually
exclusive.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text_prompt` | `str` | Yes | 1–3000 characters |
| `audio_references` | `list[AudioReference]` | No | Up to 3 references (speaker ID, URL, or Base64). Base64 WAV is preflight-checked against the 30s limit. |
| `image_reference` | `MediaSource` | No | Image for context-aware audio |
| `output` | `AudioOutputOptions` | No | Format (wav/mp3/pcm/ogg), sample_rate, speech_rate, loudness_rate, pitch_rate, subtitle options |
| `watermark` | `AudioWatermarkOptions` | No | Enable watermark and optional metadata |
| `persist` | `bool` | Yes (default `true`) | Persist to artifact store |

Returns `SeedAudioGenerateOutput` with `artifact: ArtifactRef`,
`duration_seconds`, `billing_duration_seconds`, optional `subtitle`,
`request_id`, `provider_log_id`, optional `source_url`.

**Example — basic audio generation:**

```json
{
  "text_prompt": "A gentle rain falling on a tin roof, with distant thunder rumbling every few seconds",
  "output": {
    "format": "wav",
    "sample_rate": 44100
  },
  "persist": true
}
```

**Example — voice cloning with a speaker ID:**

```json
{
  "text_prompt": "Hello, welcome to our presentation. Today we will discuss the quarterly results.",
  "audio_references": [
    { "kind": "speaker", "speaker_id": "zh_female_qingxin" }
  ],
  "output": {
    "format": "mp3",
    "subtitle": true,
    "subtitle_type": "word"
  },
  "persist": true
}
```

#### `seed_audio_generate_variations`

Generate 1–5 audio variations in parallel. Each variation is an independent
generation (no seeds are supported for audio).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text_prompt` | `str` | Yes | Base prompt (1–3000 chars) |
| `variations` | `int` | Yes | 1–5 |
| `variation_prompts` | `list[str]` | No | Per-variation prompts (one per variation) |
| All other audio params | — | No | Same as `seed_audio_generate` |

Returns `SeedAudioVariationsOutput` with `VariationSummary` (total, succeeded,
failed, per-variation results with partial failure capture).

**Example — 3 variations with per-variation prompts:**

```json
{
  "variation_prompts": [
    "A calm ocean waves soundscape",
    "A busy city street ambient noise",
    "A quiet forest with birds chirping"
  ],
  "variations": 3,
  "output": { "format": "mp3" },
  "persist": true
}
```

---

### Reusing uploaded references across shots (presign pattern)

Presigned URLs expire after 30 minutes by default (1800s, configurable
60–604800s via `TOS_PRESIGN_TTL_SECONDS`/`S3_PRESIGN_TTL_SECONDS`). When the
same reference images or audio are used across multiple shots (e.g., character
sheets reused across every scene), do **not** re-upload the same file each time.
Instead:

1. **Upload once** — call `media_upload` for each reference file and store
   the returned `object_key` (e.g., in a project-level reference registry
   like `task_ids.json` or a dedicated `ref_cache.json`).
2. **Presign on demand** — before each new shot submission, call
   `media_presign` with the stored `object_key` to get a fresh presigned
   URL in seconds. No file re-upload, no duplicate storage cost.
3. **Batch presign** — presign all needed references for a shot in one call
   with `media_presign_batch` (pass the list of `object_keys`), then
   immediately submit the Seedance task while the URLs are still valid.

This reduces upload time from minutes (re-uploading 9–10 files per shot)
to seconds (presigning 9–10 keys per shot) and avoids filling object
storage with duplicate copies of the same reference images.

---

### Seedream (Image) Tools

Requires `BYTEPLUS_MODELARK_API_KEY`. Auth scope: `seedream:generate`.

#### `seedream_edit_image`

Interactive image editing with spatial precision. Supports point-based and
bounding-box editing through structured coordinate inputs. At least one
reference image and one coordinate (point or bbox) are required.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `prompt` | `str` | Yes | 1–4000 characters. Natural-language edit instruction. |
| `images` | `list[MediaSource]` | Yes | Reference images to edit (at least 1). |
| `point` | `EditCoordinate` | No* | Point coordinate `{x, y}` (0–999). *Required if bbox not provided. |
| `bbox` | `EditBbox` | No* | Bounding-box `{x1, y1, x2, y2}` (0–999). *Required if point not provided. |
| All other image params | — | No | Same as `seedream_generate_image` |

Returns `SeedreamEditOutput` with `artifacts: list[ArtifactRef]` and
`usage: SeedreamUsage`.

**Example — replace an object near a point:**

```json
{
  "prompt": "Replace the object with a crown.",
  "images": [{"kind": "url", "url": "https://example.com/photo.png"}],
  "point": {"x": 520, "y": 460}
}
```

**Example — replace a region with a bounding box:**

```json
{
  "prompt": "Replace with a garden.",
  "images": [{"kind": "url", "url": "https://example.com/photo.png"}],
  "bbox": {"x1": 120, "y1": 180, "x2": 640, "y2": 760}
}
```

Coordinates are normalized to 0–999 (top-left = `0,0`, bottom-right =
`999,999`). Convert pixel coordinates: `normalized = round(pixel / dimension * 1000)`.

---

#### `seedream_generate_image`

Generate images from text prompts. Supports text-to-image, reference-based
generation, batch generation (Lite/4x models), seed-based reproducibility, and
prompt optimization. For interactive editing with spatial coordinates, use
`seedream_edit_image` instead.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `prompt` | `str` | Yes | 1–4000 characters |
| `images` | `list[MediaSource]` | No | Reference images for editing |
| `model` | `str` | No | Model ID. Default: `dola-seedream-5-0-pro-260628` (Pro). Lite and 4x IDs are configured via `SEEDREAM_MODEL_BINDINGS`. |
| `size` | `str` | No | e.g. `1024x1024` |
| `seed` | `int` | No | -1 to 2147483647; -1 = client-randomized |
| `max_images` | `int` | No | 1–15 (batch for Lite/4x models only) |
| `output_format` | `"png"` \| `"jpeg"` | No | Default: `png` |
| `response_format` | `"url"` \| `"b64_json"` | No | Default: `url` |
| `watermark` | `bool` | No | Provider watermark |
| `prompt_optimization` | `"standard"` \| `"fast"` | No | Prompt enhancement; defaults to fast on 5.0 Pro (lower latency), pass standard for full CoT optimization |
| `persist` | `bool` | Yes (default `true`) | Persist to artifact store |

Returns `SeedreamGenerateOutput` with `artifacts: list[ArtifactRef]` and
`usage: SeedreamUsage`.

**Example — text-to-image:**

```json
{
  "prompt": "A serene mountain landscape at sunset, digital art style",
  "size": "1024x1024",
  "output_format": "jpeg",
  "persist": true
}
```

**Example — image editing with a reference:**

```json
{
  "prompt": "Change the background to a beach scene while keeping the subject unchanged",
  "images": [
    { "kind": "url", "url": "https://cdn.example.com/original.png" }
  ],
  "size": "1024x1024",
  "persist": true
}
```

**Example — reproducible generation with a seed:**

```json
{
  "prompt": "A cat sitting on a windowsill looking outside",
  "seed": 42,
  "size": "1024x1024",
  "persist": true
}
```

#### `seedream_generate_image_variations`

Generate 1–10 image variations in parallel. Each variation gets a distinct
seed, making every result different. Supports per-variation prompts and
deterministic seed sequences.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `prompt` | `str` | Yes | Base prompt (1–4000 chars) |
| `variations` | `int` | Yes | 1–10 |
| `variation_prompts` | `list[str]` | No | Per-variation prompts |
| `base_seed` | `int` | No | None=random, -1=client-randomized, N=deterministic sequence |
| All other image params | — | No | Same as `seedream_generate_image` |

Returns `SeedreamVariationsOutput` with `VariationSummary`.

**Example — 4 variations with deterministic seeds:**

```json
{
  "prompt": "A futuristic city skyline, cyberpunk aesthetic",
  "variations": 4,
  "base_seed": 100,
  "size": "1024x1024",
  "persist": true
}
```

This produces 4 images with seeds [100, 101, 102, 103].

**Example — per-variation seasonal prompts:**

```json
{
  "variation_prompts": [
    "A cat in spring, cherry blossoms",
    "A cat in summer, sunny garden",
    "A cat in autumn, fallen leaves",
    "A cat in winter, snow"
  ],
  "variations": 4,
  "persist": true
}
```

---

### Seedance (Video) Tools

Requires `BYTEPLUS_MODELARK_API_KEY`. Auth scopes: `seedance:create`,
`seedance:read`, `seedance:delete`.

Video generation is **asynchronous**. You create a task, then poll for
completion. Tasks transition through states:

```text
queued -> running -> succeeded | failed | cancelled | expired
```

#### `seedance_create_task`

Create an async video generation task. The background result contains the
provider task ID for subsequent polling.

**Constraints:**
- At least one of `prompt`, `images`, or `videos` is required.
- Audio references cannot be the sole media input; at least one image or
  video must accompany audio.
- Text-only (prompt with no media) is supported for pure text-to-video.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `prompt` | `str` | No | 1–32,000 characters. BytePlus recommends staying under 1,000 words for focus; that recommendation is not a hard API limit. |
| `images` | `list[SeedanceImageInput]` | No | Up to 9 images with roles: `first_frame`, `last_frame`, `reference_image`. Each entry may be a plain URL string or `{"url": ...}` (coerced to `role=reference_image`) |
| `videos` | `list[SeedanceVideoInput]` | No | Up to 3 videos with role: `reference_video`. Each entry may be a plain URL string or `{"url": ...}` |
| `audios` | `list[SeedanceAudioInput]` | No | Up to 3 audios with role: `reference_audio`. Each entry may be a plain URL string or `{"url": ...}` |
| `model` | `str` | No | Model ID. Default: `dreamina-seedance-2-0-260128` (Standard). Fast and Mini IDs are configured via `SEEDANCE_MODEL_BINDINGS`. |
| `resolution` | `"480p"` \| `"720p"` \| `"1080p"` \| `"4k"` | No | |
| `ratio` | `str` | No | Aspect ratio. For `extend_video`, stripped (auto-locks to source) to prevent `InvalidParameter.TaskTypeConstraint`. For `edit_video`, auto-derived from input video. For first/last-frame, locks to first image. |
| `duration` | `int` | No | -1 (auto) to 15 seconds. Ignored for edit tasks (auto-derived from input video) |
| `omni_reference_task_type` | `str` | No | Task type hint (e.g. `edit_video`, `extend_video`). Default: `auto`. Note: 2.0 `edit_video` output caps at ~5s in practice. |
| `generate_audio` | `bool` | No | Generate audio track |
| `watermark` | `bool` | No | Provider watermark |
| `return_last_frame` | `bool` | No | Include last frame image in output |
| `execution_expires_after` | `int` | No | 3600–259200 seconds |
| `priority` | `int` | No | 0–9 |
| `safety_identifier` | `str` | No | Max 64 characters |

Returns `SeedanceCreateTaskOutput` with `task_id`, `status="queued"`, and
`recommended_poll_after_ms`.

**Example — text-to-video:**

```json
{
  "prompt": "A drone flying over a tropical island, crystal clear water, aerial view",
  "resolution": "1080p",
  "duration": 8,
  "generate_audio": true
}
```

**Example — image-to-video with first and last frame:**

```json
{
  "prompt": "Smooth transition between the two scenes",
  "images": [
    { "role": "first_frame", "kind": "url", "url": "https://cdn.example.com/start.png" },
    { "role": "last_frame", "kind": "url", "url": "https://cdn.example.com/end.png" }
  ],
  "resolution": "720p",
  "duration": 5
}
```

#### Auto-locked parameters by task type

When the provider detects (or is hinted via `omni_reference_task_type`)
that the task is video editing, extension, or first/last-frame generation,
certain parameters are auto-derived from the input media and cannot be
overridden:

| Task type | Aspect ratio | Duration |
|---|---|---|
| Video editing | Locked to input video's ratio | Locked to input video's duration (±0.3s) |
| Video extension | Locked to input video's ratio | Set freely |
| First/last-frame generation | Locked to first image's ratio | Set freely |
| Text-to-video / standard reference | Set freely | Set freely (or `-1` for auto) |

For `extend_video`, any explicit `ratio` is client-stripped (logged as
`seedance_ratio_stripped_for_extension`) to prevent the provider from
rejecting the task with `InvalidParameter.TaskTypeConstraint`.

Use `omni_reference_task_type` to force a specific task type when
auto-detection is ambiguous (e.g. set to `"edit_video"` or
`"extend_video"`). When omitted, the provider defaults to `"auto"` which
infers the task type from the prompt and media inputs.

#### `seedance_create_task_variations`

Create 1–5 video generation tasks in parallel. Each variation creates a
separate task.

| Parameter | Type | Required | Description |
|---|---|---|---|
| Same as `seedance_create_task` | — | — | — |
| `variations` | `int` | Yes | 1–5 |
| `variation_prompts` | `list[str]` | No | Per-variation prompts |

Returns `SeedanceVariationsOutput` with per-variation provider task IDs and
`recommended_poll_after_ms` values. The variation result is returned by the
background job; retrieve its terminal result before using each provider task ID
with `seedance_get_task`.

#### `seedance_get_task`

Retrieve the status and output of a video generation task. On success,
automatically persists the video (and optional last frame) to the artifact
store. Results are cached for 24 hours.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `task_id` | `str` | Yes | Provider task ID from the create tool's background result |
| `persist_output` | `bool` | Yes (default `true`) | Persist to artifact store; `true` requires background retrieval |

Returns `SeedanceTaskOutput` with `task_id`, `model`, `created_at`,
`updated_at`, `status`, optional `error`, optional `video: ArtifactRef`,
optional `last_frame: ArtifactRef`, optional `usage`, `settings`.

**Foreground status polling:**

```json
{"task_id": "provider_task_abc123", "persist_output": false}
```

Call this repeatedly (respecting the `recommended_poll_after_ms` from
creation) until `status` is `succeeded`, `failed`, `cancelled`, or `expired`.
For durable artifact persistence, repeat the same call with `persist_output`
omitted or `true` through background execution after the provider task reaches
a terminal state.

#### `seedance_list_tasks`

List recent video generation tasks (last 7 days). Supports filtering by status,
model, and service tier.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `page` | `int` | No | 1–500 |
| `page_size` | `int` | No | 1–100 |
| `status` | `SeedanceTaskStatus` | No | Filter by status |
| `task_ids` | `list[str]` | No | Filter by specific task IDs |
| `model` | `str` | No | Filter by model |
| `service_tier` | `"default"` \| `"flex"` | No | Filter by tier |

Returns `SeedanceTaskPage` with paginated task summaries.

#### `seedance_cancel_or_delete_task`

Cancel a queued task or delete a terminal task. **Destructive** — requires
explicit confirmation.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `task_id` | `str` | Yes | Task to act on |
| `mode` | `"cancel"` \| `"delete"` | Yes | Action to perform |
| `expected_status` | `SeedanceTaskStatus` | Yes | Must match current status |
| `confirm` | `Literal[true]` | Yes | Must be `true` |

- `mode=cancel` + `expected_status=queued`: Cancel a pending task.
- `mode=delete` + `expected_status=succeeded|failed|expired`: Delete a completed
  task.

Returns `SeedanceCancelOrDeleteOutput`.

---

### Seedance 2.5 (Video) Tools

Requires `BYTEPLUS_MODELARK_API_KEY`. Same auth scopes as 2.0.

Seedance 2.5 (`dreamina-seedance-2-5-260628`) is the newer, higher-capability model. Key differences from 2.0:

| Capability | Seedance 2.0 | Seedance 2.5 |
|---|---|---|
| Max duration | 15s | 30s |
| Max images | 9 | 30 |
| Max videos | 3 | 10 |
| Max audios | 3 | 10 |
| Resolution | 480p, 720p, 1080p, 4K | 480p, 720p, 1080p |
| Fast/Mini variants | Yes | No |
| Structured editing | No | Subject replacement, background replacement, audio editing |
| Forward/backward extension | No (manual `return_last_frame` chaining) | Yes (native) |
| Keyframe sequences | No | Yes |

**When to choose 2.5:** longer single-pass videos (up to 30s), richer multimodal references (30/10/10), structured editing, native extension, 1080p output.

**When to choose 2.0:** 4K output resolution, Fast/Mini speed variants, lower cost per generation.

#### `seedance_2_5_create_task`

Create an asynchronous Seedance 2.5 video generation task.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `prompt` | `str` | No | Text prompt (up to 32,000 chars). Optional when media inputs are provided. |
| `images` | `list[SeedanceImageInput]` | No | Up to 30 images with roles: `first_frame`, `last_frame`, `reference_image`. Each entry may be a plain URL string or `{"url": ...}` |
| `videos` | `list[SeedanceVideoInput]` | No | Up to 10 videos with role: `reference_video`. Each entry may be a plain URL string or `{"url": ...}` |
| `audios` | `list[SeedanceAudioInput]` | No | Up to 10 audios with role: `reference_audio`. Audio-only input is supported (unique to 2.5). Each entry may be a plain URL string or `{"url": ...}` |
| `model` | `str` | No | Default: `dreamina-seedance-2-5-260628`. No Fast/Mini variants. |
| `resolution` | `"480p"` \| `"720p"` \| `"1080p"` | No | 2.5 supports 480p, 720p, and 1080p. 4k is not supported. |
| `ratio` | `str` | No | Aspect ratio (e.g. `16:9`, `9:16`). For `extend_video`, stripped (auto-locks to source) to prevent `InvalidParameter.TaskTypeConstraint`. For `edit_video`, auto-derived from input video. For first/last-frame, locks to first image. |
| `duration` | `int` | No | -1 (auto) to 30 seconds. Ignored for `edit_video` tasks (auto-derived from input video). |
| `omni_reference_task_type` | `str` | No | Task type hint passed through to the provider. Common values: `auto` (default, provider auto-detects), `edit_video`, `extend_video`. The server does not restrict or validate this to a fixed enum for either 2.0 or 2.5; for `extend_video`, `ratio` is stripped client-side to prevent `InvalidParameter.TaskTypeConstraint`. |
| `generate_audio` | `bool` | No | Whether to generate an audio track. |
| `watermark` | `bool` | No | Apply AIGC watermark. |
| `return_last_frame` | `bool` | No | Return the last frame as a separate image. |
| `execution_expires_after` | `int` | No | Max execution time in seconds (3600–259200). |
| `priority` | `int` | No | Task priority (0–9). |
| `safety_identifier` | `str` | No | Content safety tracking ID (max 64 chars). |

Returns `Seedance25CreateTaskOutput` with `task_id`, `status="queued"`, and `recommended_poll_after_ms`.

> **Audio-only input:** Unlike Seedance 2.0, 2.5 supports audio as the sole
> media input — a single BGM, voice, or sound-effect track can drive visual
> pacing, beat matching, and lip-sync without any image or video reference.

**Example — 30s text-to-video with native audio:**

```json
{
  "prompt": "A cinematic 30-second scene...",
  "model": "dreamina-seedance-2-5-260628",
  "resolution": "720p",
  "ratio": "16:9",
  "duration": 30,
  "generate_audio": true
}
```

#### `seedance_2_5_create_task_variations`

Create multiple Seedance 2.5 video tasks in parallel. Inherits all parameters from `seedance_2_5_create_task` and adds `variations` (1–5) and `variation_prompts`.

> **Shared lifecycle tools:** `seedance_get_task`, `seedance_list_tasks`, and
> `seedance_cancel_or_delete_task` work with both 2.0 and 2.5 task IDs. Use
> them the same way regardless of which create tool produced the task.

---

### Seed 3D (Hyper3D + Hitem3d) Tools

Requires `BYTEPLUS_MODELARK_3D_ENABLED=true` (and `BYTEPLUS_MODELARK_API_KEY`).
Auth scopes: `hyper3d:create`, `hyper3d:read`, `hyper3d:delete`, `hitem3d:create`,
`hitem3d:read`, `hitem3d:delete`.

3D generation is **asynchronous**. You create a task, then poll for completion.
Tasks use the same lifecycle states as Seedance:
`queued → running → succeeded | failed | cancelled | expired`.

Two model families are supported:

- **Hyper3D** (`hyper3d-gen2-260112`) — text-to-3D and image-to-3D. Accepts a
  text prompt and/or up to 5 reference images. Supports seeds, PBR/Shaded/All/None
  materials, Raw/Quad mesh modes, custom polygon counts, HD textures, bounding-box
  conditioning, T-Pose, and subdivision levels. Output formats: GLB, OBJ, USDZ,
  FBX, STL.
- **Hitem3d** (`hitem3d-2-0-251223`) — image-to-3D only. Requires 1–4 reference
  images. Supports resolution selection (1536/1536pro), custom face counts
  (100K–2M), geometry-only or geometry+texture modes, and multi-view bitmap
  marking. Output formats: OBJ, GLB, STL, FBX, USDZ.

#### `hyper3d_create_task`

Create an asynchronous Hyper3D 3D generation task. Supports text-to-3D (prompt
required) and image-to-3D (1–5 images).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `prompt` | `str` | No* | Text prompt (English, max 400 chars). *Required for text-to-3D when no images are provided. |
| `images` | `list[Seed3DImageInput]` | No | Reference images for image-to-3D. Max 5. |
| `model` | `str` | No | Model ID. Omit for the configured Hyper3D default. |
| `seed` | `int` | No | Random seed for reproducible generation (0–65535). |
| `callback_url` | `str` | No | Optional callback URL notified on status changes. |
| `material` | `"PBR"` \| `"Shaded"` \| `"All"` \| `"None"` | No | Material type. PBR (default). |
| `mesh_mode` | `"Raw"` \| `"Quad"` | No | Mesh shape. Raw (triangles) or Quad (default). |
| `quality_override` | `int` | No | Custom polygon count (Raw: 500–1M, Quad: 1000–200K). |
| `addons` | `"HighPack"` | No | Texture enhancement. HighPack provides 4K textures. |
| `use_original_alpha` | `bool` | No | Preserve transparent areas of the input image. |
| `bbox_condition` | `list[int]` | No | Bounding box `[width, height, length]` (3 ints). |
| `ta_pose` | `bool` | No | Force T-Pose/A-Pose for humanoid models. |
| `subdivision_level` | `"high"` \| `"medium"` \| `"low"` | No | Polygon count level. Ignored when `quality_override` is set. |
| `file_format` | `"glb"` \| `"obj"` \| `"usdz"` \| `"fbx"` \| `"stl"` | No | Output 3D file format. Defaults to `glb`. |
| `hd_texture` | `bool` | No | Enable HD textures. |

Returns `Seed3DCreateTaskOutput` with `task_id`, `status="queued"`, and
`recommended_poll_after_ms` (5000ms).

**Example — text-to-3D:**

```json
{
  "prompt": "A medieval castle with tall towers and a drawbridge",
  "file_format": "glb",
  "material": "PBR"
}
```

**Example — image-to-3D with PBR materials:**

```json
{
  "images": [
    { "kind": "url", "url": "https://cdn.example.com/character.png" }
  ],
  "material": "PBR",
  "mesh_mode": "Quad",
  "file_format": "glb"
}
```

#### `hitem3d_create_task`

Create an asynchronous Hitem3d 3D generation task. Image-to-3D only; requires
1–4 reference images.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `images` | `list[Seed3DImageInput]` | Yes | Reference images for image-to-3D. 1–4 required. |
| `model` | `str` | No | Model ID. Omit for the configured Hitem3d default. |
| `callback_url` | `str` | No | Optional callback URL notified on status changes. |
| `resolution` | `"1536"` \| `"1536pro"` | No | Model resolution. 1536 (default) or 1536pro. |
| `face` | `int` | No | Custom model face count (100000–2000000). |
| `file_format` | `"obj"` \| `"glb"` \| `"stl"` \| `"fbx"` \| `"usdz"` | No | Output 3D file format. Defaults to `obj`. |
| `request_type` | `1` \| `3` | No | 1 = geometry only, 3 = geometry + texture (default). |
| `multi_images_bit` | `str` | No | Bitmap marking which views are present, in order front/back/left/right (e.g. `"1010"` = front + left). Max 4 chars. |

Returns `Seed3DCreateTaskOutput` with `task_id`, `status="queued"`, and
`recommended_poll_after_ms` (5000ms).

**Example — image-to-3D with multiple views:**

```json
{
  "images": [
    { "kind": "url", "url": "https://cdn.example.com/front.png" },
    { "kind": "url", "url": "https://cdn.example.com/left.png" }
  ],
  "multi_images_bit": "1010",
  "resolution": "1536pro",
  "file_format": "glb"
}
```

#### `hyper3d_get_task` / `hitem3d_get_task`

Retrieve the status and output of a 3D generation task. On first successful
retrieval with `persist_output=true` (default), copies the provider's 24-hour
file URL (zip package of the 3D file) into durable artifact storage so the
`seed-media://` resource remains available after expiry.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `task_id` | `str` | Yes | Provider task ID from the create tool's background result |
| `persist_output` | `bool` | No (default `true`) | Persist the 3D file to artifact store on first success; requires background execution |

Returns `Seed3DTaskOutput` with `task_id`, `model`, `created_at`, `updated_at`,
`status`, optional `error`, optional `file: ArtifactRef` (on success), and
optional `usage`.

#### 3D delivery contract

Provider success delivers a generated package, not a Blender-ready or approved
asset. Before handing a result to a DCC workflow, retain the immutable package
and record the provider family and model, request and reference hashes, the
local MCP task or Ark job ID and the provider task ID as separate values,
artifact ID, byte size, package SHA-256, requested format, material/topology
settings, usage, and source URL expiry.

Prefer GLB for an initial Blender handoff when mesh, hierarchy, materials, and
textures should travel together. Extract the package into a bounded new
directory, reject absolute paths and parent traversal, and do not overwrite the
provider archive. Import into a quarantine collection before normalizing units,
scale, axes, origin, transforms, geometry, normals, UVs, materials, textures,
or rig readiness. Record the normalized working-copy hash and viewport review
separately from the provider package.

A generated 3D asset supplies structure and appearance. It does not become a
Seedance motion authority until an animated video render is intentionally
selected and bound for a supported video-reference mode. Keep 3D generation,
Blender normalization, previz rendering, and Seedance generation as distinct
operations with distinct task IDs, costs, statuses, and review evidence.

#### `hyper3d_list_tasks` / `hitem3d_list_tasks`

List recent 3D generation tasks (previous 7 days, provider limitation). Supports
filtering by status, task IDs, and model.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `page` | `int` | No | 1–500 |
| `page_size` | `int` | No | 1–100 |
| `status` | `Seed3DTaskStatus` | No | Filter by status |
| `task_ids` | `list[str]` | No | Filter by specific task IDs |
| `model` | `str` | No | Filter by model ID |

Returns `Seed3DTaskPage` with paginated task summaries.

#### `hyper3d_cancel_or_delete_task` / `hitem3d_cancel_or_delete_task`

Cancel a queued task or delete a terminal task. **Destructive** — requires
explicit confirmation.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `task_id` | `str` | Yes | Task to act on |
| `mode` | `"cancel"` \| `"delete"` | Yes | Action to perform |
| `expected_status` | `Seed3DTaskStatus` | Yes | Must match current status |
| `confirm` | `Literal[true]` | Yes | Must be `true` |

- `mode=cancel` + `expected_status=queued`: Cancel a pending task.
- `mode=delete` + `expected_status=succeeded|failed|expired`: Delete a completed task.

Returns `Seed3DCancelOrDeleteOutput`.

---

### Seed 2.1 Multimodal Understanding

Requires `BYTEPLUS_MODELARK_API_KEY`. Auth scope: `understanding:read`.

The default model is `dola-seed-2-1-turbo-260628` (Seed 2.1 Turbo).
`dola-seed-evolving` (the latest Seed-series Pro-tier model) is also a
recognized built-in ID — set `SEED_UNDERSTANDING_DEFAULT_MODEL=dola-seed-evolving`
to opt in; its family auto-resolves to `pro` so no explicit
`SEED_UNDERSTANDING_MODEL_FAMILY` is required. Other custom model IDs can be
registered via `SEED_UNDERSTANDING_MODEL_BINDINGS`.

`seed_understand` requires background execution. Its direct tool contract uses
`execution.taskSupport="required"`; clients without that capability must use
`ark_job_submit`. Both paths return a local job ID immediately and use the
server-recommended two-second polling interval. Do not call it as a foreground
tool or retry it with a shorter prompt to work around a client timeout. Set the
requested task TTL long enough for the expected video analysis duration.

#### `seed_understand`

Understand images and videos, or reason about a task, through the Seed 2.1
multimodal model via ModelArk Chat Completions. Supports deep-thinking
(chain-of-thought) reasoning when `thinking=true`. Use this for:

- **Video understanding** — describe, summarize, or answer questions about video content
- **Image understanding / OCR** — extract text, describe scenes, analyze visual content
- **Multimodal reasoning** — combine text + images + videos for complex analysis
- **As a reasoning sub-agent** — delegate analysis tasks that need visual context

Video inputs must be HTTPS URLs (Base64 not supported by the chat endpoint).
**Prefer a public HTTPS URL the provider can already fetch as video.** Upload
local files via `media_upload` first. For page/platform links (YouTube, TikTok,
Instagram, and similar), auth-gated URLs, or any link that is not a usable video
input, download locally with an available downloader, then `media_upload` /
`media_presign` before calling `seed_understand`. Do not analyze brand ads or
inspiration footage from transcripts or article text alone when the task is
visual or motion grammar.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `prompt` | `str` | Yes | 1–32,000 characters. The question or task for the model. |
| `images` | `list[UnderstandingImageInput]` | No | Up to 32 images (URL or Base64) |
| `videos` | `list[UnderstandingVideoInput]` | No | Up to 32 videos (URL only, no Base64) |
| `system` | `str` | No | Optional system instruction (max 32,000 chars) |
| `model` | `str` | No | Override the configured Seed 2.1 model ID |
| `thinking` | `bool` | No (default `false`) | Enable deep-thinking chain-of-thought reasoning |
| `reasoning_effort` | `"low"` \| `"medium"` \| `"high"` | No | Only when `thinking=true` |
| `temperature` | `float` | No | 0.0–2.0. Lower = more deterministic |
| `max_tokens` | `int` | No | 1–32768 |
| `top_p` | `float` | No | 0.0–1.0 nucleus sampling |
| `repetition_penalty` | `float` | No | 0.0–2.0 (Ark-only parameter) |

Returns `SeedUnderstandOutput` with `model`, `completion_id`, `choices`
(each with `content` and optional `reasoning_content`), `usage`
(prompt_tokens, completion_tokens, total_tokens), and `request_id`.

**Example — image OCR / understanding:**

```json
{
  "prompt": "Extract all text visible in this image and describe the scene.",
  "images": [
    { "kind": "url", "url": "https://cdn.example.com/document.png" }
  ]
}
```

**Example — video understanding with deep thinking:**

```json
{
  "prompt": "Analyze this product demo video. What are the key features shown? Are there any UI issues or bugs visible? Rate the overall production quality.",
  "videos": [
    { "kind": "url", "url": "https://cdn.example.com/demo.mp4" }
  ],
  "thinking": true,
  "reasoning_effort": "high",
  "max_tokens": 4096
}
```

**Example — multimodal reasoning as a sub-agent:**

```json
{
  "prompt": "Compare the UI in screenshot 1 with the design spec in screenshot 2. List all differences in spacing, color, and typography.",
  "images": [
    { "kind": "url", "url": "https://cdn.example.com/screenshot.png" },
    { "kind": "url", "url": "https://cdn.example.com/design-spec.png" }
  ],
  "system": "You are a meticulous UI/UX reviewer. Be specific about pixel-level differences."
}
```

**Deep-thinking mode:** When `thinking=true`, the model produces
chain-of-thought reasoning visible in `choices[].reasoning_content`. Use
`reasoning_effort` to control depth:

| Level | When to Use | Latency |
|---|---|---|
| `low` | Quick checks, simple OCR, basic descriptions | Fastest |
| `medium` | Balanced analysis, moderate comparisons | Moderate |
| `high` | Deep analysis, complex reasoning, detailed reviews | Slowest |

Keep `thinking=false` for simple extraction, description, or lookup tasks
where speed matters more than reasoning depth.

**Prompt engineering tips:**

- **Specify output format** — ask for JSON, markdown tables, or numbered lists
  to get structured results
- **Use system instructions** for role and constraints (e.g., "You are a
  senior data analyst. Be thorough and systematic.")
- **Break complex tasks into steps** — make focused calls (extract, then
  analyze, then summarize) instead of one massive prompt
- **Ask for timestamps** when referencing specific video moments
- **For multi-language OCR**, mention expected languages in the prompt

**Limitations:**

- Video Base64 is not supported — upload via `media_upload` first
- 32 media parts max (images + videos combined)
- The provider response is non-streaming, but background execution keeps the
  long-running call outside the foreground client deadline
- No streaming — the full response is returned at once
- No artifact persistence — understanding returns text, not media

---

### Speech-to-Text

Requires `BYTEPLUS_SEED_SPEECH_API_KEY`. Auth scope: `seed:asr:transcribe`.

#### `speech_to_text`

Transcribe audio to text via Seed Speech ASR. The tool requires background
execution, internally submits the audio to the provider, polls until complete,
and returns the full transcription in the background result. The provider
lifecycle does not expose a separate task ID, object-storage upload, or second
domain tool.

The call is capped by `SEED_SPEECH_ASR_POLL_MAX_SECONDS` (default 600s).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `audio` | `AsrAudioInput` | Yes | Audio source (see below) |
| `options` | `AsrRequestOptions` | No | Transcription feature toggles |

**`AsrAudioInput`** (provide exactly one source):

| Field | Type | Required | Description |
|---|---|---|---|
| `audio_url` | `str` | No* | HTTPS URL of the audio file |
| `audio_data` | `str` | No* | Base64-encoded audio bytes. Mutually exclusive with other inputs. |
| `audio_file_path` | `str` | No* | Absolute local file path. stdio transport only. Mutually exclusive with other inputs. |
| `audio_format` | `"wav"` \| `"mp3"` \| `"ogg"` \| `"raw"` \| `"flac"` | Yes | Audio format |

**`AsrRequestOptions`:**

| Field | Type | Required | Description |
|---|---|---|---|
| `language` | `str` | No (default `en-US`) | BCP-47 language code |
| `enable_punc` | `bool` | No | Enable punctuation |
| `enable_itn` | `bool` | No | Enable ITN |

Returns `SpeechToTextOutput` with `result: TranscriptionResult` and optional
`log_id`. `TranscriptionResult` includes `text` (full transcript),
`utterances` (with word-level timestamps and speaker labels), and
`duration_ms`.

Transcription output is text — no artifact persistence needed.

**ASR error code `20000003` (silent audio).** Seed Speech ASR reports task
state in the `X-Api-Status-Code` header: `20000000` = success, `20000001` /
`20000002` = still processing, and `20000003` = terminal failure meaning
**silent audio — no human speech was detected**. The tool surfaces this as
`Seed Speech ASR query failed with status code 20000003` with
`retryable=false`. It is not transient — retrying the same task will not help.
Verify the audio actually contains speech and matches the declared
`audio_format`: for `wav`/`raw` the gateway assumes 16 kHz, 16-bit, mono PCM,
and a mismatch decodes to silence or garbage. Re-submit with corrected audio.

---

### Object Storage Upload

Requires object storage credentials (TOS or S3). No auth scope in stdio mode.
In JWT mode: `media:upload` for `media_upload`, `media:presign` for `media_presign`
and `media_presign_batch`.

#### `media_upload`

Upload media to object storage (TOS or S3) and receive a presigned HTTPS URL.
Especially useful for URL-only workflows such as Seedance video references,
which cannot be inlined as Base64.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `media_type` | `"image"` \| `"audio"` \| `"video"` | Yes | Media category for MIME and size validation |
| `mime_type` | `str` | Yes | e.g. `video/mp4`, `image/png`, `audio/wav` |
| `data` | `str` | No* | Base64-encoded media bytes. Mutually exclusive with `file_path`. |
| `file_path` | `str` | No* | Absolute path to a local file. stdio transport only. Mutually exclusive with `data`. |
| `key_prefix` | `str` | No | Object key prefix (default `references`). Alphanumeric, `-`, `_`, `/` only. |
| `expires_in_seconds` | `int` | No | Presigned URL validity in seconds (60–604800). Defaults to the configured presign TTL. Use a long value (e.g. 3600) for uploads destined for VOD tools, which fetch the source asynchronously. |

Returns `MediaUploadOutput` with `url`, `expires_at`, `object_key`, `bytes`.

**Example — upload a local video for use as a Seedance reference:**

```json
{
  "media_type": "video",
  "mime_type": "video/mp4",
  "file_path": "/absolute/path/clip.mp4"
}
```

**Example — upload Base64 audio:**

```json
{
  "media_type": "audio",
  "mime_type": "audio/wav",
  "data": "UklGRiQAAABXQVZFZm10..."
}
```

#### `media_presign`

Generate a fresh presigned HTTPS GET URL for an existing object in storage
(TOS or S3) without re-uploading. Use this when a previously uploaded
reference's presigned URL has expired or is about to expire.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `object_key` | `str` | Yes | Object key returned by a prior `media_upload` call |
| `expires_in_seconds` | `int` | No | Presigned URL validity in seconds (60–604800). Defaults to the configured presign TTL. Use a long value (e.g. 3600) when renewing for VOD tools, which fetch the source asynchronously. |

Returns `MediaPresignOutput` with `url`, `expires_at`, `object_key`.

**Example — renew an expired URL:**

```json
{
  "object_key": "references/video/abc-123-def"
}
```

JWT scope: `media:presign`.

#### `media_presign_batch`

Generate fresh presigned HTTPS GET URLs for many existing objects in a single
call (TOS or S3). Use this when preparing multiple references for one shot —
e.g. presigning 30 Seedance 2.5 reference images — instead of calling
`media_presign` once per key. Failures are reported per key: each failing key
returns `code` (`INVALID_KEY`, `NOT_OWNED`, `INTERNAL`, or a provider error
code) and `error` while the rest succeed.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `object_keys` | `list[str]` | Yes | Object keys returned by prior `media_upload` calls (1–100 entries) |
| `expires_in_seconds` | `int` | No | Presigned URL validity (60–604800) applied to every key. Defaults to the configured presign TTL. |

Returns `MediaPresignBatchOutput` with `items` (per-key `object_key`, `url`,
`expires_at`, `code`, `error`, `request_id`), `succeeded`, and `failed`.

**Example — presign a batch of references:**

```json
{
  "object_keys": [
    "references/image/char-sheet-1",
    "references/image/char-sheet-2",
    "references/audio/bgm-track"
  ]
}
```

JWT scope: `media:presign`.

---

## Resources

The server exposes two MCP resources:

### `seed-media://artifacts/{artifact_id}`

Retrieves a persisted media artifact by its UUID. Requires `artifacts:read`
scope in JWT mode. Returns the media content with the correct MIME type.

Artifacts are the durable, locally-persisted copies of generated media. Known
provider URLs expire (2h for audio, 24h for ModelArk image/video/3D), but
artifacts survive for 7
days (configurable via `ARTIFACT_TTL_SECONDS`). Always use `persist=true` (the
default) and reference the returned `ArtifactRef.uri` for long-lived access.

### `seed-health://status`

Returns a health summary with no authentication required. Lists which products
are configured (ModelArk, Seed 3D, Seed Audio, Seed Speech ASR, VOD AI MediaKit,
object storage), the
artifact backend, and the active transport.

---

## Architecture

### Three-Provider Design

The server normalizes three distinct BytePlus API surfaces:

| Provider | Auth | Base URL | Products |
|---|---|---|---|
| **ModelArk** | `Authorization: Bearer <key>` | `https://ark.ap-southeast.bytepluses.com/api/v3` | Seedream, Seedance, Seed 3D (Hyper3D + Hitem3d), Seed 2.1 Understanding |
| **Seed Speech** | `X-Api-Key: <key>` | `https://voice.ap-southeast-1.bytepluses.com` | Seed Audio, Speech-to-Text |
| **VOD AI MediaKit** | `Authorization: Bearer <key>` | `https://mediakit.ap-southeast-1.bytepluses.com/api/v1` | Video enhancement, transcode, subtitle burn-in/removal, audio separation |

One Seed Speech key covers both Seed Audio and ASR — the provider distinguishes
them by `X-Api-Resource-Id`, not by the key. ModelArk uses a separate Bearer
key that covers Seedream, Seedance, Seed 3D, and Seed 2.1 Understanding (3D
requires an additional feature flag). VOD AI MediaKit uses a third Bearer key.
Tools for a product are only registered when its provider API key is set.

### Runtime Services

Each server process maintains shared runtime services:

- **Artifact Store** — Filesystem-backed durable media persistence with
  ownership metadata and TTL-based cleanup.
- **Budget Ledger** — SQLite-backed per-principal daily spend tracking.
- **Task Ownership Store** — SQLite-backed task ID to principal mapping for
  Seedance and Seed 3D ownership enforcement.
- **Provider Limiters** — Concurrency control: a per-provider semaphore
  (default 5) for every call, plus a per-principal semaphore (default 3) that
  bounds authenticated JWT HTTP principals only. Local principals (stdio and
  HTTP-local) are bounded solely by the provider limit.
- **Safe Downloader** — SSRF-safe URL downloads with IP pinning and redirect
  validation.

### Model Capability Registry

The server validates inputs against known model capabilities before spending
quota. Eleven model families, with these default model IDs:

| Family | Default Model ID | Key Traits |
|---|---|---|
| **Seedream Pro** | `dola-seedream-5-0-pro-260628` | 10 refs, no batch, PNG/JPEG |
| **Seedream Lite** | *(configured via `SEEDREAM_MODEL_BINDINGS`)* | 14 refs, batch, streaming, PNG/JPEG |
| **Seedream 4.x** | *(configured via `SEEDREAM_MODEL_BINDINGS`)* | 14 refs, batch, streaming, JPEG only |
| **Seedance 2.5** | `dreamina-seedance-2-5-260628` | 30 imgs / 10 vids / 10 audios, 480p / 720p / 1080p, up to 30s, structured editing + extension |
| **Seedance 2 Standard** | `dreamina-seedance-2-0-260128` | 9 imgs / 3 vids / 3 audios, 480p–4K, 0–15s |
| **Seedance 2 Fast** | *(configured via `SEEDANCE_MODEL_BINDINGS`)* | 480p, 720p only |
| **Seedance 2 Mini** | *(configured via `SEEDANCE_MODEL_BINDINGS`)* | 480p, 720p only |
| **Seed 2.1 Turbo** | `dola-seed-2-1-turbo-260628` (default) | 256K context, images + videos, deep-thinking |
| **Seed 2.1 Pro** | `dola-seed-evolving` (recognized built-in; opt-in via `SEED_UNDERSTANDING_DEFAULT_MODEL`) | 256K context, images + videos, deep-thinking |
| **Hyper3D** | `hyper3d-gen2-260112` | Text-to-3D + image-to-3D (5 imgs), GLB/OBJ/USDZ/FBX/STL, seeds, PBR materials |
| **Hitem3d** | `hitem3d-2-0-251223` | Image-to-3D only (1–4 imgs), OBJ/GLB/STL/FBX/USDZ, resolution + face control |

Custom model IDs must be explicitly bound via `SEEDREAM_MODEL_BINDINGS`,
`SEEDANCE_MODEL_BINDINGS`, `SEED_UNDERSTANDING_MODEL_BINDINGS`, or
`SEED3D_MODEL_BINDINGS` JSON. When a client omits the `model` parameter, the
default model for that product is used.

---

## Usage Patterns

### Standard Generation Workflow

1. Run a Seedream or Seed Audio generation tool in the background with
   `persist=true` (default), using native task augmentation or the ordinary
   `ark_job_submit` compatibility path.
2. Poll the local job at the advertised interval and retrieve its background
   result.
3. The tool returns an `ArtifactRef` with `uri` (e.g.
   `seed-media://artifacts/abc123`).
4. Use the artifact URI as a stable reference to the media. The artifact
   survives provider URL expiry.

### Seedance Async Workflow

1. Run `seedance_create_task` (2.0) or `seedance_2_5_create_task` (2.5) in the
   background.
2. Poll the local job and retrieve its result to obtain the ModelArk `task_id`.
3. Immediately persist that provider `task_id`, the local MCP task or Ark job
   ID, request parameters, prompt hash, and intended output path to the shot
   manifest before provider polling.
4. Poll `seedance_get_task` in foreground with `persist_output=false` until the
   status is terminal.
   Respect the `recommended_poll_after_ms` from the creation response.
5. On a local timeout, disconnect, or client restart, retrieve and continue
   polling the same task. Do not submit a replacement task because the provider
   may still be running and a resubmission can create duplicate cost.
6. On success, run `seedance_get_task` in the background with
   `persist_output=true`. Download the persisted video to the project asset path
   and record artifact ID, byte size,
   SHA-256, provider timestamps, and usage.
7. Optionally call `seedance_list_tasks` to browse recent tasks.
8. Call `seedance_cancel_or_delete_task` only when cleanup is explicitly wanted.

> **Choosing 2.0 vs 2.5:** Use `seedance_2_5_create_task` when you need
> 30-second generation, 50 multimodal references, structured editing, or
> native extension. Use `seedance_create_task` for 4K or lower
> cost per task. The get/list/cancel tools are shared — `seedance_get_task`,
> `seedance_list_tasks`, and `seedance_cancel_or_delete_task` work with
> task IDs from either version.

### Seed 3D Async Workflow

1. Inspect live health or tool registration. If 3D tools are absent, report the
   unavailable capability; configuration documentation alone is not evidence
   that the current server exposes Hyper3D or Hitem3d.
2. Ensure `BYTEPLUS_MODELARK_3D_ENABLED=true` is set, along with
   `BYTEPLUS_MODELARK_API_KEY`.
3. Run `hyper3d_create_task` (text-to-3D or image-to-3D) or
   `hitem3d_create_task` (image-to-3D only) in the background.
4. Retrieve the background result and persist the returned provider `task_id`
   before polling.
5. Poll `hyper3d_get_task` or `hitem3d_get_task` with `persist_output=false`
   until the
   status is terminal (`succeeded`, `failed`, `cancelled`, `expired`).
   Respect the `recommended_poll_after_ms` (5000ms) from creation.
6. On success, run the get tool in the background with
   `persist_output=true`; the 3D file (zip package) is persisted to the artifact
   store with a 24-hour source URL backup.
7. Call `hyper3d_list_tasks` or `hitem3d_list_tasks` to browse recent tasks.
8. Call `hyper3d_cancel_or_delete_task` or `hitem3d_cancel_or_delete_task`
   only when cleanup is explicitly wanted.

> **Choosing Hyper3D vs Hitem3d:** Use `hyper3d_create_task` for text-to-3D
> or when you need seeds, PBR materials, or custom mesh modes. Use
> `hitem3d_create_task` for image-to-3D with multi-view inputs and resolution
> control. The get/list/cancel tools are family-specific — use the
> `hyper3d_*` tools for Hyper3D task IDs and `hitem3d_*` tools for Hitem3d
> task IDs.

### URL-only Video References

1. If the user has Base64 video or a local video file, run `media_upload` in the
   background.
2. Pass the returned presigned HTTPS URL into `seedance_create_task` or
   `seedance_2_5_create_task` as a video reference.

### Speech-to-Text Transcription

Run `speech_to_text` in the background with an audio URL, Base64, or local file
path (stdio only). Poll the local job and retrieve the complete
`TranscriptionResult` from its result; no separate provider task tool or
object-storage upload is required.

Use `TranscriptionResult.text` for the full transcript, or `utterances` /
`words` for timestamped segments and speaker labels.

### Generation Record Lifecycle

Use explicit manifest states so a generated take is never mistaken for an
approved take:

`ready → submitted → queued/running → review → approved/rejected`

Use `failed`, `cancelled`, or `expired` for terminal failures. While a take is
under review, record it under `outputs` or `generated_output`; reserve
`selected_variant` and `approved` for an explicit user choice.

If the provider returns null or incomplete settings, keep the submitted request
as the source of intended parameters and use media inspection as the source of
actual output properties.

### Post-generation Media QA

After downloading a Seedance result:

1. Use `ffprobe` to record actual resolution, duration, frame rate, codecs,
   pixel format, and audio streams.
2. Decode the full file with FFmpeg and fail QA on any decode error.
3. Watch the complete video at normal speed and inspect critical motion, timing,
   camera, transition, and audio segments directly.
4. Generate contact sheets around the opening, major transitions, and ending
   for appearance review only; do not use them as temporal evidence.
5. Check story acceptance criteria such as subject order, travel direction,
   boundary behavior, forbidden elements, and final location.
6. When audio is enabled, verify the audio stream and inspect important dynamic
   segments rather than inferring sound quality from the request.
7. Set the manifest to `review`; only the user can provide creative approval.
8. For HEVC or other review-host-sensitive masters, optionally generate a
   lightweight H.264 proxy while preserving the original master.

### Post-generation 3D QA

1. Validate the package type, byte size, and SHA-256 and preserve the original
   archive.
2. Inspect archive paths safely before extraction and confirm the requested 3D
   format exists.
3. Import into an isolated DCC collection and record object, mesh, face,
   material, texture, UV, and armature counts.
4. Measure dimensions, units, axes, origin, transforms, normals, non-manifold
   geometry, missing textures, and rig readiness.
5. Save a normalized working copy and viewport evidence without mutating the
   provider artifact.
6. Set the asset to `review`; provider success and successful import do not
   establish creative approval.

### Parallel Variations

Use variation tools when you want to give the user multiple options:

- `seedream_generate_image_variations` — up to 10 distinct images in one call.
- `seed_audio_generate_variations` — up to 5 audio clips in one call.
- `seedance_create_task_variations` (2.0) / `seedance_2_5_create_task_variations` (2.5) — up to 5 parallel video tasks.

Each variation is independent. Partial failures are captured — if 4 of 5
succeed, the tool returns 4 results and 1 error. The `VariationSummary` reports
`total`, `succeeded`, and `failed` counts.

### Deterministic Reproduction

For Seedream images, pass a `seed` to reproduce the same output with the same
prompt. For variation tools, pass `base_seed` to get a deterministic sequence
(e.g., `base_seed=100` with `variations=4` produces seeds [100, 101, 102,
103]).

### Image Editing

For interactive, coordinate-based editing, use `seedream_edit_image` with
structured `point` or `bbox` coordinates. The tool constructs the `<point>`
and `<bbox>` markup automatically. Do not force point or bbox logic into
`seedream_generate_image`.

For reference-based generation without spatial targeting, use
`seedream_generate_image` with the `images` parameter.

---

## Error Handling

### Provider Errors

Provider errors are normalized into `ProviderError` with a structured message.
The error includes the provider's HTTP status, error code, and a human-readable
description.

### Retry Policy

The server retries only explicitly retryable, non-ambiguous errors:
- Connection/transport errors are retried (up to 3 attempts with exponential
  backoff and jitter: 0.25s base, 4s max).
- Timeouts are NOT retried (the operation may have succeeded server-side).
- Provider errors with `retryable=true` are retried.

Exception: MediaKit mutation submissions (`vod_enhance_video`,
`vod_transcode_video`, `vod_add_subtitles`, `vod_remove_subtitles`, and
`vod_separate_audio`)
are never automatically retried. Their POSTs are non-idempotent and a transport
failure may have ambiguous completion. `vod_get_enhancement_task`,
`vod_get_transcode_task`, both subtitle poll tools, and
`vod_get_audio_separation` (read-only GET polls)
ARE retried on provider-marked
retryable errors such as HTTP 429.

For Seedance task polling, a local watcher timeout is not a generation failure.
Resume `seedance_get_task` with the existing task ID. Only create a new task
after the previous task reaches a terminal state and the user requests another
take.

For Seed 3D task polling, the same principle applies — resume
`hyper3d_get_task` or `hitem3d_get_task` with the existing task ID after a
local timeout. Do not submit a replacement task.

For `speech_to_text`, the background tool internally polls until transcription
completes or the `SEED_SPEECH_ASR_POLL_MAX_SECONDS` cap is reached. A timeout
does not produce a partial result.

### Budget Rejections

If `DAILY_BUDGET_USD` is configured (non-zero), the server tracks per-principal
daily spend. Requests exceeding the budget are rejected with a clear message.
Set to `0` (default) for record-only mode with no enforcement.

### Common Issues

| Symptom | Cause | Resolution |
|---|---|---|
| Tool not appearing | Missing API key | Set the corresponding `BYTEPLUS_*` env var |
| Model not found | Unbound custom model ID | Add to `*_MODEL_BINDINGS` JSON |
| URL expired | Provider URL TTL elapsed | Use `persist=true` and reference `ArtifactRef.uri` |
| Auth error (JWT mode) | Missing or invalid token | Check JWT configuration and scopes |
| Budget rejected | Daily limit exceeded | Wait for UTC day rollover or increase budget |
| `speech_to_text` timeout | ASR poll cap reached | Increase `SEED_SPEECH_ASR_POLL_MAX_SECONDS` or provide shorter audio |
| `speech_to_text` error code `20000003` | Silent audio — no speech detected, or a format mismatch (e.g. non-16 kHz/16-bit/mono WAV) decoded to silence | Verify the audio contains speech and matches the declared `audio_format`; re-submit with corrected audio |
| `media_upload` / `media_presign` / `media_presign_batch` not available | Missing TOS/S3 credentials | Set `TOS_*` or `S3_*` env vars and `OBJECT_STORAGE_BACKEND` |
| Presigned URL expired | TTL elapsed (default 30 min) | Call `media_presign` (single key) or `media_presign_batch` (many keys) with the `object_key` to generate a fresh URL |
| 3D tools not appearing | `BYTEPLUS_MODELARK_3D_ENABLED` not set or ModelArk key missing | Set `BYTEPLUS_MODELARK_3D_ENABLED=true` and ensure `BYTEPLUS_MODELARK_API_KEY` is configured |
| 3D task failed with `AbilityProcessingError` | Transient provider error | Re-submit the same task; do not treat the input as invalid |
| 3D package imports at the wrong scale or without expected materials | Provider output and Blender scene use different unit, axis, format, or texture assumptions | Preserve the package, import into a quarantine collection, then measure and normalize a working copy before production use |

---

## Best Practices

1. **Always persist.** Set `persist=true` (the default) so generated media
   survives provider URL expiry. Reference the returned `ArtifactRef.uri` for
   durable access.

2. **Poll with backoff for Seedance.** Use the `recommended_poll_after_ms`
   from `seedance_create_task` (2.0) or `seedance_2_5_create_task` (2.5) output. Don't
   poll faster than the interval — it
   wastes quota and can hit rate limits.

3. **Make polling resumable.** Save the local MCP task or Ark job ID and the
   provider task ID from the background result with request metadata before the
   first provider poll. A process timeout must continue the existing job, not
   create a duplicate.

4. **Use variation tools for choice.** When the user needs options (e.g., "show
   me a few versions"), use a variation tool rather than calling the single
   generate tool multiple times. Variations run in parallel and handle partial
   failures gracefully.

5. **Set seeds for reproducibility.** When the user wants consistent or
   reproducible output, pass a fixed `seed` to `seedream_generate_image` or a
   `base_seed` to `seedream_generate_image_variations`.

6. **Check health first.** Call `seed-health://status` to verify which products
   are configured before attempting generation.

7. **Respect model capabilities.** Different models support different features
   (batch generation, resolutions, reference counts). Check the capability
   registry before passing unsupported parameters.

8. **Clean up Seedance tasks.** Use `seedance_cancel_or_delete_task` to clean up
   completed or queued tasks when they are no longer needed.

9. **Validate input sizes.** Audio and image references are limited to 10 MiB
   each; video references are limited to 200 MiB. Base64 inputs are validated
   before submission.

10. **Treat cost estimates as estimates.** Record estimated cost separately
    from confirmed billing and usage. Do not infer actual cost solely from a
    preflight estimate when resolution or token usage differs.

11. **Verify the saved media.** Provider task success proves generation
    completed, not that resolution, audio, narrative continuity, or playback
    compatibility satisfy the production brief.

12. **Use `media_upload` for URL-only workflows.** Seedance video references
    are URL-only. When starting with a local or Base64 video, upload it first as
    a background job and pass the presigned URL into
    `seedance_create_task` (2.0) or `seedance_2_5_create_task` (2.5).

13. **Reuse references with `media_presign` — do not re-upload.** Presigned URLs
    expire after 30 minutes by default, but the underlying object persists in TOS/S3.
    Upload each reference file once, store the `object_key`, and call
    `media_presign` (single key) or `media_presign_batch` (many keys at once)
    to get a fresh URL for each new shot. This avoids re-uploading the same
    character/location/prop sheets for every scene.

14. **`speech_to_text` requires background execution.** Its internal provider
    polling can run until the configured poll cap. Retain the local MCP task or
    Ark job ID and retrieve the completed transcription from its terminal result.

15. **Use `seed_understand` for multimodal reasoning.** It can analyze images
    (OCR, scene description), videos (content analysis, UI review), and
    reason across multiple media inputs. Enable `thinking=true` for complex
    analysis. Prefer a public HTTPS video URL the provider already accepts;
    download and `media_upload` only when the link is a page/platform URL or
    otherwise unusable. Video Base64 is not supported.

16. **Choose the right Seedance model.** Use 2.0 (`seedance_create_task`)
    for 4K or lower cost. Use 2.5 (`seedance_2_5_create_task`) for
    30-second generation, 50 references, timestamp editing, 1080p output, or
    multi-round extension. The get/list/cancel tools are shared.

17. **Treat MediaKit persistence separately from the provider result.** Keep the
    returned `source_url` whenever a MediaKit video task reports success.
    Poll in foreground with `persist_output=false`, then use background
    execution with `persist_output=true` for the completed download. Inspect
    `persistence` and `persistence_issue`: the 200 MiB limit or a
    safe-download/storage failure can prevent the durable copy without
    invalidating the provider result. Do not resubmit after an ambiguous
    timeout, and do not present `estimated_cost_usd` as available.

18. **Enhancement is submit-then-poll.** Run `vod_enhance_video` in the
    background, retrieve its provider `task_id` from the background result, then poll with
    `vod_get_enhancement_task` until the status is `succeeded` or `failed`.
    Persist the result before its 24-hour
    source URL expires.

19. **Transcode is submit-then-poll.** Run `vod_transcode_video` in the
    background, retrieve its provider `task_id` from the background result, then poll with
    `vod_get_transcode_task` until the status is `succeeded` or `failed`. The
    default profile is portrait-to-720x720
    letterbox; set `video.codec`, `scale_*`, `bitrate_*`, `fps`, and
    `container_format` to target a specific output. Do not retry the POST after
    an ambiguous timeout — re-poll the task ID instead.

20. **Subtitle operations are submit-then-poll.** Use `vod_add_subtitles` or
    `vod_remove_subtitles` as a background job, retrieve its provider `task_id`
    from the background result, then poll with the matching task tool.
    Prefer `subtitle` removal mode unless the
    broader visual effect of `text` mode is intentional. Reuse `client_token`
    when reconciling an ambiguous submission.

21. **Choose the right 3D model.** Use `hyper3d_create_task` for text-to-3D or
    when you need seeds, PBR materials, custom mesh modes, or HD textures. Use
    `hitem3d_create_task` for image-to-3D with multi-view inputs (front/back/
    left/right) and resolution control (1536/1536pro). The get/list/cancel tools
    are family-specific — use `hyper3d_*` for Hyper3D task IDs and `hitem3d_*`
    for Hitem3d task IDs.

22. **3D output is a zip package.** The provider returns a 24-hour file URL
    containing a zip of the 3D file. On first successful poll with
    `persist_output=true` (default), the file is copied to the artifact store.
    Use the returned `ArtifactRef.uri` for durable access after the provider
    URL expires.

23. **Separate 3D generation from DCC readiness.** Preserve the immutable
    package and provenance, then normalize and review a working copy in Blender.
    Keep provider task status, import status, motion-master status, and user
    approval distinct.

---

## Environment Essentials

### Provider Credentials

- `BYTEPLUS_MODELARK_API_KEY` — enables Seedream, Seedance, Seed 3D (with flag), and Seed 2.1 Understanding
- `BYTEPLUS_SEED_SPEECH_API_KEY` — enables Seed Audio (TTS) and Speech-to-Text (ASR)
- `BYTEPLUS_VOD_MEDIAKIT_API_KEY` — enables VOD AI MediaKit enhancement, transcoding, subtitle operations, and audio separation
- `BYTEPLUS_MODELARK_BASE_URL` — override ModelArk data-plane host
- `BYTEPLUS_SEED_AUDIO_BASE_URL` — override Seed Audio host
- `SEED_SPEECH_ASR_BASE_URL` — override ASR host
- `BYTEPLUS_VOD_MEDIAKIT_BASE_URL` — override the VOD AI MediaKit HTTPS API base
- `SEED_SPEECH_ASR_POLL_INTERVAL_SECONDS` — seconds between ASR query polls (default 3)
- `SEED_SPEECH_ASR_POLL_MAX_SECONDS` — maximum total seconds to wait for ASR result (default 600)

### 3D Generation

- `BYTEPLUS_MODELARK_3D_ENABLED` — feature flag for Hyper3D + Hitem3d tools (default `false`; reuses ModelArk key)
- `HYPER3D_DEFAULT_MODEL` — default Hyper3D model ID (default `hyper3d-gen2-260112`)
- `HITEM3D_DEFAULT_MODEL` — default Hitem3d model ID (default `hitem3d-2-0-251223`)
- `SEED3D_MODEL_BINDINGS` — JSON array of 3D model bindings

### Model Selection

- `SEEDREAM_DEFAULT_MODEL`
- `SEEDANCE_DEFAULT_MODEL`
- `SEEDREAM_MODEL_FAMILY`
- `SEEDANCE_MODEL_FAMILY`
- `SEEDREAM_MODEL_BINDINGS`
- `SEEDANCE_MODEL_BINDINGS`
- `SEED_UNDERSTANDING_DEFAULT_MODEL`
- `SEED_UNDERSTANDING_MODEL_FAMILY`
- `SEED_UNDERSTANDING_MODEL_BINDINGS`

Use bindings when a custom model ID is not one of the built-in defaults.

### Transport and Auth

- `MCP_TRANSPORT` or `FASTMCP_TRANSPORT`
- `MCP_HOST` or `FASTMCP_HOST`
- `MCP_PORT` or `FASTMCP_PORT`
- `MCP_ALLOWED_ORIGINS`
- `MCP_ALLOWED_HOSTS`
- `MCP_AUTH_MODE`
- `MCP_JWT_JWKS_URI`
- `MCP_JWT_ISSUER`
- `MCP_JWT_AUDIENCE`
- `MCP_TENANT_CLAIM`
- `MCP_JWT_CLOCK_SKEW_SECONDS`
- `MCP_JWT_PROVIDE_DISCOVERY`
- `MCP_PUBLIC_BASE_URL`
- `MCP_JWT_SCOPES_SUPPORTED`

### HTTP Rate Limiting and Readiness

- `RATE_LIMIT_RPM`
- `RATE_LIMIT_BURST`
- `RATE_LIMIT_TRUST_PROXY_HEADERS`
- `READINESS_CHECK_PROVIDERS`
- `READINESS_PROVIDER_TIMEOUT_SECONDS`

### Persistence and Runtime

- `ARTIFACT_BACKEND`
- `ARTIFACT_DIR`
- `ARTIFACT_TTL_SECONDS`
- `STATE_BACKEND`
- `ARTIFACT_SWEEP_INTERVAL_SECONDS`
- `STATE_PRUNE_MAX_AGE_DAYS`
- `MCP_INLINE_MEDIA_MAX_BYTES`
- `MCP_HTTP_MAX_BODY_BYTES`
- `PROVIDER_MAX_CONCURRENCY`
- `PRINCIPAL_MAX_CONCURRENCY`
- `DAILY_BUDGET_USD`
- `PERSISTENCE_CACHE_MAX_SIZE`
- `PERSISTENCE_CACHE_TTL_SECONDS`
- `ARK_LOG_LEVEL`

### Object Storage

- `TOS_ACCESS_KEY`
- `TOS_SECRET_KEY`
- `TOS_SECURITY_TOKEN`
- `TOS_BUCKET`
- `TOS_REGION`
- `TOS_ENDPOINT`
- `TOS_PRESIGN_TTL_SECONDS`
- `S3_ACCESS_KEY`
- `S3_SECRET_KEY`
- `S3_BUCKET`
- `S3_REGION`
- `S3_ENDPOINT`
- `S3_PRESIGN_TTL_SECONDS`
- `OBJECT_STORAGE_BACKEND`
