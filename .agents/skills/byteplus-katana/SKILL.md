---
name: byteplus-katana
description: >-
  Plan a reference video edit rebuilt with the user's own characters, products
  or clothing. Measures the reference into an edit decision list (shot order,
  cut times, cut driver: beat, speech, action or none, motion inventory,
  text), maps up to five assets to slots, and routes each segment by what it
  shows: live-action footage becomes kept, recast or generated shots; posed
  cutouts, cards and graphics become HyperFrames layers; exact type stays
  deterministic. Scales shots to the reference, sets a credit budget and
  tracks per-segment refinements. Use for "make this edit with my product"
  in any format: fashion lookbooks, product launches, food, travel montages,
  talking-head explainers, music-led hero and aura-farming edits. Planning
  only. Not for style recipes (template-factory), recasting
  one clip (seedance-motion-recast), one-element swaps (seedance-object-swap)
  or single shot prompts (seedance-prompt-25).
---

# Reference Edit Rebuild

The reference edit supplies **structure**: shot order, shot length, cut
placement and what drives it (music, speech or action), pacing, transitions,
motion design and on-screen text timing. The user's assets supply **who and
what appears**. This skill turns that split into a Rebuild Plan that a
production run can execute segment by segment and refine without rebuilding
the whole edit.

**Two layers, chosen per segment from the measured reference, never from a
genre label.**

- **Footage layer.** What each reference segment shows decides its route. A
  segment that shows photographic footage of a subject moving through space
  (walking, turning, pouring, a camera moving around a person) needs footage:
  the user's own clip kept, a recast or swap with rights, or a generated shot.
  A segment that shows a subject posed on a graphic (cutout, sticker, card,
  collage, screenshot, packshot) is built from the supplied assets as layers.
  Most edits mix both. Animating a still to stand in for a moving-footage
  segment reads as cheap; animating a cutout for a cutout segment is the
  faithful rebuild.
- **Type-and-effects layer.** Always code-built in HyperFrames: words on the
  cut driver, masks, flashes, split screens, insets, grain. Typography follows
  the reference (or a rights-safe equivalent in grammar-only mode).
  Deterministic, exact, cheap and editable per segment.

It is a prompt-and-plan leaf. It never calls MCP tools, the Ark API or any
generator. Composition hints below are prose for the caller.

## Boundary

| Need | Use |
| --- | --- |
| Same edit structure and motion design, new subjects, per-segment control and targeted fixes | this skill |
| Reusable style or motion recipe from a pin, new content | `template-factory` |
| One clip, keep performance and camera, rebuild cast and world | `seedance-motion-recast` |
| One clip, replace one named element, keep source pixels | `seedance-object-swap` |
| One clip, same cast in a new medium | `seedance-restyle` |
| One static exact graphic | `html-graphic-render` |
| Animated composition, timeline, keyframes, render | `hyperframes` skills (this skill plans, they build) |
| One shot prompt | `seedance-prompt-25` |
| A still image of a character speaking supplied audio | `omnihuman-prompt-20` |

Choose this skill when the deliverable is a **multi-shot edit** that must keep
the reference's cut structure. If the reference is a single take of 30 s or
less and nothing else needs to be kept, recast or swap is simpler.

## Input contract

- **Reference edit**: an uploaded file or a link to the media file itself. A
  social profile or page URL is not a reference; acquire the file first. Record
  source, SHA-256, duration, fps, aspect ratio and audio presence.
- **Rights record**: owner or permission for the reference footage, its music,
  speech, characters and logos, each recorded separately. Unknown rights for a
  part means grammar-only for that part (see rule 1).
- **Assets**: up to five photos, clips or approved elements of characters,
  products or clothing, each with a role and SHA-256. More than five needs an
  explicit user decision recorded as a plan limit.
- **People**: for each person asset, whether it is an invented character, the
  user, or another real person, with the consent record for real people.
- **Instructions** (optional): priorities such as a hero product shot, an
  element to keep unchanged, platform, length, new script lines, version count
  and credit cap.

## Output contract

A **Rebuild Plan** returned to the caller:

1. `edl.json` summary: segments with start, end, cut type, cut driver, shot
   size, camera, subject slots, motion inventory, text and speech events, and
   beat or word alignment ([EDL contract](references/edit-decision-list.md)).
2. Slot map: every visible reference subject mapped to an asset, removed or
   kept as an extra ([slot assignment](references/slot-assignment-and-refinement.md)).
3. Route table: one production route per segment with the measured reason
   ([segment routing](references/segment-routing.md)).
4. Setup list: the distinct footage setups the generated or recast segments
   need, each with the segments it serves and its take duration.
5. Audio route: keep, replace, dialogue or silent, per part, with the rights
   and consent basis.
6. Generation windows, draft resolution, version count and credit estimate.
7. Refinement ledger with hashes, ready for targeted fixes.
8. Handoff gates: every generation-bound prompt is a draft until the caller
   runs `prompt-review`, freezes the prompt snapshot and registers the request
   with `prepare_request.py --register`; takes are saved and assembled in the
   project's HyperFrames Studio project, which renders the final cut.

## Workflow

1. **Intake and rights.** Record the reference, rights decisions, assets and
   people. Stop on an unusable link or unknown rights that the user will not
   resolve.
2. **Measure before describing.** Build the EDL from measured cuts (ffmpeg
   scene detection), picture duration and a frame strip, then add model
   analysis per segment. Measured times win over described times.
3. **Cut driver.** Find what each cut follows. Music: extract beat and
   downbeat times and attach each cut to the nearest beat with its offset in
   milliseconds. Speech: transcribe with word timings (`speech_to_text`) and
   attach each cut to its word or phrase boundary. Action: tie the cut to the
   measured action peak (a pour landing, a door closing). None: keep the
   measured durations as the timing authority. Record the driver per segment;
   edits often switch drivers.
4. **Slot assignment.** Map reference subjects to assets. Every visible
   subject gets a disposition. Prepare each asset as a layer (cutout with
   alpha, crop, safe margins) and resolve each person's identity route (rule 6).
   When a person or wardrobe asset cannot fill a layer as it is (a flat-lay
   where the reference shows the outfit worn), plan a `derived_still` for that
   slot. A product shot from the wrong angle is never redrawn: ask for or
   acquire an authorized packshot, or reframe the layer around the supplied
   angle.
5. **Motion inventory.** For each segment, list the reference's motion design
   as animatable properties: position, scale, rotation, opacity, mask reveals,
   easing, parallax, type animation, shape and gradient behavior, camera-like
   moves and transitions, with timings. This is the template the layers
   inherit. Use the [treatment vocabulary](references/treatment-vocabulary.md)
   for common treatments and their HyperFrames equivalents.
6. **Route each segment** from what it shows
   ([segment routing](references/segment-routing.md)). Then cluster the
   footage segments into **setups**: one setup per distinct subject, location,
   shot size and angle, and action in the reference. The setup count follows
   the reference, from one long take to dozens of setups in a long fast edit;
   when it exceeds the credit budget, merge the closest setups and record the
   merge. Each setup is generated once and cut into its appearances at the
   EDL times; its take duration is the longest continuous use plus handles,
   never below the live minimum and split or chained above the live maximum.
   The EDL stays the cut authority.
7. **Audio decision.** Keep each reference audio part only with a recorded
   rights basis; otherwise brief a replacement conformed to the cut driver.
   Generated shots under a music bed with no sync sound run with
   `generate_audio: false`, because native audio leaks music and speech into
   the cut. Speech-led segments with new lines use the `dialogue_sync` route.
   New lines change speech lengths, so once the final voice track exists,
   re-time those segments from its word timings, record the re-time as a user
   change and treat the re-timed EDL as the cut authority from then on.
   A segment that needs its own sync sound (a meme reaction, a pour, a door)
   gets an explicit choice of native or post sound rather than a silent
   default.
8. **Budget.** Layers cost no credits. Generated shots draft at 480p first;
   state the estimated credits per shot and wave, promote only the shots that
   made the cut to the delivery resolution under the project approval mode,
   and stop at any user cap. Re-check each promoted shot, because the final
   render is a new picture, not an upscale of the draft. Estimated and
   confirmed costs stay separate.
9. **Hand off** the plan with its gates (output item 8). After takes exist,
   run the assembly check below and keep the refinement ledger current.

## Hard rules

1. **Rights first, per part.** Rebuild the reference itself only when the user
   owns it or holds permission for the parts being kept: footage, music,
   speech, characters and logos. With unknown footage rights, extract grammar
   only: de-identify, drop its taglines, typography and trade dress, and hand
   off to `template-factory`. With owned footage but unknown music, rebuild
   the picture and replace the track.
2. **The cut grid lives in the assembly.** Seedance stretches or shifts dense
   timelines, so cut times are enforced when the takes are trimmed and
   assembled, not promised in a prompt. Never claim a generated clip hits a
   cut time; measure it and retime in the edit. Never cut mid-word on a
   speech-driven segment.
3. **Route by what the segment shows.** Footage segments get footage; posed,
   graphic and packshot segments get layers. A 0.4 s segment is never its own
   generation: generate its setup at natural duration and cut it. A long take
   is generated at its own length within the live range, not chopped into
   short shots. Do not compress the plan into an unsupported duration. Any
   footage route with a readable product label in frame also takes the
   `label_composite` treatment.
4. **Exact graphics are deterministic.** On-screen text, UI, logos, captions,
   labels and number counters are rendered with HTML/HyperFrames. Keep
   generated footage text-free, including a reference's burned-in captions.
   Never use Seedream or Seedance to reproduce a supplied product photo or a
   readable label; place the real pixels (the `label_composite` route).
5. **Every visible subject has a disposition**: mapped, removed or kept extra.
   Never write "replace everyone".
6. **Identity from approved elements only.** Real brands, logos and packshots
   come from authorized downloads before any Seedream fallback. People:
   - An invented character uses its approved element and, in generated
     segments, a Virtual Portrait `asset://` reference.
   - The user or another real person needs a recorded consent basis. Layered
     segments place their own photo; generated or dialogue segments bind an
     authorized real-person asset per `seedance-virtual-portrait`, never a
     Virtual Portrait group. Voice reuse needs its own voice consent, and a
     `derived_still` of a real person needs consent that covers generated
     edits of their likeness.
   - Without consent or an authorized asset, use layers only, or offer an
     invented character. Never disguise an input to pass a check.
7. **Refine by segment.** A correction invalidates only the segments it
   touches and their dependents. Unchanged takes keep their hashes and are not
   resubmitted.
8. **One spend authority.** Show the estimated cost before each generation
   wave and stop at the user's cap. Never submit the same paid segment twice.
9. **Deliver source with the render.** A motion-layout rebuild ships the
   HyperFrames project beside the render so segments stay editable; generated
   takes are flat clips and are labeled as such.
10. **Finish follows the reference.** Add grain, vignette, flashes or an RGB
    split only when the reference shows them, as HyperFrames layers. Keep
    generated takes in their original colours; no grade by default.

## Assembly check

Before delivery, compare the assembled edit with the EDL:

| Check | Pass condition |
| --- | --- |
| Shot order | Same sequence of segments |
| Cut times | Each cut within 2 frames of the EDL (the re-timed EDL after a new script), or a recorded reason |
| Cut driver | Beat cuts within their recorded offset; speech cuts on word boundaries with no clipped words; action cuts on the action peak |
| Subject slots | Each slot shows its assigned asset, no residual reference subject |
| Text events | Appear at EDL times, exact copy, legible at thumbnail size |
| Dialogue | Words match the approved script by transcript, mouth follows speech, speaker identity matches its consent record |
| Audio | Route matches the rights decision, no baked music or speech in silent routes |
| Motion | Easing, travel and timing of each layer match the motion inventory within tolerance |
| Layer fidelity | Supplied photos and labels are unaltered pixels, cut cleanly, no halos or stretched edges |
| Duration, ratio, fps | Match the reference unless the user changed them or a recorded re-time did |

## Design basis

Every mapping here is a design choice, not a claim about how any product
works internally:

1. Structure comes from a measured edit decision list, not from a model's
   description of the reference.
2. Each segment is routed by what it shows: layered motion design for posed
   cutouts, cards and graphics; footage for subjects moving through space; type
   and effects always code-built.
3. A refinement ledger keyed by segment and dependency lets a correction redo
   only the affected shots.
4. The cut grid is enforced in assembly, because generated timelines drift.
5. The five-asset default is a plan limit, not a model limit.
