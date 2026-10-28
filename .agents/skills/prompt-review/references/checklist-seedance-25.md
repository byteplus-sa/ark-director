# Seedance 2.5 Checklist

Source skill: `seedance-prompt-25`. Apply the universal items in
[the index](review-checklists.md#universal--all-prompts) first, then this file.
For an edit, swap, recast or restyle use [Seedance edits](checklist-seedance-edits.md)
instead of the generation-only items below. Default severity is MAJOR; an item
states CRITICAL or MINOR when it differs.

## Request and parameters

1. **Draft first and promotion (`seedance.draft_promotion`).** Every new 2.5
   generation, including edits, extensions, probes and variants, uses boolean
   `draft: true` and explicit `resolution: "480p"` in every review mode, with
   no skip-draft override. Resolve conflicting capability evidence or transport before
   submission; never drop `draft` or fall back to plain 480p. A final is promoted with
   `draft_task_id` from a passing, hash-bound draft selection under the
   project's approval mode, and carries only output settings (resolution,
   watermark, return_last_frame, expiry, priority). A final call that also
   sends prompt, references, duration, ratio, audio or task type is CRITICAL:
   those are reused from the draft and any change must happen before the
   draft. Other models without native Draft use ordinary 480p tests and a new
   reviewed final request with its own registry entry. Multi-shot work also needs a reviewed draft assembly
   and picture/audio decisions. Final outputs need fresh playback and audio QA:
   the final soundtrack is not byte-identical to the draft's. Prompt-only work
   needs no generated draft.

2. **Audio route (`audio.native_route`).** With `generate_audio: true` the
   model voices what the prompt implies, and a negative line such as "no music,
   no spoken words" does not reliably hold (speech, chants and score can leak
   in). An ambience-only, score-driven or speech-free piece uses
   `generate_audio: false` (or keeps the provider master untouched) and gets its
   bed from Seed Audio in post, recorded as not frame-synced. A prompt that
   relies on a negative audio line for one of these pieces is MAJOR.

3. **Reference count limits.** ≤ 30 images, ≤ 10 videos, ≤ 10 audio, ≤ 50 in
   total; recommended 1-8 image subjects, 1-5 video subjects (5-10 s each), only
   directly relevant audio. Exceeding a hard limit is CRITICAL.

## Formula

4. **Subject + Action present.** The prompt contains at minimum a clear subject
   and a primary action or event. These are the only grammar-required parts;
   camera and light are craft-required for narrative shots (Shot plan items).

5. **Six-part order.** Subject + Action/Event + Scene/Environment + Visual Style +
   Camera Movement/Cut + Audio, in this order when present (MINOR).

6. **Action granularity.** The Action slot describes motion at the body-part
   level with range, speed and force, grounded in weight, balance, momentum and
   contact, interruptions and recovery, following approved intent. There is
   no slow-body default or universal burst cap. Optional single-burst holds
   serve a selected pattern or demonstrated failure and cannot erase locked
   action. Actor energy, camera energy and edit rhythm are separate choices.

## References

7. **Material mapping in prompt (`references.ordered_bindings`).** Every
   reference is mapped in the prompt text; the model never guesses which asset
   belongs to which person, prop or scene. Each subject is bound individually —
   "@Images 1 through 4 define four characters" fails. Each reference states
   what to use from it and, where leakage is possible, what not to take.

8. **Organized and selected by scene.** Large bundles are grouped by type with a
   centralized profile for important subjects, and each scene names only the
   references it uses (MINOR when a small bundle is clear without grouping).

9. **Exclusions only where leakage is possible.** "Do not use..." appears for a
   plausible leak (people in a location plate, a background in a prop photo),
   not as a negative-prompt dump (MINOR).

10. **Multiple views.** Several images of one subject state that the output
    contains only one of it throughout.

11. **Video reference inheritance.** When a reference video defines motion, the
    prompt names only the attributes to inherit and does not restate every
    source action.

12. **Control-only references (`references.control_only`).** Route maps,
    blocking diagrams and timing charts are translated to text and omitted.
    Intentional conditioning needs a mode-authorized selection, current hashes,
    supported tool/mode inputs and leakage QA; labels alone grant nothing.

13. **No storyboard or board binding (`board.animatic_review_only`).** A
    storyboard grid, board or board panel is never bound to a Seedance request:
    its panel numbers and sketch or watercolour medium can leak into the video.
    Its staging goes into the prompt text and
    identity comes from element references. A bound board is CRITICAL. A first
    or last frame must be a clean, full-frame keyframe in the final medium with
    no marks. Blocking maps and other control diagrams are judged under item 12.

14. **Reference photos outrank text.** Where text and a bound photo disagree on
    a detail (gear down in the photo, retracted in the text), the photo wins;
    the prompt aligns with the reference or the reference is replaced.

15. **People in video and face inputs (`model.supported_mode`).** An extension
    or video input that shows generated or real people binds them as
    `asset://` Virtual Portrait assets; a raw clip with people is rejected
    (CRITICAL). Real-person photos without an authorized asset are CRITICAL.
    A `reference_image` face or body crop may be rejected — use the full sheet
    or a first frame. A last-frame-only request is rejected; use first + last.

## Shot plan and structure

16. **Shot plan bound (`shot.plan_bound`).** A narrative, ad, micro-drama,
    music-video or showcase shot carries a recorded shot plan: per shot,
    duration, size, angle, camera move (or a recorded `static_reason`), lens
    intent as a visible result, and a declared light source with its key side
    relative to the lens. "Cinematic lighting" or "soft fill" alone is not a
    light fact. An exempt format (the exemption list in the rule catalog)
    records its exemption; the caller omits the `shot.*` rules and the reviewer
    reports `not_applicable` with that exemption. A missing plan without an
    exemption is MAJOR.

17. **Shot density.** Derive sequence lengths and shot counts from intended
    perception, action and supported generation limits. Short multi-shot
    sequences are optional, with no fixed cadence or `wow` image quota.
    Inspect overloaded coverage against the supplied intent;
    a single setup or intentional stillness is not itself a defect. About 7
    shots per clip and about 0.8 s per shot are provisional cautions, not provider
    limits or guaranteed failure thresholds. Preserve requested timing; offer
    assembly or split source clips as optional remedies for precision or
    demonstrated failure, and return conflicts with locked timing or workflow.
    Each shot or stage has one primary state change and a clear end state.

18. **Intent-led coverage (`shot.variety`).** Neighbor contrast, angle range,
    motion ratios and uneven timing are optional craft aids, not quotas.
    Compare coverage with the confirmed script, medium and performance plan.
    A continuous take may hold its framing and light with a recorded rationale.
    Do not manufacture a turn, cut, move or light change to pass a count.
    A contradiction of a critical locked beat is MAJOR; repetition alone is not.

19. **Light sources declared (`shot.plan_bound`).** One set of declared sources
    across the scene's cuts; a new source has a motivating event. A light that
    changes inside a shot is a timed cue on a declared source ("at 3.2 s the
    overhead lamp clicks off"); timed cues are honoured closely, vague ones
    drift. Silhouette during speech is valid when facial evidence is not
    required; otherwise verify the required face and lip readability.

20. **Axis carried (`shot.axis_carry`).** Each confirmed camera, lens, lighting,
    pacing or energy axis appears on a named shot, or the scene records an
    override with its reason. `proposed` and `defaulted` axes may change freely.

21. **Static locks carry a reason (`shot.plan_bound`).** "Locked-off" or "no
    camera movement" appears with a recorded `static_reason`, not as
    boilerplate. Repeated `performance_hold` choices and a wholly held scene
    are valid when intentional. A `contrast_hold` follows a moving shot, but
    stillness needs no preceding move when it serves performance directly.
    Spoken dialogue does not exclude kinetic coverage. Check required delivery
    and performance readability at the planned framing and speed; movement
    size alone is not a finding.

22. **Selected post effects stay in the edit (`shot.plan_bound`).** Assembly
    is an optional remedy for precise blink cuts, intercuts and vision flashes,
    not a mandatory response to a sub-0.8 s shot. Preserve the requested
    ellipsis; a prompt requiring the missing action to be shown conflicts with it.
    Return incompatible locks rather than silently substituting assembly.
    A rack focus that leaves the subject soft ("focus left
    behind", subject sharp to background) mostly fails because the model keeps
    the face sharp: plan the defocus in post (MINOR). Burst count alone is not
    a finding; inspect plausible contact, continuity and recovery under item 6.

23. **Camera direction coherent.** One primary move plus at most one secondary
    is a planning heuristic. Preserve explicitly requested coherent choreography
    with subjects, paths, timing and start/end states; flag competing simultaneous
    directions or unreadable required action, not move count alone. A requested
    static camera is preserved. Uncommon terms follow Term +
    Target Subject + Visual Change + Foreground/Background + Direction or Speed.

24. **Timestamps.** Ranges are consecutive and non-overlapping, treated as a
    time budget, and never demand impossible densities ("three actions in one
    second"). The last stage ends at the requested duration.

25. **Natural duration.** Each scene runs at its natural length (4-30 s); a 30 s
    single pass or native extension is a recorded exception.

## Craft guards

26. **Exact counts (`prompt.exact_counts`).** Counted items, clones, runners,
    crowds and repeated props carry an exact number; each item is named by size
    or position and is in open view from the first frame; the count and
    positions are restated at every stage and every other item's place is
    stated. A prompt that mentions extra copies lying around, or a count only
    in the opening, is MAJOR: counts drop and duplicate.

27. **Hands and sides (`prompt.hand_frame_side`).** The model reads left/right
    as the character's own side, so mirrored hands are common. Every
    handedness or side cue names both anatomy and frame side ("her right hand,
    frame-left"). A bare "left hand" on a hero action is MAJOR; on a background
    detail MINOR.

28. **Text-free frames (`video.text_free`).** No captions, subtitles (`【】`
    included), titles, taglines, CTAs, logos, end cards or "AI-generated"
    labels are requested in the footage; they are added in post. Recurring
    generic props and generated surfaces (tubes, jars, jugs, hard-shell cases,
    garment neck labels, tickets, generated screens) are described as plain
    ("plain white ceramic jug, smooth solid surface, nothing printed") or left
    out; a story prop with markings has a reference sheet. An unqualified
    generic container in a hero shot is MAJOR because the model invents
    lettering on it.

29. **Progressive or partial change.** A change that crosses the body or frame
    over time (an outfit changing only past a line) is staged by timestamp and
    body part or region within the requested timing, with motion continuing
    unbroken. About 1.5 s for a crossing and 0.4 s between stages are provisional
    examples, not provider limits; slowing or spreading stages is an optional
    remedy for demonstrated unreadability, never an automatic rewrite.
    Preserve requested speed, stride and effect exclusions. Return real conflicts
    with locked timing; without playback, readability remains unverified.
    Wording that contradicts a requested progression by making it instantaneous ("swaps at the doorway",
    "changes in place", "the doorway is the boundary", a bare wipe) is MAJOR. It is pure
    reference-to-video; an I2I-edited first frame recomposes the scene (MAJOR).

30. **Known drift points (MINOR).** Hair covered by a shawl, blanket or high
    collar states its length falling over the garment. Night states black sky,
    low exposure and a small pale moon positively. Rounded black side bars are
    an output-QA check at the frame edges. Character count, clothing, prop
    ownership and spatial relationships stay consistent across shots.

## Audio and dialogue

31. **Bracket syntax.** Dialogue in `{}`, music in `()`, SFX in `<>`. `【】`
    subtitles fail item 28.

32. **Dialogue language reinforcement.** Non-Chinese dialogue states Dialogue
    Language + Regional Variety/Accent + Delivery Style + Speaker + `{line}`.
    Every speaking character, including phone-screen voices and narrators, has
    a scripted line; unscripted speakers ad-lib.

33. **Speech budget (`dialogue.speech_budget`).** Use measured delivery or a
    native-language-informed read, including pauses, onset and tail. About
    2.2 words/s is an English planning estimate, not a universal gate. An onset
    allowance of 0.5-1.5 s and about 0.4 s of final tail are provisional planning
    margins, not minimums, to be checked against the actual take. Preserve requested language
    and locked text; propose retiming or splitting before authorized rewrites.
    A demonstrated duration conflict is MAJOR; an English word-count estimate
    alone cannot establish one. Without delivery evidence, timing is provisional.
    Direct unused gaps. Two state changes in the final 3 s is a provisional
    caution, not an artistic gate; assess the approved ending's readability.
    Numeric onset, tail or density alone cannot establish failure; missing
    playback remains unresolved. Trimming the clip head does not lengthen the tail.

34. **Same dialogue in both prompts.** When separate audio is in scope, the Seed
    Audio text matches the `{}` text exactly: no paraphrase, reorder or omission.

## Emotion, motion and space

35. **Performance handoff (`acting.plan_bound`).** For new or revised character
    performance, collect the source-bound plan or equivalent isolated-prompt
    input. Trace critical beat IDs to intention, trigger, registration,
    maintained/changed tactic and readable consequence. Relevant listeners
    have a task or intentional non-response. Missing material input is
    incomplete; dropping a critical beat or replacing it with a generic
    mood/gesture list is MAJOR. Cues fit framing, occlusion, scale and time.
    Two to four cues is a heuristic, not a minimum. Static assets and
    preservation-only edits record not_applicable with their concrete reason;
    source performance still needs preservation review.

    **Staged fights (`fight.readable_exchange`).** Trace authored or revised
    choreography through stable actors, start/end positions, apparent contact
    or avoidance, motivated reactions, occupied hands and prop transfers.
    Timing and crop must reveal required events. Missing continuity or an
    invisible required interaction is MAJOR; style cannot change the locked
    outcome. Non-fights and preservation-only edits record their scope reason.

36. **Motion grammar.** Each moving element in stylized or reverse-engineered
    takes states motion type, direction, speed, amplitude, easing and loop
    period; the camera is stated even when static; light and colour motion
    carry a rate ("~1 Hz shimmer").

37. **Spatial map.** Movement-heavy scenes state start, travel axis, subject
    order, boundary behavior, end and forbidden transitions, using physical
    locations rather than relative verbs, and repeat the invariants that matter
    in every shot or stage.

## Mode locks

38. **Auto-locked parameters.** Edit: ratio and duration unset (locked to the
    input). First/last frame: ratio follows the first image and both frames
    share it. Extension: ratio unset, duration settable, boundary image, motion
    trend and audio continuity checked.

39. **Other modes.** One-click video defines material roles, image order, motion
    amount, editing style and audio. Seamless transitions define both videos'
    roles, the trigger action, the transition process and the arrival state.
    Blockouts identify coarse, fine or video-lock and keep the blockout as the
    motion authority only.

## Revision diff

40. **No approved per-shot detail lost (`revision.declared_delta`).** When one
    shot changes, every other shot's approved wording (descriptors, motion
    rates, camera moves, light cues) carries over verbatim. Diff the new prompt
    against the prior snapshot; a silently dropped descriptor or rate is MAJOR.
