# Frame Break Scenes and Subjects

Focused reference for `seedance-frame-break`. Read it when choosing the backdrop
or adapting the prompt to a subject type. The prompt blocks stay in
[the entrypoint](../SKILL.md) and [the template](prompt-template.md).

- [Scenic backdrop](#scenic-backdrop)
- [Subject types](#subject-types)

## Scenic backdrop

A beautiful scene helps the effect when it is confined to the central window and
stays out of the subject's way.

| Rule | Why and how |
| --- | --- |
| Confine the scene to the window | State in the layer-order block that the scene fills only the central window between the bars. |
| Calmer and darker than the subject | The subject is the brightest, most saturated thing; the backdrop is lower in contrast and value. A calm, darker, lower-contrast scene read well (observed result). |
| Colours differ from the subject | A teal sneaker sole on a teal backdrop was unreadable and a requested cobalt rendered as teal (observed result). Pick a different hue family and do not rely on a precise colour name surviving. |
| No bar-like objects near the bar zone | Boxing-ring ropes at the bar position were drawn as the bars with the subject behind them (observed result). Avoid ropes, rails, beams, fences, shutters and long horizontal edges near the top and bottom of the window; keep any such object far back in the middle distance or leave it out. |
| No lettering | Leave out signs, posters, shirts and packaging text. The model may paint real-brand logos or lettering on background objects despite plain, unmarked wording, including a logo on background bags (observed result); inspect backgrounds and keep the footage text-free. |
| Static scene, fixed camera | Dusk skyline, night plaza, twilight village, blossom park, gym and golden-hour court stayed static with a fixed camera (observed result). Prefer scenes with slow ambient motion only. |
| Depth for the approach | Give the scene a readable far distance (a quay, a plaza, a court) so the subject can travel from far to near. |
| Keep the scene free of unrequested effects | Glow arcs and flare can appear around near-lens parts (observed result); a restrained scene gives them less to build on. |

Compose lighting, lens and grade with their preset skills only when requested;
do not pad the prompt with unused defaults.

## Subject types

Observed results come from six 1080p Seedance 2.5 runs (October 2026); notes
without that label are optional technique to test. In every type the bars stay
fixed and straight, the subject is full-body inside the window at the start and
at every stage boundary, break-outs are brief limb or hem events (no near-lens
limb or head filling a third of the frame), and each stage carries one coherent
action.

| Subject | Notes |
| --- | --- |
| Illustrated or anime character | Drawn subjects gave 3 to 5 strong overlap moments (observed result). Name the art style once; limbs, hair and cape edges cross cleanly. Bind the character sheet as face, hair, clothing and style only. |
| Flat poster or graphic character | Optional technique: ask for flat shapes and a clean outline, and keep the crossing part a simple, large silhouette (a hand, a boot, a hem). Pair with `seedance-animation-styles` for medium rules. |
| Stylised 3D mascot | Optional technique: give the nearest limb a modest scale and keep the others small and tucked behind until their stage, because an arm reach followed by a kick produced a giant sole that matched neither the sheet nor the scale (observed on a stylised 3D fox take). Check soles, paws and markings against the sheet. Pair with `seedance-animation-styles`. |
| Photoreal person | Fewer overlap moments (1 to 3) and the final held pose stayed inside the window (observed result). Plan one brief break-out per bar; use a raised fist and forearm or palm for the upper bar and a robe hem or a boot for the lower bar. Keep the person full-body inside the window, about two thirds of the window height, and do not let her walk or lean closer: a boxer take with legs, shorts and robe over the lower bar for most of the clip read as standing outside the frame, and one that leaned very close to the lens distorted the lower bar edge, which tilted, bowed and jumped (both observed on boxer takes). Avoid ring ropes and rails; keep any background bags and equipment free of lettering. |
| Photoreal animal | Fewer overlap moments (1 to 3) (observed on a puppy take, where the upper bar occluded the head). Use one limb per stage (a paw, an ear tip, a tail) and give the upper bar its own stage with an End state. |
| Product | Read [product hero](product-hero.md): real photos as references, one product, no person or hand, text-free footage, end card in post. |
