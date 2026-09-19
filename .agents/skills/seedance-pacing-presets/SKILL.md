---
name: seedance-pacing-presets
description: >
  Turn a named pacing or rhythm preset — speed ramp, slow motion, slow-mo,
  bullet time, ramp up, flash in/out, impact moment, montage, montage pacing,
  cut rhythm, timing, or speed up — into a canonical, timestamped motion,
  cut, and pacing block for the Seedance 2.5 prompt. Use when the user asks
  to direct a scene's rhythm, tempo, or editing energy rather than only its
  content. Bullet time here is the freeze/slow-mo speed ramp; the camera-orbit
  technique belongs to seedance-camera-presets. Single Shot here is no-cuts
  pacing; the one-take pass-through camera path belongs to seedance-camera-presets.
---

# Seedance Pacing Presets

This skill maps a named pacing or rhythm preset into a timestamped
**motion / cut / pacing block** for the Seedance 2.5 prompt, so the scene's
rhythm — not just its content — is directed. It is a **prompt-composition-only**
skill: it never calls MCP tools or the Ark API, and it never runs generation.
The base prompt grammar — the six-part formula, `At Ns` timestamp syntax, the
bounce-speed-ramp technique contract, the audio bracket syntax `()<>{}【】`,
and scene-staging rules — is defined in `seedance-prompt-25` and is **not
redefined here**. Compose with `seedance-prompt-25` for the full prompt contract;
this skill only adds the pacing preset bank on top.

The output of this skill is always a **pacing block** — a timestamped
description of where motion speeds up, slows down, lands on a beat, or cuts —
ready to be inserted into the Action / Camera / Audio slots of a Seedance 2.5
prompt, or into the timestamped lines of a staged prompt.

**Core constraint:** timestamps are a **time budget, not frame-accurate**.
Pacing is *directed*, not guaranteed frame-by-frame. An action may land
slightly before or after the stated boundary, so write beats with margin and
never promise exact frame sync.

## Source authority

The preset bank is built from the official Seedance 2.5 timestamp and
speed-ramp grammar. All sources accessed 2026-08-13:

- [Seedance 2.5 Prompt Guide (Lark)](https://bytedance.larkoffice.com/docx/A88jd0B47oAd8zxWp5ycZFMfnxh) — official timestamp syntax (`At Ns`, `0-3 seconds...`) and the bounce-speed-ramp technique
- [BytePlus ModelArk prompt guide](https://docs.byteplus.com/en/docs/ModelArk/2607689) — official prompt guidance
- [Seedance 2.5 launch blog](https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5) — official announcement

**The base grammar is defined in `seedance-prompt-25`.** This skill adds the
pacing preset bank and block-composition rules; it does not restate or replace
the six-part formula, timestamp rules, reference-role syntax, or audio syntax
from that skill.

## Preset bank

Choose exactly **one** speed ramp (or "auto") and, for multi-shot scenes, one
montage pacing. Do not stack multiple speed ramps in one block; combine a
single ramp with a single pacing for montages.

### Speed ramps

Each row gives the intent and a canonical timestamped phrase template that
satisfies the official bounce-speed-ramp contract: name **where** action
accelerates, decelerates, or rebounds, and the **final resting state**.

| Ramp | Intent | Canonical phrase template |
|---|---|---|
| Linear | Constant speed, no emphasis | `<Subject> moves at a constant, even speed throughout the clip.` |
| Auto | Model-inferred pacing | `Use natural pacing: accelerate or slow where the action itself demands it.` |
| Slow Motion | Everything moves in deliberate slow-motion detail | `At <N>s, the action drops into slow motion; <subject> moves in deliberate slow-motion detail until <end state>.` |
| Bullet Time | Action freezes into slow motion while the camera orbits | `Bullet time: at <N>s, <action> freezes into slow motion; <subject> stays near-frozen in detail until <end state>. The camera orbit direction belongs to seedance-camera-presets.` |
| Flash In | Fast acceleration into a beat | `At <N>s, the action snaps forward into fast motion, accelerating into <beat>; the frame lands hard on <beat>.` |
| Flash Out | Fast deceleration out of a beat | `At <N>s, <beat> plays at full speed, then the action drops sharply and decelerates out into <end state>.` |
| Impact | Hard hit / staccato on a beat | `At <N>s, <action> hits in a single sharp impact beat — <detail> — then the frame holds for half a beat.` |
| Ramp Up | Gradual acceleration | `From <start time> to <N>s, the motion gradually speeds up, building tension until <N>s when <climax action> bursts forward.` |
| Ramp Down | Gradual deceleration | `At <N>s, the motion gradually slows from full speed, easing into <end state> by <end time>s with no abrupt stop.` |

### Montage pacing

For multi-shot scenes, pick one cut rhythm. Each row gives the intent and a
canonical block describing the cut rhythm. Montage requires a shot list — see
Edge cases.

| Pacing | Intent | Canonical block template |
|---|---|---|
| Chaotic | Fast, hard cuts; high-energy sequence | `Cut fast and hard: rapid-fire shots of <A>, <B>, <C>, and <D>, each under a second or two, strobing between them with jagged, high-energy rhythm.` |
| Dynamic | Rhythmic medium cuts; momentum | `Cut on the beat: quick medium shots alternating between <A> and <B>, each 2-3 seconds, building momentum toward <climax>.` |
| Calm | Slow, even pacing; held shots | `Cut slowly and evenly: hold each of <A>, <B>, and <C> for several seconds with gentle, unhurried transitions and no jump cuts.` |
| Single Shot | No cuts; one continuous take | `No cuts: one continuous, unbroken shot that follows <subject> through <spaces and events in order> at an even pace from start to finish.` |

## Parameter schema

Fill these knobs when composing a pacing block. Only `ramp` or `pacing` is
required; everything else is optional.

| Parameter | Meaning | Rules |
|---|---|---|
| `ramp` | Speed ramp from the bank | Required unless `pacing` is set. Pick exactly one: Linear, Auto, Slow Motion, Bullet Time, Flash In, Flash Out, Impact, Ramp Up, Ramp Down. |
| `pacing` | Montage cut rhythm from the bank | Required for multi-shot scenes; one per prompt: Chaotic, Dynamic, Calm, Single Shot. |
| `beat` | What lands on the beat (optional) | The action, moment, or object that must land at the timestamp. Name it explicitly so the model can place it. |
| `duration` | Total clip length in seconds | Right-size to the scene's natural length, **4-30s** for 2.5. Do not pad to 30s. Pass to the generation interface, not the prompt. |
| `cut_list` | Optional ordered shot timings | List of `N-M seconds: <shot description>` entries. Time ranges must be consecutive and non-overlapping. |
| `audio_sync` | Align cuts to a Seed Audio master timeline | bool. When true, cut on the audio beats; with dialogue, generate Seed Audio first and align pacing to its actual timing (audio-first contract). |
| `scene_type` | Single continuous take vs multi-shot montage | `single` for one unbroken shot (no cuts), `montage` for multiple cuts. Drives whether a `pacing` choice is required. |

## Output grammar

The pacing block composes with the `seedance-prompt-25` six-part formula and
scene staging. Insert the ramp/pacing phrasing as timestamped lines in the
Action or Camera description, and use the audio bracket syntax for any beat
audio.

**Pacing-block template:**

```
At <N>s, <ramp behavior with subject, beat, and end state>.
[Shot <N> (<start>-<end>s): <cut content>.]  (only when cut_list is set)
Audio: <(music)> <{dialogue}> <sfx>, cut <on / against> the beat.
```

Timestamp syntax follows `seedance-prompt-25`: **exact moments use `At N
seconds`, time ranges are written bare** (e.g. `5-9 seconds, ...`). Do not
write `At 5-9 seconds` — that hybrid form is not in the canonical grammar.

**Worked example — short action scene with a slow-mo impact beat and a
flash-out ending:**

```
@Image 1 defines Maya's appearance, hairstyle, and clothing. Do not use the background of the image.
Maya sprints down the rain-slick alley at night and slams a delivery crate against the wall to stop a pursuer.
The visuals feature a cold, desaturated grade with neon rim light.
Use a handheld follow shot at full speed, then a tight static close-up on the impact.
At 4 seconds, Maya's impact hits in a single sharp impact beat — the crate smacks the wall, dust bursts — then the frame holds for half a beat.
5-9 seconds, the action drops into slow motion; debris floats in deliberate slow-motion detail while Maya straightens up until the dust settles.
9-12 seconds, the motion flashes out: the camera whips back to a wide shot and the action decelerates sharply into stillness.
Audio: <the crate smacks hard against the wall> on the impact, then the alley falls quiet except for rain.
```

This block names the ramp (Impact, then Slow Motion, then Flash Out), names the
beat that lands (the crate impact), gives each ramp a timestamp and an end
state, and stays within a natural 12-second duration. It composes with
`seedance-prompt-25` scene staging for multi-stage scenes, with
`seedance-camera-presets` for the camera treatment, and with
`film-production` / `seedream-storyboard` when the scene needs an approved shot
list before generation.

## Edge cases and guardrails

- **Timestamps are a time budget, not frame-accurate.** Never promise exact
  frame sync, and never demand impossible frequencies (e.g. "complete three
  actions in one second"). Write beats with margin and verify in review.
- **Keep 1-2 camera moves per clip.** Pacing blocks describe timing, not camera
  gymnastics. Compose the camera treatment with `seedance-camera-presets` and
  keep simultaneous moves to at most two per clip.
- **Pacing needs a shot list.** When the scene has multiple cuts, prefer
  `seedream-storyboard` / `film-production` for the shot list rather than one
  raw prompt. A montage without an ordered cut list lets the model cut or
  reorder arbitrarily.
- **30s single-pass or native extension only for continuous seamless motion.**
  Reserve them for a genuine single continuous take or audio-driven long
  dialogue where seamless motion across scene boundaries matters more than
  per-scene iteration. Otherwise right-size each scene to its natural
  duration.
- **Per-scene natural duration 4-30s — do not pad.** Set `duration` to the
  length the scene actually needs (7s for a single beat, 12s for a short
  dialogue exchange, 20s for a multi-stage action). 30s is the ceiling, not the
  target.
- **Dialogue scenes: align pacing to audio.** When dialogue exists with
  `generate_audio: true`, the pacing timestamps should align to the spoken
  beats. For lip-sync-critical scenes, optionally compose with
  `seed-audio-prompt` to generate the Seed Audio track first, then align pacing
  timestamps to the actual audio timing.
- **Generation parameters stay in the API.** Duration, resolution, aspect
  ratio, and watermark never go in the prompt. Keep `watermark: false` by
  default.
- **One ramp, one pacing.** Do not stack multiple speed ramps or montage
  pacings in the same block; if the scene changes rhythm several times, split it
  into stages or separate takes.

## Self-check checklist

Before a pacing block is submitted as part of a Seedance 2.5 prompt, verify:

1. Pacing uses timestamped phrasing (`At <N>s`, `<start>-<end>s`), not vague
   "later" or "then" timing.
2. `ramp` or `pacing` comes from the preset bank.
3. The pacing block names the beat that lands (subject, action, and end state).
4. No frame-accurate or impossible-frequency promises are made.
5. Dialogue scenes align pacing to spoken beats; lip-sync-critical scenes pair
   with `seed-audio-prompt`.
6. `duration` is within 4-30s and not padded to fill 30s.
7. Any cut list uses consecutive, non-overlapping time ranges with ordered shot
   content.
8. Generation parameters (duration, resolution, aspect ratio) are absent from
   the prompt text.

A pacing block that passes all eight checks is ready to be composed into the
full prompt by `seedance-prompt-25`.
