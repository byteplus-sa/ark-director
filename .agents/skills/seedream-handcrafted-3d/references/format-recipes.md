# Format recipes

These are optional prompt patterns, not provider parameter requirements.
Replace bracketed content with the user's design and omit irrelevant sections.

## Portrait or hero image

```text
Subject:
[Identity, age, facial structure, hair, body shape, outfit, accessories,
expression and pose. Preserve any locked descriptors.]

Style:
Handcrafted stylized 3D with matte painterly surfaces, sculpted hair,
subtle pencil hatching and tactile cloth. [Two or three relevant craft details.]

Composition:
[Requested framing and setting.] Keep the face and costume readable.

Lighting:
[Requested lighting.] Resolve material texture with controlled highlights.
```

Do not introduce a halo, cape, emblem, or other signature feature merely because
it appears in a style reference. Hero themes describe a costume here; video
action and supernatural effects are outside this still-image skill's scope.

## Character sheet

```text
References:
@Image 1: [actual role; omit this section for T2I].

Subject:
[Exact character and wardrobe descriptors.] The same character in every view.

Style:
[Handcrafted 3D treatment tailored to this subject.]

Composition:
Three panels: back full-body, front full-body, frontal face close-up.
Show the entire hair silhouette and footwear in both body panels, with clear
margin above and below. Keep body scale consistent between full-body views.

Setting and lighting:
Plain neutral-gray studio background, soft even neutral lighting.

Constraints:
Preserve face, hair, outfit, accessory placement and palette across all views.
[Only requested and relevant exclusions, such as unwanted text or logos.]
```

Override the default layout, expression, or light when the user supplies one.
For a new collection, describe distinctive faces and bodies before varying
clothing. Skin tones and cultural backgrounds follow the brief, not this recipe.

## Wardrobe material study

Prefer an available selected character sheet as the costume reference. Preserve
its garment lengths, closures, seams, emblems, palette, and footwear silhouette.
If there is no sheet, state that the output explores materials for the described
outfit rather than claiming to reproduce a locked costume.

```text
References:
@Image 1: selected character sheet, costume construction and palette.
@Image 2: [optional authorized material craftsmanship reference].

Subject:
[Exact costume descriptors from the sheet; omit face, hair and skin details.]

Style:
Handcrafted stylized 3D material macros: visible woven fibers, stitched seams,
dimensional ornament and restrained wear, consistent with @Image 1.

Composition:
Three vertical close-up panels with narrow plain gutters. Left: [chest cloth,
stitching or ornament]. Its upper edge cuts through cloth below the neckline;
garment fabric fills that edge. Center: [waist, pleat, seam or attachment].
Right: [footwear and/or wearable detail]. Fill each panel with costume surfaces;
head and face are outside the frame. Preserve construction from @Image 1.

Lighting:
Soft neutral studio light that reveals weave without glossy highlights.
```

Adjust the panel count to the request. Inspect the actual output: a phrase such
as "below the chin" can still leave a chin in frame. A cloth-filled top-edge
instruction is a useful framing hypothesis supported by the bundled correction
example, not a guarantee. Neck skin alone is different from a face fragment;
apply the user's actual crop requirement rather than inventing a stricter one.

## Scope boundaries

For a photorealistic request, do not silently substitute this style. For exact
labels, logos, or graphic alignment, return art direction for the image layer
and let the caller arrange deterministic graphics. Drafting prompts does not
authorize generating, restyling a locked identity, or approving an output.
