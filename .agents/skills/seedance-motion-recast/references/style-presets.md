# Style Presets

Focused reference for `seedance-motion-recast`. Read [the entrypoint](../SKILL.md)
for mode selection, gates and caller responsibilities.

Each preset is a `[Style]` fragment plus what it changes and what it must keep.
Presets never change the Motion Authority: pose sequence, screen positions,
camera path, cuts and timing stay with `@Video 1`. Use one preset per take
unless the user asks for a blend. Chain look phrases in the order lighting →
lens → grade → sensor or medium.

Character, product and location references must already be designed in the
preset's look. A photoreal sheet under a clay preset leaks photoreal skin, so
build or select elements in the target medium first.

For medium-driven looks (claymation, toy miniature, handcrafted 3D, painterly
2D), the `seedance-animation-styles` skill has matching recipes by name:
`plasticine-claymation`, `toy-miniature`, `stylized-handcrafted-3d` and
`painterly-2d`. Borrow its material-motion vocabulary when composing; it is a
composition hint, not a required load.

| Preset | Changes | Keeps |
| --- | --- | --- |
| [anime-to-live-action](#anime-to-live-action) | Drawn cast and world become photoreal | Poses, staging, cuts, camera |
| [live-action-to-anime](#live-action-to-anime) | Photoreal becomes 2D cel animation | Poses, staging, cuts, camera |
| [claymation](#claymation) | Everything becomes plasticine | Motion beats and positions |
| [camcorder-1990s](#camcorder-1990s) | Capture medium and grade | Everything staged |
| [film-noir](#film-noir) | Light, grade, wardrobe era | Motion and framing |
| [luxury-commercial](#luxury-commercial) | Light, surfaces, polish | Motion and product path |
| [market-localization](#market-localization) | City, cast, signage language | Motion, product, beats |
| [product-hero-relight](#product-hero-relight) | Light on the product and set | Product identity and path |
| [period-costume](#period-costume) | Wardrobe, set dressing, era | Motion and staging |
| [sci-fi-retrofit](#sci-fi-retrofit) | Set and wardrobe to near-future | Motion and staging |
| [toy-miniature](#toy-miniature) | Scale and materials to toys | Motion and camera path |
| [handcrafted-3d](#handcrafted-3d) | Photoreal becomes stylized 3D feature look | Poses and timing |

## anime-to-live-action

```text
The visuals feature naturalistic daylight with soft bounce, a 35mm lens with
gentle depth of field, a neutral filmic grade, and real skin, fabric, and hair
texture with fine grain.
```

- **Changes:** outlines, flat fills and exaggerated proportions become real
  anatomy, materials and light.
- **Keeps:** every pose, position, camera move and cut. Exaggerated anime
  motion (smears, impossible leaps) is kept as timing, not physics.
- **Note:** character references must be photoreal sheets; describe no studio
  or franchise by name.

## live-action-to-anime

```text
The visuals feature clean 2D cel animation with crisp ink outlines, two-tone
cel shading, painted backgrounds with soft gradients, and saturated but
controlled color.
```

- **Changes:** photoreal surfaces become flat shaded drawings; backgrounds
  become painted.
- **Keeps:** poses, framing, camera path and cut timing.
- **Note:** references are drawn character and background sheets in this look.
  Name no studio, artist or franchise.

## claymation

```text
The visuals feature plasticine characters and set with visible thumbprints and
tool marks, soft key light on a small tabletop set, and slightly stepped
stop-motion cadence.
```

- **Changes:** all surfaces become clay; motion gains a stepped cadence.
- **Keeps:** beat timing, positions and camera path. Stepped cadence may soften
  fast source motion; the pose at each beat must still match.

## camcorder-1990s

```text
The visuals feature on-camera flash-like fill, soft interlaced 4:3 video
texture, slight chroma bleed and warm auto-white-balance shifts.
```

- **Changes:** capture medium, grade and sharpness.
- **Keeps:** every staged element and the camera path; handheld shake stays as
  the source moved, no extra shake.
- **Note:** no date stamp or on-screen display; add one in post if wanted.

## film-noir

```text
The visuals feature hard low-angle key light with deep shadows, venetian-blind
patterns on the walls, a 40mm lens, high-contrast black-and-white, and fine
silver grain.
```

- **Changes:** light, grade to monochrome, wardrobe and set era through the
  references.
- **Keeps:** motion, framing and cuts; faces stay readable in the key light.

## luxury-commercial

```text
The visuals feature large soft key light with controlled specular highlights,
a macro-capable 85mm lens with shallow depth of field, a clean warm-neutral
grade, and polished glass, metal, and fabric surfaces.
```

- **Changes:** light quality, surface polish, set minimalism.
- **Keeps:** motion, product path and contact windows; product markings stay as
  the product reference shows them.

## market-localization

```text
The visuals feature the natural daylight and street palette of <city>,
<local architecture and materials>, with signage shown as color and shape only.
```

- **Changes:** location, cast and local dressing, all through approved
  references for that market.
- **Keeps:** motion, product identity, beats and the product's screen position.
- **Note:** every recast talent follows the consent gates; local-language copy
  is added in post, never generated.

## product-hero-relight

```text
The visuals feature a single strong rim light tracing the product edges, a
dark gradient backdrop, slow-moving reflections across the surface, and a
crisp neutral grade.
```

- **Changes:** set and light around the product.
- **Keeps:** the product's shape, markings, path, rotation and contact windows.
- **Note:** use the approved or authorized product reference; this preset never
  redesigns the product.

## period-costume

```text
The visuals feature <era> daylight through tall windows, <era-appropriate
fabrics and set dressing>, a warm muted grade, and soft film grain.
```

- **Changes:** wardrobe and set to the named era, through period character and
  location references.
- **Keeps:** motion and staging; modern objects in the source get a disposition
  (removed or restyled).

## sci-fi-retrofit

```text
The visuals feature cool practical panel light mixed with warm work lamps,
brushed metal and worn composite surfaces, a teal-steel grade, and light haze.
```

- **Changes:** set and wardrobe to a near-future look through references.
- **Keeps:** motion, positions, camera path and cuts; screens show abstract
  light patterns, not text.

## toy-miniature

```text
The visuals feature a tabletop toy world with glossy molded plastic, visible
seams and joints, tilt-shift shallow depth of field, and bright even light.
```

- **Changes:** scale, materials and articulation to toys.
- **Keeps:** motion beats and camera path; limb motion reads within toy joint
  limits, and the pose at each beat still matches.

## handcrafted-3d

```text
The visuals feature a stylized handcrafted 3D animated look with soft rounded
forms, subsurface-lit skin, gentle global illumination, and a warm storybook
grade.
```

- **Changes:** photoreal cast and world become stylized 3D.
- **Keeps:** poses, timing and camera path; facial performance is carried as
  readable expressions.
- **Note:** name no studio or franchise.
