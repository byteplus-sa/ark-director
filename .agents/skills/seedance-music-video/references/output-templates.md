# Output Templates

Focused reference for `seedance-music-video`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Output formats](#output-formats)

## Output formats

### Music-video block

Use when the user only wants the directing layer:

```text
[Music-Video Format]
<Format name, direct or indirect address, and performance-to-atmosphere ratio.>

[Song Map]
Section 1 (<verified time range or event cue>): <visual assignment, energy, end state>.
Section 2 (<verified time range or event cue>): <visual assignment, energy, end state>.
Final Section (<verified time range or event cue>): <closing assignment and final visible state>.

[Beat & Cut Contract]
<Which audio events the cuts and camera land on; cut density per section.>

[Audio Treatment]
<Native audio brackets, or the @Audio N timing-authority binding for audio-first.>

[Genre Lock]
<Palette, lighting, camera grammar, motion cadence, and tone.>

[Style Seal]
<Compact closing sentence and relevant exclusions.>
```

### Full Seedance prompt

Use when the user asks for a complete prompt:

```text
[Audio First] (only when lip-synced vocals are requested)
@Audio 1 is the exact soundtrack and timing authority. Preserve its music,
vocals, and pauses; do not add dialogue, narration, music, subtitles, or
captions. Match <performer>'s visible mouth only to <performer>'s voice in
@Audio 1.

[Reference Roles] (only when references exist)
@Image 1 defines <performer>'s <appearance, wardrobe, or identity>.
@Image 2 defines <scene or venue>. Do not use <unwanted content>.

<Subject performs the primary action in <scene>.>
The visuals feature <genre lock: palette, lighting, lens, grade, look>.
Use <shot sizes, camera moves, and cuts>, with <beat contract>.
Audio includes <(music)> <{sung lines}> <sound effects>.
Audio: <@Audio N timing binding, or native brackets>. For rap or fast vocals,
       use verified per-line timing when available, otherwise ordered cues: <[X-Ys] { line }> per line with a
       "no line skipped" mandate (see section 3b).

[Shot Plan] or [Stage Plan]
Shot 1 (<time range>): <size>, <angle>; <camera move>. <one event and visible end state>. Light: <source, key side>.
Shot 2 (<time range>): <size>, <angle>; <camera move>. <one event and visible end state>. Light: <source, key side>.
Final Shot (<time range>): <size>, <angle>; <camera move>. <closing event and final visible state>. Light: <source, key side>.

[Maintain Consistency]
Keep <performer identity, wardrobe, venue, camera grammar, and audio>
consistent across the section chain.

[Style Seal]
<Compact genre, palette, motion cadence, beat contract, and tone.>
```

Return the prompt directly. Do not add production workflow, tool selection,
asset management, approval gates, or generation instructions unless the user
explicitly asks for them.
