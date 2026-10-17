# Server setup, architecture, and configuration

Load this when you install or run the server, share jobs across clients,
diagnose which products are registered, bind custom models, or look up an
environment variable. Never print or commit key values.

## Run the server

Prerequisites: Python 3.12+, `uv`, and BytePlus keys for the products you use.
Copy `.env.example` to `.env` in the server checkout and set at least the keys
you need.

```bash
uv run python -m ark_mcp                       # stdio (default, local clients)
MCP_TRANSPORT=http uv run python -m ark_mcp    # Streamable HTTP on 127.0.0.1:3000
```

Verify with the `seed-health://status` resource or the `/health`, `/ready`,
and `/metrics` HTTP endpoints.

## Sharing jobs across clients

- Each local stdio client starts its own server process, so `ark_job_*` jobs
  are process-local and invisible to other clients.
- To share, run one loopback HTTP server (`make shared-http`) and connect every
  client to it; loopback clients are the same `local` principal and share the
  queue.
- The default in-memory backend discards jobs when the server restarts.
  Provider task IDs survive; record them as soon as they are known.
- JWT-authenticated Redis tasks require `FASTMCP_TASKS_ENCRYPTION_KEY`; keep
  the runtime database, queue, and encryption key together. Redis does not
  remove the single-replica limitation, and backend access controls must also
  protect task arguments and results.
- Native and ordinary jobs enforce the same tenant and principal ownership as
  provider tasks. Required-task execution is claimed once in the runtime
  database, so an interrupted task cannot silently replay paid work.

## Provider surfaces

| Provider | Auth | Base URL | Products |
|---|---|---|---|
| ModelArk | `Authorization: Bearer` | `https://ark.ap-southeast.bytepluses.com/api/v3` | Seedream, Seedance, Seed 3D, Seed 2.1 and audio understanding |
| Seed Speech | `X-Api-Key` | `https://voice.ap-southeast-1.bytepluses.com` | Seed Audio, Speech-to-Text |
| VOD AI MediaKit | `Authorization: Bearer` | `https://mediakit.ap-southeast-1.bytepluses.com/api/v1` | Enhance, transcode, subtitles, audio separation |

One Seed Speech key covers Seed Audio and ASR (distinguished by
`X-Api-Resource-Id`). The ModelArk key covers its products; 3D and Premium also
need feature flags. MediaKit uses a third key. The asset library uses IAM
AK/SK.

## Runtime services

- **Artifact store:** filesystem-backed, ownership metadata, TTL cleanup
  (`ARTIFACT_TTL_SECONDS`, default 7 days).
- **Budget ledger:** SQLite per-principal daily spend.
- **Task ownership store:** SQLite task-to-principal mapping for Seedance and
  Seed 3D.
- **Provider limiters:** per-provider semaphore (default 5) for every call,
  plus a per-principal semaphore (default 3) for authenticated JWT HTTP
  principals only.
- **Safe downloader:** SSRF-safe downloads with IP pinning and redirect
  validation.

## Model capability registry

The server validates inputs against known capabilities before spending quota.

| Family | Default model ID | Traits |
|---|---|---|
| Seedream Pro | `dola-seedream-5-0-pro-260628` | 10 refs, no batch, PNG/JPEG |
| Seedream Lite | via `SEEDREAM_MODEL_BINDINGS` | 14 refs, batch, PNG/JPEG |
| Seedream 4.x | via `SEEDREAM_MODEL_BINDINGS` | 14 refs, batch, JPEG only |
| Seedance 2.5 Premium | `dreamina-seedance-2-5-premium-260915` | 2.5 plus 4k; whitelist and flag gated |
| Seedance 2.5 | `dreamina-seedance-2-5-260628` | 30/10/10 refs, 480p–1080p, ≤ 30 s, editing, extension, Draft |
| Seedance 2.0 Standard | `dreamina-seedance-2-0-260128` | 9/3/3 refs, 480p–4k, ≤ 15 s |
| Seedance 2.0 Fast / Mini | via `SEEDANCE_MODEL_BINDINGS` | 480p and 720p only |
| Seed 2.1 Turbo | `dola-seed-2-1-turbo-260628` | 256K context, images + videos, thinking |
| Seed 2.1 Pro | `dola-seed-evolving` (opt-in) | 256K context, images + videos, thinking |
| Hyper3D | `hyper3d-gen2-260112` | Text/image-to-3D, 5 images, seeds |
| Hitem3d | `hitem3d-2-0-251223` | Image-to-3D, 1–4 images |

`seed_audio_understand` is outside the registry: it calls
`SEED_AUDIO_UNDERSTANDING_MODEL` (default `seed-2-0-lite-260428`) with no
bindings or pre-validation. Custom model IDs must be bound via
`SEEDREAM_MODEL_BINDINGS`, `SEEDANCE_MODEL_BINDINGS`,
`SEED_UNDERSTANDING_MODEL_BINDINGS`, or `SEED3D_MODEL_BINDINGS` JSON. Omitting
`model` uses the product default.

## Environment variables

Provider credentials and hosts:

- `BYTEPLUS_MODELARK_API_KEY`, `BYTEPLUS_SEED_SPEECH_API_KEY`,
  `BYTEPLUS_VOD_MEDIAKIT_API_KEY`
- `BYTEPLUS_MODELARK_BASE_URL`, `BYTEPLUS_SEED_AUDIO_BASE_URL`,
  `SEED_SPEECH_ASR_BASE_URL`, `BYTEPLUS_VOD_MEDIAKIT_BASE_URL`
- `SEED_SPEECH_ASR_POLL_INTERVAL_SECONDS` (default 3),
  `SEED_SPEECH_ASR_POLL_MAX_SECONDS` (default 600)

Feature flags and models:

- `BYTEPLUS_MODELARK_SEEDANCE_2_5_PREMIUM_ENABLED` (default `false`),
  `SEEDANCE_2_5_PREMIUM_MODEL`
- `BYTEPLUS_MODELARK_3D_ENABLED` (default `false`), `HYPER3D_DEFAULT_MODEL`,
  `HITEM3D_DEFAULT_MODEL`, `SEED3D_MODEL_BINDINGS`
- `SEEDREAM_DEFAULT_MODEL`, `SEEDREAM_MODEL_FAMILY`, `SEEDREAM_MODEL_BINDINGS`,
  `SEEDREAM_PROMPT_OPTIMIZATION_MODE`
- `SEEDANCE_DEFAULT_MODEL`, `SEEDANCE_MODEL_FAMILY`, `SEEDANCE_MODEL_BINDINGS`
- `SEED_UNDERSTANDING_DEFAULT_MODEL`, `SEED_UNDERSTANDING_MODEL_FAMILY`,
  `SEED_UNDERSTANDING_MODEL_BINDINGS`, `SEED_AUDIO_UNDERSTANDING_MODEL`

Transport and auth: `MCP_TRANSPORT` / `FASTMCP_TRANSPORT`, `MCP_HOST` /
`FASTMCP_HOST`, `MCP_PORT` / `FASTMCP_PORT`, `MCP_ALLOWED_ORIGINS`,
`MCP_ALLOWED_HOSTS`, `MCP_AUTH_MODE`, `MCP_JWT_JWKS_URI`, `MCP_JWT_ISSUER`,
`MCP_JWT_AUDIENCE`, `MCP_TENANT_CLAIM`, `MCP_JWT_CLOCK_SKEW_SECONDS`,
`MCP_JWT_PROVIDE_DISCOVERY`, `MCP_PUBLIC_BASE_URL`, `MCP_JWT_SCOPES_SUPPORTED`.

HTTP rate limiting and readiness: `RATE_LIMIT_RPM`, `RATE_LIMIT_BURST`,
`RATE_LIMIT_TRUST_PROXY_HEADERS`, `READINESS_CHECK_PROVIDERS`,
`READINESS_PROVIDER_TIMEOUT_SECONDS`.

Persistence and runtime:

- `ARTIFACT_BACKEND`, `ARTIFACT_DIR`, `ARTIFACT_TTL_SECONDS`, `STATE_BACKEND`,
  `ARTIFACT_SWEEP_INTERVAL_SECONDS`, `STATE_PRUNE_MAX_AGE_DAYS`
- `MCP_INLINE_MEDIA_MAX_BYTES`, `MCP_HTTP_MAX_BODY_BYTES`
- `ARTIFACT_DOWNLOAD_TIMEOUT_SECONDS` (default 120),
  `ARTIFACT_DOWNLOAD_MAX_ATTEMPTS` (default 3),
  `ARTIFACT_INLINE_FALLBACK_MAX_BYTES` (default 8 MiB)
- `OUTPUT_ROOTS`: comma-separated absolute directories for local writes when
  the client advertises no MCP roots
- `SEED_UNDERSTANDING_TIMEOUT_MS` (defaults to `BYTEPLUS_REQUEST_TIMEOUT_MS`)
- `PROVIDER_MAX_CONCURRENCY`, `PRINCIPAL_MAX_CONCURRENCY`, `DAILY_BUDGET_USD`
- `PERSISTENCE_CACHE_MAX_SIZE`, `PERSISTENCE_CACHE_TTL_SECONDS`,
  `ARK_LOG_LEVEL`

Asset library: `BYTEPLUS_MODELARK_ACCESS_KEY`, `BYTEPLUS_MODELARK_SECRET_KEY`,
`BYTEPLUS_MODELARK_SESSION_TOKEN`, `BYTEPLUS_MODELARK_PROJECT_NAME`, and the
settings in [Assets and rights](assets-and-rights.md).

Object storage: `TOS_ACCESS_KEY`, `TOS_SECRET_KEY`, `TOS_SECURITY_TOKEN`,
`TOS_BUCKET`, `TOS_REGION`, `TOS_ENDPOINT`, `TOS_PRESIGN_TTL_SECONDS`,
`S3_ACCESS_KEY`, `S3_SECRET_KEY`, `S3_BUCKET`, `S3_REGION`, `S3_ENDPOINT`,
`S3_PRESIGN_TTL_SECONDS`, `OBJECT_STORAGE_BACKEND`,
`MEDIA_UPLOAD_BATCH_MAX_BYTES` (default 500 MiB).
