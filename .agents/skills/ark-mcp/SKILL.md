---
name: ark-mcp
description: Guide for using the Ark Seed Multimodal MCP server to generate or edit images, audio, video, and 3D models (including Seedance 2.5 and whitelist-only 2.5 Premium 4K, Hyper3D, Hitem3d, BytePlus VOD AI MediaKit enhancement, transcoding, subtitle burn-in/removal, and voice/background audio separation), understand images and videos through Seed 2.1, understand or reason about audio, transcribe speech to text, manage Advanced Creation Rights face and voice assets (virtual portraits, authorized real people, copyright IP referenced as asset://), reuse completed onboarding and diagnose privacy input rejections with BytePlus AK/SK, run background jobs, upload reference media, and fetch persisted artifacts. Long-running work is submitted through ark_job_capabilities, ark_job_submit, ark_job_get, and ark_job_cancel by default, because most clients cannot negotiate MCP task augmentation; clients that do negotiate it may call the tools with native task metadata instead.
---

# Ark Seed Multimodal MCP Server

The Ark Seed MCP server exposes BytePlus multimodal generation through one
typed MCP tool surface:

- **Seedream**: image generation and editing.
- **Seed Audio**: full-scene audio with voice cloning and subtitles.
- **Seedance**: asynchronous video tasks. 2.5 is the default (30 s, 30/10/10
  references, 480p–1080p, Draft mode); 2.0 is legacy (15 s, 9/3/3, up to 4k,
  Fast/Mini); 2.5 Premium adds 4k and is whitelist-only.
- **Seed 3D**: Hyper3D and Hitem3d (feature-flagged, off by default).
- **Seed 2.1 understanding** (`seed_understand`), **audio understanding**
  (`seed_audio_understand`), and **Speech-to-Text** (`speech_to_text`).
- **VOD AI MediaKit**: enhancement, transcoding, subtitle burn-in and removal,
  voice/background separation.
- **Artifacts** (`seed-media://`), **object storage** upload and presign, and
  the **private asset library** (`asset://`) for Advanced Creation Rights.

Generated media is persisted to a local artifact store whose URIs outlive the
provider URLs (2 h for audio; 24 h for ModelArk image, video, 3D, and
MediaKit outputs).

## When to use

Use this skill to run, poll, persist, or troubleshoot any of the tools above:
generate or edit an image, audio, video, or 3D model; analyse images, video,
or audio; transcribe speech; enhance, transcode, subtitle, or separate media
with MediaKit; upload or presign reference media; bind `asset://` identities;
fetch or export a persisted artifact; or check which products the running
server exposes.

This skill covers the tool surface, not prompt writing. Compose with the
prompt skills for the model in question (for example Seedance, Seedream, or
Seed Audio prompt skills) and with any review and task-registry process your
project uses for submission gates.

## Load the right reference

| Load when | Reference |
|---|---|
| Building a Seedance 2.0 / 2.5 / Premium request: model choice, parameters, **Draft mode**, `omni_reference_task_type`, input rejections | [Seedance creation](references/seedance.md) |
| After a Seedance create: polling, batch status, download, **server restart recovery**, cleanup, media QA | [Seedance tasks](references/seedance-tasks.md) |
| Generating, editing, or varying images | [Seedream](references/seedream.md) |
| Generating speech, music, SFX, or ambience | [Seed Audio](references/audio.md) |
| Image/video analysis, audio analysis, or word-timed transcripts | [Understanding and speech-to-text](references/understanding-and-stt.md) |
| Enhance, transcode, subtitle, or audio-separation tasks | [VOD MediaKit](references/vod-mediakit.md) |
| Hyper3D / Hitem3d generation, package handling, DCC handoff | [Seed 3D](references/3d.md) |
| Real people, Virtual Portraits, copyright IP, privacy rejections | [Assets and rights](references/assets-and-rights.md) |
| Uploading local media, reusing references across shots | [Object storage](references/object-storage.md) |
| A background job would write local files, failed with "session is not available", returned a huge result, or hit an output audit | [Background-job output](references/background-job-output.md) |
| A call failed, timed out, was rejected, or a tool is missing | [Troubleshooting](references/troubleshooting.md) |
| Running the server, sharing jobs across clients, model bindings, environment variables | [Server configuration](references/server-config.md) |

Load only the reference the current step needs.

## Registration model

Do not assume a fixed tool count; registration follows configuration. Check
the live tool list, `ark_job_capabilities`, or `seed-health://status` before
promising a capability.

| Configuration | Tools |
|---|---|
| Always | `seed_media_get_artifact`, `seed_media_export_artifact`, `seed_media_persist_url`, `ark_job_capabilities`, `ark_job_submit`, `ark_job_get`, `ark_job_cancel`, resource `seed-health://status` |
| `BYTEPLUS_MODELARK_API_KEY` | `seedream_generate_image`, `seedream_edit_image`, `seedream_generate_image_variations`, `seedance_create_task`, `seedance_create_task_variations`, `seedance_2_5_create_task`, `seedance_2_5_create_task_variations`, shared `seedance_get_task`, `seedance_get_tasks`, `seedance_list_tasks`, `seedance_cancel_or_delete_task`, `seed_understand`, `seed_audio_understand` |
| + `BYTEPLUS_MODELARK_SEEDANCE_2_5_PREMIUM_ENABLED=true` (whitelist-only) | `seedance_2_5_premium_create_task`, `seedance_2_5_premium_create_task_variations` |
| + `BYTEPLUS_MODELARK_3D_ENABLED=true` | `hyper3d_*` and `hitem3d_*` create, get, list, cancel/delete |
| `BYTEPLUS_SEED_SPEECH_API_KEY` | `seed_audio_generate`, `seed_audio_generate_variations`, `speech_to_text` |
| `BYTEPLUS_VOD_MEDIAKIT_API_KEY` | `vod_enhance_video`, `vod_transcode_video`, `vod_add_subtitles`, `vod_remove_subtitles`, `vod_separate_audio`, and their `vod_get_*` polls |
| `BYTEPLUS_MODELARK_ACCESS_KEY` + `_SECRET_KEY` | `ark_asset_*` group and asset tools |
| TOS or S3 credentials | `media_upload`, `media_upload_batch`, `media_presign`, `media_presign_batch` |

## Default path: background jobs

Long-running tools require background execution. A direct foreground call is
rejected before the provider is contacted. These are:

- `media_upload`, `media_upload_batch`
- `seed_audio_generate`, `seed_audio_generate_variations`, `speech_to_text`
- `seedream_generate_image`, `seedream_edit_image`,
  `seedream_generate_image_variations`
- every `seedance_*create_task*` tool (2.0, 2.5, Premium, and variations)
- `hyper3d_create_task`, `hitem3d_create_task`
- `seed_understand`, `seed_audio_understand`
- `vod_enhance_video`, `vod_transcode_video`, `vod_separate_audio`,
  `vod_add_subtitles`, `vod_remove_subtitles`

**Use the ordinary `ark_job_*` tools unless native MCP task support for the
current client is positively confirmed.** Discovering tools does not prove
native task support.

1. Call `ark_job_capabilities` and pick a listed target. Unknown or
   unauthorized targets are unavailable. The result is large; parse the saved
   file (see [Background-job output](references/background-job-output.md)).
2. Call `ark_job_submit`. The target tool's own arguments, which are normally
   `{"input": {...}}`, go under `arguments`:

   ```json
   {
     "input": {
       "tool_name": "seedance_2_5_create_task",
       "arguments": {
         "input": {
           "prompt": "...",
           "draft": true,
           "resolution": "480p",
           "ratio": "16:9",
           "duration": 10,
           "generate_audio": true,
           "watermark": false
         }
       }
     }
   }
   ```

   Snippets in the references show only the contents of the outer `input`
   (`{"tool_name": ..., "arguments": ...}`); wrap them in `{"input": ...}`
   when calling `ark_job_submit`.

3. Keep the returned Ark `job_id` and poll `ark_job_get` (`{"input":
   {"job_id": "..."}}`) no faster than `poll_after_ms`.
4. At a terminal status, read the original tool result from `result`; the
   typed payload is `result.structured_content`. For Seedance, Seed 3D, and
   MediaKit it contains the **provider task ID**.
5. Call `ark_job_cancel` only when cooperative local cancellation is intended.

A client that negotiated MCP `2026-07-28` and the
`io.modelcontextprotocol/tasks` extension may instead call the tool directly
with task metadata and poll `tasks/get`. Both paths run the same handler and
return the same payload. In this skill, "run in the background" means either
path, and "background result" means the terminal `ark_job_get.result` or
`tasks/get` response.

### Job IDs, provider IDs, and resubmission

- **Never confuse the Ark job ID with a provider task ID.** Record both in one
  registry write as soon as the provider ID appears.
- **A server restart loses Ark job IDs; provider task IDs survive** and can be
  polled with `seedance_get_task`, `hyper3d_get_task`, `hitem3d_get_task`, or
  the `vod_get_*` tool. Local stdio jobs are also process-local: another
  client cannot see them.
- **Never resubmit because a response was lost.** After a timeout, disconnect,
  or ambiguous provider error, reconcile first. The only safe automatic
  resubmission is a direct required-task call that was rejected for lacking
  task support.
- Required-task execution is claimed once in the runtime database, so an
  interrupted task cannot silently replay paid work.

### Foreground tools and optional background

List, presign, artifact-read, and cancel/delete tools are foreground. The
Seedance, Seed 3D, and MediaKit get tools and `seed_media_persist_url` support
optional background execution: poll in the foreground with
`persist_output=false`, then fetch the finished output with
`persist_output=true` in the background so download cannot exhaust the client
deadline. If that fails with "session is not available", download the
provider URL yourself (see
[Background-job output](references/background-job-output.md)).

## Persistence and artifacts

Generation tools default to `persist=true` and return an `ArtifactRef`
(`uri` such as `seed-media://artifacts/<id>`, `sha256`, `bytes`,
`mime_type`). Artifacts survive provider URL expiry for
`ARTIFACT_TTL_SECONDS` (default 7 days). The project folder, not the artifact
cache, holds the durable copy.

### Local writes

On stdio, these options write output straight to disk:

- `output_path` (file, or directory ending `/`) on `seedream_generate_image`,
  `seedream_edit_image`, `seed_audio_generate`, `seedance_get_task`,
  `hyper3d_get_task`, `hitem3d_get_task`, and the `vod_get_*` tools.
- `output_dir` on `seedream_generate_image_variations`,
  `seed_audio_generate_variations`, and `seedance_get_tasks`.
- `save_to` on `seed_understand` and `seed_audio_understand`.

Paths must be absolute and inside the client's MCP roots, or `OUTPUT_ROOTS`
when the client has none; with neither, path writing is disabled. They require
`persist=true` / `persist_output=true` and are validated before any provider
call. Each written `ArtifactRef` reports `local_path`, or `export_error` if
the write failed (the durable artifact is kept).

**Inside `ark_job_submit` these options can fail with "session is not
available."** Do not pass `output_path` to Seedream or Seed Audio, or
`save_to` to understanding, through `ark_job_submit` unless native task
support is confirmed. Persist server-side and export afterwards.

### Artifact tools

| Tool | Use | Key inputs | Returns |
|---|---|---|---|
| `seed_media_get_artifact` | Inline Base64 of a persisted artifact (small files only) | `artifact_id` | `media_type`, `mime_type`, `sha256`, `bytes`, `expires_at`, `data` |
| `seed_media_export_artifact` | Locate or copy an artifact on disk (stdio only) | `artifact_id`, optional absolute `destination_path` inside an output root, `overwrite` | `path`, `sha256`, `bytes`, `copied` |
| `seed_media_persist_url` | Store a temporary provider URL after `persistence_error` | `url`, `media_type` (`image`/`audio`/`video`/`three_d`), `mime_type`, optional `source_expires_at` | new `artifact` |

- With no output root, call `seed_media_export_artifact` without
  `destination_path`. It returns the store path
  (`<workspace>/.artifacts/<first two id characters>/<id>.<ext>`). Copy that
  file into the project and compare its SHA-256 with the generation result
  before use. `.artifacts/` is a gitignored cache.
- An existing destination is never silently overwritten; identical content
  counts as success.
- `seed_media_persist_url` accepts only trusted BytePlus provider hosts. Call
  it before the URL expires.
- JWT scopes: `artifacts:read` (get, export), `media:upload` (persist URL).

### Billed outputs are never dropped

When storage fails after download retries, the `ArtifactRef` carries
`persistence_error` (`code`, `message`, `retryable`, `artifact_limit_bytes`,
`source_url_expires_at`) and is either:

- `id="provider-url"`: `uri` is the temporary provider URL; recover it with
  `seed_media_persist_url`; or
- `id="inline-fallback"`: Base64 bytes in `fallback_data` (Seed Audio, or
  Seedream with `b64_json`).

Seedream storage failures are successes with `persistence_error`, not tool
errors, so always check the field.

### Resources

- `seed-media://artifacts/{artifact_id}`: the persisted media with its MIME
  type (`artifacts:read` in JWT mode).
- `seed-health://status`: unauthenticated summary of configured products,
  artifact backend, and transport.

## Records and review

Use explicit states so a generated take is never mistaken for an approved
one: `ready → submitted → queued/running → review → approved/rejected`, plus
`failed`, `cancelled`, `expired`. Provider success sets `review`. Record, for
every operation:

- Ark job ID and provider task ID as separate fields;
- request parameters and prompt hash, and reference hashes;
- artifact ID or download source, local path, bytes, SHA-256, and actual media
  properties from `ffprobe` or inspection;
- estimated cost separately from confirmed usage or billing.

While a take is under review, record it under `outputs` or
`generated_output`; reserve `selected_variant` and `approved` for a
mode-authorized, hash-bound decision after review passes.

If the provider returns null or incomplete settings, keep the submitted
request as the source of intended parameters and inspection as the source of
actual properties. Media QA steps live in
[Seedance tasks](references/seedance-tasks.md) and [Seed 3D](references/3d.md).

## Practices

1. **Check registration first.** Verify the product is configured and the
   live schema carries the fields you plan to send. Do not send fields the
   live tool lacks; for example, the Seedance create tools may expose no
   `camera_fixed` or `seed`.
2. **Draft Seedance 2.5 first.** Submit `draft: true` (480p), review, then
   promote with `draft_task_id` only. Details and constraints in
   [Seedance creation](references/seedance.md).
3. **Poll at the advertised interval** (`recommended_poll_after_ms`,
   `poll_after_ms`) and relay `queue.hint`; ModelArk publishes no queue
   position or ETA.
4. **Make polling resumable.** Save both IDs before the first provider poll;
   a client timeout continues the existing job.
5. **Batch instead of looping.** `media_upload_batch`,
   `media_presign_batch`, and `seedance_get_tasks` (stop on `all_terminal`).
6. **Use variation tools for choice.** They run in parallel and capture
   partial failures (`error.phase`: `queued` safe to retry; `generating`
   reconcile first; `persisting` billed but unstored).
7. **Upload once, presign per shot.** Store `object_key`s; presign right
   before submission. See [Object storage](references/object-storage.md).
8. **Respect input limits.** Image and audio references ≤ 10 MiB; video
   references ≤ 200 MiB and URL-only.
9. **Use the right authority for words.** `speech_to_text` with a local file
   path for exact words; `seed_audio_understand` for summaries only.
10. **Verify saved media.** Provider success proves only that generation
    finished, not that resolution, audio, continuity, or playback meet the
    brief.
11. **Clean up only in scope.** Cancel or delete provider tasks and assets only
    when cleanup is explicitly requested.
