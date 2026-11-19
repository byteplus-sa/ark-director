---
name: seedream-edit
description: Prepare bounded Seedream image edits with point or bounding-box targets. Use for replacing objects, changing regions, or placing elements in an existing image. Verify selected-model and tool support.
---

# Seedream Interactive Image Editing

Prepare a narrow Seedream edit prompt with ordered references and a spatial
target. This leaf returns the prompt, reference order, structured target and
acceptance checks; it does not submit or load sibling skills. The caller owns
authorization, mode-appropriate review, registration and execution through
`ark_job_submit` with `seedream_generate_image`. Verify the selected model,
operation and connected tool before using interactive editing.

## When to Use a Bounded Edit

Use `seedream_generate_image` with `images` and a structured `point` or `bbox`
when the user wants to **edit an existing image** at a specified target:

- The user provides a reference image and wants to modify a specific region
- The user says "replace the X with Y", "change this area to Z", "put a crown
  on the cat's head"
- The user has UI coordinates (from a canvas, click event, or drawn box) that
  need to be converted to normalized coordinates

The same tool without structured targeting can serve a separately requested
text-to-image or full-frame reference task:

- The user wants text-to-image generation (no reference image)
- The edit is a global style change ("make it look like a watercolor painting")
  without spatial targeting

A bounded request needs an edit image and a verified region or point. If either
is missing, return unresolved input; do not guess geometry or silently switch
to a full-frame edit. A multi-image composition prompt does not make structured
coordinates address arbitrary references: they target Image 1 only.

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
  sheet (a wrong button, a stray hand, a leaked label) should preserve the rest
  of the sheet, but does not guarantee it. Compare the unmarked area before accepting it,
  save the edited file as a new version with its own hash, and treat every
  review that cited the old hash as stale.
- **Plain surfaces stay plain.** When an edit adds or replaces a generic prop
  on a reference, describe it as a smooth solid surface with nothing printed
  so the edit does not invent lettering the video will then animate.

## Coordinate System

The MCP structured edit fields use **integer normalized coordinates, 0-999**,
against the first image in `images` (`images[0]`). Put the actual edit target
first, then donor/style references. After reordering, rewrite every prompt
binding and label to match the new input order.

| Corner | Coordinates |
|---|---|
| Top-left | `(0, 0)` |
| Bottom-right | `(999, 999)` |

### Converting Pixel Coordinates to Normalized

When the user provides pixel coordinates relative to an image of known
dimensions (width × height), validate the source coordinate system and positive
dimensions first. Reject missing images, inverted or degenerate boxes, and
genuinely out-of-range values rather than clamping invalid input into validity.

```text
normalized_x = min(999, round(pixel_x / image_width * 1000))
normalized_y = min(999, round(pixel_y / image_height * 1000))
```

Recheck that `x1 < x2` and `y1 < y2` after rounding. Cropping or reframing
requires recomputing coordinates against the actual submitted source.

The 5.5 guide's natural-language layout convention is separately
`bbox=[xmin, ymin, xmax, ymax]` on a **0-1000** scale, not an MCP input field
or a pixel-accuracy guarantee. When deliberately converting a valid guide box
to structured edit fields, map its 1000 endpoint to 999 at the adapter boundary.
Do not silently accept 1000 as a structured coordinate or confuse either
interface with provider decomposition OCR coordinates.

### Tool Input: Point vs Bbox

The tool accepts structured coordinates, not raw markup strings. These
hypothetical examples show fields of the caller's `ark_job_submit` input for
`seedream_generate_image`, not authorization to execute:

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

**Donor reference** - the box still targets only the first image:
```json
{
  "prompt": "In @Image 1, replace the boxed chair with the chair from @Image 2 at the same size and orientation. Preserve @Image 1's room, lighting and all unmarked objects. Use @Image 2 only for the chair design, not its background.",
  "images": [
    {"kind": "url", "url": "https://example.com/target.png"},
    {"kind": "url", "url": "https://example.com/donor.png"}
  ],
  "bbox": {"x1": 179, "y1": 283, "x2": 796, "y2": 986}
}
```

The tool automatically constructs the `<point>` and `<bbox>` markup from these
structured inputs and prepends it to the user's prompt. Do not hand-write or
duplicate that markup. If both fields are supported and supplied, both refer
to Image 1, not separate images or an arbitrary multi-target operation.

## Prompt Engineering for Editing

### Effective Prompts

- **Be specific about what changes.** "Replace the cat with a golden retriever"
  is better than "change the animal".
- **Describe the desired result, not the current state.** "Make the sky sunset
  orange" rather than "the sky is blue, change it".
- **Keep the instruction focused on the target region.** State what changes
  and what stays unchanged; coordinates are guidance, not strict boundary guarantees.
- **Bind references by role and target.** Name preserved features, excluded
  donor features and conflict precedence. A material reference must not replace
  the approved subject's shape or identity.
- **For visible markers**, use unique region numbers, distinguish move source
  and destination, state operation order and replacement size/orientation,
  and request removal of the markers. Inspect marked and unmarked areas.
- **For edit chains**, use the last approved output as the next input, one major
  delta per round. Restate preservation constraints in a self-contained prompt;
  do not assume conversational memory. Record the accepted artifact/hash,
  prompt, reference order, exact model and settings. Reject drift and roll back
  to the last accepted image instead of building on a rejected result.

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

For this MCP adapter, the prompt plus prepended coordinate markup must stay
within 4,000 characters, including each variation prompt. This is a transport
limit, not a universal creative word limit. Set `watermark: false` for reference
sheets only when supported and unless the user wants a visible watermark.

## Model Compatibility

Preserve the selected model and verify three separate contracts: its provider
interactive-edit support, the connected adapter's model mapping, and the tool's
point/bbox schema and reference limits. The family name alone proves none of
them. Unknown support stays unresolved; offer a prompt-only handoff or an
unselected compatible alternative. Do not replace a bounded edit with a
full-frame edit, switch models/transports, or submit without authorization.

Pro (`dola-seedream-5-0-pro-260628`) and 5.5
(`dola-seedream-5-5-261028`) have documented provider interactive editing.
That does not prove the installed wrapper supports 5.5. Lite, 4.x, or future
bindings require separate evidence for this operation, not generation limits.
Inspect the actual edited result, including the unmarked area, before acceptance.

Provider-only layer decomposition and its OCR output are unavailable through
the current MCP tool. Do not fabricate layer fields or claim a transparent
image is a set of editable layers.

## Common Pitfalls

1. **Coordinates outside 0-999 range.** The tool rejects these at validation
   time. Always normalize pixel coordinates first.

2. **Bbox ordering.** Require `x1 < x2` and `y1 < y2`; reject zero-area boxes
   even if a wrapper accepts equal endpoints.

3. **Too many reference images.** Verify the selected edit operation and
   wrapper limits. Do not copy batch-generation limits into an edit.

4. **Assuming the model knows image context.** The prompt should explicitly
   describe the edit. Don't rely on the model inferring intent from
   coordinates alone — they only specify *where*, not *what*.

5. **Duplicate targeting.** Pass structured fields once; do not add raw markup
   to the prompt. Reordering references without rebinding targets edits the
   wrong image.

## Artifact Persistence

Like all Seedream tools, `persist=true` (the default) saves the edited image
to the local artifact store. The returned `ArtifactRef.uri` (e.g.
`seed-media://artifacts/abc123`) survives provider URL expiry (24 hours for
images). Always use `persist=true` unless you have a specific reason not to.

The caller submits `seedream_generate_image` through `ark_job_submit` and
polls with `ark_job_get` to a terminal state. Do not pass `output_path` or
`output_dir` through `ark_job_submit`. Inspect the actual `ArtifactRef` and
`persistence_error`, export separately with `seed_media_export_artifact`, and
verify the saved file's existence, bytes and hash. A direct call with an allowed
absolute `output_path` requires confirmed native task augmentation.
Reconcile an interrupted or ambiguous submission before retrying or changing
transport; a persistence failure calls for recovery/export, not regeneration.

## Related Tools

- `seedream_generate_image` - text-to-image, reference-based generation and
  structured edits. Its `variations` field requests separate calls, not provider
  batch output. Default review uses one image; strict uses three when applicable,
  unless the user requests a count or creative alternatives. Keep comparison
  settings identical except supported seed variation; never assume reproducibility
  or authorize extra calls from a prompt-only request.
- `media_upload` / `media_presign` — turn a local file or cached object key into
  the HTTPS URL the edit needs

## Related skills

- `seedream-character-sheet-cleanup` — post-generation cleanup workflow for
  removing duplicate faces from Seedance-facing character sheets
