# Frame Break QA Checklist

Focused reference for `seedance-frame-break`. Read it when reviewing takes or
running the pixel script. QA is frame-based: judge bar motion, break-out timing,
limb continuity and camera from every frame and the script, and treat a
video-understanding model as secondary evidence only (observed: it reported no
overlap and a moving camera on clips whose frames showed overlap and a locked
camera).

- [Procedure](#procedure)
- [Hard gates](#hard-gates)
- [Soft gates](#soft-gates)
- [Pixel script](#pixel-script)
- [How the static-bar gate decides](#how-the-static-bar-gate-decides)
- [Break-out gate](#break-out-gate)
- [Reading the script output](#reading-the-script-output)
- [Observed calibration on real clips](#observed-calibration-on-real-clips)
- [Script limits](#script-limits)
- [Delivery copy](#delivery-copy)

## Procedure

1. Run the all-frames scan (below) and save the JSON beside the take. The
   static-bar gate and the break-out gate must both pass (or the static-bar gate
   report `inspect` with the listed timestamps checked by eye) before anything
   else is judged.
2. For every stage of the prompt, make a 12 fps contact sheet of that stage's
   time window with `--window START END` and read every tile in order. This step
   is mandatory: a sudden scale jump or limb swap inside a stage is found only
   this way. Sparse sampling (a frame every 0.5 s, or an 8 fps scan) did not flag
   the observed bar-edge failure and would hide a one-second limb pop-in.
3. Inspect the frames at every reported overlap interval and at each stage End
   state, and inspect the backdrop in several frames for lettering, logos, glow
   or flare.
4. Listen to the audio.
5. Apply the gates. A take that fails a hard gate is not selectable. Among takes
   that pass, rank by the soft gates; plan a few takes and pick the cleanest.
6. Record the decision per the project's approval mode; the caller owns it. A
   retouched copy is never delivered as a model output without saying so.

## Hard gates

| Gate | Evidence |
| --- | --- |
| Bars do not move. Black must not encroach into the window at any column, the far columns must not shift together, and no smooth bar-shaped bow may grow into the window; a subject covering a bar is never a violation | Script `summary.static_bar_gate.status` is `pass`, or `inspect` with every listed window checked by eye; `fail` rejects the take. Run on every frame |
| Bars are present, solid black, flat and unmarked at the top and bottom throughout | Script `bars_detected` true; frames |
| The subject starts completely inside the window and break-outs are intermittent events, not a state | Script `summary.break_out_gate`: start overlap near zero and overlap duty under the limit |
| The subject is drawn on top, never clipped or hidden behind a bar at a break-out | Frames at overlap intervals and at each peak |
| Every break-out the brief requires occurs; by default at least one on each bar. A clip with no overlap at all is the effect-absent case | Script `break_out_gate.status` is not `absent`; `frames_with_overlap`, `overlap_intervals`; frames |
| No sudden scale jump or limb swap inside a stage; the limb that arrives at the lens is the limb that crosses | 12 fps window contact sheet per stage, read tile by tile |
| The camera is locked: background features do not pan, zoom or shift | Contact sheets; compare fixed background features across frames |
| No on-screen text, logos, stray lettering or watermarks, including on background objects | Frames |
| Identity matches the approved reference, including soles, markings and colours; one subject only (one product, never a pair, for a product hero) | Frames against the reference |
| No unrequested held props, hands or people (product hero: none) | Frames |

## Soft gates

| Gate | Target | Evidence |
| --- | --- | --- |
| Bar thickness | Near 12 percent of frame height; takes measured 9.4 to 18.9 percent, and 17 to 21 percent in a rejected take (observed) | Script `thickness_pct` |
| Top and bottom match | Median difference within about 1 point | Script `top_bottom_differ` |
| Break-out moments | Drawn subject 3 to 5, photoreal 1 to 3 (observed) | Script `overlap_intervals` |
| Backdrop | Calm, darker than the subject, no bar-like objects | Frames |
| Timing | End states within about 0.5 s of the stage budget; timestamps are allocations | Frames |
| Unrequested effects | No glow arcs or flare around near-lens parts | Frames |
| Audio | Requested sound arc; no music when none was asked (effects-only may still add light music or a chime) | Listening |

## Pixel script

The script needs `ffmpeg` and `ffprobe`. By default it decodes every frame at
the clip's native frame rate, twice: the first pass takes the clip's median
far-left and far-right bar edge rows as the reference, the second measures every
frame against that reference.

```bash
uv run python .agents/skills/seedance-frame-break/scripts/measure_frame_break.py take.mp4 \
  --output take_measure.json --summary-only
uv run python .agents/skills/seedance-frame-break/scripts/measure_frame_break.py take.mp4 \
  --summary-only --contact-sheet stage2.png --window 3 6
```

- `--fps` overrides the sampling rate; leave it unset for the gates. A lower value
  is only for quick looks and can miss a 6-frame edge jump.
- `--black-level` (default 8) is the luma at or below which a pixel counts as
  black. Keep it below dark picture content: rendered bars decode to luma 0 to 2,
  while dark scenery measured 19 and above. At the older default of 24 a dark wall
  beside a bar made the bar look thicker and produced false failures.
- `--output` saves the full per-frame JSON; `--summary-only` keeps stdout short.
- `--contact-sheet` writes a tiled PNG. Without `--window` it covers the whole
  clip at 2 fps, 4 columns, 480 px tiles. With `--window START END` (seconds) it
  covers only that window at 12 fps, 6 columns, 320 px tiles; override with
  `--contact-fps`, `--contact-columns` and `--contact-width`, within
  `--max-tiles` (default 120). Tiles are unlabelled and run left to right, top to
  bottom, one every `1/contact-fps` seconds from the window start.
- Static-bar tolerances: `--edge-tolerance-px` (2), `--tilt-tolerance-px` (3),
  `--encroach-tolerance-px` (8), `--jump-threshold-px` (3), `--bar-shape-fraction`
  (0.4), `--merge-gap-s` (0.2), `--interior-columns` (19).
- Break-out tolerances: `--start-window-s` (0.25), `--start-overlap-tolerance`
  (0.02), `--max-overlap-duty` (0.7), `--overlap-threshold` (0.05).
- Existing outputs are not replaced unless `--overwrite` is given.
- Bad input (a missing file, a non-video, an out-of-range option or window) exits
  with status 1 and prints `{"error": ...}`.

## How the static-bar gate decides

The earlier rule counted any deviation of an interior column as bar motion. On a
take the user accepted, a robe flare, boots and gloves covering the lower bar
were counted as bar deformation, because a subject over a bar and a bar that
moved both change the measured edge row. The gate now separates them by
direction and by shape.

- **Retreat** (the visible edge moves toward the frame edge, the window grows
  into the bar) is how a subject covering a bar looks. At an interior column it is
  never a violation; it feeds the overlap intervals. At a far column it is
  reported as `far_retreat` and `tilt` under `inspect`, not as a failure, because
  a subject, a flare or a light streak can reach a far column and a retreating bar
  looks the same.
- **Encroachment** (black grows into the window, the bar gets thicker) is not
  something a subject does, so it counts. Growth of either far column by more
  than 2 px is `encroach` (fail). A frame-to-frame change of both far columns by
  more than 3 px at once is `jump` (fail). Interior growth over the left-right
  chord by more than 8 px is `bow_in` (fail) only when it is bar-shaped: a
  contiguous group of at least 40 percent of the sampled columns whose profile is
  smooth. A narrower or ragged group is `dark_merge` (inspect): a dark subject,
  such as black shorts or a dark robe, merging with the bar can fake a thicker bar
  and cannot be told apart from one by pixels.
- A constant left-versus-right difference is not motion; it is reported as
  `static_tilt` (inspect) when it exceeds 3 px. Changes of the difference are
  `tilt` (inspect).
- `status` is `fail` when any fail record exists or the bars are not detected,
  `inspect` when only inspect records exist, otherwise `pass`. `passed` is true
  unless the status is `fail`.

Ambiguous cases are inspect, with timestamps, on purpose: open the 12 fps window
sheet for each listed window and decide by eye.

## Break-out gate

A take whose static bars are perfect can still fail if the subject starts over a
bar or stays over one for most of the clip: it reads as standing outside the
frame, not as a frame break. The gate measures the non-black fraction of each bar
band across the central columns.

- **Starts inside**: the largest overlap fraction in the first
  `--start-window-s` (0.25 s) of each bar must be at most
  `--start-overlap-tolerance` (0.02). A failure is `starts_overlapping` with the
  bar, the offending timestamps and the peak fraction.
- **Intermittent**: the fraction of frames with overlap above `--overlap-threshold`
  in either bar (`overlap_duty.overall`; per bar is reported too) must be at most
  `--max-overlap-duty` (0.7). A failure is `overlap_too_continuous` with the duty,
  the limit and the overlap intervals.
- **Absent**: a clip with no overlap in any frame has status `absent`, the
  existing effect-absent case. `not_applicable` means the bars were not detected.
- `passed` is true only for status `pass`.

## Reading the script output

| Field | Meaning |
| --- | --- |
| `summary.static_bar_gate` | `status` (`pass`, `inspect`, `fail`), `passed`, tolerances, the fail `violations` and the `inspect` records across both bars |
| `summary.top`, `summary.bottom` | Thickness (percent and px), median edge rows, static tilt, max far encroach and retreat, max interior encroach, `status`, `violations`, `inspect`, overlap counts |
| records | `bar`, `severity`, `kind` (`encroach`, `jump`, `bow_in` fail; `far_retreat`, `tilt`, `dark_merge`, `static_tilt` inspect), `start_s`, `end_s`, `frames`, `peak_px` |
| `summary.break_out_gate` | `status` (`pass`, `fail`, `absent`, `not_applicable`), `start_overlap` per bar, `overlap_duty` per bar and overall with limits, `violations` with timestamps |
| `frames[].top` and `frames[].bottom` | Left and right edge rows in px, all sampled column rows, excess over the reference chord, thickness, tilt, overlap fraction |
| `overlap_intervals` | Runs of frames above the overlap threshold: bar, first and last frame time, frame count, peak fraction |
| `summary.top_bottom_difference_pct` | Absolute difference of the two median thicknesses, in points of frame height |
| `summary.flags` | `bars_not_detected`, `bars_thin`, `top_bottom_unequal`, `top_bar_moves`, `bottom_bar_moves`, `top_bar_inspect`, `bottom_bar_inspect`, `top_bar_never_crossed`, `bottom_bar_never_crossed`, `no_overlap`, `starts_overlapping`, `overlap_too_continuous` |

Flags and records point at frames to inspect; they are not verdicts on the
creative result.

## Observed calibration on real clips

Observed calibration on real Seedance 2.5 clips at 1920x1080, 24 fps, 8.06 s,
Lark-delivery H.264 copies, default options. The thresholds above were tuned on
these eight clips, so treat them as calibrated on a small set, not as validated
in general.

| Clip (what the user decided) | Static-bar gate | Break-out gate: start overlap top / bottom, duty top / bottom / overall |
| --- | --- | --- |
| Clip A, boxer, rejected for moving bars | fail: top `encroach` and `jump` 1.0 to 1.4 s and about 5.8 to 6.0 s, bottom `encroach` and `jump` 6.5 to 7.0 s; inspect: lower bar `far_retreat` and `tilt` 5.3 to 6.5 s | pass: 0.000 / 0.000, 0.03 / 0.29 / 0.31 |
| Clip A, provider master | fail, same windows | pass, same numbers within 0.01 |
| Clip G, boxer, static bars, rejected for standing outside the window | pass | fail: 0.000 / 0.253, 0.27 / 0.82 / 0.82 (`starts_overlapping`, `overlap_too_continuous`) |
| Clip B, illustrated courier, accepted | inspect: constant 7 px and 4 px bar tilt, lower-bar `far_retreat` 0.3 to 1.25 s, 2.5 to 2.75 s and 6.7 to 6.8 s (a flare arc and a giant sole at a far column) | pass: 0.000 / 0.000, 0.15 / 0.58 / 0.58 |
| Clip C, accepted | inspect: upper-bar `far_retreat` 5.0 to 6.0 s | pass: 0.000 / 0.000, 0.13 / 0.29 / 0.29 |
| Clip D, accepted | pass | pass: 0.000 / 0.000, 0.00 / 0.15 / 0.15 |
| Clip E, accepted | inspect: lower-bar `far_retreat` 1.1 to 1.5 s (a subject part at the right frame edge) | pass: 0.002 / 0.000, 0.53 / 0.49 / 0.64 |
| Clip F, accepted (photoreal product hero) | inspect: upper-bar `dark_merge` 2.4 to 2.5 s | pass: 0.000 / 0.000, 0.00 / 0.22 / 0.22 |
| Clip H, boxer, bars were ring ropes and the subject sat behind them | fail: `bars_not_detected` | `not_applicable`; no overlap in any frame |

What the calibration showed:

- Accepted clips never shrank to a far-column encroachment; the rejected clip
  did. That is why direction decides.
- The default `--max-overlap-duty` is 0.7, not 0.5. A limit of 0.5 would have
  failed two accepted clips (overall duty 0.58 and 0.64); the over-the-bar take
  measured 0.82. The margin is small: 0.64 against 0.7, so check clips between
  0.6 and 0.8 by eye.
- At `--black-level` 24, dark walls beside a bar inflated the bar by 45 px on
  one accepted clip and a persistent tilt appeared; at 8 it did not.
- The interior of the lower bar of the rejected clip also showed `dark_merge`
  windows (a dark robe and shorts merging with the bar) that pixels cannot
  separate from a real bar; they are inspect, not fail.
- Ambiguity that remains: the lower-bar tilt of 5.3 to 6.5 s in the rejected
  clip is reported as `inspect`, the same signature as a subject at a far
  column in two accepted clips. The clip fails on its other windows; a take with
  only such a retreat would read `inspect`.

## Script limits

- A dark subject or costume over a black bar is invisible to the overlap count;
  the count is a lower bound. Always inspect frames.
- Glow, flare or backdrop light inside a bar band also counts as non-black and
  raises the overlap duty.
- Dark scenery next to a bar edge can still read as a thicker bar when it is
  below the black level; lower `--black-level` if a dark scene is flagged.
- A near-lens object covering both far columns, or a bar that retreats rather than
  grows, is reported as `inspect`, never as `fail`.
- The duty limit and tolerances were calibrated on a handful of 1080p clips.
- Limb continuity and the camera lock are not measured; read the window sheets.

## Delivery copy

Seedance 1080p masters came back HEVC 10-bit with the moov atom at the end; make
a faststart H.264/AAC copy for browsers and shared documents, per the `ffmpeg`
skill.
