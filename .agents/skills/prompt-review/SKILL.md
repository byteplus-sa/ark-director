---
name: prompt-review
description: >-
  Review BytePlus Seedance, Seedream, and Seed Audio prompts with a sub-agent
  review pipeline and explicit model, operation, change contract, and request
  hash. Return rule findings and complete or incomplete status; fix and re-review
  changed prompts before generation. Use for video, VFX, Filipino dialogue,
  image/character/location/prop/UI/card/storyboard prompts, music, SFX, or ambience.
  Trigger when asked to review, QA, validate, or lint prompts, or before submitting
  newly authored generation prompts. Exclude manifest-only edits, generated-media
  review, and frozen snapshots unless re-review is explicitly requested.
---

# Prompt Review

A quality gate for prompts. The main agent writes prompts, a sub-agent reviews them
against the repo's skill best practices, and the main agent fixes any issues found.

## Core concept

```
Main agent writes/updates prompts
  → identify each prompt's type (Seedance 2.5, Seed Audio, Seedream, etc.)
  → load the matching review checklist from references/review-checklists.md
  → spawn a sub-agent: give it the prompt text + the checklist
  → sub-agent returns structured findings (issues by severity with suggested fixes)
  → main agent applies fixes to the prompt files
  → re-review only the changed prompts if any fixes were applied
```

## When to trigger

- After writing or updating any prompt for a BytePlus generative model.
- Before submitting a generation task (Seedance, Seed Audio, Seedream).
- When the user asks to review, check, QA, validate, or lint prompts.
- After revising a prompt based on generated output feedback.

Do not trigger for:
- Media review (project work uses its persistent `showcase-html` canvas; ad-hoc
  files may use `showcase-html --quick`).
- Manifest or scene definition edits (those are production metadata, not prompts).
- Prompts that have already been frozen as prompt snapshots unless the user explicitly
  asks to re-review a frozen snapshot.

## Creative-quality comparisons

For requested skill evaluation or alternative-draft assessment, read
[Creative Quality](references/creative-quality.md). Use brief-specific semantic
rubrics and evidence-backed blind comparisons. This offline assessment is
separate from production approval and does not require provider submission.

## Explicit review input

Collect `prompt_type`, `model`, `operation`, `language`, `requested_axes`,
`may_change`, `must_preserve`, and `request_sha256` alongside the complete prompt,
ordered reference roles/hashes, and capability evidence. The request hash covers
the semantic submitted request, not just its prompt. Missing dispatch or request
evidence leaves a production review `incomplete`; request it from the caller.
Filename/content inference is a draft-only fallback with an explicit warning.

For the same request, use generation rules for generate, 2.5 edit rules for a
2.5 edit, legacy VFX rules for a supported 2.0 edit, and extension rules for
extend. Language and named-axis checklists are additive only when applicable.
A localized change contract overrides generic preservation heuristics for items
under `may_change`; keep all `must_preserve` items unchanged.

## Prompt type detection

Use explicit input first; filenames below are fallback hints, not authority:

| Prompt type | File prefix | Checklist source |
|---|---|---|
| Seedance 2.5 video | `prompt_sNN_shNNN_tNN_vNN.md` | `seedance-prompt-25` |
| Seedance 2.0 video (4K/Fast/Mini) | `prompt_sNN_shNNN_tNN_vNN.md` | `seedance-prompt-20` |
| Seedance 2.5 edit | explicit model + edit operation | Seedance 2.5 edit section |
| Seedance 2.5 recast (motion transfer) | explicit model + recast operation | Seedance 2.5 recast section + `seedance-motion-recast` |
| Seedance VFX (video-to-video edit, legacy path) | `prompt_sNN_shNNN_tNN_vNN.md` | `seedance-vfx-prompt` |
| Seedance Filipino dialogue | `prompt_sNN_shNNN_tNN_vNN.md` | `seedance-prompt-25` + `seedance-prompt-25-filipino` |
| Seed Audio (dialogue/music/SFX/ambience) | `prompt_dlg_*`, `prompt_mus_*`, `prompt_sfx_*`, `prompt_amb_*`, `prompt_mix_*` | `seed-audio-prompt` |
| Seedream image generation | `prompt_concept_*`, `prompt_sNN_kf*` | `seedream-prompt` |
| Seedream character sheet | `prompt_char_*` | `seedream-character-sheet` |
| Seedream location asset | `prompt_loc_*` | `seedream-location-asset` |
| Seedream prop sheet | `prompt_prop_*` | `seedream-prompt` (general image rules apply) |
| Seedream screen UI reference | `prompt_screen_*` | `seedream-prompt` (general image rules apply) |
| Seedream brand/title card | `prompt_card_*` | `seedream-prompt` (general image rules apply) |
| Seedream storyboard | `prompt_sNN_kf*` (multi-panel) | `seedream-storyboard` |
| Seedance music video | `prompt_sNN_shNNN_tNN_vNN.md` (song-driven) | `seedance-music-video` |

Deterministic HTML-entrypoint screens, cards, posters, product layouts, and
overlays have no generation prompt and stay outside this table. Review only a
generative image layer inside a hybrid; the deterministic result uses
exact-copy, font, layout, dimension, alpha, provenance, and visible-design QA
instead.

The "Checklist source" column is a provenance label only — this skill never loads
a sibling; the applicable checklist is always read from this skill's own bundled
`references/review-checklists.md`.

When a prompt could match multiple types (e.g., a Seedance 2.5 prompt with Filipino
dialogue), stack the checklists — the sub-agent checks against all applicable skills.

UGC intermediate outputs (hooks, scripts) are reviewed at **Stage 1** (before
composition into a final Seedance prompt). The final composed Seedance prompt is
reviewed at **Stage 2** against the Seedance 2.5 + Universal checklists. UGC
compliance audit runs **before Stage 1** — if it returns CRITICAL, stop the pipeline.

## Workflow

### Step 1 — Collect prompts to review

Gather all prompt files that were written or updated in the current session. These are
the files with the `prompt_` prefix that sit beside their media asset. Read each file
to get its full text.

If reviewing prompts that have not yet been saved to files (drafted inline in
`shot.md` or `scene.md`), extract the prompt text from the manifest's `prompt:` field
or inline working copy. Before production submission, freeze the accepted text
as its immutable `prompt_*.md` snapshot so the calling orchestrator can embed it
in the current project canvas with `promptFile`.

### Step 2 — Detect prompt type and load checklist

For each prompt:
1. Resolve its explicit model, operation, prompt type, and requested axes; use
   the table only for a warned draft fallback.
2. Read the corresponding section from `references/review-checklists.md`.
3. Also load the **universal directing principles** section (applies to all prompts).

### Step 3 — Spawn the review sub-agent

Delegate the review to a sub-agent. The sub-agent receives:
- The full text and explicit review input for each prompt being reviewed.
- The request hash, change contract, reference evidence, and applicable rule IDs.
- The applicable checklist section(s) from `references/review-checklists.md`.
- The universal directing principles.
- Clear instructions on what to check and how to report.

**Batching strategy:**
- All prompts of the same type → one sub-agent reviews them all in one pass.
- Prompts of different types → spawn one sub-agent per type, run in parallel.
- Maximum 5 sub-agents concurrent.

**Delegation mechanisms (host-agnostic):**

Use whichever mechanism the current host provides:

- **OpenCode CLI (non-interactive):**
  `opencode run -m <review-model> "<worker prompt>"`
  Pass the prompt text and checklist inline. Capture stdout for findings.
  (`<review-model>` is the host's configured sub-agent model, not a hard-coded ID.)

- **Host Task / sub-agent tool:**
  Delegate each review batch as a separate task with the prompt text and checklist
  embedded in the task prompt.

- **Fallback (no sub-agent mechanism):**
  The main agent runs the review itself using the same checklist and findings format.
  Do not skip the review — just run it inline.

### Step 4 — Sub-agent prompt template

Use this template when constructing the sub-agent's task prompt. Replace the bracketed
placeholders with actual content.

```text
You are a prompt quality reviewer for BytePlus generative AI models.
Your job is to review prompt(s) against a specific checklist of best practices
and return structured findings. You do NOT fix the prompts — you only identify
issues and suggest fixes.

## Dispatch and request identity
prompt_type: <explicit type>
model: <resolved model>
operation: <generate/edit/extend>
language: <requested language>
requested_axes: <named axes>
request_sha256: <canonical request hash>
required_rule_ids: <IDs supplied by caller>
reference_evidence: <ordered paths, hashes, roles, and approvals>

## Change contract (may change / must preserve)

- MAY CHANGE: <list from the user's request, e.g. "spoken language + lip sync">
- MUST PRESERVE: <list, e.g. "character identity, environment, timing, camera">

## Prompts to review

### Prompt 1: <filename or identifier>
<full prompt text>

### Prompt 2: <filename or identifier>
<full prompt text>

## Review checklist

<paste the applicable checklist section from references/review-checklists.md here>

## Universal directing principles (apply to ALL prompts)

<these are always included — see Universal Directing Principles section below>

## Your task

For each prompt, go through every item in the checklist. For each item:
1. Determine if the prompt satisfies the requirement.
2. If it does not, record a finding.

Return a machine-readable review record, then optional human-readable details:

{
  "schema_version": 1,
  "request_sha256": "<same request hash>",
  "reviewer_status": "complete",
  "checks": [
    {"rule_id": "revision.declared_delta", "status": "pass",
     "evidence": "<specific preserved locks and permitted change checked>"}
  ]
}

Use one check per required rule ID. Status is pass, fail, or not_applicable.
Every not_applicable result needs a concrete applicability reason. Missing
inputs, unchecked required rules, or unusable reviewer output mean incomplete.
For failures include severity, applicability, exact evidence, and suggested fix
in the human-readable details. Do not invent evidence from missing assets.

Report any human-readable findings in this format:

### Review Findings

#### Prompt: <filename or identifier>

**PASS** — no issues found.

OR

**ISSUES FOUND:**

1. [CRITICAL] <Checklist item name>
   - Problem: <what is wrong>
   - Evidence: <quote the relevant part of the prompt>
   - Suggested fix: <specific, actionable fix>

2. [MAJOR] <Checklist item name>
   - Problem: <what is wrong>
   - Evidence: <quote the relevant part of the prompt>
   - Suggested fix: <specific, actionable fix>

3. [MINOR] <Checklist item name>
   - Problem: <what is wrong>
   - Evidence: <quote the relevant part of the prompt>
   - Suggested fix: <specific, actionable fix>

### Severity definitions
- CRITICAL: Will cause generation failure, safety rejection, identity drift,
  or fundamentally broken output. Must fix before submission.
- MAJOR: Will degrade output quality, cause inconsistency, or violate an
  applicable directing rule. Must resolve before submission.
- MINOR: Could improve quality or clarity but won't break the generation.
  Fix if time allows.

## Rules
- Check every item in the checklist. Do not skip items.
- Quote the exact text from the prompt as evidence.
- Suggested fixes must be specific and actionable — not "improve the prompt".
- If a checklist item does not apply to this prompt type, note "N/A" and move on.
- Do not rewrite the prompt. Only identify issues and suggest fixes.
- Be precise and honest. Do not invent problems that don't exist.
- If the prompt passes all items, say so clearly.
- An item listed under MAY CHANGE is a deliberate instruction — do NOT flag it
  as "modifying the subject" or "not preserving the source". Only flag:
  (a) a breakage of something under MUST PRESERVE, or (b) a real quality defect
  in how the changed thing is described (missing guards, missing numeric
  anchors, missing language reinforcement, ambiguity).
```

### Step 5 — Receive and triage findings

If a sub-agent returns an empty, truncated, or content-free result (or findings
without a complete hash-bound record per prompt), record `reviewer_status:
incomplete` and retry the same batch once (max 1 retry).
If the retry is still unusable, run the review inline against the same
checklists. If evidence is still missing, retain incomplete status and block
submission; never treat an empty sub-agent result as passed.

When the sub-agent returns findings:

1. **Read all findings** for each prompt.
2. **Triage by severity:**
   - CRITICAL issues — must fix before any generation task is submitted.
   - MAJOR issues — must resolve before submission. A user-requested creative
     change requires a new applicability decision and review, not a fake pass.
   - MINOR issues — fix opportunistically; surface to the user.
3. **Deduplicate** — if multiple sub-agents found the same issue (e.g., a universal
   principle violation), merge into one finding.
4. **Cross-check** — if the sub-agent flagged something that you believe is actually
   correct, verify against the skill file before dismissing.

### Step 6 — Apply fixes

The main agent applies fixes directly to the prompt files:

1. For each finding to be fixed, edit the prompt file with the suggested fix.
2. Preserve the prompt's structure and formatting conventions.
3. Do not rewrite the entire prompt — apply only the targeted fix.
4. After applying fixes, note what was changed.

### Step 7 — Re-review changed prompts (if any fixes were applied)

If any CRITICAL or MAJOR fixes were applied, re-review the changed prompts:
- Spawn a new sub-agent (or run inline) with the updated prompt text and the same
  checklist.
- Confirm the fixed issues are resolved and no new issues were introduced.
- If new issues appear, fix and re-review again (maximum 2 re-review rounds).
- If issues persist after 2 rounds, surface to the user for a decision.

### Step 8 — Report to the user

Summarize the review results:

```text
## Prompt Review Complete

### Reviewed
- <prompt file> — <prompt type> — <PASS | N issues fixed>

### Findings summary
- CRITICAL: <count> (all fixed)
- MAJOR: <count> (all fixed)
- MINOR: <count> (<fixed count> fixed, <remaining count> remaining)

### Changes made
- <prompt file>: <what was changed and why>

### Remaining issues (if any)
- <prompt file>: <issue> — <reason not fixed>

### Ready for generation
- <prompt file> — READY
- <prompt file> — BLOCKED (<reason>)
```

## Multi-prompt review

When reviewing multiple prompts (e.g., all prompts for a scene's shots):

1. Group prompts by type.
2. Spawn one sub-agent per type (parallel, max 5 concurrent).
3. Each sub-agent reviews all prompts of its assigned type in one pass.
4. Collect all findings, deduplicate, and apply fixes.
5. Re-review only the prompts that had CRITICAL or MAJOR fixes applied.

This is efficient because:
- Same-type prompts share the same checklist — one sub-agent loads it once.
- Different-type prompts run in parallel without blocking each other.
- The main agent only re-reviews prompts that actually changed.

## Universal directing principles

The workspace policy owner is the tracked production contract, with stable
rule IDs in `../../contracts/rules.json`. The bundled checklist provides
modality-specific review guidance, not a competing source of workspace policy.
Its source metadata is `references/rule-provenance.json`; bundle integrity
validation detects unreviewed checklist changes.

Check declared applicability before applying a heuristic: narrative shots need
observable events and intent; static character sheets, location plates, UI,
product references, music beds, SFX, and ambience do not need a story obstacle.
Static assets need composition and visible-consistency checks. Prefer positive
observable direction; concise technical exclusions and explicit preservation
constraints are permitted. Supported parameters are checked against the selected
tool/mode, and exact screen text remains an output-QA requirement.

## Element completeness review

In addition to checking prompt quality, the sub-agent **must** review the
complete set of prompts for a scene or project against the **Element
identification checklist** in AGENTS.md. This is a separate pass from the
per-prompt quality review — it checks whether the plan or prompt set is
*missing* elements that should exist, not whether existing prompts are
well-written.

### How to run the element completeness pass

When the sub-agent receives a set of prompts for review, it also receives:

1. The beat structure / scene description for each shot.
2. The full Elements table from the project's `project.md` or plan (if
   available).

The sub-agent walks every beat of every scene/shot and checks whether every
required visible element has a corresponding reference. Incidental objects
do not automatically require a sheet, and generated native sound does not
require a separate library asset. Canonical inputs may be unresolved during
draft breakdown; dependent production submission requires their evidence:

| Check | What to look for |
|---|---|
| On-camera characters | Do recurring or identity-critical on-camera characters have approved canonical references, while incidental people use approved descriptors? For screen-only callers, lock the visible call UI and describe moving callers/dialogue in text; do not attach character sheets as static screen content. |
| Locations / settings | Do recurring or geography-critical spaces have approved canonical location references? Incidental settings may use scene-level direction or keyframes; a distinct transitional or screen-only setting alone does not require a location sheet. |
| Props (held/operated) | Do branded, recurring, story-critical objects and scene-variant wearables have an approved `prop_` reference? Incidental objects may remain text-only; always-worn outfit items stay in the character sheet. Is independently relevant packaging accounted for? |
| Screen / UI surfaces | Does every phone screen, laptop screen, tablet, monitor, signage, or text-heavy surface that shows specific content have a `screen_` reference? |
| Brand / title cards | Does every ad/scene that needs a brand end card, lower third, or logo plate have a `card_` image defined? |
| Audio assets | Does every explicitly separate or reusable audio asset have a defined source? Native full-soundscape generation does not require separate sound-bed assets. |
| Costume variants | If a character wears a different outfit in different scenes, is the variant noted or generated as a separate prop sheet? |

### Reporting element findings

The sub-agent reports element completeness findings in a separate section:

```text
### Element Completeness Review

#### Missing elements
1. [CRITICAL] <Element description> — appears in <ad/scene> beat <timestamp>
   but a required canonical reference is missing; fidelity cannot be verified.
   Suggested action: Generate a <char_/loc_/prop_/screen_/card_> reference.

2. [MAJOR] <Element description> — referenced in <ad/scene> but not in the
   Elements table. May need a dedicated sheet.

#### Element coverage
- Characters: <count> defined, <count> referenced, <list any gaps>
- Locations: <count> defined, <count> referenced, <list any gaps>
- Props: <count> defined, <count> referenced, <list any gaps>
- Screen UIs: <count> defined, <count> referenced, <list any gaps>
- Title cards: <count> defined, <count> referenced, <list any gaps>
- Audio assets: <count> defined, <count> referenced, <list any gaps>
```

### Severity for element findings

- **CRITICAL:** A required identity/product/text reference is absent from a
  production request, preventing its fidelity requirements from being checked.
  Resolve the required input before dependent submission.
- **MAJOR:** An explicitly required production input is insufficiently defined
  to check its requested quality or continuity. Incidental people/settings and
  native sound do not become missing-reference findings solely from visibility.
- **MINOR:** An element could enhance the production but isn't strictly
  required (e.g. ambient SFX library for a quiet scene).

## Reference file

The consolidated review checklists for all prompt types live in:
`references/review-checklists.md`

Load the relevant section(s) when constructing the sub-agent prompt. The reference is
organized by prompt type with a table of contents at the top for quick navigation.

## Compose with other skills

- After a production prompt passes, return its snapshot path, request hash,
  reference bindings and review result to the caller. The caller must update and
  regenerate the persistent `showcase-html` canvas before submission and again
  after generated media arrives. `--quick` remains limited to ad-hoc files.
- For end-to-end production coordination, `film-production` is the production manager.
- This skill is called by the main agent during prompt-writing work; it does not call
  generation tools itself.
