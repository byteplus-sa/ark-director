# Shot Staging

Focused reference for `seedance-prompt-25`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Shots or stages](#shots-or-stages)
- [Per-shot template](#per-shot-template)
- [Carrying a shot plan](#carrying-a-shot-plan)
- [Dialogue inside shots](#dialogue-inside-shots)
- [Examples](#examples)
- [Checks](#checks)

## Shots or stages

A clip that cuts is staged by **shot**: each shot is one camera setup with its
own size, angle, move and light. A clip that never cuts is staged by **stage**
(see [Scene staging](scene-action.md#scene-staging)): each stage is one state
change inside a continuous take, and the camera path is stated for the whole
take.

| Clip | Stage by | The camera fact lives |
|---|---|---|
| Several cuts, one scene | Shot | On every shot line |
| One continuous take | Stage | In the take's camera path, ordered by space and event |
| A held reaction or a static-by-design format | Single shot | In one stated hold with its reason recorded |

The six-part formula requires only Subject and Action to be valid. A narrative
shot is not finished at that minimum: its Camera and light source are craft
requirements, and a missing camera line leaves the model free to pick the
flattest default.

## Per-shot template

State the subjects, the scene and one grade once, then one line per shot.

```text
<Subjects with reference bindings and the shared scene, stated once.>
The visuals feature <one grade for the clip>.

Shot 1 (0-3 s): <size>, <angle>; <camera move with subject, start and end>.
<Subject> <body-part-level action for this beat>. Light: <source, key side
relative to the lens, quality>.
Shot 2 (3-6 s): <size>, <angle>; <camera move>. <Subject> <action>. Light:
<source, key side, quality>.
Shot 3 (6-10 s): <size>, <angle>; <static hold, or camera move>. <Subject>
<action>. Light: <source, key side, quality>.

Audio includes <dialogue, ambience, sound effects or music>.
```

Rules:

1. Open each shot line with the camera facts, then the action, then the light.
   Camera moves use the vocabulary in
   [Camera language](audio-performance-camera.md#camera-language).
2. One primary camera move per shot, plus at most one secondary move. The clip
   as a whole is limited by its shot count (about 7 shots at most, none shorter
   than about 0.8 s), not by a move count.
3. Name the scene's light sources once, then give each shot a source and a key
   side. A cut changes which side of a source the camera sees, or a stated event
   adds a source; it never introduces a source the scene did not declare.
4. Describe an action once, in the shot where it happens. Do not repeat it in the
   shared opening.
5. A cut resets relationships. Restate the invariants that matter in each shot:
   head count, screen direction, prop ownership and wardrobe. Bind each reference
   once in the opening and name the subject in the shot lines.
6. Time ranges are consecutive and non-overlapping and are a time budget, not
   frame-accurate cut points. Use bare ranges inside the shot line parentheses.
7. Keep generation parameters (duration, resolution, aspect ratio) out of the
   prompt.

## Carrying a shot plan

When a shot plan exists for the scene, copy each shot's size, angle, move and
light facts into its shot line without softening them. If the prompt cannot hold
a planned fact, report the conflict to the plan owner instead of dropping it. A
confirmed project axis appears in the shot lines or carries a scene override.
Storyboard grids and blockout images are planning aids; the plan's facts go in
the prompt text.

When no plan exists and the shot is not static by design, write the plan first
or return the prompt as a draft with the missing camera and light decisions
labelled. Do not pad the Camera slot with unrequested competing presets; fill it
from the plan or the user's request.

## Dialogue inside shots

Place a spoken line inside the shot that frames the speaker. Make the shot at
least spoken words / 2.2 + 1 s long: the late start of speech (observed 0.5-1.5 s
in this workspace's draft runs) needs the margin. Vary size and angle between
speakers, and keep moves slow while a line is spoken so the lips and eyes stay
readable. For Filipino or Taglish lines, compose with the dialogue partner skill
for the delivery direction.

## Examples

### Four-shot kitchen beat

```text
@Image 1 defines the mother, @Image 2 the visiting aunt and @Image 3 her
seven-year-old son; each appears once. @Image 4 defines the kitchen: window and
stove at screen-left when facing the front door, table at center-right, front
door at screen-right. The room has two light sources: low late-afternoon sun
through the window, and daylight from outside once the door opens.
The visuals feature a natural warm grade with soft contrast.

Shot 1 (0-3 s): wide shot, high angle; slow crane down from ceiling height to
table height, left to right. The mother crosses the kitchen to the front door.
Light: the window sun from camera-left, long soft shadows across the table.
Shot 2 (3-5.5 s): medium close-up, eye level; slow push-in on the door handle,
ending on the mother's hand as she opens the door inward. Light: the same window
sun from camera-left, her face half in shade.
Shot 3 (5.5-9 s): close-up, low angle; static hold on the son leaning out from
behind the aunt's near leg to tap the door frame once with his fingertips.
Light: contre-jour from the open door behind him, a warm halo on his hair, his
face kept readable by window fill.
Shot 4 (9-12 s): medium shot, eye level; slow drift right as the mother glances
once at the four-place table, turns back and smiles, the aunt answering with an
easy smile. Light: the window sun from camera-left with a warm rim from the open
door.

Audio includes a door latch, one light tap on wood and quiet kitchen ambience.
```

### One continuous take

```text
One-take shot with no cuts. The camera starts at a medium wide on the courier
at the street door while the doorman waves her in, tracks beside her through the
lobby at walking pace, and ends on a close-up of her hand pressing the lift
button. Light: street daylight at the door, cooler lobby fill at the end.
```

## Checks

Before submitting a cutting clip, confirm:

1. Every shot line carries size, angle, a move or a recorded static hold, and a
   light fact from a declared source, matching the shot plan.
2. The shot count and lengths fit the duration and the shot ceiling; a single shot
   across a long clip is a recorded one-take or hold choice.
3. Every spoken line fits inside its shot with the margin above.
4. No shot stacks competing moves.
