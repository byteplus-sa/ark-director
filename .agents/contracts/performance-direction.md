# Performance Direction

## Applicability and ownership

For new or materially revised character-performance scenes, both
`film-production` and `micro-drama` must coordinate:

1. `scene-craft` for scene craft under the selected framework, preserving
   supplied writing. The five-element engine is opt-in, not a universal gate.
2. `acting-direction` before shot design to establish intentions, listening
   and performance beats.
3. `seedance-fight-choreography` when staged fighting is in scope; exchange
   visibility requirements with shot design before finalizing either plan.
4. `seedance-shot-design` to make those beats readable with the approved
   framing, timing, camera and light.
5. `seedance-acting-console` to encode the plan for Seedance, then the selected
   video prompt skill and dialogue skill to compose the final request.

Leaves consume supplied artifacts; they do not invoke each other. For
non-Seedance work, use its selected prompt encoder without changing the model.
Canonical static images, empty plates, sound beds and deterministic graphics
do not need an acting plan. Incidental extras need disposition, not invented
personal arcs. Source-preserving edits inherit performance and inspect its
preservation; do not invent new acting unless it is part of `may_change`.
A static camera, silence or a covered face is not an acting exemption.

## Durable handoff

The caller stores `## Performance plan` in the existing scene file. It records
source script/scene locators, evidence status, locks, selected method,
per-character motive/goal/obstacle/tactic, ongoing physical channel,
listener task or disposition, and beat IDs connecting:

**Trigger -> what is registered -> attempt maintained/changed -> consequence.**

Record intentional non-response and sustained attention instead of requiring
an emotion change or tactic switch. Preserve quiet holds, ambiguity, exact
words and existing performance locks. Do not invent shared agreement, moral
traits, backstory or a revelation to satisfy a template.

Shot notes identify the relevant performance beats and critical acceptance
criteria. The submitted prompt carries the pursuit, trigger and readable
response once, not a full essay or an emotion-to-gesture checklist.
Reserve time for listening and response as well as speech. Coverage cannot
hide a required cue and then claim camera movement makes it readable.

Review evidence cites the current performance-plan file and its SHA-256,
alongside source, shot plan and exact request hashes. Use existing upstream
hash fields where supported; otherwise record the bindings in review evidence.
No new request schema or provider parameter is introduced. Changes to the
source interpretation, plan or encoded cues invalidate dependent prompt and
take reviews under the existing dependency rules. Do not migrate or backfill
historical projects or immutable prompt snapshots automatically.

## Prompt review

Applicability is unchanged in both review modes (`default` and `strict`).
Default mode requires a focused report for applicable acting/fight checks,
not the full unrelated checklist. Neither approval mode waives these checks.

Apply `acting.plan_bound` to applicable performance prompts and
`fight.readable_exchange` to staged-fight prompts. The caller includes those
IDs through the existing `--required-rule` review/registration interface.
The reviewer records a check even when the caller omitted it; missing
material evidence is `incomplete`, not assumed passing.

- `acting.plan_bound`: trace each critical beat from the supplied plan to
  the prompt; check partner/situation-directed pursuit, trigger, registration,
  listener/disposition, readable consequence and timing. Isolated prompt work
  may supply these facts inline. Mood-only studies are provisional.
- `fight.readable_exchange`: check participant identities, initial/final
  states, action -> apparent contact/avoidance -> reaction, prop ownership,
  readable framing, timing and continuity. Do not accept hidden contact as
  demonstrated or let a style preset change the locked outcome.

Material omissions or contradictions are MAJOR and block submission until
resolved. Record `not_applicable` with a scope-specific reason for nonacting
assets or preservation-only edits; preservation still needs its edit checks.
These checks are semantic reviewer obligations. The CLI validates the
declared checks and evidence structure, not acting quality automatically.
Only applicable checks belong in `--required-rule`: that interface requires
`pass` and rejects `not_applicable`. Record justified non-applicability in the
review's checks without adding that ID to the required-rule list.

## Actual-take acceptance

Use the brief's project-specific artistic criteria: intended audience response,
what carries attention and why the ending matters. Identify the observable
performance, picture and sound evidence needed for this scene before generation.
Do not substitute generic "cinematic" quality, a gesture count or camera variety
for those criteria. Body speed, amplitude, interruptions and recovery follow
source intent and plausibility; neither speech nor burst count sets an energy
ceiling. Optional burst holds must fit the selected pattern and source locks.

Before selecting or promoting a take, inspect playback and, when sound is in
scope, listen. Cite timestamps and the relevant beat IDs:

- Does the character register the intended event and pursue the intended
  task? Is persistence, adjustment or deliberate non-response legible?
- Do relevant listeners remain engaged or intentionally disengage?
- Do pacing, pauses and delivery serve the attempt while preserving exact
  dialogue? A transcript alone cannot establish this.
- Does the camera/crop/light reveal the required evidence? Do cut points
  preserve the intended response and state?
- For fights, do interactions, reactions and settled positions connect,
  without swapped participants, unexplained prop changes or broken limbs?

Missing a declared critical response, speaking assignment or required
interaction is a hard failure. Record less material differences against the
brief; do not require a particular blink, mandatory tears or literal cue count
when an equivalent performance achieves the intent. No passing take means a
bounded revision within budget or a blocked stage, not the least-bad selection.
Unavailable playback/listening stays unresolved. Final outputs need fresh
review. Recheck the actual edit so trimming does not remove the accepted beat.
Review what the edit and sound reveal, withhold and emphasize at full speed,
bound to the final artifact hash. Early sound intent may be provisional, but
final cue placement must follow the measured cut and actual listening.

Prompt checks, fixtures and validators are not evidence of improved generated
acting. Establish improvement only with authorized matched media comparisons.
