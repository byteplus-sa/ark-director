# Recast Grammar

Focused reference for `seedance-motion-recast`. Read [the entrypoint](../SKILL.md)
for mode selection, gates and caller responsibilities.

- [Authority split](#authority-split)
- [Core template](#core-template)
- [Mapping syntax](#mapping-syntax)
- [Plan B: full-frame edit variant](#plan-b-full-frame-edit-variant)
- [Worked example: two dancers, new cast, new location](#worked-example-two-dancers-new-cast-new-location)

## Authority split

State authority by attribute. Each input owns only what is listed for it.

| Input | Owns | Supplies none of |
| --- | --- | --- |
| `@Video 1` source clip | Body motion, pose sequence, screen positions, camera path, framing changes, hard cuts, timing | People, faces, hair, clothing, props, products, location, colors, grade, text |
| Character `@Image N` | Identity, hair, build, wardrobe shown on that view | Pose, background, panel layout, lighting of the sheet |
| Product or prop `@Image N` | Shape, materials, color, markings | Hands, table, background |
| Location `@Image N` | Layout, materials, light direction, time of day | People or vehicles in the image |
| `@Audio 1` (optional) | The route named in the Audio block | Anything visual |
| Text | Style, guards, dispositions, end states | Motion already defined by `@Video 1` |

Inherit, do not restate. The source already defines the motion, so describe
motion in text only to name who does what (the descriptor) or to fix a known
failure. Retelling every move can conflict with the reference video.

## Core template

```text
[Recast Goal]
Rebuild @Video 1 with a new cast and world. Keep its motion; replace its
appearance.

[Motion Authority]
@Video 1 defines only body motion, pose sequence, screen positions, camera path,
framing changes, hard cuts, and timing. Use none of its people, faces, clothing,
props, location, colors, or on-screen text.

[Subject Mapping]
<descriptor of source subject 1> becomes <Name 1>: @Image 1 (front) and
@Image 2 (profile) define <Name 1>'s face, hair, build, and outfit.
<descriptor of source subject 2> becomes <Name 2>: @Image 3 defines ...
<descriptor of source subject 3> is removed; the space they occupied shows
<location detail>.
<descriptor of source group> remain as background extras dressed for <new world>.
<source object descriptor> becomes <Product>: @Image 5 defines its shape,
materials, and markings.
@Image 6 defines the location: <layout, materials, light direction, time>.

[Guards]
Each new character wears only the outfit in their reference.
Exactly <N> people appear in every shot; <per-cut presence if it varies>.
<Name 1> and <Name 2> keep their own faces and outfits through every turn,
crossing, and cut.
<residual-original guard for replaced objects>.

[Style]
<preset fragment or free text, in lighting -> lens -> grade -> sensor order>

[Audio]
<route sentence from the audio reference>
```

Rules for the blocks:

- **Recast Goal** is one or two sentences. It names the whole-frame rebuild.
- **Motion Authority** always lists both what the video supplies and that its
  appearance is excluded. This is the one necessary exclusion in every recast.
- **Subject Mapping** has one line per disposition, in the order subjects first
  appear. Group multiple views of one subject on one line.
- **Guards** hold observable counts and ownership, not a list of fears. Pick
  from the guard catalog only for risks present in this source.
- **Style** never contradicts the location or character references. If the
  preset changes the medium, it applies to every mapped element.
- **Audio** is always present, even when it says the clip is music-only or that
  audio is added in post.

## Mapping syntax

A mapping line has three parts: **descriptor → name → reference role**.

```text
The dancer on the left in the red windbreaker who starts the arm wave becomes
Mara: @Image 1 (front) and @Image 2 (left profile) define Mara's face, hair,
build, and outfit.
```

- The descriptor is observable in the source: screen position, clothing,
  action. Never a real name, and never inferred identity.
- The name is a neutral production label for the new character, used in every
  later block and cut.
- Each image states which view it is and which attributes it defines.
- Products and props belong to a named character when they are held:
  `The phone in Mara's right hand becomes the Lumen X phone from @Image 5.`
- For a subject map, append the ID in review metadata rather than in the prompt
  (`subj-01 -> Mara`), so the prompt stays readable.

Do not write "@Images 1 through 4 define the four dancers." It never says which
image maps to which dancer.

## Plan B: full-frame edit variant

Use this only if the verification probe shows R2V keeps source appearance. Edit
mode treats `@Video 1` as the editing master, locks duration and aspect ratio
to the source, and prefers 1–5 reference images.

```text
[Edit Goal]
Edit @Video 1. Replace all subjects and the environment across the entire
video, following the subject mapping below. Keep the motion and camera.

[Source Video Role]
@Video 1 is the sole editing master for body motion, pose sequence, screen
positions, camera path, framing changes, hard cuts, occlusion order, and timing.
Use none of its people, faces, clothing, props, location, colors, or on-screen
text.

[Subject Mapping]
<same mapping lines as the core template>

[Guards]
<same guard lines as the core template>

[Edit Scope]
Replace every person's face, hair, build, and clothing as mapped, every mapped
object, and the whole location. The entire video contains exactly <N> people.

[Timeline Inheritance]
Each new character inherits every appearance, movement, occlusion, and exit of
the source subject mapped to them, including timing, path, and speed changes.

[Style]
<preset fragment>

[Audio]
<route sentence>
```

The scope sentence "replace all subjects and the environment" is never used
alone; the mapping lines still give every subject its disposition.

## Worked example: two dancers, new cast, new location

Hypothetical example; no result evidence is attached.

Source: 8.0 s, 9:16, 30 fps, one continuous shot with a slow push-in and a
half orbit to the right at about 0:05. Two dancers on a concrete parking-garage
rooftop at dusk. Screen-left: red windbreaker, white sneakers, starts an arm
wave. Screen-right: black hoodie, grey cap, mirrors the wave, then both spin at
about 0:04. No other people. Source audio: a pop track, no dialogue.

Targets (all approved, hashed):

| Binding | Element | View |
| --- | --- | --- |
| `@Video 1` | source clip | motion only |
| `@Image 1` | `char-mara` | front |
| `@Image 2` | `char-mara` | left profile |
| `@Image 3` | `char-theo` | front |
| `@Image 4` | `char-theo` | right profile |
| `@Image 5` | `loc-night-market` | wide establishing view |
| `@Audio 1` | separated source music track | soundtrack |

Dispositions: screen-left dancer → Mara; screen-right dancer → Theo; rooftop
cars and railings → replaced by the market location. Count: two subjects, five
images; within the recommended range.

```text
[Recast Goal]
Rebuild @Video 1 with a new cast and world. Keep its motion; replace its
appearance.

[Motion Authority]
@Video 1 defines only body motion, pose sequence, screen positions, the slow
push-in, the half orbit to the right, and timing. Use none of its people,
faces, clothing, rooftop, cars, colors, or sky.

[Subject Mapping]
The dancer on the left in the red windbreaker who starts the arm wave becomes
Mara: @Image 1 (front) and @Image 2 (left profile) define Mara's face, braided
hair, build, and cropped olive jacket with wide cargo trousers.
The dancer on the right in the black hoodie and grey cap who mirrors the wave
becomes Theo: @Image 3 (front) and @Image 4 (right profile) define Theo's face,
short curls, build, and cream knit vest over a white shirt.
@Image 5 defines the location: a narrow night market street, wet stone paving,
food stalls on both sides with warm string lights, steam drifting from a
noodle stall, key light from warm lamps screen-left. Use none of the people in
@Image 5.

[Guards]
Mara and Theo each wear only the outfit in their own references; no cap, hood,
or windbreaker appears. Exactly two people appear in every frame; the stalls
are unattended. The output contains only one Mara and only one Theo
throughout. Mara stays screen-left and Theo screen-right until the spin,
and each keeps their own face and outfit through the spin and the orbit. Stall
signs show abstract shapes and color only.

[Style]
The visuals feature warm practical light from the string lights with cool
blue fill from the sky, reflections on the wet paving, a gentle teal-and-amber
grade, and fine digital grain.

[Audio]
@Audio 1 is the soundtrack from the source; keep it unchanged and on the same
beat. Add soft market ambience under it: <sizzling woks>, distant chatter.
```

Parameters for the first ladder rung: default R2V route,
`omni_reference_task_type: auto`, `resolution: 480p`, `ratio: 9:16`,
`duration` set to the key beat trimmed from the source (for example the
0:03–0:08 spin and orbit, 5 s), `generate_audio: true`, `watermark: false`.
The probe binds the trimmed beat as `@Video 1` and the same 0:03–0:08 window
of the separated music as `@Audio 1`, each with its own hash.
