# Restraint and shape patterns

Focused reference for `seedance-acting-console`. Read
[the entrypoint](../SKILL.md) for the supplied-intent contract and optional
cue bank. These are encoding options, not required emotion classifications.

These patterns encode a tactic more precisely. They are craft heuristics, not
measured model behavior; check the take.

## First sign

When something starts to go wrong for a character (pain, doubt, a lie noticed),
encode only its earliest visible consequence at the supplied trigger: one
channel and one small movement. For example, "His fingers shift once on the
box rim, then go still" works only if that hand is visible at the selected
scale. Preserve preceding locked action. Escalate only if a later supplied
beat calls for it; a first sign can remain the entire response.

## Suppression arc

When the supplied tactic is to regain control, encode a response toward
containment rather than automatically escalating emotion:

```text
At <supplied beat/trigger>, <character> shows <one or two readable signs>.
To <supplied intent>, <character uses the physical channel>, and <one sign>
gradually <steadies or stops>.
Finally, only <one residual cue> remains under a composed <face or posture>.
```

Pick a residual cue the framing can show. In a medium shot or wider, use a cue
with visible amplitude: one slow, deep breath that lifts the shoulders once, or
joined hands that press tight and release once. Keep fine cues such as a tremor
or a pulse for a close-up or an insert of that body part; at draft resolution a
small tremor in a medium shot does not read.

Hypothetical example: "At first her breath is quick and her eyes keep returning
to the closed door. Then she presses her palms together and slows her breathing until
her shoulders settle. Finally, only one slow, deep breath lifts her shoulders
once under a still, composed face."

## Animal image

An animal image gives a tactic a body shape the actor and the model can both
read. Translate the image into observable cues; never leave the animal word
alone in the prompt.

| Image | Fits a tactic of | Observable cues |
| --- | --- | --- |
| Snake strike | Ambush, sudden dominance | Body coiled and still for the supplied hold, head level; then one fast lunge forward that stops dead at arm's length; stillness again, with supplied wardrobe unchanged |
| Scorpion poised | Threat held in reserve | Hand raised and curled, fingertips pinching a small object, wrist arched; the hand stays motionless while the eyes watch |
| Cornered animal | Survival under pressure | Weight low and back, eyes fixed on the threat, breath fast through the nose, small sudden flinches |
| Hawk stillness | Watching for the opening | Head still and level, eyes tracking without blinking, only the head turns |
| Cat play | Toying with a weaker partner | Slow, loose movement, a relaxed half-smile, one sudden quick touch, then withdrawal |

A strike or other sudden speed change is a burst action. For this pattern,
use at most one per shot, a still hold before it and a still hold after it,
and restate supplied wardrobe after the burst ("her charcoal coat unchanged").
These controls aim to reduce motion and identity drift, not guarantee it.
Use supplied timing; about 2 seconds is only a provisional pre-burst hold when
timing is open. Return a conflict for caller retiming/splitting when the pattern
cannot fit locked beats. Do not erase additional locked actions or invent
wardrobe. The caller reconciles this burst with the surrounding motion plan.

## Eyes through concealment

A veil, mesh, net or half-mask can leave the eyes visible. Keep the concealment
and select only eye cues that serve the supplied tactic and are readable at
the shot's scale: a steady gaze or one change of focus at the supplied trigger.
Do not require all cues or enlarge the framing to show them. When supported
by the source, preserve visibility ("her eyes stay visible through the fine
black mesh"). When the covering hides the eyes too, or the shot is too wide,
use posture, spacing or the physical task as in the hidden-face repair in
[hypothetical acting repairs](acting-repairs.md) instead.
