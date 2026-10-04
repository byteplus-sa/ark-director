# Restyle Grammar

Focused reference for `seedance-restyle`. Read [the entrypoint](../SKILL.md) for
routing, rules and caller responsibilities.

- [Authority split](#authority-split)
- [Route A: full-frame edit](#route-a-full-frame-edit)
- [Route B: reference](#route-b-reference)
- [Style reference images](#style-reference-images)
- [Identity anchors](#identity-anchors)
- [Worked example: skateboard clip to claymation](#worked-example-skateboard-clip-to-claymation)

## Authority split

| Input | Owns | Supplies none of |
| --- | --- | --- |
| `@Video 1` muted master | Subjects and their count, screen positions, actions, poses, props, set layout, camera path, cuts, timing | Rendering medium, surface texture, grade |
| Style `@Image N` | Medium, palette, line quality, texture, light quality | Subjects, layout, characters, text |
| Identity anchor `@Image N` | One character's design in the target medium | Pose, background, lighting of the sheet |
| Text | The style block, content inventory, guards | Motion already in `@Video 1` |

Describe content only as an inventory that pins who and what must survive.
Retelling every move conflicts with the video.

## Route A: full-frame edit

```text
[Edit Goal]
Edit @Video 1. Replace the scene with the <style name> <environment> from
@Image 1, and restyle <the people and props> as <style name>. Keep every
subject, action, prop, set layout, camera movement, cut and timing.

[Source Video Role]
@Video 1 is the sole editing master. It defines <subject inventory>, their
positions, poses and actions, <key props>, <set layout>, the camera path, cuts
and event order.

[Environment Reference Role]    (the lever for a whole-frame restyle)
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

[Edit Scope]
Replace the scene with @Image 1: <each background element> is the modelled
<medium> of @Image 1, in the same positions as the source. Redraw every person,
object, surface, sky and effect in <style>; nothing remains photographic. Exactly <N> people appear, as in @Video 1. Each person
keeps <identity cues> as recognizable shapes and colours. <Source text
surface> shows <abstract shapes in the style>; no lettering appears.

[Timeline Inheritance]
Every pose, gesture, contact and exit keeps the timing and screen position of
@Video 1. <Cadence note for stepped styles.>

[Style]
<catalog fragment or custom recipe>

[Audio]
Silent output. Sound is added in post.
```

## Route B: reference

Use when a Route A probe keeps photographic pixels. Set `duration` to the
whole-second source length and `ratio` to the source.

```text
[Restyle Goal]
Recreate @Video 1 shot for shot in <style name>.

[Structure Authority]
@Video 1 defines only composition, subject positions, poses, actions, camera
path, framing changes, hard cuts and timing. Use none of its photographic
surfaces, textures or grade.

[Content Inventory]
<One line per subject: observable descriptor, identity cues, action.>
<Key props and set layout.>

[Style Reference Role]          (only with style images)
@Image 1 defines only the visual style: <...>. Use none of its subjects,
layout or characters.

[Guards]
Exactly <N> people appear in every shot; <per-cut presence if it varies>.
<Text surfaces> show abstract shapes only.

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

## Worked example: skateboard clip to claymation

Hypothetical example; no result evidence is attached.

Source: an owned 6 s, 16:9 handheld clip. A skateboarder in a yellow hoodie
and red cap rolls from frame left across a concrete plaza, ollies a low ledge
at about 0:03 and lands toward frame right. A parked bicycle stands at
background right. One cut at 0:04 to a low angle of the landing. A shop sign
reads in the background. Rights: owned. Route A probe, catalog
`plasticine-claymation`, no style images or anchors. Post-audio route: original.

```text
[Edit Goal]
Edit @Video 1. Restyle the entire video as plasticine claymation. Keep every
subject, action, prop, set layout, camera movement, cut and timing.

[Source Video Role]
@Video 1 is the sole editing master. It defines the skateboarder in the yellow
hoodie and red cap, the board, the low ledge, the parked bicycle at background
right, the plaza layout, the handheld follow, the cut at 0:04 and event order.

[Edit Scope]
Redraw every person, object, surface and sky in plasticine; nothing remains
photographic. Exactly one person appears. The skateboarder keeps a yellow
hoodie and red cap. The shop sign shows coloured clay shapes; no lettering
appears.

[Timeline Inheritance]
The roll, the ollie at about 0:03 and the landing toward frame right keep the
timing and screen positions of @Video 1. Stepped stop-motion cadence still
hits the take-off and landing poses on the beat.

[Style]
The visuals feature plasticine characters and set with visible thumbprints and
tool marks, soft key light on a small tabletop set, and slightly stepped
stop-motion cadence.

[Audio]
Silent output. Sound is added in post.
```

Parameters for the probe: `omni_reference_task_type: edit`, `@Video 1` the
muted 0:02–0:06 span holding the ollie and the cut, `generate_audio: false`,
`resolution: 480p`, `watermark: false`. After QA, mux the saved source audio
so the landing sound hits the landing frame.
