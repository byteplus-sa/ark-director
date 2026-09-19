---
name: seedance-camera-presets
description: >
  Turn a named camera move or preset — dolly, pan, tilt, orbit, crane, jib,
  tracking, handheld, FPV, aerial, bullet time, dolly zoom, crash zoom, whip
  pan, one-take, or static — into a canonical, drop-in Camera block for the
  Seedance 2.5 six-part prompt formula. Use when the user asks for a camera
  preset, camera movement style, or a shot's camera treatment.
  Bullet time here is the camera-orbit technique (freeze + orbit); speed-ramp
  and slow-mo timing belong to seedance-pacing-presets. One-take here is the
  pass-through camera path; single-shot no-cuts pacing belongs to
  seedance-pacing-presets. Lens and focal-length optics belong to
  seedance-lens-presets.
---

# Seedance Camera Presets

This skill turns a named camera preset, movement style, or camera personality into a
canonical, drop-in **Camera block** for the Seedance 2.5 six-part prompt formula
(Subject + Action + Scene + Visual Style + Camera + Audio). It is a
**prompt-composition-only** skill: it never calls MCP tools or the Ark API, and
it never runs generation. The base prompt grammar — the six-part formula,
`@Image N` / `@Video N` reference-role syntax, `At Ns` timestamp syntax, and
audio bracket syntax — is defined in `seedance-prompt-25` and is **not
redefined here**. Compose with `seedance-prompt-25` for the full prompt
contract; this skill only adds the preset bank on top.

The output of this skill is always a **Camera block** — one or two sentences
describing shot size, angle, camera movement, and speed — plus any timestamped
transition phrasing, ready to be inserted as the `Use <camera block>.` line of
a Seedance 2.5 prompt.

## Source authority

The preset bank is built from the official Seedance 2.5 camera vocabulary. All
sources accessed 2026-08-13:

- [Seedance 2.5 Prompt Guide (Lark)](https://bytedance.larkoffice.com/docx/A88jd0B47oAd8zxWp5ycZFMfnxh) — official camera vocabulary, timestamp rules, technique contracts
- [BytePlus ModelArk prompt guide](https://docs.byteplus.com/en/docs/ModelArk/2607689) — official prompt guidance
- [Seedance 2.5 launch blog](https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5) — official announcement

**The base grammar is defined in `seedance-prompt-25`.** This skill adds the
preset bank and Camera-block composition rules; it does not restate or replace
the six-part formula, reference-role syntax, or audio syntax from that skill.

## Preset bank

### Basic moves

Use the canonical phrase directly. Each basic move maps to the official
Seedance vocabulary (`push in`, `pull out`, `pan`, `lateral move`, `follow
shot`, `orbit`, `dolly out`, `tilt up`, `handheld shake`). Where a frame has
several subjects, still state **which subject** the camera follows, **where**
the movement begins, and **where** it ends.

| Preset | Canonical phrase template |
|---|---|
| Pan left | `Slowly pan to the left across <subject or scene>.` |
| Pan right | `Slowly pan to the right across <subject or scene>.` |
| Tilt up | `Tilt up from <subject or ground element> to <subject, ceiling, or skyline>.` |
| Tilt down | `Tilt down from <subject or high element> to <subject, floor, or ground>.` |
| Dolly in | `Slow dolly in toward <subject>, stopping at <shot size>.` |
| Dolly out | `Slow dolly out from <subject>, pulling back to <shot size>.` |
| Dolly left / right | `Dolly laterally to the left/right, keeping <subject>'s <feature> framed.` |
| Truck left / right | `Truck laterally to the left/right at the same speed as <subject>, keeping <subject> sharp while <background> streaks past.` |
| Track / follow shot | `Tracking shot: move horizontally at the same speed as <subject>, keeping <subject> sharp while <background> forms motion blur.` |
| Orbit | `Orbit around <subject> <clockwise/counterclockwise> over <N> degrees, at <height or level>.` |
| Dive | `Dive toward <subject or ground feature> from <starting height>, plunging fast and pulling up before <impact point>.` |
| Crane up | `Crane up from a <low angle> on <subject> to a <high angle or overhead> view of <scene>.` |
| Crane down | `Crane down from a <high angle or overhead> view of <scene> to <subject level>.` |
| Jib up | `Jib arc up over <subject>, <left-to-right or right-to-left>.` |
| Jib down | `Jib arc down over <subject>, <left-to-right or right-to-left>.` |
| Static / locked-off | `Locked-off static camera on a tripod, no camera movement — only <subject> moves within the frame.` |

### Technique presets

These are the named cinematic techniques. Each row states the official
"What to Specify" contract from the `seedance-prompt-25` popular-techniques
table, then gives a canonical phrase template that satisfies it.

| Preset | What to specify | Canonical phrase template |
|---|---|---|
| Dolly zoom | Subject size to preserve; whether background moves closer or farther | `Dolly zoom on <subject>: keep <subject>'s size constant while the background <moves closer / compresses behind them> (or <pulls farther away / expands>).` |
| Crash zoom / rapid zoom | Target subject; sudden speed; optional timestamp | `At <N>s, crash-zoom rapidly in on <subject>, the frame snapping inward in one aggressive push.` |
| Whip pan | Trigger time, direction, occluding element, continuation | `Whip-pan transition: at <N>s, move the camera rapidly to the <left/right>. Cut when the foreground <occluding element> fully covers the frame, then continue moving <direction> at a similar speed in the next scene.` |
| Aerial reveal | Viewing height, movement direction, area to reveal | `High aerial view at <height> above <scene>; the camera <moves direction> and gradually reveals <area>.` |
| FPV path | First-person flight/traversal path, speed, turns | `First-person view flying <path>, at <speed>, banking <left/right> through <turns or waypoints>.` |
| Bullet time | Camera orbit direction around the frozen subject | `Bullet time: the camera orbits <clockwise/counterclockwise> around <subject> while the action is frozen. Timing (freeze duration, end state) belongs to seedance-pacing-presets.` |
| Handheld | Subject being followed; amount of shake | `Handheld camera following <subject>, with <slight/moderate/heavy> shake.` |
| One-take | Subjects, spaces, and events the camera passes through in order | `One-take shot: the camera passes through <subject or space A> as <event A>, then <subject or space B> as <event B>, then <subject or space C> as <event C>, with no cuts.` |
| Rack focus | Term + subject + visual change + foreground/background + direction | `Rack focus: shift focus smoothly from the <foreground element> to <background subject>. The <foreground> gradually blurs while <background subject> changes from soft to sharp.` |

For a technique not in the table, follow the uncommon-cinematography-terms
recipe from `seedance-prompt-25`:

> **Cinematography Term + Target Subject + Visual Change + Foreground/Background Relationship + Direction or Speed**

### Camera styles

Camera styles describe the camera's personality for the whole clip — a
paragraph-level treatment you can append to a prompt. Choose one style per
prompt; do not combine styles.

| Style | Camera-treatment block |
|---|---|
| Auto | `Use a natural camera treatment that best fits the action and scene.` |
| Classic Static | `Classic static camera: locked-off, tripod-mounted, composed frames with minimal movement; all motion happens within the frame as subjects move through it.` |
| Silent Machine | `Silent machine camera: smooth, precise, mechanical gimbal moves that glide almost invisibly; neutral and unobtrusive, never drawing attention to itself.` |
| One Take | `One-take camera: a single continuous unbroken shot with no cuts, following the action through every space and event from start to finish.` |
| Epic Scale | `Epic-scale camera: vast wide establishing shots with slow sweeping aerial and crane reveals that dwarf the subject in a grand, spacious frame.` |
| Intimate Observer | `Intimate observer camera: close-ups and gentle handheld moves that stay near the subject, quiet and personal, capturing small gestures and expressions.` |
| Impossible Camera | `Impossible camera: surreal paths and extreme angles a physical camera cannot take, gliding through walls and over objects with weightless freedom.` |
| Documentary Snap | `Documentary snap camera: observational and spontaneous, naturalistic handheld with reportage framing and a sense of real, unstaged life.` |
| Raw Chaos | `Raw chaos camera: aggressive handheld with fast, erratic, disorienting moves that amplify the energy and instability of the scene.` |
| Dreamy Flow | `Dreamy flow camera: slow, floating, gently drifting moves with soft graceful motion and a calm, weightless feel.` |

### Shot size + angle vocabulary

Select from this vocabulary when filling the shot-size and angle knobs. Shot
sizes and `low angle`, `overhead view`, and `first-person view` are official
Seedance terms; `high angle` and `eye level` are common cinematography
additions — safe to use, but not in the official vocabulary list.

| Parameter | Options |
|---|---|
| Shot size | extreme wide shot, wide shot, medium shot, close-up, extreme close-up |
| Angle | low angle (official), high angle, overhead view (official), eye level |
| Viewpoint | first-person view (official), third-person observer |

## Parameter schema

Fill these knobs when composing a Camera block. Only `move` (or `style`) is
required; everything else is optional.

| Parameter | Meaning | Rules |
|---|---|---|
| `move` | Named preset from the bank | Required; one preset. If `style` is also set, `move` may be "auto" or omitted. |
| `style` | Camera style (10 above) | Optional; one per prompt. Sets the camera personality for the whole clip. |
| `subject` | What the camera follows, plus where the move starts and ends | State a named subject whenever one exists (`@gloria`, `Gloria`, `the courier`). For technique presets, state which subject the camera follows and where the movement begins and ends. |
| `shot_size` | From the shot-size vocabulary | Optional; e.g. `medium close-up`. |
| `angle` | From the angle vocabulary | Optional; e.g. `low angle`. |
| `timestamp` | Optional `At Ns` moment for a transition or beat | Use only for critical handoffs or transitions. A time budget, not frame-accurate. |
| `stack` | Number of simultaneous moves in one clip | **At most 2 per clip.** Default to one move. Add one secondary move (e.g. `dolly in` + `tilt up`) only when the shot requires it and the motions remain compatible; more than 2 risks instability. |
| `speed` | Pace of the move | Optional; use directional words (`slow`, `fast`, `rapid`, `leisurely`) rather than numeric fps. |

## Output grammar

The Camera block drops into the Camera slot of the six-part formula, replacing
the `<camera treatment>` placeholder:

```
<Subject> performs <action> in <scene>.
The visuals feature <visual style>.
Use <camera block>.
Audio includes <audio>.
```

**Camera-block template:**

```
Use [At <N>s, ] <move 1> [then <move 2>], <shot size>, <angle>, <speed> [; <timestamped transition>].
```

**Worked example (T2V, dolly-in preset):**

```
@Image 1 defines Gloria's appearance, hairstyle, and clothing. Do not use the background of the image.
Gloria walks through the neon alley at night, rain-slick asphalt reflecting the signs overhead.
The visuals feature a teal-and-orange cinematic grade with soft halation.
Use a slow dolly in toward Gloria's face, medium close-up, low angle, ending on a static lock as she stops and turns toward the camera.
Audio includes rain pattering and a distant car engine.
```

The `Use ...` sentence is the Camera block. It references the named subject,
gives the shot size and angle, states one primary move that ends in a static
lock, and matches the style of a full Seedance 2.5 prompt.

## Edge cases and guardrails

- **Optical zoom is not a dolly zoom.** A dolly zoom requires physical camera
  movement plus counter-zoom. If the user wants true optical zoom, write
  `purely optical zoom on a locked-off tripod`; if they want the dolly-zoom
  effect, write `the camera physically dollies in while the lens zooms out`.
- **Timestamps are a time budget.** `At Ns` allocates time to a beat; it is not
  a frame-accurate edit point, and actions may land slightly before or after
  the boundary.
- **At most 1-2 moves per clip.** A clip with more simultaneous moves becomes
  unstable and cuts erratically. `stack` defaults to 1; allow 2 only when the
  second move is a natural continuation (e.g. `dolly in, then tilt up`).
- **Locked-off shots use `camera_fixed`.** For a static camera, keep the
  prompt's camera block and also set the generation parameter
  `camera_fixed: true` so the frame stays locked.
- **One-take needs explicit order.** A one-take shot must list the subjects,
  spaces, and events the camera passes through **in order**; an unordered list
  lets the model cut or reorder the passage.
- **Inherit, don't restate.** If a `@Video` reference already defines motion or
  camera movement, state **only which attributes to inherit** and let the
  preset apply to anything the reference does not cover. Repeating the motion
  can conflict with the reference itself.
- **Generation parameters stay in the API.** Duration, resolution, aspect
  ratio, and watermark never go in the prompt. Keep `watermark: false` by
  default.
- **Numeric optics are advisory.** Focal length, aperture, and shutter values
  may be included, but always pair them with the intended **visible result**
  (e.g. `shallow depth of field — background soft with compressed bokeh`), per
  the official guide.

## Self-check checklist

Before a Camera block is submitted as part of a Seedance 2.5 prompt, verify:

1. The `move` is from the preset bank, or follows the Cinematography-Term +
   Subject + Visual Change + Foreground/Background + Direction recipe for
   uncommon terms.
2. `stack` is 2 or fewer simultaneous moves.
3. The Camera block names the subject the camera follows whenever a subject
   exists, and states where the move starts and ends.
4. No numeric aperture or focal value appears alone without a visible result.
5. Shot size and angle come from the official vocabulary when specified.
6. Any timestamp uses `At Ns` syntax and is reserved for a critical beat or
   transition — not paced frame-by-frame.
7. A whip pan or other transition includes the trigger time, direction,
   occluding element, and the composition or motion that continues after.
8. A one-take shot lists subjects, spaces, and events in order.
9. Generation parameters (duration, resolution, aspect ratio) are absent from
   the prompt text.

A Camera block that passes all nine checks is ready to be composed into the
full prompt by `seedance-prompt-25`.
