# Context And Preflight

Focused reference for `seedream-storyboard`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [1. Inspect existing project context](#1-inspect-existing-project-context)
- [2. Lock the brief](#2-lock-the-brief)
- [3. Break the scene into observable beats](#3-break-the-scene-into-observable-beats)
- [4. Decide panel density](#4-decide-panel-density)
- [5. Preflight every reference](#5-preflight-every-reference)
- [6. Establish geography and continuity](#6-establish-geography-and-continuity)
- [7. Build the panel plan](#7-build-the-panel-plan)

### 1. Inspect existing project context

Before creating files:

- search for the project, scene, shot, character, location, and prop;
- reuse approved assets and existing IDs;
- open every relevant `elements/*/character.md`, `elements/*/location.md`, and
  `elements/*/prop.md`; resolve
  one selected sheet/reference file per visible Element, its lifecycle state,
  and SHA-256 before writing prompts;
- preserve user-written descriptions and lifecycle states;
- do not create a duplicate project, scene, element, or same-purpose note.

If a project has relevant Element sheets, a generated panel must bind them by
role in both the submitted request and its metadata. If an Element has no
selected sheet, use the best available approved reference; otherwise record the
asset as `unresolved` and keep the output as an unlocked draft, ineligible for
video handoff. Do not quietly use a storyboard output as the canonical source.

If the request is not tied to a local project, keep the output in chat unless
the user asks for files.

### 2. Lock the brief

Extract or infer:

- project and scene;
- storyboard purpose: editorial board, continuity board, pitch board, or video
  keyframe planning;
- target medium and aspect ratio;
- cast, locations, props, wardrobe, and visible state;
- the selected character, location, and prop sheet for every visible Element;
- visual style, palette, lighting rules, and realism level;
- render style: sketch (default) or full color, and which sketch medium
  (pencil, ink, charcoal, limited palette);
- forbidden content or transformations;
- target runtime only when it affects the edit;
- panel budget, including whether the user wants one hero panel or sequence
  coverage;
- whether the user wants prompts only or actual image generation.

Ask only when a missing answer would materially change identity, format, cost,
or story meaning. Otherwise state reasonable assumptions and continue. An
explicit request to generate the storyboard authorizes a low-cost draft pass;
higher resolution, large batches, or repeated paid re-generation requires a
new explicit request or approval.

### 3. Break the scene into observable beats

Create a beat table before writing image prompts.

| Field | Meaning |
|---|---|
| Beat ID | Stable identifier |
| Purpose | New information or emotion delivered |
| Start state | What is true before the beat |
| Decisive moment | The exact instant the panel depicts |
| End state | What must be true for the next beat |
| Subjects and props | Visible entities and their state |
| Geography | Location, travel axis, entrances, exits |
| Sound/dialogue cue | Only when it changes timing or interpretation |

For a sequence board, do not convert a long action sentence directly into one
panel. Split actions such as “enters, notices the threat, drops the vial, and
attacks” into decisive states. For a requested one-panel board, still identify
all beats, then choose the single decisive moment that best communicates the
scene's subject, conflict or product, environment, and intended emotion.

### 4. Decide panel density

**Dynamic panel count.** When an upstream analysis has identified the scene's
shots or beats — a `seed_understand` breakdown, a `tig-scene-engine` beat list,
a `film-production` shot list or `seedance-shot-design` shot plan, a script/beat sheet, or any story analysis —
the board defaults to **one panel per identified scene/shot**, regardless of
any earlier guess or fixed budget. The panel count is dynamic and follows the
analysis, not a hard-coded number. If the analysis names 8 shots, the board has
8 panels; if it names 3, the board has 3. Only trim below the analysis count
when the user explicitly sets a smaller budget (then keep the most
story-critical shots and record the omitted ones as motion notes).

When the user specifies a panel count, treat it as a creative constraint.
Otherwise, if no upstream analysis exists, panel count follows information and
state changes, not duration alone.

Add a panel for:

- a new camera position or cut;
- a decisive pose, reveal, or reaction;
- a material blocking or screen-direction change;
- an entrance, exit, boundary crossing, or axis re-establishment;
- a prop, wardrobe, damage, weather, or location-state change;
- a camera move whose start and end compositions both matter;
- a transition whose visual hookup must be reviewed.

For a camera move, use start and end panels when framing or revealed information
changes. For complex action, use anticipation, contact/change, and
consequence/reaction when each state matters. Add no mandatory second-by-second
timestamps; estimate duration only for timing or animatic-ready requests.

For a one-panel board:

- select one hero beat and one frozen composition;
- favor the image that best sells the scene's central story, emotion, or product;
- record important omitted transitions as motion notes rather than extra panels;
- recommend I2V or R2V for video handoff; request a second approved panel only
  if exact start-and-end locking through FLF2V becomes necessary. R2V bundle
  sizing is version-dependent: Seedance 2.0 allows ≤9 images; 2.5 allows ≤30.

After the panel count is settled, record the **panel delivery mode**
(single-image grid or separate images) in the panel plan. Default to
single-image grid for multi-panel boards; use separate images only when the
user requests it or the downstream workflow requires individual panels.

### 5. Preflight every reference

Classify each input:

| Role | Controls |
|---|---|
| Character identity | Face, body, hair, costume, silhouette |
| Location geometry | Architecture, layout, landmarks, dressing |
| Prop identity | Shape, material, markings, orientation |
| Composition control | Blocking, pose, camera layout, depth |
| Style | Medium, texture, palette, grade |
| Continuity anchor | An approved prior panel’s exact state |

Check for:

- conflicts between the brief and visible reference content;
- extra faces, split panels, labels, watermarks, or effects that may leak;
- incompatible lighting, costume, age, scale, or perspective;
- ambiguous images that combine several reference roles;
- more references than the chosen model supports.

Use the smallest sufficient reference set: approved references for recurring or
identity-critical on-camera characters, recurring or geography-critical spaces,
and threshold-qualified props. Use approved descriptors for incidental people,
scene direction/keyframes for incidental settings, and UI plus text direction
for screen-only callers. If the required set exceeds the live model limit,
split the panel/task or resolve the asset
set; do not silently drop an Element. If a visible reference conflicts with the
requested result, clean or replace it instead of relying only on an exclusion
sentence.

Control-only floor plans and sketches guide authoring. Translate their geometry
into text and omit them from generation inputs by default. An intentional
conditioning exception needs explicit selection, live tool compatibility, and
output QA for style, labels, colors, and geometry leakage.

Apply the workspace prop threshold consistently: branded, recurring, or
story-critical objects and scene-variant wearables need their own approved
`prop_` reference, bound as `@Image N`. Incidental objects may be described in
text; always-worn outfit items remain in the character sheet. A missing required
prop reference leaves the dependent panel draft. The caller resolves required
asset preparation before submission.

Bind a required canonical location in every panel that uses it, including
close-ups and medium shots. For incidental settings, carry forward clear scene
direction or an approved scene-level keyframe instead of requiring a new sheet.

### 6. Establish geography and continuity

For dialogue, pursuit, combat, or multi-character action, define:

- durable landmarks and location boundaries;
- subject start/end positions;
- entrances and exits;
- travel direction;
- the line of action;
- camera side of the axis;
- screen-left/screen-right assignment;
- intentional axis crossings and how they are shown.

Maintain a continuity ledger:

```yaml
continuity:
  location_id: church-ruins
  time_of_day: night
  axis_id: altar-door-axis
  camera_side: south
  screen_direction:
    hunter: left-to-right
    creature: right-to-left
  subjects:
    hunter:
      wardrobe: hunter-coat-v01
      position: foreground-left
      pose_state: braced-at-threshold
      damage_state: cut-right-cheek
      held_props:
        right_hand: whip
        left_hand: none
  props:
    oil-vial-02:
      state: broken
      position: behind-hunter-right-boot
  environment_state:
    left_candle_bank: extinguished
    church_door: open-inward
```

Use permanent canon anchors plus one or two nearby approved panels. Do not chain
every panel automatically: re-anchor from canon after a rejected or compromised
frame.

### 7. Build the panel plan

Use this table:

| Panel | Beat | Decisive moment | Shot / angle | Staging and direction | State change | References | Target file |
|---|---|---|---|---|---|---|---|
| p010 | beat-01 | ... | ... | ... | ... | ... | ... |

For a multi-panel board, also record the delivery mode above the table:

```text
Delivery mode: single-image grid (default) | separate images
Grid layout: [e.g. 2×3, reading left-to-right, top-to-bottom]
```

Use panel numbers in increments of 10 so panels can be inserted without
renumbering.

For a one-panel board, create only `p010`. Generate alternatives as variants of
`p010`; do not mislabel three alternatives as three narrative panels.
