# Cross-Modality Handoff Contracts

Before each handoff, recheck independent `project.md` approval and review modes and the source decision,
review, artifact, and upstream hashes. Run `studio_project.py sync`, then
complete the source stage with `studio_project.py stage <project> complete
<stage-id>` and start the destination stage. These steps apply in
`approve_for_me` and `ask_for_approval`. The receiving stage reads its inputs
from the synchronized Studio project and owning manifests rather than
reconstructing state from chat. A pre-Studio canvas project updates its canvas
stage entries, regenerates `index.html` and runs the canvas freshness check
instead.

## Canon to storyboard

Pass selected element paths, roles, approval states, hashes, and stable prompt
tokens. If an element is not approved, keep the dependent board in `draft` or
`review` and make video handoff ineligible.

## Storyboard to video

Pass the board's staging as text, never as an image. Elements are the identity
sources and the only images bound for identity; a storyboard grid, contact
sheet or board panel is never a Seedance reference, because panel numbers,
labels and the sketch look leak into the video. Translate each panel's
framing, blocking and end state into the shot prompt, bind the approved element
references, and choose one supported mode: R2V or T2V by default, I2V or FLF2V
only with a clean first (and last) frame rendered in the delivery look and
explicitly selected for that role.

## Static graphics to motion or video

Pass the selected raster path, editable source path, render-record path, output
hash, dimensions, and background/alpha intent. Use a solid-background derivative
only when the selected video mode benefits from a model reference. Keep exact
captions, taglines, prices, CTAs, end cards, and transparent overlays out of
generated footage and composite them with the selected motion/video tool. Never
substitute a white-matted file for a transparent delivery asset.

## Audio to video (when user requests lip-synced dialogue)

Use the exact same dialogue text in both prompts. Verify audio duration does not
exceed video duration, map dialogue to observed audio timing, pass the file as
`reference_audio`, and record its path and hash in the shot manifest. Skip this
handoff when the user has not requested lip-synced audio.

## Shot to assembly

Accept only mode-authorized approved takes. Pass local paths, hashes, actual
video-stream duration, resolution, frame rate, colour range and transfer,
audio properties and route (native, or picture only awaiting a post bed),
intended order, trim points, transition notes, and known defects. Do not treat
`succeeded` as creative approval. Assembly keeps the takes' original colours
unless the brief records a look.

## Draft to final generation

This handoff applies only when using drafts: strict mode, a requested draft, or
a concrete cost/uncertainty justification. Default mode otherwise generates at
the final target directly and proceeds to output sanity and selection.

Pass the selected 480p draft paths and hashes, its provider task ID, passing
review and selection records, exact prompt snapshot, ordered approved reference
hashes, requested audio behavior and delivery resolution. For multi-shot work,
include the reviewed draft assembly and picture/audio decisions. Record any
user override or verified operation constraint.

- A native Draft (`draft: true`) is promoted by its `draft_task_id` with only
  the output settings (`resolution`, `watermark`, optional chaining fields);
  the provider reuses its prompt, references, seed, duration and audio. Any
  input change means a new Draft, not a promotion.
- A plain 480p request is not promotable; its final is a fresh generation that
  may change picture, timing and audio.

Either way, register and preflight the final request as a new operation (a
hash-bound prompt report is required in strict mode or for explicit rules), then
inspect its output again (playback, speech-to-text, listening) and select it
before updating placed takes.

## Dependency invalidation

When a selected element, audio file, storyboard anchor, shot plan, confirmed project axis, or exact prompt changes,
identify every dependent artifact. Return affected downstream artifacts to
`review`; preserve their files, prompts, task IDs, hashes, and rejection history.
Run `studio_project.py sync` and `stage <project> reopen <stage-id>` in the same
stage change so the visible dependency state cannot lag behind the manifests
(a pre-Studio canvas project updates its statuses and regenerates `index.html`). Preserve earlier decisions while returning
affected artifacts to `review`.
