# Editing Failed Panels

Focused reference for `seedream-storyboard`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Edit pattern for a failed panel](#edit-pattern-for-a-failed-panel)
- [HTTPS URL requirement for edits](#https-url-requirement-for-edits)
- [Grid-to-bbox coordinate mapping](#grid-to-bbox-coordinate-mapping)
- [Revision contract](#revision-contract)

## Edit pattern for a failed panel

Edit first. When some panels of a board fail, repair those panels and leave the
others alone; do not regenerate the whole board. For a failed panel in
separate-images mode, use a narrow revision contract on that panel's image. For a
failed panel in single-image grid mode, use `seedream_edit_image` with a bounding
box targeting just the failed panel's cell, and re-generate the grid only when most
cells fail or the cause is shared.

The scope ladder is panel, then shot, then scene. Escalate from an edit to
regenerating the panel after two failed edits on the same dimension or when the
defect is structural (a wrong beat, a reversed axis, wrong geography). An edit saves
a new version of the same panel, keeps the original as rejected, and leaves every
other panel's file, hash and approval unchanged. See [Scene Board](scene-board.md).

### HTTPS URL requirement for edits

`seedream_edit_image` requires HTTPS URLs — local file paths are not accepted.
Before editing:

1. Upload the grid image via `media_upload` (if not already cached), or
2. Call `media_presign` on an existing `object_key` from `ref_cache.json` to
   get a fresh presigned URL.

Presigned URLs expire in ~10 minutes — submit the edit task immediately after
obtaining the URL.

### Grid-to-bbox coordinate mapping

`seedream_edit_image` uses normalized coordinates (0–999) for both x and y.
For a grid with R rows and C columns, each cell occupies a range of width
`999/C` and height `999/R`. Use this table or the formula to target a specific
panel.

**Formula:**

```text
cell_width  = 999 / C
cell_height = 999 / R
panel_col   = (panel_index - 1) % C      (0-indexed)
panel_row   = (panel_index - 1) // C     (0-indexed)
x1 = round(panel_col * cell_width)
y1 = round(panel_row * cell_height)
x2 = round((panel_col + 1) * cell_width)
y2 = round((panel_row + 1) * cell_height)
```

**Quick reference — 3×3 grid (most common):**

| Panel | Position | x1 | y1 | x2 | y2 |
|---|---|---|---|---|---|
| 1 | top-left | 0 | 0 | 333 | 333 |
| 2 | top-center | 333 | 0 | 666 | 333 |
| 3 | top-right | 666 | 0 | 999 | 333 |
| 4 | mid-left | 0 | 333 | 333 | 666 |
| 5 | mid-center | 333 | 333 | 666 | 666 |
| 6 | mid-right | 666 | 333 | 999 | 666 |
| 7 | bottom-left | 0 | 666 | 333 | 999 |
| 8 | bottom-center | 333 | 666 | 666 | 999 |
| 9 | bottom-right | 666 | 666 | 999 | 999 |

**Quick reference — 2×3 grid:**

| Panel | Position | x1 | y1 | x2 | y2 |
|---|---|---|---|---|---|
| 1 | top-left | 0 | 0 | 499 | 333 |
| 2 | top-right | 499 | 0 | 999 | 333 |
| 3 | mid-left | 0 | 333 | 499 | 666 |
| 4 | mid-right | 499 | 333 | 999 | 666 |
| 5 | bottom-left | 0 | 666 | 499 | 999 |
| 6 | bottom-right | 499 | 666 | 999 | 999 |

Add a small margin (e.g. ±5) to avoid the divider line bleeding into the edit.

### Revision contract

```text
References:
@Image 1: base storyboard panel to edit
@Image 2: approved character identity

Task:
Image Editing — local storyboard correction

Edit instructions:
In @Image 1, [single requested change at the marked point or bounding box].
Use the identity from @Image 2 for [character]. Preserve the camera, composition,
pose, screen direction, background geometry, lighting, palette, and all
unmarked subjects and props.

Acceptance criteria:
- [observable result]
- [continuity property that must remain unchanged]

Constraints:
No new subjects, no wardrobe change, no background redesign, no text, no
watermark, and no changes outside the target region.
```

Change one failed dimension at a time. Use the corrected result as a continuity
anchor only after it passes review.
