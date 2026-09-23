# Review And Selection

Focused reference for `seedream-storyboard`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [12. Review the board](#12-review-the-board)
- [13. Present variants and capture selection](#13-present-variants-and-capture-selection)

### 12. Review the board

Evaluate every individual panel. For multi-panel separate-images boards, also
evaluate the ordered contact sheet. For multi-panel single-image grid boards,
evaluate the whole grid image for both per-panel quality and cross-panel flow.
For a one-panel board, compare its three variants side by side; a comparison
sheet is a review artifact, not another storyboard panel and not the canonical
video input.

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

### 13. Present variants and capture selection

Present candidates in panel order with filename or artifact ID, material
differences, known continuity or anatomy issues, and a recommendation.

For project selection, read the project mode before choosing. In
`approve_for_me`, select the best passing panel against the recorded beat,
canon, and continuity criteria, then
save the hash-bound review and agent decision. In `ask_for_approval`, record a
recommendation and ask the user to choose. If no panel passes or inspection is
unavailable, leave selection unresolved. After a mode-authorized choice:

- set `selected_variant` to the chosen file;
- mark the chosen output `approved` only through the validated decision writer;
- mark rejected candidates `rejected` without deleting them;
- preserve prompts, hashes, and metadata for every take.
