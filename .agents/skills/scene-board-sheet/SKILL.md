---
name: scene-board-sheet
description: >-
  Assemble and time a scene's storyboard from existing sketch panels. Derives the
  scene board record from the shot plan at a per-scene level (L1, L2 or L3, L2 by
  default), validates it, registers generated and edited panel files with lineage,
  plans panel-only repairs so only failed panels are edited, and builds annotated
  sheet pages, a floor-plan overview, a timed animatic and a static review page.
  Use for scene-based storyboards that must be granular and detailed, scene board
  review sheets, animatics, stale-board checks after a shot plan or panel change,
  and repair planning for failed panels. Planning and assembly only: it never
  generates images, approves a panel, or produces a Seedance reference.
---

# Scene Board Sheet

Turn a scene's shot plan into a granular, reviewable storyboard and keep it in
step as panels change. The unit is the scene: one record, one sheet, one animatic.
This skill assembles and checks; it never calls a generation tool and never
approves a result.

## Boundary

| Need | Where it lives |
| --- | --- |
| Panel prompts, panel generation, Seedream image edits | `seedream-storyboard`, `seedream-edit` |
| The shot plan this board reads | `seedance-shot-design` |
| Exact static graphics (the sheet is a deterministic render) | `html-graphic-render` |
| Blocking geometry for Seedance | `tig-blocking-map` |
| Stage order, approval modes, Studio and spending gates | `film-production` and the production policy |

These are prose pointers for the calling agent. This skill reads files and writes
files under the scene folder; the caller owns tools, spending and approval.

## Boundary rule

A board, sheet page, overview, animatic or edited panel is a planning artifact.
Never bind any of them to a Seedance request, in any mode or role
(`board.animatic_review_only`). `board.md` and every derived record state
`bind_to_seedance: false`. `check` fails when a request in `task_ids.json`
references a board file by hash, by a registered panel path, or by a path under
`scenes/scene-NN/board/`. That check lives in this skill; the shared request
validator does not know about boards, so run `check` before submitting a scene's
shots.

## Levels

The level is chosen per scene and recorded with a reason. **L2 is the default.**

| Level | Panels |
| --- | --- |
| L1 | One panel per shot |
| L2 | Key shots get start, peak and end panels; other shots get one |
| L3 | Key shots get sub-beat panels (anticipation, contact, consequence, reaction, or the shot's `sub_beats`); other shots get one |

Choose L1 for quiet dialogue, montage, product beauty, showcase and budget-limited
passes; L2 for most narrative, ad, micro-drama and music-video scenes; L3 for
action, fights, chases, state-change reveals and complex blocking. A shot may
override the scene level with `--override SHOT=LEVEL=REASON`; an override forces the
shot to count as key.

A shot is key when it is the turn, has a move, sets `blocking_change`, sets
`axis_crossed`, lists a `state_change`, or carries a light cue. At L2 a key shot
whose only triggers are `blocking_change` or `state_change` gets start and end; any
other key shot gets start, peak and end. Non-key shots always get one panel unless
overridden. The board status follows the shot plan's status (`draft` unless the plan
says `ready`).

## Input and output

Input: a project directory, a scene whose `scene.md` holds a `## Shot plan` section
with a fenced yaml `shot_plan` block (see the shot plan format), and for assembly
the registered panel files.

Output under `scenes/scene-NN/`:

| File | Purpose |
| --- | --- |
| `board.md` | The board record: level, reason, one record per panel, optional `layout` |
| `sNN_shNNN/sNN_shNNN_pNNN_tNN_vNN.png` | Panels (existing naming); an edit adds a new `vNN` |
| `board/sheet/sNN_sheet_pgNN_vNN.{html,png}` and `.sheet.json` | Annotated sheet pages and their render plans |
| `board/overview/sNN_overview_vNN.{html,png}` | Floor plan from the `layout` block |
| `board/animatic/sNN_animatic_vNN.mp4` and `.animatic.json` | Timed review video |
| `board/repair/<panel>_edit_vNN.md` | Revision contract for one edit |
| `<project>/review/scene-NN-board.html` | Static review page |

The schema is `.agents/contracts/schemas/scene-board.schema.json`. Derived files are
rebuilt, never hand-edited, and carry source hashes.

## Commands

Run from the repository root. Every command prints JSON; errors exit 2, and `check`
exits 1 when it finds an error.

```bash
uv run python .agents/skills/scene-board-sheet/scripts/scene_board.py <command> <project> <scene> [options]
```

| Command | Does |
| --- | --- |
| `init` | Derive `board.md` from the shot plan. `--level L1\|L2\|L3` (default L2), `--level-reason`, `--override SHOT=LEVEL=REASON`, `--style`, `--aspect`, `--overwrite` |
| `rebase-plan` | Follow a changed shot plan: re-derive the panels, carry registered files, versions, statuses and decisions over by panel id, mark panels whose plan facts changed `needs_edit`, and list orphaned files. `init --overwrite` is refused once panels are registered |
| `check` | Schema, shot-plan hash, panel coverage, duration sums, field agreement with the plan, file presence and hashes, version heads, approvals bound to the panel file, and board files bound as request references |
| `status` | `plan_stale`, panel lifecycle, and which sheet pages (including pages not yet rendered), overview and animatic segments are stale |
| `register-panel <panel>` | Record a generated or edited panel file. `--file`, `--edit-of` (the previous file), `--dimension`, `--bbox`, `--prompt-file`, `--task-id` |
| `mark <panel> --status` | Set `review`, `needs_edit`, `rejected`, or `approved`. Approval needs a panel in `review`, an unchanged file, and `--decision` pointing at the recorded decision file; the decision is bound to the panel's hash |
| `repair-plan` | Choose the repair scope and write revision contracts. `--panels`, `--cause local\|beat\|shared`, `--dimension` (required for an edit), `--delta`, `--accept`, `--bbox` |
| `sheet` | Write sheet page sources and render plans. `--pages 1,3` writes only those pages; `--font` names a local font family to require |
| `render-sheet` | Render the pages with the renderer script you name: `--renderer <path to html-graphic-render's render_html.py>`, optional `--pages` |
| `overview` | Write the floor plan sources when `board.md` has a `layout` block |
| `animatic` | Build the timed MP4 with FFmpeg. `--size` defaults from the board aspect ratio; `--audio` is padded or trimmed to the picture length and its hash is recorded |
| `review-page` | Write the static review page under `review/` |

## Procedure

1. **Read the shot plan.** A board follows the plan; it never invents camera, light
   or timing facts. If the plan is `draft`, the board stays `draft`.
2. **Choose the level** for the scene and record the reason. Default to L2.
3. **`init`**, then **`check`**. Fix schema or plan disagreements in the plan, not
   by editing panels to match a wrong board. When the shot plan changes later, run
   **`rebase-plan`** instead of re-initializing.
4. **Generate the panels** as separate images (the storyboard capability owns the
   prompts and the Seedream calls), then **`register-panel`** each file. Panel
   prompts carry no text.
5. **`sheet`**, then **`render-sheet`**, and optionally **`overview`** and
   **`animatic`**. Build the **`review-page`** for the owner. Rejected panels stay on
   the sheet and in the animatic with their status until a replacement is
   registered.
6. **Review** the scene (below). Selection and approval follow the project's
   approval mode and the validated decision writer; this skill records the decision
   file with `mark --status approved`.
7. **Repair** failed panels (below), then rebuild only what `status` lists as stale.
8. **Hand off** by writing each approved panel's staging, blocking, eyelines, screen
   direction and camera intent into the shot prompt text, and binding only element
   references.

## Review

After each panel passes review, look at the scene as a sequence:

| Check | Looks for |
| --- | --- |
| C1 Plan fidelity | Every panel matches its shot plan row |
| C2 Screen direction | Travel and confrontation axes hold across cuts |
| C3 Eyelines | Looks match across adjacent panels |
| C4 Light continuity | One declared source set; key sides follow the plan |
| C5 State continuity | Props, wardrobe and damage carry correctly |
| C6 Rhythm | Animatic timing matches the energy level; the turn shot differs in length |
| C7 Variety | The shot plan's variety rules still pass when seen as images |
| C8 Hygiene | No numbers, labels, borders or sketch texture in anything that goes to video |

## Repair

Fix failed panels, not the board.

1. **`mark <panel> --status needs_edit`** for each failed panel.
2. **`repair-plan`** picks the smallest scope: an **edit** for a local defect in an
   otherwise right panel, **regenerate the panel** for a wrong beat, geography or
   axis (`--cause beat`) or after two failed edits on the same dimension, and
   **regenerate the shot's panels** for a shared cause (`--cause shared`) or when
   most panels of a shot of three or more failed. It writes a revision contract per
   edit and lists the untouched panels and the stale artifacts.
3. **Edit** with `seedream_edit_image`: the failed panel as `@Image 1`, the approved
   element sheet as `@Image 2` when identity or a prop changes, HTTPS URLs from
   `media_upload` or `media_presign` immediately before the call, and a bounding box
   for a local defect. One failed dimension per edit. An edit is a paid call: state
   the count and cost first and register the operation before submitting.
4. **`register-panel --edit-of <previous file>`** with the new version. The original
   is kept and marked rejected; the new record keeps the parent hash.
5. **`status`**, then rebuild only the listed sheet pages, overview and animatic.

Sibling panels keep their files, hashes and approvals.

## Dependencies and limits

- `scene_board.py` needs `jsonschema` and `ruamel.yaml` (the workspace
  environment), FFmpeg for the animatic, and Chrome or Chromium for rendering. It
  never imports another skill: pass the renderer path to `render-sheet`.
- The sheet is 3840 x 2160, six panels per page, with the shot plan hash in the top
  bar and the cut points in the bottom bar. Long text is shortened to a fixed length
  and the shortened text is the exact copy the renderer verifies. Pass `--font` only
  with a project-local font declared in the sheet stylesheet.
- Derived files and `board.md` are written atomically and never through a symlink, but
  there is no locking: serialize edits to a scene's board between agents, as for other
  shared state.
- The system FFmpeg may lack `drawtext`, so the animatic carries no burned-in labels.
- The overview draws shapes and a legend from the `layout` block. It is a review aid,
  not a Seedance control diagram.
- Hashes catch changes after registration; they do not judge image quality.

## Checklist

Before reporting a scene board ready, confirm:

1. The level and its reason are recorded, and any per-shot override has a reason.
2. `check` passes with no error and `status` lists nothing stale.
3. Every panel is registered with its file, hash and prompt snapshot, and approved
   panels carry a decision record.
4. Repairs used the smallest scope, an edit named one failed dimension, and no
   sibling panel changed.
5. No board file is bound to a Seedance request, and the handoff is prompt text plus
   element references only.
