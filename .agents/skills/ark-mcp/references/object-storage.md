# Object storage upload and presign

Load this when local or Base64 media must become an HTTPS URL (Seedance video
references, `seed_understand` video, VOD sources, asset sources), or when you
reuse uploaded references across shots.

Requires TOS or S3 credentials (`OBJECT_STORAGE_BACKEND`, default TOS). In JWT
mode the scopes are `media:upload` and `media:presign`. `media_upload` and
`media_upload_batch` require background execution through `ark_job_submit`;
the presign tools are foreground.

## `media_upload`

| Parameter | Notes |
|---|---|
| `media_type` | `image`, `audio`, or `video` (required) |
| `mime_type` | e.g. `video/mp4`, `image/png`, `audio/wav` (required) |
| `file_path` | Absolute local path; stdio only; exclusive with `data` |
| `data` | Base64 bytes; exclusive with `file_path` |
| `key_prefix` | Default `references`; letters, digits, `-`, `_`, `/` |
| `expires_in_seconds` | 60–604800; default is the configured presign TTL (1800). Use 3600+ for VOD sources. |

Returns `url`, `expires_at`, `object_key`, `bytes`.

```json
{"tool_name": "media_upload",
 "arguments": {"input": {"media_type": "video", "mime_type": "video/mp4",
                         "file_path": "/absolute/path/clip.mp4"}}}
```

## `media_upload_batch`

1–50 files in one call.

| Parameter | Notes |
|---|---|
| `items` | Each with `media_type`, `mime_type` (optional for `file_path` items; inferred from extension), `data` or `file_path`, optional `key_prefix` |
| `expires_in_seconds` | Applied to every item |
| `max_concurrent` | 1–8, default 4 |

Total decoded size is checked against `MEDIA_UPLOAD_BATCH_MAX_BYTES` (default
500 MiB) before anything uploads. Returns per-item `index`, `file_path`, `url`,
`object_key`, `expires_at`, `mime_type`, `bytes`, `error`, `retryable`, plus
`succeeded`, `failed`, `total_bytes`. Items fail independently.

## `media_presign` / `media_presign_batch`

Fresh presigned GET URLs for existing objects, without re-uploading.

| Tool | Input | Returns |
|---|---|---|
| `media_presign` | `object_key`, optional `expires_in_seconds` | `url`, `expires_at`, `object_key` |
| `media_presign_batch` | `object_keys` (1–100), optional `expires_in_seconds` | per-key `object_key`, `url`, `expires_at`, `code`, `error`, `request_id`; `succeeded`, `failed` |

Batch failures are per key (`INVALID_KEY`, `NOT_OWNED`, `INTERNAL`, or a
provider code) while the rest succeed.

## Reuse references across shots

Presigned URLs expire (default 30 min) but the object persists.

1. **Upload once.** Store each reference's `object_key` with its content hash
   and storage scope in the project's reference cache.
2. **Presign on demand.** Before each submission, presign the stored keys with
   `media_presign_batch`, then submit immediately while the URLs are valid.
3. Re-upload only when the content hash changes.

This turns minutes of re-uploading per shot into seconds of presigning and
avoids duplicate storage. Signed URLs are transport data: never commit them
or treat them as durable identifiers.

## Limits and caveats

- Image and audio references are limited to 10 MiB each; video references to
  200 MiB. Base64 inputs are validated before submission.
- `speech_to_text` rejected presigned object-storage URLs as an untrusted host
  in this workspace; pass a local file path instead.
- VOD tools fetch sources asynchronously; use a long `expires_in_seconds`.
