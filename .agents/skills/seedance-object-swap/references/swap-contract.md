# Swap Contract

Focused reference for `seedance-object-swap`. Read [the entrypoint](../SKILL.md)
for routing, rules and caller responsibilities.

- [The five parts](#the-five-parts)
- [Using a subject map](#using-a-subject-map)
- [Contact and occlusion](#contact-and-occlusion)
- [Character and location targets](#character-and-location-targets)

## The five parts

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
   negative only for a residual original seen in review.
5. **Preservation.** Everything outside the swapped element stays as in
   `@Video 1`: identity, wardrobe, hands, performance, mouth movement, camera,
   cuts and lighting. Sound is not part of the edit; it returns in post.

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

## Character and location targets

For character and location swaps the target reference is a person or a place,
so the reference role excludes only what the target does not own: the
reference's pose and lighting for a character, its people, vehicles and
signage for a location.

**Character.** The target identity is a Virtual Portrait asset bound by
position, for example `@Image 1` (close-up) and `@Image 2` (full body). The
image defines only face, hair, build, wardrobe and accessories; the
performance, gaze and timing stay with `@Video 1`. Name the source person's
accessories that must not carry over (glasses, earrings, cap) and state that
the target wears only what the reference shows. Replacing more than one person
is a Motion Transfer.

**Location.** The kept subjects stay as filmed: their pixels, lighting,
wardrobe and performance. The location reference defines layout, materials,
time of day and light direction. Choose or describe a location whose key
direction and colour temperature match the light already on the subjects,
because the subjects are not relit. The new background follows the source
camera's movement with matching parallax, and every floor contact keeps a soft
contact shadow. People, vehicles or signage in the location image are not
used.
