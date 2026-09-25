# Overlay timeline (timed PNG layers over video)

Load this reference when rendered overlay PNGs (logo, headline words, CTA pill,
lower-third, end card) must be composited onto a generated take with timed
fades or rise-ins. It replaces hand-written ffmpeg `filter_complex` chains with
one validated JSON timeline and a hash-bound sidecar record.

## Rules

- Generated footage stays text-free. All on-screen copy arrives here as a
  layer, never through the video prompt.
- Every layer is a deterministic `render_html.py` output (with its
  `render_*.json` record) or an approved acquired logo/product asset.
- Time layers to measured cuts and beats of the actual take (scrub it or
  probe it), not to the timestamps written in the generation prompt.
- Record the sidecar (`overlay_<output-stem>.json`) path and output SHA-256 in
  the shot or scene manifest `finish` block, then update the canvas.
- The machine ffmpeg has no `drawtext`; this tool uses only `overlay`,
  `scale`, `format`, `fade` (alpha) and `enable` expressions.

## Usage

```bash
# Dry run: print the ffmpeg command
uv run python .agents/skills/html-graphic-render/scripts/overlay_timeline.py \
  --project projects/<p> --timeline scenes/scene-02/s02_sh010/finish/timeline_v01.json

# Render the MP4 and its sidecar record (refuses to replace unless --overwrite)
uv run python .agents/skills/html-graphic-render/scripts/overlay_timeline.py \
  --project projects/<p> --timeline <rel.json> --run [--overwrite]

# One review still: over the base frame at t, or over a solid colour
uv run python .agents/skills/html-graphic-render/scripts/overlay_timeline.py \
  --project projects/<p> --timeline <rel.json> --preview <rel.png> --at 8.5
uv run python .agents/skills/html-graphic-render/scripts/overlay_timeline.py \
  --project projects/<p> --timeline <rel.json> --preview <rel.png> --at 8.5 --background 0x2A2A2A
```

`--preview` without `--at` renders t=0 over `0x2A2A2A`. Output is libx264
`-crf 17`, `yuv420p`, `+faststart`, at the base frame rate.

## Schema (`schema_version: 1`)

All paths are project-relative; absolute paths, `..` and symlink escapes are
rejected. Unknown keys are rejected.

| Field | Meaning |
| --- | --- |
| `base` | Base video path (probed for fps, size, duration, audio) |
| `output` | Output MP4 path; sidecar is written beside it |
| `duration` | Output seconds; defaults to the base duration |
| `layers[]` | Composited in order; later layers sit on top |
| `layers[].src` | PNG path (transparent for partial overlays) |
| `layers[].start` / `end` | Visible window in seconds; `end: null` holds to the end |
| `layers[].x` | Integer px or `"center"`; default `0` |
| `layers[].y` | Integer px; default `0` (full-frame layers need no position) |
| `layers[].width` | Scale to this width, preserving aspect |
| `layers[].fade_in` / `fade_out` | Alpha fade seconds at the window edges (`fade_out` needs `end`) |
| `layers[].rise_px` / `rise_s` | Start `rise_px` lower and ease to `y` over `rise_s` (default 0.15) |
| `fade_to_black` | `{start, duration}` video fade after all layers |
| `audio` | `"copy"` (default; skipped if the base is silent), `"none"`, or `{"path": ...}` (AAC) |
| `loudnorm` | Optional `{i, tp[, lra]}`; re-encodes audio to AAC |

## Worked example

```json
{
  "schema_version": 1,
  "base": "scenes/scene-02/s02_sh010/vid_s02_sh010_t01_v01.mp4",
  "output": "scenes/scene-02/s02_sh010/finish/fin_s02_sh010_t01_v04.mp4",
  "duration": 10.04,
  "layers": [
    {"src": "elements/shakeys-logo/refs/ref_official_v01.png", "start": 0, "end": null, "x": "center", "y": 24, "width": 250},
    {"src": "scenes/scene-02/s02_sh010/overlays/ov_s02_word-1_v01.png", "start": 0, "end": 7.13, "fade_out": 0.08},
    {"src": "scenes/scene-02/s02_sh010/overlays/ov_s02_word-2_v01.png", "start": 2.375, "end": 7.13, "fade_in": 0.08, "fade_out": 0.08},
    {"src": "scenes/scene-02/s02_sh010/overlays/ov_s02_name_v01.png", "start": 7.45, "rise_px": 60, "rise_s": 0.15, "fade_in": 0.15}
  ],
  "audio": "copy"
}
```

The sidecar records the timeline, base, layer and audio paths with SHA-256,
the ffmpeg version, and the output SHA-256, bytes, duration, size and fps.
