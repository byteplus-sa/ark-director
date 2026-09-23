# Cross-Modality Handoff Contracts

Before each handoff, recheck `project.md` approval mode and the source decision,
review, artifact, and upstream hashes. Update the source and destination stage
entries in the project canvas, regenerate and inspect `index.html`, and run the
source stage freshness check. These steps apply in `approve_for_me` and
`ask_for_approval`. The receiving stage reads its inputs from that synchronized
canvas and owning manifests rather than reconstructing state from chat.

## Canon to storyboard

Pass selected element paths, roles, approval states, hashes, and stable prompt
tokens. If an element is not approved, keep the dependent board in `draft` or
`review` and make video handoff ineligible.

## Storyboard to video

Treat elements as identity sources and storyboard panels as derivative
composition anchors. Require a mode-authorized panel selection backed by a
passing review and current source hashes, and choose exactly one supported
image mode: I2V, FLF2V, R2V, or T2V. Never
promote a multi-panel contact sheet as a clean video keyframe.

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
duration, resolution, frame rate, audio properties, intended order, transition
notes, and known defects. Do not treat `succeeded` as creative approval.

## Dependency invalidation

When a selected element, audio file, storyboard anchor, or exact prompt changes,
identify every dependent artifact. Return affected downstream artifacts to
`review`; preserve their files, prompts, task IDs, hashes, and rejection history.
Update the canvas statuses, decision sources, and locks, then regenerate and
inspect `index.html` in the same stage change so the visible dependency state
cannot lag behind the manifests. Preserve earlier decisions while returning
affected artifacts to `review`.
