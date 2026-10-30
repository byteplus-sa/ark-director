# Worked Examples

Focused reference for `seedance-prompt-25`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

These examples are **hypothetical**: they model the current prompt practice and
have no linked generated result. Request parameters are listed beside each
prompt because they never go inside it.

- [Three-shot R2V sequence with dialogue](#three-shot-r2v-sequence-with-dialogue)
- [Ambient-only one-take](#ambient-only-one-take)
- [Video editing — subject replacement](#video-editing--subject-replacement)

## Three-shot R2V sequence with dialogue

One sequence of a longer spot, generated on its own and assembled with the
others. It shows bindings, declared light sources, ordered action plus camera, lens
intent and light per shot, a pinned count, a frame-side hand, a plain prop
surface and a budgeted line.

Request parameters: `duration: 11`, `ratio: "16:9"`, `draft: true`,
`generate_audio: true`, `watermark: false`.

```text
@Image 1 defines the baker: appearance, hairstyle and clothing only. @Image 2
defines the customer: appearance, hairstyle and clothing only. @Image 3 defines
the bakery: counter, shelves and front window; do not use any people in it.
Facing the counter, the front window is at frame-left. The bakery has two light
sources: low morning sun through the window and warm pendant lamps over the
counter.

Shot 1 (0-3 s): wide shot, low angle from behind the glass display case, the
nearest pastries soft in the foreground; slow push-in toward the counter. The
baker slides an open, plain white cardboard box, smooth surface with nothing
printed, across the counter with both hands. Inside are three pastries in open
view: two croissants at the front, one pain au chocolat behind them. Light:
window sun from frame-left, long shadows across the counter.

Shot 2 (3-6.5 s): medium close-up over the baker's shoulder, eye level, shallow
depth of field with the shelves soft; static hold. The customer lifts the front
croissant with her right hand, frame-left, and her eyebrows rise as she smells
it. One croissant and the pain au chocolat stay in the box. Light: warm pendant
top light, with a window-sun rim on her cheek from frame-left.

Shot 3 (6.5-11 s): reverse close-up of the baker from the customer's side,
slight high angle; slow drift right. The baker leans one hand on the counter,
smiles, and speaks. The reverse angle puts the window at frame-right. Light:
window sun from frame-right, pendant fill keeping her face readable.

Dialogue language: English. The baker says in warm, conversational English:
{Still warm. Enjoy them.}
Audio includes <cardboard sliding on the counter>, soft street ambience through
the window, and the baker's line.
```

Why it is built this way:

- Each shot changes size family, angle and move from its neighbour, and every
  light fact names one of the two declared sources.
- The pastries are counted, positioned and in view from the first frame, and
  the count is restated after one is lifted.
- The four-word line needs about 1.8 s of speech plus a late start, so it sits
  in a 4.5 s shot and ends well before the clip end.
- No ratio, duration or resolution appears in the prompt text.

## Ambient-only one-take

This example explicitly assigns the sound bed to Seed Audio in post, so it uses
picture-only generation. Ambient-only does not itself require this route:
requested native ambience stays native where supported. A "no music, no voices"
line is not a guarantee; either route needs listening verification.

Request parameters: `duration: 8`, `ratio: "21:9"`, `draft: true`,
`generate_audio: false`. Post: forest ambience bed from Seed Audio, recorded as
not frame-synced.

```text
One continuous take with no cuts. The camera starts low among ferns, three
fronds framing the lower third of the frame, and cranes up slowly over the whole
clip to reveal a pine valley filled with morning mist. A single grey heron
stands in the shallow river at frame-right and lifts off once, at about 5 s,
flying toward frame-left. Light: low sun from frame-right behind the far ridge,
pale shafts cutting through the mist and backlighting the heron's wings.
```

## Video editing — subject replacement

```text
[Edit Goal]
Edit @Video 1. Replace only the yellow folding desk lamp with the white folding desk lamp in @Image 1.

[Source Video Role]
@Video 1 is the sole editing master. It defines the desk, books, hand movements, camera position,
camera movement, occlusion relationships, and event order.

[Target Reference Role]
@Image 1 defines only the white folding desk lamp's appearance, structure, and material. Do not use
the image's background, composition, or other objects.

[Edit Scope]
Keep exactly one white folding desk lamp throughout the video. Replace only the original yellow
folding desk lamp. Do not modify the books, desk, hands, or background.

[Timeline Inheritance]
The white folding desk lamp inherits every appearance, lamp-arm rotation, hand occlusion, and exit
of the original yellow folding desk lamp, including timing, path, and speed changes.
Except for the object or area explicitly modified above, keep all other people, props, scene
content, camera movements, cuts, and event order from @Video 1 unchanged.
```

Request parameters: ratio and duration follow the source; `generate_audio:
false` with the source's own audio restored in post.
