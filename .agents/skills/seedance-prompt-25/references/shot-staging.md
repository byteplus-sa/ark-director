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
change inside a continuous take, and the camera path is stated once for the whole
take.

| Clip | Stage by | The camera fact lives |
|---|---|---|
| Several cuts, one scene | Shot | On every shot line |
| One continuous take | Stage | In the take's camera path, ordered by space and event |
| A held reaction or a static-by-design format | Single shot | In one stated hold with its reason recorded in the plan |

The six-part formula requires only Subject and Action to be valid. A narrative
shot is not finished at that minimum: its Camera and Visual Style (light source)
are craft requirements, and a missing camera line leaves the model free to pick
the flattest default.

## Per-shot template

State the subjects, the scene and one grade once, then one line per shot.

```text
<Subjects with reference bindings and the shared scene, stated once.>
The visuals feature <one grade for the clip>.

Shot 1 (0-4 s): <size>, <angle>; <camera move with subject, start and end>.
<Subject> <body-part-level action for this beat>. Light: <source, direction
relative to the lens, quality>.
Shot 2 (4-8 s): <size>, <angle>; <camera move>. <Subject> <action>. Light:
<source, direction, quality>.
Shot 3 (8-12 s): <size>, <angle>; <static hold, or camera move>. <Subject>
<action>. Light: <source, direction, quality>.

Audio includes <dialogue, ambience, sound effects or music>.
```

Rules:

1. Open each shot line with the camera facts, then the action, then the light.
   Camera moves use the vocabulary in
   [Camera language](audio-performance-camera.md#camera-language).
2. One primary camera move per shot, plus at most one secondary move. There is no
   cap per clip; the cap is per shot, because each cut starts a new setup.
3. Name one light source for the scene and describe how each shot sees it. A cut
   changes the side or angle of the light, not the world's source.
4. Describe an action once, in the shot where it happens. Do not repeat it in the
   shared opening.
5. A cut resets relationships. Restate the invariants that matter in each shot:
   head count, screen direction, prop ownership and wardrobe.
6. Time ranges are consecutive and non-overlapping and are a time budget, not
   frame-accurate cut points. Use bare ranges inside the shot line parentheses.
7. Keep generation parameters (duration, resolution, aspect ratio) out of the
   prompt.

## Carrying a shot plan

When a shot plan exists for the scene, copy each shot's size, angle, move and
light facts into its shot line without softening them. If the prompt cannot hold
a planned fact, report the conflict to the plan owner instead of dropping it. A
recorded project axis appears in the shot lines or carries a scene override.

When no plan exists and the shot is not static by design, write the plan first
or return the prompt as a draft with the missing camera and light decisions
labelled. Do not pad the Camera slot with unrequested competing presets; fill it
from the plan or the user's request.

## Dialogue inside shots

Place a spoken line inside the shot that frames the speaker. Estimate the line at
about 2.2 spoken words per second and make sure the shot is long enough for it,
plus the late start of speech. Vary size and angle between speakers, and keep
moves slow while a line is spoken so the lips and eyes stay readable. For
Filipino or Taglish lines, compose with the dialogue partner skill for the
delivery direction.

## Examples

### Three-shot kitchen beat

```text
@Image 1 defines the mother and @Image 2 defines the boy; each appears once.
The kitchen has a table at center and a front door at screen-right.
The visuals feature a natural warm grade with soft contrast.

Shot 1 (0-4 s): wide shot, high angle; slow crane down from ceiling height to
table height, left to right. The mother crosses to the door. Light: low
late-afternoon sun through the window at screen-left, long soft shadows across
the table.
Shot 2 (4-8 s): medium close-up, eye level; slow push-in on the door handle,
ending on her hand as she opens it. Light: the same window now cross-lights her
hand, her face half in shade.
Shot 3 (8-12 s): close-up, low angle; static hold on the boy leaning out from
behind the aunt to tap the frame. Light: contre-jour from the open door, a warm
halo on his hair.

Audio includes door latch, one light tap on wood, and quiet kitchen ambience.
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
   light fact.
2. Adjacent shots differ in at least two of size, angle, move and light
   direction, or the plan records why not.
3. The shot count fits the duration; a single shot across a long clip is a
   recorded one-take or hold choice.
4. Every spoken line fits inside its shot.
5. No shot stacks competing moves.
