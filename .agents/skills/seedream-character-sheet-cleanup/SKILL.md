---
name: seedream-character-sheet-cleanup
description: Cleans Seedream character sheets by removing the head from the full-body panels so only the close-up panel keeps a readable face. Invoke when a Seedance-bound sheet violates the requested single-face reference policy, or when the user requests this cleanup; inspect before editing.
---

# Seedream Character Sheet Cleanup

Inspect a Seedance-bound character sheet against the requested reference policy.
Use this cleanup only when an extra readable face violates that policy or the
user explicitly requests the edit.

The purpose is simple: a character sheet with multiple readable faces can
confuse Seedance during downstream video generation. If the front full-body
panel shows a second readable face, the model can drift between faces over time.
The cleanup pass keeps only one face anchor: the dedicated close-up panel.

## Non-destructive output rule

Never overwrite the source character sheet.

Always save cleanup output as a **new image file or new version** so the
original sheet remains available for review, rollback, or alternate use.

This skill is designed to partner with:
- `seedream-character-sheet` for generating the original three-panel sheet
- `seedream-edit` and the `seedream_edit_image` MCP tool for the actual cleanup
- `ark-mcp` (`seed_understand`) for verifying the cleanup result

## When to Invoke

Invoke this skill when all of the following are true:
- you already generated a character sheet
- the sheet contains a dedicated close-up face panel
- at least one full-body panel still shows a readable face
- the sheet will later be used as a Seedance identity lock or character reference
- the intended reference policy calls for one readable face

Do not invoke this skill when:
- the sheet already has only one readable face
- the user explicitly wants visible facial detail in multiple panels
- the image is a regular portrait sheet rather than a Seedance-facing identity sheet

## Core Rule

For Seedance-facing character sheets, keep exactly one readable face on the
sheet: the close-up panel.

The front full-body panel should preserve:
- pose
- clothing
- silhouette below the shoulders
- panel spacing
- background consistency

The front full-body panel should NOT preserve the head at all. Remove the
entire head (and optionally the neck) so the figure is headless. Do not blur
the face and do not replace it with a featureless surface: the head must be
gone, with the studio background filling the space where it was.

## Default Cleanup Target

The default target is the front full-body panel's face region.

If the back-view panel accidentally exposes too much face because of head turn
or profile leakage, clean that panel too. The close-up face panel remains the
only authoritative face and should stay untouched.

## Identity preservation

Cleanup can alter silhouette, hair, headwear, costume, or the close-up identity
anchor. Compare the original and edited image directly against user-approved
visible descriptors; list the features that must remain unchanged. Do not ask a
model to infer a person's gender identity from their appearance. A visual
understanding tool may assist a per-panel inventory, but its answer is evidence
to review rather than an authority over the user's stated identity.

Use one trigger: the intended downstream reference policy requires a single
readable face and inspection finds an extra readable face in a body panel, or
the user explicitly requests this cleanup. A failed video is not required.
If the sheet already meets the requested policy, keep it unchanged. Any cleanup
is a new unapproved version; preserve the original and ask the user to select
before switching the canonical reference.

## Recommended Editing Mode

Use `seedream_edit_image` with a bounding box around the entire head in the
full-body panel. This is a deletion or cleanup edit, not a full regeneration.

Box the whole head (hair and headwear included), not just the facial features.
Do not box the entire panel unless absolutely necessary.

## Prompt Template

Use this as the default edit instruction:

```text
Remove the entire head from the full-body front-view panel so the figure is
headless. There must be no head, no face, no hair and no headwear in that
panel. Fill the space where the head was with the studio background. Keep the
neck, shoulders, body, costume, pose, panel spacing, divider lines, studio
background, and the close-up face panel unchanged.
```

## Stronger Prompt Variant

Use this variant when the user also wants the neck removed, or when the edit
keeps recreating a head:

```text
Remove the entire head and neck from the full-body front-view panel so the
body begins at the shoulders and collarbone. Fill the space where the head and
neck were with the studio background. Keep the shoulders, body, costume, pose,
panel spacing, divider lines, studio background, and the close-up face panel
unchanged.
```

## Coordinate Guidance

When using `seedream_edit_image`:
- place the bbox around the entire head in the full-body panel (hair and
  headwear included, down to the neck), not just the facial features
- include the neck inside the box when the user wants the neck removed too
- avoid covering the shoulders, torso, divider line, or close-up panel
- a box that is too small leaves a blurred or featureless head — widen it to
  the full head before changing the prompt

For the standard three-panel 16:9 sheet (e.g. 2048×1152), the front full-body
panel is the middle third and the head sits at the top of that panel. A good
starting box in `seedream_edit_image` normalized coordinates (0–999) is:

```text
bbox: {x1: 454, y1: 22, x2: 549, y2: 204}
```

That box covers the head and neck with margin and stays clear of the panel
divider lines. Inspect the actual image; widen the box if direct or assisted
inspection confirms a remaining face
in the center panel, and re-run the mandatory verification after every edit.

## Acceptance Check

Compare original and edited panels directly (see Verification). Use a visual
understanding tool as supporting evidence where available. The cleanup is
technically successful when:
- the close-up panel is the only readable face on the sheet
- the front full-body panel shows no head at all — the figure is headless and
  the studio background fills the space where the head was
- the front full-body panel still reads as the same character and costume
- the sheet layout remains stable
- the background and divider lines stay consistent
- no blurred face, featureless head, or new facial detail appears in the body
  panels

## Verification (mandatory)

Inspect the original and edited sheets side by side at readable resolution.
Check each panel against the approved visible descriptors and exact edit region.
A multimodal understanding tool can assist but is not the only valid verifier.
If no image-verification surface is available, record unresolved verification
and retain `review`; do not promote the output to a canonical input.

When using `seed_understand`, provide the original and cleaned
image and a prompt that forces a per-panel answer. Ask for a structured,
panel-by-panel inventory of faces and require it to:

- confirm the full-body panel is headless: no head, no face, no hair, and no
  headwear in that panel;
- confirm the close-up panel still shows exactly one intact, readable face;
- confirm no new face appeared in any other panel.

If direct or assisted inspection finds damage to the close-up or a readable
face remaining in a targeted body panel, investigate the actual edit boundary.
Correct the bounding box or instruction as needed and verify the new version.
Do not hand the sheet to Seedance until visual verification passes and the
user selects that version.

### Example verification prompt

```text
Look at this character sheet carefully, panel by panel. In every full-body
panel, is the character headless — no head, face, hair, or headwear visible?
In the close-up panel, does the face remain intact and unchanged? Answer each
panel explicitly: list the panels left to right, state "headless" or "face
present" for each, and name by position which panel (if any) still has a face.
```

Re-run this verification after every re-edit so a second-face sheet never
reaches Seedance.

## Workflow Pairing

Recommended sequence:
1. Assumes a three-panel sheet exists (e.g. from `seedream-character-sheet`).
2. Inspect the full-body panels for duplicate readable faces.
3. If an extra face violates the requested single-face policy, apply this cleanup.
4. Use the `seedream_edit_image` MCP tool to remove the extra face.
5. Compare original and edited panels directly against the approved visible
   descriptors: target body panel headless, close-up intact. A visual-understanding
   tool may assist. Unavailable visual verification stays unresolved; re-edit only
   when inspection establishes a defect, using a corrected bbox when appropriate.
6. Save the cleaned sheet as a **new version/file**, not as an overwrite of the
   source image.
7. Present the new version for explicit selection before canonical use.

## Example From The User

The user provided a before-and-after pirate character-sheet example:
- Before: the left full-body panel still shows a readable front face, while the
  right close-up panel also shows the face. This creates two competing face
  anchors.
- After: the left full-body panel keeps the body, costume, and headwear, but
  the readable face is removed so the right close-up panel is the only face
  anchor left on the sheet.

Use the examples as inspection context, not an instruction to edit every sheet.
The requested reference policy and selected edit determine the required result.

## Notes For Example Images

The example images live beside this skill under `examples/` using these
filenames:
- `examples/before_duplicate-face.png`
- `examples/after_single-face.png`

Treat that pair as illustrative before-and-after evidence, not user approval
of a new output or a substitute for the requested visible descriptors.

### Before

![Before cleanup](examples/before_duplicate-face.png)

### After

![After cleanup](examples/after_single-face.png)
