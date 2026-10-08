# Evidence status

Recipes are written from the observed example footage of each effect (2026-10-08).
Twelve were then probed with one 480p Seedance 2.5 draft each. A probe shows that
a recipe can produce the effect on one invented subject; it does not guarantee
the effect on other photos, other subjects, other resolutions or real people.
Everything not listed as probed is an untested hypothesis.

Probe project: `projects/effects-probe/` (one invented woman, an invented vehicle
and an invented product; 14 Seedream images, 12 Seedance drafts, native audio
off except one).

## Probed on 2026-10-08

| Effect | Result | Caveat found |
| --- | --- | --- |
| `street-colossus` | Pass: striding giant, window POV with one helicopter at 4 s, low shot with hand on tower at 7 s | Needs the Seedream giant start frame; the raw photo has no city scale |
| `incline` | Pass: room rolled and levelled, three sliders moved, subject steady | Sliders must start on a named surface; list fixed objects |
| `wild-ride` | Pass: burnout, overhead sweep, low side track, one person attached | Opening view must follow the photo, not assume a rear view |
| `act-natural` | Pass: frozen subject, moving diner | Orbit angle subtle; crossing event must not add a person |
| `melting` | Pass: colour-matched drips, kneel, puddle, hat and boots left | None observed |
| `world-morphing` | Pass: street curled over, city inverted overhead, subject upright | Template wording tightened (head turn, one camera move) |
| `lacewalker` | Pass: giant head and miniature, bag hides the cut, miniature on a strap | `reference_image` route needs identity-only wording |
| `clones` | Read as the effect; count overshot (about 8 copies for 5 requested) | Treat counts as approximate or request fewer |
| `stop-world` | Pass: blurred crowd, sharp subject, finger snap, walk to medium shot | None observed |
| `eyes-in` | Pass: dive through eye and pupil to black without a blink | Opening framing slot must match the photo |
| `infinite-clones` | Pass: car drifts in, four doors open, stream of runners (about 15 for 20) | Count is a ramp; reference needs identity-only wording |
| `smash-and-grab` | Pass: palms on glass, stone, shatter, grab, hard cut to chase at 7.6 s | Native audio leaked a shouted line despite "no speech"; label clause for unlabelled products |

Not covered by the probes: 720p or 1080p finals, any second photo or subject,
real people (Virtual Portrait route), branded products, post steps, and the
chained second clip for `eyes-in`.

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

All other menu entries: the five recipe files mark each `untested hypothesis`.
Two route assumptions need a live check before use: `i2v-last-frame` with no first
frame (`earth-zoom`, `lidar`), and the same image as first and last frame
(`cutout`).
