# Errors, retries, and common issues

Load this when a call fails, times out, is rejected, or a tool is missing, and
before deciding whether anything may be retried.

## Provider errors

Provider errors are normalized into `ProviderError` with the provider's HTTP
status, error code, and a readable message. Keep the code and any request ID
in the operation record.

## Retry policy

The server retries only explicitly retryable, non-ambiguous errors:
connection/transport errors (up to 3 attempts, exponential backoff with
jitter, 0.25 s base, 4 s max) and provider errors with `retryable=true`.

| Call | Timeout error | Server retries? | What you do |
|---|---|---|---|
| Create / generate / cancel / delete / MediaKit submit | `retryable=false`, `ambiguous_completion=true` | No | It may have succeeded. Reconcile by task or request ID; never resubmit blindly. |
| Task polls (Seedance, Seed 3D, ASR query, MediaKit get) | `retryable=true`, `ambiguous_completion=false` | Yes | Keep polling the same ID. |
| `seed_understand` / `seed_audio_understand` | `retryable=true`, `ambiguous_completion=false` | No | Safe to retry yourself; each retry is billed. Raise `SEED_UNDERSTANDING_TIMEOUT_MS` for long work. |

- Any `TIMEOUT` commits the budget reservation; it may have been billed.
- Output downloads retry separately (`ARTIFACT_DOWNLOAD_MAX_ATTEMPTS`, default
  3, 1 s / 2 s / 4 s backoff); expired, untrusted, or oversized sources do not.
- MediaKit submissions are never retried automatically; MediaKit polls are
  retried on 429/5xx, poll timeouts, and connection failures.
- A local watcher timeout is not a generation failure. Resume
  `seedance_get_task`, `hyper3d_get_task`, or `hitem3d_get_task` with the
  existing ID. Create a new task only after the previous one is terminal and a
  new take is in scope.
- `speech_to_text` polls internally to `SEED_SPEECH_ASR_POLL_MAX_SECONDS`; a
  timeout yields no partial result.
- A direct required-task call from a client without task support is rejected
  before the provider is contacted, so resubmitting that exact work through
  `ark_job_submit` is safe.

## Budget rejections

With `DAILY_BUDGET_USD` above zero, requests over the per-principal daily
budget are rejected with a clear message. `0` (default) records spend without
enforcement. Wait for the UTC day rollover or raise the budget.

## Content rejections

- An output audit (`decision_in_reject_list`, code `55001310`) reported with
  `ambiguous_completion=True` is a terminal content rejection with no artifact
  and no provider task to reconcile. Mark it `terminal` / `failed`, diagnose,
  and never repeat the identical request.
- Input privacy rejections (`PrivacyInformation`) on faces, likeness, or
  voices recover through authorized `asset://` references; see
  [Assets and rights](assets-and-rights.md) and
  [Seedance creation](seedance.md).
- Moderation rejection is evidence to diagnose, not proof of a false positive.

## Common issues

| Symptom | Cause | Resolution |
|---|---|---|
| Tool not listed | Missing API key or feature flag | Set the `BYTEPLUS_*` key; Premium and 3D also need their `*_ENABLED=true` flags (Premium is whitelist-only) |
| Model not found | Unbound custom model ID | Add it to the matching `*_MODEL_BINDINGS` JSON |
| Ark job ID unknown after restart | `ark_job_*` jobs are process-local | Poll the recorded provider task ID directly; see [Seedance tasks](seedance-tasks.md) |
| "session is not available" in a job | Local-write option inside `ark_job_submit` | Omit `output_path` / `output_dir` / `save_to`; see [Background-job output](background-job-output.md) |
| `output_path` / `save_to` rejected | No MCP roots and no `OUTPUT_ROOTS`, relative path, outside roots, HTTP transport, or `persist=false` | Use an absolute path inside a root on stdio, set `OUTPUT_ROOTS`, or omit and export |
| Provider URL expired | 2 h audio / 24 h image, video, 3D, MediaKit | Use durable artifacts; persist promptly |
| Artifact has `persistence_error` | Billed output; storage failed after retries | `provider-url`: `seed_media_persist_url` before `source_url_expires_at`; `inline-fallback`: bytes in `fallback_data` |
| `InvalidParameter.TaskTypeConstraint` | Ratio sent on extend, or a 2.0 task type (`edit_video`) on 2.5 | Omit `ratio` for `edit`/`extend`; use 2.5 values `edit` / `extend` |
| Draft promotion rejected | Prompt, media, ratio, duration, or audio fields sent with `draft_task_id`, or Draft older than 7 days | Send only `draft_task_id`, `resolution`, `watermark` (plus optional output settings) |
| `seed_understand` answer too large | Long inline answer | `return_content: "summary"` / `"none"`; read `parsed` |
| No `reasoning_content` | Removed by design | Use `content` / `parsed`; `usage.reasoning_tokens` shows cost |
| Variation `QUEUE_TIMEOUT` | Never started before the batch deadline | Safe to retry that variation |
| `speech_to_text` rejects the URL | Presigned object-storage host treated as untrusted | Pass `audio_file_path` |
| `speech_to_text` code `20000003` | Silent audio or format mismatch (non-16 kHz/16-bit/mono WAV) | Verify speech and `audio_format`; resubmit corrected audio |
| `speech_to_text` timeout | ASR poll cap reached | Raise `SEED_SPEECH_ASR_POLL_MAX_SECONDS` or send shorter audio |
| Upload or presign tools missing | No TOS/S3 credentials | Set `TOS_*` or `S3_*` and `OBJECT_STORAGE_BACKEND` |
| Presigned URL expired | TTL elapsed (default 30 min) | `media_presign` / `media_presign_batch` with the stored `object_key` |
| VOD or 3D task `AbilityProcessingError` | Usually transient | Resubmit the same source |
| Auth error (JWT mode) | Missing or invalid token or scope | Check JWT configuration and scopes |
| 3D package wrong scale or missing materials | Unit, axis, format, or texture assumptions | Import to quarantine, measure, normalize a working copy; see [3D](3d.md) |
