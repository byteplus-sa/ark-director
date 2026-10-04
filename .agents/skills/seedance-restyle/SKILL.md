---
name: seedance-restyle
description: >-
  Write Seedance 2.5 Restyle prompts that redraw an entire existing clip in a
  new visual style (2D cel anime, watercolor, claymation, needle felt, toy
  miniature, stylized 3D, pixel art, woodblock, film noir and 20+ more, or a
  custom style reference image) while keeping its performance, subject
  positions, motion, camera path, cuts and timing. Covers the style catalog, the
  style-only reference role, medium-matched Virtual Portrait identity anchors,
  an environment-image recipe that restyles the background while keeping the
  same place, edit and reference routes, a muted source master with audio added
  in post, a 480p test ladder, and restyle QA. Use to turn live
  action into animation, change the medium of an animated clip, or match a
  house style. Not for replacing the cast or world (seedance-motion-recast),
  swapping one element (seedance-object-swap), grading or relighting the
  original look (seedance-vfx-prompt), or task submission.
---

# Seedance Restyle

Restyle redraws every frame in a new medium. The same people do the same things
in the same place with the same camera; only the way the world is rendered
changes.

## Boundary

| Need | Skill | What survives from the source |
| --- | --- | --- |
| Same shot in a new visual medium | this skill | Content, layout, identity cues, motion, camera, cuts, timing |
| New cast or world doing the same performance | `seedance-motion-recast` | Motion, camera and timing only |
| One element replaced | `seedance-object-swap` | Every pixel outside the element |
| Grade, relight, weather or effects on the original look | `seedance-vfx-prompt` | The photographed medium |

When the style should also change who appears (for example, the restyled
figures should not depict the source people), map them to Virtual Portrait
characters: that is a Motion Transfer.

## Input and output contract

Input:

- A source clip inspected per the
  [video-to-video inputs contract](../../contracts/video-to-video-inputs.md),
  with a recorded rights decision covering the footage and the people in it.
- The muted master and the saved source audio.
- One style: a catalog ID from the [style catalog](references/style-catalog.md),
  or one to three custom style reference images (user-owned or approved
  generated frames, each hashed).
- Optional identity anchors: Virtual Portrait `asset://` views of recurring
  characters, designed in the target style.
- The post-audio route.

Output: a restyle package with ordered bindings, roles and hashes, the content
inventory, the style block, the prompt, the route and parameters, the
post-audio route, and the test-ladder rung.

## Hard rules

1. **The performance stays; the medium changes.** Keep the subject count, their
   screen positions, actions, props, the furniture they use and identity cues
   (hair shape, wardrobe colours, silhouettes). The background keeps its place
   and is restyled through an environment image of that place (rule 9). Read
   [restyle grammar](references/restyle-grammar.md).
2. **One style per take, applied to everything.** People, props, set, sky and
   effects share one medium lock. Blends happen only on request.
3. **A style reference supplies style only**: medium, palette, line, texture
   and light quality. Never its subjects, layout or characters.
4. **No studio, artist or franchise names**, and no frames from copyrighted
   productions as style references. Copyright IP enters only as an authorized
   Copyright Library asset.
5. **Identity anchors are Virtual Portraits** designed in the target medium.
   Liveness verification is not used. A photoreal sheet under a drawn style
   leaks photoreal skin.
6. **Submit the muted master** with `generate_audio: false` and no `@Audio`
   binding; sound returns in post.
7. **No baked text.** Source signage becomes abstract shapes in the style;
   captions and copy are added in post.
8. **Test ladder**: a 480p probe of the hardest beat (fast motion, a face close-up
   or a cut), then the full clip at 480p, then the final resolution.
9. **Keep the same place.** A restyle changes how the background looks, never
   where the scene is: a city street stays a city street, with the same kind of
   buildings, furniture and plants. Never name a different location unless the
   user asks for one. Build an environment image of the same place and bind it
   (see Environment image).
10. **Frame count.** Edit routes take an 8n+1 frame input (for example 121 at
    24 fps) and return the same count.

## Routes

- **Route A (default): full-frame edit with an environment image of the same
  place.** `omni_reference_task_type: edit`, `@Video 1` as editing master,
  ratio and duration locked to the source. Use an 8n+1 frame input (for example
  121 frames at 24 fps) so the output keeps the source frame count. Say "Replace
  the scene with the <style> <place> from @Image 1" and restyle the subject and
  props in the same sentence.
- **Route B (alternative): reference.** `auto`, or `reference` when recorded
  capability evidence confirms it, with `@Video 1` as the authority for motion,
  timing and camera, a detailed shot-by-shot description, and the same
  environment image. Set `ratio` to the source and `duration` to the
  whole-second source length. Use it when the duration must be exact or Route A
  keeps photoreal pixels.

Both routes bind `@Video 1` as an `asset://` video when the source shows a
person (see the
[video-to-video inputs contract](../../contracts/video-to-video-inputs.md)).
Bind the environment image, then style images and identity anchors, as
`reference_image` after `@Video 1`; 1–5 images for Route A; `watermark: false`.
Resolve the live tool schema and model ID before writing parameters.

### Environment image

Make one for every whole-frame restyle. It carries the background into the new
medium, so the street, buildings, furniture and plants take the style while the
scene stays in the same place.

1. Describe the source's own place in the target medium (the same city,
   building style, furniture, plants and light) and generate the empty set from
   text with Seedream: no people, no props the shot does not have.
2. Check that it reads as the same place as the source and holds no stray
   objects, then approve it.
3. Bind it with an Environment Reference Role that names what to use and what to
   ignore (extra chairs, objects, people).

The background's geometry follows the image, so the image is also where
the street layout is chosen. When the request allows no image input from the
user, generate this image from text yourself; when no image may be bound at all,
offer a subject-only restyle, or a different place described in words if the
user wants one.

Start a new case (another style, camera move, people count or resolution) with a
480p test of the hardest beat.

## Procedure

1. **Route check.** The request changes the look, not the cast or one element.
2. **Source intake.** Inspect, record rights, write the muted master and save the
   audio.
3. **Content inventory.** List subjects with observable descriptors, key
   props, set layout, cuts, fast-motion windows and on-screen text.
4. **Style.** Pick a catalog entry or write a custom recipe from the user's
   style images; confirm the cadence note for stop-motion styles.
   For a whole-frame restyle, also make the environment image of the same place
   (see Environment image).
5. **Anchors.** For recurring characters, register or reuse medium-matched
   Virtual Portraits.
6. **Prompt.** Assemble the route template in
   [restyle grammar](references/restyle-grammar.md).
7. **Package** for prompt-review and submission by the caller.
8. **QA and audio.** Run [restyle QA](references/restyle-qa.md), then mux the
   post-audio route.

Medium recipes in `seedance-animation-styles` and look presets in
`seedance-motion-recast` share vocabulary with this catalog; they are
composition hints, and this leaf does not load sibling skills.

## Submission boundary and failure behavior

The caller owns production authorization, request preflight, hash-bound prompt
review, the task registry and submission. This leaf never submits, polls or
deletes tasks. An unverified route, missing rights or an unapproved style
reference stays an open item. A provider rejection follows the rejection rule
in the
[video-to-video inputs contract](../../contracts/video-to-video-inputs.md#provider-rejections).

## Checklist

- [ ] Request changes the medium and keeps the place; cast or element changes
      routed elsewhere
- [ ] Source inspected and hashed; rights decision recorded
- [ ] Muted master bound as `@Video 1`; `generate_audio: false`; audio saved
- [ ] Content inventory covers every subject, key prop, cut and text surface
- [ ] Whole-frame restyle: environment image of the same place bound; no
      different location named; output compared with the source for the place
- [ ] Edit input trimmed to an 8n+1 frame count
- [ ] One style with a medium lock that names people, props, set and effects
- [ ] Style image role limited to medium, palette, line, texture and light
- [ ] No studio, artist or franchise names
- [ ] Identity anchors are medium-matched Virtual Portraits, when used
- [ ] Stop-motion cadence note present when the style steps motion
- [ ] Source text disposition stated; no new copy requested
- [ ] Route and ladder rung stated; a new case (other style, camera or people count) tested at 480p first
- [ ] Post-audio route recorded
