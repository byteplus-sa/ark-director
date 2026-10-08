# Effect recipes - Product, creature and spectacle

Nine photo-in effects built around one oversized idea: a product heist, a ticket-wipe walk, a giant creature, an animal ride, a screen-breaking entrance, a fallen knight, a castle reveal, and a time freeze. Every recipe starts from a user photo and reuses one skeleton: photo role sentence (`@Image 1 is the first frame.` or a reference binding), subject by what the photo shows, timestamped stages with one state change each, camera as move + start + end, an optional native-audio line using `<>` sound effects only, and an observable end state. Counts are stated at every stage, props are described by shape and colour (never by lettering), and no caption, label or sign text is requested inside the video.

## Menu rows

| id | label | route | duration | start photo |
| --- | --- | --- | --- | --- |
| `smash-and-grab` | Smash and grab | `i2v-first-frame` | 10 s | Product alone on a car seat, shot through window |
| `boarding-pass` | Boarding pass | `i2v-first-frame` | 9 s | Full-body person on plain white floor |
| `monster-dab` | Monster dab | `i2v-first-frame` | 10 s | Person walking toward camera, open sky behind |
| `pigeons` | Pigeons (animal ride) | `composite` | 8 s | Full-body person on a city pavement |
| `skatedog` | Skatedog (animal ride) | `composite` | 8 s | Full-body person on smooth street or promenade |
| `agamemnon` | Agamemnon | `i2v-first-frame` | 15 s | Selfie taken seated in a dark cinema |
| `mighty-fighter` | Mighty fighter | `composite` | 11 s | Clear face-forward portrait, head and shoulders |
| `fairytale-castle` | Fairytale castle | `i2v-first-frame` | 15 s | Person in profile in an empty dusk meadow |
| `frozen-in-motion` | Frozen in motion | `i2v-first-frame` | 7 s | Full-body person mid-jump on a busy street |

### `smash-and-grab` - Smash and grab

**Look:** A locked shot from inside a car where a thief presses both palms on the window, smashes it with a stone and snatches the product, then a hard cut to a backwards-tracking police chase.
**Route:** `i2v-first-frame`. Image role: `first_frame` only (the product photo). No `reference_image` is mixed in; the thief is described in text and repeated verbatim in both shots.
**Parameters:** duration 10 s; ratio follows the photo (3:4 and 9:16 were seen); `generate_audio` true is justified here because the glass crack and sirens are the payoff (sound effects and ambience only, no music, no speech); draft 480p, then re-render at 720p or 1080p.
**Start photo:** A single product (can, snack bag, bottle) sitting alone on a car back seat, centred low in frame and sharp, shot from inside the car looking out through the closed side window onto a street. Bad inputs: product held by a person, window open or absent, several products, label hidden or blurred, an exterior already crowded with people.
**Beats (from the originals):**
- 0-1.5 s: locked interior shot, product on the seat, a stylised person walks into frame outside the glass from the right and glances in.
- 1.5-3.5 s: the person stops, presses both palms flat on the glass and stares at the product.
- 3.5-5.3 s: steps back, leaves frame, returns and looks in; window briefly empty.
- 5.3-6 s: winds up with a stone and throws it.
- 6-7.3 s: window shatters inward, glass sprays across the seat, the right arm (frame-left side as seen from inside the car) reaches through and lifts the product out toward the lens.
- **Hard cut at about 7.6 s.**
- 7.6-10 s: exterior street at golden hour, the thief runs toward camera hugging the product, two police officers with flashing lights chase behind; camera tracks backwards at runner speed with motion blur.
**Prompt template:**
```text
@Image 1 is the first frame: {product_description} alone on {seat_description} inside a parked car, seen through the closed side window with {street_view} outside. {label_clause}
Shot 1, locked-off interior camera at eye level. At 0s a thief, {thief_outfit}, walks into frame outside the glass from the right and glances in, hands empty. At 1.5s the thief stops, presses both palms flat on the glass and stares at the product. At 3.5s the thief steps out of frame, returns at 4.5s and looks in. At 5.3s the thief's right hand (frame-left side as seen from inside the car) lifts one grey stone, winds up and throws it. At 6s the window shatters inward, glass sprays across the seat, and the thief's right arm (frame-left side as seen from inside the car) reaches through, closes that hand around the product{label_cover}, and lifts it out of frame by 7.3s.
At 7.6s, hard cut to Shot 2: exterior street at golden hour, backwards tracking shot at eye level with handheld energy at the runner's speed, background streaking with motion blur. The same thief in the same outfit runs toward the camera hugging the product to the chest with both arms, label turned inward. Exactly two police officers in plain dark uniforms chase twenty metres behind, followed by one plain patrol car with flashing red and blue lights. The clothing, uniforms and vehicles are plain, with no lettering.
Audio includes <a glass pane cracking and shattering> and <distant sirens>, with street ambience only, no music and no speech.
The clip ends with the thief mid-stride in the centre of frame, product in both arms, two officers behind.
```
**Slots:**
- `{label_clause}`: "The label stays exactly as photographed, with no added lettering." for a labelled product; "The surface stays plain, with no added lettering." for an unlabelled one.
- `{label_cover}`: ", the fingers covering the label" for a labelled product, otherwise empty.
- `{product_description}`: shape, colour, material and finish read from the photo, no brand words (for example "a slim glossy pink aluminium can").
- `{seat_description}`: read from the photo (for example "a black leather back seat").
- `{street_view}`: what the window shows, read from the photo.
- `{thief_outfit}`: written once and reused unchanged in Shot 2; default "a light-blue short-sleeved shirt with a striped tie, a red baseball cap, large dark sunglasses, red shorts, white socks and blue sandals".
- The Audio sentence is included only if `generate_audio` is true; with native audio off, omit it.
- Hand naming: the thief faces the glass, so as seen from inside the car the thief's right hand is on frame-left; use "right hand (frame-left side as seen from inside the car)" every time.
- Branded product: the label comes from the real photo or an authorized real asset (official pack shot or a user-supplied download), never from Seedream or prompt text. If no usable real image exists, ask the user; do not generate a label.
**Post:** none. Optional: if the exact label must read cleanly after the cut, cover that moment with an FFmpeg or HyperFrames pack-shot insert built from the real asset.
**QA:**
- Exactly one hard cut near 7.6 s; Shot 1 has no camera movement.
- Hands are empty until the wind-up; the stone appears only at the throw.
- Glass shatters inward with spray on the seat and no intact pane left.
- Exactly two officers; the thief's outfit matches across the cut.
- No stray text on clothing, cars or the label beyond what the photo already shows.
**Risks:** outfit and identity drift across the cut; the label warps during the grab close-up (the recipe covers it with the fingers to avoid showing it); lettering invented on the can, uniforms or patrol car; officer count drifts; stone appearing early; native audio adding a music bed. If the product photo carries a real logo, never regenerate it in a derived reference. Probe result: a short shouted voice appeared in native audio despite 'no music and no speech'; for a clean track keep native audio off and add the glass and siren sound effects in post. A draft promotion reuses the draft's audio, so verify the draft's track for speech and music before promoting. Probe result: the carried object is easy to lose in the chase shot, so say what the thief carries and keep it in view.
**Status:** probed 2026-10-08, one 480p draft in project `effects-probe` (scene-12, unlabelled cream jar, native audio on): the thief walked in, pressed both palms to the glass, stepped out and back, threw a stone, the window shattered and he grabbed the jar; the hard cut to a backwards-tracked chase with two officers and a patrol car landed at 7.6 s. The soundtrack had no music and the glass crack at about 6 s, but a shouted onlooker line leaked in despite 'no speech'. A defect scan found a translucent ghost jar beside the real one at about 0.5 s, and the jar was not clearly visible in the thief's arms in the chase shot; the cut landed at about 7.2 s. The template was amended after review (the right hand and arm are named by frame side, the Audio sentence is conditional on `generate_audio` and ends with 'no music and no speech', and a plain no-lettering clause was added for clothing, uniforms and vehicles); the amendment is not re-probed.

### `boarding-pass` - Boarding pass

**Look:** A person walks left to right on a white floor and each giant flight-ticket card that sweeps in wipes the backdrop above it into a new city.
**Route:** `i2v-first-frame`. Image role: `first_frame` only (the full-body photo); the cities, tickets and optional outfits are text-described. A deterministic text overlay is optional (see Post).
**Parameters:** duration 9 s (use 10 s if the final wave is cut short); ratio follows the photo (9:16 or 3:4 were seen); `generate_audio` false; draft 480p.
**Start photo:** Full-body person standing on a plain white or light studio floor with a visible ground shadow, empty space around and above, feet visible. Bad inputs: cropped legs, busy background, floor in a strong colour or pattern, subject facing the camera squarely with arms occupied.
**Beats (from the originals):**
- 0-1.7 s: plain white studio; subject walks in profile, soft shadow.
- 1.7-3.7 s: ticket 1 sweeps across as a wipe; the backdrop above it becomes city 1 at golden hour.
- 3.7-6.7 s: ticket 2 wipes in; backdrop becomes city 2 at dusk or night; a small gesture such as adjusting glasses.
- 6.7-8.3 s: ticket 3 wipes in; backdrop becomes city 3 at sunset; subject slows.
- 8.3-9 s: subject stops, turns to the camera and waves; final backdrop and ticket hold.
- No hard cuts: the wipes happen inside one locked take.
**Prompt template:**
```text
@Image 1 is the first frame: {subject} standing on a plain white studio floor with a soft ground shadow, full body visible, wearing {outfit_description}. The face, outfit and floor stay unchanged{outfit_change_clause}.
Locked-off static camera at eye level, side-on full-body frame, no camera movement. From 0s the subject walks left to right at one constant relaxed pace, {walking_hand_action}, the white floor and soft shadow always under the feet.
Exactly three giant flight-ticket cards appear one after another. Each ticket is a flat upright card as wide as the frame, filling the lower half of the frame behind the walker, with a coloured header band, a row of vertical black barcode stripes along its lower edge, and a perforated vertical edge on its leading side; each ticket is blank apart from those shapes.
At 1.7s ticket 1 ({ticket_1_colour}) slides in from the right, its perforated edge sweeping right to left across the frame, and the area above the ticket becomes {city_1_scene}. At 3.7s ticket 2 ({ticket_2_colour}) sweeps in the same way and the backdrop above it becomes {city_2_scene}. At 6.7s ticket 3 ({ticket_3_colour}) sweeps in the same way and the backdrop becomes {city_3_scene}.
At 8.3s the subject slows, stops, turns to face the camera and raises the left hand (frame-right) in a wave. The final backdrop and ticket hold to the end.
```
**Slots:**
- `{subject}`: read from the photo (apparent age, hair, one clothing item), never a name.
- `{outfit_description}`: read from the photo.
- `{outfit_change_clause}`: default empty (one outfit, lowest identity risk). Optional: "except that the outfit changes at each ticket edge to {outfit_2}, then {outfit_3}, then {outfit_4}", with every outfit written out.
- `{walking_hand_action}`: read from the photo, naming any single hand by anatomy plus frame side (for example "the right hand (frame-left) holding a phone at chest height"); if nothing is held, "both arms swinging loosely".
- `{ticket_1_colour}`, `{ticket_2_colour}`, `{ticket_3_colour}`: three different pastel header-band colours, defaults teal, lilac, coral.
- `{city_1_scene}`, `{city_2_scene}`, `{city_3_scene}`: landmark and light described without any name text, default "a historic canal town with a tall stone bell tower at golden hour", "a golden-domed hilltop skyline under a deep blue night sky", "a coastal city skyline with a domed building against a large orange sunset". Ask the user which cities if they care; city names are for the prompt only and never appear on screen.
**Post:** optional. Tickets are generated blank because the model garbles lettering. If city names are wanted, render them with html-graphic-render or HyperFrames after each ticket settles (about 3.2 s, 6.2 s, 8.0 s) and key them behind the walker, since the subject passes in front of the ticket; otherwise ship blank tickets.
**QA:**
- Exactly three tickets, wipe edge travelling right to left, city only above the ticket.
- Camera never moves; floor and shadow persist at every wipe.
- Same face and (unless outfits were requested) same outfit before and after every wipe.
- Final wave occurs after about 8 s with the last backdrop holding.
- No lettering generated on tickets.
**Risks:** feet slide at the wipe edge; shadow breaks; ticket count drifts; outfit change per ticket causes face drift and outfit-count errors; the model writes garbled text on tickets even when asked for blank cards; 0.7 s for the turn-and-wave is tight. A real-person photo may be refused or drift; the route for identity-bound work is a Virtual Portrait asset (`asset://`) for an invented character, never a real specific person.
**Status:** untested hypothesis (analysis 2026-10-08)

### `monster-dab` - Monster dab

**Look:** A building-sized creature wearing a copy of the subject's outfit crashes in behind a calmly walking subject, looms around them and bounds out of frame.
**Route:** `i2v-first-frame`. Image role: `first_frame` only (the walking photo). The creature is text-described; do not prompt a dab pose (it never appears in the originals).
**Parameters:** duration 10 s; ratio follows the photo (4:3 and 16:9 were seen); `generate_audio` false by default (the originals had no audio); true is acceptable for the landing thud if the prompt keeps to sound effects and ambience; draft 480p.
**Start photo:** Full-body or three-quarter person walking toward the camera in daylight, open ground and visible sky, eye-level wide framing with room above and behind. Bad inputs: tight portrait, indoor ceiling, crowded foreground, subject far from the lens or facing away.
**Beats (from the originals):**
- 0-1 s: subject walks toward the camera; empty sky behind.
- 1-2.5 s: the creature crashes in from above the frame behind the subject, dust cloud on landing; it wears a colour-copy of the subject's outfit.
- 2.5-7 s: creature looms over and around the subject (feet and hands at frame edges, leaning down with a grin); subject walks on, glances up once, stays small and calm.
- 7-8.5 s: creature springs up out of the top of frame, dust hangs.
- 8.5-10 s: creature gone; subject continues into a close-up.
- No hard cuts; camera locked.
**Prompt template:**
```text
@Image 1 is the first frame: {subject} walking steadily toward the camera along {location}, looking at the lens, wearing {outfit_description}. The subject's face, outfit and walk stay unchanged and the sky behind is empty.
Locked-off static camera at eye level, standard wide lens, no push-in, no shake.
At 1s exactly one colossal invented creature, {creature_design}, drops from above the top edge of the frame behind the subject and lands in a cloud of dust. It wears a colour-matched copy of the subject's outfit: {outfit_copy}. The creature is taller than {scale_reference}, and the subject stays tiny at its feet. From 2.5s to 7s the creature looms over and around the subject, its feet and hands at the frame edges, leaning down with a wide grin and poking the air beside the subject, while the subject keeps walking toward the camera, glances up once and stays calm. The creature's shadow falls in the same direction as the subject's shadow. At 7s the creature springs upward out of the top of the frame, tail and feet last, and dust hangs in the air. At 8.5s the sky is empty again and the subject continues toward the camera into a close-up with a faint dust trail.
{audio_line}
```
**Slots:**
- `{subject}`: read from the photo (apparent age, hair, one clothing item), never a name.
- `{outfit_description}`: read from the photo (garments, colours, bag).
- `{location}`: read from the photo (market street, seaside promenade).
- `{creature_design}`: invented and unbranded, default "a lanky grey humanoid with long arms and a wide grin" or "an orange-maned horned humanoid"; no franchise or existing-character look.
- `{outfit_copy}`: the same garments in the same colours, rewritten for the creature's body.
- `{scale_reference}`: the tallest visible thing in the photo (stalls, buildings, palm trees).
- `{audio_line}`: empty unless `generate_audio` is true; then "Audio includes <a heavy landing thud> at 1s and <a soft whoosh> at 7s, with outdoor ambience only, no music and no speech."
**Post:** none.
**QA:**
- Exactly one creature, entering from above the top edge and exiting through it.
- Creature is visibly taller than the stalls or buildings; subject never grows to match.
- Creature wears the subject's outfit colours.
- Camera stays locked; subject keeps walking toward the lens and the face stays recognisable.
- Shadows share one direction; no clipping or fusing of creature and subject.
**Risks:** scale collapses to normal size; creature identity drifts frame to frame; subject face drifts as it nears the lens; creature and subject fuse or clip; shadow mismatch; unwanted push-in or shake; second creature appears; native audio invents a roar or score. Confidence from the originals is medium. Real-person photo: a real face may be refused or drift; the identity route is a Virtual Portrait asset (`asset://`) for an invented character, and a real specific person needs separate rights and consent.
**Status:** untested hypothesis (analysis 2026-10-08)

### `pigeons` - Pigeons (animal ride)

**Look:** A rider hovers down a city street standing on two flapping pigeons like roller skates, filmed on a low circular-fisheye tracking camera.
**Route:** `composite`. Seedance image role: `first_frame` only (the street photo). The circular fisheye look is applied deterministically with FFmpeg afterwards because a rectilinear first frame fights a native fisheye request.
**Parameters:** duration 8 s; ratio follows the photo (16:9 seen; the fisheye post output is square or follows the photo); `generate_audio` false; draft 480p.
**Start photo:** Full-body person standing on a city pavement or street, feet visible with clear ground below, space ahead. Bad inputs: cropped feet, sitting or crouching pose, crowded foreground, indoor floor with no street reading.
**Beats (from the originals; the shared gallery shows puffins, dolphins and dogs, none pigeons, so the page was thin for this slug):**
- 0-1.5 s: rider glides forward, arms flung out, a bird flapping under each boot, beside a curved glass tower; pedestrians whip past with motion blur.
- 1.5-4 s: rider carves round a corner, birds stay one under each foot, hovering 1-2 ft above the pavement.
- 4-6 s: camera swings from low and close to slightly wider; rider leans through a turn, crouches, steadies a held item.
- 6-8 s: rider glides away down the pavement past offices and trees, pedestrians not reacting.
- No hard cuts.
**Prompt template:**
```text
@Image 1 is the first frame: {subject} standing on {street}, full body, feet visible. The rider's face, hair and clothing stay unchanged.
Ultra-wide low-angle tracking shot at ground level, one continuous take without cuts: the camera moves forward at the rider's speed with a slight clockwise arc around the rider, starting close and low and ending slightly wider and higher.
At 0s exactly two grey city pigeons sweep in from the frame edges at ground level and slide under the soles, one under each foot, their backs flat beneath the shoes, both wings beating fast and wide. By 1.5s the rider hovers 30 to 60 centimetres above the pavement in a bent-knee skate stance with both arms flung out, gliding forward {first_path}. From 1.5s to 4s the rider carves round a gentle corner, shoulders turning first and head following, one pigeon staying under each foot. From 4s to 6s the rider leans through a turn, crouches slightly and steadies {held_item}. From 6s to 8s the rider glides away down the pavement as the camera widens, pedestrians walking past without reacting. The clip ends with the rider small in the frame, both pigeons still under both feet, wings beating.
```
**Slots:**
- `{subject}`: read from the photo (apparent age, hair, one clothing item), never a name.
- `{street}`: read from the photo.
- `{first_path}`: read from the photo (for example "along a curved glass tower").
- `{held_item}`: what the rider holds in the photo (for example "the coffee cup in the rider's right hand, frame-left side"; name any single hand by anatomy plus frame side); if nothing, "their balance with both arms".
- Species: the effect name says pigeons, the originals used puffins. Use "grey city pigeons"; swap to puffins only if the user asks.
**Post:** FFmpeg fisheye: apply `v360=input=flat:output=fisheye` with `ih_fov` and `iv_fov` set to the assumed source field of view, to a square canvas, so the corners become a round black vignette; inspect that the rider stays inside the circle and the edges are filled. Fallback if the user wants a single pass: add "circular fisheye lens with a round black vignette and heavy barrel distortion" to the camera sentence and accept lens-look drift.
**QA:**
- Exactly two birds, one under each foot, touching the soles, wings visibly beating.
- Rider hovers about 1-2 ft above the ground in a bent-knee stance with arms out.
- Camera low, tracking, one take; after post the frame is a round fisheye with black corners.
- Rider face and clothing match the photo; pedestrians neither react nor morph.
**Risks:** bird count drifts to one or three; birds fuse with shoes or drift in front; feet float above the birds; wing motion reads static; the fisheye reads as plain wide-angle (hence the post); rider face drift; pedestrians morph. Real-person photo: a real face may be refused or drift; the identity route is a Virtual Portrait asset (`asset://`) for an invented rider, and a specific real person needs separate rights and consent.
**Status:** untested hypothesis (analysis 2026-10-08)

### `skatedog` - Skatedog (animal ride)

**Look:** A rider stands on the back of one running dachshund as if it were a skateboard, carves, jumps a ledge and rides away, filmed on a low circular-fisheye tracking camera.
**Route:** `composite`. Seedance image role: `first_frame` only (the street photo). Circular fisheye is applied deterministically with FFmpeg afterwards.
**Parameters:** duration 8 s; ratio follows the photo (4:3 and 1:1 were seen); `generate_audio` false; draft 480p.
**Start photo:** Full-body person on a street, promenade or plaza with smooth ground, feet visible, ideally with a low ledge or planter somewhere ahead. Bad inputs: cropped feet, rough or cluttered ground, rider seated, no ground visible.
**Beats (from the originals; shared gallery, page thin for this slug):**
- 0-1 s: rider lands on a running brown dachshund on a wet dusk promenade, bent-knee skate stance, arms out.
- 1-4.5 s: steady ride, camera arcs round them so sea and streetlights swap sides.
- 4.5-6.3 s: dog runs up onto a low concrete ledge with the rider on its back.
- 6.3-8 s: they drop off the far edge, land and ride away; camera tilts back down as the pair shrinks.
- No hard cuts.
**Prompt template:**
```text
@Image 1 is the first frame: {subject} standing on {ground}, full body, feet visible. The rider's face, hair and clothing stay unchanged.
Ultra-wide low-angle tracking shot at ground level, one continuous take without cuts: the camera moves forward at the rider's speed, arcs around the pair so the background swaps sides, then tilts down and ends wider as they ride away.
At 0s exactly one {dog_colour} dachshund, long low body, four short legs, nose pointing forward, runs in from the frame edge beneath the rider. At 1s the rider steps onto the dog's back with both feet, bent-knee skate stance, arms out, riding on top of the dog rather than beside it. The dog keeps normal proportions and a steady even trot throughout, tail up and looking playful and unhurt. From 1s to 4.5s they ride forward along {ground}. At 4.5s the dog runs up onto {ledge} with the rider balanced on its back in a small ollie-like lift. At 6.3s they drop off the far edge, land with both of the rider's feet on the dog's back, and keep riding away. By 8s the pair is small in the distance, rider still on top of the dog.
```
**Slots:**
- `{subject}`: read from the photo (apparent age, hair, one clothing item), never a name.
- `{ground}`: read from the photo.
- `{dog_colour}`: default "short-haired brown".
- `{ledge}`: the nearest low ledge, kerb or planter in the photo; if none, "a low concrete kerb" and say so to the user.
- The dachshund is invented and unbranded; if the user supplies a dog photo, that is a different recipe (reference_image cannot mix with first_frame).
**Post:** same FFmpeg fisheye step as `pigeons`: `v360=input=flat:output=fisheye` on a square canvas, inspect rider and dog stay inside the circle.
**QA:**
- Exactly one dog with four legs and a normal-length dachshund body (no stretching).
- Both feet on the dog's back for the whole ride, dog beneath the rider, never beside.
- Ledge climb at about 4.5 s and drop at about 6.3 s; one continuous take.
- Round fisheye with black corners after post; face matches the photo.
**Risks:** dog leg count and gait errors; the dachshund elongates; rider feet float or sink into the dog; the dog's posture does not reflect the rider; dog changes between frames; face drift on the ledge jump; fisheye reads plain-wide without post. Keep the dog tone playful. Real-person photo: a real face may be refused or drift; the identity route is a Virtual Portrait asset (`asset://`) for an invented rider, and a specific real person needs separate rights and consent.
**Status:** untested hypothesis (analysis 2026-10-08)

### `agamemnon` - Agamemnon

**Look:** A cinema audience watches a burning-siege movie until the screen rips open and armoured warriors step out into the theatre.
**Route:** `i2v-first-frame`. Image role: `first_frame` only (the cinema selfie). The screen footage, hero and warriors are text-described; the whip-pan is scripted so the wide shot stays in the same auditorium.
**Parameters:** duration 15 s; ratio follows the photo (16:9 and 3:4 were seen); `generate_audio` true is justified for the screen rip and fire (sound effects and ambience only; the model otherwise invents a score and roar); draft 480p.
**Start photo:** A selfie or first-person phone photo taken seated in a dark cinema, face lit, seats and audience behind, a projector beam or screen glow visible. Bad inputs: no cinema cues, face in shadow, standing in a lobby, a screen visible with real film frames or a recognisable poster on it. Likeness: use only the user's own photo or a photo they have consent for; real-face handling follows the repo's real-person contract.
**Beats (from the originals):**
- 0-3 s: handheld selfie, the subject grins mouth open, audience and projector beam behind.
- 3-5 s: fast whip-pan from the face to the curved screen; the screen shows a medieval siege at a burning stone gate. Cut at about 3 s (a scene detector fired near 3.2 s).
- 5-7 s: static wide view from the audience of the screen; a fireball bursts from the gate.
- 7-8 s: the screen tears open in smoke and orange fire, white fabric flaps, a dark plumed-helmet warrior steps out onto the stage.
- 8-12 s: two to three smaller armoured warriors flank and rush out; audience heads turn and several stand; the hero raises a fist and stands central in the smoke.
- 12-15 s: slow push-in on the hero in front of the fire.
**Prompt template:**
```text
@Image 1 is the first frame: {subject} seated in a cinema taking a selfie, {seat_surroundings}, face lit by the projector beam. The subject's face stays unchanged while visible.
0s to 3s: handheld selfie camera with slight shake; the subject grins, mouth open in excitement. At 3s whip-pan rapidly to the {pan_direction}; cut when the blurred dark seat rows fully cover the frame, then arrive on a static wide shot from the audience side of the same auditorium, the curved screen filling the frame centre, audience seated in the foreground.
The screen shows a medieval siege at a burning stone gate. At 5s a fireball bursts from the gate. At 7s the screen fabric rips open along that same gate in smoke and orange fire, and an ancient Greek warrior king steps out of the tear onto the stage: black armour, a red-crested plumed helmet, a dark cape. From 8s exactly two smaller warriors in matching dark armour rush out and flank the hero, audience heads turn and several stand. At 10s the hero raises a fist and stands central in the smoke. From 12s a slow push-in on the hero ends in a medium close-up with the fire behind the hero. The screen, armour and banners are plain, with no lettering or subtitles.
{audio_line}
The clip ends on the hero centred in the smoke, two warriors flanking the hero, the torn screen burning behind.
```
**Slots:**
- `{subject}`: read from the photo (apparent age, hair, one clothing item), never a name.
- `{seat_surroundings}`: read from the photo (seats, popcorn, audience).
- `{pan_direction}`: left or right, whichever side the screen lies on in the photo; default "right".
- `{audio_line}`: empty unless `generate_audio` is true; then "Audio includes <a fireball roar> at 5s, <fabric tearing> at 7s and <a low crowd murmur>, with sound effects and room ambience only, no music and no speech."
- Hero costume is fixed as above and generic; never name a film, character or actor.
**Post:** none; optional Seed Audio bed or score added afterwards if the user wants music.
**QA:**
- Selfie (0-3 s), one whip-pan, then a wide shot in the same auditorium rather than a new location.
- Screen shows the gate and fire first; the tear opens at that gate and the hero steps out of it.
- Hero plus exactly two warriors, not a horde; one hero costume throughout.
- Curved screen geometry holds; hero stays visible in the smoke.
**Risks:** selfie face drifts after the whip-pan; audience faces melt; the curved screen flattens; warriors appear on the screen instead of stepping out; smoke hides the hero; fire flickers; native audio invents a score. A real-person photo may be refused or drift; the identity route is a Virtual Portrait asset (`asset://`) for an invented character, and a specific real person needs separate rights and consent. Confidence from the originals is medium.
**Status:** untested hypothesis (analysis 2026-10-08)

### `mighty-fighter` - Mighty fighter

**Look:** A battered knight in a misty poppy field drops the helmet, is revealed face-last by a slow tilt up, then lies fallen among the flowers.
**Route:** `composite`. Seedance image role: `reference_image` for the portrait in both shots (identity only), and no `first_frame`. First_frame cannot mix with reference_image, and a first_frame portrait would open on the face, which kills the legs-first, face-last reveal and puts a face-forward portrait where the scene needs boots; so the portrait is an identity reference and the opening is text-described. Two Seedance generations (shot A, shot B) are joined with an FFmpeg hard cut so the cut lands exactly where wanted.
**Parameters:** two separate requests, each with its own prompt snapshot, review and take: Shot A duration 7 s, Shot B duration 4 s (11 s total; trim shot B in post if wanted); ratio chosen to match the portrait orientation (9:16 for vertical, 16:9 for landscape) because no first frame locks it; `generate_audio` false by default (a helm thud and wind sting would help; keep it to sound effects); draft 480p.
**Start photo:** A clear face-forward portrait or head-and-shoulders photo in even light with hair and face unobstructed. Bad inputs: sunglasses, a hat or heavy shadow, a very small face, group photos, heavy filters. Likeness: use only the user's own photo or a photo they have consent for; real-face handling follows the repo's real-person contract.
**Beats (from the originals):**
- 0-1.5 s: ground-level close-up of armoured legs and a long white cape in dewy red poppies at blue-hour dusk; the knight takes a slow step, a helmet hangs from one hand.
- 1.5-3 s: the helmet drops and thuds into the grass beside the boots as the camera starts to tilt up.
- 3-6.5 s: slow tilt up greaves, belt, sword and engraved breastplate to the face: tired, bruised, dazed, mist behind; the knight sways and begins to buckle.
- **Hard cut at about 6.5 s (7 s in this recipe), made in post by joining the two takes.**
- 6.5-10 s: static side or high-angle shot of the knight lying on the back in the poppies, eyes closed, the right hand on the breastplate, petals drifting.
- Two requests: the first prompt block below is Shot A, the second block is Shot B.
**Prompt template:**
```text
@Image 1 defines the knight's face, hair and skin tone only; the face is first visible at 5s.
A battle-worn knight in {armour_block} walks slowly through dewy red poppies at blue-hour dusk, mist over the field. The armour, helm and cloak are plain, with no lettering anywhere in frame.
Low-angle camera at ground level, shallow depth of field. From 0s the frame shows only boots, greaves and the lower cloak; the knight takes one slow step, a steel great helm with a chainmail collar hanging from the knight's left hand (frame-right). At 1.5s the hand opens and the helm drops, thudding into the grass beside the boots. From 3s the camera tilts up slowly along the greaves, belt, sword and breastplate, reaching the face at 5s: tired, a few dirt smudges, dazed eyes, sunrise glow and mist behind. From 6s the knight sways and the knees begin to buckle. The shot ends on the face and shoulders.
{audio_line_a}
```
**Prompt template, Shot B (separate request, joined to Shot A by a hard cut in post):**
```text
@Image 1 defines the knight's face, hair and skin tone only.
The same knight in {armour_block} lies on the back among red poppies in a misty field at dawn, head toward frame-right, eyes closed, the knight's right hand (the hand nearest the camera, lower in frame) resting on the breastplate, a few petals drifting across the frame. Locked-off static camera in a high side-angle wide shot, no camera movement. The knight lies still; only the petals and mist move. The armour and cloak are plain, with no lettering anywhere in frame. The shot ends on the same still pose.
{audio_line_b}
```
**Slots:**
- `{armour_block}`: pasted identically into both shots; default "polished silver plate armour with an engraved breastplate, a sword belt with one sword, and a long white cloak".
- `{audio_line_a}`: empty unless `generate_audio` is true; then "Audio includes <a heavy helm thud> at 1.5s and <wind>, with ambience only, no music and no speech."
- `{audio_line_b}`: empty unless `generate_audio` is true; then "Audio includes <soft wind> only, with ambience only, no music and no speech."
- Portrait: user photo as `reference_image`; orientation sets the ratio.
- Poppy field, helm and mist are invented, no sourcing needed.
**Post:** the hard cut is made here: FFmpeg concat of the Shot A take (7 s) and the Shot B take (4 s); no crossfade.
**QA:**
- Face appears only after about 5 s of shot A; legs and helm come first.
- Helm lands on the ground (not worn); exactly one sword.
- Knight buckles at the end of shot A; shot B shows the knight already lying on the back, eyes closed.
- Face in shot B matches shot A and the portrait; no blood.
- No text anywhere in frame.
**Risks:** face drift between shot A and shot B; helmet physics (appears worn or floats); armour merges with the cloak; extra swords; the face never fully matches the portrait; the collapse reads as a glitch. Real-person photo: a real face may be rejected as a `reference_image`; the identity route is a Virtual Portrait asset (`asset://`, see the video-to-video inputs contract) for an invented character only, and a specific real person needs separate rights and consent. Single-pass fallback: one 11 s generation with the portrait as `reference_image` and the cut written as "At 7s, hard cut to", at the cost of a less reliable cut.
**Status:** untested hypothesis (analysis 2026-10-08)

### `fairytale-castle` - Fairytale castle

**Look:** A figure in an empty twilight field runs toward a glowing castle revealed by a rising pullback, with a winding stream and fireworks.
**Route:** `i2v-first-frame`. Image role: `first_frame` only (the empty-field photo); castle, stream, sheep and fireworks are text-described and must not be in the photo.
**Parameters:** duration 15 s; ratio follows the photo (4:3 seen); `generate_audio` false by default (distant fireworks and wind would be the only useful sting); draft 480p.
**Start photo:** Person in profile or three-quarter, full or near-full body, in an empty open meadow at dusk with space ahead and an empty horizon; a distinctive dress or costume helps. Bad inputs: buildings or trees on the horizon, a seated or crouching pose, a tight crop, an indoor setting.
**Beats (from the originals):**
- 0-3 s: subject in profile, pink-tinted clouds; sheep run across in front of the subject.
- 3-5 s: the subject turns the head to camera and smiles, then back to the horizon.
- 5-8 s: the subject runs away, the garment flaring; camera follows from behind and starts rising.
- 8-10 s: castle appears on the horizon, a winding reflective stream comes into view as the camera pulls up and back to a high wide shot.
- 10-15 s: fireworks bloom over the castle, reflected in the stream; the subject keeps running, the sky deepens to night.
- No hard cuts.
**Prompt template:**
```text
@Image 1 is the first frame: {subject} standing in profile in an empty meadow at dusk, wearing {outfit_description}, pink-tinted clouds above an empty horizon. The face and the {garment_colour} {garment} stay unchanged as the continuity anchor.
0s to 3s: locked-off eye-level medium-wide shot; exactly {sheep_count} white sheep run across in front of {pronoun_object} from frame-right to frame-left. At 3s {pronoun_subject} turns {pronoun_possessive} head toward the camera and smiles, then looks back to the horizon at 5s. At 5s {pronoun_subject} turns and runs away across the meadow, the {garment} flaring, and the camera follows from behind while craning up and pulling back. At 8s a glowing fairytale castle with several slender towers appears on the horizon directly ahead of {pronoun_object}, and a winding reflective stream curves through the meadow in the foreground. By 10s the camera reaches a high wide establishing view; {pronoun_subject} is small but still wears the {garment_colour} {garment} and keeps running toward the castle. From 11s to 15s exactly {firework_count} fireworks bloom one at a time above the castle, reflected in the stream, and the sky deepens to night.
The clip ends on the high wide view: castle lit, last firework fading, the runner still running toward the castle.
```
**Slots:**
- `{subject}`: read from the photo (apparent age, hair, one clothing item), never a name.
- `{outfit_description}`, `{garment}` and `{garment_colour}`: read from the photo; `{garment}` is the main flowing garment noun the photo shows (for example dress, skirt, long coat) and the colour is the continuity anchor once the subject is small.
- `{pronoun_subject}`, `{pronoun_object}` and `{pronoun_possessive}`: the subject's pronouns (for example she, her, her; he, him, his), asked from the user when the photo does not settle it. For singular they, write "the runner" in place of `{pronoun_subject}` so verbs stay singular.
- `{sheep_count}`: a number word of at least two, default four.
- `{firework_count}`: a number word of at least two, default five.
**Post:** none.
**QA:**
- No castle in the first 5 s; it appears on the horizon ahead of the subject around 8 s.
- Exact sheep count crossing right to left in the first 3 s.
- Camera rises and pulls back into a high wide view with the stream visible and curving.
- Subject keeps the garment colour and moves toward the castle; fireworks appear only from about 11 s.
**Risks:** the castle appears too early or looks pasted in; subject scale and identity drift once the subject is small; sheep count drifts; fireworks flicker or smear; sky continuity between dusk and night; the follow-plus-crane move (two moves, the limit) destabilises. Real-person photo: a real face may be refused or drift; the identity route is a Virtual Portrait asset (`asset://`) for an invented character, and a specific real person needs separate rights and consent.
**Status:** untested hypothesis (analysis 2026-10-08)

### `frozen-in-motion` - Frozen in motion

**Look:** One person hangs motionless in mid-air in a busy street while pedestrians and traffic flow past at normal speed.
**Route:** `i2v-first-frame`. Image role: `first_frame` only (the mid-air photo); the surrounding traffic and crowd are text-described additions to what the photo already shows.
**Parameters:** duration 7 s; ratio follows the photo (9:16 seen); `generate_audio` false (a Seed Audio street bed in post avoids speech or music baked into native audio); draft 480p.
**Start photo:** Full-body person captured mid-jump, mid-stride or in a mid-air pose (leg kicked out, splits, arms wide) on a busy city street or plaza, ground and background readable, ideally with a visible cast shadow. Bad inputs: a grounded stance, motion blur on the subject, a tight crop, an empty location, night scenes with an unreadable shadow.
**Beats (from the originals):**
- 0-7 s: camera locked; the subject holds the exact photographed airborne pose for the whole clip.
- 0-2 s: a bus passes behind, pedestrians stream through, one walker crosses the foreground in front of the subject.
- 2-5 s: dog walkers, more pedestrians and vehicles cross behind.
- 5-7 s: a yellow taxi crosses behind; the crowd keeps moving, the subject stays frozen.
- No hard cuts.
**Prompt template:**
```text
@Image 1 is the first frame: {subject} frozen in mid-air in the exact photographed pose ({pose_description}) on {street}, with the cast shadow on the ground. Locked-off static camera at eye level, full-body medium-wide frame, no camera movement.
For the full 7s the subject stays exactly in that pose, floating at the same height above the ground, with no movement of the body, face, hair or clothing and the cast shadow unchanged, while everything else moves at normal speed.
At 0s exactly one {vehicle_a} passes behind the subject from left to right and leaves frame by 2s; a steady stream of pedestrians walks behind at an even pace, about {pedestrian_count} visible at any moment. At 1s one pedestrian in {crosser_clothing} walks across the foreground in front of the subject, briefly hiding part of the pose without touching it, then exits. From 2s to 5s exactly one dog walker with exactly one dog crosses behind, and exactly one cyclist rides past behind. At 5s exactly one plain yellow taxi crosses behind from right to left. The vehicles, clothing and shopfronts are plain, with no lettering or signs. The clip ends with the subject still floating in the first-frame pose while the crowd keeps moving.
```
**Slots:**
- `{subject}`: read from the photo (apparent age, hair, one clothing item), never a name.
- `{pose_description}`: read from the photo; name any single limb by anatomy plus frame side (for example "the left leg (frame-right) kicked out, both arms wide").
- `{street}`: read from the photo.
- `{vehicle_a}`: default "red double-decker bus with plain solid-colour sides".
- `{pedestrian_count}`: a number word of at least three, default six.
- `{crosser_clothing}`: any clothing colour different from the subject's.
- If the photo already shows people or vehicles, keep them and reduce the added counts to match.
**Post:** optional Seed Audio street bed (traffic and footsteps, no speech or music) mixed in FFmpeg.
**QA:**
- Subject pose, height off the ground, hair and cast shadow stay identical across all 7 s.
- Camera locked.
- Counts hold: one bus, one dog with one walker, one cyclist, one taxi.
- The foreground walker crosses in front without merging with the subject.
- No lettering on vehicles or clothing.
**Risks:** the subject starts to fall, land or sway; micro-motion in the face or breathing; pedestrians morph near the subject; the shadow shifts; crowd chaos when counts are not stated; the foreground crossing is the occlusion stress test. Real-person photo: a real face may be refused or drift; the identity route is a Virtual Portrait asset (`asset://`) for an invented character, and a specific real person needs separate rights and consent.
**Status:** untested hypothesis (analysis 2026-10-08)
