# Production canvas contract

Use one project-level `showcase.json` and generated `index.html` throughout a
production. The manifest is the editable source of truth; the HTML is the
portable, read-only snapshot used to understand and review current state.

## Lifecycle schema

Add a `canvas` object and assign every section to one production stage:

```json
{
  "title": "Project production canvas",
  "canvas": {
    "approvalContractVersion": 1,
    "currentStage": "canon-elements",
    "stages": [
      {
        "id": "brief-development",
        "label": "Brief and development",
        "status": "complete",
        "summary": "Audience, format, constraints, and directing choices are locked.",
        "sources": [
          {"path": "project.md", "kind": "brief", "label": "Project brief"}
        ]
      },
      {
        "id": "scene-breakdown",
        "label": "Scene and production breakdown",
        "status": "complete",
        "sources": [
          {"path": "scenes/scene-01/scene.md", "kind": "manifest", "label": "Scene 01"}
        ]
      },
      {"id": "canon-elements", "label": "Canon and elements", "status": "review", "sources": []},
      {"id": "storyboard-visual-plan", "label": "Storyboard and visual plan", "status": "pending", "sources": []},
      {"id": "audio-preparation", "label": "Audio preparation", "status": "pending", "sources": []},
      {"id": "shot-generation", "label": "Shot generation", "status": "pending", "sources": []},
      {"id": "assembly-review", "label": "Assembly and review", "status": "pending", "sources": []},
      {"id": "delivery", "label": "Delivery", "status": "pending", "sources": []}
    ]
  },
  "sections": [
    {
      "id": "elements",
      "title": "Elements",
      "stage": "canon-elements",
      "kind": "grid",
      "cards": []
    }
  ]
}
```

The eight stage IDs and their order are fixed:

1. `brief-development`
2. `scene-breakdown`
3. `canon-elements`
4. `storyboard-visual-plan`
5. `audio-preparation`
6. `shot-generation`
7. `assembly-review`
8. `delivery`

Statuses are `pending`, `active`, `review`, `approved`, `complete`, `blocked`,
or `skipped`. Earlier stages must be `approved`, `complete`, or `skipped` before
the current stage advances. A future optional stage may be marked `skipped`.

New canvases use `approvalContractVersion: 1`. The generator reads
`approval_mode` from `project.md` and displays the effective mode and whether
it was explicitly set. An omitted mode defaults to `approve_for_me`. The
effective mode and `project.md` hash are embedded in the HTML snapshot, so a
mode change makes `--check --stage` fail until the page is regenerated. Existing
canvases without a contract version remain readable without inventing earlier
approval evidence.

For a version 1 canvas, `assembly-review` cannot be `approved` or `complete`
without a picture lock and, unless `audio-preparation` was skipped, an audio
lock. `delivery` additionally requires a final master lock. Each lock in
`canvas.stages[].locks` records `decision_id`, `decision_sha256`, `result`, `artifact_path`,
`artifact_sha256`, `review_path`, `review_sha256`, `actor`, and `reason`.
The decision JSON, accepted artifact, and review must also be listed in that
stage's `sources`. The canvas checkpoint verifies the file hashes and source
links. The decision service writes locks and sources together; do not add a
lock by editing JSON alone.

For a completed element, storyboard, audio, or shot stage on a version 1
canvas, every selectable asset must have a registered selected variant with
approved `selection_evidence`. The checkpoint verifies the selected media,
decision, passing review, upstream hashes, and stage source links. Active and
review stages can show unfinished candidates while the agent or user decides.

## What belongs on the canvas

Keep the page useful as a working production surface, not only as a final
gallery:

| Stage | Required canvas evidence |
| --- | --- |
| Brief and development | `project.md`, treatments, locked axes, constraints, unresolved decisions |
| Scene breakdown | scene/shot manifests, beat summaries, cast/location/prop/audio inventory |
| Canon and elements | all element variants, exact prompt snapshots, manifests, hashes, recommendations and selections |
| Storyboard and visual plan | panel variants, storyboard prompts, bound canon, continuity state and panel eligibility |
| Audio preparation | audio variants, exact prompts, transcript/dialogue timing, duration and inspection results |
| Shot generation | every take, exact prompt, ordered element bindings, task provenance, media properties and QA status; when a style/grammar reference pin (or other watchable reference video) exists, that pin and each generated take must appear as playable players on this stage in the same `kind: "takes"` group |
| Assembly and review | approved inputs, edit versions, comparison renders, notes, continuity and audio checks |
| Delivery | masters, proxies, captions/localization state, hashes, delivery metadata and final approval state |

Use stage `sources` for briefs, manifests, data, and review records that do not
belong in a media section. Use stage-tagged `grid`, `takes`, `table`, or `panel`
sections for visual and audio artifacts. A generated media card should point to
its immutable prompt snapshot with `promptFile`; the generator embeds the exact
file contents so the portable HTML does not depend on browser file access. Each
entry in a card's `refs` list includes the referenced element's project-relative
`path`, allowing the checkpoint to detect changed element content.

### Shot-generation video players (`kind: "takes"`)

The renderer builds playable video only from `groups[].takes[]` with
`media: { "type": "video", "src": "<project-relative>.mp4" }`. Do **not** author
`kind: "takes"` with flat `cards` or a string `media` path — those shapes render
an empty section (no `<video>` players).

When a pin or other reference video is in scope for review:

1. Keep the pin listed under `brief-development` if useful for intake history.
2. On `shot-generation`, put the **pin and every generated take in one
   `groups[]` entry** so synchronized "Play all" comparison works.
3. Point take `promptFile` / pick-winner fields (`id`, `manifest`, `filename`)
   at the shot artifacts; the pin take is comparison-only (no pick-winner).
4. Regenerate `index.html`, open or `--serve` it, and confirm both players are
   visible before calling the stage ready for user review.

See [schema.md](schema.md#kind-takes-video-take-comparison-with-synchronized-playback--pick-winner)
for the exact JSON shape.

## Stage update protocol

At project initialization, create `project.md`, then scaffold the full
eight-stage canvas and generate `index.html` without overwriting existing work:

```bash
.venv/bin/python .agents/skills/showcase-html/scripts/generate_showcase.py \
  projects/<project> --init --open
```

For each active stage:

1. Read `showcase.json` immediately before editing it.
2. Update the current stage status, summary, sources, and stage-tagged sections.
3. Preserve earlier stages and their rejected or superseded variants. Add every
   candidate review through the card or take's `reviewPath`, and keep decision
   and review files in stage `sources` after a selection. The rendered canvas
   shows selected variants with their actor, reason, and review/decision links.
4. Regenerate the HTML with the expected stage:

```bash
.venv/bin/python .agents/skills/showcase-html/scripts/generate_showcase.py \
  projects/<project> --stage <stage-id> --open
```

5. Before declaring the stage complete, run the read-only freshness check:

```bash
.venv/bin/python .agents/skills/showcase-html/scripts/generate_showcase.py \
  projects/<project> --check --stage <stage-id>
```

The generated page embeds the manifest SHA-256, `project.md` hash and effective
approval mode, plus the hashes of every local source referenced by the canvas
and its sections. The check fails when the stage does not match, a source is
missing or changed, a required lock is missing or stale, or the HTML predates a
change. Fix the evidence or regenerate the HTML; do not mark the stage complete
while the check fails. This applies in both approval modes. In
`approve_for_me`, the agent updates and inspects the page and runs this check
without waiting for a routine user selection.

When selections, stage locks, or mode changes are saved through the generator,
it refreshes the HTML after the transactional write. A failed refresh is
reported separately from the applied decision and must be resolved before
leaving the stage. In `ask_for_approval`, the user can choose variants through
`--serve`; a stage lock after an explicit user choice uses `--stage-decision`
with the recorded user instruction. The agent uses decision files with passing
review evidence for autonomous selections and stage locks.

## Review fallback

The production canvas is required for project workflows. Use `media-review`
only when the browser or HTML generator is unavailable, or when the user
explicitly requests an OS-native player. Record that fallback as unavailable
canvas evidence, restore the synchronized HTML before the stage exit, and never
treat an OS-player review as satisfying the canvas checkpoint.
