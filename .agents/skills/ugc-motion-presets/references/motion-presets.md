# Motion Presets — people and product

45 recipes, each an original Seedance 2.5 direction composed for this
workspace, split across three files by category. Recipes are creative
heuristics — no preset is ranked over another by any measured claim.

**Read only the category section containing the resolved preset.** Each recipe
fills the six-part formula slots per the skill's composition rules; cross-cut
constraints live in [execution-constraints.md](execution-constraints.md).
Duration values are single-pass suggestions for the API `duration` parameter;
ratio defaults to 9:16 everywhere and is omitted from recipes. A persuasion hint
is a one-line hook idea; angle, claims and CTA stay with `ugc-ad-modes`.

This file: Emotion / reaction, Selfie / posing, Outfit / fashion, Eating /
product. VFX spectacle is in [motion-presets-spectacle.md](motion-presets-spectacle.md);
action, lifestyle and multi-shot recipes are in
[motion-presets-action-story.md](motion-presets-action-story.md).

---

## Emotion / reaction

Category path: single-pass R2V. One identity `reference_image` (wardrobe
included unless separately supplied). Intensity is carried by observable
physical cues, never degree adjectives; compose with `seedance-acting-console`
for deeper cue work. Camera is mostly locked front framing; audio is native.

### Angry Mode <!-- id: angry-mode -->
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject sits relaxed on a curb, neutral face, slow breath; @4s
  jaw tenses, fists clench, brows drop; @6s mouth opens wide in a full scream
  toward the camera, shoulders rising; hold the scream two seconds
- Camera block: front-facing eye-level medium close-up, locked-off
- Audio: native — street ambience, sharp breath intake, then a scream
- Duration: 10
- Flags: cue graduation only; scream sound requires native audio generation
- Persuasion hint: frustration-to-release hook

### Crying <!-- id: crying -->
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject stands near carnival lights in somber stillness, blink
  rate rising; @4s chin trembles, eyes glisten; @6s tears track down the
  cheeks, lips press, one shoulder hitch
- Camera block: medium close-up with a slow push-in across the beat
- Audio: native — distant carnival ambience, quiet sniff
- Duration: 10
- Flags: expression change is the whole event; keep background lights soft
- Persuasion hint: emotional-scene hook for story ads

### Happy <!-- id: happy -->
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject adjusts hair with one hand @2s, breaks into a wide
  smile, shifts weight to one hip @4s, gives a small laugh
- Camera block: medium front framing, locked-off
- Audio: native — street ambience, soft laugh
- Duration: 10
- Flags: none
- Persuasion hint: positive reveal opener

### Happy Mode <!-- id: happy-mode -->
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject leans on a car seat smiling at the camera, tilts head
  @3s, adjusts an accessory @5s, keeps smiling
- Camera block: interior-car medium close-up from the seat opposite
- Audio: native — interior car ambience
- Duration: 10
- Flags: none
- Persuasion hint: lifestyle-positive opener

### Shocked <!-- id: shocked -->
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject looks at something off-camera; @2s eyes widen, brows
  shoot up; @3s both hands rise to cover the mouth, leaning back slightly
- Camera block: medium front framing, locked-off
- Audio: native — sharp audible gasp
- Duration: 8
- Flags: the off-camera trigger stays unseen
- Persuasion hint: curiosity-gap opener

### Saint Glow <!-- id: saint-glow -->
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
- Persuasion hint: pattern-interrupt glow hook

### Sunglasses <!-- id: sunglasses -->
- Grammar: single-pass R2V
- References: 1 identity reference_image plus the sunglasses as a wardrobe
  reference when design matters
- Motion block: subject lifts the sunglasses in the right hand (frame-left)
  @2s, slides them on slowly between @3s and @5s, ends with a small satisfied
  nod
- Camera block: close-up front framing, locked-off
- Audio: native — indoor ambience, soft contact sound
- Duration: 8
- Flags: accessory identity must match the reference
- Persuasion hint: product-on-face reveal

---

## Selfie / posing

Category path: single-pass R2V with identity framing as a front-camera or
mirror selfie. Describe phone-UI screens positively or omit them — never
expect a rendered UI; see execution-constraints for the PiP guard. Name the
phone hand by anatomy plus frame side ("her right hand, frame-left"). Locked
demos state the locked camera in the prompt and record `format_static_by_design`.

### Selfie <!-- id: selfie -->
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: arm's-length front-camera framing; subject adjusts hair @2s,
  breaks into a natural smile @4s, glances between the lens and off-frame
- Camera block: selfie framing with slight natural handheld sway
- Audio: native — outdoor ambience
- Duration: 8
- Flags: no phone UI in frame beyond a positive description
- Persuasion hint: personal direct-address opener

### Selfie Outfit <!-- id: selfie-outfit -->
- Grammar: single-pass R2V
- References: 1 identity reference_image; wardrobe reference for the outfit
- Motion block: front-camera framing on a shop-lined street; subject adjusts
  the top hem @2s, straightens, smiles at the lens @4s, shifts pose
- Camera block: selfie framing, slight sway
- Audio: native — street ambience
- Duration: 8
- Flags: outfit identity must match the wardrobe reference
- Persuasion hint: outfit-check opener

### Selfie Posing <!-- id: selfie-posing -->
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: mirror-reflection framing in a cozy living room; subject
  raises the phone to the mirror, adjusts hair @3s, tilts a hip, holds the
  pose with a soft smile
- Camera block: mirror reflection, phone visible in frame, locked-off
- Audio: native — quiet room tone
- Duration: 8
- Flags: mirror image composed positively; no fake phone UI rendered
- Persuasion hint: casual lifestyle opener

### Static Posing <!-- id: static-posing -->
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject poses in a library aisle, gently tilts the head @3s,
  changes hand placement @6s, returns to the first pose
- Camera block: medium, locked-off
- Audio: native — quiet interior
- Duration: 10
- Flags: state the locked camera in the prompt
- Persuasion hint: composed-fashion beat

### Fix and pose <!-- id: fix-and-pose -->
- Grammar: single-pass R2V
- References: 1 identity reference_image; the cup as a prop reference if
  branded
- Motion block: subject adjusts the left sleeve @2s, raises the coffee cup in
  the right hand (frame-left) @4s, holds the pose with a small smile
- Camera block: medium with a slight low angle, locked-off
- Audio: native — outdoor parking-area ambience
- Duration: 10
- Flags: a branded cup takes its prop reference and its label is inspected in
  the take; an unbranded cup is written "plain white paper cup, smooth surface,
  nothing printed" so no lettering is invented
- Persuasion hint: casual product-in-hand opener

### Group Photo <!-- id: group-photo -->
- Grammar: single-pass R2V (generation-only)
- References: 1 identity reference_image
- Motion block: subject sits alone on a bench, one figure; @4s exactly one
  identical second figure appears frame-right of them in the same outfit — two
  figures; @6s exactly two more appear, one frame-left and one standing behind
  — four figures total, positions held to the end
- Camera block: wide, locked-off
- Audio: native — street ambience
- Duration: 10
- Flags: duplicates are forbidden in edit tasks, so this is generation-only —
  describe the multiplication as a staged appearance; clone counts overshoot,
  so restate the exact count and positions at every timestamp and count on a
  full-size frame; identity-drift QA across all figures; a real group with
  distinct references is the reliable alternative
- Persuasion hint: surreal multiply gag

---

## Outfit / fashion

Category path: outfit check and sand cut are single-pass R2V showcases; outfit
switch and hair style prefer a structured edit on supplied footage (Timeline
Inheritance) with a timestamped wardrobe-change fallback for fresh generation;
clothes rain is generated falling-object spectacle. Edit tasks lock duration
(~±0.3s) and ratio, and footage that shows a person is rejected unless that
person is bound as an `asset://` asset (see execution-constraints).

### Outfit Check <!-- id: outfit-check -->
- Grammar: single-pass R2V
- References: 1 identity reference_image; handbag or featured garment as a
  product reference
- Motion block: subject walks toward the camera, stops, turns to show the
  profile @4s, lifts the handbag into frame @6s, holds
- Camera block: full-body medium-wide with a slight low angle
- Audio: native — street ambience, footsteps
- Duration: 10
- Flags: featured item identity must match its reference
- Persuasion hint: walk-and-pose showcase

### Outfit Switch <!-- id: outfit-switch -->
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
- Persuasion hint: variety/haul beat

### Clothes Rain <!-- id: clothes-rain -->
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
- Persuasion hint: wardrobe-reveal spectacle

### Hair Style <!-- id: hair-style -->
- Grammar: single-pass R2V; structured edit when restyling existing footage
- References: 1 identity reference_image
- Motion block: subject slowly turns the head left and right showing the
  hairstyle @3s, runs fingers through the hair @5s, holds a posed finish
- Camera block: medium close-up with soft beauty light
- Audio: native — quiet studio tone
- Duration: 10
- Flags: hair color, length, and texture must match the identity reference;
  edit tasks lock duration and ratio
- Persuasion hint: beauty-detail beat

### Sand Cut <!-- id: sand-cut -->
- Grammar: single-pass R2V
- References: 1 identity reference_image
- Motion block: subject walks through a cracked salt flat at sunset, scarf
  flowing in the wind, stops and faces the horizon @5s
- Camera block: wide with a slow lateral move
- Audio: native — wind over open terrain
- Duration: 10
- Flags: environment is the point; describe the wind's effect on fabric
  explicitly
- Persuasion hint: editorial environment beat

---

## Eating / product

Category path: single-pass R2V with the food or product bound as a reference
(prop sheet owns shape and materials). Stage each beat with an observable end
state. Branded packaging takes its product reference; unbranded cups, jars
and wrappers are described plain with nothing printed. Overlay text is a
finishing layer, never baked.

### Eating <!-- id: eating -->
- Grammar: single-pass R2V
- References: 1 identity reference_image; the dish as a product reference
- Motion block: subject lifts noodles with chopsticks in the right hand
  (frame-left) @2s, blows once, eats @4s, chews, nods approval @7s
- Camera block: medium across the table
- Audio: native — slurp, restaurant ambience
- Duration: 10
- Flags: dish identity matches its reference
- Persuasion hint: appetite beat

### Eating Zoom <!-- id: eating-zoom -->
- Grammar: single-pass R2V
- References: 1 identity reference_image; the bowl as a product reference
- Motion block: subject lifts noodles and eats; the bite lands between @3s
  and @6s
- Camera block: slow dolly in from a medium to a close-up, timed to the bite
- Audio: native — slurp, bowl clink
- Duration: 8
- Flags: one primary move; keep stack at 1
- Persuasion hint: sensory close-up hook

### Plate Check <!-- id: plate-check -->
- Grammar: single-pass R2V
- References: 1 identity reference_image; sandwich and fries as product
  references
- Motion block: one sandwich and one fries carton sit on the tray in open view;
  subject picks up the sandwich in both hands @2s, checks it, takes a bite @4s,
  sets it down beside the carton, gives a right-hand (frame-left) thumbs-up @7s
- Camera block: medium front framing
- Audio: native — casual restaurant ambience, crunch
- Duration: 10
- Flags: branded wrappers take their product references; unbranded ones are
  "plain kraft paper, nothing printed" so no lettering is invented
- Persuasion hint: approval-of-product beat
