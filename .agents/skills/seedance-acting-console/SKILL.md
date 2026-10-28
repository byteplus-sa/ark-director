---
name: seedance-acting-console
description: Encode supplied performance intent as Seedance cues. Use for acting blocks, delivery or cue repairs. Not for whole-scene analysis or generation.
---

# Seedance Acting Console

Translate caller-supplied performance intent into concise, shot-ready
intent/trigger/response cues. Keep scene interpretation in the performance
plan; do not repeat it in every prompt.

This skill is **prompt-composition only**. It never generates media, invokes
sibling skills, changes production state or approves a take. The caller owns
composition with `acting-direction`, `seedance-prompt-25` and any requested
audio workflow.

---

## Input contract

For scene work, consume the relevant portion of the caller's
`## Performance plan`, using the handoff in
[`acting-direction`](../acting-direction/references/performance-plan.md):

- Existing scene, character and beat IDs, source line/action locators and
  source hash when supplied.
- Motive, personal goal, tactic toward partner or situation, physical channel,
  and relevant circumstances, knowledge and obstacles.
- Beat triggers, what is registered, tactic maintained or changed, intended
  response and end state; listening task or non-responsive disposition.
- Locks on exact dialogue, language, register, outcome, medium, framing,
  timing, concealment and performance choices; unresolved coverage needs.

Use these as authority, not an invitation to redo scene analysis. Preserve
supplied evidence limits and distinguish established intent from proposed cue
wording. Return material gaps or contradictions to the caller for direction;
do not invent motive, history, a new ending or character knowledge.

For an isolated prompt, explicit intention is enough: who is trying to do
what, toward whom or what situation, with any relevant trigger and locks.
Do not require a whole-scene plan or invented beat IDs. A bare mood label
permits only a **provisional cue study**, not a production-ready performance
plan. Ask for the missing pursuit and context before treating it as one.

Include shared scene direction only when supplied and supported. Preserve
opposing intentions; do not force opponents into agreement or mirrored traits.
Sustained attention, withholding and ambiguity need not become a tactic switch
or facial change. Carry the supplied physical and emotional state across cuts.

---

## Encoding layer

Translate the supplied tactic into what the model needs to render. Tie each
cue to the relevant intent, trigger and response rather than substituting an
emotion routine. Purposeful looking can check whether an attempt lands, but
eyes are not the only channel and lighting cannot supply missing intent.

### Framing and evidence

The playable tactic and its visible evidence are separate. Preserve the supplied
pursuit, then encode **2-4 relevant cues per transition** that the chosen framing
can actually show. Facial cues are allowed
as consequences of that tactic, not a substitute for it or an arbitrary sequence
of eyebrow and mouth movements. The cue budget is a craft heuristic, not a model
limit. Fewer cues are appropriate when the brief asks for minimal action.
When framing is missing, mark visibility provisional rather than inventing
coverage or claiming the cues are ready for that shot.

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

### Optional emotion bank

Use this model-specific vocabulary only when useful. No emotion-family mapping
or intensity label is required; supplied intent may use cues outside the bank.
The six families offer **visible or audible cues** at three illustrative
strengths, not measured presets. Select only what the framing and audio can
carry. Encode strength through cue channels, amplitude, movement and delivery,
not degree adjectives such as "very sad" or "extremely angry".

| Emotion | Abstract one-liner | Intensity 1 (low) | Intensity 2 (medium) | Intensity 3 (high) | Seed Audio delivery hint |
| --- | --- | --- | --- | --- | --- |
| **Serenity** | A settled, unhurried inner calm with no internal conflict. | Gaze soft and level; breathing slow and even; corners of the mouth at rest. | Eyes half-lidded, brows relaxed; slow, deep breaths; hands loosely folded or open palms. | Shoulders fully dropped; a slow exhale with eyes briefly closed; a subtle, contented smile. | Calm, measured; slow, soft, unhurried. |
| **Joy** | Bright, open, expansive happiness that lifts the body and face. | The corner of the mouth lifts faintly; the eyes soften. | An uncontrollable smile; brows relax; steps become light. | Laughing, spinning in place, breathless; eyes crinkled. | Bright, warm; light and quickening, occasionally breaking into laughter. |
| **Terror** | Overwhelming dread that triggers the freeze response. Built from gaze fixed, brows lowered, tense stillness plus panic respiratory signs. | Gaze fixed; pupils widen; a visible swallow; breathing turns shallow. | Eyes widen fully; brows raised and rigid; chest heaves; hands freeze mid-motion. | Frozen stillness; mouth slightly open; body tensed; a choked, sharp intake of breath. | Thin, breathy; shaky, rapid, strained. |
| **Rage** | Hot, escalating anger pressing outward at a target. | Jawline tense; eyes sharp; nostrils flare slightly. | Both fists clenched; chest heaving; eyes sharp; jaw working. | Veins at the temple; trembling fists; shouts with the voice cracking; whole body coiled. | Shouted, voice cracking; harsh, escalating, clipped. |
| **Fear** | Anxious apprehension and watchfulness about a perceived danger. | Eyes darting; fingers tapping; weight shifting; frequent glancing. | Rapid breathing; eyes darting; biting the lip; hands fidgeting. | Body pulled back; shoulders hunched; gaze searching; voice cracking; quick shallow breaths. | Shaky, rapid; hesitant, tremulous, quickened. |
| **Vigilance** | Sharpened, controlled alertness scanning for threat or opportunity. Built from gaze fixed, brows lowered, tense stillness. | Gaze steady; brows level; posture still but ready. | Gaze fixed and scanning; brows lowered; body still; breathing held. | Utterly still; eyes narrow and unblinking; head slowly panning; hands ready at the sides. | Low, steady; measured, controlled, clipped. |

### Selecting cues

Start with the supplied attempt and choose its readable consequence. For
example, checking whether a partner believes a reassurance can use a purposeful
gaze return and a held reply without assigning a Fear label or level. Borrow
from the bank only where it helps; omit unrelated gestures and keep the
listener's response distinct from the speaker's.

### Intensity encoding guide

Intensity level is a **design-level encoding choice**, not a number the model
reads. If comparing levels 1/2/3, use four graduated levers:

1. **Number of cue channels engaged** - one or two readable channels at level 1,
   stronger or broader readable channels at level 3 within the shot framing.
2. **Amplitude** - faint and contained (a flicker) vs pronounced (a shaking
   fist, tears streaming).
3. **Movement degree** - static containment (held breath, frozen stillness) vs
   full-body release (spinning, shouting, recoiling).
4. **Vocal delivery** - calm and measured, strained and quickened, or shouted /
   cracking.

Do not substitute "very happy" or "extremely terrified" for observable
direction. Adjust only the channels that serve the intent; stronger intensity
does not require more movement or override a restraint lock.

### Restraint and shape patterns

Load [restraint and shape patterns](references/restraint-and-shape.md) when a
tactic needs a precise shape: a **first sign** (one small cue as the earliest
consequence), a **suppression arc** (a visible feeling brought under control),
an **animal image** translated into body cues with optional pattern-specific
single-burst holds, or **eyes through concealment** (a veil or mask that leaves only the
eyes to carry the tactic).

---

## Output grammar

### Shot-ready block

Return only the relevant beat cues, dialogue and unresolved issues. Keep
motive and full source interpretation in the caller's scene record.
Retain source locators and any supplied hash in the handoff, not as spoken
text or fabricated verification.

```text
ACTING TASK - [character ID; supplied beat ID/source locator]
INTENT: [supplied pursuit/tactic toward partner or situation]
TRIGGER -> RESPONSE: [source action/words] -> [registration and readable
consequence through the physical channel; maintained or changed tactic]
LISTENER: [relevant character ID; supplied task/disposition and readable response]
CONTINUITY: [supplied end state needed by the next shot, when relevant]
```

Omit inapplicable fields. Include shared direction once only if supplied and
supported. Use a few framing-readable cues, typically 2-4 per transition or
fewer for restraint. Do not mechanically fill every channel.

- Use playable verbs, not emotion adjectives as the sole instruction. Cues
  can include gaze, brows or mouth when visible and caused by the attempt.
- Keep a relevant silent listener's task or deliberate non-response. Do not
  force a reaction close-up, identical partner cues or conscious listening for
  an unconscious person. Preserve incidental participants' supplied disposition.
- A brief gaze correction is optional when eyes are readable and the brief or
  observed take calls for it, not a universal model requirement.
- For multiple beats, repeat `TRIGGER -> RESPONSE` with supplied beat IDs in
  order. Add timestamps only when requested, supplied as locks or needed for
  verified audio alignment. Label estimated timing provisional.
- For a sustained beat, describe the ongoing attention or non-action; do not
  invent a turn, escalating emotion or final resolution.

### Dialogue, delivery, and language

When dialogue is set, place the exact line inside `{curly braces}` and give the
delivery style plus the dialogue language (non-Chinese dialogue needs the
language stated):

```text
Dialogue language: <language>. <character> <says/shouts/whispers> in <delivery style>: {<exact line>}
```

Ask for missing exact words or material language/register choices rather than
inventing dialogue. Continue clear physical cue work with that gap flagged.

Give each line room using measured delivery or a native-language-informed
read, including pauses. About 2.2 words/s is an English planning estimate, not
a universal gate. Allow for onset (initially 0.5-1.5 s) and a final tail
(initially at least 0.4 s), then verify the actual take. Without delivery
evidence, timing is provisional. Preserve exact words, language, register,
pauses and timing locks. Return an overrun or unresolved fit to the caller
with retiming/splitting options for authorization; do not shorten text, remove
locked pauses, accelerate delivery or change shot duration to make it fit.
Keep performance beats inside the authorized speaking window.

### Worked example

Hypothetical supplied plan: B wants A to stay to finish their conversation.
At beat b020, A picks up a bag; B delays departure through their shared
tablecloth-folding task. A's supplied listening task is to consider the appeal
without accepting yet. Locks: held medium two-shot, English, no tears, no
additional dialogue, no resolved departure.

```text
ACTING TASK - B; b020
INTENT: Delay A's departure by inviting completion of the shared task.
TRIGGER -> RESPONSE: A picks up the bag -> B looks from the unfinished fold
to A and offers the remaining corner while speaking.
LISTENER - A: Consider the appeal; pause with the bag without taking the corner.
CONTINUITY: The fold remains unfinished; A has not agreed to stay.
Dialogue language: English. B says as a quiet invitation: {There is one corner left.}
```

For the full scene prompt, the caller places this block in the six-part formula
(Subject + Action + Scene + Visual Style + Camera + Audio) as the subject/action
section, per `seedance-prompt-25`.

---

## Audio reinforcement (optional)

Do not turn spoken dialogue into an automatic audio-first workflow. Only when
the user requests separate audio or synchronization, return a handoff to the
caller for `seed-audio-prompt` and the audio-video alignment contract. This leaf
neither invokes those workflows nor generates, transcribes or submits audio.

Pass the exact dialogue, requested language/register, delivery intent, voice
constraints and timing locks. The caller verifies supported reference controls
before binding any `reference_audio`/`@Audio 1`, and keeps the audio text
identical to the Seedance `{dialogue}`. No reference guarantees lip-sync,
voice fidelity or visible acting fidelity; actual playback/listening is needed.

Ask the caller for measured duration and dialogue timing, including onset,
pauses and tail. If the audio exceeds the authorized window, return the
conflict for retiming or splitting; do not trim or regenerate audio, change
locked text/timing or silently pad the video. Unmeasured alignment remains
provisional. The caller records the asset path, SHA-256, verified duration and
dialogue-to-shot mapping in existing shot/scene evidence.

---

## Edge cases and guardrails

- **Intensity is not numerically controllable.** The model reads cues, not
  numbers. When generation comparison is authorized, the caller can test the same
  brief at different cue strengths and record the result. Prompt-only work does not require
  a paid A/B; no seed guarantees identical performance.
- **Cue budget is a heuristic.** Usually use 2-4 cues per transition, fewer for
  restraint. Separate supplied beats rather than stacking unrelated gestures.
- **No degree adjectives.** "Very sad", "extremely angry", "super happy" are
  banned. Encode intensity via graduated cues (channel count, amplitude,
  movement degree, vocal delivery).
- **Cues serve the tactic, not the emotion label.** Always derive visible
  behavior from what the character is doing (the tactic), not from what they're
  feeling. The emotion bank is optional, not a required classification.
- **Burst control is optional.** For a supplied lunge, a hold before and after
  the stop can clarify the movement. Keep supplied wardrobe and timing;
  return any conflict rather than adding holds across locked action.
  There is no universal burst cap: body speed, amplitude, interruptions and
  recovery follow source intent and plausibility. Multiple bursts need not
  become slow motion or isolated holds. Speech does not set an energy ceiling.
- **Emotion arcs need ordered triggers and consequences.** Use multiple beats;
  timestamps are optional unless requested or needed for verified audio alignment.
- **Evidence limits.** A prompt-only repair predicts a clearer cue; it does
  not establish that a generated take improved. Do not report uninspected
  motion, voice quality or listener timing as observed.
- **Content safety.** Do not direct performances depicting identifiable real
  people without rights or otherwise restricted content.

---

## Self-check checklist

Before returning an acting block, verify:

- [ ] Supplied intent, beat IDs, triggers, listener disposition and continuity
      survive encoding; no new motive, shared agreement or outcome is invented.
- [ ] Exact dialogue, language, register, medium, framing and timing locks are
      preserved; missing intent is flagged as a provisional cue study.
- [ ] Output is concise intent/trigger/response evidence, not repeated scene
      analysis or mandatory emotion-family mapping.
- [ ] Cues fit the actual framing, camera side, occlusion and scale; fewer
      cues or sustained non-action remain valid for a restrained beat.
- [ ] Strength uses observable changes rather than bare degree adjectives.
- [ ] A suppression arc moves toward control and ends on one residual cue
      the framing can show.
- [ ] An animal image is translated into observable cues, and a burst action
      uses this pattern's single burst and holds only where compatible with
      source locks; conflicts are returned, not silently repaired.
- [ ] A veil or mask stays on; eye cues appear only when readable at the
      selected scale, with physical channels used otherwise.
- [ ] Supplied triggers and consequences remain ordered; timestamps are
      supplied, requested or needed for alignment, with estimates labeled.
- [ ] When dialogue is set, the line appears verbatim inside `{}` with a delivery
      style and dialogue language.
- [ ] Requested audio work is a caller handoff only, with no sibling invocation,
      generation, unsupported binding or fidelity guarantee.
- [ ] Every named hand, arm or foot gives both anatomy and frame side.
- [ ] Dialogue fit uses measured or native-language-informed delivery with onset,
      pauses and tail, not a universal English word-rate gate. Overruns and
      unverified fit return to the caller without altering locked text or timing.
