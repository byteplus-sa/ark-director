---
name: seedance-motion-design
description: >
  Write production-grade Seedance 2.5 motion-design and motion-graphics
  prompts for marketing deliverables — launch videos, motion-on-footage
  explainers, hypermotion product ads, 3D flythroughs, 2D explainers,
  editorial explainers, logo reveals, kinetic type, product motion, and
  data-driven explainers. Exact words, numbers, charts, logos, and UI are
  authored as deterministic HTML-entrypoint graphics for post-composited
  fidelity;
  Seedream supplies only synthesized image layers and Seedance supplies
  text-free footage or intentionally non-exact plate motion. Use whenever the
  user asks for motion design, motion graphics, kinetic typography, a logo
  reveal, product motion, an explainer video, an animated data story, or
  any text/graphic-driven marketing motion. Composes in prose with
  html-graphic-render for exact static graphics, seedance-prompt-25 for the
  six-part formula, seedream-prompt or seedream-storyboard for synthesized
  image/keyframe layers, and seed-audio-prompt for voice/music. Does not call
  the API itself.
---

# Seedance Motion Design

Write ready-to-use Seedance 2.5 prompts for motion design and motion
graphics — marketing motion where the message is carried by text, graphics,
charts, UI, and choreographed product motion rather than by live-action
narrative. Make the *design* govern every layer: the text and graphic plates,
the hierarchy of attention, the easing and speed contrast, and the moment the
message lands.

Motion design is a **category, not a fixed taxonomy.** The examples below are
worked references, not an exhaustive list. The same rules apply to any
text/graphic-driven marketing motion: logo reveals, kinetic type, product
motion, UI walkthroughs, data-driven explainers, boardroom presentations,
event openers, and title sequences.

## Core principle

**Separate exact graphics from generated motion.** Seedance cannot reliably
render or preserve readable text, numbers, charts, logos, or UI. Author exact
copy and geometry as deterministic HTML-entrypoint graphics. Use Seedream only
for synthesized visual layers such as illustration, photography, texture, or
keyframes. Generate text-free Seedance footage, then animate/composite exact
graphics in HyperFrames or FFmpeg. If the user intentionally accepts
model-driven plate motion, bind the selected plate explicitly and still inspect
the result; image conditioning does not guarantee text fidelity.

For every prompt, define:

```text
plates               exact deterministic graphics plus synthesized image layers
message              the one thing the viewer must take away
attention hierarchy  the editorial order in which elements enter and settle
action beat          the moment the message lands, and what the viewer should feel
motion language      easing curves, speed contrast, stagger, and weight per element
camera               whether the camera is locked-off or moving, and how far
audio                voice, music, SFX approach — and whether lip-sync is requested
failure modes        what kills legibility, trust, or conversion for this piece
```

## Motion is guidance, not decoration

Every animation must do one job for the buyer: **signal, orient, reassure, or
convert.** This is the buyer trust chain. Before you animate an element, name
which job it serves:

- **Signal** — draw the eye to what matters first (the hook, the headline).
- **Orient** — show where the viewer is in the story or how a change maps to a
  before/after.
- **Reassure** — make a claim feel credible (a number counts up, a checkmark
  lands, a progress bar fills).
- **Convert** — land the CTA, the price, the single next action.

If an animation does not guide attention, explain a change, or reduce
uncertainty, **cut it.** Motion is a budget, not a garnish. Write the positive
instruction that produces the intended result; do not enumerate what to avoid.

## Example modes (menu, not taxonomy)

These six are worked examples. Treat them as a starting point for the category;
the custom-mode procedure below extends the skill to any text/graphic-driven
motion.

| Mode | What it is | Plates to lock first | Motion emphasis |
|---|---|---|---|
| **Launch video (SaaS)** | Product launch or feature reveal, screen-led | App UI screens, feature labels, hero headline | Screen-in-screen transitions, UI state changes, headline reveal |
| **Motion-on-footage** | Talking head with graphics synced to the speaker | Lower-thirds, stat cards, callouts, logo bug | Graphics entrances timed to speech beats, subtle drift |
| **Hypermotion product ad** | Product hero with dramatic camera and material motion | Product sheet, logo, headline, spec labels | Macro orbit, speed ramps, material glints, CTA lock |
| **3D real-estate flythrough** | Architectural walkthrough of a space | Floor plan / render stills, room labels, unit numbers | Continuous camera path, room-to-room reveals, caption plates |
| **2D explainer** | Flat-illustration concept explainer | Illustration frames, icon set, key terms | Scene morphs, icon choreography, kinetic type |
| **Editorial explainer** | Dense text/chart/number story (data journalism) | Full infographic plates, charts, figure callouts | Chart draws-in, figure count-ups, section reveals |

## Prompting workflow

### 1. Resolve the motion design intent

Map the user's request to a dominant intent rather than a fixed label. Separate
materially different treatments:

- screen-led product motion reads as launch/showcase;
- speaker plus synced graphics reads as motion-on-footage;
- product-as-hero with aggressive camera reads as hypermotion;
- space-led camera traversal reads as flythrough;
- illustration-led concept reads as 2D explainer;
- chart-and-number-led reads as editorial explainer.

For a hybrid, choose one dominant treatment and state how the secondary
influence appears. **Default when unspecified:** pick the treatment that best
carries the message with the least text the model must animate.

### 2. Author and classify the plates first

Before writing any motion, enumerate every on-screen word, number, chart, logo,
screen, product, and keyframe, then route by fidelity:

- **Logo lockups, headlines, taglines, numbers, prices, CTAs, kinetic type** →
  a deterministic HTML entrypoint with local CSS/SVG and exact DOM/SVG text.
- **Exact app UI, dashboards, charts, and infographics** → deterministic
  HTML-entrypoint graphics. Use Seedream only for intentionally invented or
  illustrative UI where exact copy and data are not required.
- **Real products and logos** → approved official/user assets first; arrange
  exact lineups deterministically. Keep transparent delivery and solid model
  reference derivatives separate.
- **Illustrative or photographic plates** → `seedream-prompt` without exact
  typography; select before deterministic finishing.
- **Approved storyboard panels / keyframes** → `seedream-storyboard`, promoted
  only after review.

Generated or approved visual plates may become a `reference_image`,
`first_frame`, or `last_frame` with a stable `@Image N` binding. Exact graphic
plates stay in post when fidelity is required. **The submitted reference array
must match the `@Image N` bindings in the prompt 1:1 — same files, same order.**
Submit only what the prompt actually binds.

### 3. Establish the attention hierarchy before the story

State the editorial order in which elements enter and settle. The **first thing
that moves is perceived as most important** — make the hook or headline move
first, never a decorative flourish. List elements in the order they should
enter, with the hero claim first and the CTA last.

### 4. Write the action beat (direct, don't describe)

Write the *moment the message lands*, not a static description of the layout.
For each stage, give one primary event, a motive, and a visible end state. A
motion-design prompt that reads like a list of "headline appears, chart
appears, logo appears" is not yet directed — say *why* each element moves and
what the viewer should conclude when it settles.

### 5. Choreograph the motion language

Translate craft heuristics to 4–30s Seedance clips — do not copy in-product
micro-interaction numbers (150–300ms is a UI duration, not a film beat):

- **Stagger in editorial order.** Elements enter sequentially in importance
  order; overlap, do not queue in lockstep.
- **Non-linear easing with one curve language per scene.** Ease-out for
  entrances, ease-in-out for travel, and keep the same family of curves so the
  piece feels authored by one hand.
- **Create speed contrast.** The slowest element must be *meaningfully* slower
  than the fastest; if everything moves at one speed, nothing has weight.
- **Give motion weight.** Anticipate before a settle, settle into a hold, and
  let the fastest element carry the most energy.

For every moving element, write the full motion grammar — motion type,
direction, speed, amplitude, easing, loop period — not a bare verb (see
`seedance-prompt-25`, "Motion grammar"). State camera motion explicitly,
including when the camera is truly locked-off and only the plates move.

### 6. Compress reality, don't fake it

A product demo must depict a workflow that could plausibly exist in the
product. Simplification and shortened wait times are fine; impossible fluidity
is not — a one-click transformation that skips every step the user will actually
take erodes trust. Show the steps the buyer will recognize, just tightened.

### 7. End with a design seal

Close with one compact sentence that reinforces:

- the dominant treatment;
- the plate set and which exact graphics remain post-composited;
- the easing/speed language;
- the CTA or landing state;
- relevant exclusions (positive phrasing only).

Do not repeat the entire prompt. The seal prevents the motion language and the
text-lock discipline from drifting across later shots.

## Which Seedance mode to animate visual plates

The plate classification decides *what* Seedance animates; the mode decides
*how*. Match synthesized or intentionally non-exact visual plates to one mode
(grammar via `seedance-prompt-25`). Exact type and UI remain deterministic post
layers unless the user explicitly accepts model-driven fidelity risk:

| Plate set | Mode | Notes |
|---|---|---|
| One locked hero frame (open and/or close) | First/last frame (FLF2V) | Locks the exact composition; first and last images must share aspect ratio |
| A stack of plates in order | One-click video | Material roles → image order → motion amount → editing style → audio; the canonical "still plates → paced video" path |
| Staged reveal across beats | Keyframe sequence / `[Stage N]` | Independent keyframe images per stage, continuous transitions |
| Plates + live presenter or product identity | R2V | Plates as `reference_image` + canonical identity sheets; bind `@Image N` roles |

Prefer **one-click video** when the deliverable is a self-contained paced ad from
a stack of visual plates. Prefer **first/last frame** when only the open and
close compositions matter and the middle is a continuous, model-driven move.
Record the chosen mode and ordered roles in `shot.md` (see `seedance-prompt-25`
storyboard-to-video handoff).

## Output formats

### Motion-design block

Use when the user only wants the motion/graphic wording:

```text
[Motion Design]
<Mode-first sentence naming treatment, plate set, and attention hierarchy.>

[Motion Language]
<Stagger order, easing family, speed contrast, and weight per element.>

[Action Beat]
<The moment the message lands, one event, and a visible end state.>

[Design Seal]
<Compact treatment, plate routing, post-composited exact graphics, easing, CTA,
and exclusions.>
```

### Full motion-design prompt

Use when the user asks for a complete Seedance 2.5 prompt. The full-prompt form
overlays the six-part formula (see `seedance-prompt-25` for the grammar). The
`[Motion Design]` block is this skill's front-matter for the **Subject + Action**
slot — the message and the moment it lands — plus the attention hierarchy. It is
**not** the Visual Style slot, which stays lighting → lens → grade → sensor.
Plate bindings are declared up front as `[Material Roles]`:

```text
[Material Roles]
@Image 1 defines <selected visual plate> — use its composition and art direction.
@Image 2 defines <approved storyboard / keyframe> — use its shot structure.
@Image N defines <product / identity sheet> — use its identity and material only.

[Motion Design]
<Mode-first sentence naming the treatment, the one message, and the attention
hierarchy: the hero claim moves first, the CTA lands last.>

[Subject + Action]
<The product, brand, or message> performs <the event that lands the message> in
<environment and observable tone>. Name the moment the claim lands and what the
viewer concludes.

[Visual Style]
<Lighting → lens → grade → sensor/film look, composed via `seedance-prompt-25`
and axis presets. Include only when the user names a look.>

[Motion Language]
Stagger <elements> in <editorial order>. Use <one easing family> for entrances,
<ease-in-out> for travel. Keep the slowest element meaningfully slower than the
fastest. Keep generated footage text-free where exact graphics will be
composited in post. Preserve bound visual plates rigid, sharp, and undeformed
through every move.

[Camera]
<Locked-off, or named camera move with direction and speed.>

[Audio]
<Voice, music, SFX approach. Dialogue in {curly braces} for lip-sync when
requested.>

[Design Seal]
<Compact treatment, plate routing, post-composited exact graphics, easing, CTA,
and exclusions.>
```

For multi-beat reveals, use `seedance-prompt-25`'s `[Stage N]` grammar (one
primary event + a clear end state per stage) rather than inventing a shot list.

Right-size `duration` (4–30s) to the piece; set aspect ratio from the delivery
format; `watermark: false` unless requested. Parameter defaults live in
`seedance-prompt-25`'s quick reference.

Return the prompt directly. Do not add production workflow, tool selection,
asset management, approval gates, or generation instructions unless the user
explicitly asks for them.

## Composition (never generates)

This skill is prompt-only. It **never calls generation tools.** It composes:

- **`seedance-prompt-25`** — the six-part formula, `@Image N` reference roles,
  first/last-frame and keyframe grammar, scene staging, timestamps, audio
  bracket syntax, and generation limitations. This skill references it, it does
  not re-implement it.
- **`html-graphic-render`** — author exact text, UI, chart, logo,
  product-layout, and overlay graphics for deterministic finishing.
- **`seedream-prompt` / `seedream-storyboard`** — author synthesized
  photographic, illustrative, texture, and keyframe plates. Do not ask them to
  reproduce exact typography or layout that deterministic graphics own.
- **`seed-audio-prompt`** — voice and music for the piece, or the audio-first
  pipeline when the user requests lip-synced dialogue.
- Axis presets (`seedance-camera-presets`, `seedance-lighting-presets`,
  `seedance-pacing-presets`, `seedance-acting-console`) — only when the user
  names a specific axis. Do not let two skills fight: exactly one grade, one
  dominant lighting direction, and 1–2 camera moves per clip.

## Reference discipline

- **Keyframes as first/last frames.** Lock the exact opening and/or ending
  composition with `first_frame` / `last_frame` (FLF2V). First and last images
  must share the same aspect ratio.
- **Exact graphics as post layers.** Headlines, charts, logos, and UI stay
  deterministic when fidelity matters. A selected solid-background derivative
  may guide model motion, but it does not replace the final exact overlay.
- **Character/location as identity.** When a presenter or real environment
  appears, bind canonical character/location sheets and state "use only the
  appearance/geometry."
- **Stable `@Image N` bindings.** Assign indices once and repeat each binding
  inline where it controls the output. Never make the model guess which plate
  is which.
- **1:1 match.** The ordered reference array submitted to the tool must equal
  the `@Image N` bindings in the prompt snapshot — same files, same order, same
  roles. Record the count and order in `shot.md`.

## Custom-mode procedure

For a motion-design request outside the worked examples:

1. Identify the dominant treatment (screen-led, speaker-led, product-led,
   space-led, illustration-led, or data-led).
2. Enumerate every on-screen word, number, chart, logo, screen, and visual plate;
   route exact graphics to deterministic rendering and synthesized imagery to
   Seedream.
3. Define the one message and the attention hierarchy (what enters first, what
   lands last).
4. Write the action beat — the moment the message lands and the viewer's
   conclusion.
5. Choose one easing family and a meaningful speed contrast across elements.
6. State the camera (locked-off or named move with direction and speed).
7. Specify audio (voice, music, SFX, and whether lip-sync is requested).
8. Write a mode-first opening and a compact design seal.
9. Add only exclusions that prevent likely motion or text-lock drift.

## Exclusion rules

- Use positive phrasing throughout. Instead of "no jittery, busy motion," write
  "smooth, weighty motion with one dominant element moving at a time."
- Instead of "no distorted logo," keep the generated footage text-free and
  reserve the approved logo lockup for deterministic composition.
- Never exclude text by naming it ("no garbled text" still summons garbled
  text) — instead state the positive: "exact text is added as a deterministic
  post layer."
- Exclude only likely contradictions: camera shake in a boardroom explainer,
  idle decorative motion with no signal job, a second competing focal element
  during the headline reveal.

## Pre-submit checklist

Before returning the prompt (and before any generation task), verify:

1. **Exact graphics first.** Every exact word, number, chart, logo, and UI screen
   is authored deterministically and reserved for final composition. Seedream
   supplies synthesized imagery only; nothing exact is left to the video model
   to render.
2. **Motion has a job.** Every animation signals, orients, reassures, or
   converts. Decorative-only motion is cut.
3. **Attention hierarchy.** The hero claim or hook moves first; the CTA lands
   last; the first mover is the most important element.
4. **Direct, don't describe.** The prompt writes the moment the message lands,
   not a static list of "appears" events.
5. **Craft heuristics translated.** Stagger, non-linear easing (one curve
   family), and meaningful speed contrast are written for 4–30s, not copied
   from micro-UI durations.
6. **Reality compressed, not faked.** The demo shows a plausible workflow;
   impossible fluidity is avoided.
7. **Reference discipline.** `@Image N` indices are stable, roles are stated,
   and the submitted array matches the bindings 1:1.
8. **Composition respected.** The skill composes in prose with
   `html-graphic-render`, `seedance-prompt-25`, `seedream-*`, and
   `seed-audio-prompt`; it does not call generation tools.
9. **The design seal** is compact and does not contradict the treatment or the
   text-lock discipline.
10. **The response contains the prompt**, not an unrelated production workflow.

The calling agent owns the `prompt-review` gate before submission —
CRITICAL/MAJOR findings must be fixed before generation.
