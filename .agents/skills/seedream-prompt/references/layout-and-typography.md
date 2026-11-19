# Layout and Typography

Read for spatial placement, expressive lettering, or adaptation to a new
channel. Distinguish creative direction from exact graphic requirements and
from executable tool controls.

## Prompt layout boxes

The Seedream 5.5 prompting guide describes
`bbox=[xmin, ymin, xmax, ymax]` in a normalized **0-1000** canvas coordinate
system, with the origin at the top left. This is a documented prompting
convention for approximate placement, not an API field or a pixel-perfect
layout guarantee.

Fictional text-free layout example:

```text
Create a wide editorial image of a ceramic vase on a studio pedestal.
Place the complete vase within bbox=[560, 180, 900, 860].
Reserve bbox=[80, 180, 470, 760] as uncluttered negative space for later copy.
Use soft side light and a warm neutral palette. Keep the vase proportions
natural and the reserved area free of objects, lettering and marks.
```

Inspect actual placement. When exact geometry carries the design, generate the
image layer and leave layout to deterministic finishing.

## Structured edit controls are different

The current MCP's `seedream_generate_image` structured `bbox` and `point`
fields use **0-999** and target the **first image** in `images`. They are not
the guide's prompt-layout boxes. With those fields, do not add `<bbox>` or
`<point>` markup to the prompt: the adapter adds it. Count the adapter-added
markup toward the prompt limit.

For executable-settings proposals, write `bbox` as an object with named
`x1`, `y1`, `x2`, `y2` fields, never as an array. A `point` is an object with
`x` and `y`. For example, this fictional settings fragment is outside the
creative prompt and still requires its matching source image:

```json
{"bbox": {"x1": 100, "y1": 200, "x2": 700, "y2": 900}}
```

Put the actual edit source first and renumber every reference binding when
reordering. A donor object in another image is a reference, not a second
structured edit target. Unknown multi-target support remains unresolved.

Validate coordinates against the actual source image before conversion:

- Require known coordinate units and source dimensions; never guess them.
- Reject non-finite, negative, out-of-range, inverted or zero-area boxes.
- For pixel coordinates use the adapter's documented mapping per axis,
  `min(999, round(pixel / dimension * 1000))`, only after bounds validation.
- When translating a valid guide-normalized endpoint of 1000 to this MCP,
  map that endpoint to 999. Do not clamp arbitrary invalid input into validity.
- Recheck that the converted box still has positive area. Recompute after a
  crop, rotation or reframe. A proportional resize of the full unchanged
  canvas preserves normalized coordinates; scale pixel coordinates if used,
  and verify the actual submitted dimensions.
- Decomposition OCR boxes are a separate provider-output convention, not
  structured edit inputs. The current MCP does not expose that operation.

An executable edit requires an actual source image and verified controls. A
missing image, invalid box or unknown schema permits a clearly conditional
prompt draft, not an invented target or a silent full-frame replacement.

## Expressive typography

Use model-rendered text only when the user expressly accepts it as non-exact.
Quote the requested wording and specify useful design controls: line breaks,
headline/subtitle hierarchy, alignment, weight, spacing, color, surface and
safe margins. Do not infer permission to translate or rewrite approved copy.

Fictional expressive-lettering example:

```text
Create playful hand-painted lettering reading "OPEN" on the first line and
"SKIES" on the second. Center the two lines with generous spacing and a clear
gap between them. Use rounded blue letters with subtle painted texture and
wide clear margins. Keep the wording unchanged and add no other characters.
```

Proofread every character, punctuation mark, word and line break in the actual
output; inspect glyphs, reading order and legibility at delivery size. OCR is
supporting evidence, not a substitute for visual review. Named fonts and quoted
copy express intent, not exact font geometry or spelling guarantees.

Delivery-critical copy, pricing, legal text, logos, UI and factual chart values
stay in a deterministic layer. Use generated art as the text-free base and
keep the final copy editable. A conceptual dashboard or decorative chart must
not masquerade as verified data. A missing deterministic route calls for a
truthful handoff, not a generated substitute for an exact requirement.

## Resize and channel adaptation

Choose the operation before writing an edit:

| Need | Route |
| --- | --- |
| Same content, different pixel dimensions | Deterministic proportional resize; preserve alpha when present. |
| Existing frame can fit by trimming | Deterministic crop with agreed subject and safe-area protection. |
| New ratio needs different staging | Generative recomposition with explicit preserved features and allowed changes. |
| Missing canvas must be invented | Canvas extension only after model and transport support are verified. |

For generative adaptation, state the target ratio, visual hierarchy, protected
subject proportions, identity, materials and safe areas. Put supported output
dimensions in the separate `size` setting; wording alone does not verify the
delivered dimensions. Reposition or extend the environment without stretching
the subject. Keep exact labels, logos and copy in acquired or deterministic
layers and reflow them separately.

Fictional adaptation example:

```text
Adapt the approved square scene in @Image 1 into a wide landscape composition.
Preserve the ceramic vase's silhouette, glaze, scale relative to its pedestal
and upper-left lighting. Move the pedestal toward the right third and continue
the neutral wall to the left, leaving a broad clear area for later copy.
Do not stretch the vase, crop its rim or add lettering.
```

Compare with the last accepted source for unintended changes. Check actual
dimensions, crop, subject proportions, layout hierarchy and reading order,
safe areas, logo/copy clearance, text legibility and required alpha. Include
the applicable checks in the handoff so adaptation is reviewed as a layout,
not only as a dimension change.
Use the last accepted source again if the adaptation drifts; a new aspect
ratio does not authorize changing protected content.

Prompting source: Dola Seedream 5.5 Image Generation & Editing Prompting Guide,
sections 3.1, 3.3, 3.7 and 4.5. Provider controls:
[5.5 tutorial](https://docs.byteplus.com/docs/en/modelark/seedream-5-5.md) and
[image API](https://ai.byteplus.com/ark/region:ap-southeast-1/docs/image-generation-api.md).
