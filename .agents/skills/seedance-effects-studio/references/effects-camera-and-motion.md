# Effect recipes - Camera and motion

Nine effects whose identity is a camera path, a scale shift or a staged physical event: an orbit around a car, a tilting room, a giant in a street, a freeze-and-orbit, a flip into another scene, a weightless fall, a paper-theatre walk and a multi-copy slide. Every recipe reuses one skeleton: `@Image N` role line, subject and action with exact counts, scene, visual style, a timestamped camera line (concrete move + start + end, hard cuts as `At Ns, cut to ...`), and an observable end state. Prompts carry no text of any kind; anything that must read as graphics is added in post.

## Menu rows

| id | label | route | duration | start photo |
| --- | --- | --- | --- | --- |
| `wild-ride` | Wild ride | `i2v-first-frame` | 10 s | Car with a person leaning out, open space |
| `incline` | Incline | `i2v-first-frame` | 7 s | Calm person, visible floor, some clutter |
| `street-colossus` | Street colossus | `i2v-first-frame` | 10 s | Full-body standing person, outfit clearly visible |
| `tracking` | Tracking | `composite` | 5 s | Performer in motion, hands and face clear |
| `bullet-time` | Bullet time | `i2v-first-frame` | 15 s | Seated person holding a drink, medium shot |
| `high-flip` | High flip | `i2v-first-and-last` | 9 s | Person in a distinctive place, headroom above |
| `floating-fall` | Floating fall | `i2v-first-frame` | 12 s | Person holding 2-4 clear items outdoors |
| `moonwalk` | Moonwalk | `i2v-first-and-last` | 15 s | Full-body person, clean side-on stance |
| `studio-slide` | Studio slide | `i2v-first-frame` | 8 s | Full-body fashion photo, plain solid backdrop |

---

### `wild-ride` - Wild ride
**Look:** One unbroken camera orbit around a vehicle doing a tyre-smoking burnout, sweeping from ground level up to overhead and back down while a person leans out of the window.
**Route:** `i2v-first-frame`. `@Image 1` is the first frame (the user's vehicle photo). No second image: Seedance 2.5 cannot mix a first-frame image with `reference_image` inputs, so the vehicle's identity comes from the photo alone.
**Parameters:** duration 10 s; ratio follows the photo (the originals were 9:16 and 4:3); `generate_audio` false by default, true is justified only for an engine and tyre-squeal sting, in which case the prompt adds `Audio includes engine roar and tyre squeal, no music, no speech.`; draft at 480p.
**Start photo:** A vehicle with exactly one person visible in or leaning from a window, ideally a low three-quarter rear or side view on an open road or plaza with room for smoke and a crowd. Bad inputs: vehicle fully cropped, interior-only shots, person fully inside, more than one person hanging out, a dense parking lot with no clear space to orbit.
**Beats (from the originals):**
- 0-2.5 s: ground-level rear three-quarter wide, camera tracks the sliding vehicle in a full burnout, person leaning out of the driver window, thick tyre smoke, city towers behind.
- 2.5-3 s: whip up to a near top-down view with radial motion blur (a blur, not a cut).
- 3-8.5 s: high overhead-oblique orbit around the drifting vehicle; person looks up, points, gives a thumbs-up; crowd and crosswalk come into view.
- 8.5-9.5 s: fast rotating swoop back down.
- 9.5-10 s: low side track beside the front wheel, person far out of the window with a smirk.
No hard cuts; the analysis confirmed one continuous move (the two apparent cuts are motion-blurred whips).
**Prompt template:**
```text
@Image 1 is the first frame.
{vehicle} performs a continuous tyre-smoking burnout on {surface} in {setting}, spinning in place in thick white smoke. Exactly one person, {person}, leans out of the {window_side} window and stays attached to the vehicle for the whole clip, {person_gesture}. {crowd_line}
The visuals feature hard daylight, a wide-angle lens with strong foreground blur, heavy radial motion blur on the fast swoops, and saturated colour.
One continuous take with no cuts, the camera orbiting the vehicle counter-clockwise as seen from above at a constant direction. 0-2.5s: low ground-level {opening_view} wide, tracking the sliding vehicle. At 2.5s: swoop up in a fast arc to a high overhead-oblique view. 3-8.5s: circle the vehicle from high above. At 8.5s: fast rotating swoop back down. 9.5-10s: low side track beside the front wheel, ending framed on the person leaning far out.
The vehicle keeps {wheel_count} wheels and one body shape throughout, and the person's face and clothes stay the same as in the first frame. Every sign, plate and surface is plain and unlettered.
```
**Slots:**
- `{vehicle}`: read from the photo (colour, body type, notable parts such as a rear wing).
- `{surface}`, `{setting}`: read from the photo; default "an open tarmac plaza" / "a neon-lit city district".
- `{person}`: read from the photo (clothing, hair).
- `{window_side}`: read from the photo (driver window by default).
- `{person_gesture}`: default "looking up, pointing with the right hand on the frame-left side of the picture, then gripping the mirror with a smirk"; swap in the hand that is outside the window in the photo, always named by anatomy plus frame side.
- `{crowd_line}`: "A small crowd of about {N} onlookers stands behind red-and-white barriers." only if the photo shows space for one; else omit.
- `{wheel_count}`: count from the photo (four for a car).
- `{opening_view}`: the angle the photo already shows (for example "front three-quarter with the driver side nearest the camera"); never contradict the first frame. When the photo shows a parked car, write that it launches from standstill into the burnout and the smoke builds from the first second.
**Post:** none. Optional engine/tyre ambience bed via Seed Audio if native audio stays off.
**QA:**
- One continuous clip, no hard cut anywhere (whips with blur are acceptable).
- Camera visibly goes low, then overhead, then low again, rotating the same direction throughout.
- Exactly one person, attached to the vehicle in every frame, no duplicate or detached limb.
- Wheel count and body shape unchanged during the overhead pass; no legible licence plate or sign text.
- Ends on a low side view with the person leaning out.
**Risks:** Person detaching or doubling; wheel count or geometry drifting on the overhead pass; orbit direction flipping mid-clip; mushy crowd faces; invented plate and billboard lettering; motion blur swallowing identity; a single first frame gives no side or rear view of the vehicle, so unseen faces of the car are invented.
**Status:** probed 2026-10-08, one 480p draft in project `effects-probe` (scene-03): the burnout, the overhead sweep and the return to a low side track all landed, with one person attached to the car throughout. The opening view must follow the photo (the template had assumed a rear view). The template was amended after review (a positive unlettered-surfaces clause was added and the gesture default now names the hand by anatomy and frame side); the amendment is not re-probed.

---

### `incline` - Incline
**Look:** The whole room tilts like a ship's deck and loose objects and animals slide past a subject who stays calmly in place.
**Route:** `i2v-first-frame`. `@Image 1` is the first frame; no other image roles.
**Parameters:** duration 7 s; ratio follows the photo (originals 4:3 and 9:16); `generate_audio` false by default (a soft rolling-and-scraping sting would help but is optional); draft at 480p.
**Start photo:** A person posed calmly, seated or standing, in a wide enough shot to show a visible floor with some empty floor space and a few background items (desk, sofa, vending machine). Bad inputs: tight portrait, no visible floor, a person mid-action or mid-pose, an empty void background, a busy crowd.
**Beats (from the originals):**
- 0-1.5 s: level locked wide, subject doing a calm activity (typing, holding a cup, shielding eyes).
- 1.5-3 s: the room rolls about 15-25 degrees; windows and furniture slant together; first small items slide in.
- 3-4.5 s: peak tilt; larger sliders cross the floor (a cat, a person off a sofa, an empty rolling chair); subject sips and never reacts.
- 4.5-7 s: tilt eases back to level, sliders exit, subject and composition return to the opening frame.
No hard cuts.
**Prompt template:**
```text
@Image 1 is the first frame.
{subject} stays calmly in place {pose_clause}, never reacting and never sliding, {held_item_clause}. The whole room tilts around them like a ship's deck while the {slider_count} listed things slide across the floor. {fixed_items} stay put.
Scene: {setting}, with a clear stretch of floor on the {low_side} side of the frame.
The visuals feature {lighting_from_photo} and a slightly wide lens with the subject kept centred.
Single continuous take, no cuts. 0-1.5s: level, locked-off wide shot. 1.5-3s: the camera rolls so the {low_side} side drops lower, reaching a 20-degree tilt; walls, windows and furniture tilt together with the camera. 3-4.5s: at peak tilt, these slide toward the {low_side} side one after another and exit frame: {sliders_in_order}. 4.5-7s: the camera rolls back to level, the last sliders have left, and the frame ends level with {subject} in the exact opening pose.
Exactly {slider_count} sliding things appear in total: {slider_names}. Every sign, label and surface in the room is plain and unlettered.
```
**Slots:**
- `{subject}`, `{pose_clause}`, `{setting}`, `{lighting_from_photo}`: read from the photo.
- `{held_item_clause}`: what the subject holds, read from the photo; when the subject holds nothing, delete the slot together with the comma before it.
- `{low_side}`: "frame-left" by default; choose the side with more open floor.
- `{sliders_in_order}`: three to four items chosen to fit the setting, each named with colour and size, e.g. "a red rubber ball, three loose sheets of paper, a ginger cat, an empty mesh chair on wheels"; default pair for a vending-machine scene: "a crate of glass bottles, a closed umbrella, a plastic bag".
- `{slider_count}`: the number of items in `{sliders_in_order}`; `{slider_names}` repeats them by short name.
- `{fixed_items}`: the visible objects that must not move (laptop, mug, desk, chair); list at least two, because the template says "stay put".
- Each slider must start on the floor or on a surface the prompt names (for example "slides off the desk edge and across the floor") and must travel toward `{low_side}`.
**Post:** none. Optional sliding/scraping ambience via Seed Audio.
**QA:**
- Visible room roll peaks near 15-25 degrees and returns to level by the end.
- Subject keeps the same pose and does not slide or react.
- Sliders enter in the listed order, all toward the same side; count equals `{slider_count}`.
- Walls and furniture tilt coherently with the floor; gravity direction matches the slide.
- Last frame matches the first frame's composition, floor clear.
**Risks:** Subject also sliding or changing pose; furniture not tilting with the room; object or animal counts and species drifting; gravity contradicting the tilt; background architecture staying level while the floor tilts.
**Status:** probed 2026-10-08, one 480p draft in project `effects-probe` (scene-02): the room rolled and levelled again, the paper stack, cart and cat slid, the subject stayed put. The prompt-review fix (sliders start on a named surface, fixed items listed) is now in the template. The template was amended after review (a positive unlettered-surfaces clause was added); the amendment is not re-probed.

---

### `street-colossus` - Street colossus
**Look:** A person as a skyscraper-height giant striding through a real city avenue while tiny pedestrians and taxis give the scale.
**Route:** `i2v-first-frame`. `@Image 1` is the first frame, a start frame built by the orchestrator: generate with `seedream_generate_image`, binding the user's person photo as `@Image 1` for identity (the live edit tool needs a point or bbox and cannot re-costume a whole image), an extreme low-angle shot of the same person at building height on a city street (outfit kept, face kept, feet planted on the road, tiny pedestrians and taxis below). Scale cannot come from the raw photo because its background has no city. Fallback if the Seedream frame fails review: attach the raw photo as the sole appearance reference (`reference_image`) instead of a first frame and keep the same prompt body (this changes the route; do not mix it with a first frame). Fallback variant line, used instead of the template's first line: `@Image 1 defines the person's face, hair and outfit; use it only for the person; ignore its pose and background.`
**Parameters:** duration 10 s; ratio follows the start frame (originals 3:4 and 16:9); `generate_audio` false by default (distant sirens and traffic hum would help but belong in a Seed Audio bed); draft at 480p.
**Start photo:** Full-body or three-quarter standing person, clear outfit silhouette, face visible and facing forward. Bad inputs: seated or cropped at the knees, heavy occlusion by bags or coats, a face turned away, strong outdoor perspective that would fight the worm's-eye view.
**Beats (from the originals):**
- 0-3.7 s: extreme low worm's-eye wide, slow backward track; the giant strides toward camera at skyscraper height, small pedestrians run, taxis line the street.
- 3.7 s: hard cut.
- 3.7-7.1 s: wide point of view from inside a vehicle cabin (rounded black window frame), glass towers and a helicopter; she is half behind a tower, steps into view, looks up at the helicopter; slow pan.
- 7.1 s: hard cut back to the low street framing.
- 7.1-10 s: extreme low-angle up-shot, she has stopped, one hand flat on a glass tower, head tilted up, hair blowing, tiny people and cars far below.
Two hard cuts, written below at 4 s and 7 s.
**Prompt template:**
```text
@Image 1 is the first frame.
{subject} is a giant as tall as the surrounding skyscrapers, feet planted on the road of a dense {city_style} avenue, wearing {outfit_lock}. Normal-size pedestrians, about {pedestrian_count} visible, run along the pavement and {taxi_count} yellow taxis at ordinary car scale queue on the street far below the giant's knees.
The visuals feature handheld documentary realism, hazy daylight, and glass towers reflecting the giant.
0-4s: extreme low worm's-eye wide shot, the camera slowly tracking backward as the giant strides toward it, feet always touching the street.
At 4s, cut to a wide point-of-view shot from inside a vehicle cabin, a rounded black window frame in the foreground, glass towers and exactly one helicopter beyond; the giant stands half hidden behind a tower, steps into view and looks up at the helicopter; the camera pans slowly to the right.
At 7s, cut back to the extreme low-angle street view: the giant has stopped and rests the {tower_hand} flat against a glass tower, head tilted up, hair blowing in the wind, tiny pedestrians and cars far below.
The giant's face, hair and outfit are identical in all three shots, and the buildings, taxis and people keep their small scale. Every sign, taxi door and wall surface is plain and unlettered.
```
**Slots:**
- `{subject}`: read from the photo (apparent age, hair).
- `{outfit_lock}`: precise garment list with colours and patterns read from the photo; this is the only place the outfit is described.
- `{city_style}`: default "glass-and-steel downtown".
- `{pedestrian_count}`: default "twelve"; `{taxi_count}`: default "four".
- `{tower_hand}`: default "right hand on the frame-right side of the picture"; name the hand by anatomy plus frame side.
**Post:** none. Optional crowd, helicopter and traffic bed via Seed Audio.
**QA:**
- Cuts land near 4 s and 7 s; shots 1 and 3 share the low street framing.
- Giant reads building-tall in all three shots with feet touching the street.
- Pedestrians and taxis stay car and human scale; helicopter count is one in shot 2.
- Face, hair and outfit identical across the three shots.
- No readable lettering on shirts, signs or taxis.
**Risks:** Scale collapsing into a normal-sized person; feet floating or not touching the street; outfit pattern drifting between shots; inconsistent glass reflections; helicopter count; mushy crowd faces; a single continuous prompt loses scale, so the three-shot cut list is mandatory; identity drift on the extreme scale change. Probe result: a second helicopter appeared at about 6 s despite 'exactly one'.
**Status:** probed 2026-10-08, one 480p draft in project `effects-probe` (scene-01): the three shots and both cuts landed (low striding giant, circular window POV with one helicopter, low shot with a hand on a tower); the Seedream giant start frame worked first try. One photo and one subject only. A defect scan found a second helicopter drifting in at about 6 s although the prompt asks for exactly one. The template was amended after review (a positive unlettered-surfaces clause was added and the tower hand is now a named slot); the amendment is not re-probed.

---

### `tracking` - Tracking
**Look:** A computer-vision HUD: thin white tracking brackets, connecting lines and coordinate readouts glued to a moving performer, over a tilted, glitch-cut, low-frame-rate shot.
**Route:** `composite`: a Seedance `i2v-first-frame` clip (`@Image 1` is the first frame, the user's performer photo) followed by a deterministic HyperFrames overlay and an FFmpeg frame-rate pass.
**Parameters:** duration 5 s; ratio 16:9 recommended (originals 16:9), otherwise follows the photo; `generate_audio` false by default; draft at 480p.
**Start photo:** A performer in motion or posed with face, both hands and any held object clear and unobstructed (rapper with a mic, dancer). Bad inputs: face hidden by a hat shadow, hands out of frame, several overlapping people, a flat locked-off setting with no depth.
**Beats (from the originals):**
- 0-1.3 s: low dutch angle, slow rotation around the lead performer raising both hands; teal haze, tangled cables.
- 1.3-3.4 s: glitch cuts to a side angle then a front angle, performer points at the lens; drummer behind.
- 3.4-4.4 s: glitch cut to a tight close-up then a medium shot; a second performer enters from frame-right.
- 4.4-5.2 s: low-angle medium, hands framing the head.
The written prompt uses three cuts, at 1 s, 3 s and 4 s; the front angle comes from a camera arc, not a fourth cut. The original overlay: white square corner-bracket boxes on face, hands and mic, thin lines linking them, small coordinate readouts and a faint grid, red-blue edge fringing, 8-12 fps stutter. The page description was thin, so the overlay specifics are less certain than the camera work.
**Prompt template:**
```text
@Image 1 is the first frame.
{subject} performs {action} in {setting}, moving continuously with {key_gestures}. {second_performer_clause}
The visuals feature cool teal-green haze, hard rim light, tangled stage cables, a clean uncluttered picture with background screens showing blank glowing teal panels, and thin horizontal glitch bands at each cut.
Rolling dutch-angle camera. 0-1s: low dutch angle, slowly orbiting counter-clockwise around {subject}, ending on {subject} raising both hands. At 1s, cut to a side angle, the camera arcing to a front angle by 3s with {subject} pointing at the lens. At 3s, cut to a tight close-up of the face and raised hand, pulling back to a medium shot by 4s. At 4s, cut to a low-angle medium shot with both hands raised around the head, ending held on that pose.
{performer_count_line}
```
**Slots:**
- `{subject}`, `{action}`, `{setting}`, `{key_gestures}`: read from the photo.
- `{second_performer_clause}`: "A {second_performer} enters from the frame-right edge at 3s." only if the user wants a second target; else omit.
- `{performer_count_line}`: "Exactly one performer is visible in the final shot." by default, "Exactly two performers are visible in the final shot." with the clause above.
**Post:** Required. Keep the generated footage graphic-free and add the HUD in HyperFrames: (1) track the performer in the finished clip with a person/pose detector and export per-frame boxes for face, each hand and any held object to JSON; (2) build a HyperFrames composition that draws the thin white square brackets, straight connecting lines, a faint grid with tick marks and small numeric readouts driven from that JSON, so all text and geometry are exact and deterministic; (3) add the red-blue edge fringe and glitch bands at the detected cut seconds; (4) FFmpeg `fps=12` (or 8) on the final composite for the surveillance stutter. Detect cut seconds with FFmpeg scene detection because Seedance timestamps are a budget, not edit points.
**QA:**
- Generated clip contains no brackets, lines, grid, numbers or letters anywhere, including background screens.
- Three cuts land near 1 s, 3 s and 4 s with glitch bands.
- Performer count matches `{performer_count_line}`; face and hands visible in each shot.
- After post: brackets stay attached to face, hands and mic through every cut.
**Risks:** The model drawing its own gibberish HUD or screen lettering despite the clean-picture wording; tracking drift when a cut changes the subject's scale; hands lost behind the mic; thin source description (confidence medium); several cuts in 5 s can reduce identity stability.
**Status:** untested hypothesis (analysis 2026-10-08)

---

### `bullet-time` - Bullet time
**Look:** A server trips and sends food flying, time freezes, and the camera makes one full 360-degree orbit around the calm seated subject before everything snaps back and ends on a smirk.
**Route:** `i2v-first-frame`. `@Image 1` is the first frame (the user's seated photo); the server and the flying food are invented by the prompt.
**Parameters:** duration 15 s; ratio follows the photo (originals 3:4 and 16:9); `generate_audio` false by default (a low whoosh and a pause in ambience at the freeze would help, so an optional Seed Audio bed in post is preferred); draft at 480p.
**Start photo:** A person seated at a table or booth, facing the camera in a medium shot, holding a drink with a straw, with clear space behind and around the table for an orbit. Bad inputs: standing person, extreme close-up, cluttered table covered in objects, a person in profile, a wall directly behind that blocks the orbit.
**Beats (from the originals):**
- 0-2 s: static eye-level ultra-wide; subject sips with eyes closed; server walks up behind carrying a tray of eggs, bacon and a coffee pot.
- 2-3 s: server trips, tray contents launch; subject does not react.
- 3-9 s: time freezes with every item hanging in mid-air; camera makes one counter-clockwise 360-degree orbit (left profile, behind, right profile, three-quarter front), ultra-wide with barrel distortion.
- 9-10 s: camera returns to the front; items arc back and land on the tray.
- 10-13 s: static front; subject opens eyes, looks at the server, who walks off; subject smirks.
- 13 s: hard cut to a tight, longer-lens shallow-focus close-up of the lower face sipping through the straw, ending on a smug smile (13.1-15 s).
One hard cut, at 13 s.
**Prompt template:**
```text
@Image 1 is the first frame.
{subject} sits at {table_setting} holding {drink}, and stays completely still through the freeze. Exactly one {server}, {server_look}, walks up behind them with a tray carrying {tray_items}.
The visuals feature {lighting_from_photo}, an ultra-wide lens with strong barrel distortion during the orbit, and crisp frozen detail.
0-2s: static eye-level ultra-wide shot. At 2s the server trips and the tray contents launch: exactly {item_counts}. At 3s time freezes: every item hangs motionless in the air, the coffee pot with a spiral stream of coffee, the server upright and stunned. 3-9s: the camera makes exactly one full 360-degree orbit counter-clockwise at constant speed around {subject}, passing left profile, behind, right profile and three-quarter front, returning to the front. 9-10s: time resumes, the items arc down and land on the tray. 10-13s: static front shot; {subject} turns to the server, who walks away, and turns back with a small smirk.
At 13s, hard cut to a tight longer-lens close-up with shallow focus of {subject}'s lower face sipping through the straw, ending on a smug smile.
```
**Slots:**
- `{subject}`, `{table_setting}`, `{drink}`, `{lighting_from_photo}`: read from the photo.
- `{server}`, `{server_look}`: default "waitress" / "in a red uniform with a white apron"; adapt to the setting (barista, flight attendant).
- `{tray_items}`: default "two plates with fried eggs and bacon and a glass coffee pot".
- `{item_counts}`: default "two plates, two fried eggs, three bacon strips and one coffee pot pouring coffee".
**Post:** Optional: a freeze whoosh and ambience dip, plus the room tone, as a Seed Audio bed; no overlay needed.
**QA:**
- Hard cut near 13 s into a tight close-up; no other cut.
- Orbit completes one full turn, in one direction, during the freeze.
- Item count in the air matches `{item_counts}`; none fall before the freeze or merge with the subject.
- Subject head and hands do not move during the freeze; exactly one server before and after.
- Ends on a smirk in the close-up with no readable lettering.
**Risks:** Item counts and physics drifting; subject moving during the freeze; orbit stopping short of 360 degrees; server duplicating or changing identity; food merging with the subject; 15 s is long, so keep the beats compact and expect a trimmed take; the originals were upscaled low-resolution, so expect more softness in the references than in the model's output.
**Status:** untested hypothesis (analysis 2026-10-08)

---

### `high-flip` - High flip
**Look:** The camera cranes up over the hero, rolls upside down through a top-down view and lands in a completely different scene with a different person.
**Route:** `i2v-first-and-last`. `@Image 1` is the first frame (the user's photo, scene A); `@Image 2` is the last frame, scene B, which the orchestrator generates with Seedream from a text description (character, wardrobe, location) at the same aspect ratio as the photo. If the user supplied a destination image, use it instead after checking the ratio.
**Parameters:** duration 9 s; the ratio locks to the FIRST image, and both images must share it, so generate or crop the last image to the first image's ratio (originals 16:9 and 9:16); `generate_audio` false by default; draft at 480p.
**Start photo:** A full-body or seated person at eye level or slight low angle with open headroom above, in a distinctive location with a clear ground plane. Bad inputs: ceiling directly above the subject, extreme close-up, a top-down photo, a busy crowd, a tilted horizon.
**Beats (from the originals):**
- 0-0.6 s: opens out of focus, then snaps sharp.
- 0.6-3 s: subject A in location A, the camera starts at eye level and cranes straight up, tilting down to keep A framed; A looks up.
- 3-5 s: top-down bird's-eye view, the camera rolls through about 180 degrees, A appears upside down, then the ground fills the frame.
- 5.1-5.4 s: hard cut, hidden by the flip or a dark frame.
- 5.4-9 s: subject B in location B, slow pullback.
One hard cut, at 5 s.
**Prompt template:**
```text
@Image 1 is the first frame. It defines scene A: {subject_a} in {location_a}.
@Image 2 is the last frame. It defines scene B: {subject_b} in {location_b}, held after a slow pullback.
0-0.6s: the picture opens out of focus and snaps sharp. 0.6-3s: the camera starts at eye level on {subject_a} and cranes straight up, tilting down to keep them framed while they look up at the lens. 3-5s: the camera reaches a top-down bird's-eye view over {subject_a} and rolls through a half turn of 180 degrees, {subject_a} appearing upside down, then {ground_a} filling the frame until the picture goes dark.
At 5s, hard cut to scene B with nothing from scene A in frame: {subject_b} in {location_b}, {scene_b_action}. 5-9s: slow pullback, ending as a held shot matching the last frame.
Scene A contains only {subject_a} and scene B contains only {subject_b} and {crowd_b}.
```
**Slots:**
- `{subject_a}`, `{location_a}`, `{ground_a}`: read from the photo ("the blue salt flat", "the throne's back").
- `{subject_b}`, `{location_b}`, `{crowd_b}`, `{scene_b_action}`: from the Seedream description of scene B; default pairs that contrast scene A in setting and palette, e.g. "a dealer in a grey tee and chains" / "a green-felt casino table lit from above" / "no one else" / "dealing cards".
**Post:** Optional: a short dark dip or whoosh at the cut via FFmpeg and Seed Audio to hide the seam; otherwise none.
**QA:**
- Camera rises, reaches a top-down view and visibly rolls about 180 degrees before the cut.
- Hard cut near 5 s lands on scene B; scene A never appears after it and scene B never appears before it.
- Last frames match `@Image 2` in subject, wardrobe and location.
- Subject A has exactly one person; scene B person and crowd counts match the description.
**Risks:** Scene B leaking into scene A early; subject A staying visible after the flip; up-axis confusion during the roll; crowd density artefacts in B; the "seamless" blend becoming a visible morph; first-and-last conditioning not guaranteeing frame-accurate arrival at `@Image 2`; the analysis did not observe the roll in the model description, only in frames (confidence medium).
**Status:** untested hypothesis (analysis 2026-10-08)

---

### `floating-fall` - Floating fall
**Look:** The subject falls backward in slow motion while their belongings hang weightless and the camera glides through crisp macro shots of each item before the fall completes.
**Route:** `i2v-first-frame`. `@Image 1` is the first frame (the user's photo); the held items are read from it.
**Parameters:** duration 12 s; ratio follows the photo (originals 16:9 and 4:3); `generate_audio` false by default (a soft slow-motion swell is optional and belongs in a Seed Audio bed); draft at 480p.
**Start photo:** A person walking or standing in the open with two to four clear carried or worn items (drink bottle, popcorn tub, sunglasses, bag), on a street or rooftop with ground space behind them for the fall and room for a bystander. Bad inputs: hands empty, items occluded, tight crop above the waist, indoor clutter, a crowded pavement.
**Beats (from the originals):**
- 0-1 s: low-angle forward track on the legs and feet of a walking person (adapted: the user's photo replaces this opening, so the clip starts low and tracking back).
- 1-3 s: camera tilts up and tracks back; subject smiles, wink, holds the items; a bystander walks past behind.
- 3-5 s: she arches backward, arms out; slow motion begins; items leave her hands and hang in the air (cap pops, droplets and popcorn drift).
- 5-9 s: camera dives into crisp macro shots with rack focus on each item in turn, then pulls out to a wide of the mid-fall.
- 9-11 s: lands flat on her back; items land around her; normal speed returns.
- 11-12 s: static wide, she lies still, the bystander walks away.
**Prompt template:**
```text
@Image 1 is the first frame.
{subject} walks toward the camera on {ground}, holding {items_with_hands}. Exactly one bystander in {bystander_look} walks past in the background.
At 3s {subject} arches backward and throws both arms out, and from here everything moves in slow motion: the {item_list} leave their hands and hang weightless in the air at different heights, droplets and small particles drifting.
The visuals feature golden-hour backlight, shallow depth of field and low-sun shadows.
Low ground-level camera. 0-3s: track backward ahead of {subject}, tilting up from the legs to frame them head to toe. 3-5s: hold as the items float. 5-9s: the camera glides through the floating items in this order, pausing in a crisp macro close-up with rack focus on each: {macro_order}, then pulls out to a wide of {subject} mid-fall. 9-11s: {subject} lands flat on their back with the items settling on the ground around them in {landing_description}; speed returns to normal. 11-12s: static wide, {subject} lies still while the bystander walks away.
Exactly {item_count} items float and land; every item keeps the shape and colour it has in the first frame.
```
**Slots:**
- `{subject}`, `{ground}`, `{items_with_hands}`, `{item_list}`: read from the photo; name each item by colour, shape and which hand holds it (hand named by anatomy and frame side, e.g. "the lemonade bottle in the right hand on the frame-left").
- `{bystander_look}`: default "a grey shirt"; the recipe fixes the bystander at exactly one.
- `{macro_order}`: item-by-item macro detail from the photo (e.g. "the reflection in the sunglasses' lenses, bubbles around the bottle neck, the popcorn tub's striped side").
- `{landing_description}`: scatter pattern, default "a loose arc".
- `{item_count}`: count of items in `{item_list}`.
**Post:** none. Optional slow-motion swell via Seed Audio. Brand text that must be legible in macro belongs in a reference or an overlay, not the generated shot.
**QA:**
- Slow motion begins near 3 s and ends near 9-11 s; items float only after the arch.
- Item count and identity unchanged between float and landing.
- Macro shots show crisp items; any text is as photographed, not invented.
- Subject lands flat on the back; exactly one bystander before and after.
**Risks:** Item identity and count drift; invented or garbled label text in macro (avoid asking for legible text); subject limbs distorting in the fall; bystander appearing or vanishing; items falling too early; the original opening on the legs cannot be reproduced from a normal first-frame photo.
**Status:** untested hypothesis (analysis 2026-10-08)

---

### `moonwalk` - Moonwalk
**Look:** A person walks endlessly in profile on a handmade paper-theatre set while Moon, Sun and Earth props slide in and the ball under their feet changes planet.
**Route:** `i2v-first-and-last`. The orchestrator builds both frames with `seedream_generate_image`, binding the user's person photo as `@Image 1` for identity and adding the set description as text (the live edit tool needs a point or bbox and cannot re-costume a whole image): `@Image 1` is the first frame (the person walking in profile on a grey cratered moon-ball, pale blue sheer curtain, hung silver stars, one gold ringed star); `@Image 2` is the last frame (the same person in the same stance on a blue-green Earth globe, gold glitter arch with warm string lights, layered cloud with gold lightning cut-outs). Both frames keep identical framing, stance, outfit and 4:3 aspect so the sequence resolves cleanly.
**Parameters:** duration 15 s; ratio 4:3 - the ratio locks to the FIRST image, and both images must share it; `generate_audio` false by default (a soft music-box bed would suit it but is added in post to avoid baked music); draft at 480p.
**Start photo:** Full-body person in a clean side-on or three-quarter stance, mid-stride, clear outfit silhouette and shoes. Bad inputs: cropped legs, bulky coat hiding the gait, front-facing static pose, other people, a hat or crown that the user does not want kept (the originals show no crown).
**Beats (from the originals):**
- 0-4 s: locked full-length side-on stage shot, subject walks in place facing frame-left on the grey moon-ball before a pale blue sheer curtain.
- 4-6.5 s: she looks up as props slide down: the gold star exits and a jewelled gold crescent moon with hanging planets descends; the ball turns yellow (Sun).
- 6.5-10.5 s: continues walking on the yellow sun-ball under the crescent and four hung planets.
- 10.5-12.5 s: props slide up and out; a layered cloud with gold lightning cut-outs descends; the ball becomes a blue-green Earth globe under a gold glitter arch.
- 12.5-15 s: keeps walking on Earth, ends looking up at the cloud.
No hard cuts; the swaps are sliding transitions.
**Prompt template:**
```text
@Image 1 is the first frame. It defines the opening set: {subject} in {outfit_lock} walking in profile facing frame-left on a grey cratered moon-ball, in front of a pale blue sheer curtain with hung silver stars and one gold ringed star, in handmade paper-craft theatre style.
@Image 2 is the last frame. It defines the ending set: the same {subject} walking on a blue-green Earth globe under a layered paper cloud with gold lightning cut-outs, a gold glitter arch and warm string lights.
Fixed locked-off medium-long stage shot with no camera movement. {subject} walks in place in profile at a steady pace, centred, for the whole clip, never drifting sideways. 0-4s: moon set. At 4s {subject} looks up as the gold star slides up out of frame, a jewelled gold crescent moon with exactly four hanging planets slides down from above, and the ball beneath their feet turns warm yellow. 6.5-10.5s: sun set, walking on. At 10.5s the crescent and planets slide up and out as the lightning cloud slides down, the ball turning blue-green into Earth, the gold arch and string lights glowing in. 12.5-15s: {subject} keeps walking on the Earth globe and ends looking up at the cloud.
Props slide vertically and never pop; {subject} keeps the outfit, shoes and stance of the first frame.
```
**Slots:**
- `{subject}`, `{outfit_lock}`: read from the photo (garments and colours); add "wearing a small gold crown" only if the user asks for one.
- The two Seedream frames carry the set detail; keep the set description in the prompt text identical to what the frames show.
**Post:** none. Optional music-box or ambient bed via Seed Audio.
**QA:**
- Camera never moves; subject stays centred and walking in place in profile.
- Props enter from above and exit upward; no pop-in or hard cut.
- Ball sequence is moon, sun, Earth; planet count under the crescent is four.
- Outfit and face constant; no foot sliding that looks like skating.
- End frame matches `@Image 2` composition.
**Risks:** Subject drifting left or right instead of staying centred; props popping instead of sliding; gait foot-slide; ball swaps showing a visible cut; outfit change across 15 s; the original description says crowned but the frames show no crown (confidence medium); a single image-to-video is hard to hold for 15 s, so consider two chained 7 s takes with the mid-state as a middle keyframe if drift appears.
**Status:** untested hypothesis (analysis 2026-10-08)

---

### `studio-slide` - Studio slide
**Look:** Three copies of the same fashion model at different scales and depths slide past one another in one lateral camera move against a flat solid-colour backdrop.
**Route:** `i2v-first-frame`. `@Image 1` is the first frame (the user's single-person photo); the copies are created by the prompt. The recipe fixes the copy count at three for reliability; the originals show more copies at the edges.
**Parameters:** duration 8 s; ratio follows the photo (originals 16:9 and 4:3); `generate_audio` false by default; draft at 480p.
**Start photo:** Clean full-body fashion photo of a single person against a plain, evenly lit solid-colour seamless backdrop, face visible, accessories (bag, cap, necklace) clear. Bad inputs: textured or gradient background, props or furniture, cropped limbs, a second person, a heavily patterned outfit that will drift between copies.
**Beats (from the originals):**
- 0-0.5 s: extreme close-up of half the face with a hand lifting the cap; a tiny full-body copy far away.
- 0.5-2.5 s: camera dollies back and left; a foreground shoulder copy slides in from the left; the tiny copy snaps into focus.
- 2.5-4.5 s: camera dollies forward while moving left; a life-sized copy crosses the midground touching her necklace and turns to camera.
- 4.5-6.5 s: central copy exits right; a three-quarter profile copy looks over her shoulder and becomes the focal point.
- 6.5-8 s: camera pushes forward between foreground shoulders, ends tight on the back of one copy's neck, braids and chain.
No hard cuts; out-of-focus foreground shoulders act as natural wipes.
**Prompt template:**
```text
@Image 1 is the first frame. It defines {subject}'s face, hair, outfit and accessories and the flat {backdrop_colour} seamless backdrop.
At 0s one {subject} stands as in the first frame. By 2s there are exactly three identical copies of {subject} in the frame, and exactly three stay visible through to the end: a giant foreground copy cropped to a shoulder and half a face on the {foreground_side} of the frame, soft in focus; a life-sized copy in the midground, sharp, {midground_action}; a tiny full-body copy far in the background, small and sharp.
The copies slide past each other in parallax, swapping depth layers, each in a different pose and facing a different direction, all wearing the identical outfit and {accessory_line}.
The visuals feature even soft studio light, shallow depth of field with rack focus between the depth layers, and a flat {backdrop_colour} background without gradients or props.
One continuous lateral dolly: 0-3s dolly back and to the left; 3-6s dolly forward while still moving left; 6-8s push forward between the foreground shoulders, ending close on the back of one copy's neck and {back_detail}.
```
**Slots:**
- `{subject}`, `{backdrop_colour}`, `{accessory_line}`, `{back_detail}`: read from the photo (e.g. "braids and a gold chain"). When the photo shows no accessory, delete "and {accessory_line}"; when the neck shows no detail, delete "and {back_detail}".
- `{foreground_side}`: default "frame-left".
- `{midground_action}`: default "walking across the frame, the right hand on the frame-left side of the picture touching the necklace, then turning to the camera".
**Post:** none.
**QA:**
- Exactly three copies visible from 2 s to the end, never merging or exceeding three.
- Same face, outfit and accessories on all copies; different poses.
- Backdrop stays one flat colour, no gradient, props or text.
- Foreground crop never fully hides the focal copy's face for more than a moment.
- Ends close on the back of a neck.
**Risks:** Copy count errors (the most likely failure); identity or outfit drift between copies; copies merging at overlaps; identical poses on clones; foreground crop covering the face; backdrop gaining gradients; no second reference image can be added to a first-frame route, so identity comes from the photo alone.
**Status:** untested hypothesis (analysis 2026-10-08)
