# Worked Examples

Focused reference for `seedream-location-asset`. Load it when writing a full
location prompt from scratch. Set the aspect ratio and resolution with the
`size` parameter; none of these prompts names a ratio.

## Canonical interior lock: maritime captain's cabin

The bundled sample image `examples/pirate-location.png` was generated
from an earlier version of this prompt. That version named a 2.39:1 ratio, a
push-in, "4K", and baked lens effects (flare, halation, vignetting) in the
text; the version below removes them so the plate stays a clean reference and
the video prompt owns camera motion and lens character.

```text
Task:
Text-to-Image (T2I)

Location:
A cramped below-deck captain's cabin on an old wooden sailing ship.

Era and world rules:
Early 18th-century Golden Age of Piracy, Caribbean privateer vessel, grounded period maritime realism, lantern-and-candle era, no modern objects.

Set dressing and objects:
A large weathered sea-chart pinned to the rough plank back wall above a heavy waxed-oak table strewn with brass navigation instruments, including one pair of dividers and one sextant. One gimbaled brass lantern hangs low in the upper frame. Tarred coiled rope and one barrel fill the foreground edges. Low heavy-beamed ceiling, rough plank walls and floor, hand-hewn waxed oak grain, tarred rough hemp, tarnished brass, brittle creased parchment with faded hand-drawn coastlines and no lettering, coarse canvas.

Style:
Photorealistic cinematic movie still, grounded period maritime realism, naturalistic editorial reference, fine low-intensity 35mm grain.

Lighting and atmosphere:
Mid-morning, calm weather, warm and enclosed. The brass lantern is the single warm tungsten key from frame-left, pooling softly on the table, with deep shadow falloff into the corners. Thin hard daylight slivers leak through plank gaps on the right wall. Palette of aged oak brown, tarred black, oxidized brass amber, parchment cream and shadowed sea-grey. Drifting dust motes in the lantern light, faint smoke haze.

Composition and lens:
Wide three-quarter interior establishing view, eye-level, 24mm lens, deep depth of field with the whole cabin in focus.

Constraints:
No people, no modern objects, no electric light fixtures, no plastic surfaces, no text overlays, no watermarks.
```

![Pirate captain's cabin location asset](../examples/pirate-location.png)

## Night lock of an approved exterior

**Hypothetical teaching example. No image was generated for this prompt.**
It applies the night-lock rules; inspect the result for a blue sky, a bright
moon, or a visible light cone before approval.

```text
References:
@Image 1: approved day lock of the village street — geometry and dressing authority

Task:
Image-to-Image (I2I)

Location:
The same narrow village street from @Image 1: the same houses, the same well at the centre, the same mango tree on the right, the same camera position.

Lighting and atmosphere:
Late night. Black sky with no gradient and a small pale crescent moon high in the upper left. Low overall exposure. Two windows glow warm amber: the ground-floor window of the left house and the upper window of the far house. One small oil lamp hangs by the well and lays a soft round pool of light on the ground around it. Everything outside these pools falls to deep blue-black shadow, with only the rooftop edges faintly rimmed by moonlight.

Composition and lens:
Keep the framing, lens, and camera height of @Image 1.

Constraints:
No people, no added objects, no street lights.
```

## Same-place environment plate for a restyle

**Hypothetical teaching example. No image was generated for this prompt.**
The source clip shows a person walking down a city sidewalk; the restyle needs
the same place in claymation. The plate describes the source's own place and
stays empty.

```text
Task:
Text-to-Image (T2I)

Location:
A city sidewalk on a sunny afternoon: three-storey brick shop buildings on the left with green awnings over plain shop windows, a row of four young street trees in square planters along the curb on the right, a bus-stop bench between the second and third tree, the street receding straight ahead to a crossing.

Style:
Handmade claymation set, matte modelling-clay surfaces with soft fingerprint texture, slightly rounded edges, miniature-set scale.

Lighting and atmosphere:
Warm afternoon sun from frame-right, soft-edged shadows from the trees falling across the sidewalk.

Composition and lens:
Eye-level view down the sidewalk from its centre, matching the source camera height, moderate depth of field.

Constraints:
No people, no vehicles parked on the sidewalk, plain awnings and windows with nothing printed, no signage text.
```
