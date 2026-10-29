# Generation flow

Exact calls, parameters, records and checks for stages 6 to 10 of the
[orchestrator procedure](../SKILL.md). Recheck the live `ark-mcp` tool schema
before relying on a field.

## Project

Every submission lives in `projects/<name>/` with `project.md` (frontmatter
independent `review_mode: default` and `approval_mode: approve_for_me`),
`task_ids.json` and, once a take
exists, the Studio project (`studio_project.py sync`). Use `uv run python` for
the repo scripts. Local state follows the repo naming contract: prompt snapshot
`prompt_<stem>.md` beside the output, `<stem>.mp4` for the take.

## Start assets

| Need | How |
| --- | --- |
| Photo as `first_frame`, `last_frame` or `reference_image` | `ark_job_submit` with `tool_name: "media_upload"`, `arguments.input: {media_type, mime_type, file_path, key_prefix, expires_in_seconds}`. The result URL is a signed, expiring transport value: pass it into the request, never write it to a file or a message |
| Missing start frame (giant frame, destination image, water wall, palm-up frame) | `seedream_generate_image` through `ark_job_submit`, the user's photo as `@Image 1` bound for identity only, size matching the target ratio. Do not pass `output_path` through the job |
| Source clip for `v2v-restyle` | Follow the video-to-video inputs contract and `seedance-restyle`; the muted master and Virtual Portrait identity anchors replace the steps below |

A generated or edited image is not usable as a reference until it is saved
locally, hashed, inspected and approved: write a candidate review (criteria,
observations, limitations, recommendation), a decision record and a manifest
with `selection_evidence`. `prepare_request.py --ref path:role:manifest`
rejects an unapproved reference.

## Provider rules

Verify current model and operation capabilities against the live tool schema
and authoritative provider documentation. Preserve documented unsupported
flags; unknown support is not permission to submit. Recipe validation is
separate from capability support (see [evidence status](evidence-status.md)).

- **Person-reference restrictions.** Person face and body crops are subject to
  provider privacy restrictions (`InputImageSensitiveContentDetected.PrivacyInformation`).
  Keep the error and diagnose a rejection before any further submission.
  First-frame alternatives in the recipes require their own capability and
  rights checks; do not change roles to bypass a restriction.
- **Last-frame-only is rejected.** Require `first_frame` with `last_frame`;
  `earth-zoom` and `lidar` include a generated first frame plus the photo as the
  last frame. Verify identical first/last image support for `cutout`.
- **Ratio.** A first frame locks the ratio, so omit `ratio`. A route with no
  first frame must set `ratio`.
- **Audio review.** Review the current track against the requested sound design.
  Respect output-audio moderation (`OutputAudioSensitiveContentDetected.PolicyViolation`);
  a rejection is not permission for an automatic retry. Use native audio off
  and a separate post bed when that is the selected audio workflow.
- **Video-to-video.** Restyle, edit and extend inputs that show a realistic
  person, generated or real, are rejected with `PrivacyInformation` unless each
  person is bound as an `asset://` Virtual Portrait or authorized asset.
  Verify current asset and operation support. Every new 2.5 test, including an
  edit, uses `resolution: "480p"` and boolean `draft: true`. Resolve capability
  or transport conflicts before submission, never by dropping `draft`.
- **Lettering review.** Check generated surfaces for unwanted lettering; exact
  readable overlays remain a post-production requirement.
- **Count review.** Preserve requested counts at every timestamp and count on
  full-size frames of the current take; report the numbers found.
- **Timing review.** Compare current cut timing and cadence with the recipe.
  Use deterministic post steps when exact timing is required.

## Hash, review, register

Default review mode freezes the prompt, resolves current capabilities, checks
intent, hashes, bindings, canonical approvals, rights and generation consent inline, and
registers with `prepare_request.py --write --register --capabilities ...`.
Use native `resolution: "480p"` and boolean `draft: true`; omit `--review` and
checklist-rule flags unless explicitly needed. No full checklist report or
fake passing review is created. Inspect the actual output and retain short
candidate/final sanity records for the existing decision writer.

### Strict or explicitly requested detailed review

The following detailed checklist applies to strict review; the native Draft
parameters apply in both modes. Explicit `--required-rule` values require genuine matching
review evidence in either mode; a supplied failing or stale report always blocks.
Review is bound to the request hash, so the order is hash first.

1. Write the prompt to its snapshot path and resolve capability evidence into
   `capabilities/<name>.json` (model, source, `verified_at`, parameter schemas,
   `reference_roles`, `max_references`,
   `supports_first_frame_with_reference_images`). First-frame and reference
   images cannot be mixed.
2. Run `prepare_request.py` with the arguments below but **without** `--review`,
   `--write` and `--register`. It validates the bindings and prints
   `request_sha256`; nothing is written.
3. Run `prompt-review` bound to that hash and write the review record with
   that `request_sha256`. Review inline by default; use a sub-agent only when
   the user explicitly requests sub-agent prompt review for the project or
   specific generation. Resolve CRITICAL and MAJOR findings; any changed
   prompt, parameter or reference byte changes the hash and needs a new review.
4. Re-run the same command with `--review`, `--capabilities`, the
   `--required-rule` values and `--write --register` (a Studio project needs no
   canvas for this; a pre-Studio canvas project needs its current `showcase.json`
   and `index.html`):

   ```bash
   uv run python .agents/scripts/prepare_request.py \
     --project projects/<name> --asset s01_sh010_t01_v01 \
     --prompt scenes/scene-01/s01_sh010/prompt_s01_sh010_t01_v01.md \
     --model dreamina-seedance-2-5-260628 --operation generate \
     --param 'resolution="480p"' --param duration=10 \
     --param generate_audio=false --param watermark=false --param draft=true \
     --expected-output scenes/scene-01/s01_sh010/s01_sh010_t01_v01.mp4 \
     --operation-id seedance-s01-sh010-t01-v01 --schema-version 2 \
     --ref scenes/scene-01/s01_kf01_v01.png:first_frame:scenes/scene-01/keyframe.md \
     --review reviews/review_s01_sh010_t01_v01.json \
     --capabilities capabilities/seedance-25-draft-480p.json \
     --required-rule asset.visible_consistency \
     --required-rule narrative.observable_event \
     --required-rule references.ordered_bindings \
     --write --register
   ```

   JSON values are quoted inside `--param`; paths for `--review`,
   `--capabilities` and `--ref` are project-relative. Omit `ratio` for a
   first-frame route (it locks to the image) and set it for `reference_image`.
   The request hash covers prompt bytes, parameters and ordered reference
   hashes and roles; a changed byte needs a new review.

   Shot rules: each recipe carries an explicit per-shot camera plan, so record
   that exemption in the shot manifest and do not pass `shot.plan_bound`,
   `shot.variety` or `shot.axis_carry` as required rules; the reviewer records
   them as `not_applicable` with the exemption as the reason.

### Start frames are operations too

A Seedream start frame (giant frame, destination image, water wall, palm-up
frame) follows the same sequence: prompt snapshot, hash, mode-appropriate preflight, registry entry
(`--model dola-seedream-5-0-pro-260628 --operation generate`, the user's photo
as a `reference_image` bound as `@Image 1`), submission, local copy, hash, an
inspection record and an approval decision. One sample is enough for a start
frame; record that choice and offer three samples when the user wants
alternatives. Only an approved start frame may be passed to Seedance.

## Submit a draft

This path applies in both review modes. New Seedance 2.5 generations require
native Draft before selected promotion. The state transitions,
provider-ID persistence, polling and reconciliation below apply in either mode.

Move the operation to `submitting` before the call
(`operation_store.transition_operation`), then:

```text
ark_job_submit {tool_name: "seedance_2_5_create_task",
  arguments: {input: {prompt, images: [{kind: "url", role: "first_frame", url}],
    resolution: "480p", duration, ratio?, generate_audio, watermark: false,
    draft: true}}}
```

- The job result carries the provider task ID (`cgt-...`). **Wait for the job to
  finish and register that ID**; the provider ID is write-once, so do not store
  the Ark job ID in its place. Keep the Ark job ID in `extensions.ark_job_id`.
- A draft is a normal 480p billing; the model has no `camera_fixed` or seed
  field. Express a locked camera in the prompt.
- Poll with `ark_job_submit {tool_name: "seedance_get_task", arguments: {input:
  {task_id, persist_output: true}}}`. After a timeout keep the ID and resume
  the same task.
- Two images use roles `first_frame` and `last_frame` and no `ratio`; the first
  frame locks it.
- Never resubmit after an ambiguous timeout; reconcile first.

## Persist and inspect

The persisted video lives under `.artifacts/<id[:2]>/<artifact_id>.mp4`
(`seed_media_export_artifact` with a destination is disabled unless output roots
are configured). Copy it to the take path, check SHA-256 against the artifact
record, and read stream properties with `ffprobe`. Record artifact ID, bytes,
SHA-256, duration, resolution, whether an audio stream exists, and the usage
tokens (estimated cost stays separate from confirmed billing).

Inspect by sampling frames, not a single thumbnail:

```bash
ffmpeg -v error -i take.mp4 -vf "fps=2,scale=200:-1,tile=8x3" -frames:v 1 sheet.png
ffmpeg -v error -ss 3.6 -i take.mp4 -frames:v 1 count_check.png
```

Default mode uses actual playback and brief-focused sanity; strict mode checks
each QA item of the recipe. Sheets support but do not replace temporal
inspection or actual listening. Count people and copies on a
full-size frame at the timestamp the recipe names. For a native-audio take,
extract the track (`-vn -ac 1 -ar 16000`), upload it with `media_upload` and ask
`seed_audio_understand` what is audible; treat the answer as a flag for a human
listen, not proof. Check for music, singing and speech even though the prompt
forbade them.

## Decide and promote

- **Revise:** write Locked / Delta / Acceptance, change one thing, run
  mode-appropriate preflight, and use a new operation ID at the appropriate target.
- **Promote:** first verify current native Draft/promotion support in the live
  tool/model/operation. A 480p output alone is insufficient. If unavailable,
  resolve the capability or transport conflict before submitting; never silently
  replace native Draft with a plain generation. For a supported native promotion, `seedance_2_5_create_task`
  with `draft_task_id` (the Draft task ID,
  at most 7 days old) and only `resolution`, `watermark`, `return_last_frame`.
  Prompt, images, duration and audio come from the draft. Promotion renders
  1080p in the documented path; revalidate these constraints.
  Resolve a delivery target the promotion path cannot provide with an authorized
  post-processing route or an explicit user decision; new Seedance 2.5 generations
  have no skip-draft override.
  Follow existing generation authorization and project approval mode;
  request authorization only when the final operation exceeds that scope. A promotion is a
  paid operation and is registered before it is submitted: operation ID
  `<draft operation>-promote`, the draft's prompt snapshot and references, params
  `draft_task_id`, `resolution`, `watermark`, so a timeout can be reconciled. Its
  prompt review may reuse the unchanged prompt findings, but its complete final
  request hash, parameters, references and current capability evidence need a
  fresh mode-appropriate preflight (and a report in strict mode or when
  explicitly required); inspect and select the final output again. Check the
  registry accepts the shape on first use.
  Check the draft's audio track first (the promotion reuses its audio setting),
  then check the final's track again: final audio is not byte-identical to the
  draft's.
- Apply the recipe's **Post** steps to the accepted master; keep the provider
  master untouched.

## Post steps

| Post | Tool and note |
| --- | --- |
| HUD, labels, UI text, city names, captions | Author with `html-graphic-render` (static) or HyperFrames (timed), composite with FFmpeg; text is never prompted into the clip |
| Split-screen stack (painting effects) | `ffmpeg -i person.mp4 -loop 1 -i painting.png -filter_complex "[0]scale=W:W[a];[1]scale=W:W[b];[a][b]vstack" -t D out.mp4`; the painting is a public-domain scan with source URL and SHA-256 recorded. From a 9:16 clip: crop a 9:8 band (`crop=iw:iw*8/9:0:Y`, Y chosen so the head stays in), scale it to 720x640, stack it over a 720x640 painting panel for a 720x1280 result |
| Fisheye (animal ride) | For a 9:16 clip: scale to 720x1280, pad to a 1280 square, `v360=input=flat:output=fisheye:ih_fov=90:iv_fov=90:h_fov=90:v_fov=90:w=1280:h=1280`, black mask outside a circle of radius 630, crop the centre 720x1280. Review the chosen FOV and centre magnification on the current composite; the circle is wider than the frame, so black arcs show only at top and bottom |
| Stepped 10 to 12 fps cadence (restyle looks) | Drop to the stepped rate then hold-frame back to 24 fps (`fps=12,fps=24`) |
| Ambience or sound effects bed | `seed_audio_generate`, "no voices, no music" last in the prompt, loudness-normalise, mux over the stream-copied picture; the bed is not frame-synced |
| Chained second clip (eyes-in destination) | A separate draft whose first frame is the destination image, joined in FFmpeg |

## Failure behavior

| Failure | Response |
| --- | --- |
| Photo does not fit the recipe | Say what is wrong; rebuild the start frame or ask for a better asset |
| Moderation rejection | Keep the original error as evidence; revise only with a recorded, authorized delta |
| Count or position drift | Revise through Locked / Delta / Acceptance using the current take's observed discrepancy |
| Reference image rejected (privacy detection) | Keep and diagnose the error; any alternative needs current capability and rights checks, never a restriction bypass |
| Last-frame-only rejected | Add a generated first frame; verify support before using the same file as first and last frame |
| Output audio rejected | Keep the error as evidence; retake with a recorded audio-sentence change or `generate_audio: false` |
| Native audio contains speech or music | Regenerate with audio off or add a post bed; do not claim the take is clean |
| Provider task failed | Evidence to review, not an automatic resubmission |
