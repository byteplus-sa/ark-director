---
name: seedance-prompt-25
description: >
  Write production-grade Seedance 2.5 video prompts with the flexible six-part
  formula, 50-material multimodal referencing, variable-duration scene staging
  (4-30s), timestamp pacing, structured video editing (subject replacement,
  background replacement, audio editing), forward and backward video extension,
  keyframe sequences, storyboard grids, coarse and fine blockout references,
  one-click video, seamless transitions, audio bracket syntax, dialogue
  language reinforcement, emotional direction, and camera language. Use this
  skill for Seedance 2.5 prompts, multi-reference asset orchestration, scene
  staging, video editing, extension, and corrections to generated motion or
  continuity. For legacy Seedance 2.0 prompts, use seedance-prompt-20 instead.
  For 4K output resolution (unsupported by 2.5) or Fast/Mini speed variants,
  also use `seedance-prompt-20`.
---

# Seedance Prompt

Write production-grade prompts for the BytePlus Seedance 2.5 video generation
model. Seedance 2.5 generates **up to 30 seconds** of video with native audio in
a single pass (set the actual duration via the `duration` parameter — 30s is
the ceiling, not the target), accepts up to **50 multimodal reference
materials**, and supports video editing, extension, one-click video, and
seamless transitions. The model co-generates audio and video in one latent
space, so sound direction in the prompt shapes the final result.


## Input and output contract

Input: a video brief, resolved model/operation, duration policy, ordered input
roles, approved relevant Elements, and any current motion/blockout manifest
selected for intentional conditioning.

Output: a six-part prompt, reference bindings, applicable mode parameters,
explicit appearance and motion authorities, and observable acceptance criteria
for each critical action beat.

## Procedure and reference loading

Use reference-inputs for R2V; video-editing for edits; video-extension for
extensions; keyframes-storyboards-blockouts for approved visual conditioning
and validated blockout manifests. Add audio-performance-camera only for
applicable dialogue, acting, UI, or camera detail.

Read only the mode-specific resources needed for the request. Reference paths
mentioned in prose are relative to this skill directory unless a link says otherwise.

- [Reference Inputs](references/reference-inputs.md) — Reference materials; Multi-reference workflow (5 steps).
- [Scene Action](references/scene-action.md) — Scene staging; Action description.
- [Audio Performance Camera](references/audio-performance-camera.md) — Special audio and text syntax; Emotional direction; Scripted dialogue for all speaking characters; Describing screen and UI layout positively; Camera language; Video call scenes; Spatial continuity.
- [Video Editing](references/video-editing.md) — Video editing.
- [Video Extension](references/video-extension.md) — Video extension.
- [Keyframes Storyboards Blockouts](references/keyframes-storyboards-blockouts.md) — Keyframes, storyboards, and blockouts.
- [Transitions And One Click](references/transitions-and-one-click.md) — One-click video; Seamless video transitions.
- [Repair Examples](references/repair-examples.md) — Read after specific identity or geography feedback; hypothetical minimal repairs and tradeoffs.
- [Worked Examples](references/worked-examples.md) — Full example: T2V 30-second one-take; Full example: R2V multi-reference concert; Full example: Video editing — subject replacement.
- [Parameter Reference](references/parameter-reference.md) — Quick reference card; Guide disclaimer.

## Submission boundary and failure behavior

The caller owns production authorization, the exact request preflight, and the
complete hash-bound prompt review. A leaf returns its prompt package without
loading sibling skills. An explicitly declared orchestrator may coordinate the
review and submission stages. Missing required inputs remain unresolved; a draft
or technical success does not establish user approval. Preserve optional timing,
the three-image sampling default where applicable, and the requested delta.

## Evidence and creative advice

Distinguish four kinds of guidance when they affect a decision: **API requirement**
(verify with the selected live tool and its current source), **documented prompting
convention** (attribute to the linked guide), **observed result** (identify the
actual artifact, model and conditions), and **optional artistic technique**
(a hypothesis or choice to test). Model/price tables are reference snapshots,
not live capability evidence. Examples without linked result evidence are
hypothetical; do not describe them as proven improvements. Keep these labels in
reasoning or evaluation notes when useful, not boilerplate in every final prompt.

## Source authority

The prompt structure and rules in this skill are sourced from the official
Dreamina Seedance 2.5 Prompt Guide:
- [Seedance 2.5 Prompt Guide (Lark)](https://bytedance.larkoffice.com/docx/A88jd0B47oAd8zxWp5ycZFMfnxh)
- [Seedance 2.5 Launch Blog](https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5)
- [BytePlus ModelArk Model List](https://docs.byteplus.com/en/docs/ModelArk/1330310)
- [Seedance 2.0 Prompt Guide](https://docs.byteplus.com/en/docs/ModelArk/2222480) (legacy — for 2.0, use `seedance-prompt-20`)

When the official guide is updated, prefer the live page over this skill where
they conflict.

## Core prompt formula

> **Subject + Action or Event + Scene and Environment (optional) + Visual Style (optional) + Camera Movement/Cut (optional) + Audio (optional)**

Only **Subject + Action** is required. Every other part is optional — omit what
does not apply. Summarize the main action first; add detail only to critical
movements. Write the Action slot as granular physical detail — see
[Action description](references/scene-action.md#action-description). **Do not describe the same action
twice.** Generation parameters (duration, resolution, aspect ratio) belong in
the generation interface or API, not in the prompt.

```
<Subject> performs <primary action or event> in <scene and environment>.
The visuals feature <visual style>.
Use <shot size, camera angle, camera movement, or cuts>.
Audio includes <dialogue, ambience, sound effects, or music>.
```

### Visual Style slot composition

When combining multiple Visual Style presets (lighting, lens character, color
grade, sensor/film look), chain them in this order within a single "The visuals
feature ..." sentence:

> **lighting → lens character → color grade → sensor/film look**

Example with three presets active:

```
The visuals feature warm golden key light from screen-right, shallow depth of
field with compressed bokeh, a teal-and-orange cinematic grade, and subtle
film grain with soft halation.
```

Each preset skill (`seedance-lighting-presets`, `seedance-lens-presets`,
`color-grade-palettes`) produces one phrase; this rule defines how they
assemble. Use only the presets the user requested — do not pad the slot with
unused defaults.

### Example

```
A ceramic artist finishes a pale blue cup in a studio at dawn, lifts it from the wheel,
and places it in the center of a wooden shelf.
Soft morning light enters through the window. The wet clay has a delicate sheen, and the
workbench remains tidy.
Begin with a medium shot of the wheel-throwing process, slowly push in toward the cup's
surface texture, then cut to a frontal view of the shelf.
Retain the low hum of the pottery wheel, the friction of clay, and subtle indoor ambience.
```

### Stylized animation medium

When the user requests claymation, felt, wood puppets, toy miniatures, vintage
cel/rubber-hose animation, painterly 2D, handcrafted 3D, silicone creatures,
wax crayon, or another medium whose material behavior must persist through
motion, compose with the `seedance-animation-styles` skill, which owns the
medium, construction, deformation, craft-imperfection, and still-anchor
contract; this skill remains the authority for the full six-part prompt,
reference roles, scene staging, timestamps, audio syntax, and generation
limitations.

### Music-video treatment

When the prompt's timing, energy, and structure must follow a song — music
video, lyric video, visualizer, or performer-driven clip — compose with the
`seedance-music-video` skill, which owns the format selection, song-section
map, beat/cut-density contract, audio-first lip-sync contract, and per-genre
style lock; this skill remains the authority for the six-part formula, reference
roles, audio bracket syntax, timestamps, and generation limitations.

## Parameter auto-lock rules

Three task types automatically lock generation parameters based on input materials:

| Task Type | Aspect Ratio | Duration |
|---|---|---|
| **Video editing** | Locked to input video's ratio; **cannot be set** | Locked to ~input duration (±0.3s); **cannot be set** |
| **First/last-frame generation** | Locked to **first image's ratio**. First & last must match | Can be set |
| **Video extension** | Locked to input video's ratio; **cannot be set** | Can be set |

## Revision contract

When revising an existing take, record the creative delta before rewriting:

```text
Locked decisions:
- [approved identity, action, camera, environment, audio, and boundary behavior]

Requested delta:
- [the one behavior that must change]

Acceptance criteria:
- [observable conditions that make the next take pass]

Known rejections:
- [behaviors from earlier takes that must not return]
```

Carry locked decisions into the revised prompt. Change one of prompt wording,
reference bundle, or motion design at a time when practical so the cause of
improvement or regression remains identifiable.

## Authority split for 3D-assisted video

State authority by attribute, not by asset type alone:

- An animated blockout video may own motion, camera, cuts, blocking, and
  timing while explicitly supplying no appearance.
- A generated or modeled 3D asset may own structure and appearance while
  supplying no motion unless an animated render is also selected for that role.
- Character, product, prop, and location sheets own only their named identity,
  materials, or environment attributes.
- Text resolves intent and dressing but does not override a selected video
  motion master.

When a validated blockout manifest is supplied, derive subject mappings,
action windows, and measurable motion acceptance criteria from it. Do not
retype or reinterpret the Blender object map from memory. Keep measurements in
review metadata; translate them into observable prompt language rather than
claiming the model guarantees numeric precision.

## Preflight review

Before generation, verify:

1. **Subject & action**: Does the prompt clearly state the subject and primary action?
2. **Reference roles**: Does every reference state what to use and what not to use?
3. **Subject binding**: Is every required canonical character, product, and prop named and bound to a reference, with incidental objects handled by the prop threshold?
4. **Scene selection**: Are references selected by scene, not forced to appear all at once?
5. **Stage structure**: Does each stage contain only one primary change and a clear end state?
6. **Consistency**: Do character count, clothing, prop ownership, and spatial relationships stay consistent?
7. **Editing master**: For editing, is the sole editing master, edit scope, target quantity, and content to preserve defined?
8. **Emotion & camera**: Are abstract emotions and cinematography terms paired with visible/audible cues?
9. **First/last frames**: Are first/last frames assigned one role per image? Do first and last share aspect ratio?
10. **Storyboards & blockouts**: Does the storyboard state which structure to inherit? For blockouts, is coarse vs fine identified? Is a video-lock master treated as the sole motion authority, re-dressed not re-imagined?
11. **Auto-lock rules**: Do editing, first/last-frame, and extension follow their locked aspect-ratio and duration rules?
12. **Extension boundary**: For extension, are the boundary image, motion trend, and audio continuity checked?
13. **One-click video**: Are material roles, image order, motion amount, editing style, and audio defined?
14. **Seamless transitions**: Are the two videos' roles, trigger action, transition process, and arrival state defined?
15. **Action granularity**: Is the primary action described at the body-part level with range, speed, force, and physics grounding — not as a bare verb?
16. **Motion acceptance**: Does every critical movement have an observable
    direction, relationship, contact, or end-state criterion? Could camera
    movement falsely appear to satisfy required subject movement?
17. **Manifest currency**: When a blockout manifest exists, do its source,
    previz, selection, and reference hashes match the generation package?

## Usage limitations

- Timestamps allocate time to events; they are **not frame-accurate edit points**.
- Video-editing prompts improve the probability of alignment but cannot guarantee frame-by-frame overlap.
- Multi-reference goal is to select and combine correct materials, **not** to make every material appear at once.
- For subtitles, formulas, signs, product specs, or frame-level timing that must be completely accurate, use prepared reference materials, video generation, and post-production together.
- Video editing locks input aspect ratio and approximate duration (±0.3s); neither can be set separately.
- First/last-frame generation locks aspect ratio to the first image; duration can be set. Mismatched ratios may stretch the last frame.
- Video extension locks input aspect ratio; extension duration can be set.
- For one-click video, specify image order and character mapping explicitly if they matter.
- Seamless transitions aim for visual/audio continuity; they do not guarantee pixel-identical preservation.
- A generated 3D asset is not a motion reference unless an animated render is
  intentionally bound as the supported motion-master input.
- Contact sheets can support appearance review but cannot verify temporal
  motion, timing, camera continuity, or audio.


## Intentional conditioning representation

A sketch or blockout stays `control_only: true` while it is analysis-only. To
use intentional conditioning, first obtain explicit selection of a derived
composition or motion reference. Record its exact selected manifest, current
SHA-256, `reference_image` or `reference_video` role, and `control_only: false`.
Confirm live model/mode support. Flipping the flag alone never grants approval;
the caller applies the [production policy](../../contracts/production-policy.md).
