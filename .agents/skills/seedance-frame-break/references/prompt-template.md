# Frame Break Prompt Template

Focused reference for `seedance-frame-break`. Read
[the entrypoint](../SKILL.md) for the technique and the preflight checklist.
The six-part formula, reference-role syntax, timestamp rules and audio brackets
belong to `seedance-prompt-25`; this file only fills them for the pop-out look.

- [Fill-in template](#fill-in-template)
- [Slot rules](#slot-rules)
- [Worked example](#worked-example)
- [Preflight check of the worked example](#preflight-check-of-the-worked-example)

## Fill-in template

```text
@Image 1 defines <subject>'s face, hair, clothing and <art style> only; ignore its panel layout, borders and background.

<Subject>, in <art style>, <one-sentence main idea: stands full-body inside the window and breaks out of the black bars toward the viewer with named limbs or hem>. Two fixed black bar graphics lie at the top and bottom of the frame, with perfectly straight horizontal inner edges at the same height in every frame.

0-<t1> seconds: Inside the central window of <calm backdrop>, <subject> stands full-body, about two thirds of the window height, clear of both bars, <establishing pose, arm cue; other limbs small and tucked behind>. End state: <subject is full-body inside the window with nothing over either bar>.

<t1>-<t2> seconds: <Subject> keeps their feet planted and <one coherent lower-bar break-out by one named limb or hem>. At the peak, their <screen-left/right limb or hem> passes over the lower bar's inner edge and covers about <a third> of the bar's width, then returns. End state: <subject stands full-body inside the window, nothing over a bar>.

<t2>-<t3> seconds: <Subject> keeps their feet planted and <one coherent upper-bar break-out by one named limb>. At the peak, their <screen-left/right limb> rises across the upper bar's inner edge and covers about <a third> of the bar's width, then lowers. End state: <subject stands full-body inside the window, nothing over a bar>.

<t3>-<t4> seconds: <Subject> <one coherent hero break-out: a single limb or hem>. At the peak, <what overlaps which bar and how much>, then it settles. End state: <final pose full-body inside the window, nothing over a bar>.

Frame and layer order, back to front: (1) <backdrop> fills only the central window between the bars, which is the large majority of the frame height; (2) two flat, solid black bars, each about 12 percent of the frame height, lie at the top and bottom as static 2D graphics laid over the picture, at the same height in every frame, never moving, tilting or bending; (3) <subject> is drawn complete, full-body inside the window, and on top of the bars only during the named break-outs, in full colour, never clipped or hidden by a bar. Whatever covers a bar sits on top and never changes it; when a limb withdraws, the straight edge is simply visible again. The bars are a graphic overlay, not part of the camera's picture.

Camera: locked-off wide-angle camera on a tripod, no movement, no zoom, no cuts; the subject stays in place and only the extending limb or hem grows toward the lens.

Audio: <requested sound arc using the seedance-prompt-25 brackets>. <No music, or the requested music.>

No on-screen text, captions, logos or watermarks; no held props; the bars stay plain black and unmarked.
```

## Slot rules

| Slot | Rule |
| --- | --- |
| Identity lock | Face, hair, clothing and style only. Name the ignored parts of the sheet. One face reference per subject; see `seedream-character-sheet`. |
| Main idea | One sentence. Say the subject stands inside the window and name the limbs or hem that break through; do not describe stages here. |
| Opening | Full-body, completely inside the window, about two thirds of the window height, bars fully visible and clear of the subject. Nothing overlaps a bar at the first frame. |
| Stage action | One primary state change by one named limb. Describe how it moves (direction, speed) in body-part terms. Name the limb that arrives at the lens and keep it the actor through the stage. Never name two different limbs crossing in the same beat; keep the others small and tucked behind until a later stage. Never chain an arm reach and a kick in one stage. |
| Break-out | A brief extension with a peak and a return. The feet stay planted; the subject never walks or leans closer so that torso or legs end up over a bar. |
| Crossing anchor | Give a number or fraction (about a third of the bar's width) and an edge-by-edge direction: which bar, over which edge, how far toward the frame edge. |
| End state | A frame you could pause on: the subject full-body inside the window and nothing over a bar. The peak is stated in the action sentence. |
| Left and right | Screen-left and screen-right, never the character's own left and right. |
| Gaze, spin, sweep | Pick one gaze rule per stage. A spin or sweep direction must match the direction stated elsewhere. |
| Bars, early sentence | Said once right after the main idea: fixed graphics, perfectly straight horizontal inner edges, same height in every frame. |
| Frame and layer order | Back to front, with the bars as flat static graphics under the subject, the constant-height phrase repeated, the rule that whatever covers them never changes them, and the window stated as the large majority of the frame height. Avoid the word letterbox. |
| Scale | Scale grows only for the extending limb or hem, and no limb or head should fill a third of the frame, because a near-lens limb distorted the bars. This protects the bars; it does not mean making the subject big. |
| Audio | State the sound arc and whether music is wanted. Verify by listening, since effects-only requests may still produce light music or a chime. |
| Closing exclusions | One or two lines. Necessary exclusions are allowed; positive direction comes first. |

Stage times are budgets scaled to the clip duration the caller selects (equal
quarters are a sound default). Do not state the total duration in the prompt.

## Worked example

An original stylised character with a scenic backdrop. The identity reference is
one approved character sheet bound as `@Image 1`.

```text
@Image 1 defines the lantern-keeper girl's face, silver bob hair, orange rain cape, cream scarf and 2D anime illustration style only; ignore its panel layout, borders and background.

The lantern-keeper girl, in a clean 2D anime style, stands full-body inside the picture and bursts out of the black bars toward the viewer with her boot, open palm and cape hem. Two fixed black bar graphics lie at the top and bottom of the frame, with perfectly straight horizontal inner edges at the same height in every frame.

0-3 seconds: Inside the central window of a calm indigo dusk harbour village with still water and distant lit windows, the girl stands full-body on a stone quay, about two thirds of the window height, clear of both bars, her arms hanging loosely at her sides, looking toward the viewer while the breeze stirs her cape hem and her other limbs stay small and close to her body. End state: she is upright and full-body inside the window with nothing over either bar.

3-6 seconds: She keeps her feet planted and swings her screen-right leg forward in one slow high step. At the peak, the boot toe passes over the lower bar's inner edge and covers about a third of the bar's width, reaching halfway to the bottom edge, then the boot returns to the quay. End state: she stands upright and full-body inside the window, nothing over a bar.

6-9 seconds: She raises her screen-left arm up and forward, fingers opening. At the peak, the open palm rises across the upper bar's inner edge and covers about a third of the bar's width, with every finger visible, then the arm lowers to her side. End state: she stands upright and full-body inside the window, nothing over a bar.

9-12 seconds: She sweeps her screen-right arm out to the side; the cape follows. At the peak, the cape's lower edge flares toward the lens across the right third of the lower bar, then settles. End state: she faces the viewer upright and full-body inside the window, cape settled, nothing over a bar.

Frame and layer order, back to front: (1) the harbour village fills only the central window between the bars, which is the large majority of the frame height; (2) two flat, solid black bars, each about 12 percent of the frame height, lie at the top and bottom as static 2D graphics laid over the picture, at the same height in every frame, never moving, tilting or bending; (3) the girl is drawn complete, full-body inside the window, and on top of the bars only during her boot, palm and cape break-outs, in full colour, never clipped or hidden by a bar. Whatever covers a bar sits on top and never changes it; when her boot, palm or cape withdraws, the straight edge is simply visible again. The bars are a graphic overlay, not part of the camera's picture. The village stays calmer and darker than the girl, with no signs or lettering.

Camera: locked-off wide-angle camera on a tripod, no movement, no zoom, no cuts; the girl stays in place and only the extending boot, palm and cape grow toward the lens.

Audio: soft harbour wind and gentle water ambience, with <boot taps on stone> and <a cape snapping in the breeze>. No music and no dialogue.

No on-screen text, captions, logos or watermarks; no held props; the bars stay plain black and unmarked.
```

Notes on the choices (optional technique unless labelled):

- The backdrop is indigo and muted; the subject is orange and cream, so the
  colours differ and the subject separates from the scene (observed result for
  differing, calmer backdrops).
- The upper bar has its own stage with an open-palm peak (observed repair).
- Each stage is one event with a peak and a return. She never walks toward the
  lens, so torso and legs never end up over a bar, and the opening and every
  stage boundary are fully inside the window.
- Stage 4 is a single sweep by one arm; the cape follows it, so no second limb
  takes over.
- The boot is the limb that arrives at the lens in stage 2 and the one that
  crosses; the palm acts only in stage 3.

## Preflight check of the worked example

| Preflight item | Result |
| --- | --- |
| Three layers back to front | Pass |
| Bars flat, static, under the subject, about 12 percent, no exactness promised | Pass |
| Bars fixed once early; constant-height phrase and never-changed rule repeated in the layer-order block | Pass |
| Full-body inside the window at the start and at every stage boundary, about two thirds of the window height, no walking or leaning | Pass |
| Each break-out is a brief extension in one stage with a return; nothing over a bar between them | Pass |
| No extending limb fills a third of the frame; window stated as the large majority of the frame height | Pass |
| No bar-like scene objects | Pass: still water, windows, quay; no ropes, rails or beams |
| `@Image 1` face, clothing and style only; layout excluded | Pass |
| Four stages, one named limb, End state each; no two unconnected limb actions per stage | Pass: boot, palm, then arm with cape; the other limbs stay close to her body |
| Upper bar has its own stage, limb, peak and End state | Pass: stage 3 |
| Numeric anchor, direction and return per crossing | Pass |
| Screen-left and screen-right | Pass |
| No gaze, spin or sweep contradiction | Pass: gaze appears once, in stage 1; no spin |
| Locked camera | Pass |
| No held props | Pass |
| Calm, darker, differently coloured backdrop, no lettering | Pass |
| Duration absent from prompt text | Pass: only stage ranges |
| No on-screen text requested | Pass |
| Music stated | Pass: no music |
