# Seedance Legacy Checklist

Seedance 2.0 generation (4K, Fast, Mini) and the legacy video-to-video VFX path.
Apply the universal items in [the
index](review-checklists.md#universal--all-prompts) first.

## Seedance 2.0

Source skill: `seedance-prompt-20`

### Structure

1. **Section order.** Prompt assembles in this order: Asset preparation → Subject
   definitions → Prompt (with task type) → Shot 1/2/3 → Quality and constraints.

2. **Asset preparation first.** References are labeled with `@Image N`, `@Video N`,
   `@Audio N` (sequential, space separator) before any prompt body.

3. **Reference limits.** ≤ 9 images, ≤ 3 videos, ≤ 3 audio (15 total). Audio cannot
   be sent alone. Combined video duration ≤ 15s, combined audio duration ≤ 15s.

### Subject definitions

4. **Define keyword.** Uses `Define` keyword with 2-3 stable static features
   (clothing, hairstyle, appearance, category). Static only — no mutable attributes
   like expression or pose.

5. **Label reuse.** The same `@Image N` / `@Video N` label is reused in every shot.

6. **No Asset IDs.** Uses `@Image 1` / `@Video 1` format, not Asset IDs.

### Reference classification

7. **Classification.** Each reference is classified as: Visible identity, Visible
   environment, Motion/camera reference, or Control-only reference.

8. **Control-only handling.** Control-only images are preferably translated to text.
   If kept, labeled as control-only with extraction instructions and visual
   reproduction prohibition.

9. **Face restriction.** No direct uploads of real human faces. Uses recent model
   outputs, preset digital characters, or authorized `asset://` portrait
   assets (CRITICAL when a raw real-person photo is bound).

9a. **No storyboard binding (`board.animatic_review_only`).** Board panels and
   grids are never bound; their staging is written in the shot lines (CRITICAL
   when bound).

### Task type declaration

10. **Task type declared.** One of: Multimodal Reference | Video Editing | Video
    Extension | Combined Tasks.

11. **Edit/extend phrasing.** For edit/extend: uses `@Video 1` directly ("Strictly
    edit @Video 1..."). Does NOT write "Reference @Video 1" (which triggers
    multimodal reference mode).

### Shots

12. **Timeline storyboard.** Uses `Shot 1 / Shot 2 / Shot 3` format. Each shot
    covers one coherent unit of action.

12a. **Shot plan carried (`shot.plan_bound`, `shot.variety`, `shot.axis_carry`).**
    The Seedance 2.5 shot-plan items (`shot.plan_bound`, `shot.variety`, `shot.axis_carry` in [the 2.5 checklist](checklist-seedance-25.md#shot-plan-and-structure)) apply to a 2.0 prompt: each shot line carries
    its size, angle, camera move (or a recorded static reason) and a declared
    light source with its key side, and neighboring shots differ.

13. **Per-shot references repeated.** Every shot repeats applicable `@Image N`,
    `@Video N`, `@Audio N` references inline.

14. **Per-shot description order.** (1) Camera movement/transition, (2) Subject
    actions/expressions, (3) Position/spatial changes, (4) Lighting & color tone,
    (5) Audio.

15. **Coherent camera movement.** Use one or two clear requested movements per
    shot, with sequence and endpoints; avoid competing simultaneous directions.

16. **Complexity budget.** At most 3 major action beats or 4 tightly related shots
    for 15s generation.

17. **Action detail.** Body-part level detail (hands, legs, head, shoulders, back)
    with range, speed, force.

18. **Motion preference.** The performer's body prefers slow, gentle,
    continuous motion and avoids high-burst, large-dynamic actions unless the
    brief calls for them. Camera and cut energy follow the shot plan, not this
    item.

19. **Emotion externalization.** Emotions are externalized as physical details,
    never bare labels.

20. **Dialogue format and budget (`dialogue.speech_budget`).** Spoken text in
    `{curly braces}` or quotes for lip-sync, with speaker labels for several
    speakers. Use measured delivery or a native-language-informed read with
    pauses, onset and tail. Words / 2.2 is an English planning estimate, not a
    universal rejection rule. Initially allow 0.5-1.5 s onset and at least
    0.4 s tail, then verify actual delivery; without evidence, fit is provisional.
    Preserve approved text; propose retiming or splitting before an authorized
    wording change.

### Timing

21. **Duration via API.** Total video length set with API `duration` parameter, not
    timecodes in text.

22. **Natural pacing.** The model paces multi-shot generation naturally. Second-level
    timing only when user explicitly requests it.

23. **Timestamp format.** If used: concise ranges (`Shot 1 (0-4s):`), contiguous,
    non-overlapping, consistent with API duration.

### Spatial continuity

24. **Spatial map present.** Same 6-field format as Seedance 2.5 (Start, Travel axis,
    Subject order, Boundary behavior, End, Forbidden transitions).

25. **Physical locations.** Uses physical locations and ordered states, not relative
    verbs alone.

### Quality and constraints

26. **Inline constraints.** All constraints go inline in the text prompt (no separate
    negative_prompt field).

27. **Prioritized constraints.** Prioritizes constraints instead of accumulating a
    long blacklist.

28. **Positive phrasing.** States required physical behavior positively. Repeats only
    the few exclusions that prevent expensive failure.

### Preflight review (6-point)

29. **Parameter agreement.** Prompt and API resolution, duration, ratio, and audio
    setting agree.

30. **Reference indexing.** Every reference is indexed, classified, and bound only
    where intended.

31. **Spatial fields.** Start, travel axis, subject order, boundary behavior, and end
    state are explicit.

32. **No contradictions.** No contradictory instructions (e.g., "single continuous
    shot" plus several cuts; "no powers" plus an emitting aura reference).

33. **Focus.** Prompt is focused; repetition compressed before removing critical
    spatial state.

34. **Beats fit duration.** Requested beats fit the duration or the scene is split.

### Revision contract (if revising)

35. **Locked decisions carried.** Approved identity, action, camera, environment,
    audio, boundary behavior carried into revised prompt.

36. **One delta.** Only one of {prompt wording, reference bundle, motion design}
    changed per retry.

37. **Acceptance criteria.** Observable conditions for the next take to pass are
    stated.

38. **Known rejections.** Behaviors from earlier takes that must not return are listed.

---

## Seedance VFX (video-to-video)

Source skill: `seedance-vfx-prompt`

### Core principle

1. **Source clip is the lock.** The prompt preserves what to keep (subject identity,
   performance, camera motion) and describes only what should change. It does not
   re-describe the entire scene from scratch.

### Asset preparation

2. **@Video 1 is source.** Source clip is always `@Video 1`. Uses "Strictly edit
   @Video 1" (NOT "Reference @Video 1").

3. **Source described.** Subject, action, camera motion, and duration of source clip
   are described in asset preparation.

4. **Source inspected.** The source clip was inspected before writing (duration, fps,
   aspect ratio probed). Prompt is built from footage, not user's one-line summary.

5. **Texture references labeled.** Texture references say "texture only" — "appearance
   and fur/skin texture reference only; ignore the photo's background and lighting."

### Subject definitions

6. **Define keyword.** Uses `Define` with 2-3 core static features. Bound as
   `<Label>@Video 1`.

### Locks (preservation)

7. **Locks declared.** Identity (face, body, costume, props), Performance (gait,
   gestures, expressions, timing), Camera (motion type, framing, lens, bob),
   Continuity are locked with `<Label>@Video 1`.

### Change

8. **Change named with timestamp.** The exact change and when it happens are stated
   (`At 0:NN` for localized changes). Global changes at `0:00`.

9. **Subject reaction.** Whether the subject reacts or does not react is stated.

### New world

10. **Full description.** Replacement/added environment/element is fully described.

### Lighting (embedded)

11. **Lighting lives in the world.** Light sources are physically present in the new
    world. Not described as a layer pasted on top.

12. **No generic lighting terms.** Does not say "cinematic lighting" or "dramatic
    lighting" alone — names the source.

13. **Light on subject.** Where light falls on subject (direction, color, intensity)
    is described.

14. **Light-environment interaction.** How light interacts with environment
    (volumetric mist, reflections, shadows) is described.

15. **Integration fork decided.** Either "preserve subject's lighting; grade only new
    elements" (default) OR "relight the whole frame under one look" is explicitly
    chosen.

16. **"Looks pasted in" recipe applied.** Light (direction, softness, shadow density),
    environmental bounce, optics & atmosphere (lens, micro-contrast, haze, DOF, grain),
    edges & grounding (no hard cut-out, no halos, matched rims) are addressed.

### Space

17. **Layered space.** Foreground (parallax elements), Midground (subject + primary
    environment), Background (atmosphere and scale) are described.

### Timing

18. **Sequential timestamps.** When each event triggers and how it progresses.

19. **Timed camera moves dual-anchored.** Semantic anchor ("At the line '<exact
    words>,' the camera <move>") AND numeric anchor ("At about <T> seconds...").

20. **Zoom type specified.** Crash zoom = fast hard punch-in. Smooth push-in = slow
    steady glide.

21. **Tail after trigger.** Enough tail (~2-3s) after trigger for payoff. If clip is
    short, zoom fires on first word.

22. **Reveal pull-back.** If used: opens tight on added element, moves outward to land
    on real plate, demands 100% match of source composition at landing.

23. **Lip-sync window checked.** If lip-sync preservation: line quoted verbatim,
    anchored twice (in change/action and in audio), `SFX and source dialogue only`
    requested, "lips matching the source exactly" in Locks, line fits surviving
    dialogue window.

### Audio

24. **Diegetic only.** Only sound that physically exists in the new world. Preserves
    source-clip diegetic sounds that still make sense.

25. **No non-diegetic audio.** Does not request background music, score, or voiceover
    unless part of source footage.

### Quality and constraints

26. **NON-IP.** No recognizable real persons, no copyrighted characters, no brand logos.

27. **Face protection.** "Real human skin with pores, stubble, and catchlights — never
    waxy, smoothed, or warped."

28. **Supported model/mode (`model.supported_mode`).** Resolve operation and
    model first. A 2.5 face-containing edit uses supported 480p/720p/1080p;
    only an explicitly selected supported legacy path may use 4K. Face/detail
    fidelity is an output-QA criterion, not a guaranteed property of resolution.

### Creature/element integration (if applicable)

29. **Photoreal demanded.** "Fully photoreal, real fur with depth and individual
    strands, true anatomy, never CG, plastic, or cartoonish."

30. **Tied into plate.** Same sun direction, real soft-edged contact shadow, same hazy
    atmosphere.

31. **Scale explicit.** Scale is explicit for giant creatures.

32. **Texture fallback.** If still reads CG: second input — reference photo of real
    animal as texture-only `@Image N`.

33. **Species behavior.** Behavior matches the species (sloth slow, chimp twitchy,
    snake coils and forked tongue, snakes don't blink).

34. **Living micro-movements.** For static creature holds: slow blink, jaw shift,
    steady breath.

### Duration discipline

35. **Source runtime default.** Defaults to source clip's exact runtime.

36. **Recomputed timing.** If runtime changed, numeric zoom timing is recomputed.

37. **Prepended-intro budget.** `total runtime − intro length = surviving window for
    source performance`. If source take longer than surviving window, one of three
    resolutions offered (extend total, start source earlier, accept truncation).

### Iteration discipline

38. **Only named change.** Only the named thing changes; rest of prompt stays stable.

39. **Refine via edit.** When refining a generated still/frame, edits the chosen result
    (passes it back as base) and fixes only what is off.

### Voice

40. **No generic adjectives.** No "beautiful," "stunning," "amazing," "cinematic."

41. **Concrete language.** Names exact materials, behaviors, scale, lenses, angles,
    moves. Uses texture words. Does not inflate, soften, or explain what things
    "represent."
