---
name: seedance-pacing-presets
description: >
  Turn a named pacing or rhythm preset — speed ramp, slow motion, slow-mo,
  bullet time, ramp up, flash in/out, impact moment, montage, montage pacing,
  cut rhythm, time-lapse, freeze frame, progressive or partial change (an
  outfit or material changing part by part), named cuts or transitions,
  timing, or speed up — into a canonical, timestamped motion,
  cut, and pacing block for the Seedance 2.5 prompt. Use when the user or a
  shot plan asks to direct a scene's rhythm, tempo, or editing energy rather
  than only its content. Bullet time here is the freeze/slow-mo speed ramp; the camera-orbit
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
never promise exact frame sync. Some timed events land closely (a light cue, a
staged body-part progression), while cuts inside one clip may merge or drop.
About 0.8 s is a provisional planning caution, not a provider limit or a
guaranteed failure threshold. Preserve requested timing; offer assembly as an
optional remedy for precision or demonstrated failure, and return real conflicts
with locked timing or a one-prompt requirement rather than silently retiming.

## Source authority

The preset bank is built from the official Seedance 2.5 timestamp and
speed-ramp grammar. All sources accessed 2026-08-13:

- [BytePlus ModelArk prompt guide](https://docs.byteplus.com/en/docs/ModelArk/2607689) — official prompt guidance, timestamp syntax (`At Ns`, `0-3 seconds...`) and the bounce-speed-ramp technique
- [Seedance 2.5 launch blog](https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5) — official announcement

**The base grammar is defined in `seedance-prompt-25`.** This skill adds the
pacing preset bank and block-composition rules; it does not restate or replace
the six-part formula, timestamp rules, reference-role syntax, or audio syntax
from that skill.

## Preset bank

When a speed ramp is requested, choose exactly **one** ramp per stage (or
"auto") and, for multi-shot scenes, one montage pacing. Time treatments and
named boundaries can be requested without adding a speed ramp. Do not stack
multiple speed ramps in one block; combine a single ramp with a single pacing
for montages.

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

### Time treatments

These are prompt-authoring heuristics, not additional provider parameters or
claims of verified model support. Choose one time treatment per stage instead
of stacking it with a conflicting speed ramp.

| Treatment | What to specify | Canonical phrase template |
|---|---|---|
| Time-lapse / timelapse | Compressed event, visible progression, framing, end state | `From <start>s to <end>s, show a time-lapse of <event>: <visible changes> progress rapidly from <initial state> to <final state>, with <subject or landmark> consistently framed.` |
| Freeze frame | Exact visible pose, hold window, resume or cut | `At <N>s, freeze the entire picture on <subject's visible pose>; hold that same still image until <M>s, then <resume the action / cut to the next shot>.` |
| Progressive change | The part that changes first, timed stages by body part or region at the requested speed, unbroken motion | See [Progressive change](#progressive-change) |

A freeze frame holds the entire picture, including camera and background.
Bullet time instead allows camera motion around near-frozen action. Time-lapse
must show an event progressing through time; a fast camera move alone is not
time-lapse. A long real-world interval is story content; output duration remains
a generation parameter outside the prompt.

### Progressive change

Use when something changes part by part rather than all at once: an outfit
that changes only on the part of the body that has crossed a line (a pole, a
doorway, a shadow edge), a surface that freezes or rusts from one end, a
material that spreads across an object. This section is the one home for the
technique; other skills point here.

1. Preserve requested timing, speed and stride. A crossing of about 1.5 s with
   stages about 0.4 s apart is a provisional example: these are not provider
   limits. Slowing or spreading stages is an optional readability remedy, not
   permission to retime a locked crossing.
2. Write stages by timestamp and body part or region within the supplied
   window: the leading edge first, intermediate regions as needed, then fully
   changed. Stage count and intervals follow the action, not a fixed schedule.
3. Keep the motion and the place continuous, and rule out transition effects
   that the model otherwise adds.

```
At <T1>s, <subject>'s <leading hand and leading foot> have crossed <the line> and already show <new state>; the rest is still <old state>.
At <T2>s, the front quarter of <subject>, past <the line>, shows <new state>.
At <T3>s, about half of <subject> shows <new state>, <the line> passing through <the torso / the middle>.
At <T4>s, only <subject>'s rear quarter is still <old state>.
At <T5>s, <subject> fully shows <new state>.
The change appears only on the parts that have crossed <the line>; there is no glow, flash, sparkle, dissolve or particle effect. <Subject>'s position, stride and direction continue unbroken.
```

Staged wording works best in a locked-off, pure reference-to-video clip.
Wordings that name only the boundary tend to fail: "swap at the line" can give
a hard cut with a pose jump, "changes in place at the instant" a glowing
top-to-bottom morph or an instant whole-body swap, "the line is the boundary
between the looks" a cut, and a wipe along the line alone a cut. Generate it
as reference-to-video from the element references: an image-edited first frame
re-composes the scene and moves the subject and the line. This is a
hypothesis, not a guarantee; check a 480p draft. If required progression is
unreadable, return that evidence and any conflict with locks before proposing
retiming or another treatment. Without playback, success remains unverified.

### Named cuts and transitions

For a requested jump cut, match cut, whip pan, cross dissolve, wipe, smash cut,
J-cut, or L-cut, read [Cut and transition prompts](references/cut-transitions.md).
It supplies prompt-only boundary templates and audio relationships. Choose one
picture transition per boundary; an audio J-cut or L-cut may accompany it.
These are directed visual/audio targets, not frame-accurate editing controls.

### Assembly-only cuts

For a blink cut (a lost moment), intercut between two places, or vision flash,
offer [Assembly-only cuts](references/assembly-cuts.md) when precise editing or
demonstrated failure warrants it: generate each side at a natural length and
cut in post. This is an optional production remedy, not a provider prohibition.
Preserve requested timing and return conflicts if a locked one-prompt workflow
cannot guarantee the required result; do not silently substitute assembly.

### Montage pacing

For multi-shot scenes, pick one cut rhythm. Each row gives the intent and a
canonical block describing the cut rhythm. Montage requires a shot list — see
Edge cases.

| Pacing | Intent | Canonical block template |
|---|---|---|
| Chaotic | Fast, hard cuts; high-energy sequence | `Cut fast and hard: rapid-fire shots of <A>, <B>, <C>, and <D>, each at the requested timing, with a jagged, high-energy rhythm.` One to two seconds is an optional starting point; about 0.8 s is a provisional caution, not a guaranteed merge threshold. Offer assembly for precise strobing without changing its timing. |
| Dynamic | Rhythmic medium cuts; momentum | `Cut on the beat: quick medium shots alternating between <A> and <B>, each 2-3 seconds, building momentum toward <climax>.` |
| Calm | Slow, even pacing; held shots | `Cut slowly and evenly: hold each of <A>, <B>, and <C> for several seconds with gentle, unhurried transitions and no jump cuts.` |
| Single Shot | No cuts; one continuous take | `No cuts: one continuous, unbroken shot that follows <subject> through <spaces and events in order> at an even pace from start to finish.` |

## Parameter schema

Fill these knobs when composing a pacing block. At least one of `ramp`, `pacing`,
`time_treatment`, or `transition` is required; everything else is optional.

| Parameter | Meaning | Rules |
|---|---|---|
| `ramp` | Speed ramp from the bank | Optional when another pacing knob is set. Pick exactly one per stage: Linear, Auto, Slow Motion, Bullet Time, Flash In, Flash Out, Impact, Ramp Up, Ramp Down. |
| `time_treatment` | Time-lapse, Freeze Frame or Progressive Change | One per stage; specify visible progression, held pose or timed body-part stages, and the end state. |
| `transition` | Named picture cut/transition or audio bridge | Use the same-skill reference; identify outgoing/incoming shots and the boundary time. J-cut/L-cut also name the sound source and overlap window. |
| `assembly_cut` | Blink Cut, Intercut or Vision Flash | When assembly is selected, plan outside the prompt block in the same-skill reference; it does not count toward the required pacing knobs. Generate each side separately and preserve the requested edit timing. |
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
The visuals feature a cyan neon sign high on the wall frame-left as a hard rim on Maya, wet asphalt throwing the color back up, rain streaking through the light.
0-4 seconds, a handheld follow shot at full speed tracks Maya from behind at waist height as she closes on the wall.
At 4 seconds, the camera snaps to a tight static close-up as the crate smacks the wall in a single sharp impact beat, dust bursting, then the frame holds for half a beat.
5-9 seconds, the action drops into slow motion; debris floats in deliberate slow-motion detail while Maya straightens up, until the dust settles.
9-12 seconds, the motion flashes out: the camera pulls back fast to a wide shot and the action decelerates sharply into stillness, Maya standing frame-right.
Audio: <the crate smacks hard against the wall> on the impact, then the alley falls quiet except for rain.
```

This block names the ramp (Impact, then Slow Motion, then Flash Out), names the
beat that lands (the crate impact), gives each stage a timestamp, a camera
statement and an end state, lights it from a named source rather than a grade,
and stays within a natural 12-second duration. It composes with
`seedance-prompt-25` scene staging for multi-stage scenes, with
`seedance-camera-presets` for the camera treatment, and with
`film-production` / `seedream-storyboard` when the scene needs an approved shot
list before generation.

## Edge cases and guardrails

- **Timestamps are a time budget, not frame-accurate.** Never promise exact
  frame sync. Assess action density against the actual motion and required
  readability, not a count alone; return demonstrated timing conflicts.
- **Keep camera choreography coherent.** One or two compatible moves is a
  planning heuristic, not a provider limit. Preserve explicitly requested coherent
  choreography, including additional components, with clear paths and start/end
  states. Return incompatible directions rather than silently deleting a move.
- **Pacing needs a shot list.** When the scene has multiple cuts, prefer
  `seedance-shot-design` for the shot plan (or `seedream-storyboard` /
  `film-production` for the storyboard) rather than one raw prompt. A montage without an ordered cut list lets the model cut or
  reorder arbitrarily.
- **30s single-pass or native extension only for continuous seamless motion.**
  Reserve them for a genuine single continuous take or audio-driven long
  dialogue where seamless motion across scene boundaries matters more than
  per-scene iteration. Otherwise right-size each scene to its natural
  duration. Split overloaded requests for feasibility without imposing fixed
  shots-per-generation cadence. Short multi-shot sequences are optional;
  equal durations, repeated framing and sustained holds can carry attention.
  No turn, contrast or wow quota applies. Body speed, amplitude, interruptions
  and recovery follow source intent and plausibility, not a universal burst cap.
  Speech is not an energy ceiling; assess actor energy, camera energy and
  edit rhythm separately for required readability.
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
  ratio, and watermark never go in the prompt.
- **One ramp, one pacing.** Do not stack multiple speed ramps or montage
  pacings in the same block; if the scene changes rhythm several times, split it
  into stages or separate takes.

## Self-check checklist

Before a pacing block is submitted as part of a Seedance 2.5 prompt, verify:

1. Pacing uses timestamped phrasing (`At <N>s`, `<start>-<end>s`), not vague
   "later" or "then" timing.
2. The selected ramp, pacing, time treatment, or transition comes from its bank.
3. The pacing block names the beat that lands (subject, action, and end state).
4. No frame-accurate or impossible-frequency promises are made.
5. Dialogue scenes align pacing to spoken beats; lip-sync-critical scenes pair
   with `seed-audio-prompt`.
6. `duration` is within 4-30s and not padded to fill 30s.
7. Any cut list uses consecutive, non-overlapping time ranges with ordered shot
   content.
8. Generation parameters (duration, resolution, aspect ratio) are absent from
   the prompt text.
9. Picture transitions define outgoing/incoming shots; audio bridges define
   the sound source, overlap window, and end state, and do not promise exact sync.
10. Preserve requested timing and coherent choreography. Treat about 0.8 s
    as a provisional caution; assembly or retiming are optional remedies, not
    automatic repairs. Progressive change uses timed body-part or region stages
    with unbroken motion; return real conflicts and leave unobserved results unverified.

A pacing block that passes all ten checks is ready to be composed into the
full prompt by `seedance-prompt-25`.
