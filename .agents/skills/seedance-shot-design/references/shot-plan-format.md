# Shot plan format

Focused reference for `seedance-shot-design`. Read [the entrypoint](../SKILL.md)
for the procedure and the variety rules.

- [Where the plan lives](#where-the-plan-lives)
- [The plan record](#the-plan-record)
- [Field rules](#field-rules)
- [Sequences in a long spot](#sequences-in-a-long-spot)
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
      framing: three-shot
      featured: [mother, aunt, boy]
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
      framing: single
      featured: [mother]
      angle: eye level
      move: slow push-in on the door handle, ending on her hand as the door opens
      move_reason: moves the viewer to the point of contact
      lens_intent: shallow depth of field; hand sharp, doorway soft
      depth_layers: {foreground: the door's edge, subject: her hand on the handle, background: the hall beyond the doorway}
      light: {source: window, key_side: camera-left, quality: same sun, her face half in shade}
      contrast_with_previous: size family, angle class and move change; the light is unchanged on purpose
    - id: s02_sh010_c
      duration_s: 3.5
      turn: true
      job: emphasize
      size: close-up
      framing: single
      featured: [boy]
      angle: low
      angle_reason: the boy's sudden appearance at adult hip height gets presence
      move: static hold, no movement
      static_reason: contrast_hold
      lens_intent: the boy's face sharp against a soft doorway
      wow: true
      light: {source: door, key_side: behind the subject, quality: contre-jour halo on his hair with the face kept readable by window fill}
      contrast_with_previous: size family, angle class, move and key side all change
    - id: s02_sh010_d
      duration_s: 3.0
      job: release
      size: medium
      framing: two-shot
      featured: [mother, boy]
      angle: eye level
      move: slow drift right, ending on her smile with the boy at her side
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
| `cues` | Optional, per source. Each cue has `at_s` (scene time), `change` (`on`, `off`, `dim` or `flicker`), `trigger` (the visible or story event) and, when it lands inside a shot, that shot's `id`. A shot's `light` describes the state at its start and names any cue inside it |
| `duration_s` | Shot length in seconds from performance and delivery needs; even or held timing is valid with a rationale |
| `turn` | `true` on the intended turn when the scene has one; omit for sustained or observational scenes without a turn |
| `job` | One of establish, reveal, emphasize, connect, escalate, hold, release |
| `size` | Extreme wide, wide, medium, medium close-up, close-up, extreme close-up or insert |
| `framing` | Single, dirty single, two-shot, three-shot, group, over-the-shoulder, over-the-hip, point of view or insert, per [framing](framing.md). Required in a scene with two or more characters |
| `featured` | The subjects the shot is about, with screen sides when it matters; empty for an insert or an unpeopled point of view |
| `composition` | Optional. Balanced or deliberately unbalanced (isolation, tension), with the reason when unbalanced |
| `angle` | Eye level, over-the-shoulder, low, high, overhead or first-person. A dirty single, over-the-shoulder or over-the-hip framing records over-the-shoulder, and a point-of-view framing records first-person |
| `angle_reason` | Required for any angle other than eye level |
| `move` | The primary move with subject, start and end, or `static hold` |
| `move_reason` | What the move reveals or emphasizes |
| `static_reason` | Required with a static hold; a value from the entrypoint table |
| `lens_intent` | A visible result (sharp plane, soft background, compression), never a number alone. A focus pull away from a face is marked `post` rather than prompted |
| `depth_layers` | Recommended at standard and kinetic energy. A named foreground, the subject and a named background, each a visible thing in the declared location |
| `wow` | Optional marker for a memorable image when useful; no count is required and sequence effectiveness matters more than a still |
| `light` | A declared `source`, the `key_side` relative to the lens, and the quality and contrast |
| `contrast_with_previous` | Which choices change or deliberately repeat and why; `n/a` for the first shot. No minimum contrast count |
| `blocking_change`, `axis_crossed`, `state_change`, `sub_beats` | Optional. Facts the scene board reads to mark a shot key and to pick its panel states: `blocking_change: true` when positions change inside the shot, `axis_crossed: true` when the 180 degree axis is crossed or restated, `state_change` as a list of prop, wardrobe or location changes, and `sub_beats` as the named beats an L3 board draws |
| `transition_in`, `dialogue`, `sound_cue`, `screen_direction`, `continuity_carry`, `elements` | Optional. Copied onto the scene board's annotation strip and panel prompts; leave them out when the shot has nothing to say |

A cue that lands inside a shot is written once on the source and named on the
shot's `light` line:

```yaml
sources:
  - id: corridor-lamps
    position: ceiling lamps along both sides of the corridor, behind the subject
    switched_on_by: always on
    cues:
      - {at_s: 6.5, change: off, trigger: a power cut, shot: s01_sh030}
shots:
  - id: s01_sh030
    light: {source: corridor-lamps, key_side: behind the subject, quality: dim rim
      that goes out at about 2 s into the shot, leaving his face just above black}
```

The lighting preset skill words the cue for the prompt. The plan's job is to
give every cue a time, a change and a trigger; an untimed "partway through" switch lands
at an unplanned moment.

A plan with `energy`, `sources`, performance-led `duration_s` values and
`contrast_with_previous` for every shot after the first is complete enough for
review. Record the rationale for sustained holds or repetition, and relevant
performance/exchange beat IDs and critical readability needs in shot notes.
A `turn` marker may identify an approved change; no marker count or new turn
is required. A turn does not require different timing, camera or light.

## Sequences in a long spot

A spot using the optional sequence pattern can record sequences above its
shots. This hypothetical grouping is not a required cadence or shot count:

```yaml
sequences:
  - id: seq-01
    clip: s01_sh010
    duration_s: 5.0
    job: hook
    shots: [s01_sh010_a, s01_sh010_b]
    wow: s01_sh010_b
  - id: seq-02
    clip: s01_sh020
    duration_s: 4.5
    job: escalate
    shots: [s01_sh020_a, s01_sh020_b, s01_sh020_c]
    wow: s01_sh020_c
```

Derive sequence lengths and shot counts from action, attention and readability.
Equal durations and repeated holds remain valid; `wow` markers are optional.
Generation boundaries need not become editorial cuts. Record intended joins
in assembly, preserving critical responses when trimming a held frame.

## Carrying the plan into the prompt

The prompt author copies each shot's camera and light facts into the shot line
without softening them. The per-shot prompt block, the one-take variant and the
dialogue timing rules belong to the Seedance 2.5 prompt skill's shot-staging
reference. If the prompt cannot hold a planned fact, the author reports the
conflict to the plan owner instead of dropping it. A reviewer compares the plan
to the prompt, and the take review compares the plan to the footage.
