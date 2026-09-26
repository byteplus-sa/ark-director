---
name: film-production
description: Orchestrate an AI-assisted film, commercial, music video, or narrative production across brief, development, canon, storyboard, audio, shot generation, review, assembly, and delivery while maintaining one required showcase-html production canvas through every stage. Use when a request spans multiple scenes or modalities, asks to create or continue a film project, requires coordination between deterministic HTML-entrypoint graphics, Seedream, Seed Audio, Seedance, HyperFrames, or FFmpeg, or needs the next safe production step rather than a single prompt. Do not use for an isolated image, audio, video, or editing request that one specialist skill can complete independently.
---

# Film Production

Manage one coherent production run while keeping specialist skills modular. Read
the project's `project.md` and existing manifests first, inspect the existing
project before creating anything, and advance only as far as the available
evidence and mode-authorized decisions permit.

## Core operating model

- Act as the single manager communicating with the user.
- Treat project files and manifests as production memory; do not rely on chat
  history alone.
- Treat the persistent `showcase.json` plus generated `index.html` as the
  cumulative production canvas used for every stage review and handoff.
- Delegate modality work by invoking the narrowest applicable project skill.
- Prefer a deterministic workflow when the next action is known. Use agentic
  judgment for creative choices, contradiction resolution, and review.
- Never infer approval from provider success. Technical success places an
  output in `review`; a passing review and recorded decision may approve it.
- Never submit a replacement generation because local polling timed out. Resume
  the provider task recorded in `task_ids.json`.
- Never silently replace user writing, approved canon, selected variants, or
  unrelated project state.

## Start or resume a run

1. Resolve the project directory. Search before creating a project, scene,
   element, shot, or same-purpose artifact.
2. Read `project.md`, `handoff.md` when present, `task_ids.json`,
   `showcase.json`, relevant element manifests, scene and shot manifests,
   prompt snapshots, and the latest review decisions. `handoff.md` is a resume
   hint; manifests and the registry are authoritative on conflict. If a production project has no canvas, initialize the eight-stage
   skeleton before advancing it. New projects set
   `approval_mode: approve_for_me` in `project.md` frontmatter before `--init`.
   The alternative is `ask_for_approval`. A missing field in a legacy project
   means `approve_for_me` for new decisions only; historical selections stay as
   recorded. Reject an invalid or unreadable mode.
   - **Never hand-write `showcase.json`.** Create the canvas only with the
     canonical tool: `uv run python
     .agents/skills/showcase-html/scripts/generate_showcase.py <project>
     --init`, then open the generated `index.html`. The project directory must
     already contain `project.md` (the tool validates it before initializing)
     and the canonical shape is `canvas.stages[]` — not a top-level `stages`
     object. A hand-written manifest drifts from the schema the checker
     enforces and silently fails later stage updates. If you inherit a
     hand-written manifest, run the tool's `--check` against it and rebuild
     from the tool rather than patching the structure by hand. Delegating
     scaffolding to a sub-agent does not exempt this: the scaffold prompt must
     include the exact `--init` command, the `project.md` prerequisite, and a
     prohibition on hand-authoring the manifest.
3. Determine the current stage from recorded artifacts and lifecycle states.
   Do not infer completion from filenames alone.
4. Identify contradictions, missing inputs, stale dependencies, pending provider
   tasks, and decision gates. Recheck the effective mode before each decision;
   a stale mode read cannot authorize a selection or lock.
5. State the current stage, the next safe objective, required specialist skills,
   and any user decision needed before spending credits.

Read [stage-contracts.md](references/stage-contracts.md) for entry evidence,
required outputs, and exit conditions. Read
[handoff-contracts.md](references/handoff-contracts.md) before moving an artifact
between modalities.

## Route specialist work

<!-- markdownlint-disable MD013 -->

| Production need | Primary skill |
| --- | --- |
| Brief intake and directorial defaults | `brief-intake` |
| Brand-ad / reference-video inspiration | `template-factory` for reverse-engineering; `ark-mcp` (`seed_understand`) for lighter analysis — prefer a usable public HTTPS URL; download and upload only when needed |
| Character identity asset | `seedream-character-sheet` |
| Character sheet cleanup | `seedream-character-sheet-cleanup` |
| Location identity asset | `seedream-location-asset` |
| Exact static typography, poster, title/end card, UI, product grid, price/CTA treatment, or transparent overlay | `html-graphic-render` |
| General image generation or edit | `seedream-prompt` or `seedream-edit` |
| Storyboard and visual continuity | `seedream-storyboard` |
| Seed Audio prompt | `seed-audio-prompt` |
| Narrative audio commercial | `seed-audio-commercial` |
| Seedance 2.5 video prompt | `seedance-prompt-25` |
| Filipino or Taglish video dialogue | `seedance-prompt-25-filipino` with `seedance-prompt-25` |
| Seedance 2.0 video prompt | `seedance-prompt-20` |
| Footage-driven VFX prompt | `seedance-vfx-prompt` |
| End-to-end Seedance 2.0 VFX shot | `seedance-vfx-pipeline` |
| Model submission, polling, or artifact access | `ark-mcp` |
| Animated exact graphics or timed overlays | appropriate HyperFrames skill |
| Assembly, media transforms, captions, or final video composition | appropriate HyperFrames or FFmpeg skill |
| Persistent stage canvas, review and selection | `showcase-html` |

<!-- markdownlint-enable MD013 -->

If the needed lifecycle role does not exist, keep the work at its current stage
and record the gap. Do not disguise a generic prompt as a completed production
department workflow. The local-only `specs/SPEC_FILMMAKING_LIFECYCLE_SKILLS.md`
is optional future-planning context, not a required runtime dependency. It records planned
coverage.

## Run one stage at a time

For the active stage:

1. Record the stage objective and observable acceptance criteria.
2. Confirm every input path, selected variant, lifecycle state, and SHA-256.
3. Invoke only the specialists needed for that stage.
4. Persist exact prompts beside generated media and update the owning manifest.
   For deterministic static graphics, persist the editable HTML entrypoint,
   local CSS/SVG dependencies, input/font hashes, render record, and PNG instead
   of a model prompt or provider task.
5. Persist and inspect every actual output, not only provider response metadata.
   Set generated outputs to `review`. Images need visible inspection, video
   needs temporal inspection, and audio needs listening evidence in addition to
   technical checks. Reject hard-gate failures and rank passing candidates
   against the brief's recorded criteria; no passing candidate blocks selection.
6. In `approve_for_me`, record a hash-bound review and agent decision, then use
   the validated writer to select the best passing candidate. In
   `ask_for_approval`, record a recommendation and wait for the user's decision;
   a recommendation does not set `selected_variant` or `approved`. Preserve
   explicit user locks in either mode.
7. Update the active stage in `showcase.json` with every input, exact prompt,
   element binding, output, QA result and decision. Regenerate and inspect
   `index.html` after every material change, including autonomous decisions.
8. Run `generate_showcase.py <project> --check --stage <stage-id>`. A missing,
   stale, or incomplete canvas keeps the stage open in either mode.
9. Advance only when the stage exit contract is satisfied.

At the brief/development stage, run `brief-intake` before writing the brief's
required output: it proposes genre-appropriate defaults per directorial axis
(structure, camera, lens, lighting, grade, pacing, acting, staging, medium,
audio) in fast mode by default, or full Q&A when the user opts in, and persists
the mode-authorized confirmed set as a `locked` block in `project.md`.

## Approval and spending gates

`approve_for_me` is the default for local production decisions. It authorizes
the agent to confirm directorial defaults and select passing canon, storyboard
panels, video takes, and picture/audio/final local master locks within the
brief's stated scope and run budget. Each decision needs current input/output
hashes, passing modality-specific QA, a recorded reason and actor, and a
validated write. A tie uses stable operation ID and variation-index order.
Unavailable inspection, a hard-gate failure, stale evidence, or no passing
candidate blocks approval. Do not promote the least-bad output merely to
advance.

In `ask_for_approval`, present candidates, material differences, review
evidence, and a recommendation; wait for the user's selection or lock before
advancing. Neither mode may silently replace an explicit user selection or
lock. Rights, real-person likeness/voice consent, new spending beyond the
declared run budget, external delivery, and publishing need their own scope or
authorization. An approval to generate never approves its result. Record
estimated and confirmed cost separately and reconcile ambiguous submissions.

## Handle revisions

Write every revision as:

- **Locked decisions:** properties that must remain unchanged;
- **Requested delta:** the single intended change where practical;
- **Acceptance criteria:** observable evidence of success;
- **Known rejections:** previously rejected outcomes that must not return;
- **Invalidation scope:** dependent artifacts that return to `review` if inputs
  change.

Prefer a bounded edit over full regeneration after composition or performance is
approved. Preserve rejected history and never overwrite source media.

## Finish the run

Report the stage reached, artifacts created or changed, canvas path and freshness
check, review status, provider tasks still running, costs when known, unresolved
risks, and the next production decision. A production run is complete only when
its active stage exit contract is satisfied; the local film is complete only
after its inspected master has a mode-authorized final lock. External delivery
or publishing remains a separate action.

## Submission recovery

Persist each exact prompt snapshot and reviewed prepared request in the project
registry before submitting. Record the provider task ID as soon as available.
An ambiguous timeout leaves `submission_unknown`: reconcile that operation or
resume its known task; never repeat submission automatically or switch transport
to submit a duplicate. Any new authorized take gets a new operation record.
