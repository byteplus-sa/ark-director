# Frame Break Product Hero

Focused reference for `seedance-frame-break`. Read it when the subject is a
product shown without a person, for example a hero ad whose product breaks the
frame. The technique, the seven prompt blocks and the preflight checklist stay
in [the entrypoint](../SKILL.md); this file replaces the character parts.

- [Rules](#rules)
- [References](#references)
- [Stage design](#stage-design)
- [Product prompt skeleton](#product-prompt-skeleton)
- [Text and end card in post](#text-and-end-card-in-post)
- [Rights and fidelity](#rights-and-fidelity)

## Rules

- One product only, never a pair. State that the output contains exactly one.
- No person, hand or held pose in the frame. The product is the actor.
- The footage is text-free: no captions, taglines, CTAs, end cards or
  watermarks. Add any text in post.
- Real product photos define the product; do not describe the product from
  imagination when photos exist.
- The camera is locked off; the product moves between the far distance and
  close to the lens inside the same three layers (scene, bars, subject on top).
- A photoreal product crosses the bars less often than a drawn subject (observed
  result: 1 to 3 overlap moments), so plan one deliberate crossing per bar.

## References

Use real product photos on plain backgrounds, one view per image, bound in
order. For a shoe:

| Binding | View |
| --- | --- |
| `@Image 1` | Outside profile |
| `@Image 2` | Inside profile |
| `@Image 3` | Sole or top view |

```text
@Image 1 defines the outside profile, @Image 2 the inside profile and @Image 3 the sole of the same single shoe; use them for its shape, colours, materials and proportions only, and ignore their plain backgrounds. All three images define one shoe; the output contains only one shoe, never a pair.
```

Use the views the product actually needs (a bottle needs front and back, not an
inside profile). Several views of one product follow the multiple-views rule in
`seedance-prompt-25`.

## Stage design

The same four stage roles apply with product actions. One coherent motion by
one named part per stage:

| Stage | Product action | End state example |
| --- | --- | --- |
| 1 | The product floats upright inside the window, about two thirds of the window height, slowly turning to show the outside profile | Fully inside the window, clear of both bars |
| 2 | It tips forward; at the peak its toe or leading edge passes over the lower bar's inner edge, covering about a third of the bar's width, drawn complete in full colour, then it tips back | Fully inside the window, nothing over a bar |
| 3 | It tilts up; at the peak its heel, cap or top edge passes over the upper bar's inner edge, covering about a third of the bar's width (own stage), then it levels | Fully inside the window, nothing over a bar |
| 4 | It turns to the hero angle with one last brief extension of one part, then settles | Hero pose fully inside the window, nothing over a bar |

Name the part that crosses in each stage (toe, heel, rim, cap, handle) and
keep that part the actor through the stage. Break-outs are events: the product
sits fully inside the window at the start and at every stage boundary, and only
the named part extends over a bar briefly and returns. No part should fill a
third of the frame, because a subject very close to the lens distorted the bar
edge (observed result). One coherent motion per stage also keeps a second part
from popping in at a different scale.

## Product prompt skeleton

```text
<@Image bindings as above>

A single <product> floats out of the picture toward the viewer, its <crossing part 1> and <crossing part 2> breaking through the black bars. Two fixed black bar graphics lie at the top and bottom of the frame, with perfectly straight horizontal inner edges at the same height in every frame.

0-<t1> seconds: ...  End state: ...
<t1>-<t2> seconds: ...  End state: ...
<t2>-<t3> seconds: ...  End state: ...
<t3>-<t4> seconds: ...  End state: ...

Frame and layer order, back to front: (1) <calm backdrop> fills only the central window, which is the large majority of the frame height; (2) two flat, solid black bars about 12 percent of the frame height each lie at the top and bottom as static 2D graphics laid over the picture, at the same height in every frame, never moving, tilting or bending; (3) the <product> sits fully inside the window and is drawn complete on top of the bars only during the named break-outs, in full colour. Whatever covers a bar sits on top and never changes it; when the product withdraws, the straight edge is simply visible again. The bars are a graphic overlay, not part of the camera's picture.

Camera: locked-off wide-angle camera on a tripod, no movement, no zoom, no cuts; the <product> stays in place and only the extending part grows toward the lens.

Audio: <effects such as <a soft whoosh> and <a light tap>>. No music and no dialogue.

No people or hands; no on-screen text, captions, logos added to the scene or watermarks; the bars stay plain black and unmarked.
```

The backdrop colours must differ from the product's. A teal sole on a teal
backdrop was unreadable (observed result), so pick a calm, darker scene in a
different hue. Read [scenes and subjects](scenes-and-subjects.md).

## Text and end card in post

Keep the generated footage text-free. Render the end card as a deterministic
static graphic with `html-graphic-render` (exact copy, product name, CTA) at the
video's dimensions, then join it to the take with a cross-fade in `ffmpeg`.
Replace the durations (take length `D`, card length `2.5`, fade `0.6`, offset
`D - 0.6`) for your clip:

```bash
ffmpeg -i take.mp4 -loop 1 -t 2.5 -i endcard.png -filter_complex \
  "[0:v]format=yuv420p,fps=24,setsar=1[v0];[1:v]format=yuv420p,fps=24,setsar=1[v1];\
[v0][v1]xfade=transition=fade:duration=0.6:offset=3.4[v];\
[0:a]afade=t=out:st=3.4:d=0.6,apad=whole_dur=5.9[a]" \
  -map "[v]" -map "[a]" -t 5.9 -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -movflags +faststart out.mp4
```

The example values are for a 4 s take; total length is `D + 2.5 - 0.6`. Drop the
audio filter and the `-map "[a]"` when the take has no audio. Text on screen is
never a prompt request. The `ffmpeg` skill owns encode details.

## Rights and fidelity

- Expect logos and printed labels to distort in generated footage. Say so to the
  requester, inspect every frame where the product is close to the lens, and
  place exact logos and wordmarks in the post end card.
- Downloaded brand assets need the user's authorisation; rights stay with the
  user. Acquire official or authorised assets per the
  [element identification contract](../../../contracts/element-identification.md)
  and record the rights decision with the hashes.
- Do not claim a real brand's look is reproduced exactly; the references define
  shape, colour and materials, not pixel-accurate marks.
