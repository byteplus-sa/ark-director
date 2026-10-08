# Generation flow

Exact calls, parameters, records and checks for stages 6 to 10 of the
[orchestrator procedure](../SKILL.md). Observed on 2026-10-08 with the live
`ark-mcp` tools; recheck the tool schema before relying on a field.

## Project

Every submission lives in `projects/<name>/` with `project.md` (frontmatter
`approval_mode`, default `approve_for_me`), `task_ids.json` and the canvas
(`generate_showcase.py projects/<name> --init`). Use `.venv/bin/python` for the
repo scripts. Local state follows the repo naming contract: prompt snapshot
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

## Hash, review, register

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
   that `request_sha256`. Resolve CRITICAL and MAJOR findings; any changed
   prompt, parameter or reference byte changes the hash and needs a new review.
4. Re-run the same command with `--review`, `--capabilities`, the
   `--required-rule` values and `--write --register`:

   ```bash
   .venv/bin/python .agents/scripts/prepare_request.py \
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
frame) follows the same sequence: prompt snapshot, hash, review, registry entry
(`--model dola-seedream-5-0-pro-260628 --operation generate`, the user's photo
as a `reference_image` bound as `@Image 1`), submission, local copy, hash, an
inspection record and an approval decision. One sample is enough for a start
frame; record that choice and offer three samples when the user wants
alternatives. Only an approved start frame may be passed to Seedance.

## Submit a draft

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
  {task_id, persist_output: true}}}`. Observed render times: 1 to 2.5 minutes for
  a 6 to 10 second draft. After a timeout keep the ID and resume the same task.
- Never resubmit after an ambiguous timeout; reconcile first.

## Persist and inspect

The persisted video lives under `.artifacts/<id[:2]>/<artifact_id>.mp4`
(`seed_media_export_artifact` with a destination is disabled unless output roots
are configured). Copy it to the take path, check SHA-256 against the artifact
record, and read stream properties with `ffprobe`. Record artifact ID, bytes,
SHA-256, duration, resolution, whether an audio stream exists, and the usage
tokens (observed 58k to 96k completion tokens per 480p draft of 6 to 10 s;
estimated cost stays separate from confirmed billing).

Inspect by sampling frames, not a single thumbnail:

```bash
ffmpeg -v error -i take.mp4 -vf "fps=2,scale=200:-1,tile=8x3" -frames:v 1 sheet.png
ffmpeg -v error -ss 3.6 -i take.mp4 -frames:v 1 count_check.png
```

Check each QA item of the recipe against the sheet. Count people and copies on a
full-size frame at the timestamp the recipe names. For a native-audio take,
extract the track (`-vn -ac 1 -ar 16000`), upload it with `media_upload` and ask
`seed_audio_understand` what is audible; treat the answer as a flag for a human
listen, not proof.

## Decide and promote

- **Revise:** write Locked / Delta / Acceptance, change one thing, re-review,
  new operation ID and a new draft.
- **Promote:** `seedance_2_5_create_task` with `draft_task_id` (the Draft task ID,
  at most 7 days old) and only `resolution`, `watermark`, `return_last_frame`.
  Prompt, images, duration and audio come from the draft. Promotion renders
  1080p; for 720p run a new non-draft generation instead. Ask the user first and
  state the estimated cost (about five times the draft tokens). A promotion is a
  paid operation and is registered before it is submitted: operation ID
  `<draft operation>-promote`, the draft's prompt snapshot and references, params
  `draft_task_id`, `resolution`, `watermark`, so a timeout can be reconciled. Its
  review is the draft's (the prompt is unchanged). This path is not yet exercised
  in the probe project, so check the registry accepts the shape on first use.
  Check the draft's audio track first: the promotion reuses it.
- Apply the recipe's **Post** steps to the accepted master; keep the provider
  master untouched.

## Post steps

| Post | Tool and note |
| --- | --- |
| HUD, labels, UI text, city names, captions | Author with `html-graphic-render` (static) or HyperFrames (timed), composite with FFmpeg; text is never prompted into the clip |
| Split-screen stack (painting effects) | `ffmpeg -i person.mp4 -loop 1 -i painting.png -filter_complex "[0]scale=W:W[a];[1]scale=W:W[b];[a][b]vstack" -t D out.mp4`; the painting is a public-domain scan with source URL and SHA-256 recorded |
| Fisheye (animal ride) | FFmpeg `v360` flat-to-fisheye; untested, tune on the first take |
| Stepped 10 to 12 fps cadence (restyle looks) | Drop to the stepped rate then hold-frame back to 24 fps (`fps=12,fps=24`) |
| Ambience or sound effects bed | `seed_audio_generate`, "no voices, no music" last in the prompt, loudness-normalise, mux over the stream-copied picture; the bed is not frame-synced |
| Chained second clip (eyes-in destination) | A separate draft whose first frame is the destination image, joined in FFmpeg |

## Failure behavior

| Failure | Response |
| --- | --- |
| Photo does not fit the recipe | Say what is wrong; rebuild the start frame or ask for a better asset |
| Moderation rejection | Keep the original error as evidence; revise only with a recorded, authorized delta |
| Count or position drift | Revise through Locked / Delta / Acceptance; recipes note which counts run approximate |
| Native audio contains speech or music | Regenerate with audio off or add a post bed; do not claim the take is clean |
| Provider task failed | Evidence to review, not an automatic resubmission |
