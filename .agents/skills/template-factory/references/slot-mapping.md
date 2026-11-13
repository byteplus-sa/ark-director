# Slot Mapping — breakdown → prompt slots

How each `VideoBreakdown` field maps into Seedream and Seedance prompt slots.
This keeps the mapping reproducible and prevents slot drift.

## Seedance 2.5 six-part formula (via `seedance-prompt-25`)

| Six-part slot | Source field(s) | Notes |
|---|---|---|
| Subject | `elements[]` descriptors, bound to `@Image N` | Copy descriptors word for word; never summarize |
| Action | `shots[].action` + `shots[].motion.directing_prompt_text` | Per-beat stages with end states; motion direction comes from the combined breakdown |
| Scene | `elements[]` location descriptors | `@Image` binding |
| Visual style | `visual_style.grade` + `lighting_direction` + `lens` + `film_look` | Order: lighting → lens → palette. Capture-format and texture looks in `film_look` (camcorder, grain, scanlines, halation) go to the post recipe, not the prompt |
| Camera | `camera` + per-shot `shots[].camera` + `shots[].motion.camera_motion` (the pin's per-shot camera and light serve as the shot plan; `skill_owned_camera`) | One primary move and one secondary is a heuristic; preserve source paths and explicitly requested coherent choreography, resolving incompatible locks rather than dropping moves by count |
| Audio | `audio-analysis.json` soundscape, verified events and sync rules; `audio` fallback for older runs | Carry explicit sound ownership from the brief through generation and assembly using the table below. Speech presence, score-led genre and ambience do not select an owner. Describe replacement sound rather than copying source words or recordings |

## Sound ownership

| Owner | Prompt and assembly mapping |
| --- | --- |
| native | Retain requested native sound when the selected operation supports it, including wordless room tone and synchronized clicks. Use `( )` music, `< >` SFX and `{ }` dialogue only for requested layers; inspect native sound by listening at every seam and again after promotion |
| post | Generate picture with `generate_audio: false` only when supported and explicitly selected. Map verified grammar to the authorized post assets; do not invent a new bed |
| exact-master | Keep the supplied master bytes, independent sound span and offsets. Generate picture-only when supported and place the unchanged selected master in assembly |
| mixed | Name the native, retained-master and post layers separately with their spans and offsets. Preserve native cues and exact-master locks; mix only authorized layers |
| silent | Purposeful silence adds no score, ambience, effects or replacement bed. Use supported silent controls and verify the actual result |
| unresolved | Ask for missing ownership or capability evidence. Do not infer native sound, mute the picture or create post assets |

Separate sound is opt-in. Seam instability may justify a scoped proposal, not a
silent ownership change. Carry source hashes, timing locks and listening evidence
into the multi-clip assembly handoff.

## Reference binding order (Seedance)

1. Build the eligible input set from current approved Element references only.
   Storyboard boards, grids, panels and analysis sketches are never bound;
   translate their choreography into text.
2. Assign `@Image N` in the exact submitted order, with one role per input.
   Disabling review never grants eligibility.

The ordered `images[]` array must match `shot.md` `references:` exactly.

## Static element routing

| Type | Skill | Output prefix |
|---|---|---|
| character | `seedream-character-sheet` | `char_<id>_turnaround_vNN.png` |
| location | `seedream-location-asset` | `loc_<id>_wide_vNN.png` |
| prop | `seedream-prop-asset` | `prop_<id>_<view>_vNN.png` |
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
  full-color, or standalone-production-panel request; every board stays a
  planning and review artifact, never a video input.
- Delivery defaults to the smallest readable single-image grid. Paginate large
  boards or use separate panels when review needs individual images.
- Variant count defaults to 3. Honor an explicit requested count and vary only a
  supported seed for sampling variants. Human selection remains required even
  when `storyboard.review` hides the review UI.
