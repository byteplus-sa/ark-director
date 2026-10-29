# Execution Constraints

Cross-cutting Seedance 2.5 constraints that every preset recipe inherits.
`seedance-prompt-25` owns the prompt grammar and `ark-mcp` owns the tool
parameters; this file maps where recipes touch them, with the four flagged
presets resolved in detail. All parameters below are tool/API values — they
never appear in prompt text.

## Parameter map

| Parameter | Value and notes |
|---|---|
| `duration` | Integer seconds, 4–30; `-1` for auto. Integer only — no sub-second values. |
| `resolution` | `480p`, `720p`, `1080p`. Every new 2.5 generation uses explicit `"480p"` with boolean `draft: true` in every review mode; after passing review and selection, promote to a supported delivery target. Resolve capability or transport conflicts without plain-480p fallback. New 2.5 generations have no skip-draft override. For a 4K request follow the 4K routing in [routing.md](../../../contracts/routing.md). |
| `ratio` | `9:16` default for UGC unless the request says otherwise. Locked to the first image on first/last-frame tasks and auto-derived from the source on edit tasks — never set it there. |
| Locked camera | Locked-off selfie/posing and spectacle demos state the lock in the prompt and record `format_static_by_design`; the Seedance 2.5 tool exposes no `camera_fixed` field. |
| `generate_audio` | Enables the native audio track the recipes describe. It can leak music, chants or stray speech despite an "ambience only" line; check the track, and for an ambience-only result set `false` and add a Seed Audio bed in post (not frame-synced). |
| `watermark` | `false` by default (the tool supports the parameter). |
| `return_last_frame` | `true` chains a scene into the next one's `first_frame` — used by multi-shot and long lifestyle recipes. |
| `priority` | 0–9; leave unset unless the caller specifies. |

## Task types

`omni_reference_task_type` accepts `auto`, `reference`, `edit`, and `extend`
on 2.5.

- **R2V recipes omit it** — the provider auto-detects from the prompt and
  media. Do not set `reference` on recipes; its behavior beyond auto-detection
  is undocumented.
- **Structured edits use `edit`** (subject replacement, outfit switch, hair
  style, creature integration over footage). `edit_video` is a 2.0-only value
  and is rejected by 2.5 with `InvalidParameter.TaskTypeConstraint`.
- **Continuation uses `extend`** (beta; ratio is locked to the source and
  stripped client-side).
- **Footage with people.** `edit` and `extend` reject a source video that shows
  a realistic person, generated or real, with `PrivacyInformation` before any
  cost, unless each person is bound as an `asset://` Virtual Portrait or
  authorized asset. Submit that source muted (`generate_audio: false`) and add
  sound in post. Without assets, use the fresh-generation variant of the
  recipe; continue a long arc with new single-pass clips, not `extend`.

## Reference and duration caps

- Seedance 2.5 accepts up to 30 images, 10 videos, and 10 audios (50 materials
  total). Recipes use 1–4; extra slots stay available for the caller's own
  references.
- Edit tasks: source video under 20s with 1–5 references recommended. Output
  duration locks to the source (~±0.3s) and ratio derives from the source.
- Modes are mutually exclusive: never mix first/last-frame roles with an R2V
  reference bundle in one task.

## Flagged presets — resolutions

Four presets map to no single direct provider mode. Their canonical
resolutions:

### Group Photo — subject multiplication
Duplicates are forbidden inside edit tasks ("never a second or duplicated
copy" of a subject), so the multiply gag is **generation-only**: a single-pass
R2V describing the staged appearance of identical figures at timestamps.
Identity drift across figures is the main failure mode — QA every figure
against the identity reference. The reliable alternative for a real group
photo is distinct references per person.

### Gas Transformation — disintegration
No direct disintegration mode exists. Two supported approximations:
1. **Staged single-pass** — the dissolve into smoke is written as an explicit
   end state ("by @9s only smoke remains"), with the dissolution spreading
   across named body regions at timestamps.
2. **Object-morph transition grammar** — "corresponding shapes, materials,
   transformation process," used when the vanish bridges two states.
QA the final frame: it must read as the intended vanish, not a corrupt frame.

### Timelapse Human — frozen subject, moving crowd
No crowd-freeze or timelapse-speed parameter exists. Approximation: state the
subject's stillness explicitly ("stands perfectly still, motionless for the
full duration") while background pedestrians move constantly at fast frequency
with motion blur, on a locked-off camera stated in the prompt. QA that the subject
actually holds — any subject drift breaks the effect.

### Morning routine — over-30s arc
Two supported paths:
1. **Compress** the arc into a ≤30s staged three-beat version (default in the
   recipe).
2. **Chain** three ~10s scenes via `return_last_frame: true` → `first_frame`,
   with matched aspect ratios and wardrobe continuity across scenes.

## Cross-cutting QA

- **Phone screens (selfie presets).** Avoid the picture-in-picture prior:
  describe the screen or mirror image positively, or attach a deterministic
  mockup as `@Image N`; never expect a rendered UI.
- **Labels and packaging (eating/product).** A branded item takes its prop
  reference and its label is inspected in the take. Unreferenced cups, jars,
  tubes, cases, slates and neck labels invent lettering: describe them plain
  ("smooth surface, nothing printed") or leave them out. Overlay text (prices,
  captions, CTA) is a finishing layer (FFmpeg or HyperFrames).
- **Counts (group, rain, clones).** Counts drop or overshoot. State the exact
  number and each position at every timestamp, keep counted items in open view
  from the first frame, never mention spares, and count on a full-size frame.
- **Hands.** The model reads left/right as the subject's own side; name each
  hand by anatomy plus frame side ("his right hand, frame-left").
- **Spoken lines.** Presets are mostly non-verbal; when a line is added, budget
  measured delivery or a native-language-informed read with pauses, onset and
  tail. Words / 2.2 is an English planning estimate, not a universal rejection
  rule. Initially allow 0.5-1.5 s onset and at least 0.4 s tail, then verify
  actual delivery; without evidence, fit is provisional. Preserve approved
  text; propose retiming or splitting before an authorized rewrite.
- **Spatial continuity (action).** Name the start point, travel axis,
  boundary, and end state; never demand impossible movement frequencies.
- **Keyframe chains (multi-shot).** First and last images must share an aspect
  ratio; ordered multi-keyframe images are preferred over grids.
- **High-burst caution (creative heuristic, not a provider limit).** Describe
  speed, amplitude, contact, debris paths and recovery from source intent.
  Preserve requested energetic explosions, splashes and jumps; assess
  plausibility and required readability. Moderate dynamics or reduced debris
  are optional repairs for demonstrated failures, not a universal energy cap.
- **Generation parameters stay in the API.** Duration, resolution, ratio, and
  watermark never go in the prompt text.
