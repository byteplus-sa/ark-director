# Style Catalog

Focused reference for `seedance-restyle`. Read [the entrypoint](../SKILL.md) for
routing, rules and caller responsibilities.

Each entry is a `[Style]` fragment plus what to watch. A fragment names the
medium first, then line, surface, light and cadence. It applies to every
element in frame. Use one entry per take; adapt the wording to the source
rather than pasting extra adjectives.

| Group | IDs |
| --- | --- |
| Drawn 2D | `cel-anime-2d`, `painterly-watercolor`, `gouache-storybook`, `rubber-hose-1930s`, `comic-halftone`, `ink-wash`, `pencil-sketch`, `wax-crayon`, `pixel-art`, `flat-vector` |
| Handcrafted and stop motion | `paper-cutout`, `plasticine-claymation`, `needle-felt`, `wood-puppet`, `toy-miniature` |
| Rendered 3D | `stylized-handcrafted-3d`, `low-poly-3d`, `pearlescent-silicone` |
| Fine art | `oil-impasto`, `woodblock-print`, `stained-glass` |
| Capture looks | `film-noir`, `camcorder-1990s`, `neon-synthwave` |

## Drawn 2D

### cel-anime-2d

```text
The entire video is redrawn as clean 2D cel animation: crisp ink outlines,
two-tone cel shading, painted backgrounds with soft gradients, and saturated
but controlled colour.
```

- **Watch:** faces simplify; keep hair shape and wardrobe colours as identity
  cues. Fast motion may gain smear frames; the pose at each beat still matches.

### painterly-watercolor

```text
The entire video is redrawn as watercolor animation on cold-press paper: soft
pigment blooms, wet edges, visible paper grain, and light pencil underdrawing.
```

- **Watch:** washes bleeding across subject edges; ask for clear edges on faces
  and hands.

### gouache-storybook

```text
The entire video is redrawn as opaque gouache storybook painting: flat matte
colour shapes, dry-brush texture, simplified forms, and warm diffuse light.
```

- **Watch:** backgrounds flattening into one colour field; keep set layout.

### rubber-hose-1930s

```text
The entire video is redrawn as 1930s rubber-hose cartoon animation: bendy
limbs, pie-cut eyes, black-and-white ink with grey tones, soft film grain, and
bouncy squash-and-stretch.
```

- **Watch:** anatomy turning noodle-like can change the read of a pose; keep
  hand positions at contact moments.

### comic-halftone

```text
The entire video is redrawn as a printed comic: bold black ink lines, flat
spot colour, halftone dot shading, and slight print misregistration.
```

- **Watch:** generated speech balloons or sound-effect lettering; state that no
  lettering appears.

### ink-wash

```text
The entire video is redrawn as monochrome ink-wash painting: expressive brush
strokes, graded grey washes, rice-paper texture, and generous empty space.
```

- **Watch:** small subjects dissolving into wash; keep each person's silhouette
  readable.

### pencil-sketch

```text
The entire video is redrawn as a graphite pencil sketch on off-white paper:
loose construction lines, cross-hatched shading, smudged midtones, and gentle
line boil.
```

- **Watch:** heavy line boil hides faces; ask for steady lines on faces.

### wax-crayon

```text
The entire video is redrawn as wax-crayon and coloured-pencil animation on
textured paper: pigment buildup, imperfect layered outlines, bold handmade
colour, and lively line boil.
```

- **Watch:** backgrounds switching instead of redrawing between frames.

### pixel-art

```text
The entire video is redrawn as 16-bit pixel art: a limited palette, crisp
square pixels, dithered shading, and sprite-like characters with clean
outlines.
```

- **Watch:** pixel size drifting between shots; state one consistent pixel
  scale. Faces carry few details, so wardrobe colour carries identity.

### flat-vector

```text
The entire video is redrawn as flat vector animation: clean geometric shapes,
solid fills with subtle gradients, no outlines, and smooth motion.
```

- **Watch:** generated icons or text; exact UI and type belong to deterministic
  graphics, not this style.

## Handcrafted and stop motion

### paper-cutout

```text
The entire video is rebuilt as layered paper-cutout animation: cut card shapes
with visible edges, small drop shadows between layers, fibre texture, and
slightly stepped motion.
```

- **Watch:** stepped cadence; the pose at each beat still matches the source.

### plasticine-claymation

```text
The entire video is rebuilt as plasticine claymation: visible thumbprints and
tool marks, soft key light on a small tabletop set, and slightly stepped
stop-motion cadence.
```

- **Watch:** fast source motion softens; keep each beat's pose and position.

### needle-felt

```text
The entire video is rebuilt as needle-felted wool stop motion: fuzzy fibre
surfaces, soft rounded forms, felted miniature props, and warm practical light.
```

- **Watch:** fine detail such as fingers merging; keep hand count and grip.

### wood-puppet

```text
The entire video is rebuilt as carved-wood puppet stop motion: visible wood
grain and joint pins, sewn cloth costumes, tool marks, and deliberate stepped
movement.
```

- **Watch:** drifting into claymation; joints must stay rigid.

### toy-miniature

```text
The entire video is rebuilt as a practical toy miniature: articulated plastic
figures with molded seams, toy-scale props and set, tilt-shift shallow depth of
field, and bright even light.
```

- **Watch:** limbs bending beyond toy joints; toys turning back into people.

## Rendered 3D

### stylized-handcrafted-3d

```text
The entire video is rebuilt in a stylized handcrafted 3D animated look: soft
rounded forms, subsurface-lit skin, gentle global illumination, and a warm
storybook grade.
```

- **Watch:** proportions changing identity; keep hair shape and wardrobe.

### low-poly-3d

```text
The entire video is rebuilt as low-poly 3D: faceted flat-shaded geometry, a
limited pastel palette, soft ambient occlusion, and clean silhouettes.
```

- **Watch:** faces losing expression; carry performance through head and body
  angles.

### pearlescent-silicone

```text
The entire video is rebuilt as pearlescent silicone sculpture: soft translucent
forms, iridescent sheen, smooth seamless surfaces, and studio softbox light.
```

- **Watch:** subjects merging with set surfaces; keep separation and contact
  shadows.

## Fine art

### oil-impasto

```text
The entire video is redrawn as thick oil impasto painting: visible palette-knife
ridges, rich layered colour, painterly highlights, and canvas weave.
```

- **Watch:** stroke texture crawling frame to frame; ask for a stable canvas.

### woodblock-print

```text
The entire video is redrawn as a traditional woodblock print: carved outlines,
flat layered colour blocks, wood-grain texture in fills, and stylized waves and
clouds.
```

- **Watch:** perspective flattening the camera move; keep the source parallax.

### stained-glass

```text
The entire video is redrawn as stained glass: jewel-toned glass panes, thick
dark lead lines, light glowing through coloured glass, and subtle surface
ripples.
```

- **Watch:** lead lines cutting through faces; keep lines along natural edges.

## Capture looks

These change the capture medium and grade while the world stays photographic.

### film-noir

```text
The entire video becomes black-and-white film noir: hard low-angle key light,
deep shadows, high contrast, and fine silver grain.
```

- **Watch:** faces lost in shadow; keep them readable in the key light.

### camcorder-1990s

```text
The entire video becomes 1990s consumer camcorder footage: soft interlaced
video texture, slight chroma bleed, warm auto white balance shifts, and mild
highlight bloom.
```

- **Watch:** generated date stamps or on-screen display text; add those in post.

### neon-synthwave

```text
The entire video is restyled with neon synthwave light: magenta and cyan rim
light, glowing edges, deep violet shadows, light haze, and a retro scanline
texture.
```

- **Watch:** generated neon signage text; signage stays abstract shapes.

## Custom style from reference images

When the user supplies their own style images, write a custom entry:

- **ID:** `custom-<kebab-case-medium>`
- **Medium lock:** what the visible world is made of, read from the images.
- **Line and surface:** two to four observable traits.
- **Light and palette:** the light quality and dominant colours.
- **Cadence:** smooth, stepped or redrawn.
- **Watch:** the likely drift.

Bind each style image with the style-only role in
[restyle grammar](restyle-grammar.md#style-reference-images).
