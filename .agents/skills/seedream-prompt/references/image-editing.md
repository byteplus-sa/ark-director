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

Colored-frame region isolation (Form 1 pattern): identify each outlined region
and describe its intended content. Treat boundary adherence as a result to
inspect, not a guarantee.
```
Generate a blue furry monster watching bubbles in the red frame, and a grass-green blanket in the purple frame.
```

Anchor grounding works best on clear row-and-column layouts:
```
Shift the red chariot at the bottom left one square to the right, and move the black pawn on the second line counting from the left side of Black's position one square downwards.
```

Layout-preserving translation (Form 1 pattern): request translation while
retaining the layout, then proofread the output and inspect spatial changes.
Use deterministic text replacement when exact copy or typography is required.
```
Translate the menu into Chinese.
```

**Form 2 - Structured coordinate edit (capability-gated)**: verify the selected
model and tool before preparing executable settings. Pro and 5.5 have
documented provider support; other models require separate evidence.
The current MCP `seedream_generate_image` accepts structured `point` or `bbox`
in 0-999 coordinates and targets only the first image. Do not add `<point>` or
`<bbox>` markup to the prompt; the adapter supplies it. Its markup counts toward
the 4000-character prompt limit. Unknown support is unresolved, not permission
to substitute a full-frame edit.

```text
References:
@Image 1: room photograph to edit
@Image 2: replacement lamp, shape and material reference only

Edit instructions:
Replace the selected lamp in @Image 1 with the lamp design from @Image 2.
Keep the room geometry, camera, other objects and lighting unchanged.
```

The caller supplies the verified target box separately, on Image 1. Reorder
the actual inputs and every reference binding together if the source was
previously elsewhere in the list. A donor is not a second structured target.
The guide's `bbox=[xmin, ymin, xmax, ymax]` layout convention is 0-1000, not this
MCP field. See [Layout and Typography](layout-and-typography.md) for validation,
boundary conversion and coordinate remapping after cropping or resizing.

Semantic locations such as "the lamp on the right-hand desk" may be sufficient
when unambiguous; do not invent precise coordinates from a textual description.

### Numbered marked-region edits

Identify each marker uniquely. State the operation, source, destination,
replacement size and orientation, and what must remain unchanged. If markers
overlap or an operation changes the target of a later operation, clarify the
order or split the work into separate edits.

When a clean source and annotated guide are both supplied, bind them separately:
the clean source owns identity and pixels to preserve; the annotated guide owns
locations only. Remove all temporary numbers, arrows and colored outlines from
the result. Inspect both marked and unmarked regions for unintended changes.

Fictional example:

```text
Use @Image 1 as the clean room source and @Image 2 only as the numbered guide.
Move the small side table from marker 1 to the empty floor at marker 2,
preserving its size and orientation. Remove the folded cloth at marker 3.
Keep the chair, window, camera and light direction unchanged. Reconstruct only
the newly exposed floor. Remove every guide number, arrow and outline.
```

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
The current MCP does not expose decomposition or rich-text OCR; do not pass
these provider-only fields to it or treat a cutout as a multilayer result.

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

Use Hex color codes or swatches as color intent, naming the affected surfaces
and protected colors. Preserve lighting and perspective in the instructions,
then inspect them; a Hex value does not guarantee colorimetric accuracy.

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

### Multi-round edits and drift

Use the last accepted output as the next source, not simply the newest output.
Keep each request self-contained: restate the requested delta, reference roles
and cumulative preservation constraints. Do not assume conversational memory
or that "keep everything else" carries earlier decisions into a new call.

Prefer one major change per round when changes interact. The caller retains
the accepted source artifact/hash, exact model, prompt, ordered references and
settings; a chat-only draft needs no invented hash or production record.
Compare each candidate against the accepted source for identity, geometry,
materials, lighting, text and untouched regions before continuing.
On drift, reject the candidate and roll back to the last accepted source;
do not compound the defect or silently overwrite the approved image.
Uncertain submission status requires reconciliation, not another edit request.

### Extraction and channel changes

For cutouts and transparent extraction, use
[Transparent Assets](transparent-assets.md). For resize, crop, recompose or
capability-verified canvas extension, use
[Layout and Typography](layout-and-typography.md). Neither operation implies
decomposition, exact foreground preservation or permission to alter identity.
