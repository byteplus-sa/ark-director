---
name: seedance-restyle
description: >-
  Write Seedance 2.5 Restyle prompts that redraw an entire existing clip in a
  new visual style (2D cel anime, watercolor, claymation, needle felt, toy
  miniature, stylized 3D, pixel art, woodblock, film noir and 20+ more, or a
  custom style reference image) while keeping its content, composition,
  motion, camera path, cuts and timing. Covers the style catalog, the
  style-only reference role, medium-matched Virtual Portrait identity anchors,
  a location-change recipe that restyles the background as well as the
  subject, edit and reference routes, a muted source master with audio added
  in post, a 480p probe ladder, and restyle QA. Use to turn live
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

1. **Content stays; only the medium changes.** Keep the subject count, screen
   positions, actions, props, set layout and identity cues (hair shape,
   wardrobe colours, silhouettes). Read
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

## Routes

Probed on 2026-10-03 and 2026-10-04 (480p, 5 s, claymation, one person at a
café table, locked camera, source bound as an `asset://` video). What changed
the background and what did not:

- **Layout-keeping words, no images: the street stayed photographic.** Five
  runs on both routes, including every surface named, a very aggressive all-clay
  prompt, and "Replace the scene with a plasticine café terrace ... in the same
  positions as the source" (edit) or "same layout as @Video 1" (reference). Only
  the person (and, on the reference route, the near table, bench and shrub)
  changed.
- **A prompt that states the location changes: whole frame in clay, on both
  routes.** The prompt says the background and the whole location change, names
  what is removed ("the Paris street, its buildings, the plant, the bench and
  the sky are removed; nothing of the original street remains"), and describes a
  different clay place in words, with no instruction to keep the source layout.
  Edit and reference routes both rebuilt everything (cottages, harbour, boats,
  water, sky) while the woman, table, can, cup, motion, timing and camera held.
  The new place is not the source's place.
- **An environment image** ("Replace the scene with ... Refer to @Image 1 for the
  environment" on the edit route, or the same image on the reference route) also
  gave a whole-frame clay result, with geometry following the image. A stray
  object in the image can leak into the video.
- **Style frames made by restyling photos** (three Seedream clay frames of the
  source): the background stayed photographic, because the frames were
  themselves only partly restyled, and the woman's hair colour leaked.

Untested: rebuilding the source's own location (the same street) as clay with
words only. Layout-keeping language is the suspected reason the model preserved
the source plate; test it before promising the same place.

- **Route A (default): full-frame edit with a location-change block.**
  `omni_reference_task_type: edit`, `@Video 1` as editing master, ratio and
  duration locked to the source. Use an 8n+1 frame input (for example 121
  frames at 24 fps): it returned exactly 121 frames, while a 120-frame input
  returned 113 (4.71 s vs 5.00 s, inside the 0.3 s tolerance). Without a
  location-change statement this route changes only the subject.
- **Route B (alternative): reference.** `auto`, or `reference` when recorded
  capability evidence confirms it, with `@Video 1` as the authority for
  motion, timing and camera, a detailed shot-by-shot description, and the same
  location-change statement. Set `ratio` to the source and `duration` to the
  whole-second source length. Use it when Route A keeps photoreal pixels or the
  duration must be exact.

Both routes bind `@Video 1` as an `asset://` video when the source shows a
person (see the
[video-to-video inputs contract](../../contracts/video-to-video-inputs.md)).
With images, bind the environment image, then style images and identity
anchors, as `reference_image` after `@Video 1`; 1–5 images for Route A;
`watermark: false`. Resolve the live tool schema and model ID before writing
parameters.

### Environment image (optional)

Use one when the exact look or layout of the new place matters. Generate the
empty set in the target medium with Seedream (no people, no props the shot does
not have), approve it, and bind it with an Environment Reference Role that names
what to use and what to ignore (extra chairs, objects, people). Check the image
for stray objects before use; each one can leak into the video.

## Procedure

1. **Route check.** The request changes the look, not the cast or one element.
2. **Source intake.** Inspect, record rights, write the muted master and save the
   audio.
3. **Content inventory.** List subjects with observable descriptors, key
   props, set layout, cuts, fast-motion windows and on-screen text.
4. **Style.** Pick a catalog entry or write a custom recipe from the user's
   style images; confirm the cadence note for stop-motion styles.
   For a whole-frame restyle, write the Location Change block (see the grammar
   reference): state that the background and the whole location change, and do
   not tell the model to keep the source layout.
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

- [ ] Request changes the medium only; cast or element changes routed elsewhere
- [ ] Source inspected and hashed; rights decision recorded
- [ ] Muted master bound as `@Video 1`; `generate_audio: false`; audio saved
- [ ] Content inventory covers every subject, key prop, cut and text surface
- [ ] One style with a medium lock that names people, props, set and effects
- [ ] Style image role limited to medium, palette, line, texture and light
- [ ] No studio, artist or franchise names
- [ ] Identity anchors are medium-matched Virtual Portraits, when used
- [ ] Stop-motion cadence note present when the style steps motion
- [ ] Source text disposition stated; no new copy requested
- [ ] Route marked provisional until a probe passes; ladder rung stated
- [ ] Post-audio route recorded
