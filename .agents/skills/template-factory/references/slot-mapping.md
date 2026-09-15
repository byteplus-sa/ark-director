# Slot Mapping — breakdown → prompt slots

How each `VideoBreakdown` field maps into Seedream and Seedance prompt slots.
This keeps the mapping reproducible and prevents slot drift.

## Seedance 2.5 six-part formula (via `seedance-prompt-25`)

| Six-part slot | Source field(s) | Notes |
|---|---|---|
| Subject | `elements[]` descriptors, bound to `@Image N` | Copy descriptors word for word; never summarize |
| Action | `shots[].action` + `shots[].motion` imperative wording | Per-shot stages with end states; motion wording is the anti-static fix |
| Scene | `elements[]` location descriptors | `@Image` binding |
| Visual style | `visual_style.grade` + `lighting_direction` + `lens` + `film_look` | Order: lighting → lens → grade → film |
| Camera | `camera` + per-shot `shots[].camera` + `shots[].motion.camera_motion` | ≤2 moves per clip |
| Audio | `audio` | `( )` music, `< >` SFX, `{ }` dialogue; transcribe dialogue in braces; `No audio at all` when source is silent |

## Reference binding order (Seedance)

1. Build the eligible input set: current approved Element references and any
   explicitly selected production panel. Omit analysis sketches by default;
   translate their choreography into text.
2. Assign `@Image N` in the exact submitted order, with one role per input.
   Intentional control-image conditioning requires explicit selection, live
   model/mode support, and output QA; disabling review never grants eligibility.

The ordered `images[]` array must match `shot.md` `references:` exactly.

## Static element routing

| Type | Skill | Output prefix |
|---|---|---|
| character | `seedream-character-sheet` | `char_<id>_turnaround_vNN.png` |
| location | `seedream-location-asset` | `loc_<id>_wide_vNN.png` |
| prop | `seedream-prompt` | `prop_<id>_<view>_vNN.png` |
| exact screen/UI, title card, poster, product layout, price/CTA, static overlay | `html-graphic-render` | `screen_<id>_vNN.png`, `card_<id>_vNN.png`, or `overlay_<id>_vNN.png` |
| invented or illustrative screen/card imagery | `seedream-prompt` | `screen_<id>_vNN.png` or `card_<id>_vNN.png` |
| generated imagery with exact copy/layout | Seedream image layer, then `html-graphic-render` | matching deterministic screen/card/overlay prefix |

Bind the source keyframe as `@Image 1` (I2I) where the breakdown flags one.
For deterministic graphics, preserve same-stem editable source, render record,
input/font hashes, dimensions, and alpha intent. They do not use a `prompt_`
snapshot or provider task.

## Storyboard

- Panel count defaults to `shots.length`; an explicit user budget wins and must
  retain a documented mapping from every source shot to a panel or combined beat.
- Render defaults to monochrome sketch. Honor an explicit limited-palette,
  full-color, or standalone-production-panel request.
- Delivery defaults to the smallest readable single-image grid. Paginate large
  boards or use separate panels when downstream promotion needs individual images.
- Variant count defaults to 3. Honor an explicit requested count and vary only a
  supported seed for sampling variants. Human selection remains required even
  when `storyboard.review` hides the review UI.
