# Image Editing

Focused reference for `seedream-prompt`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Recommended prompt structure — Image Editing](#recommended-prompt-structure--image-editing)

## Recommended prompt structure — Image Editing

Use the editing patterns below only where the selected model and available tool
support the operation. A provider capability does not establish wrapper support.
Use only the sections needed for the edit:

```
References:          # required for image editing
Task:                # include when the mode needs clarification
Editing mode:        # include when it helps disambiguate the operation
Edit instructions:
Constraints:         # only preservation and exclusion requirements that matter
```

### Editing Modes

The four image-editing operation types are: **addition** (add an element at a location), **deletion** (remove an element), **replacement** (swap one element for another), and **modification** (change an attribute of an element). Every edit prompt maps to one of these four.

#### 1. Interactive Control / Positioning

Position an edit using one of two official forms.

**Form 1 — Free-form marker + natural-language location**: Mark the edit area with hand-drawn sketches, doodles, circles, or colored frames, then describe the marker and intent in natural language.

```
References:
@Image 1: base image to edit

Task:
Image Editing

Editing mode:
Interactive Control — Free-form marker

Edit instructions:
In @Image 1, [describe exactly what to modify at the marked location]. [Describe what to add/remove/change].
```

Colored-frame region isolation (Form 1 pattern): outline locations with differently colored frames, and the model generates the specified items within each designated area, each strictly respecting its coordinate boundaries.
```
Generate a blue furry monster watching bubbles in the red frame, and a grass-green blanket in the purple frame.
```

Anchor grounding works best on clear row-and-column layouts:
```
Shift the red chariot at the bottom left one square to the right, and move the black pawn on the second line counting from the left side of Black's position one square downwards.
```

Layout-preserving translation (Form 1 pattern): the model translates text while preserving the original spatial layout.
```
Translate the menu into Chinese.
```

**Form 2 — Precise coordinate location (capability-gated)**: Use `<point>` or
`<bbox>x1 y1 x2 y2</bbox>` only after verifying the selected model's interactive
editing capability and the connected tool's coordinate mapping. Pro and 5.5
have documented provider support; other models and wrapper exposure require
separate evidence. Inspect actual results for boundary fidelity. Unknown
support is unresolved, not permission to substitute a full-frame edit.

```
Edit instructions:
Use the subject from @Image 1 <bbox>118 331 933 871</bbox> to replace the subject in @Image 2 <bbox>179 283 796 986</bbox>.
```

The model can also lock onto semantic regions without explicit coordinates — e.g., "Complete all the multiple-choice questions above and write out the corresponding calculation steps in the blank spaces below each question."

#### 2. Sketch Rendering

Use doodles, color blocks, lines, or simple sketches as control signals. The model recognizes the intent of each block and renders it as a high-fidelity visual.

```
References:
@Image 1: sketch / doodle / color block layout

Task:
Image Editing

Editing mode:
Sketch Rendering

Edit instructions:
Using the sketch in @Image 1 as the layout guide, generate [describe the final output]. [Describe what each block should become, e.g. "the red rectangle at the top becomes a title banner," "the blue circle on the left becomes a product photo"].
```

#### 3. Layer Separation

Split an image into editable layers only through a verified decomposition
operation. Supply `layer_decomposition: true` and exactly one composite input.
The prompt below expresses intent, not an executable capability claim.

```
References:
@Image 1: composite image to separate

Task:
Image Editing

Editing mode:
Layer Separation

Edit instructions:
Separate @Image 1 into independent layers: [list desired layers, e.g. "background, main subject, text overlay, decorative elements"]. Output each layer as a PNG with transparent background.
```

Keep the base image distinct from its layers. The documented Pro ceiling is one
base plus up to 16 layers; the 5.5 ceiling is one base plus up to 99 layers,
not a promised output count. Layers are PNG; inspect reconstructed occluded
areas and transparency rather than claiming perfect separation.

For 5.5 only, `layer_decomposition_options.max_images` accepts integer 2-100,
default 30, counting the base; optional `text_recognition` returns OCR only on
recognized regular-text layers. Use documented size presets or `auto`, not
explicit dimensions, and omit `background` for this operation. Any failed
layer fails the request. Do not infer connected-wrapper support from provider
docs or treat decomposition as native sequential generation.

OCR output boxes use 0-1000 normalized coordinates in the base-image system,
separate from edit-input 0-999 coordinates. Approximate font/style information
is not exact design fidelity or font-license permission. See
[the quick reference](quick-reference.md) for dated provider sources.

#### 4. Color & Material Replacement

The model accepts Hex color codes or external color swatches and replaces materials while preserving lighting and perspective.

```
References:
@Image 1: material reference (e.g. velvet, wood, metal)
@Image 2: color swatch reference (e.g. palette card)
@Image 3: target image to modify

Task:
Image Editing

Editing mode:
Color & Material Replacement

Edit instructions:
Using the material from @Image 1 and the color swatch from @Image 2, modify the [specific object or region] in @Image 3. [Optional: specify Hex codes, e.g. "change to #3E4A2E dark green and #DB973E turmeric yellow in alternating pattern"].
```

#### 5. Multi-Image Fusion

Fuse objects, styles, and materials from multiple reference images into a target scene.

```
References:
@Image 1: first object on a white background
@Image 2: second object on a white background
@Image 3: third object on a white background
@Image 4: fourth object on a white background
@Image 5: fifth object on a white background
@Image 6: sixth object on a white background
@Image 7: seventh object on a white background
@Image 8: target scene and composition layout

Task:
Image Editing

Editing mode:
Multi-Image Fusion

Edit instructions:
Precisely cut out the first object from @Image 1, the second from @Image 2, the third from @Image 3, the fourth from @Image 4, the fifth from @Image 5, the sixth from @Image 6, and the seventh from @Image 7. Compose them into a real still-life photograph using the scene geometry and placement from @Image 8. Ensure correct perspective, light-and-shadow, and spatial relationships. Faithfully reproduce material details such as wood grain, leather, lace, glass, and feathers.
```

### Combining Editing Modes

Compatible prompt patterns can be combined when the selected operation and tool
support them; decomposition and its parameters remain a separate request. Example:
```
Change the pumpkins to an alternating pattern of dark green #3E4A2E and turmeric yellow #DB973E, while giving the background typography an embroidered texture.
```
