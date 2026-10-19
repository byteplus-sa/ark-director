# Seedream Elements Checklist

Seedream character, location and prop sheet prompts. Apply the universal items
in [the index](review-checklists.md#universal--all-prompts) first.

## Seedream character sheet

Source skill: `seedream-character-sheet`

### Layout

1. **Three-panel default.** Back full-body, front full-body, face close-up. Unless user
   explicitly asks for more panels.

2. **Neutral gray background.** Default studio background — neutral gray, never
   scene-specific. Deviates only if user explicitly wants stylized/filmic sheet
   background.

3. **Panel order.** Back full-body first, front full-body second, frontal close-up
   third.

### Subject

4. **Reference binding.** Each reference is bound inline.

5. **Identity continuity.** Preserve supplied age, stable facial traits, hair,
   headwear, costume and key accessories. Include ethnicity or cultural identity
   only when supplied and relevant; its absence is not a defect and never
   authorizes inferring it from appearance or the operator's market.

6. **Same person statement.** Explicitly states it is the same person in all panels.

7. **No held props.** Nothing held, carried, aimed, or operated appears in the sheet;
   branded, recurring, or story-critical ones need separate `prop_` sheets,
   while incidental objects may be text-only in scenes. Scene-variant wearables (e.g.
   sunglasses worn only in some scenes) are also excluded and made props instead.
   Only always-worn outfit elements (hat, helmet, eyewear, jewelry) may appear.

### Setting

8. **Default background.** Neutral gray seamless, no props, no held objects, no
   furniture, no environmental clutter.

### Lighting

9. **Neutral, not scene-specific.** Soft, even studio light, flat fill, neutral
   white balance, no mood, no dramatic shadows, no hotspots, no blown highlights.
   Lighting never changes to match the character's scene or story mood.

10. **Consistent across panels.** Lighting is identical across all three panels.

### Composition

11. **Three panels only.** No extra panels.

12. **Same identity.** Same character identity across all panels.

13. **Readable silhouette.** Costume silhouette readable in body panels.

14. **Face authority.** Close-up panel is the face authority.

### Constraints

15. **Common negatives.** No extra panels, no profile panel, no 3/4 panel, no props in
    hands, no held objects/weapons, no background variation, no scene lighting or
    color cast, no distorted hands, no extra fingers, no watermark.

### Workflow

16. **Cleanup check.** When the requested downstream reference policy requires
    one readable face, inspect for extra faces and return the defect to the
    caller. Cleanup is conditional, non-destructive, and requires new selection;
    this reviewer does not invoke an editing skill.

17. **Element saved.** Saved under `elements/<character-id>/`.

18. **Selected variant.** Approved filename recorded as `selected_variant` in
    `character.md`.

---

## Seedream location asset

Source skill: `seedream-location-asset`

### Location

1. **Place described.** Interior/exterior, function, scale, spatial mood, core
   architectural identity.

### Era and world rules

2. **Historical period.** Stated if relevant.

3. **Geography/climate.** Stated if relevant.

4. **Technology limitations.** Stated if relevant.

5. **Realism constraints.** Explicitly excludes modern intrusions if realism matters.

### Set dressing and objects

6. **1-3 hero set pieces.** Key defining objects.

7. **Practical objects.** Objects that imply use.

8. **Material realism and wear.** Surfaces show wear and use.

9. **Depth cues.** Foreground/midground/background.

10. **Lived in.** Not empty — feels inhabited.

### Style

11. **2-4 strong anchors.** From: photorealistic, cinematic, naturalistic editorial
    reference, grounded realism, film still, period-authentic.

### Lighting and atmosphere

12. **Practical key source.** Where the light comes from physically.

13. **Time of day / weather.**

14. **Shadow falloff.**

15. **Haze / dust / smoke / moisture.** Atmospheric particles.

16. **Brightness.** How bright or restrained the scene is.

### Composition and lens

17. **Establishing vs detail vs reference sheet.** Type stated.

18. **Camera angle.** Eye level / high angle / low angle.

19. **Lens length.**

20. **Aspect ratio.**

21. **Depth of field.**

### Ordering rules

22. **Place before mood.** What the place is comes before how it feels.

23. **Era/world rules before lens/style polish.**

### Constraints

24. **Common negatives.** No characters, no modern props, no plastic CGI surfaces,
    no bright white cyc background unless explicitly requested, no text overlays, no
    watermark.

### Three prompt patterns

25. **Pattern A — Reusable asset.** Stable architecture, clear material language,
    minimal action, readable space, reusable identity.

26. **Pattern B — Cinematic establishing still.** Emotional lighting, camera language,
    atmosphere, foreground/background layering.

27. **Pattern C — Reference-preserving iteration.** I2I for every reference-guided
    location prompt.

---

## Seedream prop asset

Source skill: `seedream-prop-asset`

### Gate

1. **Threshold met.** The prop is branded, story-critical, recurring across two
   or more shots, or a scene-variant wearable. A generic or briefly held object
   is text-only; a sheet prompt for it is a MAJOR scope defect unless the user
   explicitly asked for that sheet, which is then noted as below threshold.

2. **Acquisition first.** A real brand, logo, or labeled product the brief
   authorizes uses an existing or acquired asset unless none is usable, a
   stylized substitute is requested, or acquisition is blocked. An unauthorized
   brand stays de-identified. Inventing a real logo is CRITICAL.

### Layout

3. **View plan declared.** Front and back by default; side added when the user
   asks or the object's profile carries its identity (vehicles, machines, tools,
   footwear, furniture). Near-symmetric, thin, or flat objects stay at front and
   back. Three views at most; a detail close-up is a separate image, never a
   fourth view. A single named view (front, back, side, top, edge, detail) is valid
   when a shot or the user asks for one angle. A prompt with a single
   three-quarter hero view and no other face is a MAJOR defect unless one view
   was requested.

4. **Background.** Pure white seamless with a faint contact shadow, or neutral
   light gray, with the same faint contact shadow, for white, silver, chrome,
   clear, or translucent objects, objects where such parts make up a large share
   of the silhouette, or when the project's approved props or character sheets
   already use gray. The background runs as one continuous field across the whole
   sheet. No colored, gradient, textured, or scene background.

5. **Neutral lighting.** Even, neutral white balance, identical across views.
   Shape-revealing highlights and gentle raking light are allowed; scene mood
   and color casts are not.

### Subject

6. **Reference binding.** Each reference is bound inline to the property it
   controls; an approved prop or authorized photo leads.

7. **Task type.** I2I whenever any reference guides a visible property,
   including every state variant of an approved prop.

8. **Count stated.** One object, or an exact matched-set count with one shared
   design.

9. **Identity description.** Silhouette and proportions, real-world size in
   words, materials and finish, colors, and the identity-critical details the
   video must reproduce, with repeated features (doors, handles, wheels, lamps)
   counted per face. Wear and damage appear only as the story needs.

10. **One canonical state.** Open/closed, lit/unlit, folded/extended or similar
    is stated; emissive parts stay off unless the glow is canonical.

11. **Descriptor continuity.** A variant or revision reuses the approved
    descriptor word for word.

12. **No hands or wearers.** Held props appear without hands; wearables appear
    unworn, without a person, head, mannequin, or body part. A body continuity
    mark is the exception: it is an I2I close-up with laterality stated.

### Style

13. **Project style match.** Render style matches the approved characters and
    locations; 2–4 anchors.

### Composition

14. **Whole object.** Every view fits the whole object with a stated clear margin
    (about 6% of the sheet) to the canvas edge and to the next view.

15. **Faces, flanks, and size.** Each view names the face it shows, the back is
    the opposite face with its own described details, and the views share one
    design and one scale (the object the same height in each view; width
    targets are not used). Three-quarter views of an object whose flanks
    differ name the visible flank in object and frame terms, with the rear view
    written as a half-revolution turn of the front view and the side profile
    matching the front view's flank.

16. **One continuous background.** The prompt says "view", not "panel", and asks
    for no boxes, frames, borders, divider lines, off-white rectangles, labels,
    or captions, and a flat even field with no floor line, each shadow staying
    under its own object.

17. **Marks as pattern.** Faces are told apart by pattern, color, or placement,
    not damage, and no face pairs "unblemished" with a dark mark.

### Text in image

18. **Text route.** No readable text by default; a blank surface or an angle
    that hides the print is preferred, and pseudo-letters count as invented
    text. Identity-critical copy is acquired or finished
    deterministically; model text appears only when the user has said it is
    acceptable, never on a conditional or hypothetical mention. A fictional
    identifier is quoted once and reads identically on every view.

### Constraints

19. **Common negatives.** No hands or people, no other objects or duplicates, no
    unwanted background, no readable text or logos, no cropped edges, no boxes,
    frames, borders, or divider lines, no extra views, labels, or captions, no
    watermark — only those that apply.

### Workflow

20. **Element saved.** `prop_<prop-id>_<view>_vNN.png` under
    `elements/<prop-id>/` with a same-stem `prompt_prop_` snapshot.

21. **Selected variant.** Approved filename recorded as `selected_variant` in
    the element manifest.
