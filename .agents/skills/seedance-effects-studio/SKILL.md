---
name: seedance-effects-studio
description: >-
  Orchestrator. Offer a menu of 45 named video effects (street colossus, incline,
  clones, melting, world morphing, eyes in, bullet time, earth zoom, smash and
  grab and more), let the user pick one, inspect their photo or clip, write that
  effect's Seedance 2.5 prompt from its recipe, run prompt-review, submit a 480p
  draft through ark-mcp, save and QA the take, then ask before any higher
  resolution final. Sequences seedance-prompt-25, prompt-review, ark-mcp,
  seedance-restyle (video-to-video effects), showcase-html and the post tools
  named in each recipe. Use when the user wants a named visual effect applied to
  their own photo, product or clip, or asks what effects are available. Not for
  free-form prompts (seedance-prompt-25), whole-clip restyles that are not on the
  menu (seedance-restyle), or multi-scene films (film-production).
---

# Seedance Effects Studio

**Declared orchestrator.** This skill owns the sequence pick effect → intake →
slot fill → prompt → review → freeze → draft → QA → decision. It is exempt from
the leaf-skill rule that a skill never loads another; the specialists it loads
stay independent and usable alone. It never calls the Ark REST API: submission
goes through `ark-mcp`.

## Origin and scope

The menu catalogues the 45 effects shown on a third-party public effects page
(analysed 2026-10-08, including the twelve in that product's launch video). The
names are short descriptive labels that come from that page; this skill is not
affiliated with or endorsed by that product. Each recipe reproduces the visible
mechanic with Seedance 2.5 from the observed example footage; it does not reuse
that product's footage, prompts, models or presets. When the user cites an
effect by another name, match it to the nearest entry or say that none fits.

## Boundary

| Need | Use | Why not this skill |
| --- | --- | --- |
| A named effect on the user's photo, product or clip | this skill | Menu entry exists |
| A custom prompt with no named effect | `seedance-prompt-25` | No recipe to fill |
| Redraw a whole clip in a medium that is not a menu entry | `seedance-restyle` | The four restyle effects here delegate to it |
| Swap one element in a kept take | `seedance-object-swap` | Edit, not an effect |
| Multi-scene film or ad | `film-production` | Stage canvas and canon, not one effect |
| Exact on-screen text, HUD or UI | `html-graphic-render` or HyperFrames in post | Never baked into generated video |

## Menu

Show the user the groups below (label, one-line look from the recipe, the start
input it needs) and let them pick by label. When a request is vague, offer the
three entries whose start input matches what they have. The recipe file holds the
look, route, parameters, start-photo contract, beats, prompt template, slots,
post steps, QA and risks for each id.

### Camera and motion

Recipes: [effects-camera-and-motion.md](references/effects-camera-and-motion.md)

| id | Label | Route | Duration | Start input |
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

### Clones and identity

Recipes: [effects-clones-and-identity.md](references/effects-clones-and-identity.md)

| id | Label | Route | Duration | Start input |
| --- | --- | --- | --- | --- |
| `clones` | Clones | `i2v-first-frame` | 7 s | Full-body, standing, wide open location |
| `infinite-clones` | Infinite clones | `reference-images` | 7 s | Full-body, distinctive outfit and headwear |
| `selfception` | Selfception | `i2v-first-frame` | 5 s | Standing, open palm holding a tiny copy |
| `act-natural` | Act natural | `i2v-first-frame` | 6 s | Person caught mid-action, busy location |
| `stop-world` | Stop world | `i2v-first-frame` | 8 s | Standing figure inside a crowded space |
| `eyes-in` | Eyes in | `i2v-first-frame` (+ optional second clip) | 7 s | Portrait, open eye toward camera, well lit |
| `lacewalker` | Lacewalker | `reference-images` | 8 s | Full-body outfit, readable face with glasses or hat |
| `superstar` | Superstar | `reference-images` | 15 s | Clear face, distinctive outfit, waist-up |
| `vanish` | Vanish | `i2v-first-frame` | 5 s | Loose shape-holding clothes, kneeling or leaning |

### World and transformation

Recipes: [effects-world-and-transform.md](references/effects-world-and-transform.md)

| id | Label | Route | Duration | Start input |
| --- | --- | --- | --- | --- |
| `world-morphing` | World morphing | `i2v-first-frame` | 8 s | Centered person, open street, tall surroundings |
| `architecture-wave` | Architecture wave | `i2v-first-frame` | 7 s | Low-angle person, big rigid structure behind |
| `melting` | Melting | `i2v-first-frame` | 7 s | Full-body standing person, flat clear ground |
| `burning-man` | Burning man | `i2v-first-frame` | 7 s | Full-body person, empty space beside, dusk |
| `particles` | Particles | `composite` | 5 s | Single subject, dark high-contrast scene |
| `lidar` | Lidar transition | `i2v-last-frame` | 7 s | Person outdoors, distinct posts and skyline |
| `earth-zoom` | Earth zoom | `i2v-last-frame` | 10 s | Eye-level person on a plausible city street |
| `blue-depth` | Blue depth | `i2v-first-frame` | 8 s | Waist-up person in front of dark blue water |
| `desktop-glitch` | Desktop glitch | `composite` | 5 s | Cool-toned action shot with negative space |

### Art and style

Recipes: [effects-art-and-style.md](references/effects-art-and-style.md)

| id | Label | Route | Duration | Start input |
| --- | --- | --- | --- | --- |
| `comic` | Comic | `v2v-restyle` | source length (typ. 5 s) | user's clip, one central subject |
| `canvas` | Canvas | `v2v-restyle` | source length (typ. 5 s) | user's clip, one separable moving subject |
| `palette` | Palette | `v2v-restyle` | source length (typ. 5 s) | any clip, wide-angle or fast motion |
| `lsd` | LSD | `v2v-restyle` | source length (typ. 5 s) | clip, people close to camera |
| `scrapbook-collage` | Scrapbook collage | `composite` | 6 s | full-body standing, plain background |
| `cutout` | Cutout | `i2v-first-and-last` | 8 s | person small in structured environment |
| `pearl-earring` | Pearl earring | `composite` | 7 s | head-and-shoulders face, plain background |
| `cyclope` | Cyclope | `composite` | 7 s | one person, full body, outdoor |
| `fallen-angel` | Fallen angel | `composite` | 7 s | clear upper-body portrait, one person |

### Product, creature and spectacle

Recipes: [effects-product-and-spectacle.md](references/effects-product-and-spectacle.md)

| id | Label | Route | Duration | Start input |
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

## Procedure

Run the stages in order. A stage that cannot be satisfied stops the run and
states what is missing.

1. **Pick.** Resolve one effect id. One effect per run; a second effect is a new
   run. Read only that effect's section from its recipe file.
2. **Intake.** Collect the start asset the recipe asks for (photo, product photo,
   or source clip). Record its path and SHA-256. Check rights before any
   generation: the user records a rights decision for the asset and the people in
   it. A real face used as an image-to-video start frame needs the user's
   statement that it is their own photo or that the person consented; stop on a
   provider rejection instead of working around it. For video-to-video effects
   follow the video-to-video inputs contract: people in a source clip are bound as
   `asset://` videos, Virtual Portrait anchors are for invented characters only,
   and a specific real person as the target is outside the workflow (offer an
   invented character). Real brand marks come from an authorized real asset, never
   from generation. Unknown rights stay unresolved.
3. **Inspect and fit.** Look at the asset (and use `seed_understand` for clips).
   Compare it with the recipe's **Start photo** contract. If the asset does not
   fit, say what is wrong and either build the missing start frame
   (`seedream_generate_image` with the user's photo as an identity reference, per
   the recipe) or ask for a better asset. A generated start frame is a provider
   operation like the video: prompt snapshot, review, registry entry, local copy
   and an approval record before it is used. One sample is enough for a start
   frame; record that choice and offer three samples when the user wants
   alternatives. Never fill
   a slot with a guess about something the photo does not show.
4. **Fill slots.** Read every `{slot}` from the asset or take the recipe default.
   Count people, objects and copies that the recipe states by number. Name hands
   by anatomy and frame side. Describe unlabeled props positively with no
   invented lettering.
5. **Compose.** Take the recipe's prompt template with `seedance-prompt-25`
   grammar (six-part formula, `@Image N` role line, `At Ns` timestamps, audio
   brackets). Keep the template's mechanics intact; change only slot values and
   fix sentence logic broken by a slot. Write the roles and parameters from the
   recipe's **Route** and **Parameters**.
6. **Hash and review.** Save the prompt beside its intended output, resolve
   current capability evidence, and compute the request hash with
   `prepare_request.py` without `--write` or `--register`. Run `prompt-review`
   bound to that hash (Seedance 2.5 generate; plus Seedream for a generated start
   frame). Resolve CRITICAL and MAJOR findings; a changed prompt byte changes the
   hash and needs a new review.
7. **Freeze and register.** Re-run `prepare_request.py` with the review and
   capability files and `--write --register` so the prepared operation is in the
   project `task_ids.json` before any submission. Read
   [generation flow](references/generation-flow.md) for the exact calls.
8. **Draft.** Submit one 480p draft through `ark-mcp` (`draft: true`; the video-to-video effects use `resolution: 480p` instead, because draft mode is unproven on edit routes). Save the
   provider task ID as soon as it is acknowledged. Poll the same task; never
   resubmit after a timeout.
9. **Persist and QA.** Save the video locally, record bytes, SHA-256 and actual
   media properties, inspect it by playback or frame sampling against the
   recipe's **QA** list, and write down what passed and failed.
10. **Decide.** Show the draft and the QA result. Offer: accept, revise the prompt
    (one named change, new review, new draft), or promote to a final with the
    draft task ID. Promotion to a final needs the user's go-ahead, an
    estimated cost, and its own registered operation (see the generation flow). Apply the recipe's **Post** steps (overlay text, split-screen
    stack, fisheye, ambience bed) only after the picture is accepted.

A project folder is required for any submission: `projects/<name>/` with
`project.md`, `task_ids.json` and the showcase canvas, as in the production
policy. For a prompt-only request (the user only wants the prompt, or works in
Lumina) stop after step 6 and return the prompt package; no files, no
submission.

## Routes

| Route | Seedance inputs | Notes |
| --- | --- | --- |
| `i2v-first-frame` | One image with role `first_frame` | The photo is the opening frame; ratio locks to it |
| `i2v-last-frame` | One image with role `last_frame` | The clip ends on the photo; confirm live support, else build a first frame |
| `i2v-first-and-last` | `first_frame` and `last_frame` images | Both ratios match |
| `reference-images` | Images with role `reference_image` | The clip does not open on the photo; state ratio; add identity-only wording |
| `v2v-restyle` | Source clip, muted master | Delegate to `seedance-restyle`; its rules replace this table |
| `composite` | Generated clip plus a deterministic step | FFmpeg stack, HyperFrames overlay or `html-graphic-render` layout named in the recipe |

A first-frame image cannot be combined with reference images. Parameters that the
live tool does not expose (there is no `camera_fixed` and no seed field) are
expressed in prose or omitted.

## Hard rules

1. **Mechanics from the recipe, facts from the asset.** Do not rewrite an effect's
   beats to suit a taste; revise through the Decide stage.
2. **No text inside generated video.** HUD, labels, captions, UI and city names
   are added in post with HyperFrames or `html-graphic-render`.
3. **Native audio is off** unless the recipe justifies it. Every audio sentence in
   a template is conditional on `generate_audio`: when it is on, list sound effects
   only and end with "with ambience only, no music and no speech", then check the
   draft's track before promoting (a promotion reuses the draft's audio). Native
   audio has baked music and speech into other runs, including a shouted voice in
   the smash-and-grab probe.
4. **Counts are explicit** at every timestamp, and copies share one face and one
   outfit.
5. **Always a draft first.** 480p draft, inspect, then ask before the final.
   Never submit the same paid generation twice or through two transports; an
   ambiguous timeout is reconciled, not retried.
6. **Identity references are labelled.** A reference image gets "use only for the
   person" wording with what to ignore (pose, background, light) when its scene
   could leak.
7. **Status honesty.** Report a recipe as verified only if a probe draft showed
   its signature look; otherwise it is an untested hypothesis. See
   [evidence status](references/evidence-status.md).
8. **Rights stay separate from creative approval.** A request to generate does
   not grant likeness, brand or music rights.
9. **The recipe is the shot plan.** Each recipe carries an explicit per-shot
   camera plan (timeline, camera move, cuts). Record that as the exemption from
   the `shot.plan_bound`, `shot.variety` and `shot.axis_carry` rules in the shot
   manifest, omit those required rules in the request check, and let the reviewer
   record them as `not_applicable` with the exemption as the reason.

## Reference loading

| Need | File |
| --- | --- |
| Per-effect recipe | `references/effects-<group>.md` from the menu |
| Calls, parameters, registry, QA and post steps | [generation-flow.md](references/generation-flow.md) |
| What has been probed, results and fixes | [evidence-status.md](references/evidence-status.md) |
