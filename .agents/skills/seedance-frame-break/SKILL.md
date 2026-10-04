---
name: seedance-frame-break
description: >-
  Write and QA Seedance 2.5 prompts for the frame-break pop-out effect (3D
  billboard look): two solid black bars at the top and bottom of a 16:9 frame
  with the subject's nearest limbs or clothing drawn in front of the bars in
  full colour, so the subject bursts toward the viewer. Covers the three-layer
  prompt contract, four timed stages with observable End states, a fixed
  camera, scenic backdrops, a product-hero variant, failure repairs and a
  frame-based pixel check of bar thickness and overlap. Use for pop-out,
  frame-break, 3D billboard, a character bursting out of black bars, or a
  product hero ad whose product breaks the frame. Not for ordinary cinematic
  letterbox, general camera moves (seedance-camera-presets), the base prompt
  grammar (seedance-prompt-25), edits to existing footage, or task submission.
---

# Seedance Frame Break

Frame break is a pop-out look: two flat black bars sit at the top and bottom of
a 16:9 picture, the scene lives in the window between them, and the subject's
nearest limbs or clothing are drawn complete on top of the bars in full colour.
The subject appears to burst out of the screen toward the viewer.

This is a prompt-authoring and review leaf. It never submits, polls or deletes
generation tasks; the caller owns the task lifecycle.

## Composition

| Concern | Owner |
| --- | --- |
| Six-part formula, `@Image N` roles, timestamp rules, audio brackets | `seedance-prompt-25` |
| Locked-off camera wording | `seedance-camera-presets` |
| Identity reference for a character | `seedream-character-sheet` |
| Medium and material rules for a stylised subject | `seedance-animation-styles` |
| End cards or any on-screen text | `html-graphic-render` and `ffmpeg` in post |
| Real brand or product assets | [Element identification](../../contracts/element-identification.md) |

These are composition hints; this leaf does not load sibling skills. Do not
restate the base grammar here.

## The technique in one screen

Three layers, back to front:

1. **Scene**: the backdrop fills only the central window between the bars.
2. **Bars**: two flat, solid black graphic bars, about 12 percent of the frame
   height each, static, laid over the picture. They are graphics, not the
   camera's letterbox.
3. **Subject**: drawn complete on top of the bars wherever it crosses them, in
   full colour, never clipped or hidden by a bar.

Supporting rules:

- The camera is fixed and locked off, with a wide-angle look. The subject does
  not travel toward the lens; scale grows only for the limb or hem that extends.
- Break-outs are events, not a state. The subject is full-body and completely
  inside the central window at the start and at every stage boundary, with both
  bars fully visible and clear of it, and fills about two thirds of the window
  height. Each break-out is a brief, specific limb or hem extension during a
  stage (a fist and forearm over the upper bar, a robe hem flaring over the
  lower bar), after which the subject returns inside. Between break-outs
  nothing overlaps a bar. The subject never walks or leans closer so that torso
  or legs end up over a bar.
- The bars never move. Their inner edges stay perfectly straight, horizontal and
  at the same height in every frame; whatever covers them sits on top and never
  changes them, and when a limb withdraws the straight edge is simply visible
  again. Moving bars fail the take.
- Keep any extending limb from filling a third of the frame: a near-lens limb
  or head distorted the bar edge. This is about protecting the bars, not about
  making the subject big.
- Bars of 17 to 21 percent shrink the window and push the subject over them.
  Ask for about 12 percent and state once that the central window is the large
  majority of the frame height.
- The lower bar is crossed far more reliably than the upper bar. The upper bar
  needs its own stage, a limb or hem that plausibly reaches it, an explicit peak
  ("the open palm covers the upper bar") and an End state back inside.
- If the model reads the bars as camera letterbox, the subject stays behind or
  clipped by them and the effect is lost. Describe the bars as an overlay and
  give numeric overlap anchors.

## Input and output contract

Input:

- A brief: subject type, scene, mood, audio intent, and whether bars are wanted
  at the default of about 12 percent.
- Approved identity references with hashes (a character sheet, or real product
  photos) and their rights status from the caller.
- Duration and resolution from the caller; they belong in request parameters,
  not in prompt text. The ratio is 16:9.

Output: a prompt package with ordered `@Image N` bindings and roles, the seven
prompt blocks below, suggested parameters (`16:9`, the lowest suitable
resolution, `generate_audio` per the audio intent, `watermark: false` where
supported), the preflight result, open items, and a QA plan. The caller owns
prompt review, the request hash and submission. Plan a small set of takes so
the cleanest can be chosen.

## Required prompt blocks

Write them in this order. Read
[prompt template](references/prompt-template.md) for the slots and a worked
example.

1. **Identity lock.** `@Image 1` defines the subject's face, hair, clothing and
   art style only. State that the sheet layout, panel borders and background
   are ignored. Never ask the output to reproduce the sheet.
2. **Main idea.** One sentence: who bursts out of the black bars and how,
   followed once by a sentence fixing the bars: two fixed black bar graphics
   with perfectly straight horizontal inner edges at the same height in every
   frame.
3. **Four timed stages.** Each stage has one coherent action by one named
   limb (use screen-left and screen-right), the bar it crosses with a numeric
   anchor such as covering about a third of the bar's width, the crossing
   direction, the moment it peaks, and an observable `End state:` with the
   subject back fully inside the window and nothing over a bar. The limb that
   arrives at the lens is the limb that crosses the bar; no other limb takes
   over mid-stage, and
   two different limbs never cross in the same beat. Other limbs stay small and
   tucked behind until a later stage.
4. **Frame and layer order.** The three layers back to front, the bars as
   flat static 2D graphics drawn under the subject, never moving or bending,
   with the constant-height phrase repeated and the rule that whatever covers
   them never changes them. State once that the central window is the large
   majority of the frame height and the subject is full-body inside it,
   except during the named break-outs.
5. **Camera.** Locked off, no movement, zoom or cuts; only the subject moves.
6. **Audio.** Requested sound arc in the `seedance-prompt-25` bracket syntax.
   When no music is wanted, say so.
7. **Closing exclusions.** Short: no text, captions, logos or watermarks, no
   held props, bars unmarked. Keep necessary exclusions to one or two lines.

Stage roles: stage 1 establishes the full-body subject inside the window with
no overlap and may add a small first gesture; stage 2 has a lower-bar break-out;
stage 3 has an upper-bar break-out; stage 4 delivers the hero break-out and
resolves back inside. Every stage begins and ends inside the window. Timestamps are time allocations, so the End state should
be reachable about half a second before each boundary. Do not state the clip
duration in prompt text.

## Procedure

1. **Route check.** Confirm the request is a frame-break effect, not ordinary
   letterbox or a camera move, and not an edit of existing footage.
2. **Subject and scene.** Pick the subject type and a calm backdrop. Read
   [scenes and subjects](references/scenes-and-subjects.md).
3. **Product only.** For a product-only hero ad read
   [product hero](references/product-hero.md) before writing.
4. **Write** the seven blocks from the template.
5. **Preflight** with the checklist below; fix every failed item.
6. **Package** the prompt, bindings, parameters, open items and QA plan for the
   caller.
7. **QA returned takes** with [QA checklist](references/qa-checklist.md): the
   all-frames bar and break-out scan from `scripts/measure_frame_break.py`, a 12 fps window
   contact sheet for every stage, and frame inspection.
8. **Repair** with [failure modes](references/failure-modes.md): change one
   thing at a time; re-rolling the same wording did not help.

## Reference loading

| File | Load when |
| --- | --- |
| [references/prompt-template.md](references/prompt-template.md) | Writing or revising any frame-break prompt |
| [references/scenes-and-subjects.md](references/scenes-and-subjects.md) | Choosing the backdrop or adapting to a subject type |
| [references/product-hero.md](references/product-hero.md) | The subject is a product, shown without a person |
| [references/failure-modes.md](references/failure-modes.md) | A take failed QA or a reviewer flagged the prompt |
| [references/qa-checklist.md](references/qa-checklist.md) | Reviewing takes or running the pixel script |

## Preflight checklist

- [ ] The three layers are stated back to front.
- [ ] The bars are flat, static 2D graphics drawn under the subject, about 12
      percent of the frame height, with no promise of exactness.
- [ ] The bars are fixed once early (perfectly straight horizontal inner edges,
      same height in every frame) and the layer-order block repeats the
      constant-height phrase and says whatever covers them never changes them.
- [ ] The subject is full-body and completely inside the window at the start and
      at every stage boundary, about two thirds of the window height, with no
      walking or leaning that puts torso or legs over a bar.
- [ ] Each break-out is a brief limb or hem extension inside one stage, after
      which the subject returns inside; nothing overlaps a bar between them.
- [ ] No extending limb or head fills a third of the frame, and the window is
      stated once to be the large majority of the frame height.
- [ ] No scene object resembles a bar (ropes, rails, beams) near the bar
      position.
- [ ] `@Image 1` is bound to face, clothing and style only, with the sheet
      layout excluded.
- [ ] There are four stages, each with one coherent action by one named limb
      and an observable End state; no stage chains two unconnected limb actions
      or names two different limbs crossing in the same beat.
- [ ] The upper bar has its own stage, a limb that can reach it, an explicit peak
      and an End state back inside.
- [ ] Every crossing has a numeric anchor, a crossing direction and a return.
- [ ] Left and right are given as screen-left and screen-right.
- [ ] Gaze, spin and sweep directions do not contradict each other.
- [ ] The camera is locked off with no zoom or cuts.
- [ ] No held props unless the subject is the product.
- [ ] The backdrop is calm, darker than the subject, with different colours and
      no lettering.
- [ ] The clip duration is absent from the prompt text.
- [ ] No on-screen text or logo is requested; any text is planned for post.
- [ ] The audio request states whether music is wanted.

## Usage limitations

- Timestamps allocate time; actions arrive about 0.25 to 0.5 s late and are not
  frame-accurate cut points.
- Bars are approximate in thickness and may differ top versus bottom. Never
  promise exact geometry. Bars that tilt, bow or jump are not a limitation to
  accept: moving bars are a hard-gate failure in QA, and a take that moves them
  is rejected, however well the subject crosses.
- A sudden scale jump or limb swap inside a stage is a hard-gate failure. It is
  found by reading a 12 fps contact sheet of each stage, not by sparse sampling.
- A prompt improves the odds of overlap; it does not guarantee it. Judge overlap
  from frames and the pixel script, and treat a video-understanding model as
  secondary evidence only.
- Photoreal subjects cross the bars less often than drawn ones.
- A take whose subject starts over a bar, or overlaps a bar for most of the
  clip, reads as standing outside the frame and fails the break-out gate even
  when the bars are perfectly static.
- Real logos on a product distort. Exact text and logos are post-production
  material, not footage.
- Do not bind a mock-up or storyboard of the effect as a reference; describe
  the layers in text.
- Contact sheets and frame scans cannot judge audio; listen to it.

## Evidence labels

Distinguish the kind of claim when it affects a decision: **observed result**
(six 1080p Seedance 2.5 runs, October 2026, conditions stated, not a guarantee),
**documented convention** (owned by `seedance-prompt-25`) and **optional
technique** (a hypothesis to test).

| Claim | Label |
| --- | --- |
| Describing bars as flat overlay graphics with numeric overlap anchors fixed takes where the subject sat behind the bars; re-rolling the same wording did not | observed result |
| Bars measured 9.4 to 18.9 percent of frame height when about 12 percent was asked, often unequal; about 7 percent once when treated as letterbox | observed result |
| Bars were static within 1 px in most takes; one take had a lower-bar bow up to about 4.6 percent and one a 0.25 to 0.5 s edge jump with the subject very close to the lens | observed result |
| A photoreal boxer take was rejected by the user although it passed an older soft gate: the lower bar's inner edge tilted (about row 680 at the left against 605 at the right at 5.5 s), bowed at about 6.5 s and jumped up as a whole for 0.25 to 0.5 s at about 6.75 s, when the subject leaned very close to the lens; sampling every 0.5 s and an 8 fps scan did not flag it clearly | observed result |
| Extreme foreshortening, a limb or head very close to the lens, is the observed cause of bar-edge distortion | observed result |
| A photoreal boxer take with static bars (17.5 and 21.1 percent measured) was rejected by the user because the subject was outside the window from the first frame: big, with legs, shorts and robe over the lower bar for most of the clip (overlap in about 80 percent of frames), so it read as standing outside the frame, not as a frame break; the earlier keep-it-at-arm's-length repair overcorrected | observed result |
| Takes the user accepted overlapped a bar in about 15 to 65 percent of frames and began inside the window | observed result |
| Ring ropes and rails near the bar zone were drawn as bars; the model painted a real-brand logo on background bags despite plain, unmarked wording | observed result |
| A stylised 3D fox take was rejected by the user: the fox reached out with a paw, then a giant bare cream sole appeared at about 1.25 to 2.0 s and filled half the frame, a scale jump and limb swap from two unconnected limb actions in one stage; the sole also differed from the sheet's teal sole | observed result |
| Drawn subjects gave 3 to 5 strong overlap moments; photoreal subjects gave 1 to 3 | observed result |
| Calm, darker, lower-contrast backdrops with colours that differ from the subject read well | observed result |
| Avoid the word letterbox in the prompt; keep other limbs small and tucked behind until their stage; make each break-out a brief event that ends back inside | optional technique |

## Submission boundary and failure behavior

The caller owns production authorization, the request hash, prompt review,
the task registry and submission. This leaf returns the package without
generating media. Missing identity references, unresolved rights for a real
brand asset or a request to bake text into the footage stay open items in the
package; the text route is post-production.

## Verification

```bash
uv run python .agents/skills/seedance-frame-break/scripts/measure_frame_break.py take.mp4 --summary-only --output take_measure.json
uv run python -m unittest tests.test_frame_break_measure -v
```
