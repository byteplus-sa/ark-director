# Edit recipes

## 1. Word timings from the take

`speech_to_text` assumes 16 kHz mono PCM for `wav`, so extract that first:

```bash
ffmpeg -i s01_sh010_t01_v02.mp4 -vn -ac 1 -ar 16000 -c:a pcm_s16le qa/s01_sh010_t01_v02_16k.wav
```

Submit `speech_to_text` through `ark_job_submit` with
`audio_file_path` and `audio_format: "wav"`. Save the completed
`TranscriptionResult` JSON (its `utterances[].words` carry the timestamps)
to `qa/stt_result.json`, then flatten it:

```bash
uv run .agents/skills/seedance-avatar-news/scripts/stt_words.py qa/stt_result.json qa/stt_words.json
```

The script prints `index start-end word`. Map caption chunks to those
indices. STT can merge or split tokens ("115 inch", "2195"), so always build
the chunks from this printout, never from the script.

## 2. Render

```bash
uv run .agents/skills/seedance-avatar-news/scripts/render_short.py projects/<slug>/options/<x>/edl.json
```

`uv run` installs the script's inline dependency (Pillow). ffmpeg and ffprobe
must be on PATH, but libass and drawtext are not needed. Output: 1080×1920,
29.97 fps, H.264 CRF 17, AAC 192k at -14 LUFS, plus `<out>_cues.json`.

The script validates before rendering and exits with a list of problems
when:
- segments don't tile `0 → end` contiguously in order
- `end` is longer than the take
- a clip is missing, or shorter than `offset + duration × speed`
- a chunk's word indices are out of range or overlap

After rendering, it checks every segment's frame count so picture and speech
cannot drift.

## edl.json

All paths are relative to the EDL file. `clip` is relative to `clips_dir`, or
to the EDL folder when `clips_dir` is omitted.

```json
{
  "take": "s01_sh010_t01_v02.mp4",
  "clips_dir": "broll",
  "stt": "qa/stt_words.json",
  "end": 27.0,
  "take_focus_y": 0.3,
  "take_split_focus_y": 0.05,
  "sources_label": "Snap",
  "channel_label": "THE MANAV PODCAST",
  "out": "s01_render_v01.mp4",
  "segments": [
    {"start": 0.0, "end": 3.9, "layout": "full_m"},
    {"start": 3.9, "end": 5.1, "layout": "full_b", "clip": "src_day.mp4", "offset": 0.0, "speed": 0.6},
    {"start": 5.1, "end": 9.3, "layout": "split", "clip": "src_highlights.mp4", "offset": 12.3, "crop_bottom_frac": 0.12},
    {"start": 9.3, "end": 10.4, "layout": "full_m"},
    {"start": 10.4, "end": 12.7, "layout": "card"},
    {"start": 12.7, "end": 25.4, "layout": "split", "clip": "src_event.mp4", "offset": 114.3, "focus_x": 0.7},
    {"start": 25.4, "end": 27.0, "layout": "full_mz"}
  ],
  "chunks": [[0, 2, "Snap just put"], [3, 4, "an entire"]]
}
```

| Segment field | Meaning |
|---|---|
| `offset` | In-point in the source clip (s) |
| `speed` | Playback rate (< 1 slows). The script reads `duration × speed` seconds of source. |
| `focus_x` | 0–1 horizontal anchor for the cover-crop |
| `crop_bottom_frac` | Fraction trimmed from the bottom before cropping (burned-in subtitle bands) |

Captions are uppercased by the script.

## Layouts

| Layout | Picture | Caption y |
|---|---|---|
| `split` | B-roll top 1080×960, presenter bottom 1080×960 | 960 (on the seam) |
| `full_m` | Presenter full frame | 1350 |
| `full_mz` | Presenter full frame, 12% punch-in (closers) | 1350 |
| `full_b` | B-roll full frame | 1350 |
| `card` | Presenter in a rounded frame on black ("and here's…") | 1500 |

A faithful replica is all `split` segments plus one `card` beat on the pivot
line. A remix opens on `full_m` for the hook, alternates `full_b` and `split`
every 1.5–3s on the capability beats, uses `card` on the pivot, and closes on
`full_mz`. In practice each B-roll cut is its own segment.

A square (1:1) take works for `split` and `card`. For `full_m` it gets
cover-cropped hard, so generate the take at 9:16 when the edit goes
full-screen on the presenter.

## Captions

- A cue starts at its first word. It ends at the next cue's start, or 0.45s
  after its last word when the gap is over 0.6s. Cues are clipped at a
  layout-class change so a caption never jumps position mid-display.
- Style: Helvetica Neue Bold 64 px (Arial Bold / DejaVu Sans Bold fallback),
  white on a 22 px-radius pill at rgba(10,10,12,0.69).
- Badges: "Sources: <brand>" top-left and the channel name top-right, 26 px on
  a frosted pill with a thin outline, at y=70.

## B-roll provenance and rights

`broll/PROVENANCE.md` records, per source file: URL, title, channel, download
date and tool, SHA-256, the in-points actually used, and the **usage basis**.
The usage basis is the license, press-kit terms, written permission, or "editorial
commentary; private review only — clear before publishing". Downloading from
an official channel does not by itself grant reuse rights. Before anything is
published, the user confirms the usage basis. Also note any "prototype /
subject to change" disclaimers from the source.

## Review

The project's required review surface is the `showcase-html` production canvas
(`showcase.json` → `index.html`), updated after each take and render. A quick
side-by-side `viewer.html` is optional. Serve either over http
(`python3 -m http.server <port> --directory projects/<slug>`), because a
`file://` page in the browser pane is a static snapshot and cannot load
relative media.
