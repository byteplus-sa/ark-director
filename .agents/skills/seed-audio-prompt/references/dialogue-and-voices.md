# Dialogue And Voices

Focused reference for `seed-audio-prompt`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Characters and dialogue](#characters-and-dialogue)

### Characters and dialogue

Define each character with the voice attributes needed to distinguish them, then script their dialogue in scene order. Use the same character name on every line. Give the complete voice profile on first mention; later lines may shorten the description but must preserve the name and, in TA2A, the same `<<TGT_SPKN>>` mapping.

```text
Characters and dialogue
[Character Name] ([age/gender], [accent], [voice quality description], [emotional baseline], [delivery style]) says [delivery note]: "[dialogue]"
```

**Character voice profile format (T2A)**:

```
Name (age, gender, accent, voice timbre, emotional tone, delivery style) says: "dialogue text"
```

Examples:
```
Aric (young prince, breathless but brave, fantasy war film style) says: "There are too many. The valley is full of them."

The commentator (middle-aged male, British accent, rich and penetrating voice, classic sports commentary, extremely exhilarated) shouts in a rapid, soaring tone: "OH, HE SCORES!!! WHAT A GOAL!"
```

**Character voice profile format (TA2A)** with voice cloning tags (`<<TGT_SPKN>>` and `@AudioN` are prompting-guide conventions for mapping in-prompt speakers to the ordered entries in `references[]`):

```
Name (voice description, voiced by <<TGT_SPKN>>) says [delivery note]: "dialogue text"
```

Examples:
```
Marcus (male voice, smooth and confident, warm playful broadcaster tone, clear articulation, voiced by <<TGT_SPK1>>), upbeat and inviting, says: "Hey there! Quick question—what's the most embarrassing thing that's ever happened to you?"

Lira (clear, bright young female voice, resonant with a crystalline timbre, voiced by <<TGT_SPK1>>) says firmly yet pleadingly: "Voss, it's not too late to stop."
```

**Voice profile components** (use supplied traits or explicitly authorized voice design, not mandatory inferred fields):
- **Age**: young, teenage, young adult, middle-aged, old
- **Gender**: male, female
- **Accent**: American, British, Australian, etc.
- **Timbre**: bright, dark, warm, cold, breathy, rich, thin, gravelly, smooth, crystalline, resonant, deep, airy
- **Emotional baseline**: calm, anxious, angry, joyful, sad, determined, fearful, playful, serious
- **Tone**: soft, loud, gentle, fierce, steady, shaky, confident, hesitant
- **Speed**: slow, rapid, measured, speeding up, drawing out words
- **Delivery style**: fantasy war film, classic sports commentary, broadcaster, conversational, theatrical, whispered, shouted

**Dialogue rules**:
- Put spoken text in double quotes.
- Describe delivery before the quote: "says playfully and teasingly," "shouts in a rapid, soaring tone," "whispers, voice cracking."
- Include physical actions or appearance when they affect delivery or generate sound: "gasping then bursting out laughing," "slapping his knee with an audible clap."
- For multi-character scenes, alternate characters chronologically and place actions, music changes, and SFX between the lines where listeners should hear them.
- Preserve established voice identities and reference bindings. Contrast current delivery where useful; add identity traits only when voice design is authorized.
- For voices heard through a device or space, describe the filter or acoustics: television reverb, walkie-talkie compression, telephone band-limit, public-address echo, or whispered proximity.
- For a voice with a power beyond the speaker (a layered chorus under the lead line), use the layered-voice motif in [soundscape arrangement](soundscape-arrangement.md#sonic-motifs-and-voice-treatment).
- Keep dialogue attribution explicit. Do not write an unlabeled block of alternating quotes.
- Wrap ambient descriptions and non-speech sounds in square brackets: `[Ambient street sounds: passing cars, distant chatter.]`
- Preserve script language, including mixed-language lines. Match control wording to the user's preference; do not translate dialogue to enforce a single language.

Multi-character dialogue template:

```text
Characters and dialogue
[Name A] ([full voice profile, and voiced by <<TGT_SPK1>> in TA2A]) [action], then says [delivery]: "[dialogue]"

[Music/SFX/ambience change triggered by the line or action.]

[Name B] ([contrasting full voice profile, and voiced by <<TGT_SPK2>> in TA2A]) replies [delivery]: "[dialogue]"

[Name A] (voiced by <<TGT_SPK1>> in TA2A) [brief delivery update]: "[next dialogue]"
```

For TA2A, make the reference plan unambiguous:

1. State what audio scene will be generated.
2. Identify each reference as `@Audio1`, `@Audio2`, or `@Audio3`.
3. State the purpose of each reference, such as a character's voice timbre or emotional performance.
4. Map each character to the matching ordered speaker tag, `<<TGT_SPK1>>` through `<<TGT_SPK3>>`, and never change that mapping within the prompt.

**Timestamp control** (T2A and TA2A prompting-guide convention, not defined in the public API reference):

Use `[start_time:end_time]` only for supplied intervals or explicitly authorized timeline design. A total duration alone does not authorize segments. Put controls outside quoted speech:

```
[5.5s:8.0s] Ryan (young adult male, warm voice) calls out anxiously: "Maya! Wait—you're really leaving tonight?"
[8.5s:11.5s] Maya (young adult female, soft voice) answers softly: "I have to. I've spent years chasing this… I can't walk away now."
```

Timestamps are in seconds with decimal precision. Treat them as prompting guidance rather than an API guarantee, and ensure the requested windows fit within the validated output duration.
