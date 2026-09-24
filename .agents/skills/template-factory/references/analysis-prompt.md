# Analysis Prompt — `seed_understand` breakdown and motion

The canonical single `seed_understand` pass for source picture analysis. It
returns a reproducible, slot-complete `VideoBreakdown` with per-beat motion
grammar, so the factory does not need a second source-motion pass.

## Brand and identity mode

Choose one mode before running the analysis prompt. Record the mode in the
project brief / analysis metadata.

| Mode | When | Brand / logo treatment | People |
| --- | --- | --- | --- |
| **De-identify (default)** | Brand unknown, unauthorized, or style-only replication | Replace brand text and logos with placeholder descriptions | Describe appearance only; never name or likeness-match |
| **Authorized real brand** | User supplies or authorizes a specific brand/product | Preserve real brand and product identity in descriptors so later acquisition can match official assets | Still de-identify real people unless the user explicitly supplies approved talent identity |

After analysis, authorized real brands follow the download-first acquisition
order in the [element identification](../../../contracts/element-identification.md)
contract. Do not Seedream a fake packshot or logo when a usable official asset
can be acquired.

## Segmentation granularity: beats by default

Each `shots[]` entry is a **beat**, not only a hard cut. Cut-only breakdowns
(one entry per edit) are too coarse to reproduce motion and were rejected in
practice. Start a new beat at every hard cut **and** at every change of action
phase, camera move onset/stop/direction, focus, on-screen text or graphic,
VFX event, lighting, or subject entry/exit. Target 0.3–1.0 s beats, never
longer than 1.2 s. Rough density: ~1.2–1.6 beats per second of picture.
Each beat's `camera` field begins with `[HARD CUT IN]` or `[CONTINUOUS]`, so
"shot boundaries" for clip splitting and assembly are the `[HARD CUT IN]`
beats. Use cut-level segmentation only when the user explicitly asks for it.

## Measure before you ask (required pre-step)

`seed_understand` cut times drift by 0.2–0.6 s. Before the analysis call:

1. Read the **picture** duration from the video stream, not the container
   (`ffprobe -select_streams v:0 -show_entries stream=duration`). Audio
   padding commonly makes the container 0.1–0.25 s longer. Use the picture
   duration everywhere: prompt `{DUR}`, `--source-duration-s`, clip length.
2. Detect hard cuts: `ffmpeg -i pin.mp4 -vf "select='gt(scene,0.08)',metadata=print" -f null -`
   and keep scores ≥ ~0.25 as cuts; inspect lower scores on the strip.
3. Build a timestamped frame strip (5–8 fps) and look at it. Feed the
   measured cuts into the prompt as `{CUTS}`; after the call, correct beat
   boundaries against the strip and record the correction in `breakdown.md`.

```text
You are a film-analysis expert. Analyze the attached video and produce a JSON
object that fully describes how to REPRODUCE its style, composition, and grammar.

RULES
- Output valid JSON only. No prose outside the JSON, no markdown fences.
- People: describe a person's appearance (age, build, hair, clothing) but NEVER
  name them, infer a real identity, or likeness-match a celebrity unless the
  caller explicitly authorized a supplied talent identity.
- Brands (apply the selected mode):
  - De-identify mode: NEVER reproduce text/logos that identify real brands and
    NEVER quote on-screen copy, taglines or captions verbatim — describe them
    by role, typography, position and word count, e.g. "[two-word script tagline]".
  - Authorized real brand mode: preserve the authorized brand and product
    identity in element descriptors (exact logo/packshot cues the downstream
    acquisition step can match). Do not invent alternate brand marks.
- Say what you want positively; describe what IS shown, not what to avoid.
- Each entry in "shots" is a BEAT. Start a new beat at every hard cut AND at
  every change of action phase, camera move, focus, on-screen text/graphic,
  VFX, lighting, or subject entering/leaving frame. Beats are 0.3-1.0 s, never
  over 1.2 s. This {DUR}-second video should have roughly {TARGET} beats.
- Beats are contiguous: index starts at 1, each start_s equals the previous
  end_s, the last end_s equals {DUR}; duration_s = end_s - start_s.
- Begin every "camera" field with "[HARD CUT IN]" or "[CONTINUOUS]".
- Measured hard cuts (trust these): {CUTS}.
- "composition": exact frame placement (thirds, % of frame height, fg/mg/bg,
  subject scale). "action": concrete visible micro-actions. "end_state": the
  exact observable state at end_s.
- For every beat, describe motion in a nested "motion" object. Distinguish
  camera movement from element movement. For every significant moving element,
  report its visible motion, direction, relative speed and amplitude, easing,
  and loop period only when a repeat is observable; otherwise use null. Name
  static camera and lighting behavior explicitly. Identify the strongest motion
  cue, give confidence, list uncertainty for low/medium confidence, and write a
  concise positive directing instruction. Use qualitative estimates; do not
  invent measured speed, physical distance, or cycle timing.
- Use a unique name for each moving element within a beat; combine multiple
  phases of the same element in one entry.
- A truly static beat has an empty "moving_elements" array and says the camera
  is static. Its directing instruction should preserve that stillness. Do not
  invent motion to fill the field.
- Identify every distinct character, location, prop, screen graphic and VFX
  treatment. Assign each a short kebab-case id, a tag equal to "@" + id
  (e.g. "@ice-bed"), and an exhaustive visual descriptor. "keyframe_index" and
  "in_shots" are ARRAYS of existing beat indices; every keyframe is in in_shots.
- camera.shot_sizes, camera.moves, camera.transitions and audio.sfx are ARRAYS
  of strings. Treat this pass's audio description as provisional. If the
  soundtrack is not demonstrably available to the model, set audio.mode to
  "unverified", music and dialogue to null, sfx to [], and every shots[].audio
  to "unverified". Never infer silence from a video-only input or transcribe
  dialogue without listening or ASR verification. The separate reference-audio
  analysis supplies the verified sound map.

Return this schema:
{
  "schema_version": "1.1",
  "title": string,
  "genre": string,
  "visual_style": {"grade", "lighting_direction", "lens", "film_look"},
  "camera": {"shot_sizes": [str], "moves": [str], "framing": str, "transitions": [str]},
  "audio": {"mode": str, "music": str|null, "sfx": [str], "dialogue": str|null},
  "elements": [{ "type": "character|location|prop|screen", "id", "tag": "@id",
                 "descriptor", "keyframe_index": [int], "in_shots": [int] }],
  "shots": [{ "index", "start_s", "end_s", "duration_s", "composition",
              "camera", "action", "lighting", "audio", "end_state",
              "motion": {
                "camera_motion": string,
                "moving_elements": [{ "name", "motion", "direction", "speed",
                                      "amplitude", "easing", "loop_period": string|null }],
                "light_motion": string,
                "strongest_cue": string,
                "confidence": "low|medium|high",
                "uncertain_estimates": [string],
                "directing_prompt_text": string
              }}]
}
```

## Call parameters

```json
{
  "videos": [{ "kind": "url", "url": "<presigned pin url>" }],
  "prompt": "<analysis prompt above, with mode, {DUR}, {TARGET}, {CUTS} filled>",
  "temperature": 0.2,
  "thinking": true,
  "reasoning_effort": "high",
  "max_tokens": 32768
}
```

Notes:
- Video inputs must be HTTPS URLs (Base64 unsupported) — upload via
  `media_upload` first and pass the presigned URL.
- Beat-level analysis benefits from `thinking=true`; cut-level analysis can use
  `thinking=false` for speed.
- Results are large because every beat includes motion detail (the text payload
  may be duplicated in `structured_content` and include `reasoning_content`).
  Keep descriptions concise. When the tool result is persisted to a file, parse
  `result.structured_content.choices[0].content` with a script instead of
  retyping JSON by hand. If output is truncated, retry the same combined prompt
  with shorter field descriptions; do not omit motion from later beats.
- Validate against `breakdown-schema.json`, then run
  `scripts/validate_breakdown.py <analysis.json> --source-duration-s <picture seconds>`.
  On parse failure, retry once with an explicit "return JSON only, no markdown
  fences" correction. On other validation failures, retry once with the exact
  findings as repair constraints, or normalize mechanically (scalar→array,
  `@id` tags) and record the normalization. Never proceed with an invalid
  breakdown.

## De-identification leak scan (required in de-identify mode)

Models recognize famous brands and quote their copy even when told not to.
After the combined analysis response, grep the saved JSON for the source brand
names, product names and any on-screen copy visible in the frame strip. Replace
every hit with a role placeholder before freezing the revision. Keep the scan
list in `breakdown.md`.
