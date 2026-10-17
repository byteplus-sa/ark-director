# Reference Inputs

Focused reference for `seedance-prompt-25`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Reference materials](#reference-materials)
- [Precedence and accepted inputs](#precedence-and-accepted-inputs)
- [Multi-reference workflow (5 steps)](#multi-reference-workflow-5-steps)

## Reference materials

### Limits and recommended ranges

Seedance 2.5 accepts up to **50 reference materials** per generation.

| Material Type | Input Limit | Recommended Range |
|---|---|---|
| Images | Up to 30, each ≤ 4K | Prefer 1–8 distinct subjects |
| Videos | Up to 10, combined ≤ 30s | Prefer 1–5 subjects, 5–10s each |
| Audio | Up to 10, combined ≤ 30s | Keep only directly relevant dialogue/voice/ambience/music |
| Video Editing | Source video + reference images | Source < 20s, 1–5 reference images |

You may push beyond recommended ranges (9–12 subjects in images, 6–10 in
audio/video, 6–8 editing refs), but **stability decreases** as count grows. If
>5 subjects need multiple views, use **separate images per view** — independent
view images are more stable than collages.

### Role definition syntax

After uploading references, specify exactly what each one contributes. Add
exclusions only when a person, background, or composition could unintentionally
leak into the output.

**Three non-negotiable rules:**
1. Put the material mapping **directly in the prompt**.
2. **Never make the model guess** which asset belongs to which person, prop, or scene.
3. Add `"Do not use..."` exclusions only when leakage is genuinely possible.

```
@Image 1 defines <subject>'s <appearance, clothing, structure, or material>.
@Video 1 defines <motion, camera movement, or pacing>.
@Audio 1 defines <character or sound type>'s <voice, dialogue, ambience, or music>.

<Subject> completes <primary action or event> in <scene>.
The visuals feature <visual style>, with <camera treatment>.
```

Add `"Do not use..."` exclusions **only** when a person, background, or
composition in the reference could unintentionally leak into the output. You do
not need one for every asset.

### Multiple views of the same subject

When several images show different angles of one person or product, state this
explicitly:

```
@Image 1 defines the front view of the same folding desk lamp.
@Image 2 defines the left-side structure of the same folding desk lamp.
@Image 3 defines the right-side structure of the same folding desk lamp.
@Image 4 defines the rear structure of the same folding desk lamp.
All four images define one folding desk lamp. The output must contain only one lamp throughout.
```

### Inheritance from reference videos

If a reference video already defines the motion, camera movement, and sequence
accurately, **state only which attributes to inherit** — do not restate every
action. Repeating the motion description may **conflict with the reference
itself**. A blockout video mainly provides motion and spatial structure, so the
prompt must still define the intended subjects, scene, action, and visual style.

### Reference classification

Classify each reference by how it may influence visible output:

- **Visible identity** — character, creature, costume, prop, or vehicle that should appear.
- **Visible environment** — location, lighting, weather, or production design that should appear.
- **Motion or camera reference** — movement language to transfer without copying pixels.
- **Control-only reference** — route map, blocking diagram, timing chart, or other planning material that must not appear.

Every supplied image can leak visible pixels, colors, lines, labels, or
composition into the result. For a control-only image, prefer translating its
information into concise textual choreography and omitting the image. Reference
content can overpower negative wording — if a character sheet contains an aura,
weapon, logo, or extra face that must not appear, clean or replace the reference
rather than relying on "no aura" constraints.

## Precedence and accepted inputs

- **A bound photo outranks text for details it shows.** Landing gear that is
  down in the reference stays down whatever the prompt says. Align the text
  with the reference, or replace the reference.
- **People in video inputs.** Extension and video-to-video inputs that contain
  generated or real people are rejected for privacy unless those people are
  `asset://` Virtual Portrait assets. Real-person reference photos are rejected
  without an authorized asset. Compose with `seedance-virtual-portrait` for the
  asset route; never disguise an input to pass the check.
- **Face and body crops** bound as `reference_image` may be rejected; bind the
  full sheet, or use the image as a first frame. A last frame alone is
  rejected; use first + last.
- **Storyboards and boards are never inputs**; see
  [Keyframes Storyboards Blockouts](keyframes-storyboards-blockouts.md#storyboards-are-never-bound).

## Multi-reference workflow (5 steps)

When working with many references, the goal is **not** to put every reference
into one sentence. The goal is to define relationships and help the model
select the correct materials for each scene.

> **Define Each Material's Role → Map Subjects → Group by Type → Create Subject Profiles → Select References by Scene**

### Step 1: Name and map each subject individually

```
<Character A> corresponds to @Image 1. Use only the appearance, hairstyle, and clothing.
<Character B> corresponds to @Image 2. Use only the appearance, hairstyle, and clothing.
<Prop A> corresponds to @Image 3. Use only the structure, material, and color.
<Scene A> references @Image 4. Use only the spatial layout, architecture, and lighting. Do not use the people in the image.
```

Do **not** write `"@Images 1 through 4 define four characters respectively."` —
it never says which image maps to which character.

### Step 2: Group materials by type

```
[Characters]
<Conservator> corresponds to @Image 1. Use only the appearance, hairstyle, and clothing.
<Registrar> corresponds to @Image 2. Use only the appearance, hairstyle, and clothing.
<Exhibition Installer> corresponds to @Image 3. Use only the appearance, hairstyle, and clothing.
<Guide> corresponds to @Image 4. Use only the appearance, hairstyle, and clothing.
Do not interchange the four characters' appearances, clothing, actions, positions, or dialogue.

[Props]
<Sample Case> corresponds to @Image 5 and belongs only to <Conservator>.
<Record Board> corresponds to @Image 6 and belongs only to <Registrar>.

[Scenes]
<Conservation Lab> references @Image 7. Use only the space, materials, and lighting.
<Gallery> references @Image 8. Use only the space, materials, and lighting.

[Motion and Audio]
@Video 1 defines the motion of <Conservator> opening <Sample Case>. Do not use the person or scene from the video.
@Audio 1 defines <Guide>'s voice and specified dialogue.
```

### Step 3: Create a centralized profile for important subjects

When the same character uses several references across multiple scenes:

```
[Subject Profile: Conservator]
Appearance and clothing: @Image 1.
Fixed prop: <Sample Case> from @Image 5.
Locations: <Conservation Lab> and <Gallery>.
Motion references: the case-opening motion from @Video 1 and the sample-placement motion from @Video 2.
Do not use: other characters' clothing. Do not give this character <Record Board> or guide equipment.
```

### Step 4: Select references by scene

Each scene names **only** the assets it uses, the event, and the required end
state:

```
Scene 1 | Inspection in the Conservation Lab
Use: <Conservator>, <Sample Case>, <Conservation Lab>, and the case-opening motion from @Video 1.
Event: <Conservator> opens <Sample Case> at the workbench and inspects the sample inside.
End state: <Conservator> remains on the inner side of the workbench. <Sample Case> stays beside the
conservator's right hand, frame-left.

Scene 2 | Registration in the Gallery
Use: <Registrar>, <Record Board>, and <Gallery>.
Event: <Registrar> checks the number on <Record Board> beside the display case.
End state: <Registrar> still holds <Record Board> with both hands. No other character enters the
display-case area.
```

> The goal is to help the model select the correct materials for the current
> scene, **not** to make every material appear at the same time.
