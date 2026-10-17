# Dialogue and Audio Checklist

Filipino, Tagalog and Taglish dialogue (stacked on the Seedance checklist) and
Seed Audio prompts. Apply the universal items in [the
index](review-checklists.md#universal--all-prompts) first.

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
3. **Register grounded (`dialogue.filipino_register`).** Approved lines keep
   their register, code-switching and politeness. Newly drafted lines with no
   register in the brief default to English-dominant Taglish with simple,
   common Tagalog (po, opo, sige, tara, ingat, salamat); dense or deep Tagalog
   in a new draft is MINOR unless the brief or character calls for it. Do not
   impose contractions, honorifics or a fixed sentence length on every speaker.
3a. **Accent is not code-switching (`dialogue.filipino_register`).** "English
   with a Filipino accent" keeps every spoken word English inside the braces
   and puts the accent in a delivery note outside them. Inserting Tagalog
   words to make an accent request "sound Filipino" is MAJOR. The accent is
   verified by a listener, not by ASR or an audio-understanding model.

### Pronunciation and delivery evidence

4. **Evidence distinguished.** Identify a supplied recording, pronunciation guide
   or competent speaker's correction. Without evidence, a predicted issue is a
   hypothesis, not a proven mispronunciation.
5. **No universal phonology recipe.** Do not force a default stress, flat contour,
   consonant substitution or one regional accent across Filipino speakers.
6. **Notes separate from speech.** Preserve exact spoken text inside braces.
   Annotation or phonetic respelling inside dialogue requires explicit scope,
   and is labeled a hypothesis: respelling can add syllables.
7. **Cues serve intent.** Use concise, observable delivery rather than a dictionary
   or a prescribed pitch sequence. `speech_to_text` is the authority for the
   words; stress, intonation, accent and speaker identity need a listener
   (preferably native). A model summary of the audio is not evidence.

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

46a. **Short lines state their length.** A short line or sting states the
    clip length and the trailing silence; otherwise it can truncate (MINOR).

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
