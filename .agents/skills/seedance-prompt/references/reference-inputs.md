# Reference Inputs

Focused reference for `seedance-prompt`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Reference materials](#reference-materials)
- [Precedence and accepted inputs](#precedence-and-accepted-inputs)
- [Multi-reference workflow (5 steps)](#multi-reference-workflow-5-steps)

## Reference materials

### Scope and reference selection

These role mappings are 2.5-based prompting conventions, not an input schema.
Verify counts, sizes, durations, combinations and token syntax for the exact model,
operation and destination before execution. Historical snapshots live in
[Parameter Reference](parameter-reference.md); do not inherit them by family name.

Use only relevant references. Separate views can clarify the same subject's
structure; label them as one identity rather than inventing extra subjects.
More inputs can introduce conflicting authority, not a guaranteed fidelity gain.

### Role definition syntax

For each caller-selected reference, specify exactly what it contributes. Add
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
weapon, logo, or extra face that must not appear, propose an authorized reference
repair rather than relying on "no aura" constraints. Do not alter a locked input.

## Precedence and accepted inputs

- **Resolve conflicting visible details.** A bound photo can overpower contrary
  text. If landing gear is down but must be raised, propose aligning or replacing
  the reference with authorization, not stronger adjectives.
- **People in inputs.** Preserve independent face, likeness and voice rights.
  The caller verifies exact-model privacy rules and applicable `Active`
  authorized assets; creative approval alone is not provider authorization.
  Never disguise an input or substitute a raw recording to pass a check.
- **Face/body crops and frame roles** require current input eligibility.
  Rejection is not permission to switch to a first-frame route. Keep unknown
  combinations unresolved and propose only unselected alternatives.
- **Storyboards and boards are never inputs under workspace policy**, not
  because of a provider incapability claim; see
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

Use a stable subject label and a few distinguishing static features, such as
wardrobe, build or product structure. Reuse the label across shots; do not encode
temporary poses or emotions as identity. Number typed references independently
in supplied order. The `Define` form is an optional legacy convention, not a
mandatory heading or API token; internal asset IDs do not explain visible content.

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
