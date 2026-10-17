---
name: seedream-location-asset
description: Write structured Seedream prompts for cinematic location assets, reusable environment sheets, day and night lighting-state locks, and same-place environment plates for video restyles. Invoke when the user asks to create a location, interior, exterior, set reference, night version of a location, or establishing still with Seedream.
---

# Seedream Location Asset

Write production-grade prompts for BytePlus Seedream location and environment
asset generation. This skill is for **places**, not characters: interiors,
exteriors, establishing shots, reusable location sheets, set references,
lighting-state locks, and same-place environment plates intended for downstream
Seedance, storyboards, or project `elements/<location-id>/` assets.

Use this skill when the user wants:
- a reusable **location asset** for a project
- an **interior** or **exterior** environment still
- a **set reference** or **location sheet**
- a **night or other lighting-state lock** of an approved location
- a **same-place environment plate** for a restyle or background swap
- an **establishing shot** prompt for Seedream

Do **not** use this skill for:
- character sheets
- product packshots or prop sheets (use `seedream-prop-asset`)
- infographic-heavy layouts
- exact signage, menus, or screen copy (finish them with a deterministic
  HTML-entrypoint render over a text-free plate)
- local image edits that need coordinate-based editing

## Source authority

This skill adapts the general Seedream prompt structure (owned by
`seedream-prompt`, which also holds model limits, sizes, and reference rules)
to locations. Compose with it for anything not location-specific.

- [Seedream 5.0 Pro official blog](https://seed.bytedance.com/en/blog/beyond-generation-it-understands-design-introducing-seedream-5-0-pro)
- [Seedream 4.0-5.0 API Tutorial](https://docs.byteplus.com/en/docs/ModelArk/1824121)
- [Seedream 4.0-4.5 Prompt Guide](https://docs.byteplus.com/en/docs/ModelArk/1829186)

When official documentation changes, prefer the live docs over this skill where
they conflict.

## Reference loading

- [Worked examples](references/worked-examples.md) — load when writing a full
  prompt from scratch: a canonical interior lock, a night lock, and a same-place
  environment plate.
- [Complex architecture](references/complex-architecture.md) — load when the
  location has staircases, galleries, balconies, or other geometry the model
  tends to invent.

## Flexible prompt structure

Use this order for the sections that apply. Do not add empty boilerplate:

- **References** only when images are provided
- **Task** when the mode needs clarification
- **Location** for every location asset
- **Era and world rules**, **Set dressing and objects**, **Style**,
  **Lighting and atmosphere**, and **Composition and lens** when relevant
- **Text in image** only when non-exact signage is expressly accepted
- **Constraints** only for useful quality, continuity, and exclusion requirements

Put the **place** before the mood and the **era/world rules** before lens or
style polish.

### 1. References (when provided)

List every reference image in order with its role, then bind it again in the
instruction it controls: "Use the architecture and spatial layout from
@Image 1, the lighting mood from @Image 2, and the wood and brass materials
from @Image 3." Separate references by role: **location geometry**, **lighting
mood**, **material / dressing detail**. A prior approved still of the location
is the highest-priority identity reference.

### 2. Task type

Use **Text-to-Image (T2I)** only when the prompt uses no reference images. Use
**Image-to-Image (I2I)** whenever any reference guides geometry, dressing,
materials, style, lighting, or composition, including first-pass locations
built from mood boards.

### 3. Location

Describe the place itself first: interior or exterior, function of the space,
scale and spatial mood, and core architectural identity.

When the location has an emotional function (the space must feel like a trap,
a sanctuary, a stage), state it as visible design: scale, ceiling height, where
the floor pattern pulls the eye, how far the exits sit from the centre. "A
vast, near-dark library hall whose high shelves fall away into black, with one
circular carpet pattern at the centre like a ring" is usable; "an oppressive
room" is not.

A counterpoint location that plays against the genre can state the world's
rules without dialogue. Record that rule under era and world rules so the set
dressing keeps it (a library with no screens or devices anywhere).

### 4. Era and world rules

Anchor the image in its historical, cultural, or fictional logic: period,
geography and climate, technology level, realism rules. For example "Late-1990s
Manila urban realism, analog signage, no smartphones" or "Near-future Asian
megacity, grounded cyberpunk, practical infrastructure, not fantasy magic."

### 5. Set dressing and objects

List 1–3 hero set pieces, practical objects that imply use, material realism
and wear, and foreground/midground/background depth cues. Good location prompts
feel **lived in**, not empty.

- **Count what recurs.** Give fixed set pieces a number and position ("two
  brass lanterns, one on each side of the door"); video prompts restate the same
  count, and unnumbered repeats drift between shots.
- **Plain surfaces stay plain.** Generic boxes, jars, sacks, crates, posters,
  and shop fronts grow invented lettering, which the video then animates.
  Describe them positively, for example "plain unlabeled cardboard boxes,
  smooth solid surfaces, nothing printed". Story signage that must read is a
  deterministic overlay or a separate prop reference.

### 6. Style

Pick 2–4 strong anchors: photorealistic, cinematic, naturalistic editorial
reference, grounded realism, film still, period-authentic production design.
Avoid vague style stacks.

### 7. Lighting and atmosphere

Name the actual light sources: the practical key and its side of frame, time
of day and weather, shadow falloff, haze/dust/smoke/moisture, and how bright or
restrained the scene is. "Warm tungsten lantern as the single practical key
from frame-left, deep shadow falloff into the corners" is usable; "moody light"
is not.

### 8. Composition and lens

Say how the place is photographed: establishing vs. detail vs. reference sheet,
camera height and angle, lens length, and depth of field. Set the aspect ratio
with the `size` parameter, not a ratio sentence in the prompt. A still has no
camera move; leave push-ins and pans to the video prompt.

### 9. Text in image

Omit by default. Include only when the user expressly accepts model-rendered
signage as non-exact; otherwise keep signs blank or abstract and finish exact
copy deterministically.

### 10. Constraints

Keep exclusions short and after the positive description: no people (for a
reusable plate), no modern intrusions for period work, no plastic CGI surfaces,
no text overlays, no watermark. Set resolution with `size`, not a "4K" quality
word.

## Video-ready location locks

A bound location reference overrides prompt text for what it shows: its light,
its sky, its dressing, its layout. Lock the states the video needs instead of
hoping the shot prompt will repaint them.

### One lock per lighting state

Make a separate approved image for each lighting state that scenes use (day,
dusk, night, lights-off) from the approved day lock, as an I2I iteration that
keeps the geometry. Bind the lock that matches the shot. A day plate plus "at
night" in the video prompt keeps day light.

### Night locks

Night needs to be stated, not implied:

- **Black sky** with no blue gradient, **low overall exposure**, and a **small
  pale moon** placed in a named part of the sky when the sky is visible.
- Name every light that is on: which windows glow, which lamps or practicals
  burn, and where their pools fall. Everything else falls to deep shadow.
- Describe wanted shapes positively. Strong priors such as a cone-shaped light
  beam, a full bright moon, or a glowing horizon return under a negation
  ("never a cone"); state the shape you want instead ("a soft round pool of
  lamplight on the ground, no visible beam").

### Same-place environment plates

A restyle or background-swap video keeps its place. When a video edit needs an
environment image of the source's own location:

- Describe the **source's own place**: the same kind of street or room, layout,
  landmarks, furniture, plants, camera side, and time of day, in the target
  medium or look. Never rename the location or move it somewhere else unless
  the user asks.
- Generate it from text when no image of the place exists; it needs no user
  input. Keep it empty of people and of props the shot does not have.
- Before approval, compare it with sampled source frames: same place, same
  landmark positions, no stray objects. A different place is a failed plate,
  however attractive.

## Location prompt patterns

| Pattern | Use | Focus |
| --- | --- | --- |
| Reusable location asset | Project location sheet for `elements/<location-id>/` | Stable architecture, clear materials, readable layout, minimal action, no people |
| Cinematic establishing still | Mood and worldbuilding | Motivated light, camera language, atmosphere, foreground/background layers |
| Reference-preserving iteration | New time of day, lighting state, weather, dressing, wider or closer view of an approved place | I2I with the approved still as `@Image 1` |
| Same-place environment plate | Background for a restyle or swap | The source's own place, target look, empty |

For reusable assets, keep the frame readable and avoid dramatic obstructions.

## File targets

When a generated location asset is approved, save it under
`projects/<project>/elements/<location-id>/` using the workspace naming
contract, for example:

- `loc_<location-id>_wide_v01.png`
- `loc_<location-id>_night_v01.png`
- `loc_<location-id>_detail_v01.png`
- `loc_<location-id>_env-claymation_v01.png` for a styled environment plate

## Quick defaults

- Model: `dola-seedream-5-0-pro-260628`
- Format: `png`
- Prompt optimization: `standard`
- Typical size: `2048x2048` for square sheets, `2816x1584` for 16:9; match the
  video's delivery ratio for plates that a shot will bind.
