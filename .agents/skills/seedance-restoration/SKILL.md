---
name: seedance-restoration
description: >
  Write Seedance 2.5 video-to-video restoration prompts that remove film grain,
  video noise, black and white scratch lines, vertical and horizontal scratches,
  hairlines, streaks, dust, dirt, flicker, and compression artifacts from aged,
  damaged, or archival footage while preserving every person, object, action,
  composition, camera movement, and timing. Use whenever the user asks to
  restore, clean, denoise, or repair old, aged, or archival footage, remove
  grain or noise, erase scratch lines or film damage, or "clean up" damaged
  film through the Seedance generative-edit route. Composes the prompt and
  specifies the diagnosis and verification steps; the caller owns submission and
  the generation lifecycle.
---

# Seedance Restoration

Write production-grade **Seedance 2.5 video-to-video restoration prompts** that
clean aged, damaged, or archival footage. This is a generative re-render: the
source clip is the sole editing master, and the prompt directs the model to
erase surface damage while locking everything the shot actually contains.

Use this skill when the user wants to:

- **restore / clean / repair** old, aged, or archival footage
- **denoise** — remove film grain and video noise
- **remove scratch lines** — black lines, white lines, vertical/horizontal
  scratches, hairlines, streaks from aged film prints
- **clean up** dust, dirt, flicker, and compression artifacts

Do **not** use for deterministic VOD AI enhancement (`vod_enhance_video`) or
FFmpeg denoisers — this skill is the Seedance generative-edit route. For the
general edit grammar and the full six-part formula, compose with
`seedance-prompt-25`; for the submission lifecycle, use the `ark-mcp` tools.

> **Known ceiling.** Seedance re-renders the picture; aggressive cleanup trades
> fine-detail fidelity for smoothness, and there is a real limit to how far a
> generative model cleans before it starts re-interpreting the image. Fast,
> thin, time-varying geometric or luminance defects (a rolling scan-line tear,
> a wave/ripple, a bright band) are the hardest case — even with correct
> vocabulary they can be reproduced as "content" rather than erased. If residual
> grain or lines remain after escalation, surface the deterministic alternative
> (temporal denoiser + scratch-removal filters in FFmpeg) rather than promising
> a generative fix.

## Input and output contract

Input: a source clip prepared per the
[video-to-video inputs contract](../../contracts/video-to-video-inputs.md)
(rights decision, probe data, SHA-256, muted master and saved audio), the
requested cleanup targets, and the may-change / must-preserve contract.

Output: a Seedance 2.5 structured-edit prompt with the muted master bound as
`@Video 1`, the parameters, the ladder rung, and the post-audio step. The caller
owns prompt review, the task registry and submission.

**People in the footage.** Archival footage usually shows real people. The
provider rejects a realistic person in a video input with `PrivacyInformation`;
the only route is the contract's `asset://` video, registered under the
depicted people's authorization. Without that authorization the generative
route is closed: never crop, blur, stylize or re-encode the footage to pass the
check, and offer the deterministic route (VOD enhancement or FFmpeg filters)
instead. Footage without people binds normally.

## Source timing

Preserve the full measured source: fractional duration, frame count, fps,
decoded timestamps, cuts, playback speed, the final word and audio tails.
Derive the muted master and saved audio from the same full timeline unless a
specific derivative is approved; preserve the original picture and sound.

Missing or malformed timing measurements stop an execution-ready package.
Never guess duration, round a supplied value, or invent inspection evidence;
return an unresolved handoff requesting valid measurements.

A timing adaptation requires a specific current provider requirement for the
selected model, operation and transport, plus explicit derivative adaptation
approval from the user after explaining alternatives and timing/audio effects.
`approve_for_me` does not supply that approval. Empirical stability advice,
prior-run tolerances and creative selection do not establish a requirement.

Denied or missing adaptation approval leaves the original unchanged: no
derivative is prepared and no incompatible request is recommended for
submission. Offer unselected source-preserving alternatives or a handoff.

For an approved derivative, record source SHA-256, derivative SHA-256, the
exact window, command, timing delta and audio consequences. Keep source and
derivative measurements separate; muted picture and saved audio use the same
approved span. Never overwrite the original or extend the approved scope.

No automatic 8n+1 frame recipe or whole-second rounding is permitted. Do not
trim, pad or retime to satisfy a preferred length or center a defect.
Check current input limits; a suggested split is not an approved split.

These timing rules govern referenced recipes: examples, repair suggestions
and old ladders do not authorize adaptations or extra probes. If a reference
conflicts, preserve the full measured timeline and the approval gates above.

An output mismatch remains unresolved after measuring picture, saved audio,
timestamps, cut boundaries and playback speed and inspecting opening/ending
sync. Never hide it with `-shortest`, padding or truncation. Retain the masters,
report lost frames, the final word or sound tails, and obtain the same
requirement evidence and specific approval before a corrective adaptation.

An optional partial probe is a needs-based proposal for a bounded uncertainty,
requiring explicit approval of its window and additional generation scope.
It is not delivery and never changes the full source target. Record its span
and hashes separately; a passing probe cannot replace the full-duration native
Draft or approve untested opening/ending content.

Every new Seedance 2.5 generation uses explicit `resolution: "480p"` and boolean
`draft: true` in every review mode, including an approved probe. Missing native
Draft controls stop the package until capability or transport conflicts are
resolved; never drop `draft` or substitute plain 480p. Review and select the
full-duration native Draft before supported promotion by `draft_task_id`.

## Procedure

1. **Diagnose the defect first — never guess the vocabulary.** Inspect the damaged
   clip natively (sampled frames at full resolution, including the frames around
   the defect window) and characterize the artifact precisely: its
   exact type (grain, scratch line, dust, flicker, a horizontal scan-line tear, a
   rolling wave/ripple, a geometric warp, a luminance band), its direction of
   travel, its timing window, and whether it displaces the image or only changes
   brightness. Misnaming the defect is the single biggest cause of under-fixes —
   a wave-removal prompt will not fix what is actually a horizontal scan-line
   tear + luminance band. Use the diagnosis to drive the
   prompt's vocabulary word-for-word.
2. **Inspect the source.** Measure the full fractional timeline per
   [Source timing](#source-timing), resolution and aspect. Read the defect mix
   from the footage and the diagnosis.
3. **Preserve the source timeline.** Verify current route limits without
   automatic trimming, padding or retiming. A boundary defect remains in its
   original position; missing clean context is a limitation, not permission
   to re-center it. Any required derivative follows the evidence and approval
   gates in [Source timing](#source-timing).
4. **Choose an escalation level** (below) based on how much cleanup is wanted and
   what the last take under-delivered on. For localized tears/bands/waves, use the
   dedicated framing in [Localized transient defects](#localized-transient-defects-scans-tears-bands-waves) rather than the grain ladder.
5. **Write the prompt** using the canonical template. Make the dominant defect
   explicit and dominant; never bury it in a mixed list.
6. **Package for review.** Return the prompt, parameters and ladder rung; the
   caller runs prompt review against the Seedance 2.5 edit checklist before
   submission. Every new probe or revised take uses `resolution: "480p"` and
   boolean `draft: true` in every review mode. Resolve capability or transport
   conflicts before submission; never drop `draft`. Start with the full-span
   native Draft; an additional defect-window probe is optional and needs
   explicit scope approval. Check lines, tears, bands, people and camera across
   the full span. Grain and fine texture require final-resolution inspection.
7. **Verify the fix before splicing — do not trust the task.** Inspect
   the Seedance output the same way and check the same three things: the
   defect is gone, the people/scene/camera are intact, and no new artifacts were
   introduced. Only splice a verified-clean clip; a technical `succeeded` is not
   proof the tear/wave/grain actually left. Measure the full output timeline
   against the approved source before any splice; mismatches remain unresolved.
8. **Mux the saved original audio** onto the silent restored video, per the
   contract's post-audio section, preserving the final word and sound tails.
   Inspect opening, middle and ending sync; never hide drift with padding,
   truncation or `-shortest`.

## Escalation ladder

Levels, least → most aggressive. Escalate one step when the
previous take leaves residual damage; change only the wording and defect
emphasis, keep the preserve-locks stable.

| Level | Dominant target | Key phrasing |
|---|---|---|
| **1 — gentle cleanup** | scratches, dust, grain as a mixed list | "restore and clean the archival footage" |
| **2 — aggressive denoise** | grain / noise | "grain removal is the dominant task — push it hard, frame by frame, until no visible noise or shimmer remains" |
| **3 — scratch lines + grain** | black/white scratch lines **and** grain | "black lines and scratches … are a dominant defect — eliminate every one of them, frame by frame, until no line or scratch remains" |

## Localized transient defects (scans, tears, bands, waves)

A **distinct defect class** from broad grain/scratch cleanup. These are thin,
fast, time-varying geometric or luminance artifacts — a horizontal scan-line
tear (scan lines displaced left/right inside a narrow band), a rolling
wave/ripple, or a washed-out bright/dark luminance band that travels across the
frame. They need different vocabulary and a different mental model:

- **Reconstruct, don't remove.** These artifacts are best framed as *missing or
  corrupted data to rebuild from the clean scan lines above and below the band*,
  not as "a tear to erase." "Remove the tear" tells the model the band is content
  worth keeping; "rebuild the corrupted strip from surrounding clean context" gets
  it to redraw the band cleanly. This is the single most effective phrasing for
  this class.
- **Name it precisely.** A scan-line tear is not a "wave" and not a "geometric
  warp" — wrong vocabulary produces a partial fix. Confirm the exact type by
  direct inspection first (see Procedure step 1).
- **Do not hedge.** For these defects, "aggressively remove" + "completely
  eliminate … through the final frame" is appropriate; the timid "keep everything
  the same" framing lets the model reproduce the band as content.
- **Preserve boundary defects.** Inspect the actual defect window, including
  the final frame. Do not move it to mid-clip or add clean margins by changing
  the source timeline. An optional bounded probe follows [Source timing](#source-timing).
- **Expect the model to sometimes reproduce them.** A rolling tear is the hardest
  restoration case. Verify by direct inspection before splicing; if it persists
  after 2–3 attempts with correct vocabulary, fall back to a deterministic
  temporal repair (motion-compensated interpolation / temporal median over the
  affected frames), which can rebuild the band from neighboring clean scan lines.

### Template (scan-line tear / rolling band)

Submit with `omni_reference_task_type="edit"`, `generate_audio: false`, and the
native Draft settings `resolution: "480p"` and boolean `draft: true`.
Promote the selected draft by `draft_task_id` with only supported output settings.

```text
[Edit Goal]
Edit @Video 1 to <rebuild/eliminate> a <thin full-width horizontal band / rolling
vertical ripple> where <the scan lines are scrambled and displaced / the image is
warped> <and the exposure is washed out and uneven>, rolling <top-to-bottom>, so
the final picture is flat, continuous, and evenly exposed with no seam, while
every person, object, action, composition, camera movement, and timing stays
exactly as it is.

[Edit Scope]
A narrow <full-width horizontal band / vertical ripple> is corrupted: <describe the
scrambling/displacement and the washout>. Treat it as missing data and reconstruct
it from the clean <scan lines above and below / surrounding frames>, so the repair
is invisible. <For rolling artifacts:> It rolls from the <top> edge to the <bottom>
edge and disappears — eliminate it wherever it sits on each frame, through the
final frame, until no seam, misalignment, or exposure mismatch remains anywhere.
Do not change the framing or geometry of the scene. Do not perform broad
film-grain or noise removal; retain the real surface texture of skin, fabric, and
objects. Keep edges crisp — do not soften the image into a blurry or mushy
picture. Do not modify any person's face, body, clothing, or gestures; do not
modify the background objects, set, or props; do not modify the camera movement,
framing, or cuts; do not modify the lighting direction, color grade, contrast, or
exposure. Exactly one of each person remains in frame, each in their filmed
position.

[Audio]
Silent output. Sound is added in post.
```

## Canonical prompt template (Seedance 2.5 edit)

Submit with `omni_reference_task_type="edit"`, `generate_audio: false`, and the
native Draft settings `resolution: "480p"` and boolean `draft: true`.
Promote the selected draft by `draft_task_id` with only supported output settings.
Both templates end with the silent `[Audio]` block.

```text
[Edit Goal]
Edit @Video 1 to <aggressively/completely> remove <dominant defect(s) — name them
explicitly: film grain, video noise, black lines, white lines, vertical scratches,
horizontal scratches, hairlines, streaks>, so the final image is clean, temporally
stable, and free of <grain and line> artifacts, while every person, object, action,
composition, camera movement, and timing stays exactly as it is.

[Source Video Role]
@Video 1 is the sole editing master. It defines the people, their faces, clothing,
and body language, the scene and background, the actions and event order, the camera
position and movement, and the lighting and color.

[Edit Scope]
Aggressively remove all old-film damage across the entire video: film grain, video
noise, black lines, white lines, vertical scratches, horizontal scratches, hairlines,
streaks, dust, dirt, flicker, and compression artifacts. <Name the dominant defect
and push it hard: "…are a dominant defect — eliminate every one of them, frame by
frame, until no … remains."> Denoise temporally so grain does not flicker between
frames, without introducing motion blur, ghosting, or trailing on moving subjects
or the camera. Remove only the film-print grain, noise, and scratch artifacts —
retain the real surface texture of skin, fabric, and objects. Keep edges crisp —
do not soften the image into a blurry or mushy picture. Do not modify any person's
face, body, clothing, or gestures; do not modify the background objects, set, or
props; do not modify the camera movement, framing, or cuts; do not modify the
lighting direction, color grade, contrast, or exposure. Exactly one of each person
remains in frame — never a second or duplicated copy.

[Content to Preserve]
Keep every person's identity, face, expression, body, clothing, and motion from
@Video 1 unchanged. Keep the scene, background, set, props, camera position, camera
movement, framing, cuts, event order, and timing from @Video 1 unchanged. Keep the
lighting direction, color, contrast, and exposure from @Video 1 unchanged. Faces
stay real and natural — never waxy, plastic, or warped; faces stay naturally
grounded in the scene with no cut-out edge, no halo; rim light matches the key
direction.

[Audio]
Silent output. Sound is added in post.
```

## Guardrails

- **Name the dominant defect, don't hedge.** A mixed list with "keep everything
  exactly the same" makes the model timid and under-cleans. Make the target
  defect explicit and dominant.
- **The discriminator line is mandatory.** Always include "remove only the
  film-print grain, noise, and scratch artifacts — retain the real surface
  texture of skin, fabric, and objects." This is what prevents the model from
  over-smoothing into waxy/plastic skin when you push grain removal hard.
- **Never demand contradictory absolutes.** "Completely remove all grain" plus
  "keep every pore and fine hair" is physically unresolvable and invites
  over-smoothing. Rank the outcome: cleanup first, detail second.
- **Single source reference.** Only `@Video 1` is bound; no image/audio
  references. `[Target Material Role]` is omitted.
- **Preservation locks.** Quantity ("exactly one … never a second or duplicated
  copy"), grounding ("no cut-out edge, no halo; rim light matches the key
  direction"), and face protection ("never waxy, plastic, or warped") belong in
  every prompt that preserves people.
- **Submission.** `omni_reference_task_type="edit"`, the muted master as
  `@Video 1` (an `asset://` video when people are visible), `resolution: "480p"`
  and boolean `draft: true` (standard 2.5 has no 4K), `generate_audio: false`,
  `watermark: false` only when the tool supports the parameter. Duration and
  ratio lock to the input — do not set them.
- **Temporal denoising with a no-ghosting guard.** Always pair the temporal
  instruction with "without introducing motion blur, ghosting, or trailing."

## Self-check checklist

1. The defect was **diagnosed by direct inspection** before writing the prompt;
   the prompt uses the diagnosis's exact vocabulary (not a guessed name).
2. `[Edit Goal]` is one sentence, begins "Edit @Video 1 to …", and names the
   dominant defect explicitly.
3. `[Source Video Role]` declares `@Video 1` the sole editing master.
4. `[Edit Scope]` names the change, pushes the dominant defect hard, and carries
   the "exactly one … never a second" quantity guard.
5. The discriminator line ("remove only the film-print … retain real surface
   texture") is present — or, for a localized tear/band, the
   reconstruct-from-surrounding-context framing is used instead.
6. Temporal denoising is paired with the no-blur/ghosting/trailing guard.
7. `[Content to Preserve]` locks identity, motion, timing, camera, and lighting.
8. Grounding and face-protection locks are present when people are in frame.
9. No `[Target Material Role]` section (single `@Video 1` source only).
10. Full fractional source timing, frame timestamps, cuts and audio tails are
    preserved; any derivative has current requirement evidence and explicit
    adaptation approval, with separate measurements, spans and hashes.
11. Rights recorded; the muted master is bound, as an `asset://` video when
    people are visible; the prompt ends with the silent audio block.
12. Full-span native Draft first; any additional partial probe is optional,
    explicitly approved and not delivery. Grain is judged at final resolution.
13. The Seedance output was **verified by direct inspection** (defect gone,
    content intact, no new artifacts) before splicing.
14. The caller's prompt review passed before submission; the saved original
    audio was muxed after measured timing and sync QA without hidden tail loss.
