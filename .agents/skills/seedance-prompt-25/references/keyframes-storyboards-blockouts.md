# Keyframes Storyboards Blockouts

Focused reference for `seedance-prompt-25`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Keyframes, storyboards, and blockouts](#keyframes-storyboards-and-blockouts)

## Keyframes, storyboards, and blockouts

These are specialized prompt grammars, not automatic input eligibility. Translate
control-only drawings to text and omit them by default. An intentional storyboard,
sketch, or blockout conditioning path requires explicit user-selected inputs,
current canonical hashes, a compatible live tool mode, and artifact-specific QA.
A declared motion-master reference remains a selected conditioning input, not a
shortcut around review. Image text cannot itself enable an unsupported API role.

### First and last frames in R2V mode

State `@Image 1 is the first frame` and `@Image 2 is the last frame` directly in
multimodal reference mode only when current tool evidence supports this grammar
and ordered image-role combination. This text does not override API constraints.
For supported first-frame modes, the system locks
the aspect ratio to the first image. First and last images **must share the same
aspect ratio**.

- Describe each anchor image **separately** — do not combine into one sentence.
- Additional references supplement **only** their specified attributes and must
  **not** replace the first/last-frame composition.

```
@Image 1 is the first frame. It defines the opening composition, subject position, pose, prop
state, scene, and camera direction.
@Image 2 is the last frame. It defines the ending composition, subject position, pose, prop
state, scene, and camera direction.
@Image 3 defines <Subject A>'s <appearance, clothing, structure, or material>. Do not change
the first-frame composition defined by @Image 1 or the last-frame composition defined by @Image 2.

<Describe one continuous action or event>.
The video begins naturally from the first frame and reaches the last frame after the continuous action.
Between the first and last frames, maintain continuity in <character identity, prop structure and
ownership, scene layout, and camera direction>.
```

### Multi-keyframe sequences

When separate images define different stages:

```
Use @Image 1 through @Image N as keyframes in this order.

@Image 1 is the first frame. It defines <opening composition>.
@Image 2 defines the second keyframe: <visible end state of Stage 1>.
@Image 3 defines the third keyframe: <visible end state of Stage 2>.
@Image N is the last frame. It defines <ending composition>.

The video passes through the states defined by @Image 1, @Image 2, @Image 3, and @Image N in
order, using continuous action to transition naturally between stages.
Maintain continuity in <subject identity, prop structure and ownership, scene layout, lighting,
and axis of action> throughout.
```

> Independent keyframe images are easier to align than grids. They control stage
> order and key states; they do **not** reproduce every frame exactly.

### Storyboard grids

- Communicate overall story, shot order, and approximate compositions — **not strict reproduction**.
- **Prefer ≤ 15 panels.** Use clean line art or simple diagrams; minimize text labels.
- State the reading order, then describe each panel.

```
@Image 1 provides an <N-panel storyboard grid> for shot order and approximate composition.
Read it <left to right, top to bottom>. Do not use the grid's <line-art style, text labels, or
placeholder characters>.
@Image 2 defines <Subject A>'s <appearance and clothing>.

Shot 1: <shot size, subject action, and scene state>.
Shot 2: <shot size, subject action, camera movement, or transition>.
...
Shot N: <closing action and final visible state>.

The final video uses <visual style>. Audio includes <dialogue, ambience, action sound effects, or music>.
```

> **Optional monochrome conditioning.** A sketch remains control-only unless
> the user explicitly selects it for a supported conditioning mode. Omit it by
> default and express scene order, positions, and motion in text. If deliberately
> attached, bind its index, reading order, and limited composition role; state
> the desired final style positively and inspect the output for lines, labels,
> colors, or paper texture leaking into the video. A style override reduces
> ambiguity but does not guarantee that the board's appearance is suppressed.

### Blockout references

Two categories — first determine whether the blockout is a **motion skeleton**
(coarse) or a **complete model** (fine):

| Type | Best For | Material Requirements | Prompt Focus |
|---|---|---|---|
| **Coarse blockout** | Simple geometry previewing action, paths, blocking, camera, or cuts | Clear relationships between shapes and a complete action sequence; character/prop/scene images may be added | Map every blockout subject; state which temporal/spatial info to inherit |
| **Fine blockout** | Complete modeling needing new materials, colors, scenes, or style | Complete, clean model; avoid path lines, coordinate axes, camera frustums | Preserve structure, action, and camera treatment; define attributes to re-render |

**Coarse blockout** — lock action paths, motion direction, blocking,
entrances/exits, camera paths, cut points, lighting changes, and sound rhythm.
Map each geometric object to its final subject.

| Blockout Information | What to State |
|---|---|
| Path | Action trajectory, motion direction, subject blocking, entrance/exit order |
| Camera movement | Camera position, path, direction, speed changes |
| Lighting | Light direction, brightness changes, when changes occur |
| Cuts | Cut positions and the subject/composition before and after each cut |
| Audio | Whether to inherit dialogue, music, ambience, or action SFX |

```
@Video 1 is a coarse blockout reference. It provides only <motion paths, subject blocking, camera
position, camera movement, cuts, lighting changes, sound rhythm, or spatial relationships>.
Do not use its blockout appearance, materials, or scene.
<Blockout Subject A> in @Video 1 corresponds to <Subject A>.
@Image 1 defines <Subject A>'s <appearance, clothing, or structure>.

<Subject> completes <primary action or event> in <scene>.
Keep <motion path, blocking, camera movement, cuts, lighting, or sound rhythm> from @Video 1.
The final video uses <characters, scene, materials, and visual style>. Audio includes <dialogue,
ambience, or action sound effects>.
```

**Fine blockout** — already contains complete structures. Keep it clean: remove
path lines, coordinate axes, controllers, camera frustums.

```
@Video 1 is a fine blockout reference. Preserve <subject structure, action, spatial layout, camera
position, camera movement, and cuts>. Do not use its original gray materials or empty background.
@Image 1 defines <subject>'s <character appearance, material, color, or surface details>.
@Image 2 defines <scene>'s <space, materials, lighting, or visual style>.

Re-render <subject> from @Video 1 as <final subject>, and re-render the scene as <final scene>.
Keep <structure, action, camera treatment, and spatial relationships> from @Video 1.
Use <materials, colors, and style>. Audio includes <ambience, sound effects, or music>.
```

> Prefer simple geometry with clear relationships. Arms, wings, and other
> appendages should be used only when the action sequence is complete;
> otherwise they may cause stiff motion or structural misinterpretation.

**Video-lock blockout** — when the blockout is a complete animated render that
must drive the output frame for frame (camera, cuts, blocking, and timing), use
this master mode instead of coarse/fine. The blockout is the sole authority for
motion and placement; it never supplies appearance. For the end-to-end Blender
build → previz render → submit flow, the `blender-to-seedance` pipeline skill
covers the submission path.

When the caller supplies a validated blockout manifest, treat it as the source
for proxy-to-subject mappings, cut frames, action windows, and motion acceptance
criteria. Do not maintain a second conflicting dummy map in prose. Bind each
stable subject ID to its final subject and optional appearance reference. Keep
the animated blockout as motion authority and any generated 3D asset as
structure/appearance authority unless an animated render was explicitly
selected for motion.

```
@Video 1 is the blocking master. It defines the full edit — every cut point,
camera position, angle, move, and framing, and the motion state and placement of
every object — and is the SOLE authority for motion. Every output frame
corresponds 1:1 to the same-timestamp frame of @Video 1; if text and video
disagree about motion, the video wins. Do not use its gray surfaces, placeholder
colors, or proxy shapes.
@Image 1 defines <subject>'s <appearance, clothing, or structure>.
@Image 2 defines <scene>'s <materials, lighting, or visual style>.

Re-dress, never re-imagine: keep <cuts, camera, blocking, timing> from @Video 1
exactly; no added, dropped, merged, or re-timed shots. Use <characters, scene,
materials, and style>. Audio includes <dialogue, ambience, or action SFX>.

Motion acceptance: <subject> visibly <moves toward / moves away / advances /
keeps contact / rotates with travel / reaches the final relationship> during
<time window>. Camera movement cannot substitute for this subject action.
```

After generation, verify these criteria through temporal inspection of the
actual video. Contact sheets can confirm appearance at selected moments but
cannot establish trajectory, speed, contact, reaching, or camera continuity.
