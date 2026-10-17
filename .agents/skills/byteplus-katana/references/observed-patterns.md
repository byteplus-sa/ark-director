# Observed Patterns in Published Katana Edits

Observed 2026-10-15 by sampling frames from Higgsfield's own launch trailer
(X post of 2026-10-09, 78 s, also on YouTube) and the showcase and community
preset previews on its Katana page. These are vendor showcase pieces, not
independent tests and not guaranteed outputs. Use them as a vocabulary for the
motion inventory, not as a spec.

## What the samples show

| Sample | Length, size | Structure |
| --- | --- | --- |
| Page showcase reel | 11.1 s, 1080x608 | One new character in many poses and crops, a cut about every 0.55 s, red type slammed over the subject, negative-flash frames, magazine and grass collage backgrounds, a circular-mask face close-up, a night wide shot that resolves into a black-and-white high-contrast cutout with red type curved behind and around the figure |
| Fashion lookbook preset | 12.1 s, 9:16 | Sticker-outlined cutouts, a lineup of the same figure with bracket markup and "WHICH ONE?", counters such as `LOOK 06 / OVERPASS 15/15`, then short walking-person footage with type slams |
| Palette preset | 11 s, 9:16 | One standing figure cutout, four palette cards ("02 CHERRY, palette 02/04"), colored paper shapes behind the figure, the garment color changing per palette |
| Pink fashion preset | 15 s | Model cutouts on glass-panel and mirror layouts with lookbook captions |
| Explainer-style preset | 29 s, 4:3 | Kinetic type ("Edits", "YOU'RE"), magnifier and bracket callouts, glitch collage over mixed imagery |
| Dark cinematic preset | 11 s | X-ray figure, keyhole vignette, street and stair footage of a man; reads as generated or stock footage rather than layers |

The launch trailer also shows the Claude chat UI running a Higgsfield Katana
connector with the Opus 5.5 model selector, a prompt such as "Aura farming edit
of my car", and the result built from photos of that car with kinetic type
("BIG ENGINES", "BLOOD", "MAKE ENGAGING EDITS"). A title card reads
"CONTEXT-AWARE SHOT GENERATION" (small on screen at about 44 s), so some shots
are generated.

## Reading

- Most of each edit is layered motion design: cutouts, crops, type, color
  shapes, masks, flashes, counters and fast cuts on a beat.
- Person-in-motion shots (walking, dribbling) and cinematic street footage look
  generated, and the trailer says so. The same preset mixes both: the fashion
  lookbook is mostly cutouts with a few walking shots. This is why routing
  reads each segment rather than the format.
- Whether outfit color changes in the palette preset are image edits or color
  shifts of one cutout is not determinable from the frames.

## Vocabulary and HyperFrames mapping

| Observed treatment | Build as |
| --- | --- |
| Cut every 0.3–0.6 s on the beat | Timeline segments from the beat grid; no easing between cuts |
| Type slam over the subject | Large display type, scale or translate keyframes with a fast ease-out, text in front of or behind the cutout |
| Type curved around or behind a cutout | SVG `textPath` or CSS 3D transform behind the alpha layer |
| Negative or invert flash | CSS `filter: invert(1)` for one to three frames |
| Black-and-white high-contrast treatment | CSS `grayscale` plus `contrast` on the layer |
| Collage or magazine background | Tiled or scattered image layers with slow drift |
| Circular or keyhole mask | `clip-path: circle()` with animated radius |
| Sticker outline around a cutout | Dilated alpha as a white stroke layer under the cutout |
| Counters and captions (`LOOK 06 / 15`, `palette 02/04`) | Deterministic HTML text, stepped by the EDL |
| Colored paper shapes behind a figure | Flat SVG shapes with parallax offsets |
| Palette or colorway variants | One shared layout with swapped color tokens; garment recolor is a separate asset decision |
| Glitch, shake, scan lines | Short displacement or channel-offset passes, 2–6 frames |

Frame size follows the reference. These edits ran from 9:16 to 4:3 and 16:9,
and preset durations from 11 to 29 s.

## Limits of this evidence

- Frames were sampled at 0.5–2 s steps, so sub-0.5 s details are inferred.
- Audio was not analyzed. Beat alignment must be measured from the reference.
- Output quality of user-supplied photos is not shown by any of these samples.
