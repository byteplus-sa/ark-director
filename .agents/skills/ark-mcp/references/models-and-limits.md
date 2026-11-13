# Models and limits

Model discovery with `ark_list_models`, how the server binds model IDs to families, and the per-family limits for Seedance, Seedream, Seed 3D, and Seed 2.1 understanding. **This file is the one place per-family numbers live.** For the configured server, **`ark_list_models` is authoritative**: bindings are operator-configured, so a deployment can list fewer, more, or differently named models than the tables below. Tool parameters are in the tool schemas (see [API reference](https://byteplus-sa.github.io/ark-mcp/api-reference/)).

## Discovery with `ark_list_models`

- **Cached pricing:** `models[].pricing` carries account catalog rates when a
  fresh snapshot exists; unmatched or stale prices are null. `pricing_status`
  and `pricing_note` explain availability. Discovery never calls the provider.
  AK/SK and `BYTEPLUS_MODELARK_PRICING_REFRESH_SECONDS>0` enable the background
  refresher. Image/understanding estimates use recognized fresh rates; other
  estimates and unknown endpoint IDs retain built-in fallback rates.

**Call it before any generation or understanding tool.** It is read-only and idempotent, needs no auth scope, and **makes no provider calls**; it reads the server's own configuration.

- **`kind`** (`video`, `image`, `3d`, `understanding`) filters the list; omit it to get every configured kind.
- **`models[]`** has one entry per configured model whose service is enabled (empty when ModelArk is not configured; `3d` models appear only when 3D is enabled). Each entry carries `model_id`, `family`, `kind`, `is_default`, `tool`, and one limits object (`video`, `image`, `seed3d`, or `understanding`).
- **`model_id` is the exact value the `model` argument accepts.** Omitting `model` uses the entry with `is_default: true`.
- **`tool`** names the tool that serves the model. Understanding modalities and media limits describe this route, not every possible use of the underlying model. `seed_audio_understand` advertises only `audio` (up to eight clips); use `seed_understand` for images/videos. Neither handler accepts mixed audio/visual requests.
- **`services[]`** reports each optional service with `enabled` and, when disabled, a `reason` naming the env var or flag to set (never a secret). Services: `modelark`, `seed3d`, `seed_audio`, `speech_to_text`, `vod_mediakit`, `omnihuman`, `object_storage`, `asset_library`, `asset_delete`. **Use it to decide whether a capability exists; configuration documentation is not evidence that the running server exposes it.**

| `kind` | `tool` | Notes on `is_default` |
|---|---|---|
| `video` | `seedance_create_task` | One default (`SEEDANCE_DEFAULT_MODEL`) |
| `image` | `seedream_generate_image` | One default (`SEEDREAM_DEFAULT_MODEL`) |
| `3d` | `hyper3d_create_task` or `hitem3d_create_task` (by family) | One default per family |
| `understanding` | `seed_understand`, or `seed_audio_understand` for the `SEED_AUDIO_UNDERSTANDING_MODEL` binding | Two defaults: the non-audio default and the audio model |

### Exact IDs and typos

`seedance_create_task`, `seedream_generate_image`, `hyper3d_create_task`, `hitem3d_create_task`, and `seed_understand` accept **configured IDs only**. An unknown ID is rejected before any provider call. The error lists the configured IDs and adds a did-you-mean hint when one is close (compared case-insensitively with `.` treated as `-`; no hint when nothing is close):

```text
Model '<id>' is not configured. Did you mean '<closest-id>'? Configured video models: [...]. Call ark_list_models(kind='video') for details.
```

**`seed_audio_understand` has no `model` argument**; the server fixes the model (default `seed-2-0-lite-260428`, set by `SEED_AUDIO_UNDERSTANDING_MODEL`). It is listed under `kind='understanding'` so you can see which model answers.

### Request validation against limits

Create tools check the request against the resolved model's limits before spending quota, and **report every violation in one error** ending with `Call ark_list_models(kind='<kind>') for per-model limits.` With `dry_run: true` the same check runs without billing, so use it to test a request against a model before committing.

## Capability registry and bindings

The server maps each configured model ID to a **family**; the family decides the limits. The family is chosen by the operator, not inferred from the ID string (apart from the built-in IDs below).

| Setting | Effect |
|---|---|
| `SEEDREAM_MODEL_BINDINGS`, `SEEDANCE_MODEL_BINDINGS`, `SEED_UNDERSTANDING_MODEL_BINDINGS`, `SEED3D_MODEL_BINDINGS` | JSON list of `{"model_id": "...", "family": "..."}`; required for any custom model or endpoint ID |
| `SEEDREAM_MODEL_FAMILY`, `SEEDANCE_MODEL_FAMILY`, `SEED_UNDERSTANDING_MODEL_FAMILY` | Family for a single custom default model when no bindings are set |
| `SEEDREAM_DEFAULT_MODEL`, `SEEDANCE_DEFAULT_MODEL`, `SEED_UNDERSTANDING_DEFAULT_MODEL` | Model used when `model` is omitted |
| `HYPER3D_DEFAULT_MODEL`, `HITEM3D_DEFAULT_MODEL` | Per-family 3D defaults |
| `SEEDREAM_PROMPT_OPTIMIZATION_MODE` | `standard` (default) or `fast`; applies only to Seedream 5.0 Pro when the caller omits `prompt_optimization` |

Family values: Seedream `seedream_5_5` / `pro` / `lite` / `4x`; Seedance `standard` (2.0) / `fast` / `mini` / `seedance_2_5` / `seedance_2_5_flash`; understanding `pro` / `turbo`; 3D `hyper3d` / `hitem3d`.

### Built-in model IDs (no binding needed)

| Product | Default model ID | Family |
|---|---|---|
| Seedream 5.5 (default) | `dola-seedream-5-5-261028` | `seedream_5_5` |
| Seedream 5.0 Pro (opt-in) | `dola-seedream-5-0-pro-260628` | Pro |
| Seedance | `dreamina-seedance-2-5-260628` | 2.5 |
| Seedance Flash | `dreamina-seedance-2-5-flash-261115` | 2.5 Flash |
| Seedance 2.0 (opt-in) | `dreamina-seedance-2-0-260128` | Standard |
| Understanding | `dola-seed-2-1-turbo-260628` | Turbo |
| Understanding (opt-in) | `dola-seed-evolving` | Pro |
| Hyper3D | `hyper3d-gen2-260112` | Hyper3D |
| Hitem3d | `hitem3d-2-0-251223` | Hitem3d |

Seedream Lite, Seedream 4.x, Seedance 2.0 Fast, and Seedance 2.0 Mini have no built-in ID; bind the account's authorized ID to the family.

When Seedance bindings are empty, Flash is added alongside the selected default,
unless it is already the default. Regular 2.5 remains the default when omitted.
Explicit non-empty binding lists are never augmented. Listing Flash is not a
provider activation or account-entitlement check.

### Rules that fail startup

- **The default model must be one of the bound IDs, and bound IDs must be unique.** Startup fails with `... default model '<id>' is missing from its bindings. Set the default model env var to one of the bound IDs: [...]`.
- **5.5 is the image default and requires account authorization.** Existing explicit defaults are unchanged. A bindings list containing only older models needs an explicit default or a 5.5 entry. Set `SEEDREAM_DEFAULT_MODEL=dola-seedream-5-0-pro-260628` to retain Pro; discovery does not prove provider access.
- **`SEEDANCE_DEFAULT_MODEL` defaults to Seedance 2.5.** A `SEEDANCE_MODEL_BINDINGS` that lists only a 2.0 model therefore fails startup unless `SEEDANCE_DEFAULT_MODEL` is set to that 2.0 ID (to keep 2.0 as the default) or a 2.5 binding is added.
- A custom default model ID with no family, no bindings, and no built-in match also fails startup (set the matching `*_MODEL_FAMILY` or bindings).

### Seedance 2.5 4K

4K is selected through `resolution="4k"` on `dreamina-seedance-2-5-260628`
or an endpoint bound to `seedance_2_5`. No separate model, binding, or feature
flag is needed. Old separate-model configuration must be removed explicitly;
the server provides no compatibility aliases.

## Seedance (`kind: video`)

| Family | Resolutions | Duration | Max images / videos / audios | Draft (final res.) | Audio-only input | `omni_reference_task_type` | `output_format` |
|---|---|---|---|---|---|---|---|
| 2.0 | 480p, 720p, 1080p, 4k | 4-15 s | 9 / 3 / 3 | No | No | none | none |
| 2.0 Fast | 480p, 720p | 4-15 s | 9 / 3 / 3 | No | No | none | none |
| 2.0 Mini | 480p, 720p | 4-15 s | 9 / 3 / 3 | No | No | none | none |
| 2.5 (default) | 480p, 720p, 1080p, 4k | 4-30 s | 30 / 10 / 10 | Yes (1080p) | Yes | `auto`, `reference`, `edit`, `extend` | `mp4`, `mov` |
| 2.5 Flash | 480p, 720p | 4-30 s | 30 / 10 / 10 | No | Yes | `auto`, `reference`, `edit`, `extend` | `mp4`, `mov` |

- **Ratios** for every family: `16:9`, `4:3`, `1:1`, `3:4`, `9:16`, `21:9`, `adaptive`.
- **Duration `-1` (auto)** is accepted by every family in addition to the range.
- **`priority` 0-9 and `execution_expires_after` 3600-259200 seconds** apply to every family.
- **An empty `task_types` or `output_formats` list means the field is unsupported** on that model; setting it is rejected.
- **Audio-only input** means audio references may be the only media input; on 2.0 families an audio reference needs an image or video alongside it.

**Choosing a model.** Use regular 2.5 for 4K or Draft mode. Flash shares the 2.5 reference/edit/extend features up to 30 s at 480p/720p but rejects Draft requests. Use 2.0 when its legacy behavior is needed, or Fast/Mini for speed and lower cost. Static video estimates do not account for resolution or duration; Flash reuses the static 2.5 per-task fallback, not its token-based provider price.

**Draft mode (regular 2.5 only; not Flash).** Step 1: `draft: true` renders a cheap 480p preview (resolution omitted or `480p`). Step 2, once the Draft task has succeeded (at most 7 days old, owned by the caller): `draft_task_id` renders the final video at **1080p**, not 4K. The provider reuses the Draft's model, prompt, media, duration, ratio, seed, `generate_audio`, and `omni_reference_task_type`, so omit them (they are rejected even when they match); leave `variations` at 1. `return_last_frame`, `watermark`, `execution_expires_after`, `priority`, `safety_identifier`, and `output_format` may be set again. Each step is billed separately. Polling and the `draft` flag in results: [polling-and-artifacts.md](polling-and-artifacts.md).

## Seedream (`kind: image`)

| Family | Max references | `max_images` batch | `output_format` | Prompt optimization | Transparent background |
|---|---|---|---|---|---|
| 5.5 (default) | 10 | No | `png` (default), `jpeg` | `standard` only (provider default) | Text-only or references without alpha |
| Pro (5.0 Pro) | 10 | No | `png`, `jpeg` | Yes; omitted value uses `SEEDREAM_PROMPT_OPTIMIZATION_MODE` | Existing transparent PNG only |
| Lite | 14 | Yes | `png`, `jpeg` | Yes; provider default when omitted | No |
| 4.x | 14 | Yes | `jpeg` only | Yes; provider default when omitted | No |

- **5.5 sizes:** `1K`, `1.5K`, `2K` (default), or positive `WIDTHxHEIGHT` with inclusive pixel count 921600-4624220 and width/height ratio 1/16-16. `auto`, `3K`, and `4K` are rejected for generation. Older families keep `supported_sizes=null` (provider validation).
- **`max_images` vs `variations`.** `max_images` is one provider batch (one request, one usage record) and only works where batch is supported (Lite, 4.x). `variations` (1-10) runs separate calls in parallel and works on every model. **On 5.5 and Pro use `variations`.** Passing both is rejected.
- **`background="transparent"`** requires `output_format` omitted or `png`. 5.5 supports text-only and reference-based generation without existing alpha. Pro edits exactly one already-transparent PNG; it does not remove an opaque background.
- **5.5 background:** `auto` (default), `opaque`, `transparent`; JPEG in auto mode is always opaque. Pro accepts only `opaque` and `transparent`.
- **Safety IDs:** optional `safety_identifier` on 5.5/Pro, 1-64 non-space printable ASCII characters; use a stable hash, not personal data.
- Discovery reports transparency, named/custom size limits, `background_modes`, `prompt_optimization_modes`, and `supports_safety_identifier`. Source and remaining live-alpha validation: [model capabilities](https://byteplus-sa.github.io/ark-mcp/models/#image-capabilities-imagecapabilities). Layer-decomposition/OCR inputs are rejected.

## Seed 3D (`kind: 3d`, requires `BYTEPLUS_MODELARK_3D_ENABLED=true`)

| Family | Tool | Text-to-3D | Reference images | `file_format` | Seed |
|---|---|---|---|---|---|
| Hyper3D | `hyper3d_create_task` | Yes | prompt and/or up to 5 | `glb`, `obj`, `usdz`, `fbx`, `stl` | Yes (0-65535) |
| Hitem3d | `hitem3d_create_task` | No | 1-4 required | `obj`, `glb`, `stl`, `fbx`, `usdz` | No |

- **Choosing.** Hyper3D for text-to-3D, seeds, PBR materials, mesh modes, or HD textures. Hitem3d for image-to-3D with multi-view inputs and resolution control (`1536` or `1536pro`) and face-count control.
- 3D tools are absent and `ark_list_models(kind='3d')` is empty when the flag is off; `services` shows `seed3d` with the flag to set.
- Both families return a task ID polled with `gen_task_get`; the result is a zip package (see [polling-and-artifacts.md](polling-and-artifacts.md)).

## Understanding (`kind: understanding`)

| Family / model | Modalities | Max media parts | Context | Reasoning efforts | `response_format` |
|---|---|---|---|---|---|
| Seed 2.1 Turbo (default) | image, video | 32 | 256K tokens | `low`, `medium`, `high` | `text`, `json_object`, `json_schema` |
| Seed 2.1 Pro | image, video | 32 | 256K tokens | `low`, `medium`, `high` | `text`, `json_object`, `json_schema` |
| Audio understanding model (`SEED_AUDIO_UNDERSTANDING_MODEL`) | audio | 8 clips | 256K tokens | `low`, `medium`, `high` | see note |

- **Max media parts counts images plus videos together** in `seed_understand`; exceeding it is rejected before the call. `seed_audio_understand` accepts 1-8 audio clips.
- **Deep thinking is always on** for Seed 2.1; `reasoning_effort` sets its depth (default `medium`). `ark_list_models` reports `supports_thinking` and `reasoning_efforts` per model.
- **Audio model.** The default audio model does not enforce `json_object`; use `json_schema` for structured output from `seed_audio_understand`. If the audio model ID is also a bound Seed 2.1 model, it is listed once with only `audio` in its advertised modalities and `tool: seed_audio_understand`. The same bound ID remains usable through `seed_understand` for images/videos.
- **Default routing.** With `model` omitted, `seed_understand` uses the non-audio default; `seed_audio_understand` always uses the audio model.
- For long-form transcription with word timings and utterances use `speech_to_text`, not either understanding tool. Media input forms and limits: [understanding-media-assets.md](understanding-media-assets.md).

## Health

**`seed-health://status`** is an MCP resource that needs no authentication and
exposes no credentials or output-root paths. It prints the build stamp, configured
products, storage backends, transport, effective Seedream default model/family
and background-job local-export configuration. These are configuration-only
diagnostics, not provider authorization or filesystem readiness. A configured
absolute `OUTPUT_ROOTS` entry still needs request preflight; client roots do not
exist in jobs. Over HTTP, `/health` (liveness), `/ready` (storage readiness,
optional provider checks) and `/metrics` are also available. For per-service
enablement prefer `ark_list_models.services`. Settings: [environment.md](environment.md).
