# Dubbing preparation

Load this reference for source assessment, speaker mapping, reference preparation, and prompt authoring. Plan the reference clips before finalizing relative prompt timestamps.

## Preflight

Gather and verify all inputs before generating anything.

**Required inputs:**
- Source audio or video file (the original)
- Target-language script (text, SRT, VTT, or plain text per line)
- Target language name

**Verification checklist:**
- [ ] Source file exists and is readable
- [ ] Source audio duration (use `ffprobe`)
- [ ] Source audio is ≤ 120s (single pass) or needs generation segmentation
- [ ] Source audio is ≤ 30s (single reference clip) or needs reference segmentation
- [ ] Target script has the same number of lines as the original has spoken segments
- [ ] Target script is in the correct language (verify by reading it)
- [ ] Target language is supported by Seed Audio cross-lingual synthesis (check the current API reference; see [language reference](language-reference.md) for pronunciation)
- [ ] If source is video, extract audio track first
- [ ] Whole original soundtrack measured: RMS profile, ASR of its own audio, non-voice sound list, integrated loudness

**Common preflight issues and fixes:**

| Issue | Fix |
|---|---|
| Source audio >10MB (reference upload limit) | Compress an eligible segment to MP3; probe its duration/size and listen for changes after compression |
| Source audio >30s (reference clip limit) | Split into reference segments at natural scene boundaries; each clip must be ≤30s; generate separately and mix at absolute offsets (see Reference segmentation below) |
| Source audio >120s (generation limit) | Split into generation segments at natural scene boundaries; generate each separately; assemble at recorded absolute offsets |
| Prompt >3,000 chars | Shorten pronunciation guides, remove verbose descriptions, use abbreviated character profiles |
| Source is video (not audio) | Extract audio with `ffmpeg -i input.mp4 -vn -acodec libmp3lame -b:a 320k -ac 2 audio_ref.mp3` |
| No target script provided | Transcribe first with speech-to-text, then translate; do NOT proceed without an approved script |
| Target script is SRT/VTT | Parse timestamps and line text from the subtitle file; use the timestamps directly in the Seed Audio prompt |

## Character identification

Before writing the prompt, identify every speaker and assign them to dialogue lines; follow [character identification](character-identification.md) for clues and the validation checklist. Verify the count against the audible number of distinct voices in the source; script relationships alone do not establish who spoke a line.

**Character mapping template:**
```
Speaker A — [role description], [voice quality], [emotional baseline] — speaker number X in @Audio1
Speaker B — [role description], [voice quality], [emotional baseline] — speaker number Y in @Audio1
Speaker C — [role description], [voice quality], [emotional baseline] — speaker number Z in @Audio1
```

**Retain unresolved speaker mappings as unconfirmed.** Verify against the audible source or supplied cast information. Ask for the missing mapping before dependent generation if ambiguity remains; do not infer speaker identity or gender from a relationship phrase alone.

## Prompt authoring

Write the Seed Audio TA2A prompt. Keep it under 3,000 characters.

**Prompt structure (compact form):**

```
@Audio1: [source reference description — what to clone]. Clone all voice timbres,
cadence, emotion, pacing, pauses, speaker order, and scene timing exactly.
Same [N] characters speaking in same order. Only change dialogue from
[source language] to [target language] using the script below.
Preserve room tone and acoustic character of @Audio1.

[N] speakers from @Audio1:
A — [role] (age/gender, voice quality) — [which voice in the source]
B — [role] (age/gender, voice quality) — [which voice in the source]
...

Match every pause, rhythm, and gap in @Audio1 exactly.
Pure spoken dialogue with the source room tone and acoustic character.

[Speaker X] says [delivery]: "[start_s:end_s] [target dialogue line]"
[Speaker Y] says [delivery]: "[start_s:end_s] [target dialogue line]"
...

Pronunciation: [target language pronunciation notes, stress patterns,
intonation guidance. Keep concise — only the essential patterns.]

Ending: Clean ending matching @Audio1 exactly, same tail silence and room tone.
```

**Prompt length budget (≈3,000 chars):**
- Reference + speaker setup: ~400 chars
- Dialogue lines: ~1,500–2,000 chars (varies by script length)
- Pronunciation guide: ~300–500 chars
- Ending + other: ~100 chars

**If the prompt is too long:** follow the prompt-too-long order in [extended dubbing](extended-dubbing.md#prompt-too-long-strategies); split into segments per [long-form dubbing](extended-dubbing.md#long-form-dubbing-120s) when locked text still does not fit.

**Timestamp conventions:**
- Use the original SRT/VTT timestamps directly if available
- If no SRT, estimate timestamps based on line count and total duration
- Timestamps use seconds with one decimal: `[1.2s:3.7s]`
- Gaps between lines = room tone / silence matching the original

**Timestamp behavior and limitations:**
- Precision is approximately 100ms — the model fits delivery into the timestamp window but not to frame-exact precision
- The model **fits each line's delivery into the window** — it speeds up, slows down, and places pauses to make the line land within `[start:end]`
- Lines without timestamps are paced naturally by the model
- Long gaps between lines (2s+) are difficult for the model to preserve as silence — it tends to compress or fill them. For critical gaps, split into separate segments at the gap boundary and handle silence in assembly
- Timestamps are most effective when each line's window matches the original speech duration closely

## Reference preparation

Prepare the source audio for upload as a Seed Audio reference. The **30-second per-clip limit** is the primary constraint — not file size.

Split the source into ≤30s reference clips at cut points you choose, snapped to
subtitle gaps when a target `.srt` is available (never mid-line), output as MP3
320kbps clips with offsets for assembly, and per-segment relative timestamps for
prompt authoring. The inline splitting recipe below covers this; for SRT-snapped
cutting with per-segment relative timestamps, optionally compose with the
`audio-split` skill (`-s` flag).

**Single reference clip (source ≤30s):**
When the source is under 30s and under 10MB, compress to MP3, probe the encoded duration and size, and upload an eligible clip labeled `@Audio1`. This is the simplest case — one generation covers the full source.

**Reference segmentation (source >30s, ≤120s):**
When the source exceeds 30s but fits within the 120s generation limit, split into multiple reference clips at natural boundaries (scene gaps, dialogue pauses, speaker handoffs). Each encoded clip must be ≤30s and ≤10,000,000 bytes, including overlap and codec padding. Overlap clips by 2–3 seconds at boundaries to preserve voice identity continuity. Each clip gets its own generation with timestamps **relative to that clip's start** (not absolute timeline time). After generation, mix segments at their absolute offsets using `adelay` + `amix` (see [assembly](generation-assembly.md)).

**Splitting recipe:**
```bash
# Split a 68s source into 4 clips at natural boundaries
# Clip 1: 0s–22s, Clip 2: 20s–38s (2s overlap), Clip 3: 36s–49.5s, Clip 4: 47.5s–68s
ffmpeg -ss 0 -t 22 -i source.wav -acodec libmp3lame -b:a 320k -ac 2 -ar 44100 seg1_ref.mp3
ffmpeg -ss 20 -t 18 -i source.wav -acodec libmp3lame -b:a 320k -ac 2 -ar 44100 seg2_ref.mp3
ffmpeg -ss 36 -t 13.5 -i source.wav -acodec libmp3lame -b:a 320k -ac 2 -ar 44100 seg3_ref.mp3
ffmpeg -ss 47.5 -t 20.5 -i source.wav -acodec libmp3lame -b:a 320k -ac 2 -ar 44100 seg4_ref.mp3
```

**Encoded reference validation:** MP3 padding can push a requested 30s cut past the reference limit. Probe every actual output, check its byte size, and decode it before upload. Reserve padding inside the maximum or use WAV. Subtitle snapping and overlap must preserve the same limits; fail explicitly when a complete cue cannot fit.

**Splitting rules:**
- Split at natural boundaries: scene transitions, dialogue pauses (2s+), speaker handoffs — never mid-line
- Each clip ≤30s, under 10MB after compression
- Overlap by 2–3 seconds between clips (preserves voice identity across boundaries)
- Record the absolute offset of each clip for assembly (e.g., seg1=0s, seg2=20s, seg3=36s, seg4=47.5s)
- Timestamps within each segment's prompt are relative to that segment's start, not the original timeline

**Compression recipe (if a segment is over 10MB):**

For eligible reference segments (stereo):
```bash
ffmpeg -i source.wav -acodec libmp3lame -b:a 320k -ac 2 -ar 44100 source_ref.mp3
```
- 320kbps stereo MP3 at 44.1kHz — ~2.6MB for 60s of audio
- Preserves full frequency range and stereo imaging for voice cloning

For eligible segments that still exceed the byte limit at 320k:
```bash
ffmpeg -i source.wav -acodec libmp3lame -b:a 128k -ac 1 -ar 22050 source_ref.mp3
```
- 128kbps mono MP3 at 22.05kHz — ~1.0MB for 60s of audio
- Listen after compression; lower bitrate can change timbre and cloning quality

**Upload via MCP:**
Use `media_upload` with `media_type: "audio"` and the compressed file.
Save the returned `object_key`, URL, and actual expiry metadata. Refresh an expired upload URL before preparing a new request; an expired URL does not authorize resubmitting an uncertain generation.
