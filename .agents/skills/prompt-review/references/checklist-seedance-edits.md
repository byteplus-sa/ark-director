# Seedance Edits Checklist

Edit, object swap, recast and restyle checks for Seedance 2.5 video-to-video
work, plus the shared video-to-video input items. Apply the universal items in
[the index](review-checklists.md#universal--all-prompts) first.

## Seedance 2.5 edit (video-to-video)

Source skills: `seedance-prompt-25` (editing) + `seedance-vfx-prompt` (2.5 section).

Apply the universal items first, then this section. Mark N/A any item
whose feature is absent (no references → skip material mapping).

### Editing task

1. `[Edit Goal] Edit @Video 1 …` present and one-sentence; submit with
   `omni_reference_task_type="edit"` (2.5 values: `auto | reference | edit |
   extend` — `edit_video` is 2.0-only and is rejected).
2. `[Source Video Role]` declares `@Video 1` as the sole editing master and
   lists what it defines (subjects, scene, actions, camera, event order).
3. `[Target Material Role]` (or `[Target Reference Role]` in an object swap)
   present iff references are used: each `@Image N` mapped to one target, and
   the image's unowned content excluded ("Do not use its background/people").
   Exempt what the target class owns: a character reference owns its person, a
   location reference owns its background. Single-person sheets directed to
   use the close-up panel only.
4. `[Edit Scope]` states what changes and, for what must not change, a positive
   "exactly one <subject>, in open view at <position>" count.
5. `[Content to Preserve]` lists identity/motion/timing/camera/lighting to keep.

### Preservation locks (only where MUST PRESERVE says so)

6. Quantity: "Exactly one <subject>, in open view at <position>." Do not name
   extra copies (`prompt.exact_counts`).
7. Non-reaction (when the subject must not react): "…facial expression, gaze,
   and gestures remain exactly as in @Video 1; only <the changed thing>
   re-animates."
8. Grounding: "…naturally grounded — no cut-out edge, no halo; rim light
   matches the key direction."
9. Face protection (any preserved face): "real human skin with pores and
   catchlights — never waxy, smoothed, or warped."

### Audio / lip-sync

10. New dialogue in `{}` with language + regional variety + delivery style +
    speaker; lips directed to the NEW words. CJK punctuation: `……` not `——`.
11. Same-content contract (language swap): target `{}` line is the source line
    translated, no paraphrase/omission.
12. Diegetic audio only; SFX in `<>`, music in `()`; no non-diegetic score.

### Camera (only when the edit intentionally re-stages the camera)

13. One or two coherent camera moves when re-staging is intentionally requested;
    use semantic cues and add numeric timing only for requested or critical
    synchronization. Expand uncommon terms (orbit: direction + parallax).
    Apply the camera-direction item of the [Seedance 2.5 checklist](checklist-seedance-25.md#shot-plan-and-structure).
14. Camera-move items are N/A when the edit must preserve the source camera.

### Change contract

15. Flag only breakage of MUST PRESERVE or a quality defect in the change
    description — never an item the user explicitly asked to change.

### Object swap (only when one named element is replaced)

Source skill: `seedance-object-swap`. Object swaps submit a muted master
(V1 below), so audio items 10–12 are N/A; the silent `[Audio]` line is
correct.

16. **Residual original (`swap.residual_original`).** The original object is
    identified by observable descriptors (position, colour, material, who holds
    or wears it) and a positive guard states that it is fully replaced in every
    frame and only the target appears. A missing guard or a vague original
    ("the product") is a MAJOR finding.

17. **Count and Timeline Inheritance (`swap.timeline_inheritance`).** The prompt
    states the target count for the entire video (and per cut when it changes)
    and a `[Timeline Inheritance]` clause: the target inherits every
    appearance, motion, occlusion and exit of the original, including timing,
    duration, path and speed changes. Missing either is MAJOR.

18. **Contact and preservation.** Each grip, mouth contact, occlusion and
    set-down window is listed with its approximate time; hands, faces,
    accessories and mouth movement stay under `[Content to Preserve]`. Swapping
    several people or the whole cast belongs to the recast section below.

19. **Video-to-video inputs.** Apply the shared items under
    [Video-to-video inputs](#video-to-video-inputs-swap-recast-restyle).

---

## Seedance 2.5 recast (motion transfer)

Source skill: `seedance-motion-recast`.

Apply the universal items and the [Seedance 2.5 reference items](checklist-seedance-25.md#references)
first, then this section. A recast keeps the source clip's motion, camera path,
framing changes, cuts and timing, and rebuilds cast, wardrobe, product,
location and style from references. Mark N/A any item whose feature is absent
and record why.

### Motion authority

1. **Motion excludes appearance (`recast.motion_authority`).** The prompt limits
   `@Video 1` to motion, pose sequence, screen positions, camera path, framing,
   cuts and timing, and assigns faces, hair, wardrobe, products, location,
   palette and style to the references. A motion video with no appearance
   exclusion reproduces the source look; that is CRITICAL. The operation and
   task type match the recorded mode decision and capability evidence
   (`model.supported_mode`).

2. **Inherit, don't restate.** Only the inherited attributes are named; the
   prompt does not re-describe every source action, which conflicts with the
   motion video (Seedance 2.5 video reference inheritance).

### Subjects and mapping

3. **Every subject has a disposition (`recast.subject_disposition`).** Each
   visible source subject is listed exactly once as mapped (to a reference),
   removed, or background extra, and the list agrees with the source
   inspection or subject map per cut. An unlisted subject, or an unresolved
   ambiguity carried into the prompt, is CRITICAL.

4. **Unambiguous mapping (`recast.mapping_unambiguous`).** Each mapped subject
   is identified by observable descriptors (screen position, clothing, action)
   and bound to one `@Image N`, e.g. "the person on the left in the red jacket
   → @Image 2". Blanket wording ("replace everyone", "the people", "@Images 1–4
   are the cast") or one reference serving two subjects is CRITICAL. Several
   views of one subject state that the output contains only one of them
   (`references.ordered_bindings`).

### Guards

5. **Accessory bleed and extra people (`recast.guards`).** Each target wears
   only the wardrobe and accessories in its reference; source glasses,
   jewellery, hats and bags are named where they must not carry over. The
   person count per cut is stated, background extras are given as a count or
   density, and no additional people appear. Missing either guard is MAJOR.

6. **Audio route (`recast.audio_route`).** The prompt's audio block states a
   silent output with sound added in post, and the package records one
   post-audio route (original, new, mixed or re-voiced) with lip-sync QA when
   someone speaks on screen. An unstated route is MAJOR. Native audio appears
   only as a recorded, user-requested exception for the named take.

7. **No overlay text.** No captions, taglines, CTAs, end cards or readable brand
   copy are requested (`video.text_free`). Source on-screen text has a stated
   disposition (removed or replaced by a plain surface); overlay copy is added
   in post.

### Limits and rights

8. **Reference counts.** Within hard limits (≤ 30 images, ≤ 10 videos, ≤ 10
   audio) and the recommended range: 1–8 image subjects and one motion video.
   Exceeding a hard limit is CRITICAL. More than eight mapped subjects, or
   references above the recommended range, is MAJOR unless the
   prompt records the trade-off; suggest splitting into shots and assembling.

9. **Video-to-video inputs.** Apply the shared items under
   [Video-to-video inputs](#video-to-video-inputs-swap-recast-restyle).

### Video-to-video inputs (swap, recast, restyle)

Shared by the object swap items, the recast section and the restyle section.
Policy: [video-to-video inputs](../../../contracts/video-to-video-inputs.md).

V1. **Muted source (`v2v.muted_source`).** `@Video 1` is the recorded muted
    master with its hash, `generate_audio` is `false`, and no `@Audio` binding
    is present, unless the user explicitly requested native audio for this
    take and that exception is recorded. A source with audio bound as
    `@Video 1`, or a missing saved-audio record, is MAJOR. A source video that
    shows a person is bound as an `asset://` video; a raw upload of one is
    rejected by the provider, so flag it as MAJOR.

V2. **Virtual Portrait identities (`v2v.virtual_portrait_identity`).** Every
    person or character identity reference is a Virtual Portrait `asset://`
    binding registered from an approved invented design, with recorded asset
    IDs and source hash. A raw face or character image URL is MAJOR. A real,
    identifiable person as a target is CRITICAL and blocks the request.

V3. **Source rights.** A recorded user rights decision covers the footage and
    the people in it. A missing record is CRITICAL. Do not suggest wording that
    routes around a provider rejection.

---

## Seedance 2.5 restyle

Source skill: `seedance-restyle`.

Apply the universal items, the [Seedance 2.5 reference items](checklist-seedance-25.md#references) and,
for the edit route, Seedance 2.5 edit items 1, 2, 4 and 5. Edit item 3 is
replaced by restyle item 3 (`[Style Reference Role]`, `[Identity Anchors]`);
edit item 9 is N/A because the photoreal face line contradicts drawn and
crafted styles (use it only for a capture look); edit items 10–12 are N/A
because the output is silent (V1). A restyle keeps the source's subjects,
layout, actions, camera, cuts and timing and changes only the rendering
medium. Mark N/A any item whose feature is absent and record why.

1. **Content preserved (`restyle.content_preserved`).** The prompt pins the
   subject count, observable subject descriptors with identity cues, key props
   and set layout from the content inventory, and keeps poses, camera, cuts and
   timing with `@Video 1`. Introducing, removing or replacing a subject is
   CRITICAL; that request belongs to Object Swap or Motion Transfer.

2. **Medium lock.** One style applies to people, props, set, sky and effects,
   and nothing is left photographic unless the style is a capture look. A
   partial or conflicting style block is MAJOR.

3. **Style-only reference (`restyle.style_reference_only`).** Each style image
   supplies only medium, palette, line, texture and light quality and excludes
   its subjects, layout and characters. A style image without that exclusion
   is MAJOR. Studio, artist or franchise names, or frames from copyrighted
   productions, are CRITICAL.

4. **Identity anchors.** Anchors, when used, are Virtual Portraits designed in
   the target medium and mapped to a source subject by observable descriptor.
   A photoreal anchor under a drawn or crafted style is MAJOR.

5. **Cadence and text.** Stepped styles state that beat poses still land.
   Source text surfaces become abstract shapes; no lettering is requested.

6. **Route and limits.** The operation matches the recorded route decision and
   capability evidence (`model.supported_mode`); an unverified route is
   labeled provisional and the request is a 480p probe. Route A uses 1–5
   images; Route B sets the whole-second source duration and ratio.

7. **Same place.** A restyle keeps the source's place: the background is
   restyled through an environment image of that place, or left as it is.
   Naming a different location (a city street becoming a seaside village) is
   MAJOR unless the user asked for one. A scene replacement or style word that
   only tells the model to keep the source layout for the background is likely
   to leave it photographic; flag it MAJOR when a whole-frame restyle is
   requested. Keeping positions for the subject and the furniture they use is
   correct. A restyle that intentionally keeps the original background
   photographic is N/A.

8. **Video-to-video inputs.** Apply the shared items under
   [Video-to-video inputs](#video-to-video-inputs-swap-recast-restyle).
