# Motion Comparison Prompt — generated-take diagnosis

Use this optional `seed_understand` pass only after a generated take exists and
playback has identified a motion mismatch that needs diagnosis. The source pin's
per-beat motion grammar already comes from the initial combined breakdown
(`VideoBreakdown` v1.1). Feed the approved shot list and its analysis SHA-256
with the prompt, the pin as `@Video 1`, and the generated take as `@Video 2`.
Set `mode: comparison`.

```text
You are a senior motion designer and video analyst. Compare the source pin
(`@Video 1`) with the generated take (`@Video 2`) frame by frame. Treat the
source breakdown as the approved timing contract.

Use the supplied shot boundaries without renumbering them. In each result,
describe source motion from `@Video 1`; report missing or incorrect take motion
from `@Video 2` relative to that source. For EACH shot report:
1. time range
2. what is in the shot (subjects, background elements, effects)
3. every moving element with its motion type (translate/rotate/scale/parallax/
   drift/float-bob/pulse/flicker/color-cycle/twinkle/shimmer/sway/wave/slide/
   zoom/rotation), direction, speed, amplitude, easing, and loop period
4. camera motion (static/dolly/push/pan/tilt/rotate/shake) — be explicit when
   the camera is truly static and only elements move
5. light/color motion (pulse, strobe, flicker, hue cycle, blink, bloom, shimmer)
   and its rate
6. the single strongest motion cue that makes the shot feel alive

Separate direct observation from uncertain estimates. Give each shot a
low/medium/high confidence and list uncertainty whenever confidence is not high.
Then list the top concrete imperative prompt wording (positive only — say what
moves and how, never negative phrasing) to reproduce the same movement in a
Seedance 2.5 prompt.

Return JSON only, conforming to motion-review-schema.json. Key every result by
shot_index.
```

Legacy breakdowns at `VideoBreakdown` v1.0 may use `mode: source` only when the
user requests a separate motion analysis. For current runs, do not repeat the
pin-only pass. In comparison mode, add per-shot `missing_or_wrong` and
`concrete_fix_prompt_text`, plus `global_diffs` for pace/cut timing, energy
level, and the relevant aesthetic.

## Merge contract

- Write the exact JSON output to `templates/<template-id>/motion-review.json`
  and a readable rendering to `motion-review.md`.
- Validate it with `scripts/validate_breakdown.py <analysis.json>
  --motion-review <motion-review.json>`.
- Align comparison findings by `shot_index`, never by array position. Keep the
  comparison as a separate QA artifact; do not overwrite the approved source
  `shots[].motion` from `VideoBreakdown` v1.1.
- Use concrete fix wording to revise the Seedance prompt; it is **prompt text**
  and must follow positive-only directing principles and pass the Seedance
  `prompt-review` gate before submission.
- Preserve the approved `analysis.vNN.json` bytes and bind their hash as the
  comparison's `source_breakdown_sha256`. A proposed source-analysis timing or
  action correction requires a new breakdown revision and affected gates; do
  not silently rewrite an approved decision.

## Reliability notes

- Pass a compact beat list (`index: start-end label`) instead of the full
  breakdown; the model only needs boundaries and a short label per beat.
- Add "Output STRICT valid JSON only: no fences, no trailing commas, escape
  double quotes inside strings, keep each string under 300 characters." Long
  free-text fields are the usual source of unparseable output.
- Start with `thinking=true, reasoning_effort=medium`. On a provider timeout or
  unparseable result, retry once with `thinking=false, temperature=0.1`. If the
  retry also fails, record the comparison as skipped with the reason and use
  standard playback QA against the source motion fields — do not block further
  work on the optional comparison.
- Comparison output may quote descriptions of source people or products.
  Re-author prompt wording with the project's own talent and products, and run
  the de-identification leak scan on the saved JSON.
