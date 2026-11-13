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

Preserve the selected model; omit `model` only when no model was selected and
the effective configured default has been verified. Resolve an exact model ID,
operation, and current tool schema before submission. A family label is not an
API ID. The following describes existing mappings, not universal capabilities.

| Family | Model | Traits |
|---|---|---|
| Seedream 5.0 Pro | `dola-seedream-5-0-pro-260628` (default) | 10 refs, single image per call, PNG/JPEG |
| Seedream Lite | bound via `SEEDREAM_MODEL_BINDINGS` | 14 refs, batch (`max_images`), PNG/JPEG |
| Seedream 4.x | bound via `SEEDREAM_MODEL_BINDINGS` | 14 refs, batch, JPEG only, no `output_format` |

5.5's documented provider ID is `dola-seedream-5-5-261028`; its connected MCP
mapping and account availability remain unverified here. Do not assume this
table, the wrapper registry, or an older binding covers it or a future model.
Check provider support and wrapper exposure separately. Missing evidence is
unresolved, not permission to switch models, operations, or transports.

Native sequential output, independent variations, a grid in one image, and
layer decomposition are different operations. Pro and 5.5 have no native
sequential output. Provider decomposition/OCR support does not prove the MCP
tool exposes those fields. Offer only unselected alternatives if an operation
cannot be verified, and obtain authorization before changing the package.

## `seedream_generate_image`

Text-to-image and reference-based generation. For spatially targeted edits use
`seedream_edit_image`.

| Parameter | Type | Notes |
|---|---|---|
| `prompt` | `str` | 1–4000 characters; required |
| `images` | list | Reference images (URL, Base64, or `asset://` when the operator enabled resolve mode); count limited by model |
| `model` | `str` | Preserve the selected exact ID; omit only for a verified configured default |
| `size` | `str` | e.g. `2048x2048`, `2048x1152`; must be valid for the model |
| `seed` | `int` | Optional wrapper range -1 to 2147483647; include only with selected-model and tool support |
| `max_images` | `int` | Optional sequential-output limit where verified; not decomposition's `max_images` |
| `output_format` | `png` \| `jpeg` | Not supported by 4.x |
| `response_format` | `url` \| `b64_json` | Default `url` |
| `watermark` | `bool` | Provider watermark |
| `prompt_optimization` | `standard` \| `fast` | Pro documents both; 5.5 documents standard only. Verify the tool and effective environment fallback; latency preference never enables fast |
| `persist` | `bool` | Default `true` |
| `output_path`, `overwrite` | | stdio with confirmed native tasks only; multi-image calls need a directory |

Returns `artifacts: list[ArtifactRef]` and `usage`. Storage failures are
successes with `persistence_error`; always check it.

Illustrative arguments after selected-model and tool verification. Add only
supported optional fields; an omitted unsupported field is not a provider default.

```json
{"tool_name": "seedream_generate_image",
 "arguments": {"input": {"prompt": "A serene mountain landscape at sunset, digital art style",
                         "size": "2048x2048", "output_format": "png",
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
Verify interactive-edit support and the installed adapter's mapping for the
selected model; generation compatibility does not establish edit compatibility.
Unknown support blocks submission rather than triggering a full-frame fallback.

| Parameter | Type | Notes |
|---|---|---|
| `prompt` | `str` | 1–4000 characters; the edit instruction |
| `images` | list | At least one image to edit |
| `point` | `{x, y}` | 0–999; required when `bbox` is absent |
| `bbox` | `{x1, y1, x2, y2}` | 0–999; required when `point` is absent |
| other image params | | Same as `seedream_generate_image` |

Coordinates are normalized: top-left `0,0`, bottom-right `999,999`;
`normalized = round(pixel / dimension * 1000)`, clamped to 0–999. Do not force
point or bbox logic into `seedream_generate_image`. Decomposition OCR output
uses 0–1000 base-image coordinates, a separate convention.

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

The documented wrapper offers 1–10 independent images in parallel. Verify the
selected model and variation tool first; seed/base_seed require separate support.
Do not promise controlled seeds or reproducibility where support is unknown.

| Parameter | Type | Notes |
|---|---|---|
| `prompt` | `str` | Base prompt |
| `variations` | `int` | 1–10 |
| `variation_prompts` | `list[str]` | Optional, one per variation |
| `base_seed` | `int` | None = random, -1 = client-randomized, N = sequence N, N+1, ... |
| other image params | | Same as `seedream_generate_image`; `output_dir` instead of `output_path` |

Returns a `VariationSummary` with `total`, `succeeded`, `failed`, and
per-variation results; partial failures are captured.

- **Sampling set:** identical prompt and references; use `base_seed: 100` only
  where verified seed control is supported. Three samples are not automatic
  generation authorization; preserve review mode and explicit requested count.
- **Creative alternatives:** `variation_prompts` changes only the requested
  variable.

## Reproduction

Record the exact model, tool, prompt, reference hashes, size, effective settings,
and returned seed if present. Pass `seed` or `base_seed` only where the selected
model and tool support them. Matching settings aid experiment tracking, not a
guarantee of identical output or identity continuity. The documented Seedance
tools expose no seed.

Provider contracts checked 2026-11-13: [image API](https://ai.byteplus.com/ark/region:ap-southeast-1/docs/image-generation-api.md)
and [5.5 guide](https://docs.byteplus.com/docs/en/modelark/seedream-5-5.md).
These sources do not certify live wrapper mappings or account entitlements.
