---
name: template-factory
description: >-
  Reverse-engineer a reference video ("pin") into reproducible AIGC output.
  Orchestrates pin intake (prefer a public HTTPS URL seed_understand can watch;
  download and media_upload only when unusable), video breakdown, keyframes,
  deep motion review, dynamic sketch storyboard, optional element sheets
  (Seedream for invented identity; web/user download-first for authorized real
  brands/logos/products), and a Seedance 2.5 video — generation-bound prompts
  through prompt-review; stages on the showcase-html canvas. Explicit
  orchestrator composing modelark-mcp, seedream-storyboard, seedance-prompt-25,
  prompt-review, showcase-html, and ffmpeg; never calls the Ark REST API. Use to
  replicate style/composition/grammar, build a reusable template, or turn a
  cited brand ad, Pinterest pin, or other reference video into elements and
  video.
---

# Template Factory

Turn a reference video ("pin") into reproducible AIGC output through a reusable
"template" (the recipe). One run produces: a `VideoBreakdown` analysis, a sketch
storyboard, optional element sheets, and a Seedance 2.5 video take — all
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
- Never infer approval. Technical success places an output in `review`; only the
  user sets `approved`.
- **Every generation-bound prompt this factory submits — Seedream storyboard,
  Seedream element sheet, or Seedance video — must pass the `prompt-review`
  gate first.** Acquired brand/product/logo assets (`generation: none`) skip
  prompt-review; they still need hashes, canvas listing, and explicit selection.
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
pin_uploaded → breakdown_draft → breakdown_approved → motion_reviewed
  → elements_draft → elements_approved → storyboard_draft
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
2. **Analysis** — `seed_understand` with the template's analysis prompt
   (`references/analysis-prompt.md`) → validate `VideoBreakdown` against
   `references/breakdown-schema.json` and run
   `scripts/validate_breakdown.py` → write `analysis.json` + `breakdown.md`.
   Freeze the reviewed source as `analysis.vNN.json`; record its SHA-256 and
   approval scope. Gate A: user reviews the breakdown.
3. **Keyframes** — `ffmpeg` extracts a frame per shot (mid-shot, or the flagged
   element keyframe) into `keyframes/`.
4. **Deep motion review** — second `seed_understand` pass (`thinking=true`) per
   `references/motion-review-prompt.md` → validate against
   `references/motion-review-schema.json` → merge by `shot_index`, never array
   position, into a new analysis revision while retaining the immutable source
   revision. Motion evidence may enrich the approved breakdown without changing
   timing or action. If it changes an approved decision, invalidate affected
   downstream review and obtain review for the new revision. This is the primary
   fix for "ours looks static".
5. **Elements** — identify required canonical inputs from the draft breakdown.
   Use the workspace prop threshold: branded, recurring, story-critical, or
   scene-variant wearables need a separate locked reference; incidental objects
   may be described in text. For authorized real brands, logos, and labeled
   products, acquire official or authorized web/user assets first and promote
   them with `source: web_download` or `user_supplied` and `generation: none`;
   do not Seedream a fake packshot or logo when a usable real asset is available.
   For invented characters, locations, and other generative sheets, generate the
   user-requested number of variants, or 3 by default, after prompt review.
   Persist `selected_variant` only after explicit user choice.
6. **Storyboard** — after relevant Elements are approved, write a dynamic
   production board via `seedream-storyboard`, one panel per shot unless the
   user sets a panel budget. Review the prompt and generate the requested count,
   or 3 variants by default, using distinct seeds only when supported. Paginate
   large boards into readable grids while preserving one ordered panel plan. A
   monochrome analysis sketch is control-only: translate its blocking into text
   and omit it from video inputs by default. A production panel can be promoted
   only after explicit selection, source-hash validation, and a supported image
   mode.

7. **Video** — use current capability evidence to choose one supported clip or
   multiple natural-duration shots plus assembly. Compose the Seedance 2.5
   six-part prompt from breakdown + eligible board directions + motion review +
   element sheets (via `seedance-prompt-25`), run `prompt-review`, persist the
   prepared request, then submit via the supported durable transport. Prefer
   `seedance_2_5_create_task`; use an equivalent Ark CLI route only before any
   ambiguous submission and only when it satisfies the same contract. Persist
   the task id, poll, download, and run technical and playback QA.
8. **Review** — compare the reference and take in playback for shot timing,
   motion direction and intensity, action progression, camera movement,
   transitions, opening/ending state, and requested audio arc. Add the pin and
   every take as playable players on the `shot-generation` canvas in one
   `kind: "takes"` group (`groups[].takes[].media` as `{type, src}` — never
   flat `cards` or string media paths); include exact prompt, ordered
   references and QA evidence; regenerate/open the page, pass its stage
   freshness check, set `review`, and let the user approve there.

## Route specialist work

| Need | Primary skill |
| --- | --- |
| Pin download when URL is not seed_understand-usable | Available downloader (e.g. `yt-dlp`); then `modelark-mcp` (`media_upload`) |
| Upload / presign references | `modelark-mcp` (`media_upload`, `media_presign`) |
| Video analysis + motion review | `modelark-mcp` (`seed_understand`) |
| Keyframe extraction | `ffmpeg` |
| Storyboard grid prompt | `seedream-storyboard` |
| Element sheets (invented / generative) | `seedream-character-sheet`, `seedream-location-asset`, `seedream-prompt` |
| Brand / logo / product packshot | Web or user download first per element-identification; Seedream only as fallback |
| Seedance 2.5 video prompt | `seedance-prompt-25` |
| Prompt quality gate (generation-bound only) | `prompt-review` |
| Persistent stage canvas and visual review | `showcase-html` |

## Canvas stage mapping

| Factory work | Canvas stage | Exit evidence |
| --- | --- | --- |
| Pin intake and template intent | `brief-development` | source hash, constraints, recipe target |
| Analysis, keyframes, motion review | `scene-breakdown` | valid breakdown, motion review, approved revision |
| Element acquisition/generation and selection | `canon-elements` | hashes, explicit selections; acquired or generated variants |
| Storyboard generation and selection | `storyboard-visual-plan` | ordered panels, prompts, eligibility state |
| Audio decision | `audio-preparation` | requested assets and timing, or `skipped` with reason |
| Video generation and take review | `shot-generation` | prepared requests, task provenance, pin + take players in one `takes` group, QA |
| Multi-shot edit and final review | `assembly-review` | approved inputs and inspected assembly, or `skipped` for one clip |
| Final output | `delivery` | master/proxy hashes and approval, or `skipped` when outside scope |

Analysis, keyframes, and motion review update the same `scene-breakdown` stage;
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

- **Dynamic panel count by default** — one panel per identified shot. Honor an
  explicit user panel budget and preserve all shot-to-panel coverage decisions.
  Use the smallest readable grid and paginate large boards.
- **Sketch by default** — use colorless pencil/ink as a composition/order anchor.
  Honor an explicit request for a limited palette, full color, or standalone
  production panels and record that decision in the manifest.
- **3 variants by default** — honor an explicit requested count. Keep prompt,
  references, model, and effective parameters identical across sampling variants;
  vary only a supported stochastic seed.
- **Video eligibility** — production panels need explicit user selection and
  current canonical source hashes. Control sketches are omitted by default;
  an intentional conditioning exception requires explicit selection, supported
  tool inputs, and artifact-specific QA. Bind only eligible inputs.

## Selection gate (human review by default)

Storyboard variant selection requires explicit user choice. `storyboard.review:
false` disables the review UI only. Store an automatic suggestion under
`recommended_variant`, keep `status: review`, and wait for explicit selection
before video promotion. Neither a recommendation nor technical success writes
`selected_variant` or `approved`.

## Prompt review gates (generation-bound)

Before any **generation** call, run `prompt-review`:

- Seedream storyboard grid prompt (before `seedream_generate_image`)
- Seedream element sheet prompts (before each sheet generation)
- Seedance video prompt, including the motion-review wording merged into it
  (before `seedance_2_5_create_task`)

CRITICAL/MAJOR findings must be fixed before submission. Skip this gate for
acquired brand/product/logo assets that have no generation prompt.

## Reusable recipe contract

Validate every committed template against `references/template-schema.json`.
Keep the recipe distinct from a particular run:

- `locked_grammar` contains the reusable style, composition, motion,
  transition, and rhythm rules that define the template.
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
│   ├── breakdown-schema.json
│   ├── motion-review-schema.json
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
│   ├── motion-review.json, motion-review.md
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
