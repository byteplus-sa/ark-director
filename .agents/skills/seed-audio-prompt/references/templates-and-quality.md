# Templates And Quality

Focused reference for `seed-audio-prompt`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Reusable full-soundscape template](#reusable-full-soundscape-template)
- [Creative and quality constraints](#creative-and-quality-constraints)
- [Conversational voiceover recipe (T2A)](#conversational-voiceover-recipe-t2a)
- [Brand-name pronunciation](#brand-name-pronunciation)

### Reusable full-soundscape template

Use only the sections and fields the request needs.

```text
Input references
@Audio1: [character name] voice timbre — [purpose]
@Audio2: [character name] voice timbre — [purpose]

Scene and atmosphere
Environment: [place, time, weather/context, acoustic space]
Background music: [role, style, instruments, tempo, mood, dynamic arc, mix behavior, ending]
Ambience: [persistent foreground/midground/background environmental bed]

Characters and dialogue
[Character A] ([full voice profile], voiced by <<TGT_SPK1>>) [action] and says [delivery]: "[dialogue]"

[As the action occurs, describe the discrete SFX, position, acoustic quality, and decay. State any music or ambience change.]

[Character B] ([contrasting full voice profile], voiced by <<TGT_SPK2>>) replies [delivery]: "[dialogue]"

[Continue dialogue, actions, SFX, and score changes in chronological order.]

Ending
[Describe the final sound, music resolution or fade, ambience tail, and transition to silence.]
```

For T2A, omit `Input references` and all `<<TGT_SPKN>>` tags. Retain supplied voice profiles without inventing unknown traits.

### Creative and quality constraints

Add only constraints that affect the generated content and are supplied or clearly implied by the user's request.

```text
Creative and quality constraints
Language: [the prompt and dialogue language]
Quality notes: [any specific output requirements]
```

Do not insert `Max duration: 120 seconds` into every prompt. Duration is a request and API validation concern: explain a request beyond the documented limit and ask before splitting or changing protected content.

Key request limits (see Quick reference card for the authoritative table):
- `text_prompt` max 3000 characters.
- Generated audio max 120 seconds per call (billing is based on `original_duration`).
- Max 3 reference audio clips OR 1 reference image.
- Cross-lingual synthesis is supported; consult the [BytePlus voice list](https://docs.byteplus.com/en/docs/byteplusvoice/seedaudio-01) for current supported languages.
- Pricing: 0.15 USD per minute of generated audio (0.0025 USD/second), billed per second.

## Conversational voiceover recipe (T2A)

When the goal is a natural, non-robotic social/ad voiceover, write for
performance, not just for speech:

- **Speech budget is an estimate.** Around 2.2 words per second can be a
  starting heuristic for conversational English, not a language-independent cap.
  Account for pauses and delivery, then inspect actual audio. If locked copy is
  too long, propose revised wording or timing for approval; do not silently cut it.
- **Emotion through delivery, not extra events.** Tie pace, emphasis, and
  restraint to the intended line. Preserve requested breaths, laughter, or sighs;
  do not add them as compulsory cues or change the line's emotional intent.
- **Timestamps are a budget, not a straightjacket.** Keep per-line
  `[start:end]` windows only when lines must land on visual beats; for a
  standalone voiceover, event-relative delivery cues usually sound more natural.

## Brand-name pronunciation

Preserve approved dialogue and brand spelling. First identify the intended
pronunciation from a supplied pronunciation guide or approved spoken reference.
If it is unavailable, flag that uncertainty instead of guessing a brand's sound.
A pronunciation note is an optional technique, not a guaranteed model control.

If the user permits phonetic respelling in the spoken generation text, keep the
canonical written copy separately and identify the exact authorized replacement.
Do not alter locked dialogue, captions or visible brand copy. Compare an authorized
take against the approved pronunciation; a transcript alone does not establish
stress or phonetic accuracy.

## Repair example: crowded soundscape

**Hypothetical teaching example. No audio was generated or measured.**

- **Brief:** A quiet station announcement must remain intelligible over rain
  and a subdued music bed; preserve its exact supplied words.
- **Initial prompt:** “Loud rain, swelling strings, a train horn and the announcer
  all peak together.”
- **Simulated failure:** The announcement is masked at its destination name.
- **Hypothesis:** Competing foreground events occupy the key speech moment.
- **Smallest repair:** “Keep rain distant and music beneath the unchanged
  announcement. Let the horn sound after the destination name; return the
  music to its previous level after the sentence.”
- **Tradeoff:** Reduced simultaneous spectacle improves intelligibility.
- **Acceptance:** Listen for every supplied word, the relative positions of the
  sound layers and the return of the music after speech. Do not claim a dB mix
  change was executed by a prose prompt. If exact levels are required, the caller
  can arrange deterministic mixing of available stems within the authorized scope.
