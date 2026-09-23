# Guards and Failures

Focused reference for `seedance-motion-recast`. Read [the entrypoint](../SKILL.md)
for mode selection, gates and caller responsibilities.

Add a guard only for a risk present in this source. Each failure below has a
prompt guard, a QA check and a repair. Guards are written as observable end
states; necessary exclusions name the exact source item that must not carry
over.

- [QA baseline](#qa-baseline)
- [Accessory and wardrobe bleed](#accessory-and-wardrobe-bleed)
- [Extra or duplicated people](#extra-or-duplicated-people)
- [Identity drift on profiles and turns](#identity-drift-on-profiles-and-turns)
- [Identity swap between performers](#identity-swap-between-performers)
- [Hands and contact deformation](#hands-and-contact-deformation)
- [Residual originals and source appearance leak](#residual-originals-and-source-appearance-leak)
- [Flicker from over-broad scene prompts](#flicker-from-over-broad-scene-prompts)
- [Blurred or occluded source motion](#blurred-or-occluded-source-motion)
- [Text and logos from the source](#text-and-logos-from-the-source)
- [Provider rejections](#provider-rejections)

## QA baseline

For every take:

1. Decode the output and probe duration, fps, resolution and audio streams.
2. Build a side-by-side of source and output (the
   `ffmpeg-side-by-side-comparison` skill does this) and play it in full.
3. Extract keyframes at each source cut and at each key beat, and compare them
   with the references.
4. Count people in every cut.
5. Check motion correspondence: the same pose at the same beat, the same screen
   position, the same camera move and cut timing, within the model's
   approximate timing.

Contact sheets support review but cannot verify motion, timing or audio.

## Accessory and wardrobe bleed

**Symptom:** glasses, jewelry, caps, logos or a jacket from the source subject
appear on the new character.

**Guard:**

```text
Each new character wears only the outfit in their own reference. <Name> has no
<cap / sunglasses / chain> from @Video 1.
```

Name the specific source accessories that are at risk, taken from the subject
map or your inspection.

**QA:** compare each character's head, neck, wrists and outer layer against
their reference in every cut.

**Repair:** tighten the Motion Authority exclusion to name clothing and
accessories, and make sure the character reference clearly shows the intended
outfit. If the reference lacks the intended accessory state, fix the element,
not the prompt.

## Extra or duplicated people

**Symptom:** a third person appears, a character is doubled, or a crowd grows.

**Guard:**

```text
Exactly <N> people appear in every frame. <Per-cut presence if it varies.>
```

For crowds, add the approximate count and region from the group disposition.

**QA:** count people per cut; check reflections and background windows too.

**Repair:** make the per-cut presence explicit, reduce background extras, or
trim the source so crowd-heavy moments are a separate shot.

## Identity drift on profiles and turns

**Symptom:** the face changes when a character turns to profile or away, or
spins.

**Guard:** bind a profile view (and a back view when the source shows it) as a
separate image of the same character:

```text
@Image 1 (front) and @Image 2 (left profile) define the same person, Mara.
Mara keeps the same face and hair through the spin at about 0:04.
```

**QA:** compare frames at maximum head rotation against the profile reference.

**Repair:** add or replace the missing view. Separate view images are more
stable than a collage.

## Identity swap between performers

**Symptom:** after a crossing, an occlusion or a cut, the two new characters
trade faces or outfits.

**Guard:** state each character's position through the crossing and that each
keeps their own identity:

```text
Mara starts screen-left and crosses behind Theo at about 0:03; after the
crossing Mara is screen-right. Each keeps their own face and outfit.
```

**QA:** track each character frame by frame through every crossing and cut.

**Repair:** sharpen the descriptors with the crossing, or split at the cut.

## Hands and contact deformation

**Symptom:** fingers merge, a held product warps, or a handoff loses the object.

**Guard:** name the owner, the hand and the object state at each contact
window from the subject map:

```text
The Lumen X phone stays in Mara's right hand from 0:00 to about 0:05, screen
facing the camera, one phone throughout.
```

**QA:** step through each contact window; count objects; check fingers and the
object silhouette.

**Repair:** trim to fewer contact events per shot, add a clear product view, or
move a fast handoff into its own shot.

## Residual originals and source appearance leak

**Symptom:** the original product, face, outfit or location survives in some
frames, or the whole output looks like the source with small changes.

**Guard:**

```text
The original <object / rooftop / outfit> from @Video 1 no longer appears in
any frame.
```

**QA:** check every appearance, occlusion and exit of each replaced subject or
object, and scan for source colors or architecture.

**Repair:** a local leak is a prompt repair. A whole-frame leak on the default
route is the signal to probe the next route (explicit reference task type,
then plan B full-frame edit). Record the probe result.

## Flicker from over-broad scene prompts

**Symptom:** textures, signs, clothing detail or background layout change from
frame to frame.

**Guard:** describe the location with a few stable elements (layout, materials,
light direction) and let the location reference carry detail. Avoid long lists
of small moving items and competing light sources.

**QA:** play the output at full speed and step through static areas.

**Repair:** shorten the location and style blocks, remove conflicting look
words, or pin the look with one location reference instead of several.

## Blurred or occluded source motion

**Symptom:** during motion blur, fast spins or occlusions, limbs smear or the
new character's pose becomes ambiguous.

**Guard:** state the end pose after the blur or occlusion as an observable
state:

```text
After the spin at about 0:04 Mara faces the camera with both arms raised.
```

**QA:** compare the output pose immediately after each blur or occlusion window
with the source.

**Repair:** use a cleaner source take, trim around the smear, or split the shot.
A source whose key motion is unreadable is not a good motion master.

## Text and logos from the source

**Symptom:** source signage, jersey numbers or logos reappear, or garbled text
is generated.

**Guard:** describe signage as abstract shapes and colors, and map any required
brand to an authorized reference. Add exact copy in post.

**QA:** scan every frame for legible text and unapproved marks.

## Provider rejections

A `PrivacyInformation`, sensitive-content or policy rejection is evidence to
diagnose. Stop, report the request ID and flagged inputs, and follow the
moderation rule in the
[production policy](../../../contracts/production-policy.md). Never alter,
disguise or swap inputs to pass the check. Offer an invented cast, a generated
or owned-talent source clip, or the provider's authorized route, and resubmit
only on the user's explicit decision.
