---
name: seedance-camera-presets
description: >
  Turn a named camera move or preset — dolly, pan, tilt, orbit, crane, jib,
  tracking, handheld, FPV, aerial, bullet time, dolly zoom, crash zoom, whip
  pan, optical zoom, Dutch angle, one-take, or static — or a shot framing
  (single, two-shot, over-the-shoulder, over-the-hip, point of view, insert) —
  into a canonical, drop-in Camera block for the Seedance 2.5 six-part prompt
  formula.
  Use when the user asks for a camera
  preset, camera movement style, shot framing, or a shot's camera treatment,
  and when a shot plan names a move or framing to word.
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

- [BytePlus ModelArk prompt guide](https://docs.byteplus.com/en/docs/ModelArk/2607689) — official prompt guidance
- [Seedance 2.5 launch blog](https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5) — official announcement

**The base grammar is defined in `seedance-prompt-25`.** This skill adds the
preset bank and Camera-block composition rules; it does not restate or replace
the six-part formula, reference-role syntax, or audio syntax from that skill.

The framing templates are the exception to the official-vocabulary basis: they
use common film language, are marked as heuristics where they appear, and are
not verified model controls.

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
| Optical zoom in | `Purely optical zoom in on <subject> from <starting shot size> to <ending shot size>; the camera stays in the same position on a locked-off tripod as the subject grows larger in frame.` |
| Optical zoom out | `Purely optical zoom out from <subject> from <starting shot size> to <ending shot size>; the camera stays in the same position on a locked-off tripod as more of the scene enters the frame.` |
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

Rack focus is a focus change, not a camera move: the lens preset skill owns its
wording and its evidence (drafts keep a face sharp, so a pull away from a face
is added in post).

For a technique not in the table, follow the uncommon-cinematography-terms
recipe from `seedance-prompt-25`:

> **Cinematography Term + Target Subject + Visual Change + Foreground/Background Relationship + Direction or Speed**

### Camera styles

Camera styles describe the camera's personality for the whole clip — a
paragraph-level treatment you can append to a prompt. Choose one style per
prompt; do not combine styles. Within the chosen style, each shot of a clip that
cuts still gets its own move, size and angle.

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
Seedance terms; `high angle`, `eye level`, and `Dutch angle` are common cinematography
additions — safe to use, but not in the official vocabulary list.

| Parameter | Options |
|---|---|
| Shot size | extreme wide shot, wide shot, medium shot, close-up, extreme close-up |
| Angle | low angle (official), high angle, overhead view (official), eye level, Dutch angle / canted angle |
| Viewpoint | first-person view (official), third-person observer |
| Framing | single, dirty single / over-the-shoulder, two-shot, three-shot, group shot, over-the-shoulder, over-the-hip, point of view, insert (common film language, not official) |

**Dutch angle template:** `Dutch angle on <subject>: hold the camera rolled
<clockwise/counterclockwise> so the horizon stays visibly diagonal, framing
<shot size>.` State a mild or pronounced cant when relevant. A held cant is an
orientation, not a rolling camera move; describe a changing roll separately and
count it toward the move limit. It may accompany one compatible move, such as
a slow dolly in. These additions are prompt-authoring heuristics, not verified
model controls or guarantees of simulated optics.

### Framing templates

Framing places subjects in the frame and says how many are featured. Choosing
the right framing for a beat belongs to the shot-design skill's framing
reference; this section only words it. Name each subject and its screen side
as frame-left or frame-right so the model has positions to place (it reads
"her left" as the character's own side), and keep the foreground subject of an
over-the-shoulder or over-the-hip shot soft and unfeatured. These are
prompt-authoring heuristics, not verified model controls: check a 480p draft
before relying on one.

| Framing | Template |
|---|---|
| Single | `Single shot of <subject>, <shot size>, <angle>, with <subject> alone in the frame.` |
| Dirty single / over-the-shoulder | `Over-the-shoulder shot from behind <foreground character>: their shoulder and the back of their head sit soft and dark at frame-<left/right>, while <subject> is sharp and facing the camera, <shot size>.` |
| Over-the-hip | `Over-the-hip shot: the hip and hand of <standing character> sit soft in the frame-<left/right> foreground, while <lower character> is sharp in the middle distance, <shot size>, <angle>.` Use only when the two characters are at different heights. |
| Two-shot | `Two-shot: <A> frame-left and <B> frame-right, both fully in frame and in focus, <shot size>, <angle>.` |
| Three-shot | `Three-shot: <A> frame-left, <B> in the center and <C> frame-right, all in focus, <shot size>.` |
| Group shot | `Group shot of <group> arranged <layout>, with <front subject> nearest the camera, <shot size>.` |
| Point of view | `Point-of-view shot, first-person view from <character>'s eyes: the frame shows <what they see> and <the hands or limbs they would see>, <shot size>.` For an object, `Point-of-view shot from <object> as it <moves>`. Cover it with a shot of the looker before it and the reaction after it. |
| Insert | `Insert shot: <detail> fills the frame, <shot size>, <held or one named move>.` Add a face only when the beat needs it. |

### Composing framing with a move

A framing template supplies the featured subjects, their screen sides, the
shot size and the angle. When a move is also wanted, write the move first and
the framing clause after it, and state shot size and angle once:
`Use <move>, <framing clause without its own size and angle>, <angle>, <speed>.`
A framing-only block is allowed when the shot is held: end it with an explicit
static hold (`held static`) so the missing move is a recorded choice.

Example: `Use a slow push-in, over-the-shoulder shot from behind Ben: his
shoulder and the back of his head sit soft and dark at the left of the frame
while Marta is sharp and facing the camera, medium close-up, eye level, ending
on a static lock.`

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
| `framing` | From the framing templates | Optional; one per shot. Name each featured subject and its screen side. |
| `timestamp` | Optional `At Ns` moment for a transition or beat | Use only for critical handoffs or transitions. A time budget, not frame-accurate. |
| `stack` | Number of simultaneous moves in one shot | **At most 2 per shot.** Default to one move. Add one secondary move (e.g. `dolly in` + `tilt up`) only when the shot requires it and the motions remain compatible; more than 2 risks instability. A clip that cuts has one Camera block per shot, so the clip as a whole may carry more moves. |
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
The visuals feature a magenta neon sign frame-right as the key on Gloria's face, cold blue spill from the alley mouth behind her, and rain streaking through the light in the foreground.
Use a slow dolly in toward Gloria's face, from a medium shot to a medium close-up, low angle, ending on a static lock as she stops and turns toward the camera.
Audio includes rain pattering and a distant car engine.
```

The `Use ...` sentence is the Camera block. It references the named subject,
gives the shot size and angle, states one primary move with its start and end,
and matches the style of a full Seedance 2.5 prompt. The light is a named,
motivated source rather than a grade; a grade, when one is wanted, belongs to
the color-grade skill or to post.

## Moves that read

A clip with no camera statement tends to come back as a neutral, held frame,
and hedged wording on every line reads as flat footage. Plain wording already
produces a push-in or a fast move; the preset adds control: where the move
starts and ends, its speed, its timing, and the hold after it.

- State a move for every moving shot, with an active verb and a speed: the
  camera drives in fast, sweeps left, rises over, snaps to, glides behind.
  Reserve `gentle` and `subtle` for a shot whose stillness is the point.
- Give a timed beat to the move only where it matters (`At 3s, crash-zoom in on
  <subject>`); otherwise the start and end states carry it.
- In a clip that cuts, each shot carries its own Camera block. The shot plan
  (the shot-design skill) decides which shots move; this skill words them.

## Edge cases and guardrails

- **Optical zoom is not a dolly zoom.** A dolly zoom requires physical camera
  movement plus counter-zoom. If the user wants true optical zoom, write
  `purely optical zoom on a locked-off tripod`; if they want the dolly-zoom
  effect, write `the camera physically dollies in while the lens zooms out`.
- **Timestamps are a time budget.** `At Ns` allocates time to a beat; it is not
  a frame-accurate edit point, and actions may land slightly before or after
  the boundary.
- **At most 1-2 moves per shot.** A shot with more simultaneous moves becomes
  unstable and cuts erratically. `stack` defaults to 1; allow 2 only when the
  second move is a natural continuation (e.g. `dolly in, then tilt up`). In a
  clip that cuts, write one Camera block per shot so each cut can carry its own
  move.
- **A locked-off shot is a recorded choice.** State the static camera in the
  Camera block and record its `static_reason` in the shot plan (the
  shot-design skill owns the allowed values). The Seedance 2.5 MCP tool exposes no `camera_fixed`
  field (checked 2026-10-06; the legacy `seedance-prompt-20` skill documents it
  for the 2.0 REST API), so the prompt carries the lock. A hold lands best after
  motion.
- **One-take needs explicit order.** A one-take shot must list the subjects,
  spaces, and events the camera passes through **in order**; an unordered list
  lets the model cut or reorder the passage.
- **Inherit, don't restate.** If a `@Video` reference already defines motion or
  camera movement, state **only which attributes to inherit** and let the
  preset apply to anything the reference does not cover. Repeating the motion
  can conflict with the reference itself.
- **Generation parameters stay in the API.** Duration, resolution, aspect
  ratio, and watermark never go in the prompt, including a sentence such as
  "composed for 2.39:1"; set the ratio as a parameter.
- **Numeric optics are advisory.** Focal length, aperture, and shutter values
  may be included, but always pair them with the intended **visible result**
  (e.g. `shallow depth of field — background soft with compressed bokeh`), per
  the official guide.

## Self-check checklist

Before a Camera block is submitted as part of a Seedance 2.5 prompt, verify:

1. The `move` is from the preset bank, or follows the Cinematography-Term +
   Subject + Visual Change + Foreground/Background + Direction recipe for
   uncommon terms.
2. `stack` is 2 or fewer simultaneous moves per shot.
3. The Camera block names the subject the camera follows whenever a subject
   exists, and states where the move starts and ends with an active verb and a
   speed.
4. No numeric aperture or focal value appears alone without a visible result.
5. Shot size and angle come from the listed vocabulary when specified; common
   cinematography additions are not presented as official model controls.
   A framing template names each featured subject and its frame side and
   keeps a foreground subject soft and unfeatured.
6. Any timestamp uses `At Ns` syntax and is reserved for a critical beat or
   transition — not paced frame-by-frame.
7. A whip pan or other transition includes the trigger time, direction,
   occluding element, and the composition or motion that continues after.
8. A one-take shot lists subjects, spaces, and events in order.
9. Generation parameters (duration, resolution, aspect ratio) are absent from
   the prompt text.

A Camera block that passes all nine checks is ready to be composed into the
full prompt by `seedance-prompt-25`.
