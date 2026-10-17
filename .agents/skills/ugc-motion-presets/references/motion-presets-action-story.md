# Motion Presets — action and story

Action / movement, Lifestyle / timelapse and Multi-shot story recipes. Shared
rules (reading scope, duration, ratio, persuasion hints) are in
[motion-presets.md](motion-presets.md); cross-cut constraints live in
[execution-constraints.md](execution-constraints.md).

## Action / movement

Category path: single-pass R2V with named camera techniques and the
spatial-continuity contract — start point, travel axis, boundary, end state.
Vehicles are visible-identity references. Safety-relevant gear (helmets) is
always worn visibly. Respect the high-burst caution on jumps.

### Handheld Run <!-- id: handheld-run -->
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject runs along a sunny trail toward the camera, spins once
  with arms out @5s, resumes running
- Camera block: handheld follow with slight shake
- Audio: native — footsteps, breathing, birds
- Duration: 10
- Flags: spatial continuity — trail direction and the turnaround point named
- Persuasion hint: energy opener

### Pool Jump <!-- id: pool-jump -->
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
- Persuasion hint: joy payoff

### Ballet <!-- id: ballet -->
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject performs a ballet sequence — port de bras into a
  pirouette, hair sweeping with the turn, finishing in a held pose
- Camera block: medium with a slow orbit or locked-off
- Audio: native — quiet room, footsteps of the turn
- Duration: 10
- Flags: dance written as concrete vocabulary (arm positions, turns,
  footwork), never "dances beautifully"
- Persuasion hint: craft-skill beat

### Motor Ride <!-- id: motor-ride -->
- Grammar: single-pass R2V
- References: 1 identity reference_image; the motorcycle as a vehicle
  reference
- Motion block: subject rides through a city street, then an open coastal
  road, leaning into one named turn
- Camera block: tracking from the side, then behind
- Audio: native — engine, wind at speed
- Duration: 15
- Flags: helmet visibly worn throughout; travel axis named
- Persuasion hint: freedom-of-road beat

### Beach Ride <!-- id: beach-ride -->
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
- Persuasion hint: journey arc

### Train Rush <!-- id: train-rush -->
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject stands with arms crossed, still; a subway train blasts
  past behind from @2s to @7s, creating wind and motion blur; hair and coat
  react; the subject stays unmoved
- Camera block: medium, locked-off or a slight push
- Audio: native — train roar, wind burst
- Duration: 10
- Flags: train speed and direction stated; subject is the static anchor
- Persuasion hint: composure-vs-chaos beat

### Peak Moment <!-- id: peak-moment -->
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject climbs the last snow ridge, plants their stance, and
  raises both arms outstretched @6s, holding the summit pose
- Camera block: wide, then a slow push for the summit beat
- Audio: native — wind, exerted breathing
- Duration: 15
- Flags: end state held for visibility; no summit text overlays baked
- Persuasion hint: achievement payoff

---

## Lifestyle / timelapse

Category path: `[Stage N]` timestamped staging with consecutive,
non-overlapping timestamps. No timelapse speed parameter exists — compression
is approximated by staged bursts of activity. Anything beyond 30s chains via
`return_last_frame` → `first_frame` with matched aspect ratios.

### Morning routine <!-- id: morning-routine -->
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
- Persuasion hint: day-in-the-life opener

### Timelapse Glam <!-- id: timelapse-glam -->
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
- Persuasion hint: transformation montage

### Timelapse Human <!-- id: timelapse-human -->
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: the subject stands perfectly still center-frame; pedestrians
  cross continuously as fast, motion-blurred streaks through the whole clip;
  ambient light shifts subtly
- Camera block: locked-off wide, stated in the prompt
- Audio: native — city night crowd swell
- Duration: 10
- Flags: crowd-freeze is approximated — the static subject is stated
  explicitly while background pedestrians move constantly at fast frequency
  with blur; QA that the subject truly holds
- Persuasion hint: stillness-amid-chaos beat

---

## Multi-shot story

Category path: three supported paths — a ≤30s one-take; per-scene generation
chained via `return_last_frame` → `first_frame`; or one-click video with
explicit image order and character mapping. Keyframe chains require first and
last images sharing an aspect ratio.

### Yacht <!-- id: yacht -->
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
- Persuasion hint: aspirational arc

### BTS <!-- id: bts -->
- Grammar: one-click video (montage-native) or single-pass staged arc under
  30s
- References: 1 identity reference_image
- Motion block: the subject sits on a bench with a sandwich, relaxed; crew
  members cross the frame adjusting lights and a camera dolly around an
  orange backdrop; one claps a plain black slate with nothing written on it
  @7s
- Camera block: static wide, locked-off
- Audio: native — set chatter, equipment moves, slate clap
- Duration: 15
- Flags: slates, cases and gear invent lettering, so describe them plain; any
  backdrop text belongs to the finishing layer; crew motion stays busy but
  non-occluding
- Persuasion hint: behind-the-scenes credibility beat
