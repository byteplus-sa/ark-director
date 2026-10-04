---
name: seedance-motion-recast
description: >-
  Write Seedance 2.5 Motion Transfer (recast) prompts that keep a source clip's
  body motion, pose sequence, screen positions, camera path, framing changes,
  cuts and timing while rebuilding cast, wardrobe, product, location and style
  from locked reference images. Covers the motion-only authority split, an
  explicit mapping or disposition for every visible source subject, bleed and
  extra-people guards, Virtual Portrait asset:// identity references, a muted
  source master with audio added in post, named look presets, and a 480p
  key-beat probe ladder. Consumes a subject_map.json when available or
  inspects the source itself. Use to recast performers, localize a take for
  another market, or rebuild its world around the same performance. Not for
  replacing one element while preserving source pixels (seedance-object-swap),
  redrawing the same cast in a new medium (seedance-restyle), other edits
  (seedance-vfx-prompt), new T2V/I2V shots, or task submission; the caller
  owns the generation lifecycle.
---

# Seedance Motion Recast

Motion Transfer rebuilds everything a viewer sees and keeps only how it moves.
The source clip supplies body motion, pose sequence, screen positions, camera
path, framing changes, hard cuts and timing. Locked reference images supply the
new cast, wardrobe, products, location and style.

## Boundary

| Need | Skill | Source pixels |
| --- | --- | --- |
| Rebuild cast, world and look around the same performance | this skill | Discarded; only motion and timing survive |
| Replace one character, outfit, product, prop or location | `seedance-object-swap` | Preserved outside the swapped element |
| Redraw the same cast and place in a new medium | `seedance-restyle` | Content kept; rendering replaced |
| Add effects, weather or relight | `seedance-vfx-prompt` | Preserved outside the edit scope |

If the user wants to keep the original people, faces or location and change
only one thing, route to Object Swap. If they want the same people in a new
medium, route to Restyle. If they want new people in a new place doing exactly
what the source people did, stay here.

## Input and output contract

Input:

- A source clip inspected per the
  [video-to-video inputs contract](../../contracts/video-to-video-inputs.md)
  (duration, fps, aspect ratio, audio presence, cuts, SHA-256, recorded
  rights), its muted master and the saved source audio.
- Either a `subject_map.json` from a separate subject-mapping step, or the
  agent's own inspection of the source (see
  [multi-subject mapping](references/multi-subject-mapping.md)). Use a subject
  map only when its `status` is `ready`; open ambiguities block prompt writing.
- Approved target elements with hashes, one image per view. Characters are
  Virtual Portrait `asset://` assets; products, props and locations are
  approved sheets or authorized downloads.
- The requested style (a named preset or free text) and post-audio route.

Output: a recast prompt package containing the ordered `@Video`/`@Image`
bindings with roles and hashes, the disposition table for every source subject,
the prompt text, the selected route and parameters, the reference-count check,
the post-audio route and the test-ladder rung it targets.

## Hard rules

1. **Every visible source subject gets a disposition**: mapped to a reference,
   removed, or kept as a background extra. Never write "replace everyone" or
   any wording that leaves the model to guess who becomes whom.
2. **References come only from approved elements** (Seedream sheets or
   authorized downloads) with current SHA-256. Use separate images per view;
   never collages or turnaround strips.
3. **Every new character is a Virtual Portrait.** Register approved invented
   designs as Virtual Portrait assets and bind them as `asset://`; liveness
   verification is not used. A real, identifiable person as the target is out
   of scope, including when the job is called a test; offer a Virtual Portrait
   character. Source footage needs a recorded rights decision covering the
   footage and the people in it; unknown rights stop the work. See the
   [video-to-video inputs contract](../../contracts/video-to-video-inputs.md)
   and [element identification](../../contracts/element-identification.md).
4. **Privacy and moderation rejections are diagnosed, not routed around.**
   Follow the
   [rejection rule](../../contracts/video-to-video-inputs.md#provider-rejections):
   report the request ID and flagged inputs, never crop, blur, stylize,
   recompose or swap inputs to get a real likeness or real footage past the
   check, and resubmit only on the user's explicit decision.
5. **Stay within recommended reference ranges**: 1–8 distinct subjects in R2V,
   1–5 reference images in edit mode, source under 20 s for edit. Above those,
   warn the user that stability drops and propose splitting into shots.
6. **No baked text.** Keep generated footage free of captions, taglines, CTAs,
   end cards and legible signage copy; add text in post.
7. **Submit the muted master.** `@Video 1` is the muted master,
   `generate_audio` is `false`, and there are no `@Audio` bindings. Sound
   returns in post through the recorded route in
   [audio and lip-sync](references/audio-and-lipsync.md).
8. **Test ladder**: a 480p probe of the key beat, then the full duration at
   480p, then the final resolution. Each rung is a separate reviewed request.

## Mode selection

The default route rebuilds cast and world from a Virtual Portrait `asset://`
image while keeping the source's motion, timing and camera. It binds `@Video 1`
as an `asset://` video when the source shows a person, and runs with
`generate_audio: false`. Test multi-subject, location-image and moving-camera
cases at 480p first and record each result in the project.

- **Default route: multimodal R2V.** Bind the source as
  `@Video 1` with role `reference_video`, stated as a motion-only reference (an `asset://` video when
  the source shows a person).
  Bind targets as `reference_image`. Set `omni_reference_task_type` to `auto`,
  `ratio` to the source ratio, `duration` to the whole-second source length
  (4–30 s; trim the source to whole seconds first) and `generate_audio` to
  `false`. A 5 s request returned 121 frames at 24 fps (5.04 s); trim or pad to
  the picture when muxing.
- **Fallback plan B: full-frame edit.** If the output keeps the source's
  people, clothing or location, switch to the edit task type the live tool
  accepts for Seedance 2.5 and write the edit variant in
  [recast grammar](references/recast-grammar.md#plan-b-full-frame-edit-variant).
  Its scope sentence is "replace all subjects and the environment", always
  followed by the per-subject mapping. Edit mode locks duration and aspect
  ratio to the source and prefers 1–5 reference images.
- An explicit `reference` task type, when recorded capability evidence
  confirms it, is the second test before plan B. Change one variable per test.

Resolve the live tool's accepted parameters and model ID before writing
parameters; do not assume a `seed` parameter exists.

## Procedure and reference loading

1. **Route check.** Confirm the request is a recast, not a region edit.
2. **Gates and intake.** Record footage rights, write the muted master and
   save the source audio. Register or reuse a Virtual Portrait for every new
   character (rule 3).
3. **Source analysis.** Load the subject map, or inspect the source yourself.
   Build the disposition table and per-cut presence.
   Read [multi-subject mapping](references/multi-subject-mapping.md).
4. **Reference budget.** Count distinct subjects, views and total images; warn
   or split per rule 5.
5. **Prompt.** Assemble the template in
   [recast grammar](references/recast-grammar.md). Add guards from
   [guards and failures](references/guards-and-failures.md), a look from
   [style presets](references/style-presets.md), and the silent audio line and
   post route from [audio and lip-sync](references/audio-and-lipsync.md).
6. **Package.** Return bindings, dispositions, prompt, route, parameters and
   ladder rung to the caller for prompt-review and submission.
7. **QA after generation.** Apply the QA checks in
   [guards and failures](references/guards-and-failures.md), mux the post-audio
   route, and run the lip-sync checks when someone speaks on screen.

Load only the references the request needs. A stylized medium such as
claymation or toy miniature may also use the `seedance-animation-styles`
recipes by name; the six-part formula and reference syntax stay with
`seedance-prompt-25`. A shared subject map comes from `source-subject-map`.
These are composition hints; this leaf does not load sibling skills.

## Submission boundary and failure behavior

The caller owns production authorization, the exact request preflight, the
hash-bound prompt review, the task registry and submission. This leaf returns a
prompt package and never submits, polls or deletes tasks. Missing gates,
unapproved references, unresolved subject-map ambiguities or an unconfirmed
route remain open items in the package; a draft or technical success does not
establish approval. A provider rejection is evidence to diagnose (rule 4).

When the output fails QA, record the locked decisions, the one requested delta
and the observed failure, then change only one of prompt wording, reference
bundle or route per retry.

## Checklist

- [ ] Request is a recast; single-element swaps and same-cast restyles routed
      to `seedance-object-swap` and `seedance-restyle`
- [ ] Source inspected: duration, fps, ratio, audio, cuts, SHA-256, rights
- [ ] Muted master bound as `@Video 1`; source audio saved; `generate_audio: false`
- [ ] Every new character bound as a Virtual Portrait `asset://` reference
- [ ] Subject map ambiguities resolved, or own inspection covers every cut
- [ ] Every visible source subject and swappable object has a disposition
- [ ] Each mapped subject has an observable descriptor (position, clothing, action)
- [ ] References approved, hashed, one image per view, ordered and role-bound
- [ ] Reference count within recommended range, or warning and split proposed
- [ ] Motion Authority names what `@Video 1` supplies and excludes its appearance
- [ ] Guards: exact people count, wardrobe only from references, residual originals
- [ ] Style block present; no overlay text, captions or legible signage requested
- [ ] Post-audio route recorded, with lip-sync QA when someone speaks on screen
- [ ] Source with a person bound as an `asset://` video; route probes recorded for any new case
- [ ] Ladder rung stated: key-beat 480p probe, full-duration 480p, or final
