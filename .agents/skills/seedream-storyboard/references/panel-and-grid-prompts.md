# Panel And Grid Prompts

Focused reference for `seedream-storyboard`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [8. Write the exact prompt for each panel](#8-write-the-exact-prompt-for-each-panel)
- [9. Write the multi-panel prompt](#9-write-the-multi-panel-prompt)
- [9c. Prompt length budget](#9c-prompt-length-budget)
- [9d. Prompt-review gate](#9d-prompt-review-gate)

### 8. Write the exact prompt for each panel

Use only the sections that add value. Keep the submitted prompt within the live
tool limit.

```text
References:
@Image 1: character identity — [character]
@Image 2: location geometry — [location]
@Image 3: prop identity — [prop]
@Image 4: composition control — [layout only]
@Image 5: approved style — [style, palette, and lighting only]

Task:
Image-to-Image (I2I) — single cinematic storyboard panel

Panel purpose:
[The new story information or emotion this panel communicates.]

Subject and decisive moment:
[One frozen moment. Name every visible subject, pose, expression, action, and
prop. Bind identity and prop references inline.]

Setting and state:
[Location, time, weather, persistent landmarks, visible object state. Bind the
location reference inline.]

Staging and continuity:
[Screen-left/right positions, foreground/midground/background, eyelines,
distances, overlaps, travel direction, entrances/exits, and what must match the
previous panel. Name a held or gesturing hand by anatomy and frame side, for
example "her right hand, frame-left", so the same wording carries into video.]

Style:
[Render style: default to "rough pencil sketch, monochrome graphite, no color"
unless the user requested full color or a specific sketch medium. Bind the
style reference inline when provided.]

Lighting:
[Source, direction, quality, color, and atmosphere. In sketch mode, describe
lighting as directional shading cues (e.g. "light from upper left, cast
shadows to the lower right") rather than color temperature and material
response. Never describe a light source as a point or dot: name the physical
emitter that produces it (the device, the lamp, the window) and state its
full-frame effect. A "red point light" reads as a literal dot — instead write
"the silver device fires a bright flash that fills the frame."]

Composition:
[Aspect ratio, shot size, camera height/angle, lens intent, framing, depth, and
focus priority. Bind the composition guide inline when provided.]

Constraints:
Quality: [appropriate draft or final quality]
Preserve: [approved identity, geometry, pose, state, and style]
Exclude: [only material faults; no text overlays, labels, storyboard borders,
watermarks, unintended subjects, duplicated faces, or control-guide marks]
```

For text-to-image, omit `References` only when there are no applicable
canonical Element sheets. When character, location, or prop sheets exist, use
image-to-image/reference generation and bind them with exact `@Image N` tokens.
Use:

```text
Task:
Text-to-Image (T2I) — single cinematic storyboard panel
```

Reference inventory alone is insufficient. Repeat each binding in the section
it controls:

```text
Use the face, hair, and wardrobe from @Image 1 for Mara. Preserve the room
geometry and altar position from @Image 2. Use @Image 4 only for blocking and
camera composition; remove all sketch lines and labels.
```

### 9. Write the multi-panel prompt

Use this section when the board contains multiple narrative panels. Choose the
prompt structure based on the delivery mode recorded in the panel plan.

#### 9a. Single-image grid (default)

One output image containing all panels arranged in a reading-order grid. Works
with any model that produces a single image, including Seedream 5.0 Pro.

```text
Task:
Single-Image Grid Storyboard — [N] panels in one image

Grid contract:
Generate ONE single image containing [N] storyboard panels arranged in a
[rows]×[cols] grid, reading left-to-right, top-to-bottom. Each panel is a
separate frozen decisive moment in narrative order. Separate panels with thin
divider lines. Place a small panel number in the top-left corner of each cell.
Keep recurring character identity, wardrobe, location geometry, prop design,
palette, and rendering style consistent across all panels.

References:
@Image 1: character identity — selected character sheet
@Image 2: location geometry — selected location sheet
@Image 3: prop identity — selected prop sheet

Global visual canon:
[Stable identity, location, prop, style, aspect ratio, and lighting rules.
Default render style: "rough pencil sketch, monochrome graphite, no color"
unless full color or a specific sketch medium is requested. Bind Element
references for identity, geometry, and prop form even in sketch mode.]

Panel 1 — [panel ID and purpose]:
[Decisive moment, staging, camera, and state.]

Panel 2 — [panel ID and purpose]:
[Decisive moment, staging, camera, and state change.]

[Continue in order.]

Constraints:
Return one single image with [N] panels in a [rows]×[cols] grid. Thin dividers
between panels. Small panel numbers in top-left corners. No speech bubbles, no
captions outside panel numbers, no watermarks, no decorative borders. Preserve
character count, identity, handedness, screen direction, location landmarks, and
prop state unless a numbered panel explicitly changes them.
```

Use `max_images: 1` (or omit it). Use a large enough output size to keep each
panel legible — for a 3×3 grid prefer `2048x2048` or wider. Each panel is
lower-resolution than a dedicated single-panel generation; if a panel needs
more detail for review, re-generate it as a standalone panel using the same
canon and its recorded prompt section. Neither the grid nor a standalone panel
is a video input.

#### 9b. Separate images (one image per panel)

N output images, one per panel. Requires a sequence-capable model (Seedream 5.0
Lite or 4.x) for a single batch request, or generates one Pro image at a time
from the same canon.

```text
Task:
Sequential Generation — [N] separate cinematic storyboard images

Sequence contract:
Generate a cohesive ordered set of [N] separate images, one image per numbered
panel. Keep recurring character identity, wardrobe, location geometry, prop
design, palette, and rendering style consistent. Each image must depict one
frozen decisive moment, not a collage or multi-panel grid.

References:
@Image 1: character identity — selected character sheet
@Image 2: location geometry — selected location sheet
@Image 3: prop identity — selected prop sheet

Global visual canon:
[Stable identity, location, prop, style, aspect ratio, and lighting rules.
Default render style: "rough pencil sketch, monochrome graphite, no color"
unless full color or a specific sketch medium is requested. Bind Element
references for identity, geometry, and prop form even in sketch mode.]

Panel 1 — [panel ID and purpose]:
[Decisive moment, staging, camera, and state.]

Panel 2 — [panel ID and purpose]:
[Decisive moment, staging, camera, and state change.]

[Continue in order.]

Constraints:
Return [N] separate images in narrative order. No captions, borders, panel
numbers, speech bubbles, watermarks, or contact-sheet layout inside the images.
Preserve character count, identity, handedness, screen direction, location
landmarks, and prop state unless a numbered panel explicitly changes them.
```

Set `max_images` to the requested panel count. Ensure references plus outputs do
not exceed the live model limit. If the sequence prompt approaches the tool
length limit, split it by scene or shot rather than deleting continuity rules.

### 9c. Prompt length budget

The Seedream prompt tool enforces a **4,000-character limit**. A full 9-panel
grid prompt with reference descriptions, staging, and continuity can easily
exceed this. Follow these rules to stay within budget:

1. **Count characters before submitting.** If the prompt exceeds 3,800
   characters (leaving headroom), apply the condensed template below or split.
2. **Condense before splitting.** Shorten panel descriptions to one or two
   tight sentences each. Move detailed staging into the panel plan table
   (`scene.md` / `storyboard.md`) — the prompt only needs what the model must
   draw, not the full continuity ledger.
3. **Compress reference descriptions.** Instead of full identity paragraphs,
   use one-line summaries: `@Image 1: Elastic Man — athletic build, crimson
   costume, gold accents, confident grin`.
4. **Merge global canon and constraints.** Combine the visual canon, render
   style, and constraints into one compact block.
5. **Split by scene or act when over budget.** If condensing is not enough,
   split the board into two grid images (e.g. panels 1–5 and 6–9) and generate
   separately. Record both as takes of the same board version.

#### Condensed prompt template (for large panel counts)

```text
Single-Image Grid Storyboard — [N] panels in a [rows]×[cols] grid, left-to-right, top-to-bottom. Thin dividers, small panel numbers 1-[N] in top-left corners. [sketch or color style].

@Image 1: [character — one-line identity + costume summary].
@Image 2: [character/location — one-line summary].
@Image 3: [location/prop — one-line summary].

Use face/body/costume from @Image 1 for [name] and @Image 2 for [name], rendered as [sketch or color]. Preserve [location] geometry from @Image 3.

Panel 1: [one-two sentence decisive moment, staging, camera].
Panel 2: [one-two sentence decisive moment, staging, camera].
[Continue for all panels.]

No speech bubbles, no captions, no watermarks. Preserve identity, wardrobe, screen direction, [key prop] across all panels.
```

This template fits ~9 panels within the 4,000-character limit when panel
descriptions are kept to 1–2 sentences. If it still overflows, split the board.

### 9d. Prompt-review gate

The calling agent owns the workspace prompt-review gate. Return this prompt,
ordered reference bindings, model/mode, and change contract to the caller for a
complete review of the exact request before submission. This leaf skill does
not load or invoke a sibling skill.

- Element bindings (`@Image N` indices match the request and manifest)
- Directing principles (assets first, positive instructions, direct don't describe)
- Render style consistency (sketch vs. color, monochrome enforcement)
- Continuity props and screen direction across panels
- Prompt length within the 4,000-character limit

Run the gate after writing the prompt snapshot file but before calling
`seedream_generate_image` or `seedream_edit_image`.
