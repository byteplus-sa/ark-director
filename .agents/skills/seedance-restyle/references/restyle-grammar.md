# Restyle Grammar

Focused reference for `seedance-restyle`. Read [the entrypoint](../SKILL.md) for
routing, rules and caller responsibilities.

- [Authority split](#authority-split)
- [Route A: full-frame edit](#route-a-full-frame-edit)
- [Route B: reference](#route-b-reference)
- [A different place, only when requested](#a-different-place-only-when-requested)
- [Style reference images](#style-reference-images)
- [Identity anchors](#identity-anchors)
- [Worked example: terrace clip to claymation](#worked-example-terrace-clip-to-claymation)

## Authority split

| Input | Owns | Supplies none of |
| --- | --- | --- |
| `@Video 1` muted master | Subjects and their count, their screen positions, actions, poses, props, the furniture they use, camera path, cuts, timing, and which place the scene is in | Rendering medium, surface texture, grade |
| Optional environment `@Image N` | How the same place looks in the target medium | People, a different place, changed source geometry, props the shot lacks |
| Style `@Image N` | Medium, palette, line quality, texture, light quality | Subjects, layout, characters, text |
| Identity anchor `@Image N` | One character's design in the target medium | Pose, background, lighting of the sheet |
| Text | The style block, content inventory, guards | Motion already in `@Video 1` |

Describe content only as an inventory that pins who and what must survive.
Retelling every move conflicts with the video.

**The place stays the same.** Restyle the background through an explicit medium
lock. Add an environment image only when selected for the current input,
request or observed failure, with approval; honor no-image requests. It never
overrides source geometry, parallax or timing. Templates below omit absent
roles and number only the actual bindings.

## Route A: full-frame edit

```text
[Edit Goal]
Edit @Video 1. Redraw <people>, <props> and <the source's background surfaces>
in <style name>. Keep every subject, action, prop, layout, camera and timing
from @Video 1.

[Source Video Role]
@Video 1 is the sole editing master. It defines <subject inventory>, <key
props>, <the furniture the subject uses>, <source camera path>, <their> poses and
actions, and event order.

[Environment Reference Role] (omit unless an environment image is selected)
@Image <N> guides the environment's rendering: <the source's place in the target
medium: city, buildings, furniture, plants>. Use it for <street, buildings,
sky, bench, shrub, table surface>. Use no person from it. Do not use its <extra
objects it holds>. Keep geometry and parallax from @Video 1.
The only objects on <surface> are <the source's objects>, one
of each, never a second or duplicated copy.

[Edit Scope]
Redraw <each background element> in <medium>, in the same positions as the
source. <Subject>, <wardrobe
and accessories> and <props> are also rendered in <medium>. Exactly <N> people
appear in the foreground; <background extras>. <Source text surface> shows
<abstract shapes>; no lettering appears anywhere.

[Timeline Inheritance]
Every pose, gesture and contact keeps the timing and screen position of
@Video 1: <beats with times>. <Cadence note for stepped styles.>

[Content to Preserve]
Keep <identity cues>, <props>, <furniture position>, <source camera path> and the
whole performance from @Video 1.

[Style]
<catalog fragment or custom recipe>

[Audio]
Silent output. Sound is added in post.
```

Optional blocks, added before `[Edit Scope]`:

```text
[Style Reference Role]          (only with style images)
@Image <N> defines only the visual style: <medium, palette, line, texture,
light quality>. Use none of its subjects, layout or characters.

[Identity Anchors]              (only with anchors)
@Image <N> defines <Name>'s design in <style>: <hair shape, wardrobe colours>.
<Name> is <observable descriptor in @Video 1>.
```

## Route B: reference

Use only when currently supported and justified by the request or reviewed
output. Preserve source duration and ratio. Any trim, padding or retiming needs
current capability evidence and approval for a separate derivative; never
overwrite the original or assume an 8n+1 recipe guarantees returned timing.

```text
Create a new video using @Video 1 as the strict visual and temporal reference.
Follow the output dimensions and duration selected in the generation settings.

[Timeline fidelity: highest priority]
Each output moment corresponds to the same moment in @Video 1 at the same
playback speed, from the first frame to the last. Keep <source camera path>, the
screen positions, and every pose, gesture and contact in the same order and at
the same time as in @Video 1.

[Reference content]
@Video 1 defines content, identity cues, wardrobe, place, geometry, motion,
timing, screen positions and camera. Redraw these in the chosen medium rather
than retaining photographic surfaces.
- 0:00 to 0:NN: <what happens>
- 0:NN to 0:NN: <what happens>

[World]
<The source's place> is rendered in <medium> in the same layout. The only
objects on <surface> are <the source's objects>, one of each. Add the optional
Environment Reference Role only when an image is selected.

[Characters and props]
<The subject> is a <medium> figure with <hair>, <accessories>, <wardrobe>, and a
hand-modelled face. <Props> are <medium>. Exactly <N> people appear in the
foreground; <background extras>. No lettering appears anywhere.

[Style]
<catalog fragment or custom recipe>

[Audio]
Silent output. Sound is added in post.
```

## A different place, only when requested

When the user explicitly asks for a different location, add this block. Use it
only on request, never to restyle the background of the same scene:

```text
[Location Change]
The background and the overall location both change. <The source's street,
buildings, plant, bench and sky> of @Video 1 are all removed, and no part of the
original <location> remains. In their place is a different location: <the new
place in the target medium, left to right and near to far>. Every part of the
new location is modelled <medium>.
```

## Style reference images

- One to three images, user-owned or approved generated frames, each with
  SHA-256. One image per frame; no collage or mood board.
- Prefer frames whose content differs from the source, so the model reads them
  as style rather than layout.
- No people's faces in style images; when a style image needs a character,
  use an identity anchor instead.
- Never use frames from copyrighted productions or name a studio, artist or
  franchise.
- When the style images and the catalog fragment disagree, the images win;
  shorten the fragment to the medium only.

## Identity anchors

Restyle keeps identity as shapes and colours. For a recurring character that
must look the same across takes:

1. Design the character in the target medium with Seedream and approve it.
2. Register the approved views as a Virtual Portrait subject named for the
   medium (`"Mara (claymation)"`), per the
   [video-to-video inputs contract](../../../contracts/video-to-video-inputs.md).
3. Bind it after the style images and map it to the source subject by
   observable descriptor.

A single-take restyle without recurring characters needs no anchors.

## Worked example: terrace clip to claymation

Hypothetical prompt example, not a production result. Assume current edit
support, authorized source footage and an explicitly requested, approved
same-place environment image. The example image is optional in other requests.
Keep the original source and use a muted derivative without frame adaptation.

Source: a 5 s, 16:9 locked-off clip. A woman with shoulder-length dark hair, a
navy jacket over a cream top and a small gold hoop earring sits at a small round
café table with a Paris street, a green plant and a wooden bench behind her.
She holds a red can in her right hand beside a white espresso cup, lifts it to
her lips at about 0:01, drinks until about 0:03, and sets it down by about
0:04.5. These are fictional source facts, not measured evidence.
Post-audio route: authorized original.

Environment image (Seedream text-to-image, 2048x1152, empty set, same place):

```text
Task:
Text-to-Image (T2I)

Subject:
Empty plasticine claymation miniature set of a Parisian café terrace seen from a fixed medium-distance camera: a small round café table with a thin brass rim in the lower-left foreground with one white espresso cup on it, a long curved wooden café bench behind the table, a potted green shrub pressed from clay leaves at the right edge, and a street of cream-coloured stone buildings with balconies, windows and shop fronts receding behind. Shop signs are coloured clay shapes. The set holds no people and no cans.

Style:
Handmade plasticine claymation: every surface, including the street, buildings, sky, shrub, bench and table, is modelled clay with visible thumbprints, fingerprint ridges and tool marks, a matte clay sheen and slightly uneven hand-shaped edges.

Lighting:
Soft warm daylight key from frame left with gentle shadows, like a small tabletop set.

Composition:
Wide 16:9 frame matching a locked-off medium shot: table in the lower left, shrub at the right edge, street receding behind, pale clay sky above.

Constraints:
Quality: crisp sculpted clay detail
Negative: no people, no photograph, no live-action look, no readable text, no logos, no watermarks
```

Edit prompt, with the image bound as `@Image 1`:

```text
[Edit Goal]
Edit @Video 1. Replace the scene with the claymation café terrace from @Image 1, and restyle the woman and her props as plasticine claymation. Keep every subject, action, prop, set layout, camera and timing from @Video 1.

[Source Video Role]
@Video 1 is the sole editing master. It defines the woman with shoulder-length dark hair in a navy jacket over a cream top, the red aluminium can in her right hand, the white espresso cup, the small round café table, the static camera, her poses and actions, and event order.

[Environment Reference Role]
@Image 1 guides the plasticine rendering of the terrace, bench, shrub, street and table. Keep their geometry and camera parallax from @Video 1. Use no people or extra objects from the image. The only objects on the table are the white espresso cup and red can from @Video 1, one of each.

[Edit Scope]
Replace the scene with @Image 1: the street, the buildings, the sky, the wooden bench, the shrub and the table are the modelled clay of @Image 1, with visible thumbprints and tool marks, in the same positions as the source. The woman, her navy jacket and cream top, her small gold hoop earring, the red can and the white espresso cup are also modelled in plasticine. One person appears in the foreground; the distant passers-by stay as tiny blurred clay figures. No lettering appears anywhere, including on the can.

[Timeline Inheritance]
Every pose, gesture and contact keeps the timing and screen position of @Video 1: the can held at the start, lifted to her lips at about 0:01, drunk from until about 0:03, and set on the table by about 0:04.5. A slightly stepped stop-motion cadence still hits each of those poses on the beat.

[Content to Preserve]
Keep her identity cues, the can, the cup, the table position, the static camera and the whole performance from @Video 1.

[Style]
Plasticine claymation throughout: visible thumbprints, fingerprint ridges and tool marks, a matte clay sheen, soft warm key light on a small tabletop set, and slightly stepped stop-motion cadence.

[Audio]
Silent output. Sound is added in post.
```

Parameters: `omni_reference_task_type: edit`, `generate_audio: false`,
`resolution: "480p"`, boolean `draft: true`, `watermark: false`;
`ratio` and `duration` omitted.

Review target, not a claimed result: all requested surfaces take the clay
medium while source place, geometry, performance and timing remain intact.
Measure returned duration and frame timestamps; neither this image nor a
frame-count recipe guarantees fidelity. After picture QA, mux the saved
authorized audio and inspect sync. A different route needs its own capability
check and review.
