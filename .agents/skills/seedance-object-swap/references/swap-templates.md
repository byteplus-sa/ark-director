# Swap Templates

Focused reference for `seedance-object-swap`. Read [the entrypoint](../SKILL.md)
for routing and parameters, and [swap contract](swap-contract.md) for the facts
each template needs.

- [Shared rules](#shared-rules)
- [Product swap](#product-swap)
- [Outfit swap](#outfit-swap)
- [Character swap](#character-swap)
- [Prop or object swap](#prop-or-object-swap)
- [Location swap](#location-swap)
- [Worked example: hand-held can to product](#worked-example-hand-held-can-to-product)

## Shared rules

Fill every `<...>` from source inspection or the subject map. Every template
ends with the same audio block, because `@Video 1` is the muted master:

```text
[Audio]
Silent output. Sound is added in post.
```

Add the face-protection line whenever a face stays visible:
`Real human skin with pores and catchlights — never waxy, smoothed, or warped.`
For a stylized source, describe its own surface quality instead.

## Product swap

```text
[Edit Goal]
Edit @Video 1. Change only <original product, observable descriptors> to the
<target product> from @Image 1.

[Source Video Role]
@Video 1 is the sole editing master. It defines the people, their hands and
performance, the scene, camera position and movement, cuts, motion path,
occlusion relationships and event order.

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
Keep identity, facial expression, hands, mouth movement and lighting from
@Video 1. The <target product> takes the key light and reflections of its
surroundings.
```

## Outfit swap

```text
[Edit Goal]
Edit @Video 1. Change only <person descriptor>'s <original garment> to the
<target garment> from @Image 1.

[Source Video Role]
@Video 1 is the sole editing master. It defines the person's identity, body,
pose, movement, the scene, camera, cuts and event order.

[Target Reference Role]
@Image 1 defines only the <target garment>'s cut, fabric, colour, pattern and
closures. Do not use the mannequin, background or lighting in the image.

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
Keep the person's identity, accessories, performance, mouth movement, camera
and lighting from @Video 1.
```

Name accessories (glasses, jewellery, bag straps, watch) individually in the
preserve list so they neither vanish nor migrate onto the new garment.

## Character swap

`@Image 1` and `@Image 2` are Virtual Portrait `asset://` views of the target.

```text
[Edit Goal]
Edit @Video 1. Replace only <original person, position + clothing + action>
with <target character> from @Image 1 and @Image 2.

[Source Video Role]
@Video 1 is the sole editing master. It defines the performance, body motion,
gestures, gaze direction, mouth movement, timing, the scene, the other people,
camera and cuts.

[Target Reference Role]
@Image 1 (close-up) defines <target character>'s face and hair. @Image 2 (full
body) defines build, wardrobe and accessories. Do not use either image's
background, pose or lighting.

[Edit Scope]
Modify only <original person>. The entire video contains exactly one
<target character>. The original person is fully replaced in every frame;
only <target character> appears in that role, wearing only the wardrobe and
accessories shown in @Image 2. No <source accessories> appear. Keep every
other person exactly as in @Video 1.

[Timeline Inheritance]
<Target character> inherits every movement, gesture, gaze, mouth movement,
entrance, exit and occlusion of the original person, with the same timing and
speed.

[Content to Preserve]
Keep all other people, the scene, camera, cuts and lighting from @Video 1.
Real human skin with pores and catchlights — never waxy, smoothed, or warped.
```

## Prop or object swap

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
Keep performance, camera and lighting from @Video 1.
```

For a thrown or fast-moving prop, state its path in screen terms ("arcs from
lower left to the catch at upper right") so the target follows it rather than
staying near its first position.

## Location swap

```text
[Edit Goal]
Edit @Video 1. Replace only the <original location, descriptors> behind
<kept subjects> with the location from @Image 1.

[Source Video Role]
@Video 1 is the sole editing master. It defines <kept subjects>, their
wardrobe, performance and lighting, the camera position and movement, cuts and
event order.

[Target Reference Role]
@Image 1 defines only the new location's layout, materials, time of day and
light direction. Do not use any people, vehicles or signage in the image.

[Edit Scope]
Modify only the environment. Exactly <N> people appear, as in @Video 1. The
original <location> is fully replaced in every frame. Do not modify
<kept subjects>, their clothing, hands or held props.

[Timeline Inheritance]
The new location follows the camera movement of @Video 1 with matching
parallax: <near elements> pass faster than <far elements>. <Kept subjects>
stay naturally grounded — no cut-out edge, no halo; rim light matches the key
direction.

[Content to Preserve]
Keep every person's identity, performance, mouth movement and lighting from
@Video 1. The new location's key light comes from <source key direction> with
<colour temperature>, matching the light already on the subjects.
```

## Worked example: hand-held can to product

Hypothetical example; no result evidence is attached.

Source: `@Video 1`, the 6 s, 16:9 muted master of a static medium shot at a
café terrace. A woman in a denim jacket and gold hoop earrings lifts a red
aluminium soda can from the table at about 0:01, drinks at 0:02–0:04 while her
fingers wrap the can's front, and sets it down at about 0:05. One can is
visible throughout; no cuts. Target: `@Image 1`, the approved packshot of
`@slim-can-black`, a matte-black slim 330 ml can with a copper ring-pull and a
vertical copper wordmark. Post-audio route: original.

```text
[Edit Goal]
Edit @Video 1. Change only the red aluminium soda can in the woman's right hand
to the @slim-can-black can from @Image 1.

[Source Video Role]
@Video 1 is the sole editing master. It defines the woman, her denim jacket and
gold hoop earrings, her hand and mouth performance, the café terrace, the
static camera, the motion path of the can, occlusion relationships and event
order.

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
Keep the woman's face, expression, gaze, hands, mouth movement, jacket and
earrings, the terrace, the static framing and the daylight direction from
@Video 1. The matte-black can takes the same warm daylight key from frame
left, with a soft copper highlight on the ring-pull. Real human skin with pores
and catchlights — never waxy, smoothed, or warped.

[Audio]
Silent output. Sound is added in post.
```

Submit with `omni_reference_task_type: edit`, `@Video 1` first and `@Image 1`
second, `generate_audio: false`, at 480p for the probe. After QA, mux the saved
source audio so the set-down sound lands at 0:05.
