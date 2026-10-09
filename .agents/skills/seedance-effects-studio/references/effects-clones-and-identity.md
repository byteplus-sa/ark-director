# Effect recipes - Clones and identity

Nine effects that multiply, scale, freeze, remove or dive into one person from a single photo. They share one skeleton: an image-role line (`@Image 1 is the first frame.` for first-frame routes, `@Image 1 defines ...` for reference routes), the subject read from the photo through `{subject}`, a timestamped timeline with an exact figure or object count at every stage, one concrete camera move with start and end, and an observable end state. Every duplicated-person effect states that all copies share one face, one hairstyle and one identical outfit, and counts them at each timestamp. Prompts contain no on-screen text, no brand names and no negative-only lists; native audio is off unless the recipe says otherwise.

Route note: Seedance 2.5 cannot mix a `first_frame` image with `reference_image` inputs. Three recipes (`infinite-clones`, `lacewalker`, `superstar`) open on a frame that is not the photo, so they use reference images only. The brief's route list has no token for that; they are labelled `reference-images` below.

## Menu rows

| id | label | route | duration | start photo |
|---|---|---|---|---|
| `clones` | Clones | `i2v-first-frame` | 7 s | Full-body, standing, wide open location |
| `infinite-clones` | Infinite clones | `reference-images` | 7 s | Full-body, distinctive outfit and headwear |
| `selfception` | Selfception | `i2v-first-frame` | 5 s | Standing, open palm holding a tiny copy |
| `act-natural` | Act natural | `i2v-first-frame` | 6 s | Person caught mid-action, busy location |
| `stop-world` | Stop world | `i2v-first-frame` | 8 s | Standing figure inside a crowded space |
| `eyes-in` | Eyes in | `i2v-first-frame` (+ optional second clip) | 7 s | Portrait, open eye toward camera, well lit |
| `lacewalker` | Lacewalker | `reference-images` | 8 s | Full-body outfit, readable face with glasses or hat |
| `superstar` | Superstar | `reference-images` | 15 s | Clear face, distinctive outfit, waist-up |
| `vanish` | Vanish | `i2v-first-frame` | 5 s | Loose shape-holding clothes, kneeling or leaning |

### `clones` - Clones

**Look:** One person stands in a real location while identical copies pop into existence through the scene, until one copy steps to the lens and covers it with a palm.
**Route:** `i2v-first-frame`. `@Image 1` = first frame (the user's photo). No other images.
**Parameters:** duration 7 s; ratio follows the photo; `generate_audio` false (a native-audio sting is not needed; a soft street ambience bed can be added in post); draft 480p, final 720p or 1080p.
**Start photo:** Full-body, standing, outfit fully visible, face clear, in a wide open location (street, plaza, track) with empty room on both sides and in the distance for small copies. Bad inputs: cropped legs, seated or turned-away pose, tight indoor space, crowds already filling the background (copies get lost), face too small to read when one copy fills the lens.
**Beats (from the originals):**
- 0-1.5 s: the original stands full-body in a static wide frame with small natural movement; real traffic or pedestrians behind.
- 1.5-4 s: identical copies pop in one after another at different depths and positions, each in its own small idle pose (arms crossed, hand in hair, hand on hip); about 4-6 small copies by 4 s. No visible dissolve.
- 4-5.5 s: a foreground copy rises into the bottom of the frame right in front of the lens and fills the lower frame facing camera.
- 5.5-7 s: the near copy raises an open palm to the lens; the palm blurs, fills the frame and the picture goes black (a chaining handle).
**Prompt template:**
```text
@Image 1 is the first frame. {subject} stands full-body at {position} in {location}, wearing {outfit}, exactly as in the photo.
Locked-off static wide camera at eye level, 35mm look, deep focus, no camera movement for the whole clip. Every sign, vehicle and garment shows plain colour with no lettering.
0-1.5s: the original is the only copy in frame (1 figure); {original_idle}. {background_life} continues behind.
Copies pop in one by one. Each is fully solid from its first frame, with light and shadow matching the scene: no fade, dissolve, glow or particles. At 1.5s copy 1 appears at {spot_1}; at 2s copy 2 at {spot_2}; at 2.5s copy 3 at {spot_3}; at 3s copy 4 at {spot_4}; at 3.5s copy 5 at {spot_5}. From 3.5s there are exactly 5 copies plus the original, 6 figures. Every copy is the same person: one face, identical hair, identical outfit ({outfit}), smaller with distance. Each copy holds its own idle pose ({idle_poses}) and moves independently, never mirroring another.
At 4s a sixth copy rises into the bottom of the frame right in front of the lens and fills the lower third facing the camera, face large and sharp; the original stays in place and the five background copies keep making small adjustments.
At 5.5s the near copy raises their open right palm (the hand on the frame-left side) toward the lens; the palm fills the frame by 6.5s and the picture stays black to the end.
```
**Slots:**
- `{subject}`: read from the photo (for example "the woman in the yellow skirt").
- `{position}`: where the person stands in the photo (frame-centre, frame-right third).
- `{location}`: from the photo background.
- `{outfit}`: one sentence listing garments and colours as seen.
- `{original_idle}`: default "they turn their head slightly and shift weight onto one foot".
- `{background_life}`: default "distant traffic and a few pedestrians", only what the photo shows.
- `{spot_1}`, `{spot_2}`, `{spot_3}`, `{spot_4}`, `{spot_5}`: five distinct named places with depth, for example left sidewalk mid-distance, far crosswalk, far right kerb, near left kerb, middle distance right.
- `{idle_poses}`: default "arms crossed, left hand (frame-right side) in hair, right hand (frame-left side) on hip, hands behind back, left hand (frame-right side) shading the eyes"; name the side of every one-handed pose by anatomy plus frame side.
**Post:** none. Optional chaining: the black end frame is a clean handle for the next clip; join with FFmpeg concat. Optional street ambience bed from Seed Audio.
**QA:**
- Exactly 1 figure until 1.5 s, then 6 figures from 3.5 s, then 7 with the near copy; count by pausing at 1 s, 3.5 s and 5 s.
- All copies share one face, hair and outfit with no colour change, including the smallest distant ones.
- Pop-ins read as instant appearances, with no cross-dissolve or morph.
- The original stays where it was; the near copy does not replace her.
- Picture ends black behind the palm; no text anywhere.
**Risks:** Count drift (5 becomes 8-12). Identity and outfit drift in tiny distant copies. Dissolve or morph instead of a hard pop-in. Shadows pointing the wrong way. The near copy replacing the original. Copies mirroring each other when independence was asked. Probe result: the model drew about 8 copies instead of 5 even with the count stated; treat the count as approximate, or ask for 4 when at most 5 is acceptable. Probe result: copies stood between cars rather than on roofs and counts ran about two above the request.
**Status:** probed 2026-10-08, one 480p draft in project `effects-probe` (scene-08): copies popped in one by one on distant car roofs, a near copy rose into the lens, raised a palm that covered it, and the picture went black. Count overshot: about 8 copies at 3.6 s against the 5 requested. A frame-by-frame scan counted about nine figures at about 4 s against seven requested, copies standing between the cars rather than on roofs, and pop-ins starting at about 1.4 s, earlier than the 1.5 s asked. The template was amended after review (a positive text-free clause; one-handed idle poses name their side); the amendment is not re-probed. Showcase run 2026-10-08 (scene-10, first-frame, sound on): usable with defects; the figure count runs about one above the request (7 to 8 for 7).

### `infinite-clones` - Infinite clones

**Look:** A single car brakes to a stop and an unending stream of identical people clown-car out of every door and sprint off in all directions, filmed from a locked high angle.
**Route:** `reference-images`. `@Image 1` = reference image (identity, hair, headwear, outfit). Optional `@Image 2` = reference image of the car. No first-frame image, because the clip opens on an empty lot. With two images both use role `reference_image`, in order: person first, car second. Provider rule (run 2026-10-08): the `reference_image` role was rejected before any cost (`InputImageSensitiveContentDetected.PrivacyInformation`) for a face close-up and a clean full-body crop of a person; a generated still of the woman inside a scene was accepted as a `reference_image` in the earlier probe, so treat person-crop references as likely to fail and have the first-frame fallback ready. Verified fallback (scene-11): `i2v-first-frame` with a Seedream still of the person standing alone beside the parked car with all four doors closed (built from the person's references); replace the two role lines with `@Image 1 is the first frame: <what the frame shows>`, delete the `@Image 2` sentence, hold 'the car stays parked with its doors closed and the person holds still' for 0-2.5 s, and count the person among the figures (1 figure to 3 s, then the ramp to 20 including the person).
**Parameters:** duration 7 s; ratio 16:9 by default (wide lot), 9:16 also fine; `generate_audio` false (an SFX-only sting, tire screech then doors, could help but risks baked music; add SFX in post by default); draft 480p.
**Start photo:** Full-body, distinctive outfit and headwear (a beanie, cap or bold hair accessory) so tiny top-down copies still read as one person. Bad inputs: plain outfit with no headwear, face-only crop, heavy accessories that vary by angle, a photo with several people.
**Beats (from the originals):**
- 0-1 s: an empty rooftop lot or crosswalk at golden hour; a sports car drifts sideways into frame from the bottom edge with tire smoke and brakes to a stop in a marked bay.
- 1-2.3 s: the car is stationary and the smoke dissipates.
- 2.3-2.8 s: all four doors swing open at once.
- 2.8-4 s: identical figures pour out: about 2 at 2.7 s, 4 at 3.2 s, 8 at 3.7 s, running away immediately.
- 4-7 s: the stream continues while copies scatter toward, away from and across the camera; 20+ by the last frame; car and background stay static.
**Prompt template:**
```text
@Image 1 defines the person's face, hair, {headwear} and outfit ({outfit}); every figure in the clip is this one person. Use @Image 1 only for the person's identity; ignore its pose, background and light.
@Image 2 defines only the car's shape and colour.
Locked-off static high-angle wide shot, about 45 degrees down from a rooftop perch, deep focus, no zoom and no camera movement at any point. Setting: {location}, {light}.
0-1s: the lot is empty. {car_description} drifts sideways into frame from the bottom edge, leaves tire smoke, and brakes to a stop in a marked bay. The car stays parked for the rest of the clip; only the smoke drifts away slowly. The car, bay markings and clothing show plain colour with no lettering.
At 2.5s all four doors swing open at once and stay open.
From 3s figures climb out of the open doors and run away immediately; the stream never pauses. Figures in frame: 2 at 3s, 4 at 3.5s, 8 at 4s, 12 at 5s, 16 at 6s, 20 at 7s. Nobody leaves the frame. At 7s the 20 runners head in four groups: 6 toward the camera, 5 toward the far side of the lot, 4 to frame-left, 5 to frame-right.
All 20 are identical: same face, same {headwear}, same outfit, same height, each with its own running stride.
End state at 7s: 20 figures scattered across the lot, the car parked with four open doors, tire marks on the asphalt.
```
**Slots:**
- `{headwear}`: read from the photo; if none, write "hair in the same style".
- `{outfit}`: garments and colours as seen, one sentence.
- `{location}`: default "an empty rooftop parking lot with white bay markings".
- `{light}`: default "golden-hour light with long shadows".
- The line "@Image 2 defines only the car's shape and colour." is included only when a car image is supplied; delete it otherwise, and then use no second reference image.
- `{car_description}`: from `@Image 2` if supplied; otherwise default "a low blue four-door sports car with plain unmarked panels". For a real branded car, acquire an authorised image per the element-identification contract rather than naming a brand.
**Post:** none by default. Optional SFX bed (tire screech, door swings, footsteps) from Seed Audio, mixed under the clip.
**QA:**
- Figure counts at 3 s, 4 s, 5 s, 6 s, 7 s match the list within one or two figures; the stream does not stop early.
- All figures wear the same outfit and headwear; no size or colour drift.
- Car stays parked with four open doors; it does not drive off or close doors.
- Camera is static and high-angle throughout; no second cut.
- No lettering on the car, ground or clothing.
**Risks:** The stream fades out at 6-10 figures. Dense runners merge or lose limbs. Floaty drift physics. Car drives away or doors close. Outfit and size drift across copies. Car design unconstrained without a description or reference. Painted lot markings may render as glyphs. Probe result: runner count came in near 15 against 20; keep the count as a ramp, not an exact figure. Probe result: only two of four doors showed open and runners left the frame, so 'nobody leaves the frame' did not hold.
**Status:** probed 2026-10-08, one 480p draft in project `effects-probe` (scene-11, `reference_image` route): the car drifted in, stopped, all four doors opened, and a continuous stream of identical runners spread across the intersection (about 15 counted at 7 s against 20 requested). A frame-by-frame scan saw the runner count peak at 15 to 17 at about 5.5 s and then thin as runners left the frame, and only two car doors open rather than four. The template was amended after review (the conditional `@Image 2` binding line; a positive text-free clause); the amendment is not re-probed. Showcase run 2026-10-08 (scene-11, first-frame (reference route replaced), sound on): usable with defects; the runner count overshoots the ramp (about 20 to 25 against 20); the tyre screech is not confirmed; the car resembles a real sedan.

### `selfception` - Selfception

**Look:** The camera dives into the tiny self on a palm and that figure becomes the full-size subject holding another tiny self, Droste-style.
**Route:** `i2v-first-frame`. `@Image 1` = first frame. The first frame must already contain the miniature (see Start photo).
**Parameters:** duration 5 s; ratio 9:16 by default, otherwise follows the photo; `generate_audio` false; draft 480p.
**Start photo:** Standing person, upper body to full body, outfit with texture (fur trim, lace, denim) in a real street or outdoor scene with depth, one open palm held out at waist height with a figurine-sized copy of themself standing on it, in the same outfit and pose. If the user's photo shows an empty palm, the orchestrator makes the prepared first frame with `seedream_generate_image`, binding the user's photo as `@Image 1` for identity ("the same person as @Image 1, standing as in the photo, holding exactly one figurine-sized replica of themself standing on the open palm, identical face, hair and outfit"), inspects it, and uses that image. Bad inputs: no free hand, arms crossed, pocketed hands, a front-on pose that hides the palm, outfit with plain flat colour (tiers look identical to the background).
**Beats (from the originals):**
- 0-1.5 s: the subject holds a tiny replica on an open palm; the camera starts wide at hip height and pushes toward the hand while gently orbiting.
- 1.5-3 s: the camera glides past the torso onto the palm; the miniature grows to full frame as the new full-size subject; the previous giant's hand drops out at the bottom.
- 3-4.5 s: the camera arcs behind the new subject, seen from behind, who again holds a tiny replica on an outstretched palm; the street keeps consistent parallax.
- 4.5-5 s: the push-in finishes tight on the back of the coat and hair, a handoff point for the next tier.
**Prompt template:**
```text
@Image 1 is the first frame: {subject} stands in {location}, wearing {outfit}, holding their {hand_side} open at waist height with a figurine-sized replica of themself standing on it. The replica has the same face, hair, outfit and pose.
One continuous camera glide, no cuts, about 35mm, shallow depth of field. Every sign, screen and garment shows plain colour with no lettering.
0-1.5s: the camera starts wide at hip height and pushes toward the palm while orbiting {orbit_direction} about 20 degrees around the subject.
1.5-3s: the camera glides past the subject's torso and down onto the palm. The replica grows in frame until it is the full-size subject, in the same frame position the large subject held. The previous large subject slips out through the bottom of the frame, leaving only the sleeve and palm of that same arm at the bottom edge before it exits.
3-4.5s: the camera arcs {orbit_direction} behind the new subject, now seen from behind, who extends their {hand_side_rear} open, holding another figurine-sized replica of themself with the same hair and the same {outfit}.
4.5-5s: the push-in settles tight on the back of the coat and hair.
Exactly two complete figures are visible at any moment, one large and one figurine-sized. Every tier wears the identical {outfit} with the same hair and one shared face. The {background} keeps consistent parallax with the orbit.
```
**Slots:**
- `{subject}`: from the photo.
- `{location}`: from the photo background.
- `{outfit}`: garments, colours and textures as seen (for example "yellow-green fur-trimmed denim coat over a white top").
- `{hand_side}`: anatomy plus frame side as seen in the photo, for example "right palm (frame-left side)".
- `{hand_side_rear}`: the same palm seen from behind, so the frame side flips, for example "right palm (frame-right side)".
- `{orbit_direction}`: default "counterclockwise".
- `{background}`: default "street, buildings and crossing".
**Post:** none. Optional: join several clips whose last frame is the next first frame for deeper recursion; each extra tier is a separate generation.
**QA:**
- At 1 s: one large figure, one figurine-sized replica; at 3 s: the former replica is full-size and no second large subject remains.
- Replica is clearly smaller than the hand-holder (roughly a tenth of the height); never two figures of similar size.
- Same coat colour, trim and hair on every tier.
- Camera glides continuously; no cut and no plain push-in with no recursion.
- Ends on the back of the coat and hair.
**Risks:** Wrong miniature scale (both similar size). Hand and finger anatomy on the palm. Tier outfit drift. A cut replaces the glide. Zoom becomes a plain push-in with no handoff. Background not rotating with the orbit. Visible nesting past two tiers is unreliable, so do not ask for more.
**Status:** tested once in the 2026-10-08 showcase run (project `effects-showcase`, scene-12, first-frame, 480p draft, sound on, one invented subject at 9:16): usable with defects; the copy never grows into a full-size second woman, so the hand-over is not clearly shown. Not verified on other photos or at a higher resolution.

### `act-natural` - Act natural

**Look:** The subject and the objects tied to their action are frozen like a statue mid-action while the world carries on and the camera glides around them.
**Route:** `i2v-first-frame`. `@Image 1` = first frame.
**Parameters:** duration 6 s; ratio follows the photo; `generate_audio` false (ambient sound of the busy location from Seed Audio in post if wanted); draft 480p.
**Start photo:** Person caught mid-action (bending, drinking, reaching, dropping groceries, sipping) so the frozen pose is believable, in a busy location with room for background motion (loading dock, party, street) and visible people or a road. Bad inputs: relaxed standing portraits, empty locations (the contrast vanishes), heavy product packaging with brand lettering in the frozen group (it garbles under orbit).
**Beats (from the originals):**
- 0-6 s: the subject and the objects tied to the action (spilled groceries, cups on a table) stay frozen in the photo pose, hair and clothing included; everything else moves at normal speed (workers walk, a van drives through at about 3 s, a pallet jack enters).
- continuous: the camera slowly tracks or orbits sideways, keeping the subject centred so parallax separates frozen foreground from moving world.
**Prompt template:**
```text
@Image 1 is the first frame. {subject} is caught mid-action ({frozen_action}) in {location}.
From 0s to the end the subject and everything tied to the action ({frozen_objects}) hold the exact photo pose: the subject is rigid like a statue, eyes fixed on {gaze}, hair strands and clothing hold their positions, the chest and shoulders stay level.
The rest of the world runs at normal speed: exactly {background_count} background people ({background_motion}); at 3s {crossing_event}. The light and weather stay as in the photo. Every sign, screen and package shows plain colour with no lettering.
Camera: slow lateral orbit {orbit_direction} through about 30 degrees around the subject at eye level for the full duration, 35-50mm look, deep focus, the subject staying centred so parallax separates the frozen foreground from the moving background. No cuts.
End state at the final frame: the subject in the identical pose, the camera 30 degrees around from where it started, the background people and vehicle in new positions.
```
**Slots:**
- `{subject}`: read from the photo (apparent age, hair, one clothing item), never a name.
- `{location}`: read from the photo background.
- `{frozen_action}`: from the photo (for example "bending to pick up spilled groceries").
- `{frozen_objects}`: every object in contact with the action, named from the photo (bag, spilled items, cup).
- `{gaze}`: where the eyes point in the photo (the lens, the groceries).
- `{background_count}`: default 3, count the people visible in the photo; the crossing event must not add a person. When the count is 1 write "1 background person" in the sentence.
- `{background_motion}`: what each does ("two walk left to right, one pushes a hand truck").
- `{crossing_event}`: default "a white delivery van drives across the background from frame-right to frame-left"; in a room use an unattended object ("a wheeled food trolley, with no extra person, rolls across").
- `{orbit_direction}`: default "clockwise".
**Post:** none. Optional ambience bed.
**QA:**
- The subject, hair, clothing and frozen objects are in the same position at 1 s and at 5 s; no breathing, blinking or hair sway.
- The background moves at normal speed throughout; the clip does not turn into a static video.
- Camera orbit is smooth and keeps the subject centred; no cuts.
- Frozen items do not slide or fall; no new objects or people join the frozen group.
- Packaging shows no readable lettering.
**Risks:** Micro-motion (breathing, blinking, hair sway) creeps in. Frozen items slide. The whole frame freezes. Objects pull out of frame as the camera moves. Packaging text garbles. The subject drifts when the orbit is not explicit.
**Status:** probed 2026-10-08, one 480p draft in project `effects-probe` (scene-04): the subject held the mug pose for the whole clip while the waiter and patrons moved; the 30-degree orbit was subtle but visible as parallax. The template was amended after review (a positive text-free clause; singular noun for a count of 1); the amendment is not re-probed. Showcase run 2026-10-08 (scene-13, first-frame, sound on): usable with defects; the neon sign lettering is garbled; the orbit is modest; a faint murmur in the sound.

### `stop-world` - Stop world

**Look:** One calm person moves at normal pace through a crowd sped up into blur, as if a finger-snap fast-forwarded the world around them.
**Route:** `i2v-first-frame`. `@Image 1` = first frame.
**Parameters:** duration 8 s; ratio follows the photo; `generate_audio` false by default; a short native sting (finger snap, rising whoosh) would help the beat but risks baked music, so add it in post; draft 480p.
**Start photo:** Front-facing standing person, full body or 3/4, at the far end of a space that holds many people (subway car, crossing, plaza, field), eyes toward the camera. Bad inputs: an empty location, a person at the camera edge with no depth to walk, a crowd packed so tight it cannot move, a subject partly hidden behind others.
**Beats (from the originals):**
- 0-2 s: the subject at the far end of a crowded space, calm, eyes to camera; everyone else moves at fast time-lapse speed with motion blur.
- 2-6 s: she moves slowly toward the camera, a finger-snap or beckoning gesture at about 3 s; the crowd rushes around her in streaks.
- 6-8 s: she ends closer in a medium shot looking at camera with a small smile; the crowd shows a different arrangement from the start. It does not rewind.
**Prompt template:**
```text
@Image 1 is the first frame. {subject} stands calm at {start_spot} in {location}, eyes on the camera.
Locked-off camera at eye level, 35mm look, deep focus, no cuts. Every sign, screen and garment shows plain colour with no lettering.
Time contrast: the subject moves at normal speed and stays sharp and clear. All {crowd_count} other people move at fast time-lapse speed, about eight times normal, streaking past in different directions with motion blur; nobody stops, duplicates or merges.
0-2s: the subject stands still and calm while the crowd streams past in blur.
At 3s the subject snaps the fingers of their {snap_hand} once at chest height, then walks slowly toward the camera at an unhurried pace, upright, arms relaxed, the crowd still rushing around them.
6-8s: the subject arrives in a medium shot, looks into the lens and gives a small smile; the crowd keeps rushing and its arrangement is different from the opening.
End state: one calm sharp figure in medium shot in the foreground, {crowd_count} blurred people moving behind.
```
**Slots:**
- `{subject}`: from the photo.
- `{start_spot}`: for example "the far end of the subway car".
- `{location}`: from the photo.
- `{crowd_count}`: default 8; count the people visible in the photo and keep the number small. When the count is 1 write "the 1 other person" and "1 blurred person" in the sentences.
- `{snap_hand}`: anatomy plus frame side, for example "right hand (frame-left side)".
**Post:** optional finger-snap and whoosh sting plus ambience from Seed Audio, placed at 3 s.
**QA:**
- The subject is visibly sharper and slower than every other person throughout.
- Crowd count stays at the stated number, with no duplicated or merging figures.
- One finger snap near 3 s; reads as a snap, not a wave.
- Subject ends in medium shot near the lens; crowd arrangement differs from the opening and does not rewind.
- No cuts; camera stays locked.
**Risks:** Everything renders at the same speed (no contrast). Crowd speed-up looks like jitter. The subject gets motion-blurred too. The gesture reads as a wave. Crowd members merge or duplicate. Do not prompt a rewind: the originals do not show one.
**Status:** probed 2026-10-08, one 480p draft in project `effects-probe` (scene-09): the crowd streaked in time-lapse blur while the subject stayed sharp, snapped her fingers, walked to a medium shot and smiled. The template was amended after review (a positive text-free clause; singular noun for a count of 1); the amendment is not re-probed. Showcase run 2026-10-08 (scene-14, first-frame, sound on): usable with defects; the crowd is lighter than packed and some people are only partly blurred.

### `eyes-in` - Eyes in

**Look:** One continuous accelerating dive from a street portrait into one eye, through the iris, until the pupil swallows the frame in black.
**Route:** `i2v-first-frame`. `@Image 1` = first frame (the user's portrait). The originals end on pure black, so this clip is complete as it stands. Optional destination: a second, separate clip whose first frame is a destination image (first_frame cannot mix with reference images, and chaining two clips is the supported way); described under Post.
**Parameters:** duration 7 s (destination clip, if used: 5 s); ratio follows the photo; `generate_audio` false by default; a low rising whoosh and heartbeat would fit the dive but risk baked music, so add it in post; draft 480p.
**Start photo:** Portrait with a clearly open eye looking toward the camera, well lit so iris colour and texture can be read; waist-up or 3/4 is fine because the move starts wide. Bad inputs: closed or squinting eyes, sunglasses, strong profile, tiny face in a wide shot, heavy glare on the eye, a background of dense signage (it warps in the first second).
**Beats (from the originals):**
- 0-1 s: the subject stands in a street scene, medium shot, looking at the lens.
- 1-3 s: the camera pushes in fast to the face with a slight tilt, then to an extreme close-up of one eye (lashes, pores, wet cornea reflection).
- 3-5 s: macro of the iris fills the frame; the pupil grows.
- 5-6.5 s: the camera enters the pupil and the pupil expands to fill the frame.
- 6.5-7 s: pure black. The new scene is not in the clip.
**Prompt template:**
```text
@Image 1 is the first frame: {subject} stands in {location}, looking into the lens, with open {eye_color} eyes.
One unbroken accelerating push-in. No cuts and no blink: the eyelid stays open from start to end. Every sign and garment in the opening frame shows plain colour with no lettering.
0-1s: {opening_framing}, the subject holds still, eyes on the lens.
1-3s: the camera pushes in fast toward the face, rolling about 10 degrees, to an extreme close-up of their {eye_side} eye (the one nearer the lens); lashes, skin pores and the wet cornea reflection are visible.
3-5s: macro of the iris fills the frame, {iris_description} radial fibres, exactly one round pupil at the centre, growing slowly.
5-6.5s: the camera enters the pupil; the pupil expands until it covers the entire frame.
From 6.5s to the end the frame is uniform pure black, with no scene and no light.
```
**Slots:**
- `{subject}`, `{location}`: from the photo.
- `{eye_color}`, `{iris_description}`: read from the photo (for example "amber and green"); never invent a colour.
- `{opening_framing}`: the framing the photo already has ("medium shot" for a waist-up portrait, "extreme close portrait as in the first frame" for a face-filling one); the 0-1 s beat must not contradict the first frame.
- `{eye_side}`: the eye nearer the lens, stated as frame side ("left eye of the image").
- Optional destination (second clip): `{destination_description}` (obtain with a Seedream text-to-image prompt written by the orchestrator, or an acquired public-domain image, or ask the user; match the portrait's aspect ratio), `{ambient_motion}` (default "gentle drifting light and one slow movement typical of the place"), `{reveal}` (the new space).
**Post:** none for the base clip. Optional destination clip, generated separately as `i2v-first-frame` with `@Image 1` = the destination image:
```text
@Image 1 is the first frame and shows {destination_description}. The scene settles into life: {ambient_motion}. Slow dolly out from the opening composition, pulling back to reveal {reveal}. No cuts. End state: the full view of {reveal}, still and composed.
```
Join with FFmpeg: normalise both clips to the same size, frame rate and timebase, then `xfade=transition=circleopen:duration=0.6:offset=<clipA_duration - 0.6>` so the destination opens as a circle out of the black pupil. Duration 5 s for the destination clip.
**QA:**
- One continuous move, no cut before the final black.
- Exactly one eye and one pupil, centred; iris colour matches the photo; the eyelid never closes.
- The dive reaches pure black by about 6.5 s and holds to the end; it does not stop at the iris.
- No scene change inside the eye; no signage-style text in the first seconds.
- With the optional join: the circle opens from the black frame onto the destination.
**Risks:** Eye shape or colour drift in the macro. Double or off-centre pupil. A blink. The model cutting to a different scene halfway instead of staying in the eye. The dive stopping at the iris. Street reflection in the cornea not matching the photo. Text on clothing or signs in the opening frame warps during the push.
**Status:** probed 2026-10-08, one 480p draft in project `effects-probe` (scene-10): the dive through the eye, the iris macro, the pupil filling the frame and the black ending all landed in one unbroken move without a blink. The probe photo was a face-filling close-up. The template was amended after review (a positive text-free clause); the amendment is not re-probed. Showcase run 2026-10-08 (scene-15, first-frame, sound on): usable with defects; the iris turns amber-orange instead of her dark brown.

### `lacewalker` - Lacewalker

**Look:** A figurine-sized copy of the person strolls the ground in front of their giant sideways head, then, after a hard cut, balances on a thin strap stretched between two giant bags.
**Route:** `reference-images`. `@Image 1` = reference image (identity, outfit, glasses or hat). Optional `@Image 2` = reference image of the product that becomes the giant object. No first-frame image, because neither shot opens on the photo. Provider rule (run 2026-10-08): the `reference_image` role was rejected before any cost (`InputImageSensitiveContentDetected.PrivacyInformation`) for a face close-up and a clean full-body crop of a person; a generated still of the woman inside a scene was accepted as a `reference_image` in the earlier probe, so treat person-crop references as likely to fail and have the first-frame fallback ready. Verified fallback (scene-16): `i2v-first-frame` with a Seedream still of the giant sideways head and exactly one figurine-sized copy on the sand; replace the first paragraph with `@Image 1 is the first frame. It shows <the giant head and the one miniature>`, keep the in-clip hard cut behind the bag, and shot 2 needs no image.
**Parameters:** duration 8 s; ratio 3:4 (as seen) or follows the photo; `generate_audio` false; draft 480p.
**Start photo:** Full-body shot with a distinct outfit, plus a clear face with glasses or a hat for the giant head. Product reference (optional): one clean image of a handbag, sneaker or similar item. Bad inputs: plain outfit, face partly hidden, a product with visible lettering or logo (it garbles at giant scale; use a plain unmarked version or describe it), several products in one image.
**Beats (from the originals):**
- 0-3.5 s: the giant version of the subject lies sideways on the ground (eyes open, smiling) while a figurine-scale copy in the same outfit strolls left across the ground in front of the giant face.
- 3.5-4.8 s: the camera tracks with the walker; a huge handbag sweeps in from the side and fills the frame, covering the transition. HARD CUT at about 4.8 s, hidden behind the bag.
- 5-8 s: the miniature balances on a thin strap stretched between two giant bags, arms out, wobbles, one arm up for balance, keeps walking.
**Prompt template:**
```text
@Image 1 defines the person's face, hair, {accessories} and outfit ({outfit}) for both the giant head and the miniature figure; they are the same person. Use @Image 1 only for the person; ignore its {photo_leak_items} and framing. The miniature also wears {lower_outfit}. @Image 2 defines the {bag_description}.
Ground-level camera, about 35mm look, shallow depth of field.
Shot 1, 0-4.8s: the giant person's head lies on its side on the ground, eyes open and smiling toward the camera, filling the upper left of the frame (head and shoulder edge only). In front of its face walks exactly one figurine-sized copy of the same person, roughly one fifteenth the height of the giant head, in the same outfit, strolling toward frame-left with a relaxed stride. The camera trucks left at walking pace, keeping the miniature sharp.
From 3.5s to 4.8s a giant {bag_name} sweeps in from frame-right and fills the entire frame with plain smooth {bag_material}.
At 4.8s, while the bag fills the frame, cut to Shot 2, 4.8-8s: a fixed low shot at the same ground level in a new setup. Exactly two giant {bag_name}s stand left and right, many times taller than the miniature, joined by exactly one taut {strap} stretched between them at the height of their handles. The same miniature stands on the strap, arms out, wobbles, raises their {balance_arm} for balance and keeps walking along it. The giant head is not in Shot 2. The bags, hardware and ground show plain surfaces with no lettering or logos.
End state: one miniature on one strap between two giant bags.
```
**Slots:**
- `{accessories}`: glasses, hat or earrings as seen; if none are visible, delete "{accessories} and" so the clause reads "hair and outfit".
- `{outfit}`: garments and colours as seen.
- `{lower_outfit}`: a conditional sentence. Write "The miniature also wears <garments below the frame edge>." (trousers, shoes) only when the photo is cropped; when the photo is full-body, delete the whole sentence.
- `{photo_leak_items}`: objects and surfaces in the photo that must not carry over (a handbag, sand, a desk). If nothing leaks, delete the "{photo_leak_items} and" clause so the sentence ends "ignore its framing".
- `{balance_arm}`: anatomy plus frame side of the miniature's raised arm, for example "right arm (frame-left side)".
- `{bag_description}`: when `@Image 2` is given, "giant bag's shape, colour and hardware"; when absent, delete the `@Image 2` sentence and write the bag in text (default "a glossy dark-brown leather satchel with brass hardware, plain unmarked leather").
- `{bag_name}`: "bag" by default; "sneaker" for a shoe product.
- `{bag_material}`: from the product.
- `{strap}`: default "thin leather strap".
- Product acquisition: take the user's product photo; for a real brand use an official or authorised download; otherwise describe a generic unbranded item.
**Post:** none. Optional soft room tone and footsteps bed from Seed Audio.
**QA:**
- Shot 1 shows one giant head and exactly one miniature; the miniature is hand-sized relative to the head.
- The bag sweep fully covers the frame before the cut at about 4.8 s; exactly one cut.
- Shot 2: exactly one miniature, exactly two bags, exactly one strap; strap is taut and the miniature stands on it.
- Giant head and miniature read as the same person; the miniature keeps the outfit.
- No hardware text, logos or lettering.
**Risks:** Scale ratios collapse (the miniature grows). Giant head and miniature differ in identity. Extra bags or straps. The strap sags unrealistically or the miniature floats. Hardware text or logos garble. No cut, so the second setup never appears. Unnatural walking cadence.
**Status:** probed 2026-10-08, one 480p draft in project `effects-probe` (scene-07, `reference_image` route): the giant head and the walking miniature, the bag sweep hiding the cut at 4.8 s, and the miniature balancing on one strap between two giant bags all landed. Scale held as a ratio only; the identity-only wording was used. The template was amended after review (a positive text-free clause; the raised arm is named by anatomy plus frame side; conditional sentence slots); the amendment is not re-probed. Showcase run 2026-10-08 (scene-16, first-frame (reference route rejected), sound on): usable with defects; a drum-like musical beat from about 5 s; the handbag shape differs between the two shots.

### `superstar` - Superstar

**Look:** A fan's handheld phone video of a packed stadium concert in which the person is the star on stage and on the jumbotron.
**Route:** `reference-images`. `@Image 1` = reference image (face, hair, outfit). No first-frame image, because the clip opens on a crowd POV. The stage, crowd, phones and dancers are generated. Provider rule (run 2026-10-08): the `reference_image` role was rejected before any cost (`InputImageSensitiveContentDetected.PrivacyInformation`) for a face close-up and a clean full-body crop of a person; a generated still of the woman inside a scene was accepted as a `reference_image` in the earlier probe, so treat person-crop references as likely to fail and have the first-frame fallback ready. Verified fallback (scene-17): `i2v-first-frame` with a Seedream still of the opening crowd POV (4 raised phones, the performer centre stage, 2 backup dancers, an abstract LED screen); replace the role line with `@Image 1 is the first frame. It shows <that view>` and keep every timestamp.
**Parameters:** duration 15 s; ratio 9:16 (phone video) by default; `generate_audio` false (native audio stays off so no crowd chanting, sung words or music are baked in); draft 480p, final 720p or 1080p.
**Start photo:** Clear face and a distinctive outfit; waist-up portrait is enough. A person holding or near a microphone is helpful but not required. Bad inputs: sunglasses, a face turned away, tiny face in a wide photo, heavy costume details that change per angle.
**Beats (from the originals):**
- 0-2 s: fan POV from the crowd: backs of fans and raised phones in the foreground, a long runway stage in the distance, the subject among backup dancers, a big LED screen showing her face.
- 2-5 s: handheld digital zoom toward her as she walks to the stage edge, singing into a microphone; a phone screen at the bottom also shows her.
- 5-12 s: tight handheld medium shot of her singing, raising one arm to cue the crowd, then turning away to face the stage.
- 12.5-15 s: HARD CUT (audio continues in the original) to a wide pan of the full stadium filled with light sticks and phones, ending among the crowd heads.
**Prompt template:**
```text
@Image 1 defines the performer's face, hair and outfit ({outfit}); the performer on stage and the face on the giant screen are this same person.
A fan's smartphone video of a packed stadium concert from an elevated seat: handheld with natural shake, slight rolling shutter, phone-camera colour, one pinch-style zoom. Every sign, screen, banner, stage panel and garment shows plain abstract colour and shape with no lettering, numbers or logos, and phone screens show only a small bright image of the stage.
0-2s: wide from behind the crowd: exactly 4 phones raised in the foreground among the backs of fans' heads, a long runway stage in the distance, the performer centre stage with exactly 2 backup dancers, and a large LED screen above showing the performer's face.
2-5s: handheld digital zoom toward the performer as they walk to the stage edge, singing into a handheld microphone; one phone screen at the bottom of the frame shows them too.
5-12.5s: tight handheld medium shot of the performer singing, then raising their {arm} (frame {arm_side}) to cue the crowd, then turning away to face the stage; the 2 backup dancers stay behind them.
At 12.5s hard cut, the only cut in the clip, to a wide pan across the full stadium filled with {light_sticks} and phones, ending among the crowd heads.
```
**Slots:**
- `{outfit}`: garments and colours as seen.
- `{arm}`: for example "left arm"; `{arm_side}`: the side it appears on, for example "right side".
- `{light_sticks}`: default "glowing handheld light sticks".
**Post:** audio bed from Seed Audio (stadium ambience, crowd swell and reverb with no sung or spoken words and no chanting), laid over the 12.5 s cut; optional phone-UI record dot and similar HUD via HyperFrames or html-graphic-render (the generated video has none). No lip-sync is claimed; the mouth mimes singing.
**QA:**
- Exactly 2 backup dancers and 4 foreground phones in the opening wide shot; jumbotron shows the same face as the performer.
- Visible handheld shake and pinch-style zoom; the look is phone footage, not cinema.
- Exactly one cut, near 12.5 s, to the wide stadium pan; no second cut.
- No lettering, numbers or logos on stage, screens, phones or clothing.
- Generated clip carries no baked-in speech, chant or music.
**Risks:** Too clean a cinematic look. Warped hands and phones in the crowd. Screen content not matching the performer. Backup dancers duplicating. Mouth and mic mismatch. Logo-like glyphs on the stage. A second cut inserted. Native audio would bake in chanting, so it stays off.
**Status:** tested once in the 2026-10-08 showcase run (project `effects-showcase`, scene-17, first-frame (reference route rejected), 480p draft, sound on, one invented subject at 9:16): usable with defects; a sung vocal in the first seconds; the face is small in the opening wide shot; unreadable cursive on the jacket back. Not verified on other photos or at a higher resolution.

### `vanish` - Vanish

**Look:** A person blinks out of existence in one frame and their empty clothes slump to the surface where they stood.
**Route:** `i2v-first-frame`. `@Image 1` = first frame.
**Parameters:** duration 5 s; ratio follows the photo; `generate_audio` false (a soft cloth thud could help but is added in post); draft 480p.
**Start photo:** Person in loose, shape-holding clothing (sweater, skirt, coat, jacket) in a pose where clothes can plausibly collapse (kneeling, leaning, sitting), on an uncluttered surface with a plain background. Bad inputs: tight clothing, standing straight with no surface to collapse onto, a printed or lettered mat or floor (the text garbles), cluttered surface, shoes or accessories that are hard to separate from the body.
**Beats (from the originals):**
- 0-2 s: the subject holds the photo pose almost motionless, looking at the lens; locked camera.
- 2 s: body, head, hands, bare skin and hair vanish in a single frame step; garments remain still holding body shape. This is an instant change, not a cut.
- 2-3 s: the empty garments collapse under gravity and crumple flat on the surface.
- 3-5 s: clothing lies still; the empty scene is held to the end, with no black frame.
**Prompt template:**
```text
@Image 1 is the first frame. {subject} {pose} on {surface}, wearing exactly {garment_count} garments: {garments}. Locked-off static camera, no movement, no cuts. The surface and background show plain colour with no lettering.
0-2s: the subject holds the photo pose, almost motionless, looking into the lens.
At 2s, in a single frame, the subject's body vanishes completely: head, hair, face, neck, hands, feet and all bare skin are gone at once, with no fade, dissolve, particles, glow or see-through residue. The {garments} stay exactly where they were, still holding the body's shape, hollow and empty with no neck, hands, legs or feet inside, and the scene behind is clear through the gap.
From 2s to 3s the garments collapse under gravity in this order: {collapse_order}, crumpling flat onto {surface}.
From 3s to the end the clothes lie completely still; the empty scene stays in frame. {accessories_rule}
```
**Slots:**
- `{subject}`, `{pose}`, `{surface}`: from the photo (for example "kneels with the right hand (frame-left side) on the mat"); name the side of any hand or arm by anatomy plus frame side.
- `{garment_count}`, `{garments}`: count and name every garment in the photo (for example 2: a blue knit sweater and a denim skirt). When the count is 1 write "1 garment" in the sentence.
- `{collapse_order}`: default "sweater first, then skirt".
- `{accessories_rule}`: default "Hair ties, jewellery and shoes vanish with the body, and no new objects appear." If shoes are a visible garment, list them in `{garments}` instead.
**Post:** none. Optional soft cloth-thud effect from Seed Audio at 2-3 s.
**QA:**
- Disappearance happens within one frame step at about 2 s; no gradual fade, ghost or particles.
- Garment count at the end equals the stated count; none vanish, none are added.
- Garments hold body shape for a moment, then collapse and come to rest by about 3 s; no floating clothes.
- Camera is locked; the empty scene is held to the end; no black frame; no text on the surface.
**Risks:** The body fades out gradually. Ghost or semi-transparent residue. Clothing does not collapse and keeps floating in body shape. Invisible-body shapes remain. Extra garments, shoes or hair appear. Collapse timing off. Text on the mat garbles.
**Status:** tested once in the 2026-10-08 showcase run (project `effects-showcase`, scene-18, first-frame, 480p draft, sound on, one invented subject at 9:16): usable with defects; she vanishes about 0.3 to 0.5 s before the 2 s beat; dark trouser patches show at the hoodie shoulders. Not verified on other photos or at a higher resolution.
