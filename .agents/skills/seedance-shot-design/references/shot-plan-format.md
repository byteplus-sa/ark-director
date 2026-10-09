# Shot plan format

Focused reference for `seedance-shot-design`. Read [the entrypoint](../SKILL.md)
for the procedure and the variety rules.

- [Where the plan lives](#where-the-plan-lives)
- [The plan record](#the-plan-record)
- [Field rules](#field-rules)
- [Carrying the plan into the prompt](#carrying-the-plan-into-the-prompt)

## Where the plan lives

Store the plan with the scene so the prompt author, the reviewer and the
reviewer (pre-Studio canvas: the production canvas) read the same facts.

| Location | Contents |
| --- | --- |
| `scene.md` `## Shot plan` | The `shot_plan` record for the scene |
| `shot.md` | The slice of the plan that this clip's prompt carries, beside the prompt snapshot |
| `project.md` `directorial_axes` or `locked` | The confirmed project-wide camera, lens, lighting and pacing stance the plan must carry |

In chat-only or prompt-only work, return the record without creating files. When
project files are in scope, save the plan in the scene file; Studio's `status`
does not read scene files, so reopen `scene-breakdown` and re-run prompt-review
when the plan changes (pre-Studio canvas: add the scene file to the
`scene-breakdown` stage sources so a changed plan fails the freshness check).
Mark the plan `draft` until
the scene's locations are approved, then revalidate it before shot generation.

## The plan record

The example is a 12-second family-drama kitchen scene at standard energy.

```yaml
shot_plan:
  scene: scene-02
  status: draft
  energy: standard
  axis_carry: confirmed project axes (low camera for the child, slow motivated
    moves) appear in shots c (low angle) and a, b, d (slow moves)
  sources:
    - id: window
      position: kitchen window on the left wall, screen-left when the camera
        faces the front door; low late-afternoon sun
      switched_on_by: always on
    - id: door
      position: front door at screen-right; daylight from outside
      switched_on_by: the door opens at about 5 s
  shots:
    - id: s02_sh010_a
      duration_s: 3.0
      job: establish
      size: wide
      angle: high
      angle_reason: show the whole room and where each person will stand
      move: slow crane down from ceiling height to table height, left to right
      move_reason: lowers the viewer into the room as the mother crosses it
      lens_intent: deep focus; table and doorway both sharp
      light: {source: window, key_side: camera-left, quality: low sun, long soft shadows across the table}
      contrast_with_previous: n/a
    - id: s02_sh010_b
      duration_s: 2.5
      job: reveal
      size: medium close-up
      angle: eye level
      move: slow push-in on the door handle, ending on her hand as the door opens
      move_reason: moves the viewer to the point of contact
      lens_intent: shallow depth of field; hand sharp, doorway soft
      light: {source: window, key_side: camera-left, quality: same sun, her face half in shade}
      contrast_with_previous: size family, angle class and move change; the light is unchanged on purpose
    - id: s02_sh010_c
      duration_s: 3.5
      turn: true
      job: emphasize
      size: close-up
      angle: low
      angle_reason: the boy's sudden appearance at adult hip height gets presence
      move: static hold, no movement
      static_reason: contrast_hold
      lens_intent: the boy's face sharp against a soft doorway
      light: {source: door, key_side: behind the subject, quality: contre-jour halo on his hair with the face kept readable by window fill}
      contrast_with_previous: size family, angle class, move and key side all change
    - id: s02_sh010_d
      duration_s: 3.0
      job: release
      size: medium
      angle: eye level
      move: slow drift right, ending on her smile
      move_reason: releases the tension by sliding to the mother's reaction
      lens_intent: natural depth, mother sharp
      light: {source: window, key_side: camera-left, quality: soft sun with a warm rim from the open door}
      contrast_with_previous: size family, angle class and move change
```

## Field rules

| Field | Rule |
| --- | --- |
| `status` | `draft` until the scene's locations are approved, then `ready` after revalidation |
| `energy` | restrained, standard or kinetic |
| `axis_carry` | Where each confirmed project axis appears (camera, lens, lighting, pacing, energy), or the scene override and its reason |
| `sources` | Every light source the scene uses, with a fixed world position and the event that switches it on |
| `duration_s` | Shot length in seconds; lengths are uneven and the turn differs from its neighbors |
| `turn` | `true` on exactly one shot |
| `job` | One of establish, reveal, emphasize, connect, escalate, hold, release |
| `size` | Extreme wide, wide, medium, medium close-up, close-up, extreme close-up or insert |
| `angle` | Eye level, over-the-shoulder, low, high, overhead or first-person |
| `angle_reason` | Required for any angle other than eye level |
| `move` | The primary move with subject, start and end, or `static hold` |
| `move_reason` | What the move reveals or emphasizes |
| `static_reason` | Required with a static hold; a value from the entrypoint table |
| `lens_intent` | A visible result (sharp plane, soft background, compression), never a number alone |
| `light` | A declared `source`, the `key_side` relative to the lens, and the quality and contrast |
| `contrast_with_previous` | Which of size family, angle class, move and key side change; `n/a` for the first shot |

A plan with `energy`, `sources`, a `turn`, uneven `duration_s` values and a
`contrast_with_previous` for every shot after the first is complete enough for
review.

## Carrying the plan into the prompt

The prompt author copies each shot's camera and light facts into the shot line
without softening them. The per-shot prompt block, the one-take variant and the
dialogue timing rules belong to the Seedance 2.5 prompt skill's shot-staging
reference. If the prompt cannot hold a planned fact, the author reports the
conflict to the plan owner instead of dropping it. A reviewer compares the plan
to the prompt, and the take review compares the plan to the footage.
