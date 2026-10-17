---
name: seedance-acting-console
description: >
  Turn a directing directive into a production-grade Seedance acting block.
  Two layers: (1) Scene-level acting analysis — read the whole scene, find the
  shared direction, each character's motive, goal, obstacle, and tactic with
  eye-work as purposeful action. (2) Cue encoding — map the tactic's visible
  footprint to directly observable physical cues at three intensity levels using
  a six-emotion bank. Use this skill when directing the performance, acting,
  emotional intensity, mood of the scene, facial expression, delivering a line,
  or when a character reads dead, glassy, flat, or over-acted. Composes with
  seedance-prompt-25 and optionally with seed-audio-prompt for dialogue
  reinforcement. Never calls generation tools itself.
---

# Seedance Acting Console

Turn a single creative directive into a complete, generation-ready performance
spec. The console has two layers that work in sequence:

1. **Analysis layer** — Read the whole scene, find the shared direction, then
   derive each character's motive, goal, obstacle, and tactic. The emotion is
   a byproduct of the tactic — never the starting point.
2. **Encoding layer** — Map the tactic's visible footprint to directly
   observable physical cues at three intensity levels. The six-emotion bank is
   a lookup table for encoding, not a menu to pick from.

This skill is **prompt-composition only**. It never calls MCP/Ark generation
tools directly; it composes with `seedance-prompt-25` (prompt grammar) and
optionally with `seed-audio-prompt` (Seed Audio voice profiles).

---

## Analysis layer

### Core principle

An acting task is when the character is **INVESTED in their tactic of reaching
the goal.**

- It is NOT a description of external behavior ("eyes flick," "brows lift," "he
  looks sad") — that is playing the result, and it produces dead faces.
- It is NOT necessarily physical action. The tactic can live entirely **in the
  eyes**: a different look when someone humiliates vs. begs; a person arguing
  from conviction constantly checks BOTH eyes of the partner, hunting for a
  sparkle of trust, registering whether the partner is interested or drifting —
  and adjusts to what they find.
- The eye movement IS the doing. Aliveness = the mind visibly working on the
  task, moment to moment.
- Never fix dead eyes with lighting tricks (catchlights etc.). Fix them by
  giving the eyes a task.

### The ladder (work strictly in this order)

#### 0. Read the WHOLE scene dialogue first

Never build a task from one line. The task lives across the entire exchange —
where it holds, where it breaks. Check every line of every character before
directing any of them.

#### 1. Goal of the SCENE — one shared direction

The scene has ONE goal: a single direction ALL characters play toward, usually
unspoken — a mutual silent agreement about how this time will be lived.

Example (mother packs son's suitcase, army in an hour): the goal of the scene
is **make it painless — hide the feeling, don't leave each other with pain or
sorrow, never lose the positiveness.** It belongs to both at once.

The scene goal is NOT the film's dramaturgic function (the reveal, the theme).
Characters never know or play the film's purposes — those are accomplished
THROUGH them, as a byproduct.

#### 1a. The ENDING names the event

Always look at how the scene ENDS before naming its event. The last line/beat
is the key you read the whole scene backward through. Watch for the
double-meaning last line — spoken about one thing, meant about another ("Poor
bastard. Just can't forgive himself" — said looking at the patient, meant about
himself).

#### 1b. ALL in one event

The event must contain EVERY character in the scene — including silent or
unconscious ones — as participants or mirrors of the same process. If a
character stands outside the named event, the event is named wrong.

#### 1c. The PHYSICAL ACTION is the channel

The surface activity of the scene (the "terrain" — e.g., routine rounds;
packing a suitcase) stays as the PHYSICAL ACTION, and each character pursues
the event THROUGH it — each via their own distinct, visible physical behavior.
The invisible task must have a physical channel the camera can read.

Rule: give every character in the scene their own physical channel for the same
event — different behaviors, one event, one terrain.

#### 2. Each character's MOTIVE — different fuel, same direction

Every character pushes along the same scene direction, but each **for their own
reason**. The son keeps it painless *for mom*; the mother *out of superstition*
(no tears before a journey — bad omen). Same vector, different fuel — the fuel
is what makes each performance distinct while the scene reads unified.

Motives can be alternative hypotheses; the director picks. Given circumstances
constrain motives: a man who took the job at an experimental convict lab is
ALREADY compromised — he cannot play a moral innocent.

#### 3. Each character's GOAL — the personal fight

Born from the motive: what this person is fighting for themselves inside the
scene. Ordinary, personal, playable. Never the same words as the scene goal,
never the theme.

#### 4. OBSTACLE — what presses against the direction

The thing threatening to break the scene's line (the real feeling pressing to
surface; the case too horrifying to stay routine). One crack and the shared goal
collapses. This pressure is what the audience actually feels — precisely because
nobody plays it; everyone plays keeping it out.

#### 5. TACTIC — the acting task proper

The invested, moment-to-moment pursuit, written as what the character is DOING
to the partner — with the eye-work named as purposeful action:

- checking both of the partner's eyes for a sparkle of trust
- registering after each point: did it land? interested or about to smirk?
- stealing looks and snapping back before being caught
- measuring the partner, memorizing them, comparing what I feel with what they
  show

Beats are keyed to the actual dialogue words. Where the script demands it, mark
the point where a character's fuel runs out and the line breaks (the medic's
"...Poor bastard," under his breath — the break IS the delivery of the scene).

### Contrast pairing (build duos on mirrored +/-)

A two-character scene is richer when the pair is built on CONTRAST — each
character carries a plus and a minus, mirrored against the other, with one axis
being the essential one the audience reads.

Rules:
- Each character gets one + and one −, inverted relative to the partner.
- Name the ESSENTIAL AXIS of the scene — that opposition is what the audience
  actually reads; the other traits are the color.
- Both still push the same scene direction — the contrast lives UNDER the shared
  direction and leaks out through the tactics and the eyes.
- The seeming trait is often scar tissue over its opposite: "careless" = hope
  lost, not care absent. Direct the history, not the surface.

### Common analysis failures to catch

- Task built from one line instead of the whole dialogue → re-read the scene
  first.
- The film's reveal/theme assigned to a character as their task → characters
  never play the film's purposes.
- Scene goal confused with character goal → scene goal is the shared direction;
  character goals are personal and differ.
- Motive ignores given circumstances (playing innocence while already
  complicit) → re-derive motive.
- Prescribed eye/face choreography instead of eye-work as purposeful action →
  rewrite as verbs at the partner.
- Emotion adjectives as direction → replace with the task that produces the
  emotion.

---

## Encoding layer

The analysis layer determines *what the character is doing*. The encoding layer
translates that into *what the model needs to render*. The cues are derived from
the **tactic**, not the emotion label — instead of "character is angry →
clenched fists" (playing the result), it becomes "character is checking the
partner's eyes for trust after being humiliated — jaw tightens, eyes sharpen,
breathing controlled" (the cues come from what the character is doing, not what
they're feeling).

### Framing and evidence

The playable tactic and its visible evidence are separate. Give the character
something to accomplish with the partner; then encode **2–4 relevant cues per
transition** that the chosen framing can actually show. Facial cues are allowed
as consequences of that tactic, not a substitute for it or an arbitrary sequence
of eyebrow and mouth movements. The cue budget is a craft heuristic, not a model
limit. Fewer cues are appropriate when the brief asks for minimal action.

- **Close-up:** a purposeful gaze adjustment, a held reply, jaw release or a
  small change in breath can carry the tactic. No mandatory brow/mouth pair.
- **Medium/wide:** prioritize distance, weight, orientation, hand use and the
  ongoing physical task. Do not rely on pupils or mouth corners at unreadable scale.
  Check each cue against the actual camera side, occlusion and subject size: a
  rear hand closing against a thigh may be hidden or too small even though it is
  a body cue. Prefer a readable weight shift, silhouette change or spatial action
  when a subtle hand cue cannot be seen; preserve the requested shot and restraint.
- **Face obscured/back view:** use posture, hands, pace, proximity or audible
  delivery if audio is requested. Preserve the framing; do not uncover the face
  merely to satisfy an eye-work template.

Name a hand, arm or foot by anatomy and frame side together ("her right hand,
frame-left"): the model reads "left" and "right" as the character's own side, so
a bare side flips in mirrored or facing shots.

Keep motive and goal stable when comparing framings; translate their evidence.
For revision diagnosis, load [hypothetical acting repairs](references/acting-repairs.md)
only when a performance is stiff, overstated or unreadable.

### Emotion bank

Six emotions, each externalized as **directly visible or audible cues** at three
intensity levels. Intensity is never encoded with degree adjectives ("very
sad", "extremely angry") — it is encoded purely through graduated cues: number
of cue channels engaged, amplitude, movement degree, and vocal delivery.

| Emotion | Abstract one-liner | Intensity 1 (low) | Intensity 2 (medium) | Intensity 3 (high) | Seed Audio delivery hint |
|---|---|---|---|---|---|
| **Serenity** | A settled, unhurried inner calm with no internal conflict. | Gaze soft and level; breathing slow and even; corners of the mouth at rest. | Eyes half-lidded, brows relaxed; slow, deep breaths; hands loosely folded or open palms. | Shoulders fully dropped; a slow exhale with eyes briefly closed; a subtle, contented smile. | Calm, measured; slow, soft, unhurried. |
| **Joy** | Bright, open, expansive happiness that lifts the body and face. | The corner of the mouth lifts faintly; the eyes soften. | An uncontrollable smile; brows relax; steps become light. | Laughing, spinning in place, breathless; eyes crinkled. | Bright, warm; light and quickening, occasionally breaking into laughter. |
| **Terror** | Overwhelming dread that triggers the freeze response. Built from gaze fixed, brows lowered, tense stillness plus panic respiratory signs. | Gaze fixed; pupils widen; a visible swallow; breathing turns shallow. | Eyes widen fully; brows raised and rigid; chest heaves; hands freeze mid-motion. | Frozen stillness; mouth slightly open; body tensed; a choked, sharp intake of breath. | Thin, breathy; shaky, rapid, strained. |
| **Rage** | Hot, escalating anger pressing outward at a target. | Jawline tense; eyes sharp; nostrils flare slightly. | Both fists clenched; chest heaving; eyes sharp; jaw working. | Veins at the temple; trembling fists; shouts with the voice cracking; whole body coiled. | Shouted, voice cracking; harsh, escalating, clipped. |
| **Fear** | Anxious apprehension and watchfulness about a perceived danger. | Eyes darting; fingers tapping; weight shifting; frequent glancing. | Rapid breathing; eyes darting; biting the lip; hands fidgeting. | Body pulled back; shoulders hunched; gaze searching; voice cracking; quick shallow breaths. | Shaky, rapid; hesitant, tremulous, quickened. |
| **Vigilance** | Sharpened, controlled alertness scanning for threat or opportunity. Built from gaze fixed, brows lowered, tense stillness. | Gaze steady; brows level; posture still but ready. | Gaze fixed and scanning; brows lowered; body still; breathing held. | Utterly still; eyes narrow and unblinking; head slowly panning; hands ready at the sides. | Low, steady; measured, controlled, clipped. |

### Using the bank with the analysis

The bank is a **lookup table**, not a menu. After completing the analysis
ladder, identify which emotion family the tactic's visible footprint belongs
to, then select cues from the appropriate intensity level. Adapt the cues to
serve the tactic — the tactic determines which cues are relevant, not the other
way around.

Example: The analysis produces a tactic of "checking the partner's eyes for a
sparkle of trust after being humiliated." This lives in the **Fear** family at
intensity 2, but the cues are adapted: eyes darting becomes eyes deliberately
searching; biting the lip becomes jaw controlled to prevent a tremor. The
emotion label is a reference point; the tactic owns the cues.

### Intensity encoding guide

Intensity level is a **design-level encoding choice**, not a number the model
reads. Levels 1/2/3 differ on the same emotion through three graduated levers:

1. **Number of cue channels engaged** — one or two readable channels at level 1,
   stronger or broader readable channels at level 3 within the shot framing.
2. **Amplitude** — faint and contained (a flicker) vs pronounced (a shaking
   fist, tears streaming).
3. **Movement degree** — static containment (held breath, frozen stillness) vs
   full-body release (spinning, shouting, recoiling).
4. **Vocal delivery** — calm and measured, strained and quickened, or shouted /
   cracking.

Never write "very happy" or "extremely terrified" — replace the adjective with
more cues and more amplitude.

### Restraint and shape patterns

Load [restraint and shape patterns](references/restraint-and-shape.md) when a
tactic needs a precise shape: a **first sign** (one small cue as the earliest
consequence), a **suppression arc** (a visible feeling brought under control),
an **animal image** translated into body cues with at most one burst action
per shot, or **eyes through concealment** (a veil or mask that leaves only the
eyes to carry the tactic).

---

## Output grammar

### The ACTING TASK block

Format inside a Seedance prompt:

```
ACTING TASK — [NAME] (invested in their tactic through the visible physical channel):
SCENE DIRECTION (shared, unspoken): [one line]
MOTIVE (their fuel): [why THEY push that direction]
GOAL: [their personal fight]
OBSTACLE: [what presses against the line, what one crack costs]
TACTIC: [what they do to the partner; purposeful eye-work when readable,
otherwise the physical channel that carries the pursuit]
CUES: [2–4 consequences readable in this framing; use gaze or face when visible,
and posture, distance, hands or physical action when those carry the scene]
Moment to moment:
— "[dialogue words]" — [verb at the partner + readable response being checked]
— "[dialogue words]" — [verb + visible physical channel]
— [where the line breaks, if it breaks]
(Optional, only when eyes are visible and a frozen stare needs correction:
gaze checks the partner for a response; natural blink cadence.)
```

Rules:
- Verbs directed at the partner; no adjectives of emotion as instruction
  ("sadly," "nervously").
- Keep TACTIC playable and directed toward the partner. CUES may include brows,
  mouth or gaze when readable and caused by that tactic; do not dictate a
  mechanical face sequence unrelated to what the character is pursuing.
- Nobody plays the emotion; everyone plays the direction. The audience
  receives the feeling through the pressure.
- A short gaze correction is optional when eyes are readable and the actual
  brief or observed result calls for it. Omit it for masked, rear-view or distant
  shots; it is a craft intervention, not a universal model requirement.
- Every character in frame gets a readable task, including silent
  listeners; use eyes when visible and physical action when obscured: a listener's task is also real (e.g., "decide if they're serious,"
  "wait for the punchline," "protect the mood").

### Single emotional transition (one emotion, one change)

Use for a single emotional shift over the shot. Keep **2-4 observable cues**
for the transition — cue overload destabilizes the performance.

```
The overall emotion shifts from <starting emotion> to <ending emotion>.
After <triggering event>, <character> first shows <immediate observable reaction>.
Then, <the chosen framing-readable cue> gradually <changes>.
Finally, <character> expresses <target emotion> through <restrained or explicit outward behavior>.
```

### Multi-stage emotion (arc over time)

Use when the emotion changes several times, with trigger events. Add timestamps
only when requested or needed for verified audio alignment; ordered beats suffice
for untimed drafts.

```
When <character> hears or sees <first triggering event>, <first observable reaction>.
When <second triggering event> occurs, <change in expression, gaze, or breathing>.
After confirming <critical information>, the emotion that <character> tries to restrain
or conceal gradually becomes visible through <observable behavior>.
Finally, <character's final action, expression, or manner of speaking>.
```

### Dialogue, delivery, and language

When dialogue is set, place the exact line inside `{curly braces}` and give the
delivery style plus the dialogue language (non-Chinese dialogue needs the
language stated):

```
Dialogue language: <language>. <character> <says/shouts/whispers> in <delivery style>: {<exact line>}
```

Give each line room: native speech starts about 0.5-1.5 s after its cue and
runs at about 2.2 words per second, so a line needs a shot of at least
words / 2.2 + 1 s and should end at least 0.4 s before the clip does. The
Seedance 2.5 prompt skill owns the full dialogue timing rules; keep the
performance beats around a line inside that window.

### Worked example

Directive: A woman confronts a locked door. Her husband just left. Scene
direction: keep it together, don't break down. Tactic: checking the door for
signs he'll come back, eyes hunting for a reason. Emotion family: Fear at
intensity 2. Dialogue: "Get out of my way."

```
ACTING TASK — GLORIA (invested in checking whether he's really gone; the work
happens in her eyes):
SCENE DIRECTION (shared, unspoken): keep it together — don't let this be real yet.
MOTIVE (her fuel): superstition — if she doesn't break, he might still come back.
GOAL: find proof it's not over.
OBSTACLE: the locked door; the silence on the other side; the feeling pressing
to surface.
TACTIC: pressing the door, testing the handle, eyes hunting the frame for
anything he left behind — checking the threshold, the mat, the hallway.
CUES: gaze searches the threshold for a response; her right hand, frame-left,
tests the handle once; weight stays toward the door while her reply catches in
her breath.
Moment to moment:
— presses the handle — finds it locked — eyes snap to the gap under the door
— "Get out of my way." — said at the door, voice strained, eyes still searching
the frame
— the line breaks at "way" — she heard her own voice and it scared her
(Safety: gaze always engaged in the task; natural blink cadence.)
```

Dialogue language: American English. Gloria says in a sharp, strained voice
through gritted teeth: {Get out of my way.}

For the full scene prompt, drop this acting block into the six-part formula
(Subject + Action + Scene + Visual Style + Camera + Audio) as the subject/action
section, per `seedance-prompt-25`.

---

## Audio reinforcement (optional)

When the scene has spoken dialogue and the user wants lip-sync, generate the
Seed Audio dialogue track first and pass it as `reference_audio` to Seedance.
This is the stronger acting lever: lip-sync constrains the on-screen performance
to the voice emotion.

**Optionally compose with `seed-audio-prompt`** for Seed Audio voice profile
composition and generation. The exact dialogue lines in the Seed Audio `text_prompt` must appear
verbatim inside `{curly braces}` in the Seedance prompt. If one changes, both
change.

Keep `audio_duration <= video_duration`. If the audio exceeds the video
duration, trim the audio prompt (shorter ambience tails, fewer pauses, tighter
scene descriptions) and regenerate. Never pad the video to fit an over-long
audio.

After generating the audio, inspect it (or transcribe with `speech_to_text`)
and set the shot timestamps so each line lands at the second it actually occurs.

Record the audio asset path, SHA-256, verified duration, and the
dialogue-to-shot timestamp mapping in `shot.md` and `scene.md`.

---

## Edge cases and guardrails

- **Intensity is not numerically controllable.** The model reads cues, not
  numbers. When generation comparison is authorized, test the same brief at different
  cue strengths and record the observed result. Prompt-only work does not require
  a paid A/B; no seed guarantees identical performance.
- **2-4 cues per single transition.** More cues overload the performance and
  destabilize it. If more beats are needed, switch to the multi-stage template.
- **No degree adjectives.** "Very sad", "extremely angry", "super happy" are
  banned. Encode intensity via graduated cues (channel count, amplitude,
  movement degree, vocal delivery).
- **Cues serve the tactic, not the emotion label.** Always derive visible
  behavior from what the character is doing (the tactic), not from what they're
  feeling. The emotion bank is a lookup table, not a menu.
- **Plain wording already produces a big action.** "She lunges" makes a lunge;
  the console adds control: the timed hold before it, the stop, the hold after
  it and the wardrobe restated after it.
- **Emotion arcs need ordered triggers and consequences.** Use multiple beats;
  timestamps are optional unless requested or needed for verified audio alignment.
- **`reference_audio` forces lip-sync, not acting fidelity.** It locks the voice
  and mouth timing to the audio emotion. Whether Seedance visibly acts the
  emotion needs an empirical A/B: same prompt, neutral voice vs angry voice.
- **Content safety.** Do not direct performances depicting identifiable real
  people without rights or otherwise restricted content.

---

## Self-check checklist

Before finalizing an acting block or plan, verify:

- [ ] The whole scene dialogue was read before building any character's task.
- [ ] The scene direction is shared, unspoken, and belongs to all characters.
- [ ] Each character has a distinct motive, goal, obstacle, and tactic.
- [ ] The tactic is purposeful action; 2–4 cue choices fit the visible framing
      and do not replace the tactic with mechanical face choreography.
- [ ] No emotion adjectives as direction ("sadly," "nervously," "angrily").
- [ ] The cues are derived from the tactic, not from the emotion label.
- [ ] Every cue is directly observable or audible — no bare abstract emotion
      words standing alone.
- [ ] Intensity is encoded via graduated cues (channel count, amplitude,
      movement degree, vocal delivery), with zero degree adjectives.
- [ ] A single emotional transition uses 2-4 cues max; more beats use the
      multi-stage template.
- [ ] A suppression arc moves toward control and ends on one residual cue
      the framing can show.
- [ ] An animal image is translated into observable cues, and a burst action
      appears at most once per shot with a timed still hold before it, a still
      hold after it, and the wardrobe restated after it.
- [ ] A veil or mask that leaves the eyes visible keeps the covering and gives
      the eyes the tactic.
- [ ] Every arc beat has a trigger and readable consequence; timestamps appear
      only when requested or needed for verified audio alignment.
- [ ] When dialogue is set, the line appears verbatim inside `{}` with a delivery
      style and dialogue language.
- [ ] When audio reinforcement is used: Seed Audio voice profile composed,
      duration checked (`audio_duration <= video_duration`), `reference_audio`
      passed as `@Audio 1`, identical `{dialogue}` text in both prompts, shot
      timestamps aligned to actual audio.
- [ ] `shot.md` records the dialogue-to-shot mapping beside the audio record.
- [ ] Every named hand, arm or foot gives both anatomy and frame side.
- [ ] Each spoken line fits its shot: words / 2.2 + 1 s, ending at least 0.4 s
      before the clip ends.
