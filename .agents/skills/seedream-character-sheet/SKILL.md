---
name: seedream-character-sheet
description: Write structured Seedream prompts for three-panel character sheets and identity references. Invoke when the user asks for character sheets, model sheets, turnaround sheets, or Seedance-facing identity anchors.
---

# Seedream Character Sheet

Write production-grade prompts for BytePlus Seedream character-sheet generation.
This skill is specifically for **identity reference sheets**, not general
character portraits and not environment/location work.

Use this skill when the user wants:
- a character sheet
- a model sheet
- a turnaround-style identity sheet
- a Seedance-facing identity anchor
- a reusable `elements/<character-id>/char_<character-id>_<sheet-type>_v<NN>.png` asset

This skill is designed to partner with:
- `seedream-prompt` for general Seedream image prompting
- `seedream-character-sheet-cleanup` after generation when a full-body panel
  still shows a readable extra face
- `seedream-edit` for cleanup or local post-generation fixes

Do **not** use this skill for:
- one-off portraits
- posters or key art
- location assets
- product or prop sheets (use `seedream-prop-asset`)
- environment stills

## Default production rule

For project character sheets, default to a **three-panel** layout unless the
user explicitly asks for more angles:

1. **Back full-body**
2. **Front full-body**
3. **Face close-up**

Use a **plain gray** studio background and **neutral, even studio lighting**
by default. Lighting never changes to fit a scene or mood — character sheets
are identity references, not scene stills. The sheet lighting stays neutral
unless the user explicitly asks otherwise.

## Why this layout

This layout is optimized for downstream identity consistency:
- the back view preserves costume, silhouette, hair, and headwear logic
- the front full-body view preserves stance and overall costume read
- the close-up panel acts as the canonical face anchor

Compared with a five-view turnaround, this structure is simpler, easier to
read, and more stable for later Seedance and Seedream reference use.

## Flexible prompt structure

Use this order for the sections that apply. Do not add empty boilerplate:

- **References** only when images are provided
- **Task** when the mode needs clarification
- **Subject** and **Composition** for every character sheet
- **Setting**, **Style**, and **Lighting** when they add relevant direction
- **Text in image** only when labels or other readable text are requested
- **Constraints** only for useful quality, continuity, and exclusion requirements

## 1. References (when provided)

List every reference image the user provides.

```text
References:
@Image 1: character face or approved identity reference
@Image 2: wardrobe or costume reference
@Image 3: style or film still reference
```

Rules:
- Omit the References section when no images are provided.
- If an approved character sheet already exists, use it as `@Image 1` for
  continuity.
- If the user has a preferred costume or hair reference, separate those by role
  rather than blending them ambiguously into one description.
- Bind every reference again where it affects the output: for example, “Use the
  identity and facial traits from @Image 1,” “use the wardrobe from @Image 2,”
  and “use the photographic treatment from @Image 3.” A reference inventory
  alone is not sufficient.

## 2. Task type

Use **Text-to-Image (T2I)** only when the prompt uses no reference images.

Use **Image-to-Image (I2I)** whenever any reference image guides identity,
wardrobe, hair, style, composition, or another visible output property. This
includes first-pass character sheets assembled from face, costume, or style
references; it is not limited to revisions of an already-approved sheet.

## 3. Subject

Describe the person and the exact three-panel requirement.

```text
Subject:
[Character identity, age, ethnicity, facial features, hair, clothing, accessories, same person in all panels, three panels only: back full-body, front full-body, face close-up.]
```

Always include:
- an inline binding for each supplied reference in the section it controls
- age
- ethnicity / cultural identity when relevant
- 2–4 stable facial traits
- hair and headwear
- costume
- key accessories
- **a relaxed neutral expression** — the sheet is an identity reference, so the
  face must stay readable and emotionless; the model otherwise injects arbitrary
  mood (smiles, frowns, glare) that bleeds into every downstream use
- explicit statement that it is the **same person in all panels**

Signature accessories the character always wears — eyewear, a hat, a helmet,
jewelry, footwear — belong in the descriptor word for word **as part of the
outfit**, so identity and costume stay consistent across generations.

Use this canonical neutral-expression phrase verbatim in every character sheet:

```text
Relaxed neutral expression in all panels: mouth relaxed and closed, eyes looking straight into camera, no smile, no frown, no raised brows, no emotion.
```

**Never put held props in the character sheet.** Anything the character holds,
carries, aims, or operates on camera (devices, weapons, tools, bags) is a
separate from the character identity. Exclude held items from the sheet.
Branded, recurring, or story-critical objects need a dedicated `prop_` reference
(see `seedream-prop-asset`) bound downstream; incidental objects may remain
text-only in a scene.

**Scene-variant wearables are props, not outfit.** A wearable that is not worn
in every scene (e.g. sunglasses the character wears in some scenes and removes
in others) must be **excluded from the character sheet** and generated as a
`prop_` sheet instead. Only include wearables that are always part of the look
in every scene.

## 4. Setting

The setting for character sheets is typically simple and controlled.

```text
Setting:
Clean plain gray studio background, consistent across all three panels.
```

Default:
- plain gray seamless background
- no props
- no held objects
- no furniture
- no environmental clutter

Only deviate if the user explicitly wants a stylized or filmic sheet background.

## 5. Style

Define the image language.

```text
Style:
[Photorealistic, cinematic, editorial, film still, grounded realism, wardrobe-reference quality.]
```

Recommended anchors:
- photorealistic
- cinematic
- naturalistic editorial reference
- grounded realism
- film-photo finish

For a realistic (non-AI-looking) sheet, add the anti-AI-look cues: documentary
editorial portrait photography, shot on a
full-frame camera with a 50mm lens, visible skin pores, fine flyaway hair,
subtle film grain, and slight facial asymmetry. Keep skin matte and diffuse — never glossy, never reflective —
and forbid plastic/airbrushed skin and unnatural symmetry in Constraints.

## 6. Lighting

Character sheets use **neutral, even studio lighting** — never scene-specific
lighting. Do not change the light to match the character's world or story mood;
the sheet is an identity reference, so lighting must stay flat, readable, and
identical across all panels.

```text
Lighting:
[Soft, even, neutral studio light, flat fill, no mood, no dramatic shadows, no light reflection on the skin, consistent across all panels.]
```

Default:
- soft studio key
- gentle even fill
- neutral white balance
- no scene mood, no color cast
- no hotspots
- no blown highlights
- no specular shine, flash, gloss, or light reflection on the skin — matte, diffuse skin texture that absorbs light evenly, never glossy, never reflective

The same neutral lighting is used for every character sheet regardless of what
lighting the scene or character's world uses.

## 7. Composition

Explicitly enforce the three-panel structure.

```text
Composition:
Three-panel character sheet with even spacing: back full-body view on the left, front full-body view in the center, face close-up on the right. Eye-level camera, consistent framing across the two body panels, relaxed neutral expression in every panel.
```

Core rules:
- three panels only
- back full-body first
- front full-body second
- frontal close-up third
- same character identity across all panels
- relaxed neutral expression across all panels, face square to camera in the close-up
- readable costume silhouette in the body panels
- close-up panel is the face authority

## 8. Text in image

Omit this section by default. Include it only when the user requests
labels or other readable text. For production character sheets, avoid text
overlays unless requested.

## 9. Constraints

Use quality + negative constraints together:

```text
Constraints:
Quality: 4K, consistent character identity across all panels
Negative: no extra panels, no side profile, no 3/4 view, no props, no held objects, no weapons, no light reflection on the skin, no text overlays, no watermarks, no distorted anatomy
```

Common negatives:
- no extra panels
- no profile panel
- no 3/4 panel
- no props in hands
- no held objects, weapons, or carried items
- no background variation
- no scene lighting or color cast
- no exaggerated expressions, no smiling, no frowning, no strong emotions
- no glossy skin, no specular shine, flash, or light reflection on the skin
- no plastic skin, no airbrushed skin, no over-smoothing, no waxy texture, no CGI sheen
- no unnatural symmetry
- no distorted hands
- no extra fingers
- no watermark

## Standard prompt template

```text
Task:
Text-to-Image (T2I)

Subject:
Character reference sheet, single character [name / description]. Same person in all panels, consistent identity. Relaxed neutral expression in all panels: mouth relaxed and closed, eyes looking straight into camera, no smile, no frown, no raised brows, no emotion. Three-panel sheet only: one full-body back view, one full-body front view, and one face close-up panel. Worn outfit elements only — hat, helmet, always-worn eyewear, jewelry — nothing held in the hands, no props, no weapons.

Setting:
Clean plain gray studio background, consistent across all three panels. No props, no held objects, no furniture, no background variation.

Style:
Documentary editorial portrait photography, shot on a full-frame camera with a 50mm lens, natural skin texture with visible pores, subtle film grain, professional character-sheet quality, consistent skin tone and wardrobe detail across all panels. Realistic, not airbrushed.

Lighting:
Soft, even, neutral studio light, flat fill, neutral white balance, no mood, no dramatic shadows, no light reflection on the skin, no specular shine or flash on the skin, identical lighting across all panels.

Composition:
Three-panel character sheet with even spacing: back full-body view on the left, front full-body view in the center, face close-up on the right. Eye-level camera, consistent framing across the two body panels, relaxed neutral expression in every panel.

Constraints:
Quality: 4K, rich skin texture, natural hair detail, consistent character identity across all panels
Negative: no props in hands, no held objects, no weapons, no background variation, no scene lighting or color cast, no exaggerated expressions, no smiling, no frowning, no strong emotions, no glossy skin, no light reflection on the skin, no specular shine or flash on the skin, no plastic skin, no airbrushed skin, no over-smoothing, no waxy texture, no CGI sheen, no unnatural symmetry, no extra panels, no side profile, no 3/4 view, no text overlays, no watermarks, no distorted anatomy, no extra fingers
```

## Worked example: Film-style pirate sheet

This example mirrors the user-provided sample image in `examples/`.

```text
Task:
Text-to-Image (T2I)

Subject:
3-view character reference sheet for a film character. The same man in all three views: youthful attractive man in his early 30s, warm olive-brown skin, dark thick curly hair, thin mustache with a small soul-patch under the lip, faint stubble along the jaw, two small silver hoop earrings on the left ear, thin silver chain necklace, subtly asymmetrical face, a small subtle healed scar near the right eye. Age-of-sail pirate costume: faded mustard-yellow durag tied at the back with the tails hanging down, small shark tooth pendant attached to the durag above the left temple, open off-white linen shirt, worn dark leather vest, wide sash belt, baggy dark breeches, scuffed leather boots, weathered and dirty fabrics. Relaxed neutral expression in all panels: mouth relaxed and closed, eyes looking straight into camera, no smile, no frown, no raised brows, no emotion. Three panels only: full-body back view, full-body front view, and frontal face close-up.

Setting:
Plain gray seamless studio backdrop, consistent across all three panels, with thin subtle vertical divider lines separating the panels.

Style:
Gritty cinematic 35mm film photograph, naturalistic editorial reference, fine film grain, organic matte skin texture, never plastic CGI skin.

Lighting:
Very soft, even, neutral studio light, flat fill, neutral white balance, no mood, no dramatic shadows, no light reflection on the skin, no hotspots, no blown highlights, identical lighting across all three panels.

Composition:
Three panels side by side in a single horizontal row. Left panel: full-body back view. Center panel: full-body front view. Right panel: frontal close-up portrait from the chest up, face square to camera, relaxed neutral expression. Consistent identity, costume, scar, accessories, proportions, and lighting across all panels.

Constraints:
Quality: 16:9 horizontal sheet, film-photo finish, consistent identity across all panels
Negative: no extra panels, no 3/4 view, no profile view, no props, no missing limbs, no prosthesis, no glossy skin, no light reflection on the skin, no exaggerated expressions, no smiling, no frowning, no strong emotions, no watermarks, no text overlays
```

## Workflow pairing

Recommended sequence:
1. Use this skill to write the character-sheet prompt.
2. Generate the sheet with Seedream.
3. Inspect the body panels for extra readable faces.
4. If needed, optionally compose with `seedream-character-sheet-cleanup`.
5. Save each generated result under `elements/<character-id>/` beside `character.md`.
6. Record the approved filename as `selected_variant` in `character.md`; keep reference images in the same element folder using the `ref_<NN>_...` convention.

## Example asset

The user-provided sample image is stored beside this skill:
- `examples/pirate-character-sheet-generated-sample.png`

Use it as a visual target for layout and panel balance, not as a literal
identity reference unless the user explicitly asks for that specific character.
Note: the sample was generated with a moodier, low-key film look that predates
the current plain-gray-background / neutral-lighting default; do not copy its
lighting into new sheets.
