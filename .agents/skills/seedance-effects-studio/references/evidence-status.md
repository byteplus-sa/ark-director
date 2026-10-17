# Evidence status

Recipes are written from the observed example footage of each effect and then
tried on invented subjects at 480p. That shows a recipe can produce the effect,
or fail to, on one subject at one resolution; it does not guarantee the effect
on other photos, other subjects, other resolutions or real people. Treat every
recipe as a starting point and check its QA list on each draft.

## Confidence levels

| Level | Meaning | Say to the user |
| --- | --- | --- |
| Verified in a limited probe | The signature look has been produced at least once on an invented subject at 480p; defects such as approximate counts, leaked sound or small timing drift are possible | "Tried on an invented subject only; your photo may differ" |
| Unverified | No take has passed review (`canvas`, `palette`, `lsd`); the recipe is a hypothesis | Say so before any paid run and offer `comic` or a `seedance-restyle` catalog style |

A template amended after a probe is a hypothesis until a new draft shows the
change. Never present either level as proof on the user's photo.

## Recurring failure modes

These hold across effects; each recipe's Risks and QA lists carry the specifics.

- Counts of people, copies, objects and panels drift upward or land
  approximate. State the count at every timestamp and count on a full-size
  frame.
- Native audio can leak music, singing or stray voices despite the audio
  sentence. Check the track, or generate silent and add a bed in post.
- Described tickets, panels, screens and signs invent lettering and digits.
  Name plain surfaces and add readable overlays in post.
- Prompted cut times drift and cuts closer than about 0.8 s merge. Finish rapid
  cuts and stepped cadence in post.
- Whole-clip restyle effects may restyle only part of the frame.

Provider rules that affect routing are in
[generation-flow.md](generation-flow.md#provider-rules).

## Not covered by the probes

- 720p or 1080p finals and the draft promotion path.
- A user's own photo (a real face may be refused as a start frame; see the
  rights step), a second subject and branded products.
- Source clips with people bound as `asset://` assets, and edit-route draft
  mode.
- Reference-image routes with a user-supplied non-crop reference.
- The chained second clip for `eyes-in`.

## Tooling findings

- Reference images and start frames need `--ref` evidence: an approved manifest,
  a candidate review and a hash-bound decision.
- The provider task ID is write-once in the registry; register the `cgt-` ID, not
  the Ark job ID.
- `camera_fixed` and a seed are not exposed by `seedance_2_5_create_task`.
- `seed_media_export_artifact` with a destination path is disabled without
  configured output roots; copy from the artifact store path.
