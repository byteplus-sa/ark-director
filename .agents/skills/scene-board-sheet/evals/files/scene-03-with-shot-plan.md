---
scene_id: scene-03
title: Test
---

# Scene 3

## Shot plan

```yaml
shot_plan:
  scene: scene-03
  status: draft
  energy: standard
  sources:
    - id: sun
      position: south-east
      switched_on_by: always on
      cues:
        - {at_s: 5.0, change: dim, trigger: a cloud, shot: s03_sh020_a}
  shots:
    - id: s03_sh010_a
      duration_s: 3.5
      job: establish
      size: wide
      angle: low
      framing: group
      featured: [mother, boy]
      move: slow push-in on the plaza
      lens_intent: deep focus
      light: {source: sun, key_side: camera-right, quality: hard}
    - id: s03_sh010_b
      duration_s: 2.0
      job: reveal
      size: medium
      angle: eye level
      move: static hold on the boy
      static_reason: contrast_hold
      light: {source: sun, key_side: camera-right}
    - id: s03_sh020_a
      duration_s: 4.0
      turn: true
      job: escalate
      size: close-up
      angle: low
      move: static hold
      static_reason: performance_hold
      dialogue: "Noon today, Mr. Alder."
      light: {source: sun, key_side: behind}
    - id: s03_sh030_a
      duration_s: 3.0
      job: hold
      size: medium
      angle: eye level
      move: static hold
      static_reason: contrast_hold
      blocking_change: true
      light: {source: sun, key_side: camera-left}
```

## Notes

nothing
