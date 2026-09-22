# Edit recipes

Render with:

```bash
python3 .agents/skills/seedance-avatar-news/scripts/render_short.py projects/<slug>/options/<x>/edl.json
```

Output: 1080×1920, 29.97 fps, H.264 CRF 17, AAC 192k at -14 LUFS, plus
`<out>_cues.json`. Needs ffmpeg and Pillow only (no libass/drawtext). Paths in
the EDL are relative to the EDL file.

## edl.json

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
    {"start": 3.9, "end": 5.1, "layout": "full_b", "clip": "src_day.mp4", "offset": 0.0, "speed": 0.6, "focus_x": 0.5},
    {"start": 5.1, "end": 7.25, "layout": "split", "clip": "src_highlights.mp4", "offset": 12.3, "crop_bottom_frac": 0.12},
    {"start": 10.4, "end": 12.7, "layout": "card"},
    {"start": 25.4, "end": 27.0, "layout": "full_mz"}
  ],
  "chunks": [[0, 2, "SNAP JUST PUT"], [3, 4, "AN ENTIRE"]]
}
```

- `stt` is a JSON file with `{"words": [[word, start_ms, end_ms], …]}` built
  from `speech_to_text` on the generated take.
- Segments must tile `0 → end` contiguously. They are frame-quantized at 29.97.
- Clips are raw source files. The script cover-crops them (`focus_x` 0–1),
  optionally trims a burned-in subtitle band (`crop_bottom_frac`), and
  retimes them (`speed` < 1 slows).

## Layouts

| Layout | Picture | Caption y |
|---|---|---|
| `split` | B-roll top 1080×960, presenter bottom 1080×960 | 960 (on the seam) |
| `full_m` | Presenter full frame | 1350 |
| `full_mz` | Presenter full frame, 12% punch-in (closers) | 1350 |
| `full_b` | B-roll full frame | 1350 |
| `card` | Presenter in a rounded frame on black ("and here's…") | 1500 |

Faithful replica: all `split` plus one `card` beat on the pivot line.
Remix: open `full_m` on the hook, alternate `full_b` / `split` every 1.5–3s on
the capability beats, `card` on the pivot, and close on `full_mz`.

A square (1:1) take works for `split` and `card`. For `full_m` it is
cover-cropped hard, so generate 9:16 when the edit goes full-screen on the
presenter.

## Captions

- Cue start = first word start. Cue end = next cue start, or the last word end +
  0.45s when the gap is over 0.6s. Cues are clipped at a layout-class change so
  a caption never jumps position mid-display.
- Style: Helvetica Neue Bold 64 px (Arial Bold fallback), white, uppercase, on
  a 22 px-radius pill at rgba(10,10,12,0.69).
- Badges: "Sources: <brand>" top-left and the channel name top-right, 26 px on
  a frosted pill with a thin outline, at y=70.

## B-roll provenance

`broll/PROVENANCE.md` lists, per source file: URL, title, channel (official),
download date and tool, SHA-256, and the in-points actually used. Note any
"prototype / subject to change" disclaimers from the source.

## Review surface

Add each render and its raw take to a local `viewer.html`: video pairs, script,
contact sheet, links to topic/NOTES/provenance, and the shared assets. Serve it
over http (`python3 -m http.server <port> --directory projects/<slug>`). A
`file://` page in the browser pane is a static snapshot and cannot load
relative media.
