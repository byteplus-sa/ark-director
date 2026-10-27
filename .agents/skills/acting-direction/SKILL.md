---
name: acting-direction
description: Direct character objectives, tactics, listening and performance beats. Use for scene acting, dialogue delivery or flat performances. Not for generation or model-specific cue encoding.
---

# Acting Direction

Give the character work to do, not an expression to display. Return a
model-independent performance plan derived from the supplied scene.
The caller composes this with `scene-craft`, `seedance-shot-design` and
`seedance-acting-console`. This leaf never invokes them, generates media,
changes production state or approves a take.

## Inputs and authority

Read the whole supplied scene, its ending, preceding circumstances and
character knowledge before directing a line. Preserve locked words, language,
register, outcome, medium, timing and performance choices. Mark facts as
established, inferred or missing; label new interpretations as proposals.
An excerpt permits a scoped reading, not invented context.

Read [Performance plan](references/performance-plan.md) for every plan.
Read [Repair cases](references/repair-cases.md) for flat, overstated or
unreadable performances. Missing framing does not prevent a provisional
acting plan; its visibility checks remain unresolved until shot design.

## Analysis order

1. **Event and scene direction.** Read the ending back through the scene.
   Name what happens between these people, separate from the film's theme
   or the audience's discovery. Consider the shared-direction method below;
   do not impose it on a scene whose approved intentions conflict with it.
2. **Given circumstances and motive.** What does each character know, and why
   does this encounter matter to them now? Distinguish actual history from
   an interpretation. Do not invent guilt, trauma or a cultural belief to
   make a performance interesting.
3. **Personal goal.** What does this character need from the other person,
   or from the immediate situation? Use a playable objective, not "show grief"
   or "deliver the plot twist".
4. **Obstacle and stakes.** What resists the attempt, and what could be lost?
   An internal pressure can matter as much as an external barrier. Record
   ambiguity when the scene intentionally withholds the answer.
5. **Tactic and physical channel.** What is the character doing to pursue
   that goal: reassure, delay, test, distract, challenge, conceal? Which
   ongoing activity carries it? The task can happen through listening or
   purposeful looking, not only through large bodily action.
6. **Register and adjust.** At each material line/action trigger, identify
   what the character notices, how it affects their attempt and whether
   they persist, change tactic, withhold action or let control slip.
   A beat is not a compulsory expression change. Preserve sustained pursuit.
7. **Listeners and contrast.** Give silent scene participants an appropriate
   task or disposition. Distinguish motives and tactics; do not give both
   partners identical emotion cues. Incidental crowds need only relevant
   disposition; an unconscious person is not assigned conscious listening.
8. **Handoff and criteria.** Return the compact plan, unresolved choices and
   a few observable success/failure criteria. The shot designer determines
   readability; the model-specific encoder derives cues without changing
   intent. Neither camera movement nor a cue count proves acting quality.

## Shared-direction method

The downloaded Higgsfield acting skill attributes this approach to Tigran.
Retain it as a named craft method, not a universal law or performance guarantee.
The meaning of the old repository prefix is not established by that attribution.

In this method, the scene direction is a shared, often unspoken agreement:
for example, two people try to make a departure painless. Their motives and
personal goals differ. One may protect the person leaving; the other may
try to leave without a visible rupture. Feeling presses against the shared
direction, while ordinary activity gives each person a different channel.

Look for the ending that names the event and the moment when the effort
fails, if it fails. Purposeful eye-work checks whether an attempt is landing;
it is not a fixed pupil/brow routine. Opposed qualities can enrich a pair,
but do not manufacture mirrored good/bad traits or shared agreement when
the script establishes incompatible intentions.

State `method: shared-direction` when using this interpretation, or name
the other selected approach. When none was selected, offer a brief-specific
tactic-first proposal rather than silently enforcing a school. Approval
of a method never authorizes rewriting locked pages.

## Output

Return:

- Scope, source beat/line locators, locks and evidence limits.
- Method, event, scene direction and each principal's motive/goal/obstacle.
- A beat ledger linking trigger -> registration -> tactic -> consequence.
- Listening/disposition for relevant silent characters and an ongoing
  physical channel for each principal.
- Readability needs, dialogue pauses and end-state continuity for shot design.
- Critical performance criteria for actual playback/listening.

In a production, the caller stores this as `## Performance plan` in the
existing scene file, binds its source hash in review evidence and carries
relevant beat IDs into shot notes. This is prose evidence, not a new provider
payload or a replacement production manifest.

## Review boundaries

For a flat-performance diagnosis, separate:

1. **Script:** no intelligible pursuit, opposition or meaningful event.
2. **Direction:** pursuit exists but is reduced to mood labels or gestures.
3. **Encoding/coverage:** the prompt omits it or the shot cannot reveal it.
4. **Generated take:** text is adequate but motion, timing or delivery fails.
5. **Edit:** the take's registration or response is trimmed away.

Do not claim the cause without the corresponding evidence. A prompt-only
assessment cannot judge the take; frame samples cannot establish listening
timing or vocal performance. Return timestamped observations only when actual
media has been inspected. No acting improvement is proven by adding a skill.

## Source and limits

Adapted from the existing workspace acting analysis and the user-supplied
`higgsfield-acting-skill.skill`, whose entrypoint attributes the method to
Tigran. No source-specific production examples or downloaded source library
are bundled here. New examples are hypothetical, not approved canon.
Model-independent direction does not establish model capability, rights to a
performer's likeness or voice, or permission to submit paid requests.
