# Effect recipes - World and transformation

Nine effects where the world, the body, or the camera scale changes around one photographed subject: environment folds and waves, body-to-puddle melting, a fire double, scale dives, point-cloud scans, and glitch-UI strobes. Every recipe follows the same skeleton: an `@Image 1` frame-role sentence, one subject sentence built from the `{subject}` slot, a timestamped timeline with one primary state change per stage and explicit `Cut to` seconds, one camera sentence with move, start and end, a visual-style sentence, and an observable end state. Counts are stated at every stage. All on-screen text (HUD labels, error dialogs, signage) is added in post; the generated clips contain only abstract shapes. Status of every recipe: untested hypothesis, derived from the Higgsfield example footage analysed on 2026-10-08.

## Menu rows

| id | label | route | duration | start photo |
| --- | --- | --- | --- | --- |
| `world-morphing` | World morphing | `i2v-first-frame` | 8 s | Centered person, open street, tall surroundings |
| `architecture-wave` | Architecture wave | `i2v-first-frame` | 7 s | Low-angle person, big rigid structure behind |
| `melting` | Melting | `i2v-first-frame` | 7 s | Full-body standing person, flat clear ground |
| `burning-man` | Burning man | `i2v-first-frame` | 7 s | Full-body person, empty space beside, dusk |
| `particles` | Particles | `composite` | 5 s | Single subject, dark high-contrast scene |
| `lidar` | Lidar transition | `i2v-last-frame` | 7 s | Person outdoors, distinct posts and skyline |
| `earth-zoom` | Earth zoom | `i2v-last-frame` | 10 s | Eye-level person on a plausible city street |
| `blue-depth` | Blue depth | `i2v-first-frame` | 8 s | Waist-up person in front of dark blue water |
| `windows` | Windows | `composite` | 5 s | Cool-toned action shot with negative space |

### `world-morphing` - World morphing

**Look:** The street and skyline peel up and fold over a calm, upright subject until the whole city hangs inverted overhead.
**Route:** `i2v-first-frame`. `@Image 1` is the first frame; no other image roles.
**Parameters:** 8 s; ratio follows the photo (16:9 and 9:16 both seen); `generate_audio` false (a low rumble sting would help but bakes easily into music, so use a Seed Audio bed in post); draft at 480p.
**Start photo:** Full or three-quarter-body person centered in an open, geometrically legible space with a clear ground plane (street, crosswalk, plaza) and tall surroundings, sharp daylight. Bad: motion blur, cropped legs, crowds, a person leaning on or touching the ground plane's edge, tiny subject.
**Beats (from the originals):**
- 0-2s: grounded eye-level shot, subject standing or walking, buildings start to lean.
- 2-4s: buildings tilt, the street plane curls upward at the frame edges like a lifting page, subject looks up.
- 4-6s: the ground curls over the subject's head and becomes a ceiling; skyscrapers hang down from it; subject turns to show the back.
- 6-8s: the inverted city settles overhead (cars upside down), the subject, right side up, turns back to camera and holds.
- No cuts; one continuous take with a gentle orbit and roll.
**Prompt template:**
```text
@Image 1 is the first frame. It defines {subject}, the outfit, the {location} and the eye-level framing.
{subject} stands upright and calm at the center, anchored to the ground, with the same face, hair and {outfit_details} in every frame. Exactly one person is in the frame{extra_people}. Only the surroundings move; {pronoun_subject} only turns {pronoun} head.
0-2s: the {location} looks normal; the surrounding {building_type} begin to lean slowly inward and {subject} turns {pronoun} head to look up.
2-4s: the street surface at the frame edges peels upward like a lifting page and curls toward the sky; the buildings stay rigid blocks that tilt and fold with smooth liquid easing.
4-6s: the curled street closes over {subject} as a ceiling; the {building_type} hang downward from it with open sky below the inverted blocks.
6-8s: the inverted city settles overhead with {ceiling_street}; {subject}, right side up, turns back to the camera and holds still.
Camera: one continuous take; start at the framing of the photo, orbit slowly about 20 degrees to the {orbit_side} with a gentle clockwise roll, then settle in the same framing.
The visuals feature natural daylight, photorealistic detail and the color grade of the photo. Shop signs stay small and softly out of focus.
```
**Slots:**
- `{subject}`: read from the photo ("the woman in the beige trench coat").
- `{location}`: read ("crosswalk", "plaza").
- `{outfit_details}`: read; list garment colors, bag and hair length so identity survives the turn away.
- `{extra_people}`: default empty, otherwise ", plus {n} distant pedestrians".
- `{building_type}`: read ("glass towers", "brick tenements").
- `{pronoun}`: "her" or "his" from the photo.
- `{ceiling_street}`: "{n} vehicles upside down on the ceiling street" counted from the photo, or "an empty ceiling street" when no vehicle is visible.
- `{pronoun_subject}`: "she" or "he" from the photo.
- `{orbit_side}`: "left" or "right"; default "right".
**Post:** none. Optional rumble and wind bed via Seed Audio.
**QA:**
- Subject stays right side up, with the same face, outfit and hair, in every frame.
- The ground visibly curls over the subject between 2s and 6s; the inverted city is overhead at 6-8s.
- Buildings fold as rigid blocks, not melt.
- Final framing is a medium shot close to the opening framing.
- No readable lettering appears on signs.
**Risks:** Identity drift when the subject turns away and back; the subject flipping upside down with the world; buildings melting instead of folding; crosswalk stripe or vehicle counts changing; signage garbling; the fold not completing by 6s (move the peak earlier or raise duration to 10 s).
**Status:** probed 2026-10-08, one 480p draft in project `effects-probe` (scene-06): the street peeled up and closed over the subject as a ceiling with the city hanging inverted; she stayed upright. One photo and one subject only.

### `architecture-wave` - Architecture wave

**Look:** Rigid buildings and bridges behind the subject bend like liquid and curl into a giant wave while the person stays crisp and unchanged.
**Route:** `i2v-first-frame`. `@Image 1` is the first frame.
**Parameters:** 7 s; ratio follows the photo (16:9 and 3:4 both seen); `generate_audio` false; draft at 480p.
**Start photo:** Person in the foreground in a low-angle wide frame, with a large rigid structure (bridge, tower, skyscraper) filling the upper frame and open sky so the warped geometry reads. Bad: structure cropped to a sliver, flat high-angle view, dense crowds, no sky.
**Beats (from the originals):**
- 0-2s: low-angle wide shot, subject poses or walks toward camera; structure looks normal.
- 2-4s: the upper structure begins to warp; the arch rotates and bends, the tower tip leans and peels.
- 4-6s: a large smooth ripple curls the tower top into a wave over the frame; slight clockwise camera roll.
- 6-7s: the warp holds at its peak around the unchanged subject.
- No cuts.
**Prompt template:**
```text
@Image 1 is the first frame. It defines {subject}, the {structure} behind {pronoun_obj}, the low-angle wide framing and the sky.
{subject} {subject_action} in the foreground, with the same face, outfit and hair in every frame. Exactly one person is in the frame. The ground, {foreground_prop} and {subject} stay rigid and unchanged.
0-2s: the {structure} looks normal and solid.
2-4s: only the {structure} begins to deform: it bends and rotates slowly with smooth liquid easing, its upper part leaning toward the camera.
4-6s: the {structure} ripples into a large wave that curls overhead in the direction of the {curl_side} of the frame, its steel and glass bands bending in long continuous arcs, while the camera rolls gently clockwise.
6-7s: the {structure} holds at the peak of the curl, frozen like a breaking wave above {subject}.
Camera: one continuous low-angle wide shot, nearly static, with a slight clockwise roll that builds from 2s to 6s and holds.
The visuals feature crisp natural daylight, photorealistic materials and clear sky showing through the curl.
```
**Slots:**
- `{subject}`, `{pronoun_obj}` ("her"/"him"): read from the photo.
- `{structure}`: the single dominant rigid structure ("the suspension bridge and the tower beside it").
- `{subject_action}`: one action only; default "stands and looks toward the camera".
- `{foreground_prop}`: read ("the lamp post"), or "the pavement" if none.
- `{curl_side}`: "top" by default; "left" or "right" when the structure sits to one side.
**Post:** none.
**QA:**
- Only the background structure deforms; the subject, ground and foreground prop stay rigid.
- Peak curl is visible in the last 2 s.
- Subject identity matches the photo at 7 s.
- Structure bends as one body, not shattered fragments.
**Risks:** The warp spreading to the subject or ground; the structure shattering instead of bending; lattice and window detail smearing; identity drift if the subject walks toward the camera (prefer a pose); the wave not reaching its peak within the short duration (the prompt already places the peak in the last 2 s).
**Status:** untested hypothesis (analysis 2026-10-08)

### `melting` - Melting

**Look:** The person's outfit and body sag into a glossy, color-matched puddle on the pavement, leaving only a hat or shoes floating in it.
**Route:** `i2v-first-frame`. `@Image 1` is the first frame.
**Parameters:** 7 s; ratio follows the photo (1:1 and 4:3 seen); `generate_audio` false (a soft wet-drip sting could help, add it in post); draft at 480p.
**Start photo:** Full-body, standing, well-lit outfit with distinct colors and accessories (hat, bag, boots) on a flat, uncluttered ground, locked-off framing. Bad: seated pose, busy ground, a body cropped at the knees, groups without a stated per-person color list.
**Beats (from the originals):**
- 0-2s: subject poses with small gaze or hand movement; camera locked off.
- 2-3s: color-matched liquid begins dripping from legs, bag and hem.
- 3-5s: the cap and head sag, the boots slump, the subject sinks to a kneel as the torso liquefies; puddles spread.
- 5-7s: the jacket flattens into a glossy marbled puddle; only hat, boots and bag fragments float on top; subject gone, street empty.
- No cuts.
**Prompt template:**
```text
@Image 1 is the first frame. It defines {subject}, the outfit, the {ground} and the locked-off framing.
Exactly one person stands in the frame until 5s. The background stays unchanged.
0-2s: {subject} stands with the same face and outfit, making only a small {small_motion}.
2-3s: the clothing begins to liquefy first: glossy liquid drips from the hem, the legs and {accessory_list}, each liquid exactly the color of its garment: {garment_color_list}.
3-5s: the {headwear} sags forward, the boots slump, and {subject} sinks slowly to a kneel as the torso turns to the same color-matched liquid; puddles spread across the {ground}.
5-7s: the liquid gathers into one glossy, reflective marbled puddle; only the {remnants} float on its surface; {subject} is gone and the empty {ground} surrounds the puddle.
Camera: locked-off static eye-level shot, no camera movement.
The visuals feature glossy liquid with sharp reflections of the sky, rich saturated garment colors and the photo's natural light.
```
**Slots:**
- `{subject}`, `{ground}`: read from the photo.
- `{small_motion}`: read a plausible one ("head turn", "hand adjustment").
- `{accessory_list}`: read (bag strap, scarf).
- `{garment_color_list}`: read every garment color ("cream from the cap and shirt, burgundy from the jacket, black from the boots").
- `{headwear}`: "cap", "hat", or "hair" if none (then say it sags without the face changing).
- `{remnants}`: items that remain, with counts ("1 cap, 2 boots and 1 bag"); default "cap and boots".
**Post:** none. Optional wet drip and splash bed via Seed Audio.
**QA:**
- Liquid colors match the garments they come from.
- Clothing liquefies first; the face is never distorted.
- By 7s the subject is gone, the remnant count matches the slot, the background is unchanged.
- Camera does not move.
**Risks:** Faces or skin melting grotesquely (the clothing-first wording reduces this); body-horror tone; puddle color mismatch; accessory counts drifting; the subject remaining as a statue; the background also melting. For a group, state the exact count and per-person colors at every stage.
**Status:** probed 2026-10-08, one 480p draft in project `effects-probe` (scene-05): clothes liquefied into colour-matched puddles, the subject knelt and dissolved, and the hat and boots were left floating on one marbled puddle.

### `burning-man` - Burning man

**Look:** A copy of the subject wrapped head to toe in living fire walks in and shakes hands with the untouched original.
**Route:** `i2v-first-frame`. `@Image 1` is the first frame; no other image roles.
**Parameters:** 7 s; ratio follows the photo (3:4 and 4:3 seen); `generate_audio` optional true with "fire crackle and low flame whoosh only" because that sound genuinely sells the effect; if the take bakes music or speech, regenerate with false and add the bed in post; draft at 480p.
**Start photo:** Standing or walking person fully visible head to footwear, medium-full body, with empty space on one side for the double to appear, ideally dusk or night on a street. Bad: cropped body, crowd, no free side, strong back light that hides the outfit.
**Beats (from the originals):**
- 0-1s: subject walks toward the camera, camera pulls back keeping her centered.
- 1-2s: she looks to frame right; orange flame glow bleeds in at the right edge.
- 2-3s: reveal: an identical double, same outfit, bag and boots, wreathed in fire stands on the right; the original stops and turns to face it.
- 3-4s: camera settles into a static two-shot.
- 4-5s: the double extends its hand; the original raises hers to meet it.
- 5-7s: handshake holds; flames flicker on the double only.
- No cuts.
**Prompt template:**
```text
@Image 1 is the first frame. It defines {subject}, the outfit, the {location} and the framing.
Exactly two people appear: the original {subject}, unburned, and one identical double covered in realistic fire. Only the double burns; the original, the ground and the {location} do not.
0-1s: the camera pulls back slowly while {subject} walks toward it, centered.
1-2s: {subject} turns to look toward the {double_side} of the frame; orange firelight flickers in from that edge.
2-3s: the double, wearing the same {outfit_details}, steps into view on the {double_side}, fire outlining the clothes and hair; {subject} stops and turns to face it; firelight shows on the ground.
3-4s: the camera settles into a static medium two-shot, the two facing each other.
4-5s: the double extends {double_hand}; {subject} raises {subject_hand} to meet it.
5-7s: the two hands clasp at the center of the frame and hold, as flames keep flickering on the double only.
Camera: one continuous eye-level take; pull back from a medium shot until 3s, then lock into a static medium two-shot.
The visuals feature warm firelight against the cool {ambient_light}, natural film detail and sharp flame edges.
```
**Slots:**
- `{subject}`, `{location}`, `{outfit_details}`: read from the photo, with every garment, bag and boot named so the double matches.
- `{double_side}`: the empty side of the photo ("right of the frame").
- `{double_hand}` and `{subject_hand}`: name by anatomy plus frame side, for example "its right hand, on the frame-left side of its body" and "her right hand, on the frame-right side of her body"; the facing pair clasps right hand to right hand.
- `{ambient_light}`: read ("blue night street light").
**Post:** none. Optional crackle bed via Seed Audio if native audio is off.
**QA:**
- Exactly two people are visible from 3s on, exactly one on fire.
- Double's outfit matches the original's, and both faces stay readable.
- The handshake shows two hands with five fingers each and no fusion.
- Fire does not spread to the original, the ground or the scene.
**Risks:** Both figures burning; a third person appearing; the double's face or outfit not matching; finger fusion at the handshake; fire spreading into the scene; crowd count changing in the background; moderation flags on fire plus a real person's face (reflect before submit; moderation rejection is evidence to diagnose, not proof of a false positive).
**Status:** untested hypothesis (analysis 2026-10-08)

### `particles` - Particles

**Look:** The subject and the world dissolve into glowing iridescent point clouds, with strobing cuts to a black void.
**Route:** `composite`. Generated clip with `@Image 1` as the first frame (single image role), plus an optional HyperFrames HUD-label overlay in post.
**Parameters:** 5 s; 16:9 or the photo's ratio; `generate_audio` false; draft at 480p. The originals run at only 8 fps; keep native 24 fps and, if the stutter look is wanted, drop to 8 fps in post with FFmpeg.
**Start photo:** One clear subject or action in a moody, dark environment (night street, wave), high contrast against a dark background. Bad: bright flat daylight, several equal subjects, a subject lost in clutter.
**Beats (from the originals):**
- 0-1.5s: real scene with a silver particle-scan overlay, flicker frames and tiny HUD boxes.
- Cut at 1.5s: pure black void, subject as a rainbow point cloud.
- Cut at 2s: back to the real scene, camera pushes in, cyan glow, bokeh particles, perspective grid.
- Cut at 3.5s: black-void point-cloud shot.
- Cut at 4s: real scene again, background fragmenting into a partial 3D scan tinted cyan, to the end.
**Prompt template:**
```text
@Image 1 is the first frame. It defines {subject}, the {environment} and the dark moody lighting.
Exactly one subject, {subject}, appears in every shot. Every on-screen box and panel is an abstract rectangle outline with no lettering.
0-1.5s: the real scene with a fine silver particle-scan overlay across {subject} and the {environment}; faint flicker frames; small empty rectangular outline boxes drift at the frame edges.
Cut to 1.5s: a pure black void; {subject} is a rainbow iridescent point cloud with the face and silhouette still readable.
Cut to 2s: the real scene again; the camera pushes in closer; cyan glow, floating bokeh particles, a perspective grid on the ground and thin scan lines drifting across the frame.
Cut to 3.5s: the black void with the point-cloud {subject}, brighter and denser.
Cut to 4s: the real scene; the background fragments into a partial 3D scan tinted cyan while {subject} stays solid and sharp to the end.
Camera: mostly static eye-level wide shot with a slow push in from 2s, ending on a medium wide framing of {subject}.
The visuals feature luminous cyan, silver and iridescent particles on dark tones, with particles never covering the face.
```
**Slots:**
- `{subject}`: read from the photo ("the hooded man in the white tracksuit").
- `{environment}`: read ("rain-wet brick street at night", "dark wave face").
**Post:** Optional HUD data labels (scan IDs, coordinates, drift readings) in HyperFrames or html-graphic-render over the clip, in small type at the edges; FFmpeg `fps=8` for the stutter look. Readable text exists only in this layer.
**QA:**
- Hard cuts occur near 1.5s, 2s, 3.5s and 4s.
- Point-cloud shots keep the subject's silhouette and face readable.
- No lettering or digits inside the generated clip.
- Particles do not hide the face in real-scene shots.
**Risks:** Gibberish HUD text if the model invents labels (the template keeps boxes empty and puts text in post); identity lost in the point-cloud shots; over-bright particles hiding the face; cut count drifting. Lowest-confidence effect in this category: the page gave one line and the two examples differ (night street and surf), so treat the beats as indicative.
**Status:** untested hypothesis (analysis 2026-10-08)

### `lidar` - Lidar transition

**Look:** A neon-cyan point-cloud flythrough of the location solidifies into the real photographed scene with the person scanned into place.
**Route:** `i2v-last-frame`. `@Image 1` is the last frame (the user's photo); no first-frame image. If the live tool does not accept a last-frame-only role, fall back to `i2v-first-and-last` with a generated black-and-cyan ground-plane first frame from Seedream (same ratio as the photo).
**Parameters:** 7 s; ratio follows the photo (3:4 and 4:3 seen); `generate_audio` false (a rising electronic hum would help; add it in post); draft at 480p.
**Start photo:** Person in a wide outdoor location with distinct foreground posts or rails and a skyline or tree line, so the scan has geometry to trace. Bad: indoor flat wall, close-up face, cluttered scene without clear objects, heavy overexposure.
**Beats (from the originals):**
- 0-0.5s: black frame with a bright cyan ground edge rising from the bottom.
- 0.5-2s: fast low forward dolly over a roiling cyan point-cloud ground with heavy radial blur; wireframe posts and rail trace in.
- 2-3.5s: a glowing particle skyline builds behind the posts; the camera passes the nearest post.
- 3.5-4.5s: a cyan hologram figure of the subject appears beside a post; the sky lightens and the scan dissolves into real color.
- 4.5-7s: the photo-real scene is solid; the camera decelerates and settles on the portrait.
- No cuts.
**Prompt template:**
```text
@Image 1 is the last frame. It defines the final location, the {foreground_objects}, {subject} and the settled medium framing.
One continuous first-person forward dolly with no cuts.
0-0.5s: a black frame with a bright cyan glowing ground-plane edge rising from the bottom.
0.5-2s: a fast low dolly forward over a roiling cyan point-cloud ground with heavy radial motion blur; glowing wireframe outlines of {foreground_count} {foreground_objects} trace in along the way.
2-3.5s: a glowing particle skyline of {background_landmarks} builds behind them as the camera passes the nearest {foreground_object}.
3.5-4.5s: a cyan hologram figure of {subject} appears beside the {foreground_object}; the sky lightens and the scan dissolves into real color, completed at 4.5s.
4.5-7s: the photographed scene is fully solid; the camera decelerates to a gentle slow dolly and settles in the exact composition of @Image 1, with {subject} standing {pose}.
Color appears only during the dissolve; before 3.5s everything is cyan on black. The visuals feature luminous cyan points on black, heavy radial blur on the fast run, and a glow that fades to natural exposure at the end.
Camera: wide-angle first-person dolly forward at low height, fast at the start, decelerating from 4s, ending in the framing of @Image 1.
```
**Slots:**
- `{foreground_objects}` / `{foreground_object}` / `{foreground_count}`: the posts, rails or trees in the photo, with the exact count visible ("3 wooden bollards").
- `{background_landmarks}`: skyline or tree line from the photo ("a dense downtown skyline").
- `{subject}` and `{pose}`: read ("the woman", "turned slightly toward the camera").
**Post:** none. Optional rising synth hum via Seed Audio.
**QA:**
- No color before about 3.5s; the dissolve completes near 4.5s.
- Wireframe objects match the photo's objects and count.
- The camera decelerates; the final 2 s match `@Image 1`.
- The subject does not appear as a real person before the dissolve.
**Risks:** The page text describes a tilting world with sliding objects, but the footage shows a point-cloud flythrough; this recipe follows the footage (the discrepancy is unresolved and the page text may belong to another effect). The scan not matching the photo's objects; the subject appearing early as a real person; overglow washing out the final frame; constant camera speed; identity drift at materialisation; last-frame-only conditioning support is unverified. Confidence is medium.
**Status:** untested hypothesis (analysis 2026-10-08)

### `earth-zoom` - Earth zoom

**Look:** One unbroken dive from orbit through clouds and over the city that lands in front of the person in the photo.
**Route:** `i2v-last-frame`. `@Image 1` is the last frame (the user's street photo); no first-frame image. If last-frame-only is unsupported, fall back to `i2v-first-and-last` with a Seedream-generated low-orbit planet frame at the same ratio as the photo.
**Parameters:** 10 s; ratio follows the photo (9:16 and 16:9 seen); `generate_audio` false (a rushing-air sting then street ambience would help; add it in post); draft at 480p. The dive is about 6 s and the settled shot about 4 s.
**Start photo:** Street-level eye-level medium or full shot of a person standing on a sidewalk or intersection, photoreal daylight, with the street receding behind or beside them. Bad: indoor, night, close-up face, a location implausible from above (interior courtyard, forest trail).
**Beats (from the originals):**
- 0-1s: low Earth orbit, black space, bright blue curved limb, patchy clouds; the dive starts.
- 1-2s: dive through a thick white cloud deck with heavy blur; emerges over forest and river terrain.
- 2-4s: rapid descent over a city grid and winding river along an avenue; radial zoom blur.
- 4-6s: drops between facades to sidewalk level and decelerates; trees, pedestrians and a distant figure come into focus.
- 6-10s: camera at rest or slowly pushing in on the person, who looks aside amid ambient street motion; ends in a medium shot.
- No cuts.
**Prompt template:**
```text
@Image 1 is the last frame. It defines the final street, the buildings, the daylight and {subject} standing in the final medium shot.
One continuous plunge with no cuts, ending exactly on @Image 1. The video opens in low Earth orbit: black space above, the curved bright blue edge of the planet, patchy white clouds below.
0-1s: the camera dives straight down toward the planet at accelerating speed.
1-2s: it plunges through a thick white cloud deck with heavy blur and emerges over {terrain}.
2-4s: it descends rapidly over a city grid and a winding river, following {road_type} with strong radial zoom blur as the buildings rush past.
4-6s: it drops between the facades to sidewalk level and decelerates sharply; {tree_count} trees, {pedestrian_count} pedestrians and traffic come into focus along the street of @Image 1; {subject} first becomes visible at 5s.
6-10s: the camera comes to rest at eye level and pushes in slowly on {subject}, who {end_action}, while street motion continues.
Camera: top-down orbital start, exponential dive, rapid ease-out at eye level at 5s, then a slow push in, ending in the framing of @Image 1.
The visuals feature photorealistic daylight, a motion-blurred descent and the sharp color of @Image 1 in the final seconds. All signs and screens stay plain and unlettered.
```
**Slots:**
- `{subject}`: read from the photo.
- `{terrain}`: "forest and a river" by default; match the photo's climate (desert, coast).
- `{road_type}`: "a tree-lined avenue" or as read from the photo's street.
- `{tree_count}` / `{pedestrian_count}`: count what the photo shows; default "3" and "4".
- `{end_action}`: read ("stands relaxed and glances to the side").
**Post:** none. Optional wind and street ambience via Seed Audio.
**QA:**
- Orbit, clouds, terrain, avenue, facade drop and eye-level stop appear in that order, without cuts.
- Subject is absent until about 5s and matches the photo at the end.
- The final 2 s match `@Image 1`'s street and framing.
- No lettering on signs or screens.
**Risks:** City geography not matching the photo's street; the subject appearing during the dive; a scale seam at the cloud break; motion blur hiding the landing so the person looks new (identity drift); 10 s costs more than the shorter recipes; last-frame-only conditioning is unverified.
**Status:** untested hypothesis (analysis 2026-10-08)

### `blue-depth` - Blue depth

**Look:** A person held perfectly still against a wall of dark blue water while fish and jellyfish drift past in slow motion.
**Route:** `i2v-first-frame`. `@Image 1` is the first frame. Whether the original adds the water wall or needs it in the photo is unknown, so this recipe adds it: if the photo has no water wall, the orchestrator first makes a start still with `seedream_edit_image` (keep the person unchanged, replace the background with a dark blue aquarium glass wall with no fish), checks identity against the photo, and uses that still as `@Image 1`.
**Parameters:** 8 s (the originals ran 12 s; shorter limits identity drift); ratio follows the photo (4:3 and 9:16 seen); `generate_audio` false (an underwater hum is a post bed); draft at 480p.
**Start photo:** Medium or waist-up person facing slightly off camera, simple clothing, even lighting. Bad: busy colorful background, strong motion blur, backlit silhouette, hands near the face.
**Beats (from the originals):**
- 0-2s: subject stands centered or left looking to the side; fish and jellyfish already drift in the water wall.
- 2-4s: subject slowly turns the head to the camera, then settles neutral.
- 4-12s: subject essentially frozen; fish at different depths, some passing in front of the clothing; jellyfish drift upward; faint light shifts; very slow push-in.
- No cuts.
**Prompt template:**
```text
@Image 1 is the first frame. It defines {subject}, the clothing and the {wall_state}.
Exactly one person stands in the frame. Only the water creatures move; {subject}'s body, clothing and the camera stay almost still after one slow head turn.
0-2s: {fish_count} fish and {jelly_count} jellyfish drift slowly through the deep blue water wall behind {subject}, at different depths.
2-4s: {subject} turns {pronoun} head slowly to face the camera and settles with a neutral expression.
4-8s: {subject} holds still; the fish glide across the frame at different depths, {front_count} of them passing in front of the clothing without touching the face, while the jellyfish drift gently upward with a slow soft pulse about once every 3 seconds; faint blue light ripples across the water wall.
Camera: locked-off medium shot with an extremely slow push in from the opening framing to a slightly tighter medium shot over the whole clip, shallow depth of field.
The visuals feature deep blue low-key light, a moody hypnotic mood and soft highlights on the glass.
```
**Slots:**
- `{subject}`, `{pronoun}`: read from the photo.
- `{wall_state}`: "dark blue aquarium glass wall behind" (confirmed present in the photo or added by the Seedream prep step).
- `{fish_count}` / `{jelly_count}` / `{front_count}`: defaults "6", "3", "2".
**Post:** none. Optional underwater hum via Seed Audio.
**QA:**
- Fish count stays near the stated count and species do not change.
- No fish crosses the face; fish pass in front of clothing only.
- Subject stays still after the 2-4s head turn, same identity at 8s.
- Jellyfish pulse slowly.
**Risks:** The water wall origin is unconfirmed in the originals (the recipe adds it; if the Seedream prep alters the person, rerun the edit before submitting); fish counts and species changing; fish merging with the subject or crossing the face; jellyfish pulsing too fast; micro-motion identity drift over long durations (hence 8 s); fish passing through the body. Confidence is medium.
**Status:** untested hypothesis (analysis 2026-10-08)

### `windows` - Windows

**Look:** Stacked retro desktop error panels, swarming cursors and blue-screen layers strobe over blue-toned CRT footage.
**Route:** `composite`. Generated clip with `@Image 1` as the first frame (single image role) containing only abstract panel shapes, plus a HyperFrames overlay in post for all readable error text.
**Parameters:** 5 s; 16:9 or the photo's ratio; `generate_audio` false; draft at 480p. The originals run at 10 fps; keep native 24 fps and, if the stutter look is wanted, drop to 10 fps in post with FFmpeg.
**Start photo:** High-contrast, cool or blue-toned action or street shot (skateboarder, crouching crew), subject clearly readable and moving, with empty negative space for panels. Bad: warm flat portrait, subject filling the frame edge to edge, no motion.
**Beats (from the originals):**
- 0-1s: heavy blue duotone with CRT feel; blue-screen text blocks, stacked error popups and scattered cursors.
- Cut at 1s: new popups with progress bars and file-explorer windows; cursor swarm multiplies; pixel corruption on the subject.
- Cut at 2s: popups freeze in stacks at the edges; small duplicated thumbnails of the clip; scanline banding rolls.
- 3-5s: command-prompt and run-dialog windows, more error stacks, strobing color bars at the edge; hard glitch cuts every 0.3-1 s; the underlying footage keeps moving.
**Prompt template:**
```text
@Image 1 is the first frame. It defines {subject}, the {location} and the framing; {subject} keeps moving naturally ({action}) in every shot, unchanged.
The whole clip is heavily blue-duotone with a CRT look: fine horizontal scanlines rolling slowly downward and a slight phosphor glow. Every panel holds only abstract bars and color blocks, and every panel stays clear of {subject}'s face.
0-1s: stacked rectangular panels with title bars, solid blue full-screen panels and small arrow cursors fill the empty areas of the frame, with {cursor_count} cursors in total.
Cut to 1s: a new layout of {panel_count} overlapping panels with progress bars and folder-style windows, and a swarm of about 12 cursors; blocky pixel corruption flickers on {subject}.
Cut to 2s: the panels freeze in stacks along the frame edges with 4 small duplicated thumbnails of the clip; scanline banding rolls.
3-5s: rapid glitch cuts about every half second swap in dark terminal-style panels and dialog boxes, with colored bars strobing at the frame edge; the footage of {subject} keeps moving beneath.
Camera: locked off at {shot_size}, no pan or tilt.
The visuals feature a cold blue duotone, scanlines and a phosphor glow.
```
**Slots:**
- `{subject}`, `{location}`, `{action}`: read from the photo ("the skateboarder", "an empty parking lot", "preparing to ollie").
- `{cursor_count}`: default "6".
- `{panel_count}`: default "7".
- `{shot_size}`: read from the photo ("wide shot", "medium shot").
**Post:** Error-dialog titles and body text, a crash-screen text block and terminal lines are built in HyperFrames or html-graphic-render as generic, brand-neutral wording (no operating-system logos, flag or trademarked phrasing) and overlaid in FFmpeg. Optional FFmpeg `fps=10` for the stutter. All readable text exists only in this layer; the generated clip has none.
**QA:**
- Hard glitch cuts at about 1s and 2s, then rapid cuts in 3-5s.
- Panels hold abstract shapes only, with no readable text, digits or logos.
- The subject stays readable and uncovered and keeps moving.
- Blue duotone and scanlines persist throughout.
**Risks:** Gibberish text if the model writes labels (the template keeps panels abstract and moves text to post); panels covering the subject; text baked into video violating the no-overlay rule; trademark risk from reproducing a real operating system's interface; cut timing drifting (timestamps are a time budget, not frame-accurate); stutter look needing post. Confidence is medium and the page gave one line.
**Status:** untested hypothesis (analysis 2026-10-08)
