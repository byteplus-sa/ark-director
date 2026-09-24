---
name: template-factory
description: >-
  Reverse-engineer a reference video ("pin") into reproducible AIGC output.
  Orchestrates pin intake (prefer a public HTTPS URL seed_understand can watch;
  download and media_upload only when unusable), video and audio breakdown,
  per-beat motion analysis, keyframes, dynamic sketch storyboard, optional
  element sheets
  (Seedream for invented identity; web/user download-first for authorized real
  brands/logos/products; deterministic HTML-entrypoint graphics for exact posters, cards,
  screens, product layouts, and overlays), and a Seedance 2.5 video —
  generation-bound prompts through prompt-review; stages on the showcase-html
  canvas. Explicit orchestrator composing ark-mcp (including
  seed_audio_understand), seedream-storyboard,
  seedance-prompt-25, prompt-review, html-graphic-render, hyperframes,
  showcase-html, and ffmpeg; never calls the Ark REST API. Use to
  replicate style/composition/grammar, build a reusable template, or turn a
  cited brand ad, Pinterest pin, or other reference video into elements and
  video.
---

# Template Factory

Turn a reference video ("pin") into reproducible AIGC output through a reusable
"template" (the recipe). One run produces: a `VideoBreakdown`, a timestamped
reference-audio analysis when sound is available, a sketch storyboard, optional
element sheets, and a Seedance 2.5 video take — all
manifested for later reproduction.

This skill is an **explicitly-marked orchestrator** (precedent: `film-production`).
It composes MCP tools + specialist skills; it never calls the Ark REST API
directly.

Follow the implementation structure in `plans/PLAN_TEMPLATE_FACTORY.md`, with
the current workspace contracts taking precedence where the plan is stale.

## Core operating model

- Act as the single manager communicating with the user.
- Treat `project.md`, `task_ids.json`, `ref_cache.json`, shot manifests and the
  persistent `showcase.json`/`index.html` production canvas as production memory.
- Never infer approval from technical success. An output enters `review`, then
  only a passing inspection and mode-authorized decision can set `approved`.
- **Every generation-bound prompt this factory submits — Seedream storyboard,
  Seedream element sheet, or Seedance video — must pass the `prompt-review`
  gate first.** Acquired brand/product/logo assets (`generation: none`) skip
  prompt-review. Deterministic static graphics (`generation:
  deterministic_html`) also skip prompt-review and provider registration. Both
  still need hashes, canvas listing, visible QA, and explicit selection.
- Replicate style, composition, and grammar. Do not clone copyrighted footage.
  De-identify real people in analysis. For brands: de-identify when unknown or
  unauthorized; when the user authorizes a real brand, preserve that identity and
  acquire official/authorized packshots or logos before inventing them with
  Seedream (see [element identification](../../contracts/element-identification.md)).
- Default `watermark: false` only where the selected live tool supports the
  parameter, unless the user requests otherwise.
- Initialize the eight-stage HTML canvas at intake. After every numbered step,
  update its stage sources/sections, regenerate `index.html`, and pass the
  matching `--check --stage` checkpoint before advancing.
- Resolve live model and operation capabilities before authoring request-bound
  parameters or reference roles. Defaults remain proposals until accepted.

## Pipeline (one stage at a time)

```text
pin_uploaded → breakdown_draft → breakdown_approved → elements_draft
  → elements_approved → storyboard_draft
  → storyboard_approved → video_draft → video_review → approved
```

1. **Pin intake** — resolve watchable media for the pin before analysis.
   Prefer a public HTTPS URL that `seed_understand` already accepts as a video
   input. Download into `pins/` and `media_upload` only when the cited link is a
   page/platform URL, auth-gated, or otherwise unusable as a video input (use an
   available downloader such as `yt-dlp` when present). User-supplied local files
   always upload. Record `object_key` (when uploaded), content SHA-256, source
   URL, and storage scope in `ref_cache.json`. Re-presign unchanged cached
   objects on demand; re-upload only if content changed or the recorded remote
   object is missing. Do not treat transcripts, scripts, or article write-ups as
   the pin.
2. **Analysis** — first measure the pin: picture (video-stream) duration,
   ffmpeg scene-detected hard cuts, and a 5–8 fps timestamped frame strip.
   Then make one `seed_understand` call with the template's combined picture
   and motion prompt (`references/analysis-prompt.md`), which segments into
   **beats by default** (0.3–1.2 s, every cut plus every action/camera/text/VFX
   change, each tagged `[HARD CUT IN]` or `[CONTINUOUS]`) and returns per-beat
   motion grammar in `VideoBreakdown` v1.1. The validator still accepts legacy
   v1.0 breakdowns. Parse large results from the persisted tool-result file
   with a script. Correct
   beat boundaries against the frame strip, run the de-identification leak
   scan, validate `VideoBreakdown` against `references/breakdown-schema.json`,
   and run `scripts/validate_breakdown.py --source-duration-s <picture
   duration>` → write `analysis.json` + `breakdown.md` (one keyframe per beat,
   corrections recorded). Freeze the reviewed source as `analysis.vNN.json`;
   record its SHA-256 and approval scope. Gate A: user reviews the breakdown.
   Use cut-level segmentation only when the user asks for it.
3. **Reference audio analysis** — this remains a separate audio-only review;
   follow `references/audio-analysis.md`. Probe the original pin's audio stream
   and measure silence/loudness. Extract the soundtrack, then submit it to
   `ark-mcp` (`seed_audio_understand`) as a background job. Record the response
   or review-note reference in `auditory_review`. A playable UI and FFmpeg output
   alone do not show that the agent heard the soundtrack. When no auditory
   review is available, leave sound identity and reusable audio grammar
   unresolved. Build `audio-analysis.json` with timestamped music, voice, effect,
   ambience, silence, and tail events, plus evidence, confidence, and overlapping
   visual beat indices. Use ASR only when speech matters; use stem separation
   only when the mix obscures needed evidence. Validate against
   `references/audio-analysis-schema.json` with the pin SHA-256 and frozen
   breakdown SHA-256. An absent stream and unavailable audio are distinct
   states. Do not assume `seed_understand` heard the soundtrack merely because
   it accepted a video. Carry only reusable sound grammar and sync rules into
   the template; keep source recordings and words out of it.
4. **Keyframes** — `ffmpeg` extracts a frame per beat (mid-beat, or the flagged
   element keyframe) into `keyframes/`. Seek after `-i` (accurate seek) so
   beats near the end of the picture still decode.
5. **Elements** — identify required canonical inputs from the draft breakdown.
   Use the workspace prop threshold: branded, recurring, story-critical, or
   scene-variant wearables need a separate locked reference; incidental objects
   may be described in text. Classify each static element before production:
   acquire official/user assets for authorized brands, logos, and products; use
   deterministic HTML-entrypoint graphics for exact copy, typography, screen/UI, title
   cards, posters, product lineups, price/CTA treatments, and simple geometry;
   use Seedream for invented characters, locations, photography, illustration,
   and expressive imagery; use a hybrid when selected imagery needs
   deterministic type/layout. Promote acquired files with `source:
   web_download` or `user_supplied` and `generation: none`. Promote
   deterministic renders with `source: deterministic_render`, `generation:
   deterministic_html`, editable source, render record, input/font hashes,
   dimensions, and alpha intent. Do not Seedream a fake packshot/logo or ask it
   to reproduce exact graphic geometry. For generative sheets, create the
   user-requested number of variants, or 3 by default, after prompt review. One
   deterministic specification produces one exact version. Persist
   `selected_variant` only after a mode-authorized, hash-bound choice.
6. **Storyboard** — after relevant Elements are approved, write a dynamic
   production board via `seedream-storyboard`, one panel per beat unless the
   user sets a panel budget. Review the prompt and generate the requested count,
   or 3 variants by default, using distinct seeds only when supported. Paginate
   large boards into readable grids while preserving one ordered panel plan. A
   monochrome analysis sketch is control-only: translate its blocking into text
   and omit it from video inputs by default. A production panel can be promoted
   only after explicit selection, source-hash validation, and a supported image
   mode.

7. **Video** — use current capability evidence to choose one supported clip or
   multiple natural-duration shots plus assembly. Compose the Seedance 2.5
   six-part prompt from breakdown + eligible board directions + per-beat motion
   grammar + verified audio grammar and sync cues when audio is requested +
   element sheets (via `seedance-prompt-25`), run `prompt-review`, persist the
   prepared request, then submit via the supported durable transport. Prefer
   `seedance_2_5_create_task`; use an equivalent Ark CLI route only before any
   ambiguous submission and only when it satisfies the same contract. Persist
   the task id, poll, download, and run technical and playback QA. Keep exact
   brand copy, logos and captions out of the video prompt ("no on-screen text",
   leave clean space) and composite them afterwards as deterministic
   `html-graphic-render` overlays (ffmpeg `overlay` with a short alpha fade).
   Expect Seedance to stretch dense beat timelines by roughly 0.5–1.2 s; a
   stronger timing prompt rarely fixes it. When a take's beats land late, retime
   in the edit (trim a held tail, clone-pad the final hold, crossfade audio)
   rather than regenerating, and record the edit operations on the take.
   Measure take loudness and normalise delivery masters (e.g. `loudnorm`
   -16 LUFS / -1.5 dBTP) after mode-authorized take locks.
8. **Review** — compare the reference and take in playback for shot timing,
   motion direction and intensity, action progression, camera movement,
   transitions, opening/ending state, and requested audio arc. Add the pin and
   every take as playable players on the `shot-generation` canvas in one
   `kind: "takes"` group (`groups[].takes[].media` as `{type, src}` — never
   flat `cards` or string media paths); include exact prompt, ordered
   references and QA evidence; regenerate/open the page, pass its stage
   freshness check, and set `review`. If playback finds a motion mismatch that
   needs diagnosis, use `references/motion-review-prompt.md` in comparison mode
   against the generated take; do not rerun source-motion analysis. Apply the project
   mode: the agent may choose a passing take with a recorded decision in `approve_for_me`; in
   `ask_for_approval`, display the recommendation and await the user.

### Competitor or category reference pins

When pins are other brands' ads used as a style reference: keep the analysis
in de-identify mode, never bind the pin video (or its frames) as a video
reference, give original talent wardrobe and colours clearly distinct from the
people in the pin (prompt-review checks this), and never carry over the pin's
taglines, typography or trade dress. Replace the product slot with the
authorized brand's official packshot.

### Still / poster track

Reference stills (photos, key visuals) run as a parallel poster track, not as
video pins: describe the still's camera angle, pose, lens and grade in text,
bind only the official product packshot as `@Image 1` (I2I), write the prompt
under `posters/<id>/`, pass prompt-review, generate 3 variants, and add any
logo or copy as a deterministic overlay. List variants on the canvas as
selectable cards with a `poster.md` manifest.

## Route specialist work

| Need | Primary skill |
| --- | --- |
| Pin download when URL is not seed_understand-usable | Available downloader (e.g. `yt-dlp`); then `ark-mcp` (`media_upload`) |
| Upload / presign references | `ark-mcp` (`media_upload`, `media_presign`) |
| Video breakdown + per-beat motion grammar | One `ark-mcp` (`seed_understand`) call |
| Generated-take motion diagnosis when needed | `ark-mcp` (`seed_understand`) comparison pass |
| Auditory review of a pin with sound | `ark-mcp` (`seed_audio_understand`) on the extracted soundtrack, or documented human listening review |
| Reference audio stream, silence, loudness, and waveform | `ffmpeg` (`ffprobe`, audio filters) |
| Speech transcription when needed | `ark-mcp` (`speech_to_text`), then listening verification |
| Voice/music/effect separation when needed | `ark-mcp` (`vod_separate_audio`, `vod_get_audio_separation`), then listening verification |
| Keyframe extraction, cut detection, frame strips, end-card compositing, retiming, loudness | `ffmpeg` |
| Storyboard grid prompt | `seedream-storyboard` |
| Element sheets (invented / generative) | `seedream-character-sheet`, `seedream-location-asset`, `seedream-prompt` |
| Brand / logo / product packshot | Web or user download first per element-identification; Seedream only as fallback |
| Exact typography, screen/UI, title/end card, poster, product lineup, price/CTA, or static overlay | `html-graphic-render` |
| Generative image with exact copy/layout | Select the generated image, then finish with `html-graphic-render` |
| Animated exact graphic | HyperFrames; FFmpeg or HyperFrames for final video composition |
| Seedance 2.5 video prompt | `seedance-prompt-25` |
| Prompt quality gate (generation-bound only) | `prompt-review` |
| Persistent stage canvas and visual review | `showcase-html` |

## Canvas stage mapping

| Factory work | Canvas stage | Exit evidence |
| --- | --- | --- |
| Pin intake and template intent | `brief-development` | source hash, constraints, recipe target |
| Analysis and keyframes | `scene-breakdown` | valid VideoBreakdown v1.1 with per-beat motion, audio sound map or absence/unavailability record, approved revision |
| Element acquisition/generation/rendering and selection | `canon-elements` | hashes, explicit selections; acquired, generated, or deterministic variants |
| Storyboard generation and selection | `storyboard-visual-plan` | ordered panels, prompts, eligibility state |
| Audio decision | `audio-preparation` | sound map translated into requested assets and timing, or `skipped` with reason |
| Video generation and take review | `shot-generation` | prepared requests, task provenance, pin + take players in one `takes` group, QA |
| Multi-shot edit and final review | `assembly-review` | approved inputs and inspected assembly, or `skipped` for one clip |
| Final output | `delivery` | master/proxy hashes and approval, or `skipped` when outside scope |

Combined visual and motion analysis, separate audio analysis, and keyframes
update the same `scene-breakdown` stage;
run its freshness check after each material update. Mark optional stages
`skipped` explicitly before advancing so no earlier stage remains pending.

## Capability and request preflight

Before freezing a generation request, resolve the current model binding,
operation, duration range, resolution, reference count and roles, supported
image mode, seed support, audio support, and optional flags. Record the evidence
source and verification time. Then freeze the prompt and ordered references and
run the workspace request validator. If the requested duration exceeds one
supported clip, split on shot boundaries, generate natural-duration clips, and
assemble approved takes; do not compress the whole template into an unsupported
duration.

## Storyboard rules

- **Dynamic panel count by default** — one panel per identified beat. Honor an
  explicit user panel budget and preserve all shot-to-panel coverage decisions.
  Use the smallest readable grid and paginate large boards.
- **Sketch by default** — use colorless pencil/ink as a composition/order anchor.
  Honor an explicit request for a limited palette, full color, or standalone
  production panels and record that decision in the manifest.
- **3 variants by default** — honor an explicit requested count. Keep prompt,
  references, model, and effective parameters identical across sampling variants;
  vary only a supported stochastic seed.
- **Video eligibility** — production panels need mode-authorized selection and
  current canonical source hashes. Control sketches are omitted by default;
  an intentional conditioning exception requires explicit selection, supported
  tool inputs, and artifact-specific QA. Bind only eligible inputs.

- **Paginated boards bind the same ordered reference set on every page** so
  `@Image N` numbering never shifts between pages; say which references a page
  does not use instead of dropping them from the upload.

## Selection gate

Storyboard variant selection follows `project.md` approval mode.
`storyboard.review: false` disables the review UI only; it does not remove QA
or the validated decision. In `approve_for_me`, inspect and rank candidates,
record a passing hash-bound review and agent decision, then select. In
`ask_for_approval`, store a suggestion under `recommended_variant`, keep
`status: review`, and wait for the user's choice before video promotion.
Neither a recommendation nor technical success alone writes `selected_variant`
or `approved`. Regenerate and inspect `index.html` and pass the stage freshness
check after the decision in either mode.

## Prompt review gates (generation-bound)

Before any **generation** call, run `prompt-review`:

- Seedream storyboard grid prompt (before `seedream_generate_image`)
- Seedream element sheet prompts (before each sheet generation)
- Seedance video prompt, including per-beat motion wording from
  `VideoBreakdown.shots[].motion.directing_prompt_text`
  (before `seedance_2_5_create_task`)

CRITICAL/MAJOR findings must be fixed before submission. Skip this gate for
acquired brand/product/logo assets and deterministic HTML-entrypoint renders that
have no generation prompt. Deterministic renders still require source/output
hashing, exact-copy, font, layout, dimension, alpha, thumbnail-legibility,
canvas, and selection checks.

## Reusable recipe contract

Validate every committed template against `references/template-schema.json`.
Keep the recipe distinct from a particular run:

- `locked_grammar` contains the reusable style, composition, motion,
  transition, rhythm, and optional audio rules that define the template.
- `replaceable_inputs` declares subject, product, environment, palette, copy,
  and other slots the caller may substitute, including constraints.
- `adaptation_rules` explains how duration, aspect ratio, audio, and shot-count
  changes preserve the grammar.

Never bundle source media, historical approval, identities, brands, or signed
URLs into the reusable recipe. A new run must resolve and approve its own canon.

## Revisions

Write every revision as: locked decisions, requested delta, acceptance criteria,
known rejections, invalidation scope. Change one of prompt wording, reference
bundle, or motion design at a time.

## File layout

Skill (committed):

```text
.agents/skills/template-factory/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── analysis-prompt.md
│   ├── motion-review-prompt.md
│   ├── audio-analysis.md
│   ├── breakdown-schema.json
│   ├── motion-review-schema.json
│   ├── audio-analysis-schema.json
│   ├── template-schema.json
│   ├── slot-mapping.md
│   └── templates/
│       ├── index.json
│       └── <template-id>/template.md + template.json
├── scripts/validate_breakdown.py
└── evals/evals.json
```

Run (local-only, project-scoped):

```text
projects/<project>/
├── pins/                     # downloaded reference videos
├── project.md, task_ids.json, ref_cache.json
├── templates/<template-id>/
│   ├── analysis.json, analysis.vNN.json, breakdown.md
│   ├── audio-analysis.json, audio-analysis.md
│   ├── motion-review.json, motion-review.md (only for generated-take comparison)
│   └── keyframes/
├── elements/<id>/
└── scenes/scene-01/...
```

## Submission recovery

Persist each exact prompt snapshot and reviewed prepared request in the project
registry before submitting. Record the provider task ID as soon as available.
An ambiguous timeout leaves `submission_unknown`: reconcile that operation or
resume its known task; never repeat submission automatically or switch transport
to submit a duplicate. Any new authorized take gets a new operation record.

## Intentional conditioning representation

A sketch or blockout stays `control_only: true` while it is analysis-only. To
use intentional conditioning, first obtain explicit selection of a derived
composition or motion reference. Record its exact selected manifest, current
SHA-256, `reference_image` or `reference_video` role, and `control_only: false`.
Confirm live model/mode support. Flipping the flag alone never grants approval;
the caller applies the [production policy](../../contracts/production-policy.md).
