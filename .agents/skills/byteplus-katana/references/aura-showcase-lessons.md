# Lessons from the Aura Showcase Comparison

Learned on 2026-10-15 by putting a first build next to Higgsfield's own Katana
showcase reel, an aura-farming hero edit that cuts between cinematic shots of
one character. The first build was judged ugly. These are examples of what a
reference of that kind needs, not defaults for other formats: a reference built
from cutouts, cards or a talking head sets its own bar through the EDL and the
motion inventory.

| Higgsfield reel | Cheap-looking build |
| --- | --- |
| A different cinematic video shot on almost every beat: overhead, close-up, low-angle walk, night | One static cutout repeated on several beats where the reference showed moving footage |
| The character fills the frame; photographic light (golden hour, sodium night, flare) | Small figure centred in empty space |
| Photographic backgrounds with grain | Flat red, yellow or white cards |
| Words on the beat in mixed fonts and colours: red condensed, heavy white sans, cream italic serif; arcs and perspective | One condensed font with thick black meme outlines everywhere |
| Restrained effects on footage: negative or thermal invert, split screen with a thin coloured divider, a circle-cut face with curved text, an inset close-up | Pill badges, concentric clip-art rings, counters |

The general lesson: the failure was routing footage segments to layers. Read
each segment (see [segment routing](segment-routing.md)) and give footage
segments footage.

## When the reference is this kind of edit

- Count the distinct setups the reel actually shows (sizes, angles, times of
  day, actions) and generate one take per setup; that reel needed about five.
- First frames from Seedream with the locked identity cutouts as references,
  at the reference aspect ratio; inspect identity on every still before
  animating.
- In that run the provider rejected `ratio` on first-frame image-to-video and
  followed the first frame's shape. Resolve it from the live capability each
  time.
- Type follows the reference: that reel used three families at most, no
  outlines, soft shadows and one word or short phrase per beat, landing on the
  cut frame. Another reference's type system is copied the same way, or
  replaced with a rights-safe equivalent in grammar-only mode.
- A meme caption uses the platform-native style (white rounded box, black
  sans, sentence case) when the reference does.

## Generated-shot lessons

Observed in a follow-up live build (2026-10-16); they apply to any
`fresh_generation` shot.

- **Physical outcomes need frame locks.** When a shot must end in a specific
  state (who wins, what lands where), lock it with a first and last frame pair
  from Seedream; a last frame alone is rejected. Read the result by the
  direction of motion and conventional signals (a raised winner's arm, a
  slumped loser), not by the end position of one hand, and zoom-check hands.
- **Name arms in camera terms.** In side views the models default to both
  near-camera arms; say which arm is nearest the camera for each person, and
  name hands by anatomy plus frame side.
- **Two identity references can add a second character.** Seedream given two
  characters' references may draw both when only one is asked for; inspect
  every still before animating.
- **Mirroring in post flips handedness.** A horizontal flip turns a right-handed
  action left-handed; regenerate instead when handedness matters.
