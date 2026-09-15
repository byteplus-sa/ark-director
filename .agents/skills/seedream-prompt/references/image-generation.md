# Image Generation

Focused reference for `seedream-prompt`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Recommended prompt structure — Image generation](#recommended-prompt-structure--image-generation)

## Recommended prompt structure — Image generation

Use this order for the sections that apply. Do not add empty boilerplate sections:

```
References:          # only when images are provided
Task:                # include when the mode needs clarification
Subject:
Setting:             # when environment matters
Style:               # when style is specified or useful
Lighting:            # when lighting matters
Composition:         # when framing matters
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
- Seedream 5.0 Pro: up to 10 input images. Seedream 5.0 Lite: reference images + generated images ≤ 15 (so up to 14 refs when generating 1 image).
- First reference image is free. Each additional image: $0.003 (Pro).
- Formats: JPEG, PNG, WebP, BMP, TIFF, GIF, HEIC, HEIF.
- Up to 30 MB per image.
- Input resolution: each dimension > 14px, aspect ratio [1/16, 16], total pixels ≤ 36,000,000 (per API reference).
- When no references are provided, omit the References section.
- The reference list is an inventory, not the instruction. Bind each reference
  again where it affects the output, naming both its role and target:
  `Use the face and hairstyle from @Image 1 for the main character, apply the
  oil-paint texture from @Image 2 to the full scene, and use the leather from
  @Image 3 on the sofa.`
- Use the exact `@Image N` token every time; do not drop the `@` or replace the
  token with an ambiguous phrase such as “the references.”

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

**Sequential Generation**: Generate multiple coordinated images in one call. **Not supported on Seedream 5.0 Pro** — Pro supports only single-image and multi-layer output. Sequential/batch generation requires Seedream 5.0 Lite (or 4.5/4.0) with `sequential_image_generation` set to `auto` (or `disabled`). Include "series", "set", or "sequence" in the prompt.

**Infographic / Information Visualization**: Transform data, concepts, and dense text into professional layouts. Seedream 5.0 Pro is specifically optimized for this.

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

### 4b. Prop / product sheets (Seedance identity references)

For any prop or product sheet that will be used as a Seedance `@Image` identity
reference, isolate the subject on a **pure white seamless background** by
default. This prevents the sheet's backdrop from leaking into the generated
video. Character sheets use a **neutral gray** studio background (see
`seedream-character-sheet`); location assets have no background mandate (see
`seedream-location-asset`).

- Setting: "Isolated product shot on a pure white seamless background." with at
  most a soft, faint contact shadow directly beneath the object.
- Constraints (negative): no colored backdrop, no gradient background, no props,
  no hands, no reflections of other objects.
- When the sheet will be used with a Seedance blockout or R2V reference, also
  state in the video prompt "Use only the <subject> from @Image N — do not use
  its background."

**Prop threshold test — before generating a prop sheet, verify it is needed.**
Not every held or visible object requires a `prop_` sheet. A prop needs a
**locked Element reference** only if it meets **at least one** of these criteria:

| Criterion | Example | Needs locked reference? | Acquisition |
|---|---|---|---|
| Branded product with logo or specific design | 555 Tuna can, GFiber modem, smartphone with app UI | Yes | Prefer official/authorized web or user download; Seedream only if unavailable or a stylized substitute is requested |
| Object the camera lingers on or that drives the plot | A key, a device screen the camera shows | Yes | Generate or photograph as appropriate |
| Object that recurs across 2+ shots or scenes | Same phone in multiple ads | Yes | Generate, photograph, or download by identity |
| Generic, unbranded, briefly visible background object | A coffee cup, a birthday cake, a tablet in a montage | No — describe in prompt text | — |
| Object held for only 1-2 seconds in a single shot | A pen, a glass of water | No — text is sufficient | — |

A locked reference is an approved local asset with a content hash — not
automatically a Seedream generation. Generating a `prop_` sheet for a generic,
briefly-visible object wastes credits and adds reference noise to the Seedance
prompt. Inventing a fake branded packshot or logo with Seedream when a usable
official download exists is also wrong. When in doubt for unbranded objects,
describe them in the Seedance prompt text and skip the Element. See the
workspace [element identification](../../../contracts/element-identification.md)
contract for brand acquisition order.

### 5. Style

Define the artistic direction, medium, rendering quality, and aesthetic keywords.

```
Style:
[Art style, medium, rendering quality, aesthetic keywords.]
```

**Art style and medium**: photorealistic, cinematic, oil painting, watercolor, 3D render, anime, illustration, flat design, pencil sketch, charcoal, vector art, pixel art.

**Aesthetic keywords** (from the Seedream 5.0 Pro manual):

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

### 7. Composition

Specify shot type, viewing angle, and composition method.

```
Composition:
[Shot type, angle, composition rule, framing.]
```

**Shot types**: close-up, medium shot, long shot, extreme close-up, wide shot, full body.

**Viewing angles**: high angle, low angle, eye level, bird's eye view, worm's eye view, Dutch angle.

**Composition methods**: symmetric, diagonal, rule of thirds, leading lines, frame within a frame, negative space, golden ratio.

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
- Seedream 5.0 Pro natively renders text in 14 languages: Arabic, Filipino, French, German, Indonesian, Japanese, Korean, Malay, Portuguese, Russian, Spanish, Thai, Turkish, Vietnamese. English is the base language. Other languages also work but with weaker in-image text rendering and cultural understanding.
- Small text may still be unstable. If fidelity matters, remove it from the
  generative layer and render it deterministically.

### 9. Constraints (when useful)

Close with only the quality directives and negative constraints that materially affect the output.

```
Constraints:
Quality: [HD, 4K, 2K, rich details, cinematic texture]
Negative: [no watermarks, no signatures, clean background, no text overlays, no distorted anatomy]
```

All constraints go inline in the text prompt. The Seedream API has no separate `negative_prompt` field.
