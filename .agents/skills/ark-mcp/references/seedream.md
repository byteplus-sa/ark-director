# Seedream image tools

Load this when you generate, edit, or vary images with Seedream:
`seedream_generate_image`, `seedream_edit_image`, or
`seedream_generate_image_variations`.

Requires `BYTEPLUS_MODELARK_API_KEY`. Auth scope: `seedream:generate`. All three
tools require background execution through `ark_job_submit`.

**Do not pass `output_path` or `output_dir` to Seedream through
`ark_job_submit`.** The background worker may have no MCP session to resolve
output roots, and the job then fails. Keep `persist: true`, read the
`ArtifactRef` from `ark_job_get.result.structured_content`, then copy the file
with `seed_media_export_artifact` (see `SKILL.md`). Use `output_path` only on a
client with confirmed native task augmentation.

## Models

| Family | Model | Traits |
|---|---|---|
| Seedream 5.0 Pro | `dola-seedream-5-0-pro-260628` (default) | 10 refs, single image per call, PNG/JPEG |
| Seedream Lite | bound via `SEEDREAM_MODEL_BINDINGS` | 14 refs, batch (`max_images`), PNG/JPEG |
| Seedream 4.x | bound via `SEEDREAM_MODEL_BINDINGS` | 14 refs, batch, JPEG only, no `output_format` |

## `seedream_generate_image`

Text-to-image and reference-based generation. For spatially targeted edits use
`seedream_edit_image`.

| Parameter | Type | Notes |
|---|---|---|
| `prompt` | `str` | 1–4000 characters; required |
| `images` | list | Reference images (URL, Base64, or `asset://` when the operator enabled resolve mode); count limited by model |
| `model` | `str` | Omit for the default |
| `size` | `str` | e.g. `2048x2048`, `2048x1152`; must be valid for the model |
| `seed` | `int` | -1 (random) to 2147483647 |
| `max_images` | `int` | 1–15; Lite and 4.x only |
| `output_format` | `png` \| `jpeg` | Not supported by 4.x |
| `response_format` | `url` \| `b64_json` | Default `url` |
| `watermark` | `bool` | Provider watermark |
| `prompt_optimization` | `standard` \| `fast` | 5.0 Pro falls back to `SEEDREAM_PROMPT_OPTIMIZATION_MODE` (`standard` by default) |
| `persist` | `bool` | Default `true` |
| `output_path`, `overwrite` | | stdio with confirmed native tasks only; multi-image calls need a directory |

Returns `artifacts: list[ArtifactRef]` and `usage`. Storage failures are
successes with `persistence_error`; always check it.

```json
{"tool_name": "seedream_generate_image",
 "arguments": {"input": {"prompt": "A serene mountain landscape at sunset, digital art style",
                         "size": "2048x2048", "output_format": "png", "seed": 42,
                         "persist": true}}}
```

Reference-based change without a target region:

```json
{"prompt": "Change the background to a beach scene while keeping the subject unchanged",
 "images": [{"kind": "url", "url": "https://cdn.example.com/original.png"}],
 "size": "2048x2048"}
```

## `seedream_edit_image`

Interactive editing with a point or bounding box. At least one image and one
coordinate are required; the tool builds the `<point>` / `<bbox>` markup.

| Parameter | Type | Notes |
|---|---|---|
| `prompt` | `str` | 1–4000 characters; the edit instruction |
| `images` | list | At least one image to edit |
| `point` | `{x, y}` | 0–999; required when `bbox` is absent |
| `bbox` | `{x1, y1, x2, y2}` | 0–999; required when `point` is absent |
| other image params | | Same as `seedream_generate_image` |

Coordinates are normalized: top-left `0,0`, bottom-right `999,999`;
`normalized = round(pixel / dimension * 1000)`. Do not force point or bbox
logic into `seedream_generate_image`.

```json
{"prompt": "Replace the object with a crown.",
 "images": [{"kind": "url", "url": "https://example.com/photo.png"}],
 "point": {"x": 520, "y": 460}}
```

```json
{"prompt": "Replace with a garden.",
 "images": [{"kind": "url", "url": "https://example.com/photo.png"}],
 "bbox": {"x1": 120, "y1": 180, "x2": 640, "y2": 760}}
```

## `seedream_generate_image_variations`

1–10 images in parallel, each with a distinct seed.

| Parameter | Type | Notes |
|---|---|---|
| `prompt` | `str` | Base prompt |
| `variations` | `int` | 1–10 |
| `variation_prompts` | `list[str]` | Optional, one per variation |
| `base_seed` | `int` | None = random, -1 = client-randomized, N = sequence N, N+1, ... |
| other image params | | Same as `seedream_generate_image`; `output_dir` instead of `output_path` |

Returns a `VariationSummary` with `total`, `succeeded`, `failed`, and
per-variation results; partial failures are captured.

- **Sampling set:** identical prompt and references, `base_seed: 100`,
  `variations: 3` yields seeds 100, 101, 102.
- **Creative alternatives:** `variation_prompts` changes only the requested
  variable.

## Reproduction

Pass `seed` (single) or `base_seed` (variations) to reproduce a Seedream
result with the same prompt, references, model, and size. Seed control is a
Seedream and Hyper3D feature; the Seedance tools expose no seed.
