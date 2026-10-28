---
name: seedance-prompt-25
description: >-
  Write production-grade Seedance 2.5 video prompts with the flexible six-part
  formula, per-shot camera, lens and light lines, 50-material multimodal
  referencing, variable-duration scene staging (4-30s), timestamp pacing and
  dialogue timing, structured video editing (subject replacement, background
  replacement, audio editing), forward and backward video extension, keyframe
  sequences, coarse and fine blockout references, one-click video, seamless
  transitions, audio bracket syntax, dialogue language reinforcement, emotional
  direction, camera language, and draft-first request packaging. Use this
  skill for Seedance 2.5 prompts, multi-reference asset orchestration, scene
  staging, video editing, extension, and corrections to generated motion or
  continuity. For legacy Seedance 2.0 prompts, 4K output through 2.0, or the
  Fast/Mini speed variants, use seedance-prompt-20; whitelist-only 2.5 Premium
  (4K) uses this skill.
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
For new or revised character performances, consume the caller's performance
plan and encoded beat cues; for staged fights, also consume the choreography
ledger. Missing intentions, listener tasks, critical triggers or end states
remain unresolved rather than being replaced by emotion adjectives.

Output: a six-part prompt, reference bindings, applicable mode parameters,
explicit appearance and motion authorities, and observable acceptance criteria
for each critical action beat.
Preserve the caller's compact premise, early sound/editorial intent and
project-specific criteria. Missing material intent remains a handoff question;
settled single-prompt edits do not acquire an alternatives exercise.
Body speed, amplitude, interruptions and recovery follow source intent and
plausibility, with no universal burst cap. Speech is not a kinetic exclusion;
actor energy, camera energy and edit rhythm must preserve required readability.
Coverage and duration serve perception, not contrast, turn, hold or `wow` quotas.

## Procedure and reference loading

Use scene-action for new action; reference-inputs for R2V; video-editing for edits; video-extension for
extensions; keyframes-storyboards-blockouts for keyframes, boards and validated
blockout manifests; shot-staging for any clip that cuts or carries dialogue.
Add audio-performance-camera only for applicable dialogue, sound, acting, UI, or
camera detail.

When packaging generation parameters, read the parameter reference: a Seedance
2.5 clip is drafted first (boolean `draft: true`, `resolution: "480p"`) and the selected draft is
promoted by `draft_task_id`, so every prompt, reference, duration and audio
decision is final before the draft. This applies in every review mode, including
edits, extensions, probes and variants, with no skip-draft override.
Resolve capability or transport conflicts before
submission; never drop `draft` to submit plain 480p.

Read only the mode-specific resources needed for the request. Reference paths
mentioned in prose are relative to this skill directory unless a link says otherwise.

- [Reference Inputs](references/reference-inputs.md) — Reference materials; Multi-reference workflow (5 steps).
- [Scene Action](references/scene-action.md) — Scene staging; Action description; Counts, hands and surfaces; Progressive change.
- [Shot Staging](references/shot-staging.md) — Shots or stages; Building a spot from sequences; Per-shot template; Carrying a shot plan; Dialogue inside shots.
- [Audio Performance Camera](references/audio-performance-camera.md) — Special audio and text syntax; Choosing the audio route; Emotional direction; Scripted dialogue for all speaking characters; Describing screen and UI layout positively; Camera language; Video call scenes; Spatial continuity.
- [Video Editing](references/video-editing.md) — Video editing.
- [Video Extension](references/video-extension.md) — Video extension.
- [Keyframes Storyboards Blockouts](references/keyframes-storyboards-blockouts.md) — Keyframes; why boards are never bound; blockouts.
- [Transitions And One Click](references/transitions-and-one-click.md) — One-click video; Seamless video transitions.
- [Repair Examples](references/repair-examples.md) — Read after specific identity or geography feedback; hypothetical minimal repairs and tradeoffs.
- [Worked Examples](references/worked-examples.md) — Three-shot R2V sequence with dialogue; ambient-only one-take; video editing subject replacement.
- [Parameter Reference](references/parameter-reference.md) — Quick reference card; Draft mode; Guide disclaimer.

## Submission boundary and failure behavior

The caller owns production authorization, the exact request preflight, and the
complete hash-bound prompt review. The caller reviews inline by default and
uses a sub-agent only when the user explicitly requests sub-agent prompt review
for the project or specific generation. A leaf returns its prompt package without
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
Dreamina Seedance 2.5 Prompt Guide, plus these public pages:
- [Seedance 2.5 Launch Blog](https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5)
- [BytePlus ModelArk Model List](https://docs.byteplus.com/en/docs/ModelArk/1330310)
- [Seedance 2.0 Prompt Guide](https://docs.byteplus.com/en/docs/ModelArk/2222480) (legacy — for 2.0, use `seedance-prompt-20`)

When the official guide is updated, prefer the live page over this skill where
they conflict.

## Core prompt formula

> **Subject + Action or Event + Scene and Environment (optional) + Visual Style (optional) + Camera Movement/Cut (optional) + Audio (optional)**

Only **Subject + Action** is required for a valid prompt. Every other part is
optional in the grammar, but a narrative, ad or music-video shot is not finished
at that minimum: its Camera and light source are craft requirements, taken from
the scene's shot plan (see [Shot Staging](references/shot-staging.md)) or
recorded as a static choice with a reason. Summarize the main action first;
add detail only to critical movements. Write the Action slot as granular physical detail — see
[Action description](references/scene-action.md#action-description). **Do not describe the same action
twice.** Generation parameters (duration, resolution, aspect ratio, audio on
or off) belong in the request, not the prompt: a sentence such as "composed for
2.39:1" or "a 30-second 16:9 video" is wrong (`prompt.parameters_in_request`).

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
field with compressed bokeh, and the teal-and-orange cinematic grade the brief
requested.
```

Each preset skill (`seedance-lighting-presets`, `seedance-lens-presets`,
`color-grade-palettes`) produces one phrase; this rule defines how they
assemble. Fill the slot from the shot plan or the user's request — do not pad it
with unused defaults or competing presets. In a clip that cuts, the grade stays
in the shared opening and each shot line carries its own light fact.

### Example

```
A ceramic artist finishes a pale blue cup in a studio at dawn, lifts it from the wheel,
and places it in the center of a wooden shelf.
Soft morning light enters through the window at frame-left. The wet clay has a delicate
sheen, and the workbench remains tidy.
Begin with a medium shot of the wheel-throwing process, slowly push in toward the cup's
surface texture, then cut to a low frontal view of the shelf as she sets the cup down
with her right hand, frame-left.
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

## Prompt hygiene that changes results

These habits come from reviewed takes; each has a rule ID that `prompt-review`
checks, so the reasons live here and the checks live there.

- **Say what you want to see** (`prompt.positive_direction`). A negation does not
  remove a strong visual prior: "never a cone" still draws a cone. Describe the
  wanted shape, state or layout. Night is "black sky, low exposure, a small pale
  moon", not "not daytime".
- **Pin every count** (`prompt.exact_counts`). Counted items, clones, runners and
  crowds drop or duplicate. Name each item by size or position, keep all of them
  in open view from the first frame, restate the count and positions at every
  stage, and never mention spare copies lying around.
- **Name hands by anatomy and frame side** (`prompt.hand_frame_side`): "her right
  hand, frame-left". The model reads left/right as the character's own side.
- **Keep frames text-free** (`video.text_free`). No captions, subtitles, titles,
  CTAs, logos or end cards in the footage; they are added in post. Generic
  tubes, jars, jugs, hard cases, garment labels, tickets and generated screens
  grow invented lettering: describe them as plain ("plain white ceramic jug,
  smooth solid surface, nothing printed"), leave them out, or give a story prop
  a reference sheet.
- **Bound photos outrank text.** A detail visible in a bound reference (landing
  gear down) wins over contrary text; change the reference, not the adjectives.
- **Write hair past covering garments.** Hair length drifts under shawls and
  blankets; state the hair falling over the garment.
- **Choose the audio route before writing** (`audio.native_route`). Ambient-only,
  score-driven and speech-free pieces are picture-only requests; see
  [Choosing the audio route](references/audio-performance-camera.md#choosing-the-audio-route).
- **Budget speech** (`dialogue.speech_budget`); see
  [Dialogue inside shots](references/shot-staging.md#dialogue-inside-shots).
- **Never bind a board** (`board.animatic_review_only`); see
  [Keyframes Storyboards Blockouts](references/keyframes-storyboards-blockouts.md).

## Preflight review

Before handing the package to review, confirm:

1. Subject and primary action are clear, and the action is at body-part level
   with an observable end state for every critical beat.
2. Every reference has one stated role, subjects are bound individually, and
   references are selected by scene.
3. Every shot or stage carries its planned size, angle, move and named light,
   or a recorded static reason; shot count and lengths fit the duration.
4. Performance intentions, triggers, registration and listener responses reach
   the prompt with framing-readable consequences (`acting.plan_bound`).
   Staged fights retain actor/prop state and readable action, apparent contact
   or avoidance, and reaction chains (`fight.readable_exchange`). Stillness and
   deliberate non-response remain valid; mood labels alone are insufficient.
5. The hygiene items above hold: positive wording, counts, frame-side hands,
   text-free frames, no parameters in the text.
6. Spoken lines fit the speech budget; the audio route matches the piece.
7. Mode rules hold: auto-locked ratio and duration for edit, frames and
   extension; one editing master; first and last frames share a ratio.
8. For blockouts, coarse, fine or video-lock is identified and a manifest's
   hashes match the package; camera movement cannot stand in for required
   subject movement.
9. Every new generation request is a native Draft (boolean `draft: true`,
   `resolution: "480p"`), and the final is promoted from the reviewed and
   selected draft with `draft_task_id` and only output settings.

## Usage limitations

- Timestamps allocate time to events; they are **not frame-accurate edit points**.
- Video-editing prompts improve the probability of alignment but cannot guarantee frame-by-frame overlap.
- Multi-reference goal is to select and combine correct materials, **not** to make every material appear at once.
- For subtitles, formulas, signs, product specs, or frame-level timing that must be completely accurate, keep the footage text-free and add the exact layer in post.
- Mismatched first/last-frame ratios may stretch the last frame (auto-lock rules above).
- About 0.8 s per shot is a provisional caution, not a provider limit or guaranteed merge threshold. Preserve requested timing; offer assembly for precision or demonstrated failure and return conflicts with locked workflows.
- A rack focus that leaves the subject soft mostly fails; the model keeps the face sharp. Add that defocus in post.
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
