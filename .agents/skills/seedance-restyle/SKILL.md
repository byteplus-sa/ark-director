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
   and geometry while taking the requested medium. Read
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
6. **Submit the muted master** with `generate_audio: false`, per the
   [video-to-video inputs contract](../../contracts/video-to-video-inputs.md#muted-source-master);
   sound returns in post.
7. **No baked text.** Source signage becomes abstract shapes in the style;
   captions and copy are added in post.
8. **Test ladder**: follow the workspace draft policy with currently supported
   parameters. Propose a short probe only for a difficulty identified in the
   current source or result, with user approval for its selected span. Use
   `resolution: "480p"` and boolean `draft: true` for every new test in every
   review mode, then promote the selected native Draft. Resolve capability or
   transport conflicts before submission; never drop `draft` or substitute
   plain 480p. Prior runs do not gate a new case.
9. **Keep the same place.** A restyle changes how the background looks, never
   where the scene is: a city street stays a city street, with the same kind of
   buildings, furniture and plants. Never name a different location unless the
   user asks for one. Select an environment image only when the current brief,
   input or observed failure warrants it (see Environment image).

## Routes

- **Route A (when supported): edit.** Use `omni_reference_task_type: edit`
  with `@Video 1` as editing master. Preserve source content, ratio and timing;
  describe subjects, props and background surfaces in the requested medium.
  A words-only style block is valid; an environment image is not required.
- **Route B (when supported): reference.** Use the currently accepted task type
  with `@Video 1` authoritative for content, motion, timing and camera.
  Select this alternative from the current brief or reviewed failure, not a
  prior probe. Neither route guarantees exact duration or medium coverage.

Preserve the original source and full timeline. Verify current route constraints
before setting duration or preparing media. Any trim, padding, rounding or
retiming needs current capability evidence and user approval for that specific
change. Record approved derivatives, source spans, hashes and audio consequences;
derive muted picture and saved audio from the same span. Measure returned timing
rather than relying on a frame-count recipe.

Both routes bind `@Video 1` as an `asset://` video when the source shows a
person (see the
[video-to-video inputs contract](../../contracts/video-to-video-inputs.md)).
Bind only selected environment images, style images and identity anchors in
supported roles after `@Video 1`; omit absent roles and number actual bindings.
Resolve the live tool schema, reference budget, model ID and supported
parameters before writing the package.

### Environment image

An environment image is optional guidance for the same place's surfaces, palette
and texture. Use one supplied or requested by the user, or propose one for a
specific need found in the current input or reviewed failure.

1. Name the background surfaces needing medium guidance in the prompt.
2. When warranted, propose an authorized same-place plate or generated reference
   through the caller. A missing upload does not authorize image generation.
3. Inspect and approve the selected image, record its hash, and exclude its
   people and extra props in the Environment Reference Role.
4. Keep source geometry, layout, camera parallax and timing authoritative.
   Reject conflicting references rather than accepting an unintended new place.

**Honor words-only requests.** Include the background in the requested restyle
without inventing an image binding or reducing the task to subject-only. If a
current draft leaves surfaces photographic, report those surfaces and offer a
scoped wording or supported-route repair. An image remains optional. Do not use
one medium's prior test as proof of another medium's limitations or as a gate.

## Procedure

1. **Route check.** The request changes the look, not the cast or one element.
2. **Source intake.** Inspect, record rights, write the muted master and save the
   audio.
3. **Content inventory.** List subjects with observable descriptors, key
   props, set layout, cuts, fast-motion windows and on-screen text.
4. **Style.** Pick a catalog entry or write a custom recipe from the user's
   style images; confirm the cadence note for stop-motion styles.
   Include an environment image only when selected for the current case
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
- [ ] Background takes the medium; any environment image is justified and
      approved, with source place and geometry preserved
- [ ] Original timeline preserved; adaptations have current evidence, user
      approval and separate derivative records
- [ ] One style with a medium lock that names people, props, set and effects
- [ ] Style image role limited to medium, palette, line, texture and light
- [ ] No studio, artist or franchise names
- [ ] Identity anchors are medium-matched Virtual Portraits, when used
- [ ] Stop-motion cadence note present when the style steps motion
- [ ] Source text disposition stated; no new copy requested
- [ ] Verified route and ladder rung stated; any probe addresses a current need
- [ ] Post-audio route recorded
