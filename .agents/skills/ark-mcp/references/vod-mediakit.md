# VOD AI MediaKit

Load this when you enhance, transcode, burn in or remove subtitles, or
separate voice from background audio with the `vod_*` tools.

Requires `BYTEPLUS_VOD_MEDIAKIT_API_KEY`. Scopes: `vod:enhance`,
`vod:transcode`, `vod:subtitle:add`, `vod:subtitle:remove`, `vod:extract`
(submit tools) and `vod:read` (poll tools).

## Shared contract

- Every operation is **submit-then-poll**. Run the submit tool in the
  background through `ark_job_submit`, read the provider `task_id` from
  `result.structured_content`, then poll the matching get tool. Never poll one
  operation with another operation's get tool.
- Submit tools are mutating, non-idempotent, and open-world. The server never
  retries them, and neither should you after a timeout or 5xx: completion may
  be ambiguous. Re-poll the task ID, or reconcile with a stable
  `client_token` (subtitle tools).
- Get tools are read-only and retried on 429/5xx, poll timeouts, and
  connection failures. They map provider `running` → `processing`,
  `completed` → `succeeded`, `failed` → `failed`; there are no
  queued/expired/cancelled states.
- Sources must be **public HTTPS URLs**; private and link-local targets are
  rejected. The provider fetches asynchronously, so the URL must stay live
  until it downloads. A default presigned URL (30 min) can expire first: upload
  with `media_upload` and `expires_in_seconds` of 3600 or more, or use a stable
  URL.
- Outputs carry a 24 h `source_url`. Poll in the foreground with
  `persist_output: false`; after success, poll again in the background with
  `persist_output: true` for a best-effort durable copy (200 MiB cap, cached by
  task ID). Keep `source_url` even when the copy fails; inspect `persistence`
  (`not_applicable`, `persisted`, `failed`, `not_requested`) and
  `persistence_issue`. A persistence failure never erases provider success.
- `estimated_cost_usd` stays null until pricing is confirmed; do not present
  it as available.

## `vod_enhance_video` / `vod_get_enhancement_task`

Enhances with the single currently supported profile.

| Parameter | Value |
|---|---|
| `video_url` | Public HTTPS source (required) |
| `scene` | `common` (fixed) |
| `tool_version` | `professional` (fixed) |
| `resolution` | `4k` (fixed) |
| `bitrate_level` | `high` (fixed) |
| `fps` | `24` (fixed) |
| `project` | Optional; default `default`, sent as `Project` |
| `input_duration_seconds` | Reserved; no estimate is produced |
| `persist` | Default `true` |

The submit result is `status="accepted"` with `task_id`. The poll requires
`task_type="enhance-video"` and on success returns `source_url`, duration,
resolution, frame rate, enhancement tier, and normalized timestamps.

## `vod_transcode_video` / `vod_get_transcode_task`

Defaults reproduce a portrait-to-720x720 letterbox profile
(`scale_type=2`, `scale_width=720`, `scale_height=720`, `scale_mode=2`); set
the fields below to target another output.

| Parameter | Notes |
|---|---|
| `video_url` | Public HTTPS source (required) |
| `container_format` | `MP4` (default), `FLV`, `MPEGTS` |
| `video` | Object; fields below |
| `persist` | Default `true` |

`video` fields: `codec` (`h264` default, `h265`); `scale_type` (`0`/`1`/`2`,
default `2`); `scale_mode` (`0`/`1`/`2`, default `2`);
`scale_width` / `scale_height` (0–4320 px, only with `scale_type=2`, default
720); `scale_short` / `scale_long` (0–4320 px, only with `scale_type=1`);
`bitrate_mode` (`crf` default, `abr`, `cbr`); `bitrate_crf` (0–51, default
25); `bitrate_kbps` (10–50000, default 2000); `fps_mode` (`vfr` default,
`cfr`); `fps` (1–240; unset keeps the source rate); `is_hdr_to_sdr` (default
`true`).

Submit returns `task_id` and a heuristic `recommended_poll_after_ms`. The
poll returns `source_url` plus optional `duration_seconds`, `resolution`,
`video_codec`, and ISO-8601 `created_at` / `finished_at` /
`source_expires_at`; on failure, `error` carries the safe provider detail.

## `vod_add_subtitles` / `vod_get_subtitle_addition_task`

Burns an SRT/VTT/ASS file or inline timed cues into a video.

- Provide `subtitle_url` or `subtitles` (the file URL wins if both are set).
- Inline cues need nonblank `subtitle_text`, a nonnegative `start_time`, and a
  later `end_time`.
- Optional position, font size, RGBA colour, and font identifier control
  styling. Callback and queue fields are supported.
- The poll requires `task_type="add-subtitle-to-video"`.

## `vod_remove_subtitles` / `vod_get_subtitle_removal_task`

Precision erasure of burned-in text.

- `subtitle` mode (default) targets dialogue subtitles; `text` mode is broader
  and may erase titles, labels, or watermarks. Prefer `subtitle` unless the
  broader effect is intended.
- Optional normalized rectangles, selected/skipped time segments, and OCR
  thresholds constrain processing.
- `project` and removal `model_version` are optional legacy extensions,
  omitted by default.
- The poll requires `task_type="erase-video-subtitle-pro"`.

## `vod_separate_audio` / `vod_get_audio_separation`

Voice and background separation (`POST /api/v1/tools/separate-voice`).

| Parameter | Notes |
|---|---|
| `audio_url` | Exactly one of `audio_url` / `video_url`; mp3, m4a, wav |
| `video_url` | mp4, flv, ts, avi, mov, wmv, mkv |
| `scene` | `Audio` (default) or `Music` = 2 tracks; `Drama` or `Narrate` = 3 tracks |
| `output_format` | `aac` (default), `mp3`, `wav`, `m4a`, `flac` |

Submit returns `task_id`, `request_id`, and `provider_log_id`. The poll takes
`task_id` and `persist_output` (default `true`, requires background
execution). On success, `voice`, `background`, `music`, and `sfx` each carry
a 24 h `source_url` and, when persisted, a durable `artifact`.

- Separation usually takes tens of seconds but can take minutes; keep polling
  to a terminal state.
- A provider `failed` with `AbilityProcessingError` or `InternalError` is
  usually transient: resubmit the same source rather than treating the input
  as invalid.
