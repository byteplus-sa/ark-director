# Restraint and shape patterns

Focused reference for `seedance-acting-console`. Read
[the entrypoint](../SKILL.md) for the analysis ladder and the emotion bank.

These patterns encode a tactic more precisely. They are craft heuristics, not
measured model behavior; check the take.

## First sign

When something starts to go wrong for a character (pain, doubt, a lie noticed),
encode only its earliest visible consequence: one channel, one small movement,
and nothing before it. "His fingers shift once inside the box, then go still"
carries more than a grimace. Use it as the first beat of a multi-stage arc, and
let the next trigger escalate it.

## Suppression arc

The single-transition template runs from a hidden feeling to a visible one.
When the tactic is to regain control, run it the other way:

```
The overall emotion shifts from <visible emotion> to <controlled surface>.
At first, <character> shows <one or two readable signs of the feeling>.
Then, <character> works to <tactic that restores control>, and <one sign>
gradually <steadies or stops>.
Finally, only <one residual cue> remains under a composed <face or posture>.
```

Pick a residual cue the framing can show. In a medium shot or wider, use a cue
with visible amplitude: one slow, deep breath that lifts the shoulders once, or
joined hands that press tight and release once. Keep fine cues such as a tremor
or a pulse for a close-up or an insert of that body part; at draft resolution a
small tremor in a medium shot does not read.

Example: "At first her breath is quick and her eyes keep returning to the
closed door. Then she presses her palms together and slows her breathing until
her shoulders settle. Finally, only one slow, deep breath lifts her shoulders
once under a still, composed face."

## Animal image

An animal image gives a tactic a body shape the actor and the model can both
read. Translate the image into observable cues; never leave the animal word
alone in the prompt.

| Image | Fits a tactic of | Observable cues |
|---|---|---|
| Snake strike | Ambush, sudden dominance | Body coiled and still for about 2 seconds, head level; then one fast lunge forward that stops dead at arm's length; stillness again, with <wardrobe> unchanged |
| Scorpion poised | Threat held in reserve | Hand raised and curled, fingertips pinching a small object, wrist arched; the hand stays motionless while the eyes watch |
| Cornered animal | Survival under pressure | Weight low and back, eyes fixed on the threat, breath fast through the nose, small sudden flinches |
| Hawk stillness | Watching for the opening | Head still and level, eyes tracking without blinking, only the head turns |
| Cat play | Toying with a weaker partner | Slow, loose movement, a relaxed half-smile, one sudden quick touch, then withdrawal |

A strike or other sudden speed change is a burst action. Plain wording already
produces it; in workspace 480p drafts a timed snake strike landed, with the coat
color drifting after the burst. What this pattern adds is control. Use at most
one per shot, give the still hold before it a length (about 2 seconds), keep a still
hold after it, and restate the wardrobe after the burst ("her charcoal coat
unchanged"): the burst is where wardrobe and identity drift. Record the
exception: the Seedance 2.5 prompt skill's scene-action guidance prefers slow,
continuous motion otherwise.

## Eyes through concealment

A veil, mesh, net or half-mask that leaves the eyes visible is a choice that
concentrates power in the eyes. Keep the concealment and let the eyes carry the
whole tactic: a fixed, steady gaze, a slow narrowing, one change of focus at
the turn. Ask for the eyes to stay readable through the covering ("her eyes
stay visible through the fine black mesh"). When the covering hides the eyes
too, use the hidden-face repair in
[hypothetical acting repairs](acting-repairs.md) instead.
