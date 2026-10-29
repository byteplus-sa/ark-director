---
name: seedance-graybox-world
description: >
  Write Seedance 2.5 prompts for the Blender gray look — an untextured gray
  graybox / blockout 3D world with matcap-style shading, ambient-occlusion
  depth, a neutral gray viewport background, and clean mechanical motion, like
  Blender's Solid viewport or Material Preview on default gray materials. Use
  whenever the user asks for a "Blender-like world", "gray world", graybox,
  blockout, untextured 3D, previs or previz look, whitebox, layout pass,
  matcap gray, neutral gray studio, or a video that must look like a default
  Blender viewport render — even if they never say "graybox". Use only when
  gray IS the desired final look; when the user wants a coarse or fine
  blockout reference to re-render into final materials, use
  seedance-prompt-25's blockout-reference mode instead.
---

# Seedance Graybox World

Write ready-to-use Seedance 2.5 prompts for the Blender gray look: an
**untextured gray graybox / blockout world**. The whole scene reads as flat
mid-gray 3D geometry shaded only by ambient occlusion and one soft neutral
studio light, on a neutral gray background — the look of Blender's default
Solid viewport or Material Preview with untextured gray materials.

Prompt-composition only — this skill emits prompt text; it never calls models.

## Source basis

The gray look described here is the default Blender viewport shading documented
in the Blender Manual — Solid viewport shading (flat gray material preview,
ambient-occlusion, neutral background) and Material Preview (matcap / studio
HDRI gray lighting):

- https://docs.blender.org/manual/en/latest/editors/3dview/display/shading.html
- https://docs.blender.org/manual/en/latest/editors/3dview/display/shading.html#material-preview-mode

The prompt grammar lives in the partner skill `seedance-prompt-25` (six-part
formula: Subject + Action + Scene + Visual Style + Camera + Audio). Compose with
it when writing a full prompt; this skill supplies the graybox look block only.

## What "graybox" means here

One material system, everywhere:

- **Single flat material.** Every surface is the same neutral mid-gray with no
  albedo texture, no metalness, no sharp environment reflections.
- **Shading is AO plus one soft light.** Depth comes from ambient occlusion in
  crevices, contact shadows, and a soft neutral studio/matcap gradient on
  curved surfaces. Flat faces stay flat. No colored light, no dramatic
  contrast, no filmic grade.
- **Geometry reads through silhouette and edges.** Clean contours, visible
  bevels, and facet edges on low-poly forms. Detail is geometric, not
  photographic.
- **Neutral gray background.** A flat mid-gray or a subtle vertical gray
  gradient, like the viewport background. An optional faint gray grid sits on
  the ground plane.
- **Mechanical motion.** Rigid, smooth, constant-speed transforms — turntable
  rotations, object translation — like a viewport tumble. No squash-and-stretch,
  no cloth, hair, or fluid unless the user explicitly asks.
- **People are gender-neutral mannequins.** Human figures render as
  gender-neutral articulated mannequins — jointed limbs, a featureless head,
  no skin, hair, facial features, or gendered clothing. Character reads through
  posture, gait, and motion only, never anatomy or costume.

This is the inverse of the `seedance-prompt-25` **blockout reference** modes
(coarse and fine), where gray geometry is a reference you re-render into final
materials. Here, gray **is** the final look, not an input to be replaced.

## When to use

- Previs / blockout pass — validate motion, geography, and camera before
  spending on final materials.
- A deliberately neutral, tool-like aesthetic: "Blender gray world", "default
  viewport look", "untextured 3D render".
- A product turntable or architectural walkthrough that should read as a clean
  gray model, not a textured scene.

## Figure contracts

### Scale contract

Every human figure is full adult height. When two or more figures share a
frame, set them near-equal in stature and state it plainly.

- Use absolute, repeated descriptors: `adult-height`, `near-equal in stature`.
- Never separate figures with relative size words such as "smaller", "larger",
  or "petite" — the model reads them literally, and a figure described as
  "slightly smaller" can render child-sized.
- Distinguish figures by role and position, not by size: `the pursuing
  mannequin`, `the second mannequin`.
- Repeat the scale descriptor in the Subject, the Look block, each relevant
  stage end state, and the Gray Seal, so scale cannot drift across cuts.

### Reaction-motion contract

Reactions read as whole-body movement, never a head-only turn.

- Write a turn as `pivots on its planted feet and turns its whole body, hips
  and shoulders rotating together as one rigid unit`.
- If a head motion is needed, bind it: `tilts its whole head on the neck joint
  by a fixed angle, body otherwise locked`.
- Mannequin figures tend to react with the head only; state the whole-body
  pivot explicitly, never imply it.

## Look block

Open every prompt with a medium-first sentence naming the construction,
shading, and background:

```text
An untextured gray graybox 3D world: every surface is flat neutral mid-gray,
shaded only by ambient occlusion and one soft neutral studio light, set against
a flat gray viewport background.
```

Then pin the look with the six elements below. Use only the toggles the user
requested — do not pad the block with unused defaults.

### Toggles

| Toggle | Positive wording |
|---|---|
| **Background — flat** | `flat mid-gray background with no horizon detail` |
| **Background — gradient** | `subtle vertical gray gradient background, slightly darker at the top` |
| **Grid floor** | `a faint gray grid lies on the ground plane, receding with perspective` |
| **Wireframe overlay** | `thin darker-gray edge lines trace the geometry contours` |
| **Faceted / low-poly** | `visible flat facets and hard edges, low-poly construction` |
| **Beveled / smooth** | `soft beveled edges and smooth curved surfaces` |
| **Turntable motion** | `the object rotates slowly at constant speed like a viewport turntable` |
| **Orbiting camera** | `the camera orbits slowly around the subject at constant speed` |

### Shading depth

State how depth is produced so the flat material still reads as 3D:

```text
Depth comes only from ambient occlusion in crevices and contact shadows where
surfaces meet; curved surfaces catch a soft neutral gradient, flat faces stay
uniform.
```

### Mechanical motion cadence

Use verbs that match rigid gray geometry:

- rotate, translate, hinge, slide, settle — smooth and constant-speed;
- weight shifts read as a pivot, not a squash;
- nothing bends, stretches, or compresses unless the scene is explicitly soft.

### Dynamic and action camera

The turntable and orbit toggles above suit product and architectural display
shots. For chase, action, or story sequences, prescribe a dynamic camera per
cut instead of leaving it implicit — a single tracking shot reads flat.

- Give each cut its own primary move and shot size, with cut timestamps aligned
  to stage boundaries: `Shot 1 (0-8s): fast low-angle tracking tight on the
  pumping legs and torso, the walls streaking past. At 8s, cut to ...`
- Make each camera beat resolve on a state that exists at that timestamp. A move
  aimed at a future beat (a push-in on an event that happens 7s later) can make
  the model jump the timeline.
- End the sequence with a terminal hold so the final frames are directed, not
  implied: `the push-in holds tight on the face-off for the remaining five
  seconds while both figures stay still`.
- One primary move and one secondary is a planning heuristic; preserve
  explicitly requested coherent choreography and resolve incompatible paths
  rather than dropping moves by count.
- Give every shot one action with its intent (`the pursuing mannequin lunges to
  close the gap`), a lens intent (`wide 24mm-equivalent depth`, `long-lens
  compression`) and the side of the single soft studio light (`key from
  frame-left`). About 0.8 s per shot is a provisional caution, not a provider
  limit or guaranteed merge threshold. Preserve requested timing; offer assembly
  for precision or demonstrated failure and return conflicts with locked workflows.

## Spatial and architectural lock

Continuity breaks at cuts, not within a shot. State geometry and travel once in
the Scene, then repeat the invariant in every stage and the Gray Seal.

- Assert architectural orientation positively: `the staircase descends
  continuously the whole way` — never rely on a single mention.
- State travel axis, subject order, and boundary behavior, and restate them per
  stage: `travel stays left-to-right`, `the pursuing mannequin stays behind the
  second until the landing`, `both figures remain fully in frame at all times`.
- Use ordered physical states, not relative verbs alone
  (`hall → colonnade → corner → corridor → open area`).
- Prefer same-plane obstacles (columns, barriers, doorways) over vertical
  traversal for the middle beats of an action scene. Vertical elements such as
  staircases are a drift risk — if one is required, assert its direction in
  every shot and be ready to replace it if a take flips it.

## Prompting workflow

### 1. Resolve the look

Confirm scope: pure graybox (default), or graybox plus one or two toggles
(grid floor, wireframe overlay, turntable/orbit). Keep toggles minimal — the
look is strongest when nothing competes with the gray.

### 2. Open with the medium-first sentence

Lead with the untextured gray construction and shading before any story action.
The model must know the material system governs everything before it reads the
event.

### 3. Translate the whole scene into the gray system

Apply the single gray material to every visible category:

- characters and figures become the gender-neutral articulated mannequins
  defined above;
- props, vehicles, and architecture become gray primitives and blocky masses;
- ground, sky, and background are flat or gradient gray (plus grid if requested);
- water, fire, smoke, dust, and debris become simple gray untextured volumes or
  particles — no colored flames, no photoreal spray.

Give effects a construction: gray voxel smoke, blocky gray dust puffs, simple
gray particle bursts.

### 4. Direct mechanical motion

Preserve object count, proportions, and construction while forms move. Rotation
and translation are constant-speed; joints pivot, parts slide. State the axis
and end state of each move so the model does not invent squash or flex.

### 5. Add two or three readability cues

Choose only what makes the gray readable:

- AO pooling in crevices and under overhangs;
- soft contact shadows grounding each object;
- a bevel highlight or facet shading on edges;
- one or two faint gray grid lines for scale (only when requested);
- a subtle vertical gradient across the background.

### 6. Structure the sequence

Compose with the `seedance-prompt-25` stage structure. Give each stage one primary event
and a visible end state. Right-size the duration (4–30s) to the action; do not
pad to fill 30s. For revisions, use a revision contract (locked decisions / requested delta / acceptance criteria).

### 7. End with a gray seal

Close with one compact sentence that reinforces the material system, shading,
background, and motion cadence, so the look does not drift:

```text
Keep every surface flat untextured mid-gray, depth from ambient occlusion and
a soft neutral light, the neutral gray background, and rigid constant-speed
motion throughout.
```

## Output formats

### Graybox style block

Use when the user only wants the gray look wording:

```text
[Graybox Look]
<Medium-first sentence: untextured gray construction, AO + soft light, gray background.>

[Shading]
Depth from ambient occlusion and contact shadows; curved surfaces catch a soft
neutral gradient, flat faces stay uniform.

[Readability]
<Two to three cues: AO pockets, bevel/facet edges, contact shadows, optional grid.>

[Motion]
<Mechanical cadence: rigid, constant-speed transforms, joints pivot.>

[Gray Seal]
<Compact look sentence and the exclusions that would break the gray.>
```

### Full prompt

Use when the user asks for a complete Seedance prompt. Compose with the
`seedance-prompt-25` six-part formula; the gray look lives in the Visual Style
slot:

```text
[Subject and Action]
<Subject> performs <primary action or event>.

[Stage Plan]
Stage 1 (<time range>): <one event and visible end state>.
Stage 2 (<time range>): <one event and visible end state>.
Final Stage (<time range>): <closing event and final visible state>.

[Scene]
<scene and environment, reduced to flat gray geometry>.

[Graybox Look]
An untextured gray graybox 3D world: every surface is flat neutral mid-gray,
shaded only by ambient occlusion and one soft neutral studio light, set against
<flat | gradient> gray viewport background <+ grid if requested>.

[Camera]
<Display shots: shot size, lens intent and the turntable/orbit move. Chase or
story: one line per cut — Shot N (time range): size, angle, lens intent, one
primary move, the action and its intent, the visible end state.>
Light: the single soft neutral studio light, key from <frame side>.

[Audio]
Clean room tone, a soft UI-style whoosh, or subtle mechanical ticks.

[Gray Seal]
Keep every surface flat untextured mid-gray, depth from ambient occlusion and
a soft neutral light, the neutral gray background, and rigid constant-speed
motion throughout.
```

### Worked example (10 s chase, two cuts)

```text
[Subject and Action]
Two adult-height, near-equal-in-stature gray mannequins race through a gray
colonnade; the pursuing mannequin closes the gap on the second mannequin.

[Stage Plan]
Stage 1 (0-5s): the second mannequin sprints left-to-right past three columns;
the pursuing mannequin follows two strides behind. End: both pass the third column.
Stage 2 (5-10s): the second mannequin pivots on its planted feet and turns its
whole body at the open area; the pursuing mannequin stops one stride away. End:
both stand still, facing each other.

[Scene]
A straight colonnade of six gray columns opening onto a flat open area; travel
stays left-to-right; both figures remain fully in frame at all times.

[Graybox Look]
An untextured gray graybox 3D world: every surface is flat neutral mid-gray,
shaded only by ambient occlusion and one soft neutral studio light, set against
a flat gray viewport background.

[Camera]
Shot 1 (0-5s): low-angle medium-wide, wide 24mm-equivalent depth; fast lateral
tracking move left-to-right beside the runners, columns streaking past in the
foreground; the pursuit reads as urgency.
Shot 2 (5-10s): cut at 5s to an eye-level two-shot, long-lens compression;
slow push-in that stops at 8s and holds to the end on the face-off.
Light: the single soft neutral studio light, key from frame-left.

[Audio]
Clean room tone and soft rhythmic footfall ticks.

[Gray Seal]
Keep every surface flat untextured mid-gray, depth from ambient occlusion and
a soft neutral light, the neutral gray background, and rigid constant-speed
motion while figures and camera move; both mannequins stay adult-height and near-equal in stature.
```

Return the prompt directly. Do not add production workflow, tool selection,
asset management, approval gates, or generation instructions unless the user
explicitly asks for them.

## Guardrails

- **Gray is the only material.** No color, no albedo textures, no reflections.
  If the user asks for a colored element, ask whether they want a color accent
  (a deliberate exception) or a different look entirely — this skill does not
  do colored scenes. If the user confirms an accent, state it as the single
  allowed color: `one accent color — <named color> — on <specific element>
  only; everything else stays mid-gray.`
- **Exclude only contradictions, and write positively.** Avoid bare negatives
  like "no CGI" or "no textures" as the main direction. Name the gray system
  first, then add exclusions only for likely drift: no color, no sharp
  environment reflections, no photoreal skin or hair, no filmic color grade.
- **Do not mix with other style presets.** One look per shot. Do not combine
  graybox with a teal-orange grade, a lighting preset, or an animation-medium
  style — they fight the gray. Lighting here is always the single soft neutral
  studio light; do not stack a lighting preset on top of the gray.
- **People are mannequins, not people.** Apply the mannequin rule from "What
  graybox means here"; never write photoreal facial detail or gendered body
  cues.
- **Audio stays neutral and minimal.** Native audio should read as clean room
  tone, soft UI-style whooshes, or subtle mechanical ticks unless the user
  requests otherwise. Native audio can still add a score or voices; when a
  strictly neutral bed matters, set `generate_audio: false` and add the bed in
  post (it is not frame-synced).
- **References are geometry-only.** If the user supplies reference images, bind
  them as structure and silhouette only — `use only the shape and proportions;
  do not use its color, texture, or materials` — or omit references and write
  T2V. A colored identity sheet injected directly would fight the gray.
- **Chain verbatim.** Repeat the same look block and gray seal word for word
  across every chained scene in a sequence.
- **Watermark false.** Set `watermark: false` on all generation unless the user
  explicitly requests the AIGC watermark.

## Self-check

Before returning the prompt, verify:

1. The medium-first sentence names untextured gray construction, AO shading, and the gray background before any story action.
2. Every visible category — figures, props, environment, effects — shares the single gray material system.
3. Any human figure is a gender-neutral articulated mannequin: featureless head, no skin, hair, facial features, or gendered clothing.
4. Depth is stated through AO, contact shadows, and a neutral gradient — not colored or dramatic lighting.
5. Motion is rigid, constant-speed, and mechanical; no unrequested squash, cloth, hair, or fluid.
6. Two or three readability cues make the gray legible without adding color.
7. The background matches the requested toggle (flat, gradient, grid) and nothing else.
8. Each stage has one primary event and a visible end state; the duration is right-sized.
9. The gray seal is compact and does not contradict the look.
10. No other style preset (grade, lighting, animation medium) is mixed in.
11. The response contains the prompt, not an unrelated production workflow.
12. All figures are full adult height and near-equal; no relative size descriptors separate figures.
13. Any reaction is a whole-body pivot, not a head-only turn; head motion is bound to a fixed neck-joint angle.
14. Architectural orientation and travel invariants are repeated in the Scene and in every stage, not stated once.
15. For chase/action scenes, the camera prescribes per-cut moves and shot sizes with timestamps aligned to stage boundaries; each beat resolves on a state present at that timestamp.
