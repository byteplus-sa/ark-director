---
name: micro-drama
description: >-
  Produce vertical short-form micro-drama episodes end to end for any market:
  source-led 9:16 episodes, with an optional hook, reveal and cliffhanger
  template and optional to-be-continued card.
  Orchestrates a market story writer when one exists (for example
  filipino-micro-drama), then appealing canon sheets, planning-only
  storyboards, draft-first Seedance 2.5 scene clips with native dialogue bound
  to element references, speech-to-text dialogue QA with word-scoped fixes,
  ungraded assembly, loudness-matched delivery, and an optional full-episode
  showreel, all in a HyperFrames Studio project. Use for micro-dramas, vertical
  dramas, ReelShort/DramaBox-style series, TikTok drama episodes, or batches of
  several independent episodes produced in parallel. Do not use for a single
  prompt, a non-episodic ad, a music video, or long-form film; use
  film-production for general multi-scene work.
---

# Micro-Drama

Produce one or more vertical micro-drama episodes. The default proposal is a
reviewable 45–60 s unit built from three Seedance scene clips, not a mandatory
cadence or arc for supplied writing. This skill owns
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
   `approval_mode`, format, run budget, the native-dialogue audio route and an
   ungraded look in `project.md`, run `brief-intake` with a fast proposal, then
   run `studio_project.py init <project> --aspect 9:16 --resolution 1080p` (see
   the [production policy](../../contracts/production-policy.md); pre-Studio
   canvas projects with `showcase.json` keep the `showcase-html` canvas).
   Resolve the compact premise: intended audience response, what carries
   attention and why the ending matters. Alternatives are only for unresolved
   or requested direction. Record early sound and editorial intent, including
   silence, and project-specific artistic criteria for actual take and
   final-edit playback/listening; no final audio assets are needed at intake.
2. **Breakdown.** For new or revised character performances, run
   `acting-direction` before shot design and record `## Performance plan`
   under the [performance contract](../../contracts/performance-direction.md).
   Use `scene-craft` for the selected framework without forcing its
   five-element engine. Coordinate `seedance-fight-choreography` for fights.
   Hook/Turn/Cliffhanger at about 15/20/15 s is an optional episode template.
   Preserve supplied structure, including scenes without a turn. Derive clip
   groupings and shot durations from perception and generation feasibility;
   equal timing, repeated framing and sustained holds need no contrasting shot.
   Each scene gets a shot plan (size, angle, move or hold and light per shot)
   from `seedance-shot-design`. Choose actor energy, camera energy and edit
   rhythm separately. Kinetic dialogue is valid when required delivery and
   performance retain readability at the planned framing and speed.
   Walk every beat against the element-identification
   contract.
3. **Canon.** Character sheets, location plates and threshold props as
   three-sample Seedream sets. Design every character to be appealing and spread
   a natural range of complexions across the cast. Inspect every image and
   select with hash-bound decisions.
4. **Storyboard.** Optional planning and review grid per scene. It is never
   bound as a Seedance reference; its staging goes into the prompt text. Skip
   the stage when the shot plan already carries the staging.
5. **Audio preparation.** Mark it skipped unless the user requests a separate
   lip-sync track. Native Seedance audio carries the dialogue.
6. **Shots.** Encode performance beats with `seedance-acting-console`.
   Require applicable `acting.plan_bound` and `fight.readable_exchange` checks.
   Inspect actual registration, listening, response and delivery before
   selecting or promoting takes; transcript accuracy alone is insufficient.
   Preserve deliberate stillness and exact dialogue without motion quotas.
   Write each clip prompt from its shot plan with
   `seedance-prompt-25` and the market's dialogue partner skill (for Filipino,
   `seedance-prompt-25-filipino`), binding element references only. Apply the
   prompt, dialogue-timing and QA rules in the
   [production recipe](references/production-recipe.md), and run
   `prompt-review`. Register the operations, submit independent planned clips in
   parallel as 480p native Drafts, QA each Draft, then promote the selected
   Drafts to 1080p and QA the finals again.
7. **Assembly.** In Studio, follow the approved structure. The default template
   places the cold open first, then title, scenes and to-be-continued card; cuts,
   holds and transitions follow editorial intent, in original
   colours with no grade. Fix wrong words with word-scoped audio patches. Add a
   subtitle sidecar for each requested language and normalize loudness. Omit
   sidecars only for an explicit no-subtitles choice. Picture and audio locks come from
   real playback and listening evidence. Verify that trims retain accepted
   performance beats and any fight exchange continuity. Review the project's
   artistic criteria with artifact hashes and timestamps; final sound cues
   follow the measured cut and actual listening. Missing inspection or a failed
   critical criterion blocks acceptance in either approval mode.
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
- When the optional hook template is selected, place its hook in the first
  3 s; a title card must not consume that window. Preserve a supplied held
  opening or different ending instead of imposing this arc.
- Every spoken line is checked word by word against the locked dialogue with
  speech-to-text before a take can pass. A model's own summary of what was
  said is not sufficient.
- Retakes fix hard-gate failures only, within the declared budget, as a new
  Draft. Dialogue errors are patched word by word, never re-dubbed whole.
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
