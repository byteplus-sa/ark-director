# Worked Examples

Focused reference for `seedream-prompt`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Full example: T2I — Cinematic scene](#full-example-t2i--cinematic-scene)
- [Full example: Infographic visual layer](#full-example-infographic-visual-layer)
- [Full example: Image Editing — Color & Material Replacement](#full-example-image-editing--color--material-replacement)
- [Full example: Multi-image fusion](#full-example-multi-image-fusion)

## Full example: T2I — Cinematic scene

```
Task:
Text-to-Image (T2I)

Subject:
A young woman in a flowing red dress, windswept dark hair, standing at the edge of a cliff, arms slightly raised, face turned toward the horizon with a serene expression.

Setting:
A dramatic coastal cliff at golden hour. The ocean stretches endlessly below, waves crashing against rocks. Distant seabirds circle. A lighthouse is visible on a far promontory.

Style:
Cinematic, photorealistic, widescreen anamorphic look. Kodak Portra 400 film stock aesthetic.

Lighting:
Golden hour backlight, warm amber and rose tones, soft rim light on the subject's hair and dress, gentle fill from the ocean reflection. God rays breaking through scattered clouds.

Composition:
Wide shot, eye level, rule of thirds — subject positioned on the left third line, horizon on the lower third, negative space to the right filled by the ocean and sky.

Constraints:
Quality: 4K, rich textures, cinematic depth of field
Negative: no watermarks, no text overlays, no distorted anatomy, natural skin texture
```

## Full example: Infographic visual layer

This is the generative half of a hybrid. Seedream creates a text-free editorial
image layer; the caller adds all verified data, charts, labels, and title through
the deterministic static-graphics route.

```
Task:
Infographic / Information Visualization

Subject:
A text-free editorial image system about scientific research at Antarctica's Qinling Station. Place the main station building at the center. Surround it with realistic vignettes of research equipment, summer weather, fieldwork, on-site sampling, ice shelves, penguin colonies, and aurora. Leave structured negative-space panels for later data visualization; do not invent charts, labels, values, or title text.

Setting:
Clean, academic presentation layout. Antarctic landscape references in the background — ice shelves, penguin colonies, aurora.

Style:
Scientific editorial image system, National Geographic-inspired documentary photography, professional cool-toned palette.

Lighting:
Even, bright studio lighting for equipment and research vignettes. Dramatic natural lighting for the landscape elements.

Composition:
Central anchor with a radial visual flow. Reserve a clean horizontal band along the top, three empty rectangular panels on the left, one tall empty panel on the right, and a modular photo strip along the bottom. Keep the reserved panels uncluttered for deterministic charts and copy.

Constraints:
Quality: 2K, detailed documentary imagery, clean panel boundaries
Negative: no words, letters, numbers, charts, labels, logos, watermarks, or signatures
```

The deterministic finish supplies the verified title, timeline, chart geometry,
labels, values, flowchart, fonts, and alignment. Its render record binds this
selected image layer by content hash.

## Full example: Image Editing — Color & Material Replacement

```
References:
@Image 1: velvet fabric swatch (material reference)
@Image 2: color palette card — teal and gold
@Image 3: living room photo — brown leather sofa to modify

Task:
Image Editing

Editing mode:
Color & Material Replacement

Edit instructions:
Using the velvet material from @Image 1 and the teal color from @Image 2, modify the sofa in @Image 3. Replace the brown leather with teal velvet. Keep the wood frame, surrounding decor, and room lighting unchanged. The new material should catch light naturally with the same highlights and shadows as the original.

Constraints:
Quality: 2K, photorealistic material rendering
Negative: do not change the room background, do not alter the sofa's shape or proportions
```

## Full example: Multi-image fusion

```
References:
@Image 1: wooden desk on white background
@Image 2: leather-bound journal on white background
@Image 3: brass desk lamp on white background
@Image 4: porcelain teacup on white background
@Image 5: fountain pen on white background
@Image 6: composition layout sketch
@Image 7: window light reference photo

Task:
Image Editing

Editing mode:
Multi-Image Fusion

Edit instructions:
Precisely cut out the objects from @Image 1 through @Image 5 and compose them according to the layout in @Image 6 into a real still-life photograph on the desk. Use the window lighting from @Image 7 as the scene lighting reference. Ensure correct perspective, light-and-shadow, and spatial relationships. Faithfully reproduce material details — wood grain, leather texture, polished brass, glazed ceramic.

Constraints:
Quality: 2K, photorealistic, natural shadow casting
Negative: no floating objects, no mismatched lighting directions
```
