---
name: micro-drama
description: >-
  Produce vertical short-form micro-drama episodes end to end for any market:
  a hook in the first seconds, a mid-episode reveal or confrontation, and a
  close-up cliffhanger, delivered as 9:16 episodes with a to-be-continued card.
  Orchestrates a market story writer when one exists (for example
  filipino-micro-drama), then appealing canon sheets, planning-only
  storyboards, review-mode-aware Seedance 2.5 scene clips with native dialogue bound
  to element references, speech-to-text dialogue QA with word-scoped fixes,
  ungraded assembly, loudness-matched delivery, and an optional full-episode
  showreel, all in a HyperFrames Studio project. Use for micro-dramas, vertical
  dramas, ReelShort/DramaBox-style series, TikTok drama episodes, or batches of
  several independent episodes produced in parallel. Do not use for a single
  prompt, a non-episodic ad, a music video, or long-form film; use
  film-production for general multi-scene work.
---

# Micro-Drama

Produce one or more vertical micro-drama episodes. Each episode is a complete,
reviewable 45–60 s unit built from three Seedance scene clips. This skill owns
the episode format and its production sequencing. Market story craft, such as
tropes, dialogue register and cultural signifiers, belongs to a market writer
skill. Stage, approval, Studio, prompt-review and submission rules come from
`AGENTS.md` and the production contracts; this skill does not restate or relax
them.

## Inputs and outputs

Input: a market or audience, a premise or formula, the episode count, and any
locked dialogue, cast, budget or approval mode. When a market writer skill
exists for the audience, obtain a locked episode brief from it first. Otherwise
draft the brief with the fields in
[episode structure](references/episode-structure.md).

Output per episode: a project under `projects/<slug>/` with all eight production
stages closed, a final master (1080×1920 H.264/AAC), subtitle sidecars in the
requested languages, locks, and an honest defect list. Confirm subtitle
languages or an explicit no-subtitles choice in the brief; never assume English.
For a batch, also a portfolio page
and an optional full-episode showreel.

## Workflow

1. **Brief.** Lock logline, formula, a cast of at most three recurring
   characters, one or two locations, threshold props, and exact dialogue per
   scene within the language-aware timing budget in
   [episode structure](references/episode-structure.md). Record
   independent `review_mode` (default unless strict is requested), `approval_mode`,
   format, run budget, the native-dialogue audio route and an
   ungraded look in `project.md`, run `brief-intake` with a fast proposal, then
   run `studio_project.py init <project> --aspect 9:16 --resolution 1080p` (see
   the [production policy](../../contracts/production-policy.md); pre-Studio
   canvas projects with `showcase.json` keep the `showcase-html` canvas).
2. **Breakdown.** Three scenes: Hook (about 15 s), Turn (about 20 s),
   Cliffhanger (about 15 s). Each scene is one multi-shot Seedance clip with
   internal cuts, and each gets a shot plan (size, angle, move and light per
   shot) from `seedance-shot-design` at standard energy by default; kinetic is for
   shots without spoken lines. Walk every beat against the element-identification
   contract.
3. **Canon.** Character sheets, location plates and threshold props as one
   Seedream image each by default, three-sample sets in strict mode, or the
   user's requested count. Design every character to be appealing and spread
   a natural range of complexions across the cast. Inspect every image and
   select with hash-bound decisions.
4. **Storyboard.** Optional planning and review grid per scene. It is never
   bound as a Seedance reference; its staging goes into the prompt text. Skip
   the stage when the shot plan already carries the staging.
5. **Audio preparation.** Mark it skipped unless the user requests a separate
   lip-sync track. Native Seedance audio carries the dialogue.
6. **Shots.** Write each clip prompt from its shot plan with
   `seedance-prompt-25` and the market's dialogue partner skill (for Filipino,
   `seedance-prompt-25-filipino`), binding element references only. Apply the
   prompt, dialogue-timing and QA rules in the
   [production recipe](references/production-recipe.md). Default review mode uses
   minimal inline preflight without a full checklist or prompt-review report.
   Register the operations, submit the three clips in parallel at the final
   target, then inspect the actual outputs. Strict mode runs `prompt-review`
   and uses 480p native Drafts before selected promotion and fresh final QA.
   Requested or concretely justified drafts may use that route in default mode.
7. **Assembly.** In Studio, place the cold open first, then the title card, the
   three clips with short dissolves, and the to-be-continued card, in original
   colours with no grade. Fix wrong words with word-scoped audio patches. Add a
   subtitle sidecar for each requested language and normalize loudness. Omit
   sidecars only for an explicit no-subtitles choice. Picture and audio locks come from
   real playback and listening evidence.
8. **Delivery.** Final lock and passing Studio stage-exit checks, with the final
   master from `studio_project.py render`; FFmpeg assembly, subtitle and
   loudness work is placed in Studio as a clip or overlay and rendered, not
   delivered directly (pre-Studio canvas: `--check --stage delivery`).

For a batch of episodes, follow [batch production](references/batch-production.md):
one agent per episode with exclusive project ownership, on-disk checkpoints,
and a single integrating manager.

## Non-negotiables

- Generated footage stays text-free. Titles, cards and subtitles are added in
  post from deterministic sources; no AI or fictional label is added unless
  required.
- Storyboards are never Seedance references. Bind character, location and prop
  elements; write staging in the prompt.
- The hook lands within the first 3 s of the delivered episode. Never let a
  title card consume the hook window.
- Every spoken line is checked word by word against the locked dialogue with
  speech-to-text before a take can pass. A model's own summary of what was
  said is not sufficient.
- Retakes fix hard-gate failures only, within the declared budget, at the
  mode-appropriate target. Dialogue errors are patched word by word, never re-dubbed whole.
  Record residual defects instead of silently promoting a flawed take.
- Provider success is `review`, never approval. Never resubmit an ambiguous
  paid operation; reconcile it from the task registry.

## References

| Need | Reference |
| --- | --- |
| Beat timing, hooks, reveals, cliffhangers, cards, brief fields | [Episode structure](references/episode-structure.md) |
| Canon appeal, prompt clauses, dialogue timing, draft-promote, QA gates, word-scoped fixes, budget, assembly | [Production recipe](references/production-recipe.md) |
| Several episodes in parallel, checkpoints, portfolio, showreel | [Batch production](references/batch-production.md) |

Workspace contracts: [production policy](../../contracts/production-policy.md),
[element identification](../../contracts/element-identification.md),
[audio-video alignment](../../contracts/audio-video-alignment.md).
