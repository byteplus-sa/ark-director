---
name: seedance-motion-recast
description: >-
  Write Seedance 2.5 Motion Transfer (recast) prompts that keep a source clip's
  body motion, pose sequence, screen positions, camera path, framing changes,
  cuts and timing while rebuilding cast, wardrobe, product, location and style
  from locked reference images. Covers the motion-only authority split, an
  explicit mapping or disposition for every visible source subject, bleed and
  extra-people guards, audio and lip-sync routes, named style presets, consent
  and real-likeness gates for real people in targets or source footage, and a
  480p key-beat probe ladder. Consumes a subject_map.json when available or
  inspects the source itself. Use to recast performers, localize a take for
  another market, restyle a clip, or rebuild its world around the same
  performance. Not for changing one region or object while preserving source
  pixels (use seedance-vfx-prompt), new T2V/I2V shots, or task submission; the
  caller owns the generation lifecycle.
---

# Seedance Motion Recast

Motion Transfer rebuilds everything a viewer sees and keeps only how it moves.
The source clip supplies body motion, pose sequence, screen positions, camera
path, framing changes, hard cuts and timing. Locked reference images supply the
new cast, wardrobe, products, location and style.

## Boundary with VFX editing

| Need | Skill | Source pixels |
| --- | --- | --- |
| Rebuild cast, world and look around the same performance | this skill | Discarded; only motion and timing survive |
| Change one region, object, background, weather or light | `seedance-vfx-prompt` | Preserved outside the edit scope |

If the user wants to keep the original people, faces or location and change
only one thing, route to VFX editing instead. If they want new people in a new
place doing exactly what the source people did, stay here.

## Input and output contract

Input:

- A source clip that the agent has inspected (duration, fps, aspect ratio,
  audio presence, cuts) with SHA-256 and recorded footage rights.
- Either a `subject_map.json` from a separate subject-mapping step, or the
  agent's own inspection of the source (see
  [multi-subject mapping](references/multi-subject-mapping.md)). Use a subject
  map only when its `status` is `ready`; open ambiguities block prompt writing.
- Approved target elements (character, product, prop, location sheets or
  authorized downloads) with hashes, one image per view.
- The requested style (a named preset or free text) and audio route.

Output: a recast prompt package containing the ordered `@Video`/`@Image`/`@Audio`
bindings with roles and hashes, the disposition table for every source subject,
the prompt text, the selected route and parameters, the reference-count check,
and the test-ladder rung it targets.

## Hard rules

1. **Every visible source subject gets a disposition**: mapped to a reference,
   removed, or kept as a background extra. Never write "replace everyone" or
   any wording that leaves the model to guess who becomes whom.
2. **References come only from approved elements** (Seedream sheets or
   authorized downloads) with current SHA-256. Use separate images per view;
   never collages or turnaround strips.
3. **Real people pass the consent and likeness gates.** A real, identifiable
   person as a target needs recorded consent and a recorded real-likeness
   generation approval. Source footage needs recorded rights, and identifiable
   real performers in it need recorded consent for reuse of their performance.
   Unknown facts stop the work; creative approval mode never supplies them, and
   calling the job a test does not either. Offer an invented cast or a
   consenting performer instead. See
   the [production policy](../../contracts/production-policy.md) and
   [element identification](../../contracts/element-identification.md).
4. **Privacy and moderation rejections are diagnosed, not routed around.** On a
   `PrivacyInformation` or other sensitive-content rejection, stop and report
   the request ID and flagged inputs. Never crop, blur, stylize, recompose or
   swap inputs to get a real likeness or real footage past the check. Offer an
   invented cast, generated or owned-talent source footage, or the provider's
   authorized route, and resubmit only on the user's explicit decision.
5. **Stay within recommended reference ranges**: 1–8 distinct subjects in R2V,
   1–5 reference images in edit mode, source under 20 s for edit. Above those,
   warn the user that stability drops and propose splitting into shots.
6. **No baked text.** Keep generated footage free of captions, taglines, CTAs,
   end cards and legible signage copy; add text in post.
7. **Test ladder**: a 480p probe of the key beat, then the full duration at
   480p, then the final resolution. Each rung is a separate reviewed request.

## Mode selection (provisional)

This route is unverified. No project has yet confirmed which Seedance 2.5 mode
rebuilds appearance from references while keeping motion from a video. Confirm
it with a low-cost 480p probe on synthetic or owned footage before any
production use, and record the result in the project before relying on it.

- **Default route (pending verification): multimodal R2V.** Bind the source as
  `@Video 1` with role `reference_video`, stated as a motion-only reference.
  Bind targets as `reference_image`. Set `omni_reference_task_type` to `auto`,
  `ratio` to the source ratio and `duration` to the source length (4–30 s).
- **Fallback plan B: full-frame edit.** If the probe output keeps the source's
  people, clothing or location, switch to the edit task type the live tool
  accepts for Seedance 2.5 and write the edit variant in
  [recast grammar](references/recast-grammar.md#plan-b-full-frame-edit-variant).
  Its scope sentence is "replace all subjects and the environment", always
  followed by the per-subject mapping. Edit mode locks duration and aspect
  ratio to the source and prefers 1–5 reference images.
- An explicit `reference` task type, if the live tool lists it, is a second
  probe before plan B. Change one variable per probe.

Resolve the live tool's accepted parameters and model ID before writing
parameters; do not assume a `seed` parameter exists.

## Procedure and reference loading

1. **Route check.** Confirm the request is a recast, not a region edit.
2. **Gates.** Establish footage rights and real-person consent for the source
   and every target before collecting references (rule 3).
3. **Source analysis.** Load the subject map, or inspect the source yourself.
   Build the disposition table and per-cut presence.
   Read [multi-subject mapping](references/multi-subject-mapping.md).
4. **Reference budget.** Count distinct subjects, views and total images; warn
   or split per rule 5.
5. **Prompt.** Assemble the template in
   [recast grammar](references/recast-grammar.md). Add guards from
   [guards and failures](references/guards-and-failures.md), a look from
   [style presets](references/style-presets.md), and the audio block from
   [audio and lip-sync](references/audio-and-lipsync.md).
6. **Package.** Return bindings, dispositions, prompt, route, parameters and
   ladder rung to the caller for prompt-review and submission.
7. **QA after generation.** Apply the QA checks in
   [guards and failures](references/guards-and-failures.md) and the lip-sync
   checks when dialogue is present.

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

- [ ] Request is a recast; region-only edits routed to `seedance-vfx-prompt`
- [ ] Source inspected: duration, fps, ratio, audio, cuts, SHA-256, rights
- [ ] Real-person consent and likeness approvals recorded, or invented cast used
- [ ] Subject map ambiguities resolved, or own inspection covers every cut
- [ ] Every visible source subject and swappable object has a disposition
- [ ] Each mapped subject has an observable descriptor (position, clothing, action)
- [ ] References approved, hashed, one image per view, ordered and role-bound
- [ ] Reference count within recommended range, or warning and split proposed
- [ ] Motion Authority names what `@Video 1` supplies and excludes its appearance
- [ ] Guards: exact people count, wardrobe only from references, residual originals
- [ ] Style block present; no overlay text, captions or legible signage requested
- [ ] Audio route stated, with lip-sync plan when dialogue is kept or re-voiced
- [ ] Route marked provisional until the verification probe passes
- [ ] Ladder rung stated: key-beat 480p probe, full-duration 480p, or final
