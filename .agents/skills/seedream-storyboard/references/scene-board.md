# Scene Board

Focused reference for `seedream-storyboard`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities. Use it when the request is a
storyboard for a whole scene, not one hero panel.

- [Scene boards at a glance](#scene-boards-at-a-glance)
- [Choose the level for the scene](#choose-the-level-for-the-scene)
- [Which shots are key](#which-shots-are-key)
- [Author the panels](#author-the-panels)
- [Repair failed panels by editing](#repair-failed-panels-by-editing)
- [Boundaries](#boundaries)

## Scene boards at a glance

A scene board is the ordered set of panels for every shot in one scene, derived
from the scene's shot plan. The panel records live in `scenes/scene-NN/board.md`.
A scene-board assembly capability (named in prose only) derives and validates
that record, registers panel files, and builds the annotated sheet, the animatic
and the repair plan. This skill owns the panel prompts and the repair edits.

A scene board uses **separate panel images**, one file per panel, never a grid.
The annotated sheet is assembled from those files, so no grid, divider or panel
number is needed in the image, and a single panel can be edited as a whole file.

## Choose the level for the scene

Every scene has one level, recorded with a reason. **L2 is the default.**

| Level | Panels | Choose when |
| --- | --- | --- |
| L1 | One decisive panel per shot, key shots included | Quiet dialogue, montage, product beauty, showcase, text-led cards, a budget-limited pass |
| L2 | Key shots get start, peak and end panels; other shots get one | Most narrative, ad, micro-drama and music-video scenes |
| L3 | Key shots get sub-beat panels (anticipation, contact, consequence, reaction); other shots get one | Action, fights, chases, reveals that hinge on a state change, complex blocking, a scene whose turn is a physical event |

Choose a higher level only when the extra panels will change a decision about
staging, continuity or timing. A single shot may depart from the scene level with
a recorded reason (for example an insert that needs beats). State the panel count
and the generation cost before generating: an L2 key shot is three panels, and the
workspace default of three samples applies per panel unless a staging-only pass
asks for one.

## Which shots are key

A shot is key when it is the turn, has a camera move, changes blocking, crosses or
restates the axis, changes a prop, wardrobe or location state, or carries a light
cue. Start, peak and end states show the framing at the start and end of a move,
the decisive moment and the resulting state. A held shot whose only trigger is a
blocking or state change gets start and end.

## Author the panels

- Copy each panel's framing, featured subjects, size, angle, move, lens intent and
  light from its board record. Do not re-invent them.
- Write the panel prompt with the existing panel contract. Fill `Composition` and
  `Staging and continuity` from the record, including screen direction and the
  continuity carry (prop, wardrobe and damage state). Name a hand or shoulder by
  anatomy and frame side.
- Panels carry no text, labels, numbers or borders. The annotation lives only in
  the derived sheet.
- Bind the same approved element sheets in every state of one shot so identity
  holds between start, peak and end.
- Name files and prompt snapshots by the naming contract:
  `sNN_shNNN_pNNN_tNN_vNN.png` and `prompt_sNN_shNNN_pNNN_tNN_vNN.md`.

## Repair failed panels by editing

When review finds errors in some panels, repair those panels. Do not regenerate the
board.

| Finding | Repair |
| --- | --- |
| A local defect in an otherwise right panel (a prop, a hand, a count, an expression, a detail) | **Edit that panel** with `seedream_edit_image`, using a bounding box or point when the defect is local |
| A wrong beat, geography or axis in one panel | Regenerate that panel from a corrected prompt |
| A shared cause across most panels of a shot (element sheet, shot plan or prompt wrong) | Fix the cause, then regenerate that shot's panels |
| A cause that touches every panel (rare) | Regenerate the scene's panels, with a recorded reason |

Rules:

- **Smallest scope first**: panel, then shot, then scene.
- **One failed dimension per edit.** Use the revision contract in
  [Editing Failed Panels](editing-failed-panels.md): locked decisions, the single
  requested delta, acceptance criteria, known rejections and the invalidation scope.
- **Inputs**: the failed panel as `@Image 1` and the approved element sheet for any
  corrected identity or prop as `@Image 2`. The edit tool needs HTTPS URLs, so call
  `media_upload` or `media_presign` immediately before submitting.
- **Lineage**: the edit is a new version of the same panel (`_vNN+1`). The original
  stays on disk, marked rejected, with its prompt and hash. The new record keeps the
  parent file and hash, the edit prompt snapshot and the bounding box. The edit
  prompt is frozen beside its output and registered before submission like any paid
  operation.
- **Escalate** after two failed edits on the same dimension, or when the defect is
  structural. Edits fix local detail; they do not rebuild a composition.
- **Siblings are untouched**: their files, hashes and approvals do not change. Only
  the sheet page, the overview and the animatic segment that use the repaired panel
  go stale.
- **Cost**: an edit is a paid call. State the count and estimated cost before the
  first edit of a repair pass and respect the run budget. Use the lowest supported
  resolution for sketch drafts.

## What to expect from edits

Treat these as hypotheses to verify on each edit, not measured rates. Edits suit a
local removal. Additions at the frame edge and global geometry changes can drift
outside the target, so review the whole panel, not only the box, and prefer
regeneration for a geometry error. The edit tool needs a point or a bounding box, and
the registry needs approval evidence for the panel used as the edit source.

## Boundaries

A board, sheet, overview, animatic frame or edited panel is a planning artifact.
Never bind it as a Seedance reference in any mode or role. Carry the approved
staging into the shot prompt as text and bind only the element references the panel
used.
