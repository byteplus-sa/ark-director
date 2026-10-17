# Seedance 2.5 Checklist

Source skill: `seedance-prompt-25`. Apply the universal items in
[the index](review-checklists.md#universal--all-prompts) first, then this file.
For an edit, swap, recast or restyle use [Seedance edits](checklist-seedance-edits.md)
instead of the generation-only items below. Default severity is MAJOR; an item
states CRITICAL or MINOR when it differs.

## Request and parameters

1. **Draft first and promotion (`seedance.draft_promotion`).** An initial or
   revised draft is `draft: true` at 480p (or an explicit `resolution: "480p"`
   where native Draft is unavailable), unless a recorded user override or
   verified operation constraint applies. A final is promoted with
   `draft_task_id` from a passing, hash-bound draft selection under the
   project's approval mode, and carries only output settings (resolution,
   watermark, return_last_frame, expiry, priority). A final call that also
   sends prompt, references, duration, ratio, audio or task type is CRITICAL:
   those are reused from the draft and any change must happen before the
   draft. Without native Draft support the final is a new reviewed request with
   its own registry entry. Multi-shot work also needs a reviewed draft assembly
   and picture/audio decisions. Final outputs need fresh playback and audio QA:
   the final soundtrack is not byte-identical to the draft's. Prompt-only work
   needs no generated draft.

2. **Audio route (`audio.native_route`).** With `generate_audio: true` the
   model voices what the prompt implies, and a negative line such as "no music,
   no spoken words" often fails (speech, chants and score have leaked into most
   ambient-only takes). An ambience-only, score-driven or speech-free piece uses
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
   contact — not as bare verbs. High-burst actions appear only when the shot or
   energy level requires them.

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

13. **No storyboard or board binding (`references.no_board_binding`).** A
    storyboard grid, board or board panel is never bound to a Seedance request:
    its panel numbers and sketch or watercolour medium leak into the video and
    output-copyright rejections rise. Its staging goes into the prompt text and
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

17. **Shot density.** A spot is built from short sequences of 2-3 shots with
    one action per shot (a 30 s spot as about six 5 s sequences), not one pass
    of many beats. A 30 s single pass with nine or more beats, or a single-setup
    clip with no stated camera move, reads as stock footage (MAJOR). About 7
    shots per clip at most, none shorter than about 0.8 s; shorter cuts merge.
    Each shot or stage has one primary state change and a clear end state.

18. **Neighbor contrast and angle range (`shot.variety`).** Adjacent shots
    differ in at least two of size family, angle class, camera move and key
    side. The scene has a non-eye-level shot, moving shots at its energy level,
    uneven shot lengths and one turn shot, or a recorded reason. A continuous
    take shows a motivated camera path, a named light at each stage and a
    distinct payoff. MAJOR when the clip repeats one framing, MINOR when one
    dimension is thin.

19. **Light sources declared (`shot.plan_bound`).** One set of declared sources
    across the scene's cuts; a new source has a motivating event. A light that
    changes inside a shot is a timed cue on a declared source ("at 3.2 s the
    overhead lamp clicks off"); timed cues are honoured closely, vague ones
    drift. No silhouette on a shot with spoken lines.

20. **Axis carried (`shot.axis_carry`).** Each confirmed camera, lens, lighting,
    pacing or energy axis appears on a named shot, or the scene records an
    override with its reason. `proposed` and `defaulted` axes may change freely.

21. **Static locks carry a reason (`shot.plan_bound`).** "Locked-off" or "no
    camera movement" appears with a recorded `static_reason`, not as
    boilerplate. A scene has at most one `performance_hold` and one
    `contrast_hold`; a `contrast_hold` follows a moving shot; in a scene of four
    or more shots, one reason on more than a third of the shots is MAJOR.
    Quiet moves are fine during a spoken line; large moves there are MINOR.

22. **Post-only effects stay in the edit (`shot.plan_bound`).** Blink cuts,
    intercuts and vision flashes shorter than about 0.8 s are assembly cuts,
    never requested inside one prompt; asking the model to skip an action it
    describes is MAJOR. A rack focus that leaves the subject soft ("focus left
    behind", subject sharp to background) mostly fails because the model keeps
    the face sharp: plan the defocus in post (MINOR). A sudden burst action
    appears at most once per shot with a still hold before and after (MINOR).

23. **Camera direction coherent.** One primary move plus at most one secondary
    per shot, each with subject, start and end; no competing simultaneous
    moves; a requested static camera is preserved. Uncommon terms follow Term +
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
    body part, slow enough that the crossing lasts about 1.5 s, with the motion
    continuing unbroken and no glow, flash, sparkle, dissolve or particle
    effect. Wording that makes it instantaneous ("swaps at the pole", "changes
    in place", "the pole is the boundary", a bare wipe) is MAJOR. It is pure
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

33. **Speech budget (`dialogue.speech_budget`).** Lines start 0.5-1.5 s late,
    later after long pre-line action, and speech tends to fill to the clip end.
    Each shot or stage that holds a line lasts at least spoken words / 2.2 +
    1 s; the last line ends at least 0.4 s before the clip end; the final 3 s
    hold at most two state changes. Opening hook words are short and ASR-clean.
    A script far shorter than the duration directs the gap (pauses, beats). An
    over-budget line is MAJOR; trimming the clip head does not lengthen the
    tail.

34. **Same dialogue in both prompts.** When separate audio is in scope, the Seed
    Audio text matches the `{}` text exactly: no paraphrase, reorder or omission.

## Emotion, motion and space

35. **Visible or audible cues.** Abstract emotions are paired with 2-4 readable
    cues (eyes, brows, mouth, breathing, gaze, hands) grounded in the tactic and
    framing; masked wide shots use posture, spacing or hand action. Bare labels
    such as "very sad" fail.

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
