# AGENTS.md — ai-director

This is the single workspace entrypoint for agents and contributors. The public
README uses the existing `ark-director` display name; the checkout is
`ai-director`. Do not rename the project as incidental maintenance.

## Scope and authority

This workspace produces AI-generated image, video, audio and 3D content using
BytePlus tools and independent skills. Follow current user instructions and
preserve authorization already given for the task. Task scope does not expand
into unrelated global configuration, external publishing, or production edits.

Keep project-specific instructions and tooling in `.agents/`. Personal global
rules may add preferences but a clean checkout must contain its own operational
contracts. Do not create a second competing `.agents/AGENTS.md`.

Before editing, inspect relevant files, plans and existing Git changes. Never
revert, overwrite or clean up work you did not create for this task. When a plan
is supplied, reference it during implementation. Substantial independent work
may use sub-agents with explicit, non-overlapping file ownership.

Ask for missing information when it materially affects the intended result.
Continue reversible work whose requirements are already clear. Do not repeat an
approval request when existing user instructions authorize the same action.

## Operational contracts

Load only the contract relevant to the current stage:

| Need | Tracked source |
| --- | --- |
| Production stages, approval, review, durable submission and QA | [Production policy](.agents/contracts/production-policy.md) |
| Required stage canvas and HTML freshness checks | [Production canvas](.agents/skills/showcase-html/references/production-canvas.md) |
| MCP, Ark CLI, Lumina and capability routing | [Routing](.agents/contracts/routing.md) |
| Canon, props, screens and control references | [Element identification](.agents/contracts/element-identification.md) |
| File prefixes and numbering | [Asset naming](.agents/contracts/asset-naming.md) |
| Requested dialogue synchronization and assembly | [Audio-video alignment](.agents/contracts/audio-video-alignment.md) |
| Requested camera, lens, lighting, acting and other axes | [Directorial axes](.agents/contracts/seedance-reference.md) |
| Vendored Blender adapter/setup | [Blender setup](.agents/contracts/blender-mcp-setup.md) |

Stable validation rule IDs live in `.agents/contracts/rules.json`. Request,
registry and review schemas live in `.agents/contracts/schemas/`.

## Routing and capability boundaries

Use Ark CLI for platform administration and interactive generation. Prefer
ModelArk MCP for in-agent durable generation. If MCP is unavailable before
submission, use an equivalent available CLI surface with the same review,
reference and persistence contracts. An ambiguous timeout is a reconciliation
case, never a reason to submit through a second transport.

Skills never call the Ark REST API directly. Resolve tool availability and
current model bindings before selecting parameters. Seedance 2.5 remains the
workspace default; a verified requested capability may require another model.
Do not force 4K, switch models because a face is present, or assume a workflow
exception makes unsupported mixed reference roles valid.

Choose static-graphic production by fidelity requirement. Prefer a deterministic
HTML entrypoint with project-local CSS/SVG dependencies, rendered to a
reviewable raster, for exact copy, typography, logos, screen/UI layouts, title
cards, posters, price/CTA treatments, product lineups, and simple vector or
gradient geometry. Use Seedream for invented photographic
or illustrative content, expressive textures, and image synthesis where
controlled variation is useful. Hybrid work generates or acquires the visual
base first, then finishes exact copy and layout deterministically. Do not spend
generation credits to reproduce spelling, alignment, or geometry that code can
render exactly.

In this workspace, the shorthand "HTML/CSS/SVG" means one HTML entrypoint with
project-local CSS and SVG dependencies. The deterministic renderer does not
accept standalone CSS or SVG entrypoints.

Lumina is opt-in. When the user explicitly works in Lumina, deliver prompts in
chat without MCP/CLI generation or production file writes unless requested.
Prompt-only work may deliver drafts without generating assets or demanding
production locks. Software/system diagrams use Mermaid; cinematic blocking
uses the blocking-map capability.

## Skills and orchestration

One skill provides one capability. Leaf skills remain independently usable;
composition hints are prose, not directives to load siblings. Declared
orchestrators own cross-skill sequencing, generation gates and delegation.
`film-production` manages multi-scene production using its stage/handoff
contracts. Load only specialists needed for the current stage or requested axis.

### Parallel production and nested delegation

When multiple assets, videos, scenes or production stages are independent, run
them in parallel. An agent assigned a bounded workstream may delegate
independent subtasks to its own sub-agents when this reduces waiting or lets
downstream preparation begin earlier.

- Give every agent explicit, non-overlapping ownership of files, assets,
  document sections and provider operations.
- Begin succeeding work as soon as its required inputs are stable; do not wait
  for unrelated workstreams to finish.
- Keep the main agent responsible for scope, shared-state coordination,
  integration, final verification and user communication.
- A sub-agent remains responsible for reviewing and integrating the work of any
  nested sub-agents it creates.
- Serialize edits to shared mutable state, including `showcase.json`,
  `task_ids.json`, selection manifests, Lark documents, assemblies and shared
  registries, unless the tool provides an explicit conflict-safe transaction.
- Never submit the same paid generation through multiple agents or transports.
  Reconcile ambiguous submissions before retrying.
- Do not let speculative downstream work change approved inputs or user
  selections. Revalidate dependent work when an upstream input changes.
- Respect available concurrency limits. Prioritize work on the critical path
  rather than spawning agents for trivial tasks.

Vendored HyperFrames, Blender and FFmpeg bundles are exempt from local
skill-isolation remediation. Preserve upstream design, record local overlays,
and review changes before re-vendoring. Do not remove a skill because it is
currently unused. All installed bundles and `skills-lock.json` belong in Git.

Keep skill metadata concise and valid YAML. Move substantial conditional modes
and examples into focused same-skill references with explicit loading guidance.
A reference file must ship with the bundle or be a declared workspace adapter.

When a skill is added, renamed, removed or its description changes, update the
README skill entry and catalog together. Each skill appears once. Preserve
source-specific lock hash semantics; bundle integrity also covers scripts,
references and UI metadata. Do not refresh hashes to hide unexplained changes.

## Production invariants

- Draft breakdown may precede canon. Dependent production generation requires
  the relevant approved recurring, branded or story-critical elements.
- Identify all visible props; only threshold-qualified props require separate
  locked references. Incidental generic props may be described. Keep canonical
  held props separate from character sheets and distinguish always-worn/variant
  wearables. For authorized real brands, logos, and labeled products, prefer an
  official or authorized web/user download over Seedream; generate only when no
  usable real asset exists or a stylized substitute is requested. See
  [Element identification](.agents/contracts/element-identification.md).
- When the user cites real brand video ads or other footage for visual or motion
  inspiration, obtain media the provider can actually watch before borrowing
  grammar. Prefer a public HTTPS URL that `seed_understand` already accepts;
  download locally and `media_upload` only when the link is a page/platform URL,
  auth-gated, or otherwise unusable as a video input. Transcripts, scripts, and
  article write-ups are not a substitute for the video. Route full reverse-
  engineering through `template-factory`; lighter analysis may use
  `modelark-mcp` (`seed_understand`) alone. See
  [Routing](.agents/contracts/routing.md).
- Elements define identity; derivative boards require current source hashes and
  explicit selection before video use. Control-only diagrams stay analysis-only
  by default. Automated recommendations cannot set selected_variant or approved.
- Static assets use visible-design criteria. Narrative shots need action and
  intent. Audio uses its requested sound arc. Do not apply narrative tactics to
  every static sheet or ambience prompt. Deterministic HTML/CSS/SVG is a
  first-class static production route, not merely a repair step.
- Lock exact copy/layout with a deterministic reference before video when
  typography, logos, UI, title cards, posters, product lineups, or simple
  geometry carry the design. Preserve editable source, local input/font hashes,
  dimensions, background/alpha intent, renderer version, and source/output
  hashes. A separate solid-background model reference may accompany a
  transparent delivery asset; never reuse a white-matted file as transparency.
  Inspect conditioned video because references do not guarantee pixel-perfect
  text.
- Do not bake captions, taglines, CTAs, end cards or other overlay text into
  generated video. Keep generated footage text-free and add on-screen text in
  post with FFmpeg or HyperFrames.
- Preserve exact canonical descriptors where applicable. Prefer positive,
  observable direction; necessary edit-scope exclusions are allowed.
- Run prompt-review for every generation-bound prompt. Resolve CRITICAL/MAJOR
  findings. Missing reviewer output is incomplete. Documentation/manifest-only
  edits, acquired brand/product assets (`generation: none`), and deterministic
  static renders (`generation: deterministic_html`) do not trigger paid
  generation or prompt-review; changed worked examples are reviewed offline.
  Deterministic renders still require exact-copy, font, overflow, dimension,
  alpha, thumbnail-legibility, provenance, canvas, and visible-design QA.
- Freeze the exact prompt beside its intended output before submission. Verify
  request hash, current reference hashes, ordered roles/bindings, explicit
  selections and supported parameters. Changed inputs invalidate review.
- Persist a prepared operation in the project task registry before submission;
  save an acknowledged task ID immediately. Resume existing tasks after poll
  timeouts. Unknown acceptance holds for reconciliation or explicit retry scope.
- Save every generated modality locally and record artifact/task IDs, bytes,
  SHA-256, actual media properties and separate estimated/confirmed costs. Save
  deterministic static source and render records beside their raster outputs;
  they do not enter the provider task registry.
- Create one project `showcase.json` and generated `index.html` at initialization.
  Keep that production canvas synchronized with briefs, manifests, prompts,
  elements, audio, video, review evidence, assemblies and delivery state after
  every material stage change. A stage cannot exit until its
  `showcase-html --check --stage <stage-id>` freshness check passes.
- Provider success sets review, not approved. User choice alone approves a
  variant. Preserve other variants and prior history unless explicitly changed.
- Default generative-image selection sets contain three stochastic samples with
  identical prompt, references and effective parameters except supported seed
  variation. Deterministic renders produce one exact version per specification.
  Explicit requested count or creative alternatives override the generative
  default.
- Use the lowest suitable cost/resolution within the request. Set watermark
  false only when the tool supports that parameter, unless the user requests it.
- Separate lip-sync audio is opt-in. Generate scenes at natural supported
  duration, then chain supported modes or assemble. Continuous native extension
  is exceptional and requires seam inspection.
- Moderation rejection is evidence to diagnose, not proof of a false positive.
  Revisions remain legitimate and authorized; task cleanup requires explicit
  scope rather than being inferred from provider completion.

## Local production state and naming

`projects/<project-name>/` is the durable local source of truth, never a default
Git staging target. Keep existing production assets and manifests untouched by
repository maintenance unless explicitly scoped.

| Location | Contents |
| --- | --- |
| `projects/<project>/project.md` | Brief, proposed/confirmed axes, project state |
| `projects/<project>/showcase.json` and `index.html` | Canonical canvas manifest and synchronized stage review surface |
| `projects/<project>/task_ids.json` | Single provider-operation registry |
| `projects/<project>/ref_cache.json` | Content hashes and storage-scoped object keys |
| `projects/<project>/elements/<element-id>/` | Reusable identity/location/prop manifests, references, and deterministic graphic sources/renders |
| `projects/<project>/scenes/scene-NN/` | Scene manifest, keyframes and scene renders |
| `projects/<project>/scenes/scene-NN/sNN_shNNN/` | Shot manifest, exact prompt snapshots, takes and dialogue |
| `projects/<project>/library/` | Reusable non-shot music, SFX and ambience |

Folders and IDs use lowercase kebab-case. Scene IDs use two digits; shot/panel
numbers use three digits with gaps of ten. Asset prefixes distinguish modality;
see the naming contract. Prompt snapshots use `prompt_<asset-stem>.md` beside
the media and are immutable after submission. Manifest `prompt_file` and
`prompt_sha256` identify the canonical snapshot rather than duplicating it.

Provider state, local submission state and editorial approval are distinct.
New records use versioned schemas. Read legacy metadata conservatively and
propose migration previews rather than inventing missing IDs, approval or cost.
Reference caches key reuse by content hash plus storage scope; expiring signed
URLs are transport data. Selection manifests are authoritative; derived JSON
and browser state must agree with validated committed selections.

`docs/`, `plans/` and `specs/` contain local research, implementation plans and
exploratory specifications. Never stage their contents or `projects/` by default.
Plans use `PLAN_<NAME>.md` and include concrete implementation details.
Reusable operational contracts, schemas, scripts, tests and maintenance runtime
configuration are an explicit tracked exception to the local-document rule.
Do not leave ad hoc research files at the workspace root.

## Portable security and change boundaries

Resolve credentials and base URLs from runtime configuration. Canonical names
are `BYTEPLUS_MODELARK_API_KEY` and `BYTEPLUS_SEED_AUDIO_API_KEY`; transport
compatibility aliases may exist. Never output or commit credentials, `.env`
files, signed URLs, account secrets or sensitive production input in fixtures.

Validate external data before use. Use subprocess argument arrays rather than
evaluated command strings; confine project paths including symlinks. Use
parameterized data access. Keep review servers on loopback with bounded,
validated state-changing requests and owned temporary files.

Lark/shared artifacts must be self-contained and link only to audience-accessible
resources. Do not publish local paths, private vault context or tooling noise.
External messages require explicit authorization. Do not infer approval to
publish from approval to draft or generate.

Never commit or push repository changes unless requested. When authorized,
stage only task-owned files. Clean up only your own temporary fixtures/scripts;
retain durable local production state, user edits, secrets and required caches.

## Verification and maintenance commands

Install dependencies with `uv sync --locked`; use the package manager for new
dependencies. Consult current primary documentation and audit dependencies.
Keep code simple, explicit and small; match neighboring conventions. Do not add
code comments unless requested or leave debug output in committed code.

Run the applicable checks from the repository root:

```bash
uv run python .agents/scripts/validate_workspace.py --offline
uv run python -m unittest discover -s tests -v
uv run ruff check .agents/scripts tests
uv run mypy .agents/scripts
PYTHONPYCACHEPREFIX=/tmp/ai-director-pycache uv run python -m compileall -q .agents/scripts
uv run pip-audit
git diff --check
```

Whitespace checks also apply to new files. `pip-audit` needs network access;
report unavailable evidence accurately. The offline validator never generates
media or sends messages. Use a supplied tracked-file inventory to validate an
uncommitted change as a prospective clean checkout without staging it.

Documentation changes need metadata/link/schema and scoped lint checks. Helper
changes additionally need meaningful unit tests and synthetic-media/browser
smoke tests. Provider adapters use mocked contract tests; live paid checks need
appropriate explicit generation scope. Report pass/fail/not-applicable for
unit, smoke, lint, type, build/syntax, diff and secrets checks. A missing runtime
or unavailable tool is not a passing test.

Production-stage verification also runs the project canvas checkpoint from the
showcase skill. `media-review` is an unavailable-browser or explicitly requested
OS-player fallback and does not satisfy this checkpoint.

For reviewed skill changes, preview `uv run python .agents/scripts/sync_catalog.py --refresh-integrity`; add `--write` only after inspecting the listed source changes. Catalog summaries determine README rows. This command preserves upstream hash semantics and does not stage or commit files.
