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

## Source timing

Preserve the full measured source: fractional duration, frame count, fps,
decoded timestamps, cuts, playback speed, the final word and audio tails.
Derive the muted master and saved audio from the same full timeline unless a
specific derivative is approved; preserve the original picture and sound.

Missing or malformed timing measurements stop an execution-ready package.
Never guess duration, round a supplied value, or invent inspection evidence;
return an unresolved handoff requesting valid measurements.

A timing adaptation requires a specific current provider requirement for the
selected model, operation and transport, plus explicit derivative adaptation
approval from the user after explaining alternatives and timing/audio effects.
`approve_for_me` does not supply that approval. Empirical stability advice,
prior-run tolerances and creative selection do not establish a requirement.

Denied or missing adaptation approval leaves the original unchanged: no
derivative is prepared and no incompatible request is recommended for
submission. Offer unselected source-preserving alternatives or a handoff.

For an approved derivative, record source SHA-256, derivative SHA-256, the
exact window, command, timing delta and audio consequences. Keep source and
derivative measurements separate; muted picture and saved audio use the same
approved span. Never overwrite the original or extend the approved scope.

No automatic 8n+1 frame recipe or whole-second rounding is permitted. Do not
trim, pad or retime to satisfy a preferred length. Check current input limits;
a suggested split is not an approved split.

These timing rules govern referenced recipes: examples, repair suggestions
and old ladders do not authorize adaptations or extra probes. If a reference
conflicts, preserve the full measured timeline and the approval gates above.

An output mismatch remains unresolved after measuring picture, saved audio,
timestamps, cut boundaries and playback speed and inspecting opening/ending
sync. Never hide it with `-shortest`, padding or truncation. Retain the masters,
report lost frames, the final word or sound tails, and obtain the same
requirement evidence and specific approval before a corrective adaptation.

An optional partial probe is a needs-based proposal for a bounded uncertainty,
requiring explicit approval of its window and additional generation scope.
It is not delivery and never changes the full source target. Record its span
and hashes separately; a passing probe cannot replace the full-duration native
Draft or approve untested opening/ending content.

Every new Seedance 2.5 generation uses explicit `resolution: "480p"` and boolean
`draft: true` in every review mode, including an approved probe. Missing native
Draft controls stop the package until capability or transport conflicts are
resolved; never drop `draft` or substitute plain 480p. Review and select the
full-duration native Draft before supported promotion by `draft_task_id`.

## Hard rules

1. **Every visible source subject gets a disposition**: mapped to a reference,
   removed, or kept as a background extra. Never write "replace everyone" or
   any wording that leaves the model to guess who becomes whom.
2. **References come only from approved elements** (Seedream sheets or
   authorized downloads) with current SHA-256. Use separate images per view;
   never collages or turnaround strips.
3. **Every new character is a Virtual Portrait**, and the source footage
   carries a recorded rights decision, both per the
   [video-to-video inputs contract](../../contracts/video-to-video-inputs.md).
   A real, identifiable person as the target is out of scope, including when
   the job is called a test; offer a Virtual Portrait character. Brands and
   products follow [element identification](../../contracts/element-identification.md).
4. **Rejections are diagnosed, not routed around**, per the contract's
   [rejection rule](../../contracts/video-to-video-inputs.md#provider-rejections).
5. **Stay within recommended reference ranges**: 1–8 distinct subjects in R2V,
   1–5 reference images in edit mode, source under 20 s for edit. Above those,
   warn the user that stability drops and propose splitting into shots.
6. **No baked text.** Keep generated footage free of captions, taglines, CTAs,
   end cards and legible signage copy; add text in post.
7. **Submit the muted master** with `generate_audio: false`; sound returns in
   post through the recorded route in
   [audio and lip-sync](references/audio-and-lipsync.md).
8. **Native Draft first**: use the full measured source span with
   `resolution: "480p"` and boolean `draft: true` in every review mode.
   An extra key-beat probe is optional, needs-based and explicitly approved;
   it does not replace full-duration QA or authorize shortening delivery.
   Promote the selected draft with only `draft_task_id`, `resolution` and
   `watermark`. Resolve capability or transport conflicts before submission;
   never drop `draft` or substitute plain 480p.

## Mode selection

The default route rebuilds cast and world from a Virtual Portrait `asset://`
image while keeping the source's motion, timing and camera. It binds `@Video 1`
as an `asset://` video when the source shows a person, and runs with
`generate_audio: false`. Evaluate multi-subject, location-image and moving-camera
cases in the full-duration native Draft and record the result. Do not infer
route verification from another run or require an extra partial probe.

- **Default route: multimodal R2V.** Bind the source as
  `@Video 1` with role `reference_video`, stated as a motion-only reference (an `asset://` video when
  the source shows a person).
  Bind targets as `reference_image`. Set `omni_reference_task_type` to `auto`,
  `ratio` to the source ratio and `generate_audio` to `false`. Set `duration`
  to the full measured fractional source length only when the selected
  operation and transport accept it. Unsupported or unknown fractional
  duration support leaves an unresolved handoff, not a rounded request.
  Offer an unselected source-preserving edit route or a specifically approved
  derivative after checking current requirements; never silently switch routes.
  Measure returned picture and saved audio before muxing.
- **Fallback plan B: full-frame edit.** If the output keeps the source's
  people, clothing or location, switch to the edit task type the live tool
  accepts for Seedance 2.5 and write the edit variant in
  [recast grammar](references/recast-grammar.md#plan-b-full-frame-edit-variant).
  Its scope sentence is "replace all subjects and the environment", always
  followed by the per-subject mapping. Edit mode locks duration and aspect
  ratio to the source and prefers 1–5 reference images.
- An explicit `reference` task type is a needs-based alternative only when
  recorded capability evidence confirms it and the caller authorizes that
  additional test. Do not mandate a second test before plan B.

Resolve the live tool's accepted parameters and model ID before writing
parameters; do not assume a `seed` parameter exists. Extending a recast take
with `omni_reference_task_type: extend` is also a video input: a take that shows
people is rejected unless it is bound as an `asset://` video, so plan the full
length as one natural-duration recast or assemble separate shots.

## Procedure and reference loading

1. **Route check.** Confirm the request is a recast, not a region edit.
2. **Gates and intake.** Record footage rights, measure source timing, write
   the full-span muted master and save the source audio without tail loss.
   Any adaptation follows [Source timing](#source-timing).
   Register or reuse a Virtual Portrait for every new
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
   route without hiding timing mismatches, and run the lip-sync checks when
   someone speaks on screen. Inspect the full span, including final words,
   audio tails and cut boundaries, before selection or promotion.

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
- [ ] Full fractional source timing inspected: duration, fps, frame count,
      timestamps, ratio, audio, cuts, SHA-256, rights; final word and tails kept
- [ ] Any timing derivative has current requirement evidence, explicit user
      adaptation approval, separate span/hashes, timing delta and audio effects
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
- [ ] Source with a person bound as an `asset://` video; route evidence recorded
- [ ] Full-duration native Draft first; any extra partial probe is optional
      and explicitly approved, recorded separately and not delivery
- [ ] Mux timing measured; no automatic padding, truncation or `-shortest`
