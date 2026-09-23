# Object Swap

Focused reference for `seedance-vfx-prompt`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities, and
[Seedance 2.5 editing](seedance-25-edit.md) for the shared edit structure and
guardrails.

- [Scope and boundary](#scope-and-boundary)
- [Swap contract](#swap-contract)
- [Using a subject map](#using-a-subject-map)
- [Contact and occlusion](#contact-and-occlusion)
- [Templates](#templates)
- [Worked example: hand-held can to product](#worked-example-hand-held-can-to-product)
- [Swap QA](#swap-qa)

## Scope and boundary

Object Swap replaces **one named element** in existing footage and preserves
everything else as filmed: people, performance, camera path, cuts, lighting,
audio and event order. It runs on the Seedance 2.5 `edit` operation with
`@Video 1` as the sole editing master.

| Request | Route |
| --- | --- |
| One product, garment, prop or person replaced; rest of the shot kept | Object Swap (this reference) |
| Background or location replaced behind kept subjects | Background replacement in [Seedance 2.5 editing](seedance-25-edit.md) |
| Added creature, effect or new element | VFX integration ([Fidelity And Continuity](fidelity-and-continuity.md)) |
| Whole cast, wardrobe, product and world rebuilt, keeping only motion, camera and timing | Motion recast (`seedance-motion-recast`), not this skill |

Swap one element class per request. When two unrelated elements must change,
run two sequential swaps and inspect between them, or treat the job as a
recast if most of the frame changes.

## Swap contract

Every swap prompt states five things. Missing any one of them is the usual
cause of a failed swap.

1. **Identification.** Name the original by observable descriptors: screen
   position, colour, material, what holds or wears it, and when it first
   appears. "The red aluminium can in the woman's right hand" — never "the
   product".
2. **Object count.** State how many target objects the entire video contains,
   and per cut when the count changes: `The entire video contains exactly one
   <target>.`
3. **Timeline Inheritance.** The target inherits every appearance, motion,
   occlusion and exit of the original, including timing, duration, path and
   speed changes, across every cut.
4. **Residual-original guard.** Phrase the result positively: `The original
   <object> is fully replaced in every frame; only the <target> appears.` Add a
   negative only where a leak was observed in a probe.
5. **Preservation.** Everything outside the swapped element stays as in
   `@Video 1`: identity, wardrobe, hands, performance, camera, cuts, lighting,
   dialogue, lip sync and ambience.

Target reference rules:

- `@Image N` defines only the target's appearance, structure, material and
  label layout. State what to ignore in the image: its background, table,
  hands, people or lighting.
- Prefer 1–5 references: one clean packshot or sheet view per image, not a
  collage. Several views of one target need `The output contains only one
  <target> throughout.`
- For an authorized real brand or labeled product, bind the official or
  user-supplied product asset. Generate a substitute only when no usable real
  asset exists.
- Match the target's scale to the original's grip or fit. When the target is
  larger or smaller, state the new scale and how the hand or body accommodates
  it, or the model rescales the hand instead.
- Do not ask the model to render overlay copy, taglines or end cards. A label
  printed on the product is part of the product; captions go in post.

Keep lighting on the target physical: the same key direction, colour
temperature and reflections as the original's surroundings.

## Using a subject map

A separate source-analysis step may supply a subject map: per-subject
descriptors, cuts, per-cut counts (`count_per_cut`), occlusions, and contact
windows (`contact_windows`) (when a hand, mouth or body touches the object). When one
exists, copy from it rather than re-deriving:

- the original's identifying descriptors, verbatim, into `[Edit Goal]` and
  `[Edit Scope]`;
- the per-cut count into the object-count line;
- each contact window into `[Contact and Occlusion]` with its approximate time;
- every other mapped subject into `[Content to Preserve]`.

Without a subject map, inspect the source yourself and record the same facts
before writing the prompt. Uncertain counts or contact windows remain open
questions, not guesses.

## Contact and occlusion

Swaps fail most often where the original touches something. List each contact
and occlusion event with its approximate time:

- **Grip.** Fingers wrap the target as they wrapped the original: same finger
  count, same knuckle positions, thumb on the same side.
- **Mouth or face contact.** Drinking, biting or applying: the lips meet the
  target's opening or edge; the face and jaw performance stay as in `@Video 1`.
- **Occlusion.** When a hand, arm or another object passes in front of the
  original, the same part of the target is hidden for the same duration and
  reappears in the same place.
- **Exit and re-entry.** When the original leaves frame or a cut hides it, the
  target leaves and returns at the same times and positions.
- **Surface contact.** Set-down moments keep a soft contact shadow and the same
  resting position.

## Templates

Each template extends the canonical structure in
[Seedance 2.5 editing](seedance-25-edit.md). Fill every `<...>` from source
inspection or the subject map. Add the face-protection line from that
reference whenever a face stays visible.

### Product swap

```text
[Edit Goal]
Edit @Video 1. Change only <original product, observable descriptors> to the
<target product> from @Image 1.

[Source Video Role]
@Video 1 is the sole editing master. It defines the people, their hands and
performance, the scene, camera position and movement, cuts, motion path,
occlusion relationships, audio and event order.

[Target Reference Role]
@Image 1 defines only the <target product>'s shape, proportions, material,
colour and label layout. Do not use its background, surface or lighting.

[Edit Scope]
Modify only the <original product>. The entire video contains exactly one
<target product>. The original <product> is fully replaced in every frame;
only the <target product> appears. Do not modify <people, hands, wardrobe,
set dressing, background>.

[Timeline Inheritance]
The <target product> inherits every appearance, motion, occlusion and exit of
the <original product>, including timing, duration, path and speed changes.
Except for the product, keep all people, props, scene content, camera
movements, cuts and event order from @Video 1 unchanged.

[Contact and Occlusion]
<At about 0:NN, grip / contact / occlusion event and how the target behaves.>

[Content to Preserve]
Keep identity, facial expression, hands, performance, lighting, dialogue, lip
sync and ambience from @Video 1. The <target product> takes the key light and
reflections of its surroundings.
```

### Wardrobe swap

```text
[Edit Goal]
Edit @Video 1. Change only <person descriptor>'s <original garment> to the
<target garment> from @Image 1.

[Source Video Role]
@Video 1 is the sole editing master. It defines the person's identity, body,
pose, movement, the scene, camera, cuts and event order.

[Target Reference Role]
@Image 1 defines only the <target garment>'s cut, fabric, colour, pattern and
closures. Do not use the model, pose, background or lighting in the image.

[Edit Scope]
Modify only the <original garment> on <person descriptor>. The person wears
exactly one <target garment>. The original <garment> is fully replaced in
every frame; only the <target garment> appears. Keep <face, hair, skin,
accessories, other garments, other people> exactly as in @Video 1.

[Timeline Inheritance]
The <target garment> follows every movement of the body: folds, stretch and
sway match the pose changes, timing and speed of @Video 1. Where arms, hair or
props cover the garment, the same area stays covered for the same duration.

[Content to Preserve]
Keep the person's identity, accessories, performance, camera, lighting,
dialogue and lip sync from @Video 1.
```

Name accessories (glasses, jewellery, bag straps, watch) individually in the
preserve list so they neither vanish nor migrate onto the new garment.

### Single-character swap

```text
[Edit Goal]
Edit @Video 1. Replace only <original person, position + clothing + action>
with <target character> from @Image 1.

[Source Video Role]
@Video 1 is the sole editing master. It defines the performance, body motion,
gestures, gaze direction, timing, the scene, the other people, camera and cuts.

[Target Reference Role]
@Image 1 defines only <target character>'s face, hair, build, wardrobe and
accessories. Use the close-up view for the face. Do not use the image's
background, pose or lighting.

[Edit Scope]
Modify only <original person>. The entire video contains exactly one
<target character>. The original person is fully replaced in every frame;
only <target character> appears in that role, wearing only the wardrobe and
accessories shown in @Image 1. Keep every other person exactly as in @Video 1.

[Timeline Inheritance]
<Target character> inherits every movement, gesture, gaze, entrance, exit and
occlusion of the original person, with the same timing and speed.

[Content to Preserve]
Keep all other people, the scene, camera, cuts, lighting, dialogue timing and
ambience from @Video 1. Real human skin with pores and catchlights — never
waxy, smoothed, or warped.
```

Record consent for the target likeness and for the source performer whose
performance is kept before this template reaches a request. A creative
selection never implies consent. Swapping more than one person, or the whole
cast, is a recast.

### Prop swap

```text
[Edit Goal]
Edit @Video 1. Change only <original prop, descriptors> to <target prop> from
@Image 1.

[Source Video Role]
@Video 1 is the sole editing master. It defines the people, their handling of
the prop, the scene, camera, cuts, motion path and event order.

[Target Reference Role]
@Image 1 defines only <target prop>'s shape, size, material and surface
detail. Do not use its background or lighting.

[Edit Scope]
Modify only the <original prop>. The entire video contains exactly <N>
<target prop>. The original <prop> is fully replaced in every frame; only the
<target prop> appears. Do not modify <people, hands, other props, background>.

[Timeline Inheritance]
The <target prop> inherits every appearance, motion, occlusion and exit of the
<original prop>, including timing, duration, path and speed changes, and its
bounces, spins and contacts land at the same moments.

[Contact and Occlusion]
<Each hand-off, throw, catch or set-down with approximate time.>

[Content to Preserve]
Keep performance, camera, lighting, dialogue, lip sync and sound effects from
@Video 1.
```

For a thrown or fast-moving prop, state its path in screen terms ("arcs from
lower left to the catch at upper right") so the target follows it rather than
staying near its first position.

## Worked example: hand-held can to product

Source: `@Video 1`, 6 s, 16:9, static medium shot at a café terrace. A woman
in a denim jacket and gold hoop earrings lifts a red aluminium soda can from
the table at about 0:01, drinks at 0:02–0:04 while her fingers wrap the can's
front, and sets it down at about 0:05. One can is visible throughout; no cuts.
Target: `@Image 1`, the approved packshot of `@slim-can-black`, a matte-black
slim 330 ml can with a copper ring-pull and a vertical copper wordmark.

```text
[Edit Goal]
Edit @Video 1. Change only the red aluminium soda can in the woman's right hand
to the @slim-can-black can from @Image 1.

[Source Video Role]
@Video 1 is the sole editing master. It defines the woman, her denim jacket and
gold hoop earrings, her hand and mouth performance, the café terrace, the
static camera, the motion path of the can, occlusion relationships, audio and
event order.

[Target Reference Role]
@Image 1 defines only @slim-can-black's slim shape, matte-black finish, copper
ring-pull and vertical copper wordmark. Do not use the image's background,
surface or studio lighting.

[Edit Scope]
Modify only the soda can. The entire video contains exactly one
@slim-can-black can. The original red can is fully replaced in every frame;
only the matte-black can appears. Do not modify the woman, her jacket,
earrings, hands, the table or the terrace.

[Timeline Inheritance]
The @slim-can-black can inherits every appearance, motion, occlusion and exit
of the red can, including timing, duration, path and speed changes: resting on
the table, the lift at about 0:01, the drink at 0:02–0:04 and the set-down at
about 0:05. Except for the can, keep all people, props, scene content, camera
movement and event order from @Video 1 unchanged.

[Contact and Occlusion]
The slim can is taller and narrower than the red can. Her right hand keeps its
size, position and finger count from @Video 1 and closes slightly further
around the narrower can from the lift to the set-down, covering the lower half
of the wordmark during the drink. Her lips meet the can's rim at 0:02–0:04. At
the set-down the can rests in the same spot with a soft contact shadow on the
tabletop.

[Content to Preserve]
Keep the woman's face, expression, gaze, hands, jacket and earrings, the
terrace, the static framing, daylight direction, ambience and the can's
set-down sound from @Video 1. The matte-black can takes the same warm daylight
key from frame left, with a soft copper highlight on the ring-pull. Real human
skin with pores and catchlights — never waxy, smoothed, or warped.
```

Submit with `omni_reference_task_type="edit"`, `@Video 1` first and
`@Image 1` second, at the lowest suitable resolution for the probe. The caller
owns prompt review, the request record and submission.

## Swap QA

Inspect the output side by side with the source, frame by frame around each
contact window and cut. Record each item as pass, fail or not applicable.

- **Residual original.** No frame shows the original object, a blend of old and
  new, or a second copy of the target. Check the first and last frames and
  every re-entry.
- **Tracking on every appearance.** The target follows the original's path,
  timing, occlusions and exits across every cut; it does not drift, freeze or
  lag behind.
- **Hands and contact points.** Finger count, grip and knuckle placement match
  the source; lips, teeth and skin meet the target cleanly; no melted or
  merged edges at contact.
- **Logo and text fidelity.** Label layout, wordmark shape and colour match the
  reference. Small printed text is not guaranteed; flag drift for a fix pass or
  a post correction, and never accept invented copy.
- **Scale and lighting.** The target sits at the intended scale with the
  surroundings' key direction, reflections and contact shadow.
- **Everything else untouched.** Faces, wardrobe, accessories, other props,
  background, camera and cuts match `@Video 1`.
- **Lip sync and audio untouched.** Dialogue, lip movement, ambience and
  sound effects match the source unless the change contract says otherwise.
- **Consent for character swaps.** Recorded consent covers the target likeness
  and the retained source performer before approval; a missing record blocks
  the take regardless of visual quality.
