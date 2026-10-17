---
name: seedream-edit
description: Guide for using the seedream_edit_image MCP tool for interactive image editing with Seedream 5.0 Pro. Use when the user wants to edit an existing image (replace objects, change regions, add elements at specific positions), especially when coordinate-based precision is needed via point or bounding-box selection.
---

# Seedream Interactive Image Editing

The `seedream_edit_image` MCP tool wraps Seedream 5.0 Pro's interactive
editing capability with structured coordinate inputs. It is the dedicated
editing tool — distinct from `seedream_generate_image` which is primarily for
text-to-image generation.

## When to Use `seedream_edit_image`

Use `seedream_edit_image` when the user wants to **edit an existing image**
with spatial precision. The tool is a better fit than `seedream_generate_image`
when:

- The user provides a reference image and wants to modify a specific region
- The user says "replace the X with Y", "change this area to Z", "put a crown
  on the cat's head"
- The user has UI coordinates (from a canvas, click event, or drawn box) that
  need to be converted to normalized coordinates

Use `seedream_generate_image` instead when:

- The user wants text-to-image generation (no reference image)
- The edit is a global style change ("make it look like a watercolor painting")
  without spatial targeting
- The user does not provide specific coordinates or region information; the
  edit tool requires at least one `point` or `bbox`

## Edits that feed video

An image edit is a still-image tool. Before using it to prepare a Seedance
input, check what the video actually needs:

- **A full-frame image-to-image edit re-composes the scene.** Figures shift,
  poses change, and background geometry drifts even when the prompt asks to
  keep them. Do not use an edited first frame as a shortcut for a video
  change that should happen on screen.
- **Progressive or partial changes belong in the video prompt.** A change that
  travels across a subject over time, such as an outfit changing only on the
  part of the body that has crossed a line, is
  directed in a pure reference-to-video prompt with timestamped stages and the
  element references, not in an I2I-edited first frame.
- **Local edits of element references are fine.** A bounded edit that fixes a
  sheet (a wrong button, a stray hand, a leaked label) keeps the rest of the
  sheet. Compare the unmarked area against the source before accepting it,
  save the edited file as a new version with its own hash, and treat every
  review that cited the old hash as stale.
- **Plain surfaces stay plain.** When an edit adds or replaces a generic prop
  on a reference, describe it as a smooth solid surface with nothing printed
  so the edit does not invent lettering the video will then animate.

## Coordinate System

Seedream 5.0 Pro uses **normalized coordinates** in the range **0 to 999**:

| Corner | Coordinates |
|---|---|
| Top-left | `(0, 0)` |
| Bottom-right | `(999, 999)` |

### Converting Pixel Coordinates to Normalized

When the user provides pixel coordinates relative to an image of known
dimensions (width × height):

```
normalized_x = round(pixel_x / image_width * 1000)
normalized_y = round(pixel_y / image_height * 1000)
```

Always clamp to `[0, 999]` after conversion.

### Tool Input: Point vs Bbox

The tool accepts structured coordinates, not raw markup strings. The examples
below show the fields of the tool's `input` object:

**Point** — for object-level editing near a position:
```json
{
  "prompt": "Replace the object with a crown.",
  "images": [{"kind": "url", "url": "https://example.com/photo.png"}],
  "point": {"x": 520, "y": 460}
}
```

**Bounding-box** — for region-based editing:
```json
{
  "prompt": "Replace with a garden.",
  "images": [{"kind": "url", "url": "https://example.com/photo.png"}],
  "bbox": {"x1": 120, "y1": 180, "x2": 640, "y2": 760}
}
```

**Both** — for cross-image or multi-target editing:
```json
{
  "prompt": "Place the subject from Image 1 at the position of Image 2, and replace the object at Image 2 with a crown.",
  "images": [
    {"kind": "url", "url": "https://example.com/source.png"},
    {"kind": "url", "url": "https://example.com/target.png"}
  ],
  "bbox": {"x1": 179, "y1": 283, "x2": 796, "y2": 986},
  "point": {"x": 50, "y": 50}
}
```

The tool automatically constructs the `<point>` and `<bbox>` markup from these
structured inputs and prepends it to the user's prompt.

## Prompt Engineering for Editing

### Effective Prompts

- **Be specific about what changes.** "Replace the cat with a golden retriever"
  is better than "change the animal".
- **Describe the desired result, not the current state.** "Make the sky sunset
  orange" rather than "the sky is blue, change it".
- **Keep the instruction focused on the target region.** The model knows the
  spatial context from the coordinates.

### Prompt Patterns by Scenario

| Scenario | Prompt Pattern | Coordinates |
|---|---|---|
| Replace object | `Replace the object with a [description].` | Point |
| Change region | `Replace the area with a [description].` | Bbox |
| Add element | `Add a [description] at this position.` | Point |
| Remove object | `Remove the object and fill with [background description].` | Bbox |
| Style transfer | `Apply [style] to this area.` | Bbox |

## Reference Images

At least one reference image is required. The tool accepts:

```json
{
  "kind": "url",
  "url": "https://example.com/photo.png"
}
```

or:

```json
{
  "kind": "base64",
  "data": "iVBORw0KGgo...",
  "mime_type": "image/png"
}
```

URLs are validated for SSRF safety (HTTPS only, public IPs, no metadata
endpoints). Base64 data is limited to 10 MiB. When the operator has enabled asset resolve
mode, an Active private asset can be passed as
`{"kind": "url", "url": "asset://<asset_id>"}`. Local file paths are
not accepted: upload the file or presign a cached object key first, then submit
promptly because presigned URLs expire.

The prompt plus the prepended coordinate markup must stay within 4,000
characters. Set `watermark: false` for reference sheets unless the user wants a
visible watermark.

## Model Compatibility

The edit tool works with all Seedream models:

| Model | Max References | Notes |
|---|---|---|
| `dola-seedream-5-0-pro-260628` (default) | 10 | Pro model, no batch |
| Lite models (via `SEEDREAM_MODEL_BINDINGS`) | 14 | Supports batch |
| 4.x models (via `SEEDREAM_MODEL_BINDINGS`) | 14 | JPEG output only |

The `<point>` and `<bbox>` markup is specifically documented for
`seedream-5-0-pro` but may work with other models.

## Common Pitfalls

1. **Coordinates outside 0-999 range.** The tool rejects these at validation
   time. Always normalize pixel coordinates first.

2. **Bbox ordering.** `x1` must be ≤ `x2` and `y1` must be ≤ `y2`. The tool
   validates this.

3. **Too many reference images.** Pro models accept up to 10; Lite/4x accept
   up to 14. The tool validates this against the capability registry.

4. **Assuming the model knows image context.** The prompt should explicitly
   describe the edit. Don't rely on the model inferring intent from
   coordinates alone — they only specify *where*, not *what*.

5. **Using `seedream_generate_image` with raw markup.** While possible, it
   shifts coordinate validation onto the agent. Prefer `seedream_edit_image`
   when you have structured coordinates.

## Artifact Persistence

Like all Seedream tools, `persist=true` (the default) saves the edited image
to the local artifact store. The returned `ArtifactRef.uri` (e.g.
`seed-media://artifacts/abc123`) survives provider URL expiry (24 hours for
images). Always use `persist=true` unless you have a specific reason not to.

The edit runs as a long task. Submit it through `ark_job_submit` and poll with
`ark_job_get`; do not pass `output_path` through `ark_job_submit` (the
background job fails). Read the `ArtifactRef` from the finished job and copy it
locally with `seed_media_export_artifact`. `output_path` is only for clients
that negotiate MCP task augmentation and call the tool directly.

## Related Tools

- `seedream_generate_image` — text-to-image and reference-based generation
  (without coordinate markup)
- `seedream_generate_image_variations` — parallel image generation with
  distinct seeds
- `media_upload` / `media_presign` — turn a local file or cached object key into
  the HTTPS URL the edit needs

## Related skills

- `seedream-character-sheet-cleanup` — post-generation cleanup workflow for
  removing duplicate faces from Seedance-facing character sheets
