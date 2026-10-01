---
name: seedream-prop-asset
description: Write structured Seedream prompts for prop and product identity sheets used as Seedance or storyboard references. Applies the prop threshold and acquisition-first rule before writing. Invoke when the user asks for a prop sheet, product reference, hero object, vehicle, device, tool, scene-variant wearable, or prop state variant with Seedream.
---

# Seedream Prop Asset

Write production-grade prompts for BytePlus Seedream prop and product identity
sheets. This skill is for **objects**: held and operated props, hero objects the
camera lingers on, recurring products, vehicles, devices, mechanisms, and
wearables that appear in only some scenes. The output becomes a reusable
`elements/<prop-id>/` reference for Seedance, storyboards, or later Seedream I2I.

Use this skill when the user wants:
- a prop sheet or prop reference
- a product identity reference for video
- a vehicle, device, tool, or mechanism reference
- a scene-variant wearable (sunglasses, a jacket, a mask) kept off the
  character sheet
- a state variant of an approved prop (open/closed, lit/unlit, intact/broken)

Do **not** use this skill for:
- always-worn outfit items, which stay in the character sheet
- locations, set dressing, or furniture that belongs to a place
- commercial product scenes, hero ads, or packshots set in an environment
- exact labels, logos, packaging copy, UI screens, or product lineups
- local edits to an approved prop image

Composition hints: `seedream-character-sheet` owns people and always-worn
outfits, `seedream-location-asset` owns places, `seedream-prompt` owns general
product imagery, `seedream-edit` owns point and box edits, and
`html-graphic-render` owns exact copy and layout.

## Source authority

This skill follows the Seedream prompt structure from `seedream-prompt` and
adapts it for prop and product identity references.

- [Seedream 5.0 Pro official blog](https://seed.bytedance.com/en/blog/beyond-generation-it-understands-design-introducing-seedream-5-0-pro)
- [Seedream 4.0-5.0 API Tutorial](https://docs.byteplus.com/en/docs/ModelArk/1824121)
- [Seedream 4.0-4.5 Prompt Guide](https://docs.byteplus.com/en/docs/ModelArk/1829186)
- Workspace [element identification](../../contracts/element-identification.md)
  and [asset naming](../../contracts/asset-naming.md) contracts

When official documentation changes, prefer the live docs over this skill where
they conflict.

## Submission boundary

The caller owns production authorization, request preflight, prompt review,
and submission. This skill returns a prompt package — or a text-only descriptor
when the gate below says no sheet is needed — without loading sibling skills. A
draft or a provider success does not establish approval.

## Gate: does this prop need a sheet?

Identify every visible object, then apply the threshold. A prop needs a
**locked reference** only when at least one row says yes:

| Criterion | Example | Locked reference? |
|---|---|---|
| Branded product with a logo or specific design | canned tuna, fiber modem, phone with app UI | Yes — acquire first |
| The camera lingers on it or it drives the plot | a key, a letter, a device screen the camera shows | Yes |
| It recurs across two or more shots or scenes | the same phone in several ads | Yes |
| Scene-variant wearable | sunglasses worn in some scenes only | Yes |
| Generic, unbranded, briefly visible | a coffee cup, a cake, a tablet in a montage | No — describe in text |
| Held for one or two seconds in one shot | a pen, a glass of water | No — describe in text |

A locked reference is an approved local asset with a content hash, not
automatically a Seedream generation. Choose the source in this order:

1. **Reuse** a project asset whose content hash still matches the identity.
2. **Acquire** an official or authorized image for a real brand, logo, or
   labeled product.
3. **Generate** with this skill only when no usable real asset exists, the user
   asks for a stylized or fictional substitute, or acquisition is blocked.

When the gate says text-only, return a short object descriptor for the scene
prompt instead of a sheet prompt.

## Default production rule

Choose one layout per image.

**Hero view (default).** One isolated object in a three-quarter view from
slightly above eye level, the whole object in frame with margin on every side.
Use it for compact rigid objects seen mainly from one side.

**Multi-view sheet.** Two or three panels of the same object in one horizontal
row: a three-quarter hero view, a side profile or back view, and an optional
close-up of an identity-critical detail. Use it when the object is seen from
several sides, is large or mechanical (vehicles, machines, doors), or carries a
detail too small to read in the hero view.

A single `front`, `side`, `top`, or `edge` view is still valid when a shot
needs one specific angle.

**Background.** Pure white seamless with only a faint contact shadow directly
beneath the object, so the backdrop does not leak into generated video. Switch
to neutral light gray when the object is white, clear, translucent, silver, or
chrome and would lose its silhouette on white, or when the project's approved
props already use gray. Never use a colored, gradient, textured, or scene
background.

**Lighting.** Neutral, even studio light with neutral white balance, identical
across panels. Controlled shape-revealing highlights on metal, glass, and gloss
are allowed, as is a gentle raking light to read embossing, engraving, or
texture. No scene mood or color cast.

**One canonical state.** Each image shows one state, stated explicitly: closed
or open, folded or extended, screen off or a specified screen, unlit or
glowing. Default to the state seen most on camera. Every other state needed on
camera gets its own image in the same element folder, reusing the identity
descriptor word for word.

## Flexible prompt structure

Use this order for the sections that apply. Do not add empty boilerplate:

- **References** only when images are provided
- **Task** when the mode needs clarification
- **Subject** and **Composition** for every prop image
- **Setting**, **Style**, and **Lighting** when they add relevant direction
- **Text in image** only when non-exact model text is expressly accepted
- **Constraints** only for useful quality, continuity, and exclusion requirements

## 1. References (when provided)

List every reference image the user provides, in order:

```text
References:
@Image 1: approved prop sheet or authorized product photo — shape, proportions, materials
@Image 2: style reference — project render style
@Image 3: material or finish reference
```

Rules:
- Omit the References section when no images are provided.
- An approved prop image or authorized product photo is the highest-priority
  identity reference and goes first.
- Bind every reference again where it controls the output: "Use the shape,
  proportions, and paint layout from @Image 1, the render style from @Image 2,
  and the brushed-steel finish from @Image 3." A reference inventory alone is
  not sufficient.
- For a continuity mark on a character's body (birthmark, tattoo, scar), bind
  the approved character sheet for skin tone and build only, and describe the
  mark itself in Subject.

## 2. Task type

Use **Text-to-Image (T2I)** only when the prompt uses no reference images.

Use **Image-to-Image (I2I)** whenever any reference guides shape, material,
style, state, or another visible property. This includes first-pass sheets built
from photos or concept art, and every state variant of an approved prop.

## 3. Subject

```text
Subject:
[Prop reference of one <object>: silhouette and proportions, real-world size, materials and finish, colors, identity-critical details, wear, canonical state, count.]
```

Always include:
- **the object and its count** — "one coin only"; for a matched set, the exact
  number and that every item shares one design
- **silhouette and proportions** first, then materials and color
- **real-world size in words** — dimensions or a familiar comparison ("about one
  metre long", "palm-sized", "the size of a thumbnail"); never hands, rulers, or
  other objects in frame for scale
- **2–4 identity-critical details** the video must reproduce (a knurled grip
  band, a chrome hood ornament, rows of brass pegs)
- **wear and age** only as far as the story needs; do not invent damage as a
  realism cue
- **the canonical state**, stated explicitly
- for a multi-view sheet, "the same object in all panels, identical design"

Copy the approved descriptor word for word into every later variant and every
prompt that binds the prop.

**Held props** appear without hands, with the grip area and any operated
controls visible.

**Wearables** appear unworn — no person, head, mannequin, or body part — in the
configuration seen on camera: glasses with temples open, a jacket laid flat or
shaped on an invisible hollow form.

**Surface print.** Unless exact text is required, render printed areas as
illegible fine texture or choose an angle that hides them, and state "no readable
text, letters, or numbers."

## 4. Setting

```text
Setting:
Isolated on a pure white seamless background with a single faint contact shadow directly beneath the object. No other objects.
```

Gray variant: "Neutral light-gray seamless studio background, consistent across
all panels. No other objects."

## 5. Style

Match the project's approved render style so the prop sits in the same world as
its characters and locations. Pick 2–4 anchors:

- photorealistic product-reference photography, macro or 50mm lens, true
  material micro-texture
- stylized 3D animated-feature prop design, sculpted appealing forms, authored
  materials, not photoreal
- period-authentic production-design reference

For photoreal props, ask for honest material response and real micro-texture
rather than a waxy CGI finish.

## 6. Lighting

```text
Lighting:
Soft, even, neutral studio light, gentle fill, neutral white balance, controlled highlights on [metal/glass], identical across all panels.
```

No mood lighting, colored gels, hotspots, or blown highlights. Emissive parts
(screens, LEDs, lamps, magical glow) stay off unless the glowing state is the
canonical one.

## 7. Composition

Hero view:

```text
Composition:
Single isolated hero view, three-quarter angle from slightly above eye level, the whole object centered with margin on every side, deep focus across the object.
```

Multi-view sheet:

```text
Composition:
Three panels side by side in one horizontal row with even spacing: left, the whole object in a front three-quarter view; center, a full side profile; right, a close-up of [identity-critical detail]. Same object, scale, and lighting in every panel.
```

Core rules:
- the whole object fits inside every full-view panel — no cropped ends, wheels,
  handles, or straps
- one object per panel, unless the prop is a matched set
- consistent scale between full-view panels
- the detail panel shows only a feature the full views cannot resolve
- three panels at most

## 8. Text in image

Omit by default. When readable copy carries identity (labels, wordmarks, plates,
packaging), use the first route that applies:

1. Acquire the real authorized asset.
2. Generate a text-free base here, then finish the copy deterministically.
3. Only when the user expressly accepts non-exact model text, quote it in double
   quotes with its surface, size, and color.

Never invent a real brand's logo.

## 9. Constraints

```text
Constraints:
Quality: 4K, sharp material detail, consistent design across all panels
Negative: no hands, no people, no other objects, no readable text, no logos, no colored or gradient background, no cropped edges, no extra panels, no watermarks
```

Choose the negatives that apply:
- no hands, people, mannequins, or body parts
- no second object or duplicate
- no colored backdrop, gradient, scene, or floor texture
- no reflections of other objects
- no readable text, letters, numbers, logos, or brand marks
- no cropped object edges
- no extra panels
- no glow, beam, or effect unless canonical
- no watermark

## Standard prompt template

```text
Task:
Text-to-Image (T2I)

Subject:
Prop reference of one [object]: [silhouette and proportions], about [real-world size], [materials and finish], [colors], [2–4 identity-critical details], [canonical state]. One [object] only.

Setting:
Isolated on a pure white seamless background with a single faint contact shadow directly beneath the object. No other objects.

Style:
Photorealistic product-reference photography, 50mm lens, true material micro-texture, not CGI-waxy.

Lighting:
Soft, even, neutral studio light, gentle fill, neutral white balance, controlled highlights on [material].

Composition:
Single isolated hero view, three-quarter angle from slightly above eye level, the whole object centered with margin on every side, deep focus across the object.

Constraints:
Quality: 4K, sharp material detail, clean silhouette
Negative: no hands, no people, no other objects, no readable text, no logos, no colored or gradient background, no cropped edges, no watermarks
```

## Worked example: photoreal hero view

A hypothetical pattern without bundled result evidence. Brass reads clearly on
white, so the default background applies; the dial's cardinal points avoid
letters.

```text
Task:
Text-to-Image (T2I)

Subject:
Prop reference of one antique brass pocket compass, about five centimetres across: a round hinged case of worn polished brass with a domed lid standing open at ninety degrees, a cream enamel dial with a fine black compass rose whose cardinal points are small triangles, a slim blued-steel needle, a small knurled crown, and a brass suspension ring at the top. Soft wear on the case edge where a thumb opens it, faint fine scratches on the lid. One compass only, lid open.

Setting:
Isolated on a pure white seamless background with a single faint contact shadow directly beneath the compass. No other objects.

Style:
Photorealistic product-reference photography, 50mm macro lens, true brass and enamel micro-texture, not CGI-waxy.

Lighting:
Soft, even, neutral studio light, gentle fill, neutral white balance, controlled highlights along the brass rim, no hotspots.

Composition:
Single isolated hero view, three-quarter angle from slightly above, the open lid and the dial both visible, the whole compass centered with margin on every side, deep focus across the object.

Constraints:
Quality: 4K, sharp material detail, clean silhouette
Negative: no hands, no chain, no other objects, no letters or numbers on the dial, no engraved text, no colored or gradient background, no cropped edges, no watermarks
```

## Worked example: stylized vehicle sheet

A hypothetical pattern without bundled result evidence. Chrome trim and a gray
character-sheet convention in the same project call for the gray background.

```text
Task:
Text-to-Image (T2I)

Subject:
Vehicle prop sheet for an original stylized-3D animated family film: one small motorcycle-and-sidecar tricycle, about two metres long. A compact motorcycle with a rounded teal fuel tank and a single round headlight, joined on its right side to a boxy covered sidecar with a curved teal roof, a cream body with a hand-painted marigold-yellow stripe, a padded red vinyl bench seat, and polished chrome grab bars. A small chrome rooster ornament stands on the front of the sidecar roof. The plate holder is empty and blank. Parked upright, headlight off. The same tricycle in all three panels, identical design.

Setting:
Neutral light-gray seamless studio background, consistent across all three panels. No people, no other vehicles, no other objects.

Style:
Original stylized-3D family-feature animation vehicle design: rounded appealing proportions, tactile painted metal with a soft clear-coat, mirror-polished chrome, clean animated-feature render quality. Not photoreal, not flat 2D.

Lighting:
Soft, even, neutral studio light, flat fill, neutral white balance, soft controlled chrome highlights, identical across all panels.

Composition:
Three panels side by side in one horizontal row with even spacing: left, the whole tricycle in a front three-quarter view from eye level; center, a full side profile from the sidecar side with both wheels and the sidecar wheel fully visible; right, a close-up of the chrome rooster ornament on the sidecar roof. Same scale in the two full-view panels.

Constraints:
Quality: 16:9 horizontal sheet, crisp stylized detail, consistent vehicle design across all panels
Negative: no letters, no words, no numbers, no plate characters, no logos, no maker badges, no people, no driver, no other vehicles, no cropped wheels, no extra panels, no watermarks
```

## QA after generation

Inspect every candidate before selection and return defects to the caller:

- the whole object is in frame with margin; nothing is cropped
- exactly the requested count; no duplicates, hands, people, or stray objects
- the silhouette separates cleanly from a uniform background
- identity-critical details read at thumbnail size
- no invented text, logos, or brand marks
- scale and proportions are plausible for the stated size
- the state matches the request
- multi-view panels share one design, scale, and lighting

## Downstream binding

When a Seedance or storyboard prompt binds the approved prop:

- reference only the selected image whose state the shot needs
- copy the approved descriptor word for word
- for blockout or reference-to-video use, add "Use only the [prop] from
  @Image N — not its background."

## Suggested file targets in this workspace

Save generated images under `projects/<project>/elements/<prop-id>/` beside the
element manifest:

- `prop_<prop-id>_hero_v<NN>.png`
- `prop_<prop-id>_sheet_v<NN>.png`
- `prop_<prop-id>_<state>-hero_v<NN>.png` for a state variant
- `prompt_prop_<prop-id>_<view>_v<NN>.md` as the exact prompt snapshot beside
  each output

Record the approved filename as `selected_variant` in the element manifest.
Acquired brand or product files record `generation: none` and have no
`prompt_prop_` snapshot.

## Quick defaults

- Model: `dola-seedream-5-0-pro-260628`
- Format: `png`
- Prompt optimization: `standard`
- Typical size:
  - `2048x2048` for hero and single views
  - `2816x1584` for multi-view sheets
- Watermark: false where the tool supports it
