---
name: seedance-fight-choreography
description: Plan fictional screen fights with readable action and continuity. Use for fight choreography, brawls or staged combat prompts. Not for real-world combat instruction or generation.
---

# Seedance Fight Choreography

Return screen direction, not a martial-arts lesson or a production operation.
Keep narrative outcome, performance intent, approved medium, dialogue, timing,
cast and prop locks authoritative. Choreography makes those choices visible;
it does not supply a new winner, emotional arc or compulsory fighting style.

## Boundary

- Work from supplied text and caller-provided evidence. Do not call tools,
  invoke sibling skills, launch subagents, generate media, install dependencies
  or modify production state. Return any missing evidence request to the caller.
- Describe fictional appearance, staged contact or avoidance, reactions and
  resulting positions. Do not teach vulnerable targets, injury mechanics,
  force optimization or real-world weapon, disarm, restraint-escape or
  fighting drills. Ordinary fictional strikes, holds and prop-blade exchanges
  can be described as non-instructional screen events. A fictional label
  does not make operational injury instruction safe.
  For such requests, decline that detail and offer non-instructional screen
  action, separation, a cutaway or aftermath that serves the approved story.
- Treat physical stunt execution as outside scope. Apparent contact and
  falls in this plan are not rehearsal instructions or safety certification.
  Live performance needs qualified stunt supervision.
- The caller owns authorization, canon, reference selection, rights and
  likeness handling, generation, request registration, draft tracking, prompt
  review, media inspection and approval. This skill grants none of them.
  For new Seedance 2.5 requests, the caller must use native Draft mode with
  explicit `resolution: "480p"` and boolean `draft: true`, including edits and
  retries. Never fall back to ordinary 480p or promise a final from this plan.
- Do not bind storyboards, panels, sheets or animatics as video references.
  Blocking maps are analysis-only by default; carry geometry in text.
  Caller-selected conditioning requires separate approval and live support.

## Read By Need

Read [Choreography Contract](references/choreography-contract.md) for every
plan or repair, and [Continuity QA](references/continuity-qa.md) before returning
it. Read [Screen Style Options](references/screen-style-options.md) only when
style selection or intensity needs resolution. Read
[Screen Action Vocabulary](references/screen-action-vocabulary.md) for concrete
strike, avoidance, grapple, prop and recovery wording. See
[Source Notes](references/source-notes.md) for attribution and adaptation limits.
Do not ingest books, videos or new source libraries as part of this leaf.

## Inputs And Procedure

1. **Bound the change.** Identify scene/shot IDs, supplied scene beats, dramatic
   function, required ending and requested delta. Separate locked facts from
   proposals and missing facts. Preserve exact dialogue, language, register,
   delivery, silent holds, costume, injury state and medium. Do not assume
   action means anger, dominance, a knockout, live action or a kinetic camera.
2. **Record style explicitly.** Use the selected style per actor, including
   custom, mixed or explicitly no named style. If none was supplied, record
   `style_selection: unspecified`; describe only the supplied action without
   importing JKD or Wing Chun. Ask when recognizability materially matters.
   A style choice never authorizes a real person's likeness or voice.
3. **Establish state.** Map stable actor IDs to supplied identities. Record
   world marks, camera-relative positions, facing, posture, visible limbs,
   movement paths and prop ownership. Include silent actors and extras.
   Do not infer unseen hands, weapons, exits or offscreen outcomes.
4. **Build readable beats.** Use one primary state change per beat:
   start -> initiating actor/action -> apparent contact or avoidance ->
   motivated reaction -> end. Include a held or aborted action when that is
   the beat; every fight need not escalate or make contact. Name the anatomy
   and its frame side where relevant, and describe the visible result rather
   than technical technique mechanics.
5. **Fit staging and time.** Carry the caller's shot plan unchanged. Name what
   must remain readable through the framing and any occlusion. Reserve room
   for reaction, recovery and locked dialogue; use ordered beats unless timing
   is supplied or needed. Timed ranges are provisional budgets, not guaranteed
   frame-exact control. If locked scope cannot fit, return the conflict and
   options for approval instead of speeding speech or adding cuts.
6. **Check and hand back.** Run the text-level QA reference. Repair only within
   the requested scope. Distinguish `complete` for a coherent text plan from
   `incomplete` for unresolved material inputs; neither means prompt-review
   approval or verified generated motion.

## Composition Contracts

These are caller-owned data handoffs, not an invocation sequence. Consume only
the selected companion's supplied output. If a companion is absent, return
the missing fields or questions; do not install it, claim it ran or silently
substitute a different craft framework.

| Companion | Consume | Return |
| --- | --- | --- |
| `scene-craft` | Locked scene events, character knowledge, dramatic function, selected craft framework and outcome | Beat-to-story mapping and unresolved narrative conflicts; no new mandatory reversal or winner |
| `acting-direction` | Playable intentions, partner-directed tasks, performance limits and approved transitions | Action opportunities and reaction triggers that retain those intentions |
| `seedance-shot-design` | Shot IDs, durations, size, angle, move, lens intent, named light sources and locks | Visibility needs, action windows and proposed coverage changes for its owner to resolve |
| `seedance-acting-console` | Supplied tactic and framing-readable cue block | Beat triggers and visible reaction channels; no replacement emotion template |
| `blocking-map` | Actor-to-mark mapping, facing, paths, crops, obstacles and camera axis | Start/end geometry and occlusion questions, not a reference attachment |
| `seedance-prompt-25` | Prompt operation, subject bindings, approved shot facts and locked audio context | One action block per shot/stage, state invariants and observable acceptance criteria for its six-part grammar |

Keep supplied actor IDs stable across all contracts. Diagram letters are text
handles, not wardrobe, on-screen text or newly approved identities.

## Return Package

Use the compact record in the choreography contract. Always return:

1. Scope, locks, explicit style status, intensity limits and unresolved inputs.
2. Actor/prop start state, ordered beat ledger and required final state.
3. Paste-ready action text grouped by existing shot or stage. Describe each
   action once, carry the selected medium, and retain supplied dialogue
   verbatim when included. Leave final reference tokens, parameter packaging
   and audio grammar to `seedance-prompt-25`.
4. Text QA findings and caller acceptance checks, with evidence limits.

For a repair, identify the failed beat, its prior state and the smallest
wording/staging delta. Do not rewrite unaffected beats or claim that a
prompt-only revision fixed an unseen take. When inputs are incomplete, return
the usable portion plus targeted questions rather than inventing canon.
