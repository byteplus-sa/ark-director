# Transparent Assets

Read for transparent backgrounds, isolated cutouts, translucent materials, or
interior holes. These are prompting recipes, not proof of a delivered alpha
channel. Preserve the selected model and verify its operation and transport.

## Specify the intended transparency

| Intent | Prompt requirements |
| --- | --- |
| Transparent canvas | Describe the subject and explicitly request an empty transparent background, without a backdrop, floor, or painted checkerboard. |
| Opaque cutout | Preserve the complete subject, fine edges and opaque surfaces while removing the surrounding background. |
| Translucent material | Describe which material transmits light and which parts remain opaque; do not make the entire subject uniformly transparent. |
| Interior holes | Name the openings that must reveal the new background, separately from glass or other translucent material. |

Clarify a materially ambiguous request such as "make it transparent": removing
the canvas and turning an object into glass are different changes. Retain
required shadows only when requested, and specify whether they belong in the
alpha asset or a later composite. Extraction does not promise pixel-identical
foregrounds or hidden-detail recovery.

## Separate prompt intent from settings

For verified Seedream 5.5 generation, `background="transparent"` supports
text-only input and opaque reference images. Request `output_format="png"`;
JPEG cannot preserve alpha. A request for both transparency and JPEG needs
clarification or separately authorized transparent and opaque deliverables.
Do not silently discard the alpha requirement.

Keep these settings outside the paste-ready prompt. With the current MCP,
`seedream_generate_image` exposes these controls; the caller owns submission.
`background="auto"` lets the prompt influence the background, but an explicitly
required transparent deliverable should use the verified transparent control.
Do not infer transparency from the default format.

The documented 5.0 Pro operation instead needs exactly one PNG input that
already contains transparent pixels. Preserve an explicit Pro pin: an opaque
reference does not become eligible just because its file extension is PNG.
Explain unsupported combinations rather than changing the model.

Transparent generation is not layer decomposition. The current MCP does not
expose decomposition or rich-text OCR; do not invent those fields or promise
multiple editable layers from a single generated image.

## Fictional prompt examples

### New asset

```text
Create a single unbranded amber-glass pendant, viewed straight on, with a small
opaque brass mounting loop. Keep the glass translucent and the loop opening
fully transparent. Isolate the complete pendant on a transparent background.
Use soft upper-left light, crisp fine edges and no surrounding scene or floor.
```

### Extract from an opaque source

```text
Use @Image 1 as the source of the pendant's shape, material and orientation.
Remove only the surrounding background. Preserve the full brass loop, amber
glass, highlights and fine edges. The opening inside the loop must remain
empty and transparent. Do not add a replacement background or change the design.
```

Bind `@Image 1` to the actual source. These examples are unexecuted creative
patterns, not evidence of extraction fidelity.

## Acceptance checks

Decode the delivered file and verify its actual dimensions, format and alpha
channel. A PNG filename, white background, checkerboard preview, or provider
success does not prove transparency.

- Inspect alpha extrema and distribution: a fully opaque alpha channel fails
  a required cutout; a fully transparent image fails a visible-asset request.
- Verify expected interior holes and translucent areas, not just transparent
  corner pixels. Partial alpha at antialiased edges alone does not prove glass.
- Composite over both light and dark backgrounds to reveal halos, matte
  contamination, clipped edges, missing fine details and unwanted remnants.
- Compare shape, identity, colors and approved text against the source. Exact
  logos, labels or critical foreground pixels need deterministic preservation.
- Keep the original alpha asset separate from an intentionally matted preview.
  If decoding or visual inspection is unavailable, report it as unverified.

Provider controls: [Seedream 5.5 tutorial](https://docs.byteplus.com/docs/en/modelark/seedream-5-5.md)
and [image API](https://ai.byteplus.com/ark/region:ap-southeast-1/docs/image-generation-api.md).
Prompting conventions follow the Dola Seedream 5.5 Image Generation & Editing
Prompting Guide, sections 3.6 and 4.4. Recheck the live schema before execution.
