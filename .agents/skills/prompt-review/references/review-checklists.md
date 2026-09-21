# Review Checklists

Consolidated, actionable validation checklists for every prompt-writing skill in the
repo. Each section is self-contained — pass the relevant section to the review
sub-agent along with the prompt text.

## Table of contents

- [Universal — all prompts](#universal--all-prompts)
- [Seedance 2.5](#seedance-25)
- [Seedance 2.0](#seedance-20)
- [Seedance VFX (video-to-video)](#seedance-vfx-video-to-video)
- [Seedance 2.5 edit (video-to-video)](#seedance-25-edit-video-to-video)
- [Seedance Filipino dialogue](#seedance-filipino-dialogue)
- [Seed Audio](#seed-audio)
- [Seedream image generation](#seedream-image-generation)
- [Seedream character sheet](#seedream-character-sheet)
- [Seedream location asset](#seedream-location-asset)
- [Seedream storyboard](#seedream-storyboard)
- [Seedance music video](#seedance-music-video)

---

## Universal — all prompts

Applicability comes from explicit prompt type, model, operation, and change
contract. Workspace invariants are owned by `../../../contracts/rules.json`;
this section maps them into review guidance. Check applicability before each
item and record a reason for not_applicable. Specialized heuristics do not
change the production policy. Source metadata: `rule-provenance.json`.

1. **Visible consistency (`asset.visible_consistency`).** Required canonical
   inputs are named, versioned, and approved before dependent production
   generation. Draft breakdown may identify unresolved inputs. Branded,
   recurring, story-critical props and scene-variant wearables need separate
   references; incidental objects can be text-only. Copy locked descriptors
   exactly when they apply; a new element prompt is authoring canon, not
   consuming a pre-existing approved version of itself.

2. **Positive direction.** Prefer concrete desired behavior and appearance.
   Technical exclusions, precise edit boundaries, and preservation constraints
   are allowed when they reduce ambiguity; a negation alone is not a failure.

3. **Narrative event (`narrative.observable_event`).** Narrative shot prompts
   contain observable action and relevant intent. Static turnarounds, location
   plates, UI/product sheets, music beds, SFX, and ambience are not_applicable;
   evaluate their composition, consistency, or sonic event instead.

4. **Watermark.** Apply only where the selected tool supports the parameter.
   If the request specifies watermark behavior, it defaults to `false`
   unless the user explicitly requested the AIGC watermark.

5. **Duration right-sizing.** The prompt does not pad a scene to fill a maximum
   duration. Each scene is set to its natural length (4-30s for Seedance 2.5, up to
   15s for Seedance 2.0).

6. **Parameters in the API, not the prompt.** Generation parameters (duration,
   resolution, aspect ratio) are not embedded in the prompt text unless the skill's
   structure explicitly includes them. They belong in the API call.

7. **Prompt snapshot location.** The prompt is saved beside the media asset it
   produced, using the `prompt_` prefix convention. It is not duplicated in shot
   folders, scene folders, or any other location.

8. **No duplicate action descriptions.** The same action is not described twice in
   the same prompt. Each beat appears once.

9. **No generic adjectives.** The prompt avoids "beautiful," "stunning," "amazing,"
   "cinematic" as standalone descriptors. It uses concrete, specific, observable
   language instead.

10. **@tag references.** All project Elements (characters, locations, props) are
    referenced by their locked `@tag` and bound to the correct `@Image N` / `@Video N`
    / `@Audio N` index.

11. **Reference-derived talent is distinct.** When a template came from a
    competitor or category reference, character descriptors do not reproduce
    the reference performer's distinctive combination of face, hair, wardrobe
    and styling. Keep the role and staging; change the identity.

12. **Product descriptors match the packshot.** Every product cue in the prompt
    (pack type, size, colour, cap, label layout) agrees with the bound official
    product reference. A descriptor inherited from the reference ad's product
    fails.

13. **No invited copy or marks.** The prompt does not quote taglines, captions,
    slogans or source-brand names, and does not ask the model to render readable
    brand text or logos that a deterministic overlay or official asset should
    supply. Words like "logo", "tagline" or "text reads" are deliberate only.

---

## Seedance 2.5

Source skill: `seedance-prompt-25`

### Formula check

1. **Subject + Action present.** The prompt contains at minimum a clear subject and a
   primary action or event. These are the only required parts.

2. **Six-part formula.** The prompt follows: Subject + Action/Event + Scene/Environment
   (optional) + Visual Style (optional) + Camera Movement/Cut (optional) + Audio
   (optional). Parts are in this order.

3. **No double-description.** The same action is not described in multiple sections.

4. **Action granularity.** The Action slot describes motion at the body-part
   level (hands, arms, legs, head, shoulders, back, hips, feet) with range,
   speed, and force, grounded in weight, balance, momentum, and contact — not
   as bare verbs. High-burst, large-dynamic actions are avoided unless the
   shot requires them.

### Reference materials

5. **Material mapping in prompt.** Every reference material is mapped directly in the
   prompt text — the model never has to guess which asset belongs to which
   person/prop/scene.

6. **Individual naming.** Each subject is named and bound individually. The prompt
   does not use lazy groupings like "@Images 1 through 4 define four characters."

7. **Grouped by type.** References are organized as [Characters], [Props], [Scenes],
   [Motion and Audio] sections.

8. **Centralized profiles.** Important subjects have a centralized profile block with
   stable attributes that is referenced in each scene.

9. **Per-scene selection.** Each scene names only the references it uses — not all
   materials at once.

10. **Exclusion phrasing.** "Do not use..." exclusions appear only when leakage is
   genuinely possible. Not as a generic negative-prompt dump.

11. **Multiple views.** If multiple images define one subject, the prompt explicitly
    states "The output must contain only one [subject] throughout."

12. **Video reference inheritance.** If inheriting from a reference video, only the
    attributes to inherit are stated. The prompt does not restate every action from
    the reference (which can conflict).

13. **Control-only references (`references.control_only`).** Translate to text
    and omit by default. Intentional conditioning requires explicit user selection,
    current source hashes, supported tool/mode inputs, and leakage QA; labels or
    extraction instructions alone do not grant eligibility.

14. **Reference count limits.** ≤ 30 images, ≤ 10 videos, ≤ 10 audio. Recommended:
    1-8 image subjects, 1-5 video subjects (5-10s each), only directly relevant audio.

### Scene staging

15. **Stage structure.** The story is divided into consecutive stages. Each stage has
    ONE primary state change and a clear end state.

16. **Natural duration.** Each scene is generated at its natural duration (4-30s),
    not padded to 30s. 30s single-pass or extension is the exception, not the default.

17. **Timestamp ranges.** Time ranges are consecutive and non-overlapping. They are
    treated as a time budget, not precise edit points.

18. **No impossible frequencies.** The prompt does not demand impossible action
    densities (e.g., "complete three actions in one second").

### Audio syntax

19. **Audio bracket syntax.** Dialogue in `{}`, music in `()`, SFX in `<>`, subtitles
    in `【】`. All audio content uses the correct bracket type.

20. **Dialogue language reinforcement.** Non-Chinese dialogue includes: Dialogue
    Language + Regional Variety/Accent + Delivery Style + Speaker + `{dialogue}`.

21. **Same dialogue in both prompts.** If audio-first pipeline is used, the exact
    dialogue text in the Seed Audio prompt matches the `{curly brace}` text in the
    Seedance prompt. No paraphrasing, reordering, or omitted lines.

### Emotional direction

22. **Visible/audible cues.** Abstract emotions are paired with directly visible or
    audible cues (eye movement, brow tension, mouth movement, breathing, gaze, hand
    movement). Select 2-4 readable cues per emotional transition, grounded in
    the playable tactic and framing. Close-ups can use eye/mouth detail; masked
    wide shots need posture, spacing or hand action. Blink guidance is relevant
    only when visible and needed; do not move the camera to rescue unreadable cues.

23. **No bare emotion words.** The prompt does not rely solely on emotion labels like
    "very sad" or "extremely angry" without physical externalization.

### Camera language

24. **Coherent camera direction.** Use one or two clear camera movements when
    requested, with the subject, beginning, and endpoint of each stated. Avoid
    competing simultaneous moves; preserve a requested static camera.

25. **Uncommon cinematography terms.** If used, they follow the format:
    Term + Target Subject + Visual Change + Foreground/Background Relationship +
    Direction or Speed.

### Spatial continuity

26. **Spatial map present.** Movement-heavy scenes include: Start positions,
    Travel axis, Subject order, Boundary behavior, End state, Forbidden transitions.

27. **Physical locations.** Uses physical locations and ordered states, not relative
    verbs alone.

28. **Invariants repeated.** Critical spatial invariants are repeated in every
    shot/stage since every cut can reset relationships.

### Parameter auto-lock

29. **Editing task.** Aspect ratio and duration are not set (locked to input). Edit
    scope, target quantity, and content to preserve are defined.

30. **First/last-frame task.** Aspect ratio locks to first image. First and last
    frames share the same aspect ratio.

31. **Extension task.** Aspect ratio is not set (locked to input). Duration can be
    set. Boundary image, motion trend, and audio continuity are checked.

### Preflight review (15-point)

32. **Subject & action** clearly stated.
33. **Reference roles**: every reference states what to use and what not to use.
34. **Subject binding**: every required canonical character/product/prop named and bound to a
    reference.
35. **Scene selection**: references selected by scene, not forced to appear all at once.
36. **Stage structure**: each stage has only one primary change and a clear end state.
37. **Consistency**: character count, clothing, prop ownership, spatial relationships
    stay consistent.
38. **Editing master**: for editing, sole editing master, edit scope, target quantity,
    content to preserve defined.
39. **Emotion & camera**: abstract emotions and cinematography terms paired with
    visible/audible cues.
40. **First/last frames**: one role per image; first and last share aspect ratio.
41. **Storyboards & blockouts**: storyboard states which structure to inherit;
    blockouts identify coarse vs fine.
42. **Auto-lock rules**: editing, first/last-frame, and extension follow locked
    aspect-ratio and duration rules.
43. **Extension boundary**: boundary image, motion trend, and audio continuity checked.
44. **One-click video**: material roles, image order, motion amount, editing style,
    and audio defined.
45. **Seamless transitions**: two videos' roles, trigger action, transition process,
    and arrival state defined.

46. **Speech fits duration.** For dialogue-driven shots, estimate speech length
    ≈ spoken words / 2.2 (conversational) to seconds. If the `{}` script reads
    far shorter than the API `duration`, the prompt must explicitly direct the
    gap (pauses, hesitations, action beats); otherwise right-size the duration.

### Motion grammar (stylized animation & reverse-engineered takes)

47. **Every moving element has motion grammar.** Each element that moves is
    described with motion type (translate/rotate/scale/parallax/drift/float-bob/
    pulse/flicker/color-cycle/twinkle/shimmer/sway/wave/slide/zoom/rotation),
    direction, speed, amplitude, easing, and loop period — not as a bare verb.
    A prompt that names *what* moves but not *how* it moves produces a static
    take.

48. **Camera motion stated explicitly.** The prompt states camera motion — and
    explicitly says when the camera is static and only elements/light move.

49. **Light/color motion stated.** Any pulse, strobe, flicker, hue cycle, bloom,
    or shimmer is described with its rate (e.g. "~1Hz chromatic shimmer").

### Storyboard grid reference

50. **Eligible storyboard conditioning.** Omit control sketches by default.
    Only after explicit selection, source-hash checks, and live mode compatibility
    may a storyboard grid be bound to an `@Image N` with the reading
    order (left-to-right, top-to-bottom) AND a positive style override — the
    prompt must state the board is used ONLY for scene order and composition and
    that the output must render in the target style, not copy the board's
    rendering medium. The bare "Do not use the grid's sketch lines, panel
    numbers, or divider lines" exclusion only removes the board's *markup* — it
    does not stop the model from copying the *medium* (line art, paper texture,
    monochrome shading). It locks shot order and composition only; color,
    motion, and timing stay in the prompt text.

### Revision diff

51. **No approved per-shot detail lost.** When a prompt is revised to change one
    shot, every OTHER shot's previously-approved wording (descriptors, motion
    rates, glow pulses, gradient outlines, camera moves) is carried over
    verbatim. A revision that silently drops detail from untouched shots is a
    MAJOR finding — diff the new prompt against the prior snapshot and flag any
    removed descriptor or rate.

---

## Seedance 2.5 edit (video-to-video)

Source skills: `seedance-prompt-25` (editing) + `seedance-vfx-prompt` (2.5 section).

Apply "Universal — all prompts" first, then this section. Mark N/A any item
whose feature is absent (no references → skip material mapping).

### Editing task

1. `[Edit Goal] Edit @Video 1 …` present and one-sentence; submit with
   `omni_reference_task_type="edit"` (2.5 values: `auto | reference | edit |
   extend` — `edit_video` is 2.0-only and is rejected).
2. `[Source Video Role]` declares `@Video 1` as the sole editing master and
   lists what it defines (subjects, scene, actions, camera, event order).
3. `[Target Material Role]` present iff references are used: each `@Image N`
   mapped to one target; "Do not use its background/people" present;
   single-person sheets directed to use the close-up panel only.
4. `[Edit Scope]` states what changes and, for what must not change, a positive
   "exactly one <subject> — never a second or duplicated copy" guard.
5. `[Content to Preserve]` lists identity/motion/timing/camera/lighting to keep.

### Preservation locks (only where MUST PRESERVE says so)

6. Quantity: "Exactly one <subject> in frame — never a second or duplicated copy."
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
    Apply the same camera-complexity guidance as general Seedance 2.5 item 24.
14. Camera-move items are N/A when the edit must preserve the source camera.

### Change contract

15. Flag only breakage of MUST PRESERVE or a quality defect in the change
    description — never an item the user explicitly asked to change.

---

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

9. **Face restriction.** No direct uploads of real human faces. Uses model outputs,
   preset digital characters, or authorized real-person assets.

### Task type declaration

10. **Task type declared.** One of: Multimodal Reference | Video Editing | Video
    Extension | Combined Tasks.

11. **Edit/extend phrasing.** For edit/extend: uses `@Video 1` directly ("Strictly
    edit @Video 1..."). Does NOT write "Reference @Video 1" (which triggers
    multimodal reference mode).

### Shots

12. **Timeline storyboard.** Uses `Shot 1 / Shot 2 / Shot 3` format. Each shot
    covers one coherent unit of action.

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

18. **Motion preference.** Prefers slow, gentle, continuous motion. Avoids
    high-burst, large-dynamic actions.

19. **Emotion externalization.** Emotions are externalized as physical details,
    never bare labels.

20. **Dialogue format.** Spoken text in `{curly braces}` or quotes for lip-sync.
    Multi-speaker format with speaker labels.

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

---

## Seedance Filipino dialogue

Source skill: `seedance-prompt-25-filipino`

Use as an additional checklist alongside Seedance 2.5 when the scene contains Tagalog,
Filipino, or Taglish dialogue.

### Words, register and scope

1. **Exact words protected.** Locked dialogue, names and approved spelling are
   unchanged. A pronunciation request alone does not authorize simplification.
2. **Smallest relevant repair.** Separate wording, delivery, pronunciation and
   timing problems. Change vocabulary only when authorized and appropriate to
   the speaker, relationship, region and period; literary language is valid.
3. **Register grounded.** Do not impose modern Manila Taglish, contractions,
   honorifics or a fixed sentence length on every speaker. Preserve intentional
   code-switching and politeness.

### Pronunciation and delivery evidence

4. **Evidence distinguished.** Identify a supplied recording, pronunciation guide
   or competent speaker's correction. Without evidence, a predicted issue is a
   hypothesis, not a proven mispronunciation.
5. **No universal phonology recipe.** Do not force a default stress, flat contour,
   consonant substitution or one regional accent across Filipino speakers.
6. **Notes separate from speech.** Preserve exact spoken text inside braces.
   Annotation or phonetic respelling inside dialogue requires explicit scope.
7. **Cues serve intent.** Use concise, observable delivery rather than a dictionary
   or a prescribed pitch sequence. Verify actual pronunciation by listening;
   ASR text alone does not establish stress, intonation or speaker identity.

### Separate audio, only when requested

8. **Native default retained.** Filipino language or an accuracy concern alone
   does not trigger a separate Seed Audio track.
9. **Same approved words.** When separate lip-sync audio is requested, both
   prompts preserve exact words; simplification is not a prerequisite.
10. **Actual evidence retained.** Audio path/hash, inspected duration and original
    timestamp evidence remain separate from proposed prompt timing. Align only
    the synchronization detail required by the request.
11. **Input binding checked.** The resolved tool supports the submitted audio
    role, and the caller records the exact ordered binding and review evidence.

---

## Seed Audio

Source skill: `seed-audio-prompt`

### Full-soundscape ingredients

1. **Environment.** Location, weather, context, acoustic space described.
2. **Background music and SFX.** Dramatic role, style, instruments, rhythm, mood,
   volume, opening intensity described.
3. **Character actions/appearance.** Included when they affect performance.
4. **Character voice profile.** Age, gender, accent, emotion, tone, speed, timbre for
   each character.
5. **Exact dialogue.** In double quotes, with delivery note before the quote.

### Arrangement order

6. **Input references** (only when reference audio included).
7. **Opening environment, ambience, music.**
8. **Dialogue, actions, SFX** in chronological order.
9. **Ending behavior.** Resolve, fade, sustain, or cut.
10. **Creative/quality constraints** (only when user supplies them).

### Input references

11. **Reference count.** ≤ 3 reference audio (TA2A) OR exactly 1 reference image
    (reference-image mode). Mutually exclusive.

12. **Per-clip limits.** ≤ 30s, ≤ 10 MB. Formats: WAV, MP3, PCM, OGG_OPUS.

13. **Single purpose per clip.** Each clip serves exactly one purpose: voice timbre
    cloning, emotion reference, or SFX reference.

14. **TA2A mapping.** `<<TGT_SPK1>>`, `<<TGT_SPK2>>`, `<<TGT_SPK3>>` mapped to ordered
    entries in `references[]`, labeled `@Audio1`, `@Audio2`, `@Audio3`.

15. **No references section.** When no references, the input references section is
    omitted entirely.

### Environment

16. **Acoustic quality specific.** "Hallway reverb," "stone corridor echo" — not just
    "echoey room."

17. **Layers described.** Foreground, midground, background.

18. **Evolution.** How environment evolves over time.

### Background music

19. **Dramatic role.** Underscore, tension bed, transition, reveal, celebration, outro.

20. **Style/genre/instruments.** Concrete musical language, not generic phrases.

21. **Dynamic arc.** How it begins, swells, thins, changes instrumentation, stops.

22. **Relationship to speech/effects.** When music ducks, effects dominate, ambience
    remains distant.

23. **Ending.** Clean stop, held unresolved note, crossfade, gradual fade.

### Ambience

24. **Persistent bed.** Separate from one-off effects.

25. **Distance/direction/room tone.** Echo, reverb, gradual evolution described.

26. **Subordinate to dialogue.** Unless scene requires otherwise.

### Sound effects

27. **Source/action/material/acoustic character.** Spatial position described.

28. **Positioned relative to actions/dialogue.**

29. **Evolution/decay.** Described when important.

30. **Onomatopoeia in quotes.** "ring-a-ling," "zzzip," "clack" — used to clarify
    texture, not as a substitute for describing the sound.

31. **Foreground/midground/background.** Identified when mix could be ambiguous.

### Character voice profiles

32. **T2A format.** `Name (age, gender, accent, voice timbre, emotional tone, delivery
    style) says: "dialogue text"`

33. **TA2A format.** `Name (voice description, voiced by <<TGT_SPKN>>) says [delivery
    note]: "dialogue text"`

34. **Voice contrast.** Each voice contrasts through pitch, timbre, accent, pacing,
    emotional baseline, or performance style.

### Dialogue

35. **Double quotes.** Spoken text in double quotes.

36. **Delivery note before quote.**

37. **Physical actions included.** When they affect delivery or generate sound.

38. **Multi-character chronological.** Alternates chronologically; actions/music/SFX
    between lines where listeners should hear them.

39. **Explicit attribution.** No unlabeled blocks of alternating quotes.

40. **Non-speech in brackets.** Ambient descriptions and non-speech sounds wrapped in
    square brackets.

41. **Prompt language = script language.** The prompt and the dialogue script are in
    the same language.

### Scene transitions

42. **Transition block format.** Audio state A → Transition trigger → Transition
    behavior → Audio state B → Forbidden carryover. All five fields present.

### Timestamp control

43. **Format.** `[start_time:end_time]` immediately before dialogue, in seconds with
    decimal precision.

44. **Used only when precision matters.** Omitted when event-relative cues suffice.

### Validation

45. **Character limit.** `text_prompt` ≤ 3000 characters.

46. **Duration limit.** Generated audio ≤ 120 seconds per call.

47. **No API concerns in prompt.** Does not insert "Max duration: 120 seconds" into the
    prompt — that is an API concern.

48. **Long requests split.** If requested generation > 120s, split before sending.

### Audio-video alignment (when used with Seedance)

49. **Same dialogue text in both prompts.** Exact lines match between Seed Audio
    `text_prompt` and Seedance `{curly braces}`.

50. **Audio duration ≤ video duration.**

51. **Shot timestamps align to audio.** Seedance shot time ranges match actual audio
    timing.

52. **Audio as reference_audio.** Passed to Seedance task as `reference_audio`.

### Brand-name pronunciation

53. **Respelling inside the dialogue line.** Any brand or domain name the
    voiceover must say correctly has its phonetic respelling written *inside*
    the dialogue line itself (not only in a note), using a real-word anchor
    rather than spaced or capitalized letters (e.g. `Echo-nos`, not `EH ko nos`).

---

## Seedream image generation

Source skill: `seedream-prompt`

### Structure

1. **Section order.** Subject > Setting > Style > Lighting > Composition > Technical.
   Order matters — earlier concepts carry more weight.

2. **Most important subject first.** The primary subject appears before secondary
   subjects.

3. **Reference labeling.** `@Image 1`, `@Image 2`, ... sequential numbering with `@`.

4. **Reference list is inventory.** Each reference is also bound again where it affects
   output — not just listed in the reference section.

5. **Exact tokens.** Uses exact `@Image N` token every time. Does not drop `@` or
   replace with ambiguous phrase.

### Reference limits

6. **Seedream 5.0 Pro.** ≤ 10 input images.
7. **Lite.** Refs + outputs ≤ 15.

### Task type

8. **Correct task type.** T2I, I2I, Image Editing, Sequential Generation, or
   Infographic/Information Visualization.

9. **Sequential generation.** NOT supported on 5.0 Pro. Requires Lite/4.5/4.0.

### Subject

10. **2-3 stable attributes.** Each subject defined with 2-3 stable attributes.

11. **Multi-subject priority order.** Listed in order of visual priority.

### Photographic treatment, when requested

12. **Intent preserved.** Camera/film terminology is optional shorthand. Do not
    require it or a cinematic treatment for every photographic image.
13. **Lighting appropriate.** Soft, flat or shadowless light may be intentional.
    Preserve the approved lighting unless changing it is within scope.
14. **Identity protected.** Describe relevant existing texture; do not invent
    freckles, age, wrinkles or material damage as a generic realism cure.
15. **Readable hierarchy.** Lead with the requested result. Headings and ordering
    are clarity conventions, not proven positional weighting laws.
16. **Focused exclusions.** Use only necessary scope or demonstrated-leakage
    exclusions; do not demand aggressive boilerplate negatives.
17. **Diagnosis grounded.** Cite a visible symptom in a supplied output or label
    the example hypothetical. Do not promise a prompt will produce realism.
18. **Parameters verified.** Actual size and optimization settings belong in
    request metadata and must be supported by the resolved live model/tool.

### Text in image

19. **Routing boundary.** Model-rendered text is present only when the user
    expressly accepts it as expressive and non-exact. Delivery-critical copy,
    data, UI, pricing, CTA, logos, or pixel layout is a MAJOR routing defect;
    require a text-free generative layer plus deterministic finishing.

20. **Quoted prompt intent.** Accepted model text is in double quotes and its
    surface is described; quoting does not establish pixel-exact output.

21. **Instability disclosed.** Small text may still be unstable and the prompt
    does not claim deterministic fidelity.

### Constraints

22. **Inline only.** All constraints in the text prompt. No separate `negative_prompt`.

23. **Quality directives and negative constraints.** Only those that materially affect
    output.

### Prompt length

24. **30-100 words.** For standard images. Infographics and complex scenes can go
    longer but stay focused.

---

## Seedream character sheet

Source skill: `seedream-character-sheet`

### Layout

1. **Three-panel default.** Back full-body, front full-body, face close-up. Unless user
   explicitly asks for more panels.

2. **Neutral gray background.** Default studio background — neutral gray, never
   scene-specific. Deviates only if user explicitly wants stylized/filmic sheet
   background.

3. **Panel order.** Back full-body first, front full-body second, frontal close-up
   third.

### Subject

4. **Reference binding.** Each reference is bound inline.

5. **Required elements.** Age, ethnicity/cultural identity, 2-4 stable facial traits,
   hair and headwear, costume, key accessories.

6. **Same person statement.** Explicitly states it is the same person in all panels.

7. **No held props.** Nothing held, carried, aimed, or operated appears in the sheet;
   branded, recurring, or story-critical ones need separate `prop_` sheets,
   while incidental objects may be text-only in scenes. Scene-variant wearables (e.g.
   sunglasses worn only in some scenes) are also excluded and made props instead.
   Only always-worn outfit elements (hat, helmet, eyewear, jewelry) may appear.

### Setting

8. **Default background.** Neutral gray seamless, no props, no held objects, no
   furniture, no environmental clutter.

### Lighting

9. **Neutral, not scene-specific.** Soft, even studio light, flat fill, neutral
   white balance, no mood, no dramatic shadows, no hotspots, no blown highlights.
   Lighting never changes to match the character's scene or story mood.

10. **Consistent across panels.** Lighting is identical across all three panels.

### Composition

11. **Three panels only.** No extra panels.

12. **Same identity.** Same character identity across all panels.

13. **Readable silhouette.** Costume silhouette readable in body panels.

14. **Face authority.** Close-up panel is the face authority.

### Constraints

15. **Common negatives.** No extra panels, no profile panel, no 3/4 panel, no props in
    hands, no held objects/weapons, no background variation, no scene lighting or
    color cast, no distorted hands, no extra fingers, no watermark.

### Workflow

16. **Cleanup check.** When the requested downstream reference policy requires
    one readable face, inspect for extra faces and return the defect to the
    caller. Cleanup is conditional, non-destructive, and requires new selection;
    this reviewer does not invoke an editing skill.

17. **Element saved.** Saved under `elements/<character-id>/`.

18. **Selected variant.** Approved filename recorded as `selected_variant` in
    `character.md`.

---

## Seedream location asset

Source skill: `seedream-location-asset`

### Location

1. **Place described.** Interior/exterior, function, scale, spatial mood, core
   architectural identity.

### Era and world rules

2. **Historical period.** Stated if relevant.

3. **Geography/climate.** Stated if relevant.

4. **Technology limitations.** Stated if relevant.

5. **Realism constraints.** Explicitly excludes modern intrusions if realism matters.

### Set dressing and objects

6. **1-3 hero set pieces.** Key defining objects.

7. **Practical objects.** Objects that imply use.

8. **Material realism and wear.** Surfaces show wear and use.

9. **Depth cues.** Foreground/midground/background.

10. **Lived in.** Not empty — feels inhabited.

### Style

11. **2-4 strong anchors.** From: photorealistic, cinematic, naturalistic editorial
    reference, grounded realism, film still, period-authentic.

### Lighting and atmosphere

12. **Practical key source.** Where the light comes from physically.

13. **Time of day / weather.**

14. **Shadow falloff.**

15. **Haze / dust / smoke / moisture.** Atmospheric particles.

16. **Brightness.** How bright or restrained the scene is.

### Composition and lens

17. **Establishing vs detail vs reference sheet.** Type stated.

18. **Camera angle.** Eye level / high angle / low angle.

19. **Lens length.**

20. **Aspect ratio.**

21. **Depth of field.**

### Ordering rules

22. **Place before mood.** What the place is comes before how it feels.

23. **Era/world rules before lens/style polish.**

### Constraints

24. **Common negatives.** No characters, no modern props, no plastic CGI surfaces,
    no bright white cyc background unless explicitly requested, no text overlays, no
    watermark.

### Three prompt patterns

25. **Pattern A — Reusable asset.** Stable architecture, clear material language,
    minimal action, readable space, reusable identity.

26. **Pattern B — Cinematic establishing still.** Emotional lighting, camera language,
    atmosphere, foreground/background layering.

27. **Pattern C — Reference-preserving iteration.** I2I for every reference-guided
    location prompt.

---

## Seedream storyboard

Source skill: `seedream-storyboard`

### Core rules

1. **One frozen, decisive moment per panel.** Not a collage or multi-panel grid.

2. **Dynamic panel count.** When an upstream analysis (`seed_understand`,
   `tig-scene-engine`, `film-production`, or a script/beat sheet) has identified
   N scenes/shots, the board defaults to one panel per identified scene/shot —
   not a fixed budget. A user-specified smaller count is honored only when
   explicit, with omitted shots recorded as motion notes.

3. **Storyboard handoff eligibility.** Sketches guide authoring and are omitted
   from video inputs by default. A selected production panel or intentional
   conditioning exception needs current source hashes, explicit approval, live
   mode compatibility, and leakage QA. A board's style is a creative choice;
   it is not guaranteed to remain absent from the output.

4. **Explicit canon.** Recurring identities, locations, props, and style are in an
   explicit canon section.

5. **Canonical Element sheets attached.** When matching Element sheets exist, they are
   attached to the generation request — not substituted with text descriptions.

6. **Screen direction and geography.** Treated as sequence-level constraints.

7. **Natural language.** Coherent natural language, not comma-heavy keyword piles.

8. **References bound by role and target.** Every reference bound with exact `@Image N`
   tokens.

9. **Production notes outside image.** Arrows, labels, dialogue, timing, and production
   notes are outside the generated image unless visible story-world text is required.

### Panel prompt structure

10. **References.** Each reference labeled with role (character identity, location
    geometry, prop identity, composition control, approved style).

11. **Panel purpose.** The new story information or emotion this panel communicates.

12. **Subject and decisive moment.** One frozen moment. Every visible subject, pose,
    expression, action, and prop named. Identity and prop references bound inline.

13. **Setting and state.** Location, time, weather, persistent landmarks, visible
    object state. Location reference bound inline.

14. **Staging and continuity.** Screen-left/right positions, foreground/midground/
    background, eyelines, distances, overlaps, travel direction, entrances/exits, and
    what must match the previous panel.

15. **Style.** Medium, realism level, palette, stable treatment. Style reference bound
    inline when provided.

16. **Lighting.** Source, direction, quality, color, and atmosphere.

17. **Composition.** Aspect ratio, shot size, camera height/angle, lens intent,
    framing, depth, and focus priority. Composition guide bound inline when provided.

18. **Constraints.** Appropriate quality (draft or final), preservation (approved
    identity, geometry, pose, state, style), exclusion (only material faults — no text
    overlays, labels, storyboard borders, watermarks, unintended subjects, duplicated
    faces, control-guide marks).

### Sequential generation

19. **Sequence contract.** Cohesive ordered set of N separate images, one per panel.
    Recurring identity, wardrobe, location geometry, prop design, palette, and
    rendering style kept consistent.

20. **Each image is one moment.** Not a collage or multi-panel grid.

21. **Global visual canon.** Stable identity, location, prop, style, aspect ratio, and
    lighting rules stated before individual panels.

### Revisions

22. **Local edits preferred.** After a composition is approved, prefer local edits over
    full re-generation.

23. **Seeds for tracking.** Used for experiment tracking, not as the identity system.

### Status

24. **Review on generation.** Technically successful generation enters `review`.

25. **Explicit user choice.** Only explicit user choice sets `selected_variant` or
    `approved`.

---

## Seedance music video

Source skill: `seedance-music-video`

### Format and genre

1. **Format declared.** Performance, narrative, conceptual, lyric, visualizer,
   or hybrid — with address mode (direct / indirect / none).

2. **Treatment serves intent.** Preserve approved visual choices. Format and
   style follow the desired audience effect and available track evidence; genre
   recipes are optional examples, not compulsory locks or a ban on coherent hybrids.

### Song map

3. **One event per section.** Each song section has one primary visual
   assignment and a visible end state.

4. **Repeated sections have an intentional relationship.** Escalation, restraint,
   repetition or counterpoint follows supplied audible changes or the requested
   effect. A quiet return need not become larger or faster.

5. **Structure is evidenced.** Do not invent a bridge or assume it requires a
   new location, wardrobe or angle. Label a plan provisional when no track or
   user section map supports exact structural claims.

### Audio contract

6. **Audio treatment explicit.** Native audio brackets, `@Audio N` timing
   authority, or hybrid (reference + native generation) — never ambiguous.

7. **Lip-sync lines verbatim in `{...}`.** Match the audio master exactly —
   no paraphrasing, no reordering, no omitted lines.

8. **Timestamped lyric timeline used when coverage is critical.** Each lyric
   line is bound to its own `[X-Ys] { line }` beat slot — not grouped into
   large blocks. Applies to rap, fast vocal delivery, and any verse where
   complete lyric coverage is a hard requirement.

9. **"No line skipped" mandate present.** When the timestamped timeline is
   used, the prompt includes an explicit instruction that no line may be
   skipped, shortened, mumbled, or reordered.

10. **Native audio caveat acknowledged.** If `generate_audio` is true, the
    prompt accounts for re-performance risk (the model re-performs, not copies,
    the reference).

### Beat contract

11. **Audio events named.** Which beats trigger cuts and camera moves —
    not just "cuts on the beat."

12. **Cuts follow intent and evidence.** Do not assume verses are quiet, choruses
    are loud, or every edit precedes a downbeat. Preserve continuous performance
    and unmetered pauses when requested; keep raw timing separate from simplification.

### Structure

13. **Right-sized (4–30s).** One song section per pass, or an explicit
    continuous one-take. Not padded to fill 30s.

14. **Style remains coherent.** A closing summary is optional. Judge consistent
    visual decisions and preservation of the brief, not a required style-seal phrase.

### Rap-specific (when applicable)

15. **Timing is proportional.** Use source-grounded lyric timing when coverage
    or synchronization requires it; rap genre alone does not mandate timestamps.
    Do not invent beat timings or claim to have listened to unavailable audio.

16. **Delivery cue present.** The prompt includes a physical delivery cue
    (e.g., "jaw opening fully on vowels, lips stay in frame throughout").

---

## UGC hooks and scripts

1. **Product truth.** Trace numerical, comparison, performance and personal-use
   claims to supplied evidence. No invented trial duration, testimonial, saving
   or demonstrated result. Missing facts allow a truthful demonstration angle.
2. **Audience objection.** The hook addresses the supplied concern using a
   supported feature or proposed demonstration, not unrelated hype.
3. **Distinct angles.** Requested alternatives differ in persuasive mechanism
   or objection addressed; synonym swaps alone do not make distinct concepts.
4. **CTA fidelity.** Preserve the supplied offer and destination. Do not invent
   a discount, guarantee, scarcity claim or purchase experience.
5. **Mode respects scope.** Hooks/scripts can be completed without generating
   assets. Hypothetical actors are not evidence of real customer experiences.
