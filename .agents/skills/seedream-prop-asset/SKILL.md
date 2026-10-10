---
name: seedream-prop-asset
description: Write structured Seedream prompts for prop and product identity sheets used as Seedance or storyboard references. Applies the prop threshold and acquisition-first rule, then plans the views - front and back by default, plus a side view when the user asks or the object's profile carries its identity. Invoke when the user asks for a prop sheet, product reference, hero object, vehicle, device, tool, scene-variant wearable, or prop state variant with Seedream.
---

# Seedream Prop Asset

Write production-grade prompts for BytePlus Seedream prop and product identity
sheets. This skill is for **objects**: held and operated props, hero objects the
camera lingers on, recurring products, vehicles, devices, mechanisms, and
wearables that appear in only some scenes. The output becomes a reusable
`elements/<prop-id>/` reference for Seedance, storyboards, or later Seedream I2I.
Every sheet shows the object from more than one side: **front and back by
default, with a side view added when the object or the user needs it.**

Use this skill when the user wants:
- a prop sheet or prop reference
- a product identity reference for video
- a vehicle, device, tool, or mechanism reference
- a scene-variant wearable (sunglasses, a jacket, a mask) kept off the
  character sheet
- a state variant of an approved prop (open/closed, lit/unlit, intact/broken)
- a continuity mark on a character's body (birthmark, tattoo, scar), see
  Body continuity marks below

Do **not** use this skill for:
- always-worn outfit items, which stay in the character sheet
- locations, set dressing, or furniture that belongs to a place
- commercial product scenes, hero ads, or packshots set in an environment
- exact labels, logos, packaging copy, UI screens, or product lineups
- local edits to an approved prop image
- a full outfit change on an approved character sheet (`seedream-character-outfit`)

Composition hints: `seedream-character-sheet` owns people and always-worn
outfits, `seedream-location-asset` owns places, `seedream-prompt` owns general
product imagery, `seedream-edit` owns point and box edits, and
`html-graphic-render` owns exact copy and layout.

## Source authority

This skill follows the Seedream prompt structure from `seedream-prompt` and
adapts it for prop and product identity references.

- [Seedream 5.0 Pro official blog](https://seed.bytedance.com/en/blog/beyond-generation-it-understands-design-introducing-seedream-5-0-pro)
- [Seedream 4.0-5.0 API Tutorial](https://docs.byteplus.com/en/docs/ModelArk/1824121)
- [Seedream 4.0-4.5 Prompt Guide](https://docs.byteplus.com/en/docs/ModelArk/1829186)
- Workspace [element identification](../../contracts/element-identification.md)
  and [asset naming](../../contracts/asset-naming.md) contracts

When official documentation changes, prefer the live docs over this skill where
they conflict.

## Submission boundary

The caller owns production authorization, request preflight, prompt review,
and submission. This skill returns one of three outcomes without loading sibling
skills: a prompt package, a text-only descriptor when the gate says no sheet is
needed, or a reuse-or-acquire handoff with no prompt when a real asset should
be used instead. A draft or a provider success does not establish approval.

## Gate: does this prop need a sheet?

Identify every visible object, then apply the threshold. A prop needs a
**locked reference** only when at least one row says yes. When the user
explicitly asks for a sheet of an object below the threshold, write it and note
that it is below the threshold:

| Criterion | Example | Locked reference? |
|---|---|---|
| Branded product with a logo or specific design, when the brief authorizes the real brand | canned tuna, fiber modem, phone with app UI | Yes — acquire first |
| The camera lingers on it or it drives the plot | a key, a letter, a device screen the camera shows | Yes |
| It recurs across two or more shots or scenes | the same phone in several ads | Yes |
| Scene-variant wearable | sunglasses worn in some scenes only | Yes |
| Generic, unbranded, briefly visible | a coffee cup, a cake, a tablet in a montage | No — describe in text |
| Held for one or two seconds in one shot | a pen, a glass of water | No — describe in text |

A locked reference is an approved local asset with a content hash, not
automatically a Seedream generation. Choose the source in this order:

1. **Reuse** a project asset whose content hash still matches the identity.
2. **Acquire** an official, authorized, or user-supplied image when the brief
   authorizes a real brand, logo, or labeled product, or the user supplied a
   photo of the object. An unknown or unauthorized brand stays de-identified
   and is described with placeholder descriptors.
3. **Generate** with this skill only when no usable real asset exists, the user
   asks for a stylized or fictional substitute, or acquisition is blocked.

The contract's reuse, hash-check, provenance, and no-copied-approval steps are
in [element identification](../../contracts/element-identification.md).

When the gate says text-only, return a short object descriptor for the scene
prompt instead of a sheet prompt. When in doubt about an unbranded object,
describe it in the video prompt and skip the Element.

**Views and acquisition.** Gather the real front and back, plus the side when the
view plan below calls for it. When the source lacks a planned view, report the
gap to the caller. An unbranded object's missing view may be generated I2I from
the source image; never invent the missing face of a real branded or labeled
product, whose back carries its own copy and marks.

## Default production rule

Plan the views for each prop before writing the prompt.

**View plan.** Default to **front** and **back**. Add **side** when the user asks
for it, or when the object's identity or use lies in its profile. Decide from the
object, and tell the caller the chosen views with one line of why.

Add a side view when the object is deep and its flanks carry detail the front
and back do not show: doors, wheels, handles, hinges, controls, a distinctive
profile silhouette. Front and back are enough when the object is near-symmetric
around its vertical axis, thin or flat, or has plain flanks that repeat the face.

| Object | Views | Why |
|---|---|---|
| Car, taxi, motorcycle, cart, boat, aircraft | front, back, side | every flank carries identity: doors, wheels, profile |
| Machine, appliance, instrument, tool, chair, shoe, bag | front, back, side | profile and controls differ by side |
| Apple, orange, egg, ball, coin | front, back | near-symmetric; the second face shows the other markings |
| Phone, tablet, card, mask, jacket laid flat | front, back | thin or planar; the faces carry it |
| Bottle, can, jar, mug | front, back | rotationally even; the second face turns the object |

When the object is ambiguous, ask whether the shots will show its flanks; if they
will, add side. Top, underside, and edge views are single-view requests, never
part of the default plan.

**Angle per view.** A flat or planar face, and a rotationally even object (fruit,
bottles, cans), is shown straight-on at eye level. A volumetric object whose
flanks differ is shown at a three-quarter angle from slightly above eye level so
the near flank reads with the face. **Side** is always a full profile, square to
the object.

**Flanks.** Image models mix up left and right and ignore "the opposite side".
For a three-quarter view of an object whose flanks differ, and for any
three-view sheet, load [view layouts](references/view-layouts.md) before writing
Composition: it holds the turntable flank rule, the frame-term table, and the
three-view and long-object Composition blocks.

**Layout.** One sheet, one image, with the views placed directly on one
continuous seamless background and separated by empty space only. No boxes,
frames, borders, divider lines, or off-white rectangles behind a view. Say
"view" in the prompt, never "panel", which invites boxed frames.

- two views: front left, back right, in one row
- three views: front, side, back from left to right in one row, in turnaround
  order
- long, low objects (vehicles, long tools): a single row makes each view tiny,
  so put front and back in a top row and the side profile centered beneath them,
  on a square canvas

Every view is drawn at the same scale, the object the same height in each, with
a clear margin of at least 6% of the sheet requested to the canvas edge and the
next view. Width targets cannot all fit a row (widths plus margins can pass 100%),
so ask for equal height. Check scale by height or wheel diameter, never
width: a profile is wider in frame than a three-quarter view at equal scale.

A single `front`, `back`, `side`, `top`, `edge`, or `detail` image is still valid
when a shot needs one specific angle or the user asks for one view only. A
close-up of an identity-critical detail the views cannot resolve is its own
`detail` image, never a fourth view. An existing `hero` three-quarter image stays
a valid reference; do not rename or replace it.

**State variants.** A state variant shows only the views where the state is
visible. Default to front, add back or side where the state change shows, and
reuse the identity descriptor word for word.

**Background.** Pure white seamless, one continuous field across the whole
sheet, with only a faint contact shadow directly beneath each object, so the backdrop does not leak into generated video. Switch
to neutral light gray when the object is white, silver, or chrome, or such parts
make up a large share of its silhouette, or it is clear or translucent and its
silhouette would be lost on white — check the candidate
before choosing — or when the project's approved props or character sheets
already use gray. Gray keeps the same faint contact shadow. Never use a
colored, gradient, textured, or scene background. A transparent delivery asset
is a separate output; never key the white reference into transparency.

**Lighting.** Neutral, even studio light with neutral white balance, identical
across views. Controlled shape-revealing highlights on metal, glass, and gloss
are allowed, as is a gentle raking light to read embossing, engraving, or
texture. No scene mood or color cast.

**One canonical state.** Each image shows one state, stated explicitly: closed
or open, folded or extended, screen off or a specified screen, unlit or
glowing. Default to the state seen most on camera. Every other state needed on
camera gets its own image in the same element folder, reusing the identity
descriptor word for word.

## Flexible prompt structure

Use this order for the sections that apply. Do not add empty boilerplate:

- **References** only when images are provided
- **Task** when the mode needs clarification
- **Subject** for every prop image
- **Setting** for every prop image, because it fixes the background
- **Style** and **Lighting** when they add relevant direction
- **Composition** for every prop image
- **Text in image** only when non-exact model text is expressly accepted
- **Constraints** only for useful quality, continuity, and exclusion requirements

## 1. References (when provided)

List every reference image the user provides, in order:

```text
References:
@Image 1: approved prop sheet or authorized product photo — shape, proportions, materials
@Image 2: style reference — project render style
@Image 3: material or finish reference
```

Rules:
- Omit the References section when no images are provided.
- An approved prop image or authorized product photo is the highest-priority
  identity reference and goes first.
- Bind every reference again where it controls the output: "Use the shape,
  proportions, and paint layout from @Image 1, the render style from @Image 2,
  and the brushed-steel finish from @Image 3." A reference inventory alone is
  not sufficient.
- For a continuity mark on a character's body, see Body continuity marks below.

## 2. Task type

Use **Text-to-Image (T2I)** only when the prompt uses no reference images.

Use **Image-to-Image (I2I)** whenever any reference guides shape, material,
style, state, or another visible property. This includes first-pass sheets built
from photos or concept art, and every state variant of an approved prop.

## 3. Subject

```text
Subject:
[Prop reference of one <object>: silhouette and proportions, real-world size, materials and finish, colors, identity-critical details, wear, canonical state, count. Then each planned face: Front: ... Back: ... Side: ...]
```

Always include:
- **the object and its count** — "one coin only"; for a matched set, the exact
  number and that every item shares one design
- **silhouette and proportions** first, then materials and color
- **real-world size in words** — dimensions or a familiar comparison ("about one
  metre long", "palm-sized", "the size of a thumbnail"); never hands, rulers, or
  other objects in frame for scale
- **the few identity-critical details** the video must reproduce (a knurled grip
  band, a chrome hood ornament, rows of brass pegs); a complex object may need
  more, but each one earns its place. Count repeated features per face ("a front
  door and a separate rear door, each with its own brass handle")
- **wear and age** only as far as the story needs; do not invent damage as a
  realism cue
- **the canonical state**, stated explicitly
- **each planned face described on its own** — "Front: ... Back: ... Side: ...".
  The back is not a mirror of the front: name its identity-critical details
  (rear lights, a stitched seam, an unmarked case back, the stem end) so the
  approved sheet fixes them as canon instead of letting each regeneration
  invent a different one. When the flanks differ, name each flank's features
- **faces told apart by pattern, color, or placement** — blush, crown lean, which
  side a handle sits on — never by damage. Do not pair "unblemished" with a dark
  mark on the same face: a dark mark with no "natural pattern, no scar or spot"
  reads as a blemish
- "the same object in all views, identical design"

Copy the approved descriptor word for word into every later variant and every
prompt that binds the prop.

**Held props** appear without hands, with the grip area and any operated
controls visible.

**Wearables** appear unworn — no person, head, mannequin, or body part — in the
configuration seen on camera: glasses with temples open, a jacket laid flat.

**Surface print.** Unless exact text is required, prefer a blank surface or an
angle that hides the printed area, with soft focus on a deliberately hidden
face. Fine texture standing in for print tends to render as pseudo-letters, so
state "no readable text, letters, or numbers" and check the candidate for marks
that read as writing.

## 4. Setting

```text
Setting:
Isolated on a pure white seamless background that runs continuously across the whole sheet as a flat even field with no floor line, with a faint contact shadow directly beneath each object that does not join the next. No other objects.
```

Gray variant: "Neutral light-gray seamless studio background running continuously
across the whole sheet as a flat even field with no floor line, with a faint
contact shadow directly beneath each object that does not join the next. No
other objects."

## 5. Style

Match the project's approved render style so the prop sits in the same world as
its characters and locations. Pick 2–4 anchors:

- photorealistic product-reference photography, macro or 50mm lens, true
  material micro-texture
- stylized 3D animated-feature prop design, sculpted appealing forms, authored
  materials, not photoreal
- period-authentic production-design reference

For photoreal props, ask for honest material response and real micro-texture
rather than a waxy CGI finish.

## 6. Lighting

```text
Lighting:
Soft, even, neutral studio light, gentle fill, neutral white balance, controlled highlights on [metal/glass], identical across all views.
```

No mood lighting, colored gels, hotspots, or blown highlights. Emissive parts
(screens, LEDs, lamps, magical glow) stay off unless the glowing state is the
canonical one.

## 7. Composition

Two views (default):

```text
Composition:
Two views side by side in one horizontal row on one continuous background, separated by empty space only: left, the whole object in a [front three-quarter / straight-on front] view; right, the same object turned half a revolution on a turntable, in a [rear three-quarter / straight-on back] view. Both views drawn at the same scale, the object the same height in each view, each centered with a clear margin of at least 6% of the sheet on every side; same framing and lighting, deep focus across the object.
```

Single view, only when one angle is requested:

```text
Composition:
Single isolated [front / back / side] view on a continuous background, the whole object centered with a clear margin of at least 6% of the sheet on every side, deep focus across the object.
```

Core rules:
- the whole object fits inside every view — no cropped ends, wheels, handles, or
  straps — with a clear margin to the canvas edge and to the next view
- one object per view, unless the prop is a matched set or the user asks for a
  multi-prop board
- one scale for every view (the object the same height), and each object large enough to
  read its identity details at thumbnail size
- one continuous background: no boxes, frames, borders, divider lines, off-white
  rectangles, labels, or captions; views are identified by the plan, not by text
  or shapes in the image
- three views at most; a third view or a long object uses [view layouts](references/view-layouts.md); a detail close-up is a separate image

## 8. Text in image

Omit by default. When readable copy carries identity (labels, wordmarks, plates,
packaging), use the first route that applies:

1. Acquire the real authorized asset.
2. Generate a text-free base here, then finish the copy deterministically.
   This suits flat, near-frontal surfaces with a blank label area; curved
   packaging or oblique views need the real asset.
3. Only when the user has said model-rendered text is acceptable, quote it in
   double quotes with its surface, size, and color. A conditional or
   hypothetical mention does not count: leave the surface blank and tell the
   caller the option exists.

A fictional identifier the user accepts as model text (a taxi roof number, a
plate) is quoted once and must read identically on every view that shows it.

Never invent a real brand's logo. A device screen the camera shows is a
`screen_` reference: exact UI goes to `html-graphic-render`, invented screen
imagery to `seedream-prompt`.

## 9. Constraints

```text
Constraints:
Quality: sharp material detail, consistent design across all views
Negative: no hands, no people, no other objects, no readable text, no logos, no colored or gradient background, no boxes, frames, borders, or divider lines, no off-white rectangles behind the views, no cropped edges, no extra views, no labels or captions, no watermarks
```

Choose the negatives that apply:
- no hands, people, mannequins, or body parts
- no second object or duplicate
- no colored backdrop, gradient, scene, or floor texture
- no reflections of other objects
- no readable text, letters, numbers, logos, or brand marks
- no cropped object edges
- no boxes, frames, borders, divider lines, or off-white rectangles behind a view
- no extra views, labels, or captions
- no glow, beam, or effect unless canonical
- no watermark

## Standard prompt template

The default two-view sheet. For a third view or a single view, swap in the
matching Composition block above and add the Side line to Subject.

```text
Task:
Text-to-Image (T2I)

Subject:
Prop reference of one [object]: [silhouette and proportions], about [real-world size], [materials and finish], [colors], [2-4 identity-critical details], [canonical state]. One [object] only, the same object in both views, identical design. Front: [front-face details]. Back: [back-face details].

Setting:
Isolated on a pure white seamless background that runs continuously across the whole sheet as a flat even field with no floor line, with a faint contact shadow directly beneath each object that does not join the next. No other objects.

Style:
Photorealistic product-reference photography, 50mm lens, true material micro-texture, not CGI-waxy.

Lighting:
Soft, even, neutral studio light, gentle fill, neutral white balance, controlled highlights on [material], identical across both views.

Composition:
Two views side by side in one horizontal row on one continuous background, separated by empty space only: left, the whole object in a [front three-quarter / straight-on front] view; right, the same object turned half a revolution on a turntable, in a [rear three-quarter / straight-on back] view. Both views drawn at the same scale, the object the same height in each view, each centered with a clear margin of at least 6% of the sheet on every side; same framing and lighting, deep focus across the object.

Constraints:
Quality: sharp material detail, clean silhouette, consistent design across both views
Negative: no hands, no people, no other objects, no readable text, no logos, no colored or gradient background, no boxes, frames, borders, or divider lines, no off-white rectangles behind the views, no cropped edges, no extra views, no labels or captions, no watermarks
```

## Worked examples

Load [worked examples](references/worked-examples.md) when writing a first prompt
of a kind or checking a layout: a photoreal front and back sheet (an apple) and a
stylized three-view vehicle sheet with the stacked long-object layout. Both are
hypothetical patterns without bundled result evidence.

## Body continuity marks

A birthmark, tattoo, or scar that must stay consistent across shots is a
close-up reference, not a prop sheet. Load
[body continuity marks](references/body-continuity-marks.md).

## QA after generation

Inspect every candidate before selection and return defects to the caller:

- the sheet shows the planned views, no more and no fewer, and each view shows
  the face it should: the back is the opposite face, not a repeat of the front,
  and a planned side is a true profile
- flank coverage: when front and back are three-quarter views, they show
  opposite flanks and the side profile matches the front view's flank. Confirm
  each flank by a landmark (door handles, sidecar, hood vent, which side a
  feature sits on), never by assuming the prompt was obeyed
- one scale: object height, roof lamp included, and wheel diameter are within
  about 15% across views; never compare widths
- margin: 3% of the sheet or more to every canvas edge and the next view (models
  typically deliver 55-80% of the requested 6%); nothing touches or is cropped
- one continuous background: no boxes, frames, borders, divider lines,
  off-white rectangles, labels, captions, floor line, or shadow band joining the
  views; the declared color, uniform within about 3 levels (white at or above
  245) and identical in every view
- exactly the requested count; no duplicates, hands, people, or stray objects;
  repeated features (doors, handles, wheels, lamps) match the Subject per face
- the silhouette separates cleanly from a uniform background
- identity-critical details read at thumbnail size
- no invented text, logos, or brand marks; marks that read as letters or
  numerals count as invented text
- scale and proportions are plausible for the stated size
- the state matches the request
- views share one design, scale, and lighting
- the back face carries the details the Subject named for it
- distinguishing marks read as the intended pattern, not damage; a face described
  as unblemished has no dark spot
- a fictional marking such as a plate or roof number reads identically on every
  view that shows it

## Downstream binding

When a Seedance or storyboard prompt binds the approved prop:

- reference only the selected image whose state the shot needs
- a multi-view sheet binds as one identity reference; name the face the shot
  shows ("the back of the [prop]") so the model reads the matching view
- when a shot needs one face alone, generate that single-view image I2I from the
  approved sheet rather than cropping the sheet
- copy the approved descriptor word for word
- for blockout or reference-to-video use, add "Use only the [prop] from
  @Image N — not its background."

## Suggested file targets in this workspace

Save generated images under `projects/<project>/elements/<prop-id>/` beside the
element manifest:

- `prop_<prop-id>_sheet_v<NN>.png` for the front and back sheet, with or without
  the side view
- `prop_<prop-id>_<view>_v<NN>.png` for a single `front`, `back`, `side`, `top`,
  `edge`, or `detail` image
- `prop_<prop-id>_<state>-<view>_v<NN>.png` for a state variant, for example
  `prop_<prop-id>_open-front_v<NN>.png`
- `prompt_prop_<prop-id>_<view>_v<NN>.md` as the exact prompt snapshot beside
  each output, using `sheet` as the view for a multi-view sheet

Record the approved filename as `selected_variant` in the project's element
manifest (`prop.md` or `element.md`, whichever the project already uses), and
note the planned views and the one-line reason beside it. An existing
`prop_<prop-id>_hero_v<NN>.png` keeps its name.
Acquired brand or product files record `generation: none` and have no
`prompt_prop_` snapshot.

## Quick defaults

- Model: `dola-seedream-5-0-pro-260628`
- Format: `png`
- Prompt optimization: `standard`
- Typical size:
  - `2816x1584` for front and back sheets and for three-view single-row sheets
  - `2048x2048` for the stacked long-object sheet and for single views
- Watermark: false where the tool supports it
