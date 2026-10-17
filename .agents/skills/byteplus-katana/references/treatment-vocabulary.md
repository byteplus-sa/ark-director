# Treatment Vocabulary

Common motion-design treatments in fast reference edits and how to build each
in HyperFrames. Use it as vocabulary for the motion inventory, not as a spec:
measure the actual reference and build what it shows.

## Reading a reference

- Most of a layered edit is motion design: cutouts, crops, type, color shapes,
  masks, flashes, counters and cuts on a beat.
- Segments that show a subject moving through space (walking, turning, pouring)
  need footage, not layers. Many references mix both, which is why routing
  reads each segment rather than the format.
- Whether a color change is an image edit or a color shift of one cutout cannot
  always be determined from frames. Decide it as a separate asset question.

## Treatment mapping

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

Frame size and duration follow the reference, whatever its aspect ratio.

## Limits

- Sub-0.5 s details sampled from frames are inferred; measure cuts at frame
  level.
- Beat alignment must be measured from the reference audio.
