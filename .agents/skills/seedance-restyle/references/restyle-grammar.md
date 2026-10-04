# Restyle Grammar

Focused reference for `seedance-restyle`. Read [the entrypoint](../SKILL.md) for
routing, rules and caller responsibilities.

- [Authority split](#authority-split)
- [Route A: full-frame edit](#route-a-full-frame-edit)
- [Route B: reference](#route-b-reference)
- [Style reference images](#style-reference-images)
- [Identity anchors](#identity-anchors)
- [Worked example: terrace clip to claymation](#worked-example-terrace-clip-to-claymation)

## Authority split

| Input | Owns | Supplies none of |
| --- | --- | --- |
| `@Video 1` muted master | Subjects and their count, their screen positions, actions, poses, props, the furniture they use, camera path, cuts, timing | Rendering medium, surface texture, grade, and the background when a Location Change is stated |
| Location Change text | The new place, described in the target medium | Motion already in `@Video 1` |
| Style `@Image N` | Medium, palette, line quality, texture, light quality | Subjects, layout, characters, text |
| Identity anchor `@Image N` | One character's design in the target medium | Pose, background, lighting of the sheet |
| Text | The style block, content inventory, guards | Motion already in `@Video 1` |

Describe content only as an inventory that pins who and what must survive.
Retelling every move conflicts with the video.

**Keep positions only for the subject and the furniture they use.** A prompt
that both replaces the scene and says "same positions" or "same layout" for the
background makes the model keep the source plate: five such runs left the street
photographic. State the location change instead.

## Route A: full-frame edit

```text
[Edit Goal]
Edit @Video 1. Change the whole location and background, and restyle everything
as <style name>. <The subject> keeps <their> performance, and the location
around <them> changes completely.

[Source Video Role]
@Video 1 is the sole editing master. It defines <subject inventory>, <key
props>, <the furniture the subject uses>, the camera, <their> poses and
actions, and event order.

[Location Change]
The background and the overall location both change. <The source's street,
buildings, plant, bench and sky> of @Video 1 are all removed, and no part of the
original <location> remains. In their place is a different location: <the new
place in the target medium, left to right and near to far>. Every part of the
new location is modelled <medium>.

[Edit Scope]
<Subject>, <wardrobe and accessories>, <props> and <the furniture they use> are
rendered in <medium> and stay in the same place in the frame. Exactly <N> people
appear in the foreground; <background extras>. The only objects on <surface> are
<the source's objects>, one of each, never a second or duplicated copy. <Source
text surface> shows <abstract shapes>; no lettering appears anywhere.

[Timeline Inheritance]
Every pose, gesture and contact keeps the timing and screen position of
@Video 1: <beats with times>. <Cadence note for stepped styles.>

[Content to Preserve]
Keep <identity cues>, <props>, <furniture position>, the camera and the whole
performance from @Video 1.

[Style]
<catalog fragment or custom recipe>

[Audio]
Silent output. Sound is added in post.
```

Optional blocks, added before `[Edit Scope]`:

```text
[Environment Reference Role]    (only with an environment image)
@Image 1 defines the whole environment: <what it shows, in the target medium>.
Use it for <street, buildings, sky, furniture>. Use no person from it. Do not
use its <extra objects it holds>. The only objects on the table are <the
source's objects>, one of each, never a second or duplicated copy.

[Style Reference Role]          (only with style images)
@Image 1 defines only the visual style: <medium, palette, line, texture,
light quality>. Use none of its subjects, layout or characters.

[Identity Anchors]              (only with anchors)
@Image 2 defines <Name>'s design in <style>: <hair shape, wardrobe colours>.
<Name> is <observable descriptor in @Video 1>.
```

With an environment image, the Edit Goal says "Replace the scene with the <style
name> <environment> from @Image 1" and the Location Change block can be dropped.

To restyle the source's own location (the same street) instead of a new place,
describe that street in the target medium inside the Location Change block and
keep the "remove the original" wording. This variant is untested.

## Route B: reference

Use when a Route A probe keeps photographic pixels or the duration must be
exact. Set `duration` to the whole-second source length and `ratio` to the
source.

```text
Create a new video using @Video 1 as the strict visual and temporal reference.
Follow the output dimensions and duration selected in the generation settings.

[Timeline fidelity: highest priority]
Each output moment corresponds to the same moment in @Video 1 at the same
playback speed, from the first frame to the last. Keep the static camera,
<the subject's> screen position, and every pose, gesture and contact in the same
order and at the same time as in @Video 1.

[Reference content]
@Video 1 defines only the motion, timing, <the subject's> screen position and the
camera. Use none of its photographic surfaces, faces, wardrobe or location.
- 0:00 to 0:NN: <what happens>
- 0:NN to 0:NN: <what happens>

[World]
The location is completely different from @Video 1, and the background changes
with it. <The source's street, buildings, plant, bench and sky> are gone, and
nothing of the original <location> remains. The whole world is a miniature
<medium> <new place>: <description>. Everything is modelled <medium>. The only
objects on <surface> are <the source's objects>, one of each, never a second or
duplicated copy.

[Characters and props]
<The subject> is a <medium> figure with <hair>, <accessories>, <wardrobe>, and a
hand-modelled face. <Props> are <medium>. Exactly <N> people appear in the
foreground; <background extras>. No lettering appears anywhere.

[Style]
<catalog fragment or custom recipe>

[Audio]
Silent output. Sound is added in post.
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

Verified on 2026-10-04, edit route, 480p, 121-frame muted source bound as an
`asset://` video, no images.

Source: a 5 s, 16:9 locked-off clip. A woman with shoulder-length dark hair, a
navy jacket over a cream top and a small gold hoop earring sits at a small round
café table with a Paris street, a green plant and a wooden bench behind her.
She holds a red can in her right hand beside a white espresso cup, lifts it to
her lips at about 0:01, drinks until about 0:03, and sets it down by about
0:04.5. Rights: generated by the project. Post-audio route: original.

```text
[Edit Goal]
Edit @Video 1. Change the whole location and background, and restyle everything as plasticine claymation. The woman keeps her performance, and the location around her changes completely.

[Source Video Role]
@Video 1 is the sole editing master. It defines the woman with shoulder-length dark hair in a navy jacket over a cream top, the red aluminium can in her right hand, the white espresso cup, the small round café table in front of her, the static camera, her poses and actions, and event order.

[Location Change]
The background and the overall location both change. The Paris street, its buildings, the green plant, the wooden bench and the sky of @Video 1 are all removed, and no part of the original street remains. In their place is a different location: a plasticine seaside village café terrace. A curved wooden bench stands behind the table. White-washed clay cottages with blue shutters climb a hillside on the left. A clay harbour with small clay fishing boats and gently rippled clay water fills the right side. A pale clay sky with soft clay clouds is above. Every part of the new location is modelled clay with visible thumbprints and tool marks.

[Edit Scope]
The woman, her navy jacket and cream top, her small gold hoop earring, the red can, the white espresso cup and the round café table are modelled in plasticine and stay in the same place in the frame. One person appears in the foreground; a few tiny blurred clay figures stand far down the quay. The only objects on the table are the white espresso cup and the red can from @Video 1, one of each, never a second or duplicated copy. No lettering appears anywhere, including on the can.

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
`resolution: 480p`, `watermark: false`; `ratio` and `duration` omitted.

Result: the whole frame became clay (white-washed cottages, harbour, boats,
water, sky) while the woman, table, can and cup kept their place, motion and
timing; 121 frames in, 121 out. The same request on the reference route
returned the same kind of result. Earlier prompts that said "in the same
positions as the source" or "same layout as @Video 1" for the background left
the street photographic. After QA, mux the saved source audio.
