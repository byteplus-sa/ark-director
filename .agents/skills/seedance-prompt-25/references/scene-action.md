# Scene Action

Focused reference for `seedance-prompt-25`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Scene staging](#scene-staging)
- [Action description](#action-description)
- [Counts, hands and surfaces](#counts-hands-and-surfaces)
- [Progressive change](#progressive-change)

## Scene staging

Use consecutive stages when they clarify the story. A shot or stage may contain
several readable ordered actions or reveals, or a sustained state. Describe the
critical action, its causal order and the perceptual outcome; do not split an
exchange merely to give every event its own stage. Deliberate stillness, waiting
and listening may end unchanged. Preserve the requested rhythm and reveal timing.

A clip that cuts uses shots rather than stages; see
[Shot Staging](shot-staging.md). Stages suit a continuous take or a story that
changes state without changing camera setup.

**Generate per scene at its natural duration (4–30s), not per 30-second block.**
Right-size each scene using the `duration` parameter — 7s for a single beat,
12s for a short dialogue exchange, 20s for a multi-stage action sequence. Do
not pad scenes to fill 30s. Chain approved scenes via `return_last_frame` /
`first_frame` and assemble in post. Add a shared reference bundle only when
the selected live tool/model explicitly supports mixed frame/reference roles;
a chaining recipe never overrides input compatibility.

```
[Generation Goal]
Generate a <video type>. The central subject is <subject>, and the primary event is <story summary>.

[Stage 1]
Initial state: <initial state of characters, props, and scene>.
Action: <critical ordered actions, reveal, or sustained state>.
Camera and light: <size, angle, move, and light source for this stage>.
End state: <character positions, prop ownership, or visible scene state>.

[Stage 2]
Continue from the previous stage: <state that must remain unchanged>.
Action: <critical ordered actions, reveal, or sustained state>.
Camera and light: <size, angle, move, and light source for this stage>.
End state: <observable state>.

[Stage 3]
Primary event: <closing event>.
Camera and light: <size, angle, move, and light source for this stage>.
End state: <final visible state>.

[Maintain Consistency]
Keep <character identity, number of characters, clothing, prop ownership, spatial direction,
and audio relationships> consistent.
```

### When to use 30s single-pass or native extension (exception)

Native extension (up to 180s, beta) and full 30s single-pass are the **exception**,
not the default. Use them only when you explicitly need continuous, seamless
motion across what would otherwise be scene boundaries:

- **Single continuous take** — a one-shot with no cuts where seamless motion
  across 30s+ matters more than per-scene iteration control.
- **Minimal scene variation** — same location, same characters, gradual change
  that the model handles well in one pass.
- **Audio-driven long dialogue** — one long dialogue block where lip-sync must
  be continuous across scene boundaries; extension keeps it seamless.

If using extension: generate a 30s base take, then extend it forward/backward
in rounds — **do not force scene changes at every 30s mark**; scene changes
happen naturally where the story needs them.

- **Audio with extension (only when separate lip-sync audio is requested).**
  Align a single Seed Audio master to the full timeline
  (up to ~2 min) and pass it as `reference_audio` so dialogue and sound stay
  continuous across the extension.
- **Validate seams.** Extension boundaries are not pixel-identical; inspect the
  boundary image, motion trend, and audio continuity on both sides of each seam.
  Multi-round extension is beta — validate each seam before committing.
- **Aspect ratio** is locked to the input video's ratio for extended segments.

### Timestamps and pacing

Use stages by default for a continuous take, and shots when the clip cuts (see
[Shot Staging](shot-staging.md)). Use one-second precision **only** for critical handoffs,
entrances/exits, transitions, or explicit beats.

| Pattern | Example |
|---|---|
| Time range | `0-3 seconds... 3-7 seconds... 7-12 seconds...` |
| Exact time point | `At 5 seconds, the camera whip-pans rapidly to the left.` |
| Relative timing | `Three seconds after the character presses the button, the lights dim.` |

Rules:
- Time ranges must be **consecutive and non-overlapping**.
- They are a **time budget**, not a precise edit point — actions may occur slightly before or after a boundary.
- Too little content gives the model too much freedom; too much causes excessive cutting or omitted events.
- Assess action frequency by travel distance, amplitude, contact, balance,
  recovery and required readability, not count alone. Three small finger taps
  in one second may be plausible; a sequence requiring incompatible positions
  or more travel/recovery time than available is a concrete conflict.
  Preserve source-requested actions and timing; return demonstrated conflicts
  before retiming or splitting. Without sufficient motion or playback evidence,
  feasibility or readability remains unverified, not failed by a numeric cap.

## Action description

The Subject and Action slots identify who or what matters and what the audience
must perceive. Describe critical action or sustained attention concretely; leave
incidental execution open. "She enters the lab" may be sufficient when entry is
all that matters. Specify the hand, contact or gaze when it carries the beat.

- **Relevant physical detail.** Name body parts, range, speed or force only
  when needed to communicate the critical action.
- **Physics grounding.** Clarify weight, balance, contact, momentum and recovery
  where they determine continuity or feasibility, not as an exhaustive checklist.
- **Intent-led body energy.** Speed, amplitude, interruptions and recovery
  follow the approved intention and action. Preserve urgent reaches, abrupt
  withdrawals, excited interruptions and sustained stillness when supplied.
  Ground acceleration, contact, balance and recovery in plausible physics;
  do not soften the body merely because the camera moves or dialogue is present.
- **No universal burst cap.** Multiple bursts may carry one coherent action.
  Slow motion or a single burst with holds is an optional selected pattern or
  a remedy for a demonstrated failure, not a general acceptance condition.
  Preserve locked timing and actions; return conflicts before retiming or
  splitting. Actor energy, camera energy and edit rhythm are separate choices.
- **Describe transitions between actions** for continuity: "use the inertia of
  turning around to naturally raise a hand."
- **Externalize emotions as physical detail**, never bare emotion labels. Use
  the [Emotional direction](audio-performance-camera.md#emotional-direction) cues below.
- **Stay inside the stage budget.** Preserve readable ordered actions and
  sustained attention; return concrete timing conflicts rather than imposing
  a per-stage event count.

### Selective motion grammar

When intended movement is underspecified, use the relevant motion grammar
below for subjects, props, effects, light or background. Describe only the
axes needed for readability; intentional stillness needs no invented motion,
loop or light change. A missing motion term alone does not prove a failed take:

| Axis | Question to answer |
|---|---|
| **Motion type** | translate / rotate / scale / parallax / drift / float-bob / pulse / flicker / color-cycle / twinkle / shimmer / sway / wave / slide / zoom / rotation |
| **Direction** | up/down, left/right, toward/away, clockwise/counterclockwise, along what axis |
| **Speed** | slow / medium / fast, or a frequency (e.g. "~0.5Hz sway") |
| **Amplitude** | how far ("~5% of body height", "full spectrum cycle") |
| **Easing** | constant / sinusoidal / accelerating / smooth |
| **Loop period** | only for intended repetition; how often it repeats ("~2s per cycle") |

Separate subject motion from the planned camera path or hold. Specify light or
color motion and its rate only when the effect needs it. An organic one-off
movement needs no easing curve, numeric amplitude or loop period.

Optional repeating-effect example: instead of "the neon figure floats, a rainbow beam shines from its
head", write "the featureless neon figure floats with a gentle up-down bob
(~0.5Hz sine, ~5% of body height) in a leaning pose, while a fan-shaped rainbow
beam projects from its head with the color bands continuously scrolling along
the beam (~1s full-spectrum cycle) and the background stars twinkle randomly."

## Counts, hands and surfaces

These three failures recur across takes and are cheap to prevent in text.

**Counts** (`prompt.exact_counts`). Track total identity separately from the
visible count. Name counted items by identity, size or position; account for
hidden, off-screen, entering, exiting and occluded subjects where relevant.
Restate counts and positions after relevant changes, without requiring all
subjects in frame one. Preserve deliberate reveals. Flag contradictory totals,
unexplained duplication or incompatible positions, not concealment itself.

```text
Three ceramic cups stand in a row on the counter from the first frame: small at
frame-left, medium in the center, large at frame-right. She lifts only the
medium cup; the small and large cups stay where they are. Three cups in total
throughout.
```

For a reveal: three people total; two visible at the table, the third hidden
behind the closed door until it opens. The same third person enters, making
three visible; the reveal does not create a fourth identity.

**Hands** (`prompt.hand_frame_side`). The model reads left and right as the
character's own side, so a bare "left hand" is often mirrored. Name anatomy and
frame side together: "her right hand, frame-left". When the character faces
away from the camera the two sides agree; say so anyway.

**Surfaces** (`video.text_free`). Generic tubes, jars, jugs, hard-shell cases,
garment neck labels, tickets and generated screens grow invented lettering.
Describe a recurring non-sheet prop positively as plain ("a plain white ceramic
jug, smooth solid surface, nothing printed"), leave it out, or give a story prop
a reference sheet with its real markings. Exact copy is a post layer.

## Progressive change

A change that spreads across the body or frame over time (an outfit changing
only on the part of the body that has crossed a line) is staged by timestamp
and body part in a pure reference-to-video prompt, never as an instant swap or
an image-edited first frame. The working recipe and the wordings that failed
live in `seedance-pacing-presets` (Progressive change); compose with it.
