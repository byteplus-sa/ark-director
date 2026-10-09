# Evidence status

Recipes are written from the observed example footage of each effect (2026-10-08).
Two local runs then tested them on invented subjects: a first probe of twelve
effects, and a full run of all 45. A run shows that a recipe can produce the
effect, or fail to, on one invented subject at one resolution; it does not
guarantee the effect on other photos, other subjects, other resolutions or real
people. Neither project is committed, so the results below are the agent's own
records, not reproducible from the repo.

Probe project: `projects/effects-probe/` (one invented woman, an invented vehicle
and an invented product; 14 Seedream images, 12 Seedance drafts, native audio
off except one).

## Probed on 2026-10-08

| Effect | Result | Caveat found |
| --- | --- | --- |
| `street-colossus` | Pass: striding giant, window POV at about 4 s, low shot with hand on tower at about 7 s | Needs the Seedream giant start frame; a second helicopter drifted in at about 6 s despite 'exactly one' |
| `incline` | Pass: room rolled and levelled, three sliders moved, subject steady | Sliders must start on a named surface; list fixed objects |
| `wild-ride` | Pass: burnout, overhead sweep, low side track, one person attached | Opening view must follow the photo, not assume a rear view |
| `act-natural` | Pass: frozen subject, moving diner | Orbit angle subtle; crossing event must not add a person |
| `melting` | Pass: colour-matched drips, kneel, puddle, hat and boots left | None observed |
| `world-morphing` | Pass: street curled over, city inverted overhead, subject upright | Template wording tightened (head turn, one camera move) |
| `lacewalker` | Pass: giant head and miniature, bag hides the cut, miniature on a strap | `reference_image` route needs identity-only wording |
| `clones` | Read as the effect; count overshot (about nine figures at 4 s for seven requested) | Copies stood between cars, not on roofs; treat counts as approximate or request fewer |
| `stop-world` | Pass: blurred crowd, sharp subject, finger snap, walk to medium shot | None observed |
| `eyes-in` | Pass: dive through eye and pupil to black without a blink | Opening framing slot must match the photo |
| `infinite-clones` | Read as the effect: car drifts in, doors open, stream of runners (peak 15 to 17 for 20) | Only two doors showed open and runners left the frame; count is a ramp; reference needs identity-only wording |
| `smash-and-grab` | Read as the effect: palms on glass, stone, shatter, grab, hard cut to a chase at about 7.2 s | Native audio leaked a shouted line despite "no speech"; a ghost jar at about 0.5 s; the carried jar was not clearly visible in the chase; label clause for unlabelled products |

Not covered by the probes: 720p or 1080p finals, any second photo or subject,
real people (Virtual Portrait route), branded products, post steps, and the
chained second clip for `eyes-in`.

## Full run on 2026-10-08

Project `projects/effects-showcase/` (local, not committed): all 45 effects, one
invented adult subject with an identity sheet, 9:16 start frames, one or more
480p Seedance 2.5 drafts per effect with generated sound on, each take inspected
from 2 fps and 6 fps contact sheets and full-size frames, the sound checked with
`seed_audio_understand`. The four restyle effects used a person-free 5 s source
clip (scene-46). Outcome counts: 14 clean, 28 usable with defects, 3 not
achieved (`canvas`, `palette`, `lsd`).

- **clean**: the signature look landed and the review found only minor or
  sound-only deviations.
- **usable with defects**: the signature look landed but the review recorded a
  real defect (a leaked music or vocal track, a count or timing miss, invented
  lettering, a missing beat).
- **not achieved**: no take passed the review.

Review status in the project is written by a helper and can read `pass` beside a
recorded defect; this table follows the recorded defects, not the status field.

| Effect | Scene | Tested | Route used | Outcome | Main defect |
| --- | --- | --- | --- | --- | --- |
| `wild-ride` | 01 | yes (2 runs) | first-frame | usable with defects | the person is out of view during the overhead orbit; the start frame seats her on the bonnet instead of leaning from a window |
| `incline` | 02 | yes (2 runs) | first-frame | clean | the tilt is subtle; the sound is a hum and scrapes, not the paper, cart and cat foley |
| `street-colossus` | 03 | yes (2 runs) | first-frame (Seedream giant frame) | clean | pedestrian and taxi counts are approximate; the footfall thuds may read as explosions |
| `tracking` | 04 | yes | first-frame plus tracking overlay in post | usable with defects | the cuts land at about 1.4 s and 2.7 s, not at the prompted times |
| `bullet-time` | 05 | yes | first-frame | usable with defects | faint chatter and a gasp in the sound; frozen-item counts are approximate |
| `high-flip` | 06 | yes | first and last frames | usable with defects | the camera closes to chest-up within 0.5 s; the second person reads as two or three chains and his hands pass through the cards |
| `floating-fall` | 07 | yes | first-frame | clean | the straw is not clear in the macro shot; the landing is a clatter, not a soft thud |
| `moonwalk` | 08 | yes | first and last frames | usable with defects | a sustained bowed-string drone (music-like) leaked into the sound; she ends facing forward, not up at the cloud |
| `studio-slide` | 09 | yes | first-frame | clean | three copies counted, a fourth not ruled out; the choker is only partly visible at the end |
| `clones` | 10 | yes (2 runs) | first-frame | usable with defects | the figure count runs about one above the request (7 to 8 for 7) |
| `infinite-clones` | 11 | yes (2 runs) | first-frame (reference route replaced) | usable with defects | the runner count overshoots the ramp (about 20 to 25 against 20); the tyre screech is not confirmed; the car resembles a real sedan |
| `selfception` | 12 | yes | first-frame | usable with defects | the copy never grows into a full-size second woman, so the hand-over is not clearly shown |
| `act-natural` | 13 | yes (2 runs) | first-frame | usable with defects | the neon sign lettering is garbled; the orbit is modest; a faint murmur in the sound |
| `stop-world` | 14 | yes (2 runs) | first-frame | usable with defects | the crowd is lighter than packed and some people are only partly blurred |
| `eyes-in` | 15 | yes (2 runs) | first-frame | usable with defects | the iris turns amber-orange instead of her dark brown |
| `lacewalker` | 16 | yes (2 runs) | first-frame (reference route rejected) | usable with defects | a drum-like musical beat from about 5 s; the handbag shape differs between the two shots |
| `superstar` | 17 | yes | first-frame (reference route rejected) | usable with defects | a sung vocal in the first seconds; the face is small in the opening wide shot; unreadable cursive on the jacket back |
| `vanish` | 18 | yes | first-frame | usable with defects | she vanishes about 0.3 to 0.5 s before the 2 s beat; dark trouser patches show at the hoodie shoulders |
| `world-morphing` | 19 | yes (2 runs) | first-frame | usable with defects | the towers tilt like leaning blocks rather than folding; the sound reads as a passing vehicle |
| `architecture-wave` | 20 | yes | first-frame | clean | no wind bed was audible; a low groan and creaking instead |
| `melting` | 21 | yes (2 runs) | first-frame | usable with defects | only one boot is left at the end; brown drips also run down her arms |
| `burning-man` | 22 | yes | first-frame | clean | the footsteps sound hard-soled on tile; the flame reflection on the pavement is subtle |
| `particles` | 23 | yes | first-frame | usable with defects | she barely moves, so the overlay carries the effect; the overlay boxes hold text-like line patterns |
| `lidar` | 24 | yes | first and last frames (generated cyan first frame; last-frame-only rejected) | clean | the change into real colour finishes about 1 s later than planned |
| `earth-zoom` | 25 | yes | first and last frames (generated orbit first frame; last-frame-only rejected) | clean | one continuous move; street counts are approximate in motion |
| `blue-depth` | 26 | yes | first-frame, second take | usable with defects | the first take let fish cross her face (fixed in the retake); fish and jellyfish counts are approximate |
| `desktop-glitch` | 27 | yes | first-frame, retake | usable with defects | both takes have review status fail: take 1 panels carried pseudo-lettering; the retake has plain panels but she barely moves and the panel counts are 4 and 6 for 5 and 7 |
| `comic` | 28 | yes | video edit with an environment image | usable with defects | the background changes about every second, not every 0.3 s; no stepped look until retimed in post |
| `canvas` | 29 | yes | video edit | not achieved | take 1 doodled only the sky between 1.5 and 4 s; take 2 put doodles on the car body, which the prompt forbade |
| `palette` | 30 | yes | video edit, then reference-to-video retake | not achieved | the edit route painted only the sky; the retake paints sky and buildings but the car and road stay lightly painterly (review fail) |
| `lsd` | 31 | yes | video edit; the first submission was rejected for its output audio | not achieved | no wave warp or halftone dots, a slow look hold, and the car turns dark grey (review fail) |
| `scrapbook-collage` | 32 | yes | first-frame plus deterministic layout | clean | the kick goes to frame-left; the cadence reads stepped |
| `cutout` | 33 | yes | first and last frames with the same image | usable with defects | a quiet orchestral underscore leaked; the floating pieces read as crumpled paper, not clearly the lamps and counter |
| `pearl-earring` | 34 | yes | first-frame plus FFmpeg stack | clean | the fabric rustle is not audible; the turban top sits close to the crop edge |
| `cyclope` | 35 | yes | first and last frames plus FFmpeg stack | usable with defects | a rising orchestral score leaked; the giant head arrives about 1 s late; her face is small and turned away |
| `fallen-angel` | 36 | yes | first-frame plus FFmpeg stack | clean | the lift is about 0.5 s early; one quiet sigh in the sound |
| `smash-and-grab` | 37 | yes (2 runs) | first-frame | clean | the patrol car is not clearly seen; the thief is an invented second character, not the hero |
| `boarding-pass` | 38 | yes | first-frame, three submissions | usable with defects | the first tickets carried invented prices and digits; the plain-card retake shows perforation holes instead of the described band and stripes |
| `monster-dab` | 39 | yes | first-frame | usable with defects | the creature is never fully in frame; only legs, hands, hem and lower face show |
| `pigeons` | 40 | yes | first-frame plus FFmpeg fisheye | clean | the head is cropped in the close low shots |
| `skatedog` | 41 | yes | first-frame plus FFmpeg fisheye | clean | the dog huffing can read as a growl and the sound is loud |
| `agamemnon` | 42 | yes | first-frame | usable with defects | orchestral music baked in from about 10 s to the end |
| `mighty-fighter` | 43 | yes | shot A first and last frames, shot B first-frame, joined in post (reference route failed) | usable with defects | shot A opens with the torso as well as the boots; shot B is almost silent |
| `fairytale-castle` | 44 | yes | first-frame | usable with defects | an orchestral score from about 3 s; the castle resembles a well-known theme-park castle; sheep and firework counts not verified |
| `frozen-in-motion` | 45 | yes | first-frame | usable with defects | the crossing pedestrian hides her too much and a cyclist wheel overlaps her legs |

What the run did not cover: 720p or 1080p finals and the draft promotion path,
a second subject, real people and Virtual Portraits, branded products, the
chained second clip for `eyes-in`, and any photo supplied by a user instead of a
generated start frame. Provider rules found are in
[generation-flow.md](generation-flow.md#provider-rules-observed).

## Tooling findings

- Reference images and start frames need `--ref` evidence: an approved manifest,
  a candidate review and a hash-bound decision.
- The provider task ID is write-once in the registry; register the `cgt-` ID, not
  the Ark job ID.
- `camera_fixed` and a seed are not exposed by `seedance_2_5_create_task`.
- `seed_media_export_artifact` with a destination path is disabled without
  configured output roots; copy from the artifact store path.
- Draft renders finished in 1 to 2.5 minutes; promotion with `draft_task_id`
  renders 1080p only.

## Untested hypotheses

None of the 45 menu entries is untested any more, but each has one take on one
invented subject. Still unverified: the same recipes on a user's photo (a real
face may be refused as a start frame; see the rights step), the reference-image
routes with a user-supplied non-crop reference, edit-route draft mode, and the
promotion path.
