---
name: template-factory
description: Reverse-engineer reference videos with native-agent analysis and available tool fallbacks. Use to build reusable style and motion recipes, then orchestrate reviewed assets and video generation.
---

# Template Factory

Turn a reference video ("pin") into reproducible AIGC output through a reusable
"template" (the recipe). One run produces: a `VideoBreakdown`, a timestamped
reference-audio analysis when sound is available, a sketch storyboard, optional
element sheets, and a Seedance 2.5 video take — all
manifested for later reproduction.

This skill is an **explicitly-marked orchestrator** (precedent: `film-production`).
The host agent owns analysis, synthesis, prompt writing and review using local
media and available perception tools. It composes specialist skills and
MCP analysis or generation tools; it never calls the Ark REST API directly.
Approval modes, Studio commands, stage gates, prompt review,
registration and submission recovery follow `AGENTS.md` and the
[production policy](../../contracts/production-policy.md); this skill adds the
factory-specific steps.

## Core operating model

- Act as the single manager communicating with the user.
- Establish whether the request is analysis-only, recipe/prompt-only, or a
  production run. For analysis-only work, stop after the validated breakdown
  and requested recipe; do not initialize Studio, generate assets, or demand
  production-stage locks. Studio and stage-exit instructions below apply to
  production runs. A recipe is not authorization to spend generation credits.
- Prefer the current host-agent session or a capable local LLM for visual,
  audio and motion reasoning. When native capabilities are insufficient, use
  available tools, including `ark-mcp` `seed_understand` for visual/motion
  analysis and `seed_audio_understand` for audio analysis. These are optional
  fallbacks, not mandatory dependencies. Available MCP tools may also assist
  with ASR, stem separation, media preparation and measurements; local ASR and
  separation are not required. Select tools
  by capability, availability and the user's privacy and cost constraints.
  Native reasoning needs no ModelArk credentials, uploads or provider task IDs;
  an optional provider tool still follows its own authentication, upload,
  authorization and persistence contracts. Do not require tool setup for
  unrelated analysis that the host can already perform.
  "Local" describes orchestration and media tooling, not a guarantee that the
  host model runs on-device. Respect an explicit offline-only constraint:
  use only verified on-device perception or human review in that case.
- Check actual image, video and audio input capabilities independently.
  A file-reading shell or player launch is not visual or auditory perception.
  Inspect extracted images when native video input is unavailable, or use an
  available visual-understanding tool. If no permitted route can inspect the
  picture, request human visual evidence and keep the breakdown incomplete.
  Never fill gaps from filenames or transcripts.
- Prefer native audio input or a capable local audio model; when unavailable,
  use an available audio-understanding tool or documented human listening.
  Missing perception leaves audio grammar unresolved only when no permitted
  reviewer/tool can inspect the sound. Record the fallback reason, actual
  tool/model, input hashes, inspected ranges and saved results. Do not report
  tool observations as native listening. Generation remains a separate,
  authorized provider operation with its existing review and registry gates.
- Treat `project.md`, `task_ids.json`, `ref_cache.json`, shot manifests and the
  Studio project (pre-Studio canvas projects: the `showcase.json`/`index.html`
  canvas) as production memory.
- Provider success is `review`; only a passing inspection and mode-authorized
  decision sets `approved`.
- **Every generation-bound prompt this factory submits — Seedream storyboard,
  Seedream element sheet, or Seedance video — passes `prompt-review` first**
  (see [Prompt review gates](#prompt-review-gates-generation-bound)).
- Replicate style, composition, and grammar. Do not clone copyrighted footage.
  De-identify real people in analysis. For brands: de-identify when unknown or
  unauthorized; when the user authorizes a real brand, preserve that identity and
  acquire official/authorized packshots or logos before inventing them with
  Seedream (see [element identification](../../contracts/element-identification.md)).
- Default `watermark: false` only where the selected live tool supports the
  parameter, unless the user requests otherwise.
- Set up the Studio project at intake. After every numbered step, update the
  manifests, run `studio_project.py sync`, and pass the stage-exit checks in the
  production policy before advancing. Pre-Studio canvas projects with `showcase.json` keep
  the eight-stage canvas and its matching `--check --stage` checkpoint.
- Resolve live model and operation capabilities before authoring request-bound
  parameters or reference roles. Defaults remain proposals until accepted.

## Pipeline (one stage at a time)

```text
pin_local → breakdown_draft → breakdown_approved → elements_draft
  → elements_approved → storyboard_draft
  → storyboard_approved → video_draft → video_review → approved
```

1. **Pin intake** — resolve a local, decodable copy before analysis.
   Reuse user-supplied files without changing them; download remote media into
   `pins/` with an available downloader such as `yt-dlp`. A page URL is not the
   video. Record the local path, bytes, content SHA-256 and nonsensitive source
   provenance in `breakdown.md`; omit credentials and signed query strings.
   Native inspection needs no upload. When a selected MCP operation needs
   media, reuse an accepted media URL or upload only its needed input under
   the applicable privacy and tool contracts. Cache transport references
   without making analysis media eligible for generation. Transcripts, scripts and
   article write-ups do not substitute for inspecting the media.
2. **Analysis** — first measure the pin: picture (video-stream) duration,
   ffmpeg scene-detected hard cuts, and a 5–8 fps timestamped frame strip.
   Inspect the picture with native video/image tools or a capable fallback and apply the
   analysis checklist (`references/analysis-prompt.md`), which segments into
   **beats by default** (0.3–1.2 s, every cut plus every action/camera/text/VFX
   change, each tagged `[HARD CUT IN]` or `[CONTINUOUS]`) and returns per-beat
   motion grammar in `VideoBreakdown` v1.1. The validator still accepts legacy
   v1.0 breakdowns. Record inspected timestamp ranges, frame files, runtime
   capabilities, measurements and uncertainty in `breakdown.md`. Correct
   beat boundaries against the frame strip, run the de-identification leak
   scan, validate `VideoBreakdown` against `references/breakdown-schema.json`,
   and run `scripts/validate_breakdown.py --source-duration-s <picture
   duration>` → write `analysis.json` + `breakdown.md` (one keyframe per beat,
   corrections recorded). Freeze the reviewed source as `analysis.vNN.json`;
   record its SHA-256 and approval scope. Gate A: review and record the
   decision under the project's approval mode.
   Use cut-level segmentation only when the user asks for it.
   For a pin longer than about 20 s or with more than about 25 beats, plan
   windowed analysis on hard cuts from the start; see
   [long pins and multi-clip takes](references/long-pins-and-multi-clip.md).
3. **Reference audio analysis** — this remains a separate audio-only review;
   follow `references/audio-analysis.md`. Probe the original pin's audio stream
   and measure silence/loudness. Extract the soundtrack, then inspect it through
   verified native audio input, a local audio model, an available
   audio-understanding tool, or human listening.
   Record the review-note reference in `auditory_review`. A playable UI and FFmpeg output
   alone do not show that the agent heard the soundtrack. When no auditory
   review is available, leave sound identity and reusable audio grammar
   unresolved. Build `audio-analysis.json` with timestamped music, voice, effect,
   ambience, silence, and tail events, plus evidence, confidence, and overlapping
   visual beat indices. Use ASR only when speech matters; use stem separation
   only when the mix obscures needed evidence. Validate against
   `references/audio-analysis-schema.json` with the pin SHA-256 and frozen
   breakdown SHA-256. An absent stream and unavailable audio are distinct
   states. Do not assume the host heard the soundtrack merely because
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
   large boards into readable grids while preserving one ordered panel plan.
   The board is a planning and review artifact: translate its blocking into
   prompt text and **never bind a board, grid or panel as a Seedance
   reference**: panel numbers, corner labels and the sketch look can leak into
   video.

7. **Video** — use current capability evidence to choose one supported clip or
   multiple natural-duration shots plus assembly. Compose the Seedance 2.5
   six-part prompt from breakdown + board staging written as text + per-beat
   motion grammar + verified audio grammar and sync cues when audio is
   requested + element sheets (via `seedance-prompt-25`), run `prompt-review`,
   persist the prepared request, then submit via the supported durable
   transport. Prefer `seedance_2_5_create_task`; use an equivalent Ark CLI route
   only before any ambiguous submission and only when it satisfies the same
   contract. Set the pin's ratio as a request parameter, never as a prompt
   sentence. Submit each clip as a 480p native Draft (`draft: true`), review it,
   then promote the selected Draft by `draft_task_id`; edit inputs only before
   the Draft. Persist the task id, poll, download, and run technical and
   playback QA, including frame samples with corner crops for leaked text. Keep
   exact brand copy, logos and captions out of the video prompt (plain, clean
   space) and composite them afterwards as deterministic `html-graphic-render`
   overlays (ffmpeg `overlay` with a short alpha fade).
   **Audio route:** when the pin's sound is score-led, ambient or a music bed,
   generate picture with `generate_audio: false` and rebuild the sound grammar
   with Seed Audio in post, because a "no speech" or "ambience only" line on
   native audio does not reliably keep speech or score out. Keep native audio for on-camera
   dialogue.
   Seedance can stretch dense beat timelines, and a stronger timing prompt does
   not reliably fix it. Measure the take's actual cuts. When its beats land late, retime
   in the edit (trim a held tail, clone-pad the final hold, crossfade audio)
   rather than regenerating, and record the edit operations on the take.
   Capture-format and texture looks in the pin (camcorder, film grain,
   scanlines, halation) are not reliably produced by prompt words; record them
   as a post treatment in the recipe and apply them only when the run locks
   them. Otherwise assemble in the takes' original colours with no grade,
   from exact-length intermediates encoded once. Measure take loudness and
   normalise delivery masters (e.g. `loudnorm` -16 LUFS / -1.5 dBTP) after
   mode-authorized take locks; place the result in Studio and deliver it with
   `studio_project.py render`.
   When the picture needs several clips, follow the shot budget, trim-point,
   state-ledger, and continuous-audio rules in
   [long pins and multi-clip takes](references/long-pins-and-multi-clip.md).
   Prepare each request with `.agents/scripts/prepare_request.py`. Composite
   timed overlays from a JSON timeline with
   `html-graphic-render/scripts/overlay_timeline.py`, timed to the take's
   measured cuts rather than the prompt timestamps.
8. **Review** — compare the reference and take in playback for shot timing,
   motion direction and intensity, action progression, camera movement,
   transitions, opening/ending state, and requested audio arc. Each take appears
   in its Studio frame and the pin is played from its file; include exact prompt,
   ordered references and QA evidence in the shot manifest; run `studio_project.py sync`, open the project
   in Studio, pass the stage-exit checks, and set `review`. Pre-Studio canvas: add
   the pin and takes as playable players on the `shot-generation` canvas in one
   `kind: "takes"` group (`groups[].takes[].media` as `{type, src}` — never
   flat `cards` or string media paths) and pass its stage freshness check. If playback finds a motion mismatch that
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

### Multi-pin batches

When the host supports sub-agents, run one native analysis sub-agent per pin,
each owning only `templates/<pin-id>/`, with explicit local input paths and
perception requirements. Otherwise process bounded windows in the main session.
The main agent integrates findings and owns shared state. Native reasoning creates no
provider registry entries; optional provider operations retain their required
task IDs and records. Generation registry writes still use the lock in
`.agents/scripts/operation_store.py`. See
[multi-pin batches](references/long-pins-and-multi-clip.md#multi-pin-batches).

### Still / poster track

Reference stills (photos, key visuals) run as a parallel poster track, not as
video pins: describe the still's camera angle, pose, lens and grade in text,
bind only the official product packshot as `@Image 1` (I2I), write the prompt
under `posters/<id>/`, pass prompt-review, generate 3 variants, and add any
logo or copy as a deterministic overlay. Record variants with a `poster.md`
manifest (pre-Studio canvas: selectable cards); Studio frames exist for shot
takes only.

## Route specialist work

| Need | Primary skill |
| --- | --- |
| Pin acquisition | Local file reuse or available downloader (e.g. `yt-dlp`); native inspection needs no upload |
| Upload / presign inputs for selected MCP operations or eligible generation references | `ark-mcp` (`media_upload`, `media_presign`); analysis upload does not grant generation eligibility |
| Video breakdown + per-beat motion grammar | Native host-agent/local LLM inspection plus FFmpeg measurements; `ark-mcp` `seed_understand` when native perception is insufficient |
| Generated-take motion diagnosis when needed | Native comparison of source/take media and timestamped frames; capable visual-understanding tool when needed |
| Auditory review of a pin with sound | Native audio input or capable local model first; `ark-mcp` `seed_audio_understand`, another audio-capable tool, or documented human listening when needed |
| Reference audio stream, silence, loudness, and waveform | `ffmpeg` (`ffprobe`, audio filters) |
| Speech transcription when needed for analysis | Available MCP ASR (e.g. `ark-mcp` `speech_to_text`) or local ASR; verify important words and timing where listening is available; transcripts alone do not verify soundscape |
| Voice/music/effect separation when needed for analysis | Available MCP separation (e.g. `ark-mcp` VOD separation) or local separator, then listening verification; unavailable tooling leaves uncertainty |
| Keyframe extraction, cut detection, frame strips, end-card compositing, retiming, loudness | `ffmpeg` |
| Storyboard grid prompt | `seedream-storyboard` |
| Element sheets (invented / generative) | `seedream-character-sheet`, `seedream-location-asset`, `seedream-prop-asset` |
| Brand / logo / product packshot | Web or user download first per element-identification; Seedream only as fallback |
| Exact typography, screen/UI, title/end card, poster, product lineup, price/CTA, or static overlay | `html-graphic-render` |
| Generative image with exact copy/layout | Select the generated image, then finish with `html-graphic-render` |
| Animated exact graphic | HyperFrames; FFmpeg or HyperFrames for final video composition |
| Seedance 2.5 video prompt | `seedance-prompt-25` |
| Prompt quality gate (generation-bound only) | `prompt-review` |
| Persistent Studio review surface for shot takes (pre-Studio canvas: stage canvas) | `studio_project.py` (pre-Studio canvas: `showcase-html`) |

## Stage mapping

The stage IDs below apply to Studio projects and pre-Studio canvas projects
alike; Studio projects add the stage-exit checks in the production policy.

| Factory work | Stage | Exit evidence |
| --- | --- | --- |
| Pin intake and template intent | `brief-development` | source hash, constraints, recipe target |
| Analysis and keyframes | `scene-breakdown` | valid VideoBreakdown v1.1 with per-beat motion, audio sound map or absence/unavailability record, approved revision |
| Element acquisition/generation/rendering and selection | `canon-elements` | hashes, explicit selections; acquired, generated, or deterministic variants |
| Storyboard generation and selection | `storyboard-visual-plan` | ordered panels, prompts, eligibility state |
| Audio decision | `audio-preparation` | sound map translated into requested assets and timing, or skipped with `stage skip audio-preparation --reason` |
| Video generation and take review | `shot-generation` | prepared requests, task provenance, a Studio frame per take (pre-Studio canvas: pin + take players in one `takes` group), QA |
| Multi-shot edit and final review | `assembly-review` | approved inputs and inspected assembly (a single clip is inspected as one take) |
| Final output | `delivery` | master/proxy hashes, approval and, in a Studio project, a delivery-level `render` record |

Combined visual and motion analysis, separate audio analysis, and keyframes
update the same `scene-breakdown` stage;
run its stage-exit check after each material update. Only
`storyboard-visual-plan` and `audio-preparation` may be skipped, with
`studio_project.py stage <project> skip <stage-id> --reason TEXT`; every other
stage is completed before advancing so no earlier stage remains pending.

## Capability and request preflight

Before freezing a generation request, resolve the current model binding,
operation, duration range, resolution, reference count and roles, supported
image mode, seed support, audio support, and optional flags. Record the evidence
source and verification time. Then freeze the prompt and ordered references and
run the workspace request validator. If the requested duration exceeds one
supported clip, split on shot boundaries, generate natural-duration clips, and
assemble approved takes; do not compress the whole template into an unsupported
duration.

Seedance 2.5 template runs default to 480p native Drafts for video drafts and
revisions, with the delivery resolution recorded as a separate project
decision. Promote only after passing draft review and mode-authorized selection
(including draft assembly review for multi-shot work), then re-inspect the
final: its audio is not identical to the Draft's. Honor explicit user overrides
and record verified operation constraints.

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
- **Never a video input** — boards, grids, sketches and panels stay out of
  every Seedance request; their staging becomes prompt text and identity comes
  from element references.

- **Paginated boards bind the same ordered reference set on every page** so
  `@Image N` numbering never shifts between pages; say which references a page
  does not use instead of dropping them from the upload.

## Selection gate

Storyboard variant selection follows `project.md` approval mode. In
`approve_for_me` the agent inspects and ranks the candidates, records a
hash-bound decision and selects the passing one.
`storyboard.review: false` disables the review UI only; it does not remove QA
or the validated decision. In `ask_for_approval`, the strongest candidate is
stored under `recommended_variant` with `status: review` until the user
chooses. Run `studio_project.py sync` and the stage-exit checks after the
decision in either mode.

## Prompt review gates (generation-bound)

Before any **generation** call, run `prompt-review`:

- Seedream storyboard grid prompt (before `seedream_generate_image`)
- Seedream element sheet prompts (before each sheet generation)
- Seedance video prompt, including per-beat motion wording from
  `VideoBreakdown.shots[].motion.directing_prompt_text`
  (before `seedance_2_5_create_task`)

Review inline by default. CRITICAL/MAJOR findings must be fixed before
submission. Acquired brand/product/logo assets (`generation: none`) and
deterministic HTML-entrypoint renders (`generation: deterministic_html`) skip
this gate and provider registration, but still need hashes, a manifest entry,
visible QA, and explicit selection.

## Reusable recipe contract

Validate every committed template against `references/template-schema.json`.
Keep the recipe distinct from a particular run:

- Prefer the native host session for `analyze` and `motion_review`; use
  capability-driven tool fallbacks when needed. Legacy recipe
  temperature, reasoning-effort and token-limit fields are historical hints,
  not instructions to call a provider or change the host runtime.
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
│   ├── long-pins-and-multi-clip.md
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

## Intentional conditioning representation

Storyboards and analysis sketches are never conditioning inputs. Another
derived control asset (for example a motion blockout) stays
`control_only: true` until it is explicitly selected as a composition or motion
reference; then record its manifest, current SHA-256, `reference_image` or
`reference_video` role, and `control_only: false`, and confirm live mode
support. Flipping the flag alone never grants approval.
