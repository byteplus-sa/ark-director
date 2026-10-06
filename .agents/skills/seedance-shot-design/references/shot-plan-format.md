# Shot plan format

Focused reference for `seedance-shot-design`. Read [the entrypoint](../SKILL.md)
for the procedure and the variety rules.

- [Where the plan lives](#where-the-plan-lives)
- [The plan record](#the-plan-record)
- [Per-shot block for a cutting clip](#per-shot-block-for-a-cutting-clip)
- [One-take variant](#one-take-variant)
- [Carrying the plan into the prompt](#carrying-the-plan-into-the-prompt)

## Where the plan lives

Store the plan with the scene so the prompt author, the reviewer and the
production canvas read the same facts.

| Location | Contents |
| --- | --- |
| `scene.md` `## Shot plan` | The `shot_plan` record and the summary table for the scene |
| `shot.md` | The slice of the plan that this clip's prompt carries, beside the prompt snapshot |
| `project.md` `directorial_axes` | The project-wide camera, lens, lighting and pacing stance the plan must carry |

In chat-only or prompt-only work, return the table and the per-shot blocks
without creating files. When project files are in scope, add the scene plan file
to the `scene-breakdown` stage sources so a changed plan fails the freshness
check.

## The plan record

```yaml
shot_plan:
  scene: scene-02
  energy: standard
  light_story: late-afternoon window light from screen-left; the lamp on the
    table pays off at the turn
  axis_carry: project camera axis (low, object-eye-level) appears in shots a and c
  shots:
    - id: s02_sh010_a
      job: establish
      size: wide
      angle: high
      move: slow crane down from kitchen-ceiling height to table height, left to right
      lens_intent: deep focus; table and doorway both sharp
      light: low sun through the window screen-left, long soft shadows across the table
      contrast_with_previous: n/a
    - id: s02_sh010_b
      job: reveal
      size: medium close-up
      angle: eye level
      move: slow push-in on the door handle, ending on the hand
      lens_intent: shallow depth of field; hand sharp, doorway soft
      light: window light now falls across the hand from screen-left, face half in shade
      contrast_with_previous: size and move change; light direction shifts to a side cross
    - id: s02_sh010_c
      job: emphasize
      size: close-up
      angle: low
      move: static hold, no movement
      static_reason: contrast_hold
      lens_intent: the face sharp against a soft window
      light: contre-jour from the window behind, warm halo on the hair
      contrast_with_previous: angle and light direction change; the move stops
```

Field rules:

| Field | Rule |
| --- | --- |
| `job` | One of establish, reveal, emphasize, connect, escalate, hold |
| `size` | Extreme wide, wide, medium, medium close-up, close-up, extreme close-up, or insert |
| `angle` | Eye level, low, high, overhead, first-person, or over-the-shoulder |
| `move` | The primary move with subject, start and end, or `static hold` |
| `static_reason` | Required with a static hold or a locked light; a value from the entrypoint table |
| `lens_intent` | A visible result (sharp plane, soft background, compression), never a number alone |
| `light` | Source, direction relative to the lens, quality, contrast |
| `contrast_with_previous` | Which of size, angle, move and light direction change; `n/a` for the first shot |
| `axis_carry` | Plan-level note naming where each recorded project camera, lens, lighting or pacing axis appears, or the scene override and its reason |

A plan that records `energy`, a `light_story`, and a `contrast_with_previous`
for every shot after the first is complete enough for review.

## Per-shot block for a cutting clip

A clip that cuts uses one shared opening (subject, scene, grade), then one line
per shot. Time ranges are consecutive and non-overlapping, and they are a time
budget rather than frame-accurate edit points. The `Shot N (a-b s):` line is the
documented Seedance 2.0 convention, carried into 2.5 prompts in this workspace.

```text
<Subjects and the shared scene, with reference bindings, stated once.>
The visuals feature <one grade for the whole clip>.

Shot 1 (0-4 s): <size>, <angle>; <move with subject, start and end>. <Subject>
<body-part-level action for this beat>. Light: <source, direction, quality>.
<Lens result when it matters.>
Shot 2 (4-8 s): <size>, <angle>; <move>. <Subject> <action>. Light: <source,
direction, quality>.
Shot 3 (8-12 s): <size>, <angle>; <move or "static hold">. <Subject> <action>.
Light: <source, direction, quality>.

Audio includes <dialogue, ambience, sound effects or music>.
```

Rules for the block:

1. Each shot line opens with the camera facts, then the action, then light. A
   cut resets relationships, so restate the invariants that matter: head count,
   screen direction and prop ownership.
2. Describe the same action once, in the shot where it happens.
3. Keep one grade per clip. Light direction changes shot to shot; the source
   and the room stay consistent.
4. A dialogue line belongs inside the shot that frames the speaker. Check that
   the shot is long enough for the line at about 2.2 spoken words per second.
5. Resolve each named move through the camera preset wording when the move is
   unusual; state which subject the camera follows and where it ends.

## One-take variant

When the plan chooses one continuous take, the clip has one shot and the camera
passes through ordered spaces and events. Record why in the plan (`job` per
stage, `static_reason` absent because the camera moves).

```text
One-take shot with no cuts. The camera starts <size> on <subject or space A>
while <event A>, moves <direction> to <size> on <subject or space B> while
<event B>, then ends <size> on <subject or space C> as <event C>.
Light: <source and direction at the start>, shifting as the camera passes
<space B> to <source and direction at the end>.
```

Variety rules V3, V4 and V5 still apply inside a take: a motivated move, a named
light at each stage, and a distinct payoff at the end.

## Carrying the plan into the prompt

The prompt author copies each shot's camera and light facts verbatim from the
plan. If the prompt cannot hold a fact, the author reports the conflict to the
plan owner instead of dropping it silently. A reviewer compares the plan to the
prompt, and the take review compares the plan to the footage.
