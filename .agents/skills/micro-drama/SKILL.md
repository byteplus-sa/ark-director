---
name: micro-drama
description: >-
  Produce vertical short-form micro-drama episodes end to end for any market:
  a hook in the first seconds, a mid-episode reveal or confrontation, and a
  close-up cliffhanger, delivered as 9:16 episodes with a to-be-continued card.
  Orchestrates a market story writer when one exists (for example
  filipino-micro-drama), then canon sheets, text-free storyboard conditioning,
  Seedance 2.5 scene clips with native dialogue, dialogue-accuracy QA,
  assembly, loudness-matched delivery, and an optional full-episode showreel,
  all on the showcase-html production canvas. Use for micro-dramas, vertical
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
skill. Stage, approval, canvas and submission rules come from `AGENTS.md` and
the production contracts; this skill does not relax them.

## Inputs and outputs

Input: a market or audience, a premise or formula, the episode count, and any
locked dialogue, cast, budget or approval mode. When a market writer skill
exists for the audience, obtain a locked episode brief from it first. Otherwise
draft the brief with the fields in
[episode structure](references/episode-structure.md).

Output per episode: a project under `projects/<slug>/` with all eight canvas
stages closed, a final master (1080×1920 H.264/AAC), an English subtitle
sidecar, locks, and an honest defect list. For a batch, also a portfolio page
and an optional full-episode showreel.

## Workflow

1. **Brief.** Lock logline, formula, a cast of at most three recurring
   characters, one or two locations, threshold props, and exact dialogue per
   scene. Record `approval_mode`, format and run budget in `project.md`,
   run `brief-intake` in fast mode, then initialize the canvas with the
   canonical `--init` command.
2. **Breakdown.** Three scenes: Hook (about 15 s), Turn (about 20 s),
   Cliffhanger (about 15 s). Each scene is one multi-shot Seedance clip with
   internal cuts. Walk every beat against the element-identification contract.
3. **Canon.** Character sheets, location plates and threshold props as
   three-sample Seedream sets. Inspect every image and select with hash-bound
   decisions.
4. **Storyboard.** One grid per scene, bound to the selected canon. A grid is a
   composition anchor only.
5. **Audio preparation.** Mark it skipped unless the user requests a separate
   lip-sync track. Native Seedance audio carries the dialogue.
6. **Shots.** Write each clip prompt with `seedance-prompt-25` and the market's
   dialogue partner skill (for Filipino, `seedance-prompt-25-filipino`). Apply
   the storyboard-leak and dialogue rules in the
   [production recipe](references/production-recipe.md). Run `prompt-review`,
   register the operation, submit the three clips in parallel, and QA each take.
7. **Assembly.** Cold open first, then the title card, the three clips with
   short dissolves, and the to-be-continued card. Add a subtitle sidecar and
   normalize loudness. Picture and audio locks come from real playback and
   listening evidence.
8. **Delivery.** Final lock and a passing `--check --stage delivery`.

For a batch of episodes, follow [batch production](references/batch-production.md):
one agent per episode with exclusive project ownership, on-disk checkpoints,
and a single integrating manager.

## Non-negotiables

- Generated footage stays text-free. Titles, cards and subtitles are added in
  post from deterministic sources.
- The hook lands within the first 3 s of the delivered episode. Never let a
  title card consume the hook window.
- Every spoken line is checked word by word against the locked dialogue with
  speech-to-text before a take can pass. A model's own summary of what was
  said is not sufficient.
- Retakes fix hard-gate failures only, within the declared budget. Record
  residual defects instead of silently promoting a flawed take.
- Provider success is `review`, never approval. Never resubmit an ambiguous
  paid operation; reconcile it from the task registry.

## References

| Need | Reference |
| --- | --- |
| Beat timing, hooks, reveals, cliffhangers, cards, brief fields | [Episode structure](references/episode-structure.md) |
| Clip plan, prompt clauses, QA gates, retakes, budget, assembly | [Production recipe](references/production-recipe.md) |
| Several episodes in parallel, checkpoints, portfolio, showreel | [Batch production](references/batch-production.md) |

Workspace contracts: [production policy](../../contracts/production-policy.md),
[element identification](../../contracts/element-identification.md),
[audio-video alignment](../../contracts/audio-video-alignment.md).
