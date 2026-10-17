# Specialized Formats

Focused reference for `seedance-music-video`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Format-specific rules](#format-specific-rules)
- [Custom-format procedure](#custom-format-procedure)

## Format-specific rules

- **Performance**: keep the performer on screen and the mouth in frame for
  lip-sync; vary shot size between close-ups (intimacy) and full-body (dance);
  a direct-address close-up reads as intimacy, a 3/4 angle as outward
  performance.
- **Narrative**: indirect address — characters never acknowledge the camera;
  keep the song as score and let the lyric relation be a deliberate choice
  (literal, amplified, or disjunct).
- **Conceptual**: choose one governing visual rule that encodes the track, then
  execute it with mechanical rigor; do not add a plot unless the rule needs it.
- **Lyric**: the type is the star, but it is added in post. The prompt asks
  for simple, text-free imagery with a stated calm zone and a background dim
  enough for type. In the edit, pop each word on its accent from ASR word
  times, hold every word long enough to read, keep to one or two fonts, and
  make kinetic type faster and tighter in the chorus, looser in the verses.
- **Visualizer**: no performer, no story, no lyrics; audio-reactive shapes,
  waveforms, particles, or geometry that shift with the sections.
- **Hybrid**: state which sections carry performance and which carry the
  narrative/concept; do not let either strand crowd the other.

### Vertical vs landscape

- **9:16 (vertical)** is the discovery default for TikTok / Reels / Shorts:
  center the subject, prefer close and medium shots, plan fast cuts (roughly
  1–3s, faster ones made in the edit), open with the hook, and use vertical
  motion (reveals, tilts, drops) over horizontal pans. Native 9:16 composition
  beats cropping 16:9.
- **16:9 (landscape)** is the YouTube master: allow richer backgrounds,
  multi-subject staging, and continuity. Render one purpose-built 9:16 cut
  rather than stretching a 16:9 master.
- State the aspect ratio as a generation parameter, never inside the prompt.

## Custom-format procedure

For an unlisted format or genre:

1. Identify the format's address mode (direct, indirect, or none).
2. Define the song map: which sections carry what visual energy.
3. Choose the audio treatment (native vs audio-first) and the beat contract.
4. Name the genre lock: palette, lighting, camera grammar, and motion cadence.
5. Define the performance-to-atmosphere ratio per section.
6. Write a format-first opening and a compact style seal.
7. Add only exclusions that prevent likely drift or genre leakage.
