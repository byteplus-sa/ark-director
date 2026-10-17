# Motion Presets — VFX spectacle

Twelve VFX spectacle recipes. Shared rules (reading scope, duration, ratio,
persuasion hints) are in
[motion-presets.md](motion-presets.md); cross-cut constraints live in
[execution-constraints.md](execution-constraints.md).

## VFX spectacle

Category path: a static posed subject plus an environment event described with
motion grammar (direction, speed, amplitude, easing). The event stays behind or
around the subject — never harming them unless the request intends it. Fresh
generation from references, or a structured edit over supplied footage with
`omni_reference_task_type=edit` and the edit-goal grammar. Avoid high-burst
debris; keep the identity reference dominant in the face.

### Atomic <!-- id: atomic -->
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
- Persuasion hint: pattern-interrupt hook

### Explosion <!-- id: explosion -->
- Grammar: single-pass R2V; structured edit over footage for real plates
- References: 1 identity reference_image
- Motion block: subject crosses a crosswalk calmly; @2s an explosion erupts
  behind, a fireball rising and spreading down the street; @6s the subject
  glances back once and keeps walking
- Camera block: wide, locked-off
- Audio: native — deep blast rumble, ringing decay
- Duration: 10
- Flags: fire stays behind the subject; no debris contact
- Persuasion hint: pattern-interrupt hook

### Firework <!-- id: firework -->
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject stands still in a crowded street; fireworks burst in
  the sky from @3s in multiple colors; subject looks up @5s
- Camera block: medium with a slight tilt up
- Audio: native — distant booms, crowd murmur
- Duration: 10
- Flags: bursts stay in the sky, away from the subject
- Persuasion hint: celebration beat

### Northern Lights <!-- id: northern-lights -->
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject walks across snowy terrain; aurora curtains shift
  overhead continuously with slow, waving motion; subject stops and looks up
  @6s
- Camera block: wide with a slow follow
- Audio: native — wind, quiet ambience
- Duration: 15
- Flags: aurora motion described as slow waving bands, not flicker
- Persuasion hint: awe beat

### Aquarium <!-- id: aquarium -->
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
- Persuasion hint: surreal reveal hook

### Color Rain <!-- id: color-rain -->
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject stands holding a phone; @2s red liquid pours from
  above in a thick viscous stream, progressively covering the head and
  shoulders by @8s; subject stays still with a small smile
- Camera block: medium, locked-off
- Audio: native — liquid pour and splatter
- Duration: 10
- Flags: liquid motion described as viscous; keep the eyes clear
- Persuasion hint: ASMR-adjacent spectacle

### Money Rain <!-- id: money-rain -->
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject stands in night light; @3s stylized banknotes begin
  drifting down around them; subject looks up @5s and reaches up with the right
  hand (frame-left) to catch one @7s
- Camera block: medium with an available low angle
- Audio: native — paper flutter, night street tone
- Duration: 10
- Flags: currency renders stylized and generic — plain tinted paper with no
  readable numerals, portraits or counterfeitable detail; subject action stays
  neutral
- Persuasion hint: payoff spectacle

### Pizza Fall <!-- id: pizza-fall -->
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject sits in stadium seats; @3s an oversized pepperoni
  pizza descends from above, covering them by @8s and dripping
- Camera block: medium-wide, locked-off
- Audio: native — soft impact and drip
- Duration: 10
- Flags: comedic scale; keep the face peeking out
- Persuasion hint: absurd humor hook

### Cotton Cloud <!-- id: cotton-cloud -->
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject stands beside a motorcycle in a parking garage; @2s
  pink smoke drifts in low and thickens to waist height by @6s; subject waves
  a hand through it @8s
- Camera block: medium, locked-off
- Audio: native — soft whoosh, garage reverb
- Duration: 10
- Flags: smoke direction, speed, and density stated explicitly
- Persuasion hint: color-wash reveal

### Gas Transformation <!-- id: gas-transformation -->
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
- Persuasion hint: vanishing cliffhanger

### Beast Appearance <!-- id: beast-appearance -->
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
- Persuasion hint: surreal-encounter hook

### Giant Grab <!-- id: giant-grab -->
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject stands casually; @4s an enormous hand reaches into
  frame from above; the fingers close loosely around the subject @6s and lift
  them slightly; the subject waves
- Camera block: wide, locked-off
- Audio: native — deep whoosh, low rumble on the grab
- Duration: 10
- Flags: scale contrast is the effect; state exactly one giant hand and keep
  the subject's face clear of the fingers
- Persuasion hint: impossible-scale hook
