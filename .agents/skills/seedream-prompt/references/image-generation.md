# Image Generation

Focused reference for `seedream-prompt`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Recommended prompt structure — Image generation](#recommended-prompt-structure--image-generation)

## Recommended prompt structure — Image generation

Lead with the requested task, then describe the subject and scene, composition,
visual style and constraints. This is a readability convention, not a weighting
law. A short natural-language paragraph is enough for a simple request; use only
the sections that clarify the result and do not add empty boilerplate.

```
References:          # only when images are provided
Task:                # requested result or edit
Subject:
Setting:             # when environment matters
Composition:         # when framing matters
Style:               # when style is specified or useful
Lighting:            # when lighting matters
Text in image:       # only when readable text is requested
Constraints:         # only useful quality or exclusion requirements
```

### 1. References (when provided)

List every reference image the user provides. Label them with `@Image 1`, `@Image 2`, ... using sequential numbering starting from 1 (space separator). Include a short role or description.

```
References:
@Image 1: [role, e.g. "subject reference — female character portrait"]
@Image 2: [role, e.g. "style reference — oil painting texture"]
@Image 3: [role, e.g. "material reference — leather sofa"]
@Image 4: [role, e.g. "color swatch — target palette"]
```

Rules for references:
- Preserve the selected model and verify its requested operation, reference
  limits, input formats and connected tool schema. Pro and 5.5 generation
  document up to 10 references; older Lite/4.x sequential limits are separate.
- Historical Pro reference-pricing snapshots are not current account prices
  or family-wide billing rules. Verify pricing separately when requested.
- Provider input formats and size limits do not prove a wrapper accepts them;
  verify the selected transport before packaging executable settings.
- When no references are provided, omit the References section.
- The reference list is an inventory, not the instruction. Bind each reference
  again where it affects the output, naming both its role and target:
  `Use the face and hairstyle from @Image 1 for the main character, apply the
  oil-paint texture from @Image 2 to the full scene, and use the leather from
  @Image 3 on the sofa.`
- Keep `@Image N` labels consistent with the actual input order, rather than
  using ambiguous phrases such as "the references." This is the workspace's
  naming convention, not a required provider API token.

For multi-image work, specify each reference's role, target, preserved features,
excluded features and conflict priority. Use only what matters to the request.
For example, identity may override material shape while the environment
reference contributes only background and light. A style reference does not
authorize changing identity, language, approved text or protected geometry.
Ask when conflicting references have no specified precedence.

Fictional binding example:

```text
Use the ceramic vase in @Image 1 for its silhouette and handles. Apply only the
surface texture from @Image 2 to that vase; ignore the donor object's shape
and lettering. Use @Image 3 only for the room and side-light direction.
The silhouette from @Image 1 takes precedence over the texture reference.
```

For a structured MCP edit, the actual edit target must be the first image.
Renumber the inventory and all inline bindings together when reordering.
Do not invent a missing reference or describe an uninspected image as verified.

### 2. Task type

Declare which generation mode applies.

```
Task:
Text-to-Image (T2I)  |  Image-to-Image (I2I)  |  Image Editing  |  Sequential Generation  |  Infographic / Information Visualization
```

**Text-to-Image (T2I)**: Pure text prompt, no reference images.

**Image-to-Image (I2I)**: Reference images guide subject, style, composition, or material. Use patterns like:
- `Using @Image 1 as the subject reference, generate...`
- `In the style of @Image 1, create...`

Reference-based generation sub-types (Reference Target + Generated Scene Description):
- **Reference Character**: `Use @Image 1 as the character reference, generate [scene description].`
- **Reference Style**: `In the style of @Image 1, generate [scene description].`
- **Reference Virtual Entity**: `Using the [entity] in @Image 1, generate [scene].`
- **Reference Product**: `Using the [product] in @Image 1, generate [commercial scene].`

**Image Editing**: Modify an existing image with localized changes. See the editing modes section below.

**Sequential Generation**: Multiple coordinated images in one call require
verified native sequential support for the selected model and tool. Pro and
5.5 do not support it. Older Lite/4.x configurations or future models need
current evidence; do not silently switch to them. Offer per-panel prompts,
a single-image grid, or an unselected verified alternative, with authorization
before changing the model or request count. Layers and stochastic variations
are not ordered sequences.

**Infographic / Information Visualization**: Seedream may supply an expressive
image layer. Exact typography, logo geometry, data placement, and delivery-critical
layout belong in a deterministic render, not a model-quality promise.

### Generation size

For documented Pro and 5.5 generation, presets are `1K`, `1.5K`, and `2K`;
explicit `widthxheight` dimensions are also valid within pixel totals
[921600, 4624220] and aspect ratios [1/16, 16]. Examples include `2048x2048`,
`1728x2160`, and `2816x1584`. Do not replace valid dimensions with invented
3K/4K tiers. Verify the selected model and tool; decomposition is a separate
operation with presets or `auto`, not explicit dimensions. See
[Quick reference](quick-reference.md) for operation-scoped settings.

### 3. Subject

Describe the main subject clearly and concisely. Lead with the requested visual priority for clarity; this ordering is not a measured weighting guarantee.

```
Subject:
[Who or what. Key attributes: appearance, clothing, hair, expression, pose, motion, props.]
```

Rules:
- Put the most important subject first.
- Use 2-3 stable attributes to define each subject.
- For multi-subject images, list subjects in order of visual priority.
- Describe pose, expression, and action: "standing confidently with arms crossed," "leaning forward, eyes wide with curiosity."

### 4. Setting

Describe the environment, time, weather, and background.

```
Setting:
[Location, time of day, season, weather, background elements, spatial context.]
```

Examples:
- "A sunlit Tokyo alley at golden hour, cherry blossoms drifting in the breeze, wooden shop signs overhead."
- "A futuristic cyberpunk city at night, neon reflections on wet asphalt, holographic billboards flickering."
- "A minimalist Scandinavian living room, morning light through sheer curtains, white walls and oak floors."

### 4b. Prop / product identity sheets

Prop and product sheets that become Seedance or storyboard identity references
belong to the sibling `seedream-prop-asset` skill, which owns the prop
threshold, acquisition-first order, view layout, background, and QA. Use this
reference for product imagery that is not an identity reference: a commercial
scene, or a clean isolated packshot, which can borrow the plain seamless
setting but is not locked as an Element. The workspace
[element identification](../../../contracts/element-identification.md)
contract governs brand acquisition order.

### 5. Style

Define the artistic direction, medium, rendering quality, and aesthetic keywords.

```
Style:
[Art style, medium, rendering quality, aesthetic keywords.]
```

**Art style and medium**: photorealistic, cinematic, oil painting, watercolor, 3D render, anime, illustration, flat design, pencil sketch, charcoal, vector art, pixel art.

**Aesthetic keywords** (historical Pro guide vocabulary, reusable creative intent):

| Category | Keywords |
|---|---|
| Lighting style | Soft Light, Hard Light, Backlit, Dappled Light, Golden Hour, Night Neon, Low Key, Overexposed |
| Color tone | Warm Tone, Cool Tone, Blue Tone, Purple Tone, Monochrome, Low Saturation, Black and White Tone |
| Lens & perspective | Fisheye Lens, Macro Photography, Bird's Eye View, Wide Angle, Tilt-Shift |
| Mood & atmosphere | Cinematic, Motion Blur, Out of Focus, Diagonal Composition, Symmetrical Composition, Rule of Thirds |
| Genre | Cyberpunk, Retro Film, Minimalism, Japanese Fresh Style, Baroque, Art Deco, Brutalist |

### 6. Lighting

Describe light direction, quality, color temperature, and time of day.

```
Lighting:
[Direction, quality, color, time, key-to-fill ratio.]
```

Examples:
- "Soft studio key light at 45 degrees left, warm 3200K, gentle fill from right."
- "Golden hour backlight, rim light on subject's hair, warm amber tones."
- "Moody low-key lighting, single overhead source, deep shadows, cool blue moonlight through window."

Relate reflections, contact shadows, perspective and material response to the
same light sources and scene geometry. Describe concrete surface behavior
instead of stacking quality adjectives; inspect physical coherence afterward.

### 7. Composition

Specify shot type, viewing angle, and composition method.

```
Composition:
[Shot type, angle, composition rule, framing.]
```

**Shot types**: close-up, medium shot, long shot, extreme close-up, wide shot, full body.

**Viewing angles**: high angle, low angle, eye level, bird's eye view, worm's eye view, Dutch angle.

**Composition methods**: symmetric, diagonal, rule of thirds, leading lines, frame within a frame, negative space, golden ratio.

For approximate placement boxes, safe areas or channel adaptation, read
[Layout and Typography](layout-and-typography.md). Prompt boxes and structured
edit coordinates are distinct controls, neither a guarantee of exact geometry.

### 8. Text in image (when non-exact model text is expressly accepted)

Include this section only when the user expressly accepts model-rendered text as
expressive and non-exact. For delivery-critical copy, omit model text, generate
the text-free image layer, and finish through the deterministic static-graphics
route.

```
Text in image:
"Exact text to render" — [surface it appears on, style, color, size hint]
```

Rules:
- Put exact text in double quotes.
- Treat the quoted string as prompt intent, not proof of pixel-exact output.
- Describe the surface: "on a storefront window," "on a vintage paper scroll," "on a digital screen."
- A historical Pro guide lists multilingual text examples; that is not a
  family-wide fidelity guarantee. Inspect actual spelling and typography in
  the requested language, and keep exact copy in the deterministic layer.
- Small text may still be unstable. If fidelity matters, remove it from the
  generative layer and render it deterministically.
- For expressive text, specify hierarchy, line breaks, alignment, weight,
  spacing and safe margins, then proofread the actual output. Detailed patterns
  live in [Layout and Typography](layout-and-typography.md).

### 9. Constraints (when useful)

Close with only the quality directives and negative constraints that materially affect the output.

```
Constraints:
Quality: [rich details, cinematic texture, consistent identity]
Negative: [no watermarks, no signatures, no text overlays, no distorted anatomy]
```

All constraints go inline in the text prompt. The Seedream API has no separate `negative_prompt` field.

- Use supported explicit `widthxheight` in `size` when dimensions or aspect
  ratio matter. A tier such as `2K` is not proof of a particular delivered
  shape, and a "4K" quality adjective is not a resolution setting.
- A negation does not remove a strong visual prior. Describe the wanted shape,
  surface, or light positively first ("a soft round pool of lamplight", "a
  plain white jug, smooth solid glaze, nothing printed"), then add a short
  exclusion only when it protects something specific.
- Generic surfaces (jars, boxes, labels, signs, screens, garment tags) tend to
  grow pseudo-text. When no text is wanted, say the surface is plain with
  nothing printed. Images that become video references carry that text into
  every shot.
- For a transparent canvas, cutout, translucent material or interior holes,
  read [Transparent Assets](transparent-assets.md); a background description
  is not evidence of an actual alpha channel.
