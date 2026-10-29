# Review And Selection

Focused reference for `seedream-storyboard`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [12. Review the board](#12-review-the-board)
- [13. Present variants and capture selection](#13-present-variants-and-capture-selection)

### 12. Review the board

Evaluate every individual panel. For multi-panel separate-images boards, also
evaluate the ordered contact sheet. For multi-panel single-image grid boards,
evaluate the whole grid image for both per-panel quality and cross-panel flow.
For a one-panel board, inspect its actual output; default review mode generates
one variant unless the user requests a count, while strict uses three. Compare
multiple variants only when they exist. A comparison sheet is a review artifact,
not another storyboard panel and never a video input. Three-panel layouts are
not three stochastic variants.

Default review mode records short, truthful output sanity against the brief,
canon and continuity, not the full checklist report below. The detailed
dimensions below apply to strict or explicitly requested review. Neither mode
can approve an uninspected, failing or stale result.

| Dimension | Review question |
|---|---|
| Narrative clarity | Does each panel communicate one necessary beat? |
| Composition | Is the story point immediately dominant in each panel? |
| Spatial continuity | Are geography, axis, eyelines, entrances, exits, and travel direction coherent? |
| Character consistency | Do identity, body, wardrobe, scale, handedness, and damage state persist? |
| Environment and props | Are geometry, landmarks, ownership, position, and state correct? |
| Camera and motion | Are shot, angle, subject movement, and camera movement unambiguous? |
| Sequence logic | Do cause, effect, reveals, reactions, and transitions connect? |
| Grid flow (grid mode only) | Are panels in correct reading order? Are dividers clean? Are panel numbers present and correct? |
| Grid legibility (grid mode only) | Is each panel large enough to read key story information and staging? |
| Element fidelity | Do character faces, body types, wardrobe silhouettes, location geometry, and prop forms match the canonical Element sheets — even in sketch mode? |
| Render style | Is the sketch style consistent across all panels? If sketch mode, is it monochrome with no unintended color? If full color, is the palette stable? |
| Reproducibility | Are prompt, references, model, parameters, files, and status recorded? |
| Video handoff | Does the handoff carry staging as prompt text and list only element references to bind, with `bind_board: false`? |

Reject or repair:

- swapped, omitted, duplicated, or blended subjects;
- wrong subject count or screen order;
- accidental axis reversal;
- location geometry drift;
- missing, duplicated, or changed props;
- visible reference-sheet panels, labels, or sketch marks;
- a frame that is attractive but depicts the wrong beat;
- near-identical copy-paste panels that suppress required action change;
- a local correction that breaks previously approved areas;
- in grid mode: panels out of reading order, illegible panel content, missing or
  misaligned dividers, panel numbers bleeding into image content.

Send each failed panel to the edit-first repair path in
[Editing Failed Panels](editing-failed-panels.md). A failed panel never sends the
whole board back to generation. For a scene board, also review the scene as a
sequence (eyelines, screen direction, light and prop continuity, rhythm) after the
panels pass.

### 13. Present variants and capture selection

Present candidates in panel order with filename or artifact ID, material
differences, known continuity or anatomy issues, and a recommendation.

For project selection, follow the project's `approval_mode` per the
[Production policy](../../../contracts/production-policy.md): against the recorded beat, canon, and continuity criteria, save the hash-bound review and either the validated agent decision or a recommendation awaiting the user's choice. If no panel passes or inspection is
unavailable, leave selection unresolved.

`approve_for_me` permits the agent to select a passing candidate without a new
user confirmation; `ask_for_approval` waits for the user's explicit choice.
Review mode changes evidence depth, never approval authority. Keep explicit
user locks and historical records. The writer still requires a short actual
candidate sanity record in default mode; never fabricate passing evidence.

After a mode-authorized choice:

- set `selected_variant` to the chosen file;
- mark the chosen output `approved` only through the validated decision writer;
- mark rejected candidates `rejected` without deleting them;
- preserve prompts, hashes, and metadata for every take.
