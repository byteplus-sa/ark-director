---
name: seedance-object-swap
description: >-
  Write Seedance 2.5 Object Swap prompts that replace one named element in
  existing footage (a character, outfit, product, prop or object, or the
  location behind the subjects) and preserve everything else as filmed:
  performance, camera path, cuts, lighting and event order. Covers the
  five-part swap contract (identification, object count, Timeline Inheritance,
  residual-original guard, preservation), contact and occlusion windows,
  Virtual Portrait asset:// references for character swaps, a muted source
  master with audio added in post, and swap QA. Use for product placement,
  competitor-to-own SKU swaps, wardrobe changes, single-character replacement
  or location swaps on a kept take. Not for rebuilding the whole cast or world
  around the source motion (seedance-motion-recast), whole-frame style changes
  (seedance-restyle), new T2V/I2V shots, or task submission.
---

# Seedance Object Swap

Object Swap changes **one named element** in existing footage and keeps the
rest of the shot as filmed. `@Video 1` is the sole editing master; one or more
reference images define only the target's appearance.

## Boundary

| Need | Skill | What survives from the source |
| --- | --- | --- |
| Replace one character, outfit, product, prop, object or the location | this skill | Every pixel outside the swapped element |
| New cast and world doing the same performance | `seedance-motion-recast` | Motion, camera and timing only |
| Same shot redrawn in a new visual medium | `seedance-restyle` | Content, layout, motion and camera; the look changes |
| Added creature, effect, weather, relight, or a background rebuild that relights the subjects | `seedance-vfx-prompt` | Everything except the edit |

Swap one element class per request. Two unrelated changes run as two sequential
swaps with inspection between them. When most of the frame changes, the job is
a Motion Transfer.

## Swap classes

| Class | Target reference | Typical scope |
| --- | --- | --- |
| Character | Virtual Portrait `asset://` views | One person replaced; others kept |
| Outfit | Garment packshot, flat-lay or mannequin view | One garment on one person |
| Product | Official or authorized packshot | One product, including grip and labels |
| Prop or object | Prop sheet view | One object, including its path and contacts |
| Location | Location sheet or plate | Environment behind kept subjects |

## Input and output contract

Input:

- A source clip inspected per the
  [video-to-video inputs contract](../../contracts/video-to-video-inputs.md):
  duration, frame rate, ratio, audio streams, cuts, SHA-256 and a recorded
  rights decision.
- The muted master and the saved source audio from the same contract.
- One approved target element with hashes. A character target is a Virtual
  Portrait asset; a real brand or labeled product uses the official or
  authorized asset per
  [element identification](../../contracts/element-identification.md).
- An optional `subject_map.json` with `status: ready`.
- The post-audio route (original, new, mixed or re-voiced).

Output: a swap prompt package with ordered `@Video 1`/`@Image N` bindings,
roles and hashes, the five-part contract facts, contact windows, the prompt,
parameters, the post-audio route, and the test-ladder rung.

## Hard rules

1. **State the five-part contract**: identification, object count, Timeline
   Inheritance, residual-original guard and preservation. Read
   [swap contract](references/swap-contract.md).
2. **Character targets are Virtual Portraits.** Bind character identities only
   as `asset://` Virtual Portrait assets registered from approved invented
   designs. Liveness verification is not used. A real, identifiable person as
   the target is out of scope; offer a Virtual Portrait character.
3. **Submit the muted master.** `@Video 1` is the muted master;
   `generate_audio` is `false`; there are no `@Audio` bindings. Sound returns in
   post through the recorded route.
4. **Reference budget**: 1–5 target images, one view per image, no collage.
   Several views of one target state that the output contains only one.
5. **No baked text.** A label printed on a product is part of the product;
   captions, taglines, CTAs and end cards are added in post.
6. **Test ladder**: a 480p probe of the hardest contact window, then the full
   clip at 480p, then the final resolution. Each rung is a separate reviewed
   request.

## Route and parameters

Seedance 2.5 edit, through `seedance_2_5_create_task`:

- `videos`: the muted master as `@Video 1`, first in order.
- `images`: target views as `reference_image`, in binding order.
- `omni_reference_task_type`: `edit`. Field notes record that 2.5 rejects
  `edit_video`; confirm the accepted value from current capability evidence
  before the first request.
- Omit `ratio` and `duration`; both lock to the source (about ±0.3 s).
- `generate_audio: false`, `watermark: false`, `resolution` per ladder rung.

Resolve the live tool schema and model ID before writing parameters.

## Procedure

1. **Route check.** One element class changes; everything else is kept.
2. **Source intake.** Inspect, record rights, write the muted master and save the
   audio ([video-to-video inputs](../../contracts/video-to-video-inputs.md)).
3. **Facts.** Copy descriptors, counts and contact windows from the subject map,
   or inspect the source and record them. Uncertain facts stay open questions.
4. **Target.** Confirm the approved element and hash. For a character, register
   or reuse the Virtual Portrait and record its asset IDs.
5. **Prompt.** Fill the class template in
   [swap templates](references/swap-templates.md).
6. **Package.** Return bindings, facts, prompt, parameters, audio route and rung
   to the caller for prompt-review and submission.
7. **QA and audio.** Run [swap QA](references/swap-qa.md) on the silent output,
   then mux the post-audio route and check sync.

The canonical 2.5 edit blocks and face-protection lines come from
`seedance-prompt-25` and `seedance-vfx-prompt`; a source subject map comes from
`source-subject-map`. These are composition hints; this leaf does not load
sibling skills.

## Submission boundary and failure behavior

The caller owns production authorization, request preflight, hash-bound prompt
review, the task registry and submission. This leaf never submits, polls or
deletes tasks. Missing rights, unregistered character assets or open
contact-window questions remain open items in the package.

A provider rejection follows the rejection rule in the
[video-to-video inputs contract](../../contracts/video-to-video-inputs.md#provider-rejections).
When a take fails QA, record the locked decisions, the one requested delta and
the observed failure, then change only one of wording, reference or route per
retry.

## Checklist

- [ ] One element class changes; recast and restyle requests routed elsewhere
- [ ] Source inspected and hashed; rights decision recorded
- [ ] Muted master bound as `@Video 1`; source audio saved; `generate_audio: false`
- [ ] Original identified by observable descriptors and first appearance
- [ ] Object count stated for the whole video and per cut when it changes
- [ ] Timeline Inheritance clause present
- [ ] Residual-original guard phrased positively
- [ ] Contact and occlusion windows listed with approximate times
- [ ] Preservation list names faces, accessories, hands, camera and lighting
- [ ] Character target bound as a Virtual Portrait `asset://` reference
- [ ] Target reference states what to ignore in the image
- [ ] 1–5 target images, one view each
- [ ] Post-audio route recorded
- [ ] Ladder rung stated
