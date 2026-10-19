# Frame Break QA Checklist

Read this when reviewing returned takes or using `scripts/measure_frame_break.py`.
Measurements locate evidence; they do not establish creative acceptance.

## Procedure

1. Run the scan and save its JSON beside the take. Default results are advisory,
   not automated passes or rejections. Inspect the reported windows.
2. Read a contact sheet for each stage, then step through native frames around
   crossings, returns, scale changes and suspected bar motion. A 12 fps sheet is
   a navigation aid, not proof that every native frame was checked.
3. Check the first frame, stage End states, backdrop, identity and camera lock.
4. Listen to the audio; pixel measurements cannot assess it.
5. Compare against the brief's visual requirements below. The caller owns the
   selection and decision record. Disclose any retouching of a model output.

## Visual Requirements

| Requirement | Evidence |
| --- | --- |
| Bars stay fixed, straight, solid black and unmarked throughout; no extra side bars | Native frames before, during and after suspected motion; edge measurements are leads |
| Subject starts inside, crosses on top of the bars and returns inside between the specified events | Opening, peak and End-state frames, with overlap intervals as navigation |
| Every crossing requested by the brief occurs; normally at least one on each bar | Frames confirming the subject, not scenery or flare, covers the bar |
| No scale jump, limb swap or clipped crossing part | Ordered stage frames against the identity reference |
| Camera stays locked | Compare fixed background features across frames |
| Identity, subject count and props match the approved inputs | Frames against the reference |
| No unwanted text, logos, watermarks, people or hands | Inspect subject and background; product-only means one product |

Confirmed violations of these requirements reject the take. An uncalibrated
pixel classification alone cannot confirm a violation or acceptance.

Soft targets come from the brief: approximate bar height (the prompt template
suggests 12 percent), top/bottom symmetry, crossing count, timing, backdrop
contrast and sound arc. These are design choices, not measured model success
rates. Do not infer a required crossing count from photoreal versus drawn style.

## Pixel Script

Requires `ffmpeg` and `ffprobe`; no Python dependencies. It decodes at the native
frame rate by default in two passes: median far-edge references, then per-frame
measurement against those references. `--fps` overrides sampling; sparse scans
can miss brief events. Variable-frame-rate media are resampled by the fps filter,
so the output is not a native presentation-timestamp inventory.

```bash
python .agents/skills/seedance-frame-break/scripts/measure_frame_break.py take.mp4 \
  --output take_measure.json --summary-only
python .agents/skills/seedance-frame-break/scripts/measure_frame_break.py take.mp4 \
  --summary-only --contact-sheet stage2.png --window 3 6
```

`--output` always contains full per-frame data; `--summary-only` omits frames only
from stdout. Existing outputs require `--overwrite`. A contact sheet defaults
to 2 fps, 4 columns and 480 px tiles, or 12 fps, 6 columns and 320 px tiles with
`--window START END`. Tiles run left to right, top to bottom from the window
start. Override with `--contact-fps`, `--contact-columns`, `--contact-width`;
`--max-tiles` defaults to 120.

## Calibration Contract

**No calibration is bundled.** Existing numeric defaults remain for diagnostic
compatibility, not as universal QA thresholds:

| Options | Diagnostic defaults |
| --- | --- |
| `--black-level`, `--edge-fraction`, `--centre-span`, `--edge-margin` | 8, 0.01, 0.7, 4 px |
| `--edge-tolerance-px`, `--tilt-tolerance-px`, `--encroach-tolerance-px`, `--jump-threshold-px` | 2, 3, 8, 3 px |
| `--interior-columns`, `--bar-shape-fraction`, `--merge-gap-s` | 19, 0.4, 0.2 s |
| `--overlap-threshold`, `--start-window-s`, `--start-overlap-tolerance`, `--max-overlap-duty` | 0.05, 0.25 s, 0.02, 0.7 |
| `--min-bar-pct`, `--thin-pct`, `--top-bottom-tolerance-pct` | 1, 8, 1 percentage points of frame height |

With no `--calibrated-resolution WIDTH HEIGHT`:

- `calibration.mode` is `advisory`, with `resolution: null`.
- Both bar summaries, both gates and `summary.verdict` have `status: inspect`.
  Gates and verdict have `passed: false`, `needs_review: true`; bar `static`
  values are false, meaning not certified static.
- `diagnostic_status` retains the previous classification, including `pass`,
  `fail`, `absent` and `not_applicable` where relevant. Measurements, intervals,
  flags and violation records retain their original meanings and values.
- A diagnostic `fail`, a record with `severity: fail`, or a `*_bar_moves` flag
  is an inspection lead, not an uncalibrated rejection gate. False `passed` is
  not a rejection either. Never route these directly to acceptance automation.
- Overriding a threshold alone does not opt in to gating.

Use `--calibrated-resolution WIDTH HEIGHT` only after the caller has calibrated
the effective settings for the current resolution, encoding, scene contrast,
bar geometry and intended timing. Record the command, settings, representative
accepted and defective examples, human decisions and limitations with the
current task. Check more than one example and include dark content, occlusion,
motion and near-boundary cases; do not select limits from one take's outcome.
Review every setting, including unchanged defaults. There is no universal duty
limit: overlap duration must reflect the requested choreography.

The flag is a **caller declaration**, not calibration performed or validated
by the script. It sets `calibration.mode: explicit` and records the dimensions.
Dimensions must exactly match the decoded input or the command fails before
measurement. Pixel values remain in input pixels; they are not automatically
scaled. Recalibrate for drafts, finals or changed content instead of carrying
thresholds across them. Keep advisory mode when calibration evidence is absent.

Explicit mode restores the prior gate behavior: `pass`, `inspect`, `fail` for
the static-bar gate and verdict; `pass`, `fail`, `absent`, `not_applicable` for
the break-out gate. `passed` is true only for `pass`. The verdict fails when
the static gate fails or the break-out gate is not `pass`; otherwise it requires
review if the static gate does. Even a calibrated pass does not assess all the
visual requirements above.

Exit status remains 0 for a completed analysis, including `inspect` or `fail`;
it is not a QA exit code. Invalid input, resolution mismatch, nonfinite numeric
settings or out-of-range values return 1 with `{"error": ...}`. Argument syntax
errors use argparse's exit status 2.

## Diagnostic Logic And Limits

- Edge growth beyond the configured far-edge tolerance gives `encroach`.
  Both far edges changing between frames beyond the jump threshold gives `jump`.
- Interior growth beyond the encroachment tolerance gives `bow_in` when a
  contiguous group covers the configured fraction of samples and is smooth.
  Smooth means adjacent excess differences are at most `max(3 px, 0.25 * peak)`.
  Narrow or ragged groups give `dark_merge`, requiring inspection.
- Far-edge retreat or changing tilt gives `far_retreat` or `tilt`; a constant
  tilt beyond tolerance gives `static_tilt`. These are ambiguous inspection leads.
- Both far columns retreating beyond tolerance gives `bar_opening`. Its exposed
  band is retained as `raw_overlap_fraction` but `overlap_fraction` becomes zero.
  This heuristic can mislabel an object covering both far columns.
- Overlap is the non-black fraction of the central bar band, excluding the edge
  margin. Intervals include frames strictly above `--overlap-threshold`.
  `starts_overlapping` means opening overlap exceeds the configured tolerance;
  `overlap_too_continuous` means overall frame duty exceeds its limit.
  Equality with those limits is allowed. No measured overlap gives `absent`;
  undetected bars give `not_applicable`.
- Dark subjects may be invisible to overlap measurement; dark scenery can merge
  with bars, while flare and background light can masquerade as overlap. Neither
  direction nor shape proves object identity or the cause of apparent motion.
- Side bars, identity, limb continuity, required crossings and camera lock are
  not checked automatically. A median reference can hide persistent deformation.

The report retains `frames`, `overlap_intervals`, thickness in pixels and percent,
edge rows, tilt, encroachment, retreat, overlap counts, `violations`, `inspect`
records and flags. Records carry bar, kind, severity, timestamps, count and peak.
Effective settings are recorded in `parameters` and gate tolerance/limit fields.

## Delivery Copy

Probe the actual output codec and container. If the destination needs a browser
copy, the caller can prepare faststart H.264/AAC and verify that copy separately.
Do not assume all masters share an encoding or transfer calibration between copies.
