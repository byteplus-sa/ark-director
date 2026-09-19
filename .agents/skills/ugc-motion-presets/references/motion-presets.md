# Motion Presets

45 recipes, each an original Seedance 2.5 direction composed for this
workspace. Recipes are creative heuristics — no preset is ranked over another
by any measured claim.

**Read only the category section containing the resolved preset.** Each recipe
fills the six-part formula slots per the skill's composition rules; cross-cut
constraints live in [execution-constraints.md](execution-constraints.md).

Duration values are single-pass suggestions for the API `duration` parameter;
ratio defaults to 9:16 everywhere and is omitted from recipes.

---

## Emotion / reaction

Category path: single-pass R2V. One identity `reference_image` (wardrobe
included unless separately supplied). Intensity is carried by observable
physical cues, never degree adjectives; compose with `seedance-acting-console`
for deeper cue work. Camera is mostly locked front framing; audio is native.

### Angry Mode <!-- id: angry-mode -->
- Category: Emotion / reaction
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject sits relaxed on a curb, neutral face, slow breath; @4s
  jaw tenses, fists clench, brows drop; @6s mouth opens wide in a full scream
  toward the camera, shoulders rising; hold the scream two seconds
- Camera block: front-facing eye-level medium close-up, locked-off
- Audio: native — street ambience, sharp breath intake, then a scream
- Duration: 10
- Flags: cue graduation only; scream sound requires native audio generation
- Persuasion hint: frustration-to-release hook; angle/CTA owned by ugc-ad-modes

### Crying <!-- id: crying -->
- Category: Emotion / reaction
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject stands near carnival lights in somber stillness, blink
  rate rising; @4s chin trembles, eyes glisten; @6s tears track down the
  cheeks, lips press, one shoulder hitch
- Camera block: medium close-up with a slow push-in across the beat
- Audio: native — distant carnival ambience, quiet sniff
- Duration: 10
- Flags: expression change is the whole event; keep background lights soft
- Persuasion hint: emotional-scene hook for story ads; angle/CTA owned by ugc-ad-modes

### Happy <!-- id: happy -->
- Category: Emotion / reaction
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject adjusts hair with one hand @2s, breaks into a wide
  smile, shifts weight to one hip @4s, gives a small laugh
- Camera block: medium front framing, locked-off
- Audio: native — street ambience, soft laugh
- Duration: 10
- Flags: none
- Persuasion hint: positive reveal opener; angle/CTA owned by ugc-ad-modes

### Happy Mode <!-- id: happy-mode -->
- Category: Emotion / reaction
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject leans on a car seat smiling at the camera, tilts head
  @3s, adjusts an accessory @5s, keeps smiling
- Camera block: interior-car medium close-up from the seat opposite
- Audio: native — interior car ambience
- Duration: 10
- Flags: none
- Persuasion hint: lifestyle-positive opener; angle/CTA owned by ugc-ad-modes

### Shocked <!-- id: shocked -->
- Category: Emotion / reaction
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject looks at something off-camera; @2s eyes widen, brows
  shoot up; @3s both hands rise to cover the mouth, leaning back slightly
- Camera block: medium front framing, locked-off
- Audio: native — sharp audible gasp
- Duration: 8
- Flags: the off-camera trigger stays unseen
- Persuasion hint: curiosity-gap opener; angle/CTA owned by ugc-ad-modes

### Saint Glow <!-- id: saint-glow -->
- Category: Emotion / reaction
- Grammar: single-pass R2V (fresh generation); structured edit for footage
- References: 1 identity reference_image
- Motion block: subject sits in a car; @3s a halo of light forms above the
  head and intensifies; @6s the eyes begin emitting bright light, face tilting
  up slightly
- Camera block: medium close-up through the windshield, locked-off
- Audio: native — rising shimmer tone under quiet ambience
- Duration: 10
- Flags: supernatural effect generated with the scene; keep the identity
  reference dominant in the face; disclosure reminder for ad delivery
- Persuasion hint: pattern-interrupt glow hook; angle/CTA owned by ugc-ad-modes

### Sunglasses <!-- id: sunglasses -->
- Category: Emotion / reaction
- Grammar: single-pass R2V
- References: 1 identity reference_image plus the sunglasses as a wardrobe
  reference when design matters
- Motion block: subject lifts the sunglasses with one hand @2s, slides them on
  slowly between @3s and @5s, ends with a small satisfied nod
- Camera block: close-up front framing, locked-off
- Audio: native — indoor ambience, soft contact sound
- Duration: 8
- Flags: accessory identity must match the reference
- Persuasion hint: product-on-face reveal; angle/CTA owned by ugc-ad-modes

---

## Selfie / posing

Category path: single-pass R2V with identity framing as a front-camera or
mirror selfie. Describe phone-UI screens positively or omit them — never
expect a rendered UI; see execution-constraints for the PiP guard. Locked
demos use `camera_fixed: true` in the API call.

### Selfie <!-- id: selfie -->
- Category: Selfie / posing
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: arm's-length front-camera framing; subject adjusts hair @2s,
  breaks into a natural smile @4s, glances between the lens and off-frame
- Camera block: selfie framing with slight natural handheld sway
- Audio: native — outdoor ambience
- Duration: 8
- Flags: no phone UI in frame beyond a positive description
- Persuasion hint: personal direct-address opener; angle/CTA owned by ugc-ad-modes

### Selfie Outfit <!-- id: selfie-outfit -->
- Category: Selfie / posing
- Grammar: single-pass R2V
- References: 1 identity reference_image; wardrobe reference for the outfit
- Motion block: front-camera framing on a shop-lined street; subject adjusts
  the top hem @2s, straightens, smiles at the lens @4s, shifts pose
- Camera block: selfie framing, slight sway
- Audio: native — street ambience
- Duration: 8
- Flags: outfit identity must match the wardrobe reference
- Persuasion hint: outfit-check opener; angle/CTA owned by ugc-ad-modes

### Selfie Posing <!-- id: selfie-posing -->
- Category: Selfie / posing
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: mirror-reflection framing in a cozy living room; subject
  raises the phone to the mirror, adjusts hair @3s, tilts a hip, holds the
  pose with a soft smile
- Camera block: mirror reflection, phone visible in frame, locked-off
- Audio: native — quiet room tone
- Duration: 8
- Flags: mirror image composed positively; no fake phone UI rendered
- Persuasion hint: casual lifestyle opener; angle/CTA owned by ugc-ad-modes

### Static Posing <!-- id: static-posing -->
- Category: Selfie / posing
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject poses in a library aisle, gently tilts the head @3s,
  changes hand placement @6s, returns to the first pose
- Camera block: medium, locked-off
- Audio: native — quiet interior
- Duration: 10
- Flags: set `camera_fixed: true`
- Persuasion hint: composed-fashion beat; angle/CTA owned by ugc-ad-modes

### Fix and pose <!-- id: fix-and-pose -->
- Category: Selfie / posing
- Grammar: single-pass R2V
- References: 1 identity reference_image; the cup as a prop reference if
  branded
- Motion block: subject adjusts a sleeve @2s, raises the coffee cup @4s,
  holds the pose with a small smile
- Camera block: medium with a slight low angle, locked-off
- Audio: native — outdoor parking-area ambience
- Duration: 10
- Flags: branded cup text goes to finishing, never baked
- Persuasion hint: casual product-in-hand opener; angle/CTA owned by ugc-ad-modes

### Group Photo <!-- id: group-photo -->
- Category: Selfie / posing
- Grammar: single-pass R2V (generation-only)
- References: 1 identity reference_image
- Motion block: subject sits alone; @4s an identical second figure appears
  beside them in the same outfit and pose, then two more @6s — four total,
  arranging into a loose group
- Camera block: wide, locked-off
- Audio: native — street ambience
- Duration: 10
- Flags: duplicates are forbidden in edit tasks, so this is generation-only —
  describe the multiplication as a staged appearance; identity-drift QA
  required across all figures; a real group with distinct references is the
  reliable alternative
- Persuasion hint: surreal multiply gag; angle/CTA owned by ugc-ad-modes

---

## Outfit / fashion

Category path: outfit check and sand cut are single-pass R2V showcases; outfit
switch and hair style prefer a structured edit on supplied footage (Timeline
Inheritance) with a timestamped wardrobe-change fallback for fresh generation;
clothes rain is generated falling-object spectacle. Edit tasks lock duration
(~±0.3s) and ratio.

### Outfit Check <!-- id: outfit-check -->
- Category: Outfit / fashion
- Grammar: single-pass R2V
- References: 1 identity reference_image; handbag or featured garment as a
  product reference
- Motion block: subject walks toward the camera, stops, turns to show the
  profile @4s, lifts the handbag into frame @6s, holds
- Camera block: full-body medium-wide with a slight low angle
- Audio: native — street ambience, footsteps
- Duration: 10
- Flags: featured item identity must match its reference
- Persuasion hint: walk-and-pose showcase; angle/CTA owned by ugc-ad-modes

### Outfit Switch <!-- id: outfit-switch -->
- Category: Outfit / fashion
- Grammar: structured edit on supplied footage (Timeline Inheritance); fresh
  generation alternative with timestamped wardrobe changes
- References: footage variant — the source video plus 1–2 look references,
  source under 20s; fresh variant — 1 identity reference_image plus 2–3
  wardrobe references
- Motion block: subject smiles at the camera; @3s the outfit
  changes to look B; @6s to look C; pose continuous throughout (fresh-variant
  direction; edit tasks inherit the source timeline instead)
- Camera block: medium front framing, locked-off
- Audio: native — room or street ambience; optional beat-aligned swishes as a
  finishing layer
- Duration: 10 (edit tasks lock to source duration ~±0.3s)
- Flags: identity continuity QA between looks; edit tasks derive ratio from
  the source; never mix first/last-frame roles into an R2V bundle
- Persuasion hint: variety/haul beat; angle/CTA owned by ugc-ad-modes

### Clothes Rain <!-- id: clothes-rain -->
- Category: Outfit / fashion
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject sits against a wall; coats fall from above from @2s
  onward, drifting down at moderate speed and layering on the shoulders and
  lap; subject brushes one aside @7s
- Camera block: medium-wide, locked-off
- Audio: native — soft fabric thuds
- Duration: 10
- Flags: falling garments use direction/speed/easing wording; keep the face
  unoccluded
- Persuasion hint: wardrobe-reveal spectacle; angle/CTA owned by ugc-ad-modes

### Hair Style <!-- id: hair-style -->
- Category: Outfit / fashion
- Grammar: single-pass R2V; structured edit when restyling existing footage
- References: 1 identity reference_image
- Motion block: subject slowly turns the head left and right showing the
  hairstyle @3s, runs fingers through the hair @5s, holds a posed finish
- Camera block: medium close-up with soft beauty light
- Audio: native — quiet studio tone
- Duration: 10
- Flags: hair color, length, and texture must match the identity reference;
  edit tasks lock duration and ratio
- Persuasion hint: beauty-detail beat; angle/CTA owned by ugc-ad-modes

### Sand Cut <!-- id: sand-cut -->
- Category: Outfit / fashion
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject walks through a cracked salt flat at sunset, scarf
  flowing in the wind, stops and faces the horizon @5s
- Camera block: wide with a slow lateral move
- Audio: native — wind over open terrain
- Duration: 10
- Flags: environment is the point; describe the wind's effect on fabric
  explicitly
- Persuasion hint: editorial environment beat; angle/CTA owned by ugc-ad-modes

---

## Eating / product

Category path: single-pass R2V with the food or product bound as a reference
(prop sheet owns shape and materials). Stage each beat with an observable end
state. Label and packaging text is a finishing layer, never baked.

### Eating <!-- id: eating -->
- Category: Eating / product
- Grammar: single-pass R2V
- References: 1 identity reference_image; the dish as a product reference
- Motion block: subject lifts noodles with chopsticks @2s, blows once, eats
  @4s, chews, nods approval @7s
- Camera block: medium across the table
- Audio: native — slurp, restaurant ambience
- Duration: 10
- Flags: dish identity matches its reference
- Persuasion hint: appetite beat; angle/CTA owned by ugc-ad-modes

### Eating Zoom <!-- id: eating-zoom -->
- Category: Eating / product
- Grammar: single-pass R2V
- References: 1 identity reference_image; the bowl as a product reference
- Motion block: subject lifts noodles and eats; the bite lands between @3s
  and @6s
- Camera block: slow dolly in from a medium to a close-up, timed to the bite
- Audio: native — slurp, bowl clink
- Duration: 8
- Flags: one primary move; keep stack at 1
- Persuasion hint: sensory close-up hook; angle/CTA owned by ugc-ad-modes

### Plate Check <!-- id: plate-check -->
- Category: Eating / product
- Grammar: single-pass R2V
- References: 1 identity reference_image; sandwich and fries as product
  references
- Motion block: subject picks up the sandwich @2s, checks it, takes a bite
  @4s, sets it down, gives a thumbs-up @7s
- Camera block: medium front framing
- Audio: native — casual restaurant ambience, crunch
- Duration: 10
- Flags: branded packaging text goes to finishing, never baked
- Persuasion hint: approval-of-product beat; angle/CTA owned by ugc-ad-modes

---

## VFX spectacle

Category path: a static posed subject plus an environment event described with
motion grammar (direction, speed, amplitude, easing). The event stays behind or
around the subject — never harming them unless the request intends it. Fresh
generation from references, or a structured edit over supplied footage with
`omni_reference_task_type=edit` and the edit-goal grammar. Avoid high-burst
debris; keep the identity reference dominant in the face.

### Atomic <!-- id: atomic -->
- Category: VFX spectacle
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject holds a raised-phone selfie pose, arm steady; @3s a
  slight head turn glances at the sky; @5s return to camera with an
  open-mouth reaction; a mushroom cloud rises behind at slow easing and grows
  over the remaining duration; no debris reaches the subject
- Camera block: front camera at eye level, locked-off
- Audio: native — low distant rumble swell, wind
- Duration: 10
- Flags: environment event behind a static subject; avoid high-burst debris;
  disclosure reminder for ad delivery
- Persuasion hint: pattern-interrupt hook; angle/CTA owned by ugc-ad-modes

### Explosion <!-- id: explosion -->
- Category: VFX spectacle
- Grammar: single-pass R2V; structured edit over footage for real plates
- References: 1 identity reference_image
- Motion block: subject crosses a crosswalk calmly; @2s an explosion erupts
  behind, a fireball rising and spreading down the street; @6s the subject
  glances back once and keeps walking
- Camera block: wide, locked-off
- Audio: native — deep blast rumble, ringing decay
- Duration: 10
- Flags: fire stays behind the subject; no debris contact
- Persuasion hint: pattern-interrupt hook; angle/CTA owned by ugc-ad-modes

### Firework <!-- id: firework -->
- Category: VFX spectacle
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject stands still in a crowded street; fireworks burst in
  the sky from @3s in multiple colors; subject looks up @5s
- Camera block: medium with a slight tilt up
- Audio: native — distant booms, crowd murmur
- Duration: 10
- Flags: bursts stay in the sky, away from the subject
- Persuasion hint: celebration beat; angle/CTA owned by ugc-ad-modes

### Northern Lights <!-- id: northern-lights -->
- Category: VFX spectacle
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject walks across snowy terrain; aurora curtains shift
  overhead continuously with slow, waving motion; subject stops and looks up
  @6s
- Camera block: wide with a slow follow
- Audio: native — wind, quiet ambience
- Duration: 15
- Flags: aurora motion described as slow waving bands, not flicker
- Persuasion hint: awe beat; angle/CTA owned by ugc-ad-modes

### Aquarium <!-- id: aquarium -->
- Category: VFX spectacle
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject squats taking a mirror selfie; @3s water begins
  rising indoors; @6s the subject is submerged to the shoulders, still
  holding the pose, hair drifting
- Camera block: mirror-reflection framing, locked-off
- Audio: native — water rush settling into muffled quiet
- Duration: 10
- Flags: surreal transition; keep the face readable through the water;
  describe buoyancy and hair drift explicitly
- Persuasion hint: surreal reveal hook; angle/CTA owned by ugc-ad-modes

### Color Rain <!-- id: color-rain -->
- Category: VFX spectacle
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject stands holding a phone; @2s red liquid pours from
  above in a thick viscous stream, progressively covering the head and
  shoulders by @8s; subject stays still with a small smile
- Camera block: medium, locked-off
- Audio: native — liquid pour and splatter
- Duration: 10
- Flags: liquid motion described as viscous; keep the eyes clear
- Persuasion hint: ASMR-adjacent spectacle; angle/CTA owned by ugc-ad-modes

### Money Rain <!-- id: money-rain -->
- Category: VFX spectacle
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject stands in night light; @3s stylized banknotes begin
  drifting down around them; subject looks up @5s and reaches to catch one
  @7s
- Camera block: medium with an available low angle
- Audio: native — paper flutter, night street tone
- Duration: 10
- Flags: currency renders stylized and generic — never counterfeitable
  detail; the official demo includes smoking; this recipe keeps the subject
  action neutral
- Persuasion hint: payoff spectacle; angle/CTA owned by ugc-ad-modes

### Pizza Fall <!-- id: pizza-fall -->
- Category: VFX spectacle
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject sits in stadium seats; @3s an oversized pepperoni
  pizza descends from above, covering them by @8s and dripping
- Camera block: medium-wide, locked-off
- Audio: native — soft impact and drip
- Duration: 10
- Flags: comedic scale; keep the face peeking out
- Persuasion hint: absurd humor hook; angle/CTA owned by ugc-ad-modes

### Cotton Cloud <!-- id: cotton-cloud -->
- Category: VFX spectacle
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject stands beside a motorcycle in a parking garage; @2s
  pink smoke drifts in low and thickens to waist height by @6s; subject waves
  a hand through it @8s
- Camera block: medium, locked-off
- Audio: native — soft whoosh, garage reverb
- Duration: 10
- Flags: smoke direction, speed, and density stated explicitly
- Persuasion hint: color-wash reveal; angle/CTA owned by ugc-ad-modes

### Gas Transformation <!-- id: gas-transformation -->
- Category: VFX spectacle
- Grammar: single-pass R2V with a staged vanish end state; object-morph
  transition grammar as the alternative
- References: 1 identity reference_image
- Motion block: subject stands in an elevator holding a phone; @3s the edges
  of the coat begin dissolving into drifting smoke; the dissolution spreads
  across the body by @6s; by @9s only smoke remains and the phone drops out
  of view
- Camera block: elevator interior framing, locked-off
- Audio: native — hiss of dispersing gas, elevator hum
- Duration: 10
- Flags: no direct disintegration mode exists — the vanish is written as an
  explicit staged end state or an object-morph transition; QA the final
  frame reads as intended
- Persuasion hint: vanishing cliffhanger; angle/CTA owned by ugc-ad-modes

### Beast Appearance <!-- id: beast-appearance -->
- Category: VFX spectacle
- Grammar: single-pass R2V; structured edit for creature-over-footage
- References: 1 identity reference_image; the creature as a reference when
  species identity matters
- Motion block: subject walks down a street sipping a drink; @4s a large
  panda materializes beside them, matching their pace; subject stops and
  stares @6s; the panda looks back
- Camera block: tracking that settles into a static two-shot
- Audio: native — street tone, low animal rumble
- Duration: 10
- Flags: creature realism cues — fur texture and weight-shift walk; keep
  creature identity consistent across the shot
- Persuasion hint: surreal-encounter hook; angle/CTA owned by ugc-ad-modes

### Giant Grab <!-- id: giant-grab -->
- Category: VFX spectacle
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject stands casually; @4s an enormous hand reaches into
  frame from above; the fingers close loosely around the subject @6s and lift
  them slightly; the subject waves
- Camera block: wide, locked-off
- Audio: native — deep whoosh, low rumble on the grab
- Duration: 10
- Flags: scale contrast is the effect; the official demo shows a different
  gag (a dog runs off, peace sign) — this recipe targets the name's intent
- Persuasion hint: impossible-scale hook; angle/CTA owned by ugc-ad-modes

---

## Action / movement

Category path: single-pass R2V with named camera techniques and the
spatial-continuity contract — start point, travel axis, boundary, end state.
Vehicles are visible-identity references. Safety-relevant gear (helmets) is
always worn visibly. Respect the high-burst caution on jumps.

### Handheld Run <!-- id: handheld-run -->
- Category: Action / movement
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject runs along a sunny trail toward the camera, spins once
  with arms out @5s, resumes running
- Camera block: handheld follow with slight shake
- Audio: native — footsteps, breathing, birds
- Duration: 10
- Flags: spatial continuity — trail direction and the turnaround point named
- Persuasion hint: energy opener; angle/CTA owned by ugc-ad-modes

### Pool Jump <!-- id: pool-jump -->
- Category: Action / movement
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject takes a selfie at the pool edge @2s, lowers the phone
  out of frame @4s, jumps into the pool @5s with a splash, surfaces smiling
  @8s
- Camera block: static wide from the deck
- Audio: native — splash, laughter
- Duration: 10
- Flags: high-burst caution — splash size and timing described explicitly;
  the phone's exit from frame must be stated to keep the prop safe
- Persuasion hint: joy payoff; angle/CTA owned by ugc-ad-modes

### Ballet <!-- id: ballet -->
- Category: Action / movement
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject performs a ballet sequence — port de bras into a
  pirouette, hair sweeping with the turn, finishing in a held pose
- Camera block: medium with a slow orbit or locked-off
- Audio: native — quiet room, footsteps of the turn
- Duration: 10
- Flags: dance written as concrete vocabulary (arm positions, turns,
  footwork), never "dances beautifully"
- Persuasion hint: craft-skill beat; angle/CTA owned by ugc-ad-modes

### Motor Ride <!-- id: motor-ride -->
- Category: Action / movement
- Grammar: single-pass R2V
- References: 1 identity reference_image; the motorcycle as a vehicle
  reference
- Motion block: subject rides through a city street, then an open coastal
  road, leaning into one named turn
- Camera block: tracking from the side, then behind
- Audio: native — engine, wind at speed
- Duration: 15
- Flags: helmet visibly worn throughout; travel axis named
- Persuasion hint: freedom-of-road beat; angle/CTA owned by ugc-ad-modes

### Beach Ride <!-- id: beach-ride -->
- Category: Action / movement
- Grammar: one-click video with ordered images, or three chained scenes
- References: 1 identity reference_image; the taxi as a vehicle reference;
  one establishing image per scene on the one-click path
- Motion block: scene 1 — the taxi rolls past a desert motel; scene 2 — the
  taxi speeds along a coastal road; scene 3 — the subject walks alone on a
  beach
- Camera block: varies per scene — tracking, then speed framing, then a slow
  beach wide
- Audio: native — engine, then surf
- Duration: 20 (chain via return_last_frame/first_frame if scenes exceed 30s
  combined)
- Flags: one-click requires explicit image order and subject mapping;
  chained scenes need matched aspect ratios
- Persuasion hint: journey arc; angle/CTA owned by ugc-ad-modes

### Train Rush <!-- id: train-rush -->
- Category: Action / movement
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject stands with arms crossed, still; a subway train blasts
  past behind from @2s to @7s, creating wind and motion blur; hair and coat
  react; the subject stays unmoved
- Camera block: medium, locked-off or a slight push
- Audio: native — train roar, wind burst
- Duration: 10
- Flags: train speed and direction stated; subject is the static anchor
- Persuasion hint: composure-vs-chaos beat; angle/CTA owned by ugc-ad-modes

### Peak Moment <!-- id: peak-moment -->
- Category: Action / movement
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject climbs the last snow ridge, plants their stance, and
  raises both arms outstretched @6s, holding the summit pose
- Camera block: wide, then a slow push for the summit beat
- Audio: native — wind, exerted breathing
- Duration: 15
- Flags: end state held for visibility; no summit text overlays baked
- Persuasion hint: achievement payoff; angle/CTA owned by ugc-ad-modes

---

## Lifestyle / timelapse

Category path: `[Stage N]` timestamped staging with consecutive,
non-overlapping timestamps. No timelapse speed parameter exists — compression
is approximated by staged bursts of activity. Anything beyond 30s chains via
`return_last_frame` → `first_frame` with matched aspect ratios.

### Morning routine <!-- id: morning-routine -->
- Category: Lifestyle / timelapse
- Grammar: single-pass staged arc, or chained scenes when compressed past
  30s is unacceptable
- References: 1 identity reference_image; wardrobe references per stage
- Motion block: [Stage 1] subject wakes and stretches @0s–6s; [Stage 2]
  close-up of a hand lifting a polka-dot mug @6s–12s; [Stage 3] subject in a
  trench coat takes mirror selfies @12s–20s
- Camera block: varies per stage — bed medium, mug close-up, mirror framing
- Audio: native — morning room tone, mug clink
- Duration: 20 (chain three ~10s scenes via return_last_frame/first_frame
  for a fuller arc)
- Flags: wardrobe continuity across stages; chained scenes need matched
  ratios
- Persuasion hint: day-in-the-life opener; angle/CTA owned by ugc-ad-modes

### Timelapse Glam <!-- id: timelapse-glam -->
- Category: Lifestyle / timelapse
- Grammar: single-pass staged arc
- References: 1 identity reference_image
- Motion block: [Stage 1] two stylists adjust the subject's hair and jacket
  @0s–5s; [Stage 2] a third stylist adds an accessory in quick bursts @5s–10s;
  the subject holds a pose throughout
- Camera block: static medium-wide, locked-off
- Audio: native — street tone, brushing and rustling
- Duration: 10
- Flags: the stylists' busy motion is the timelapse effect; the subject stays
  the anchor
- Persuasion hint: transformation montage; angle/CTA owned by ugc-ad-modes

### Timelapse Human <!-- id: timelapse-human -->
- Category: Lifestyle / timelapse
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: the subject stands perfectly still center-frame; pedestrians
  cross continuously as fast, motion-blurred streaks through the whole clip;
  ambient light shifts subtly
- Camera block: locked-off wide, `camera_fixed: true`
- Audio: native — city night crowd swell
- Duration: 10
- Flags: crowd-freeze is approximated — the static subject is stated
  explicitly while background pedestrians move constantly at fast frequency
  with blur; QA that the subject truly holds
- Persuasion hint: stillness-amid-chaos beat; angle/CTA owned by ugc-ad-modes

---

## Multi-shot story

Category path: three supported paths — a ≤30s one-take; per-scene generation
chained via `return_last_frame` → `first_frame`; or one-click video with
explicit image order and character mapping. Keyframe chains require first and
last images sharing an aspect ratio.

### Yacht <!-- id: yacht -->
- Category: Multi-shot story
- Grammar: one-click video with ordered images, or chained scenes
- References: 1 identity reference_image; one establishing image per scene on
  the one-click path
- Motion block: scene 1 — the subject raises a champagne glass to the camera;
  scene 2 — walks toward a group on deck; scene 3 — the yacht cruises open
  water
- Camera block: toast in a medium, then a follow, then an aerial wide
- Audio: native — glasses, deck ambience, then wind and sea
- Duration: 20
- Flags: one-click requires explicit image order and subject mapping;
  chained scenes need matched ratios
- Persuasion hint: aspirational arc; angle/CTA owned by ugc-ad-modes

### BTS <!-- id: bts -->
- Category: Multi-shot story
- Grammar: one-click video (montage-native) or single-pass staged arc under
  30s
- References: 1 identity reference_image
- Motion block: the subject sits on a bench with a sandwich, relaxed; crew
  members cross the frame adjusting lights and a camera dolly around an
  orange backdrop; one claps a slate @7s
- Camera block: static wide, locked-off
- Audio: native — set chatter, equipment moves, slate clap
- Duration: 15
- Flags: any backdrop text belongs to the finishing layer, never baked into
  generation; crew motion stays busy but non-occluding
- Persuasion hint: behind-the-scenes credibility beat; angle/CTA owned by
  ugc-ad-modes
