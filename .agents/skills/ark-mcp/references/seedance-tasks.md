# Seedance task lifecycle

Load this after a Seedance create call returns: polling, batch status,
downloading and persisting the video, resuming after a timeout or server
restart, cleanup, and post-generation media QA. Request building lives in
[Seedance creation](seedance.md).

The get, list, and cancel tools are shared across 2.0, 2.5, and 2.5 Premium
task IDs.

```text
queued -> running -> succeeded | failed | cancelled | expired
```

## Workflow

1. Submit the create tool through `ark_job_submit` and poll `ark_job_get`.
2. **Record both IDs at once**: the Ark `job_id` and, from
   `result.structured_content`, the provider `task_id`, together with request
   parameters, prompt hash, and intended output path, before the first provider
   poll.
3. Poll `seedance_get_task` in the foreground with `persist_output: false`
   (or `seedance_get_tasks` for several tasks until `all_terminal`). Respect
   `recommended_poll_after_ms`. While queued, relay `queue.hint`; ModelArk
   publishes **no queue position or ETA**.
4. On a local timeout, disconnect, or client restart, keep polling the same
   provider task. Never submit a replacement while the provider may still be
   running.
5. On success, save the video locally (see Persist the output), then record
   artifact ID or download source, local path, bytes, SHA-256, provider
   timestamps, and usage.
6. Run media QA, then set the take to `review`. Provider success is not
   approval.
7. Use `seedance_list_tasks` to browse; call `seedance_cancel_or_delete_task`
   only when cleanup is explicitly in scope.

## Server restart

`ark_job_*` jobs live in the server process. A restart of the ark-mcp server
(or a new stdio client process) loses Ark job IDs, but provider task IDs
survive on ModelArk and can still be polled with `seedance_get_task`. This is
why step 2 records the provider `task_id` the moment it is known. If a job is
lost before its provider ID was read, reconcile with `seedance_list_tasks`
(filter by time, model, or status) before any resubmission.

## Persist the output

Preferred, when local writes work on the current transport: run
`seedance_get_task` in the background with `persist_output: true` and
`output_path` set to the project file (or `seedance_get_tasks` with
`output_dir`). The last frame is written beside the video with a
`-last-frame` suffix.

`seedance_get_task` can fail to write local files when no output roots are
configured, and a background job can fail with "session is not available".
The reliable route is:

1. Poll in the foreground with `persist_output: false`.
2. Read `settings.video_url` (valid about 24 h) from the result.
3. Download it to the project path with an HTTPS client.
4. Record bytes, SHA-256, and `ffprobe` properties. Set the artifact `source`
   to the provider-URL download; there is no durable MCP artifact ID.

If an artifact carries `persistence_error` with `id="provider-url"`, recover it
with `seed_media_persist_url` before the 24 h URL expires. Details:
[Background-job output](background-job-output.md).

## Tools

### `seedance_get_task`

| Parameter | Type | Notes |
|---|---|---|
| `task_id` | `str` | Provider task ID from the create tool's background result |
| `persist_output` | `bool` | Default `true`, which requires background execution; use `false` for foreground polling |
| `output_path` | `str` | Local file, or directory ending `/`; stdio only; requires `persist_output: true` |
| `overwrite` | `bool` | Default `false` |

Returns `task_id`, `model`, `created_at`, `updated_at`, `status`, optional
`error`, optional `video` and `last_frame` (`ArtifactRef`), optional `usage`,
`settings`, and `queue`. Results are cached for 24 h after first persistence.

`queue` (queued/running only; `null` once finished) holds `queued_seconds`,
`running_seconds`, `service_tier`, `expires_at`, `expires_at_estimated` (48 h
default assumed), and `hint`.

If the provider returns null or incomplete `settings`, treat the submitted
request as the source of intended parameters and media inspection as the
source of actual output properties.

### `seedance_get_tasks`

Check 1–50 tasks in one call; prefer it over a loop after variations or
multi-shot work. One provider list call per page of 20 IDs.

| Parameter | Type | Notes |
|---|---|---|
| `task_ids` | `list[str]` | 1–50; duplicates ignored |
| `persist_output` | `bool` | Default **`false`**; `true` requires background execution |
| `output_dir` | `str` | stdio only; requires `persist_output: true` |
| `overwrite` | `bool` | Default `false` |

Returns `tasks` (request order), `errors` (`task_id`, `code`: `NOT_OWNED` /
`NOT_FOUND` / provider code, `message`), `counts`, `all_terminal`, and
`active_tasks`. Stop when `all_terminal` is `true`.

### `seedance_list_tasks`

Last 7 days. Filters: `page` (1–500), `page_size` (1–100), `status`,
`task_ids`, `model`, `service_tier` (`default` \| `flex`). Returns paginated
summaries with the same `queue` timing.

### `seedance_cancel_or_delete_task`

**Destructive**; requires explicit cleanup scope.

| Parameter | Notes |
|---|---|
| `task_id` | Task to act on |
| `mode` | `cancel` (with `expected_status: queued`) or `delete` (with `succeeded`, `failed`, or `expired`) |
| `expected_status` | Must match the current status |
| `confirm` | Must be `true` |

## Variations

Variation tools return per-variation provider task IDs inside one background
result; read the terminal result before polling each ID. There is no
per-variation timeout; one batch deadline bounds the call. `error.phase` is
`queued` (`QUEUE_TIMEOUT`, safe to retry), `generating` (may have completed;
reconcile first), or `persisting` (billed output not stored).

## Post-generation media QA

1. `ffprobe` the file: resolution, duration, frame rate, codecs, pixel format,
   audio streams.
2. Decode the whole file with FFmpeg; any decode error fails QA.
3. Watch the complete video at normal speed; inspect critical motion, timing,
   camera, transitions, and audio directly.
4. Use contact sheets around the opening, major transitions, and ending for
   appearance only, never as temporal evidence. Crop frame edges and corners to
   catch stray text, panel numbers, or drawn side bars.
5. Check story acceptance criteria: subject order and counts, travel
   direction, boundary behaviour, forbidden elements, final location.
6. When audio is enabled, verify the stream and listen to important segments;
   use `speech_to_text` for exact words. A promoted Draft final needs its own
   audio check.
7. Set the record to `review`. Approval needs a passing review and a
   mode-authorized decision.
8. For HEVC or other review-host-sensitive masters, optionally make a
   lightweight H.264 proxy and keep the original master.
