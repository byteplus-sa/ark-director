# Seedream Checklist

Seedream image generation and storyboard prompts. Apply the universal items in
[the index](review-checklists.md#universal--all-prompts) first.

## Seedream image generation

Source skill: `seedream-prompt`

Apply this checklist when review is invoked under workspace policy. Default
preflight does not automatically load it; strict review, explicit review and
applicable required-rule evidence retain their existing invocation rules.
Prompt-only review never authorizes generation or extra samples.

### Structure

1. **Task-first clarity.** Task > Subject and scene > Composition > Visual style >
   Constraints is a flexible writing aid, not a required template or measured
   weighting law. Omit irrelevant sections while preserving the requested result.

2. **Subject priority.** The primary subject and visual hierarchy are unambiguous.

3. **Reference labeling.** `@Image 1`, `@Image 2`, ... match actual input order.
   The `@` prefix is a repository convention, not a newly established 5.5 API rule.

4. **Reference precedence.** Each reference has a role, target, preserved features,
   excluded features and conflict priority, bound where it affects the output.
   A material or environment donor must not override the identity source's shape.

5. **Bindings stay consistent.** Reordering inputs requires rewriting every label
   and binding. Do not rely on an inventory alone or ambiguous image references.

### Reference limits

6. **Exact-model limits.** Preserve the selected model. Verify reference counts
   against its operation and current transport; Pro/Lite limits are not family limits.
7. **Batch versus variations.** Verify provider batch support separately from
   adapter `variations` (separate calls). The documented 5.5 and 5.0 Pro bindings
   do not support provider sequential batches; do not silently switch models.

### Task type

8. **Correct task type.** T2I, I2I, Image Editing, Sequential Generation, or
   Infographic/Information Visualization; extraction and channel adaptation
   state the requested change and protected features.

9. **Sampling follows review mode.** Default uses one image; strict uses three
   when applicable. An explicit requested count or creative alternatives wins.
   Comparison samples keep identical prompts, references and effective settings
   except supported seed variation. Seeds do not guarantee identical pixels.

### Subject

10. **Stable attributes.** Include enough supplied attributes to identify each
    subject; do not invent identity details to meet a quota.

11. **Multi-subject priority order.** Listed in order of visual priority.

### Photographic treatment, when requested

12. **Intent preserved.** Camera/film terminology is optional shorthand. Do not
    require it or a cinematic treatment for every photographic image.
13. **Lighting appropriate.** Soft, flat or shadowless light may be intentional.
    Preserve the approved lighting unless changing it is within scope.
14. **Identity protected.** Describe relevant existing texture; do not invent
    freckles, age, wrinkles or material damage as a generic realism cure.
15. **Readable hierarchy.** Lead with the requested result. Headings and ordering
    are clarity conventions, not proven positional weighting laws.
16. **Focused exclusions.** Use only necessary scope or demonstrated-leakage
    exclusions; do not demand aggressive boilerplate negatives.
17. **Diagnosis grounded.** Cite a visible symptom in a supplied output or label
    the example hypothetical. Do not promise a prompt will produce realism.
18. **Parameters verified.** Actual size and optimization settings belong in
    request metadata and must be supported by the resolved live model/tool.

### Text in image

19. **Routing boundary.** Model-rendered text is present only when the user
    expressly accepts it as expressive and non-exact. Delivery-critical copy,
    data, UI, pricing, CTA, logos, or pixel layout is a MAJOR routing defect;
    require a text-free generative layer plus deterministic finishing.

20. **Quoted prompt intent.** Accepted model text is in double quotes and its
    surface, line breaks, hierarchy, alignment, weight, spacing and safe margins
    are clear where relevant; quoting does not establish pixel-exact output.

21. **Proofread output.** Inspect every character, line break and spatial hierarchy
    in supplied results; OCR can assist but is not a substitute for inspection.
    Small text may remain unstable. A prompt-only check cannot pass unseen text.

### Constraints

22. **Creative constraints inline.** No separate `negative_prompt`. Supported
    settings such as `background`, `output_format`, size and structured edit fields
    stay in request metadata, not creative prose.

23. **Quality directives and negative constraints.** Only those that materially affect
    output.

### Prompt length

24. **Focused length.** Keep simple prompts concise; retain necessary bindings
    and preservation constraints in complex edits. The verified MCP adapter's
    4,000-character limit includes added coordinate markup, not just user prose.

### Coordinates and output acceptance

25. **Separate coordinate interfaces.** Guide prompt boxes
    `bbox=[xmin, ymin, xmax, ymax]` use 0-1000 as layout guidance, not exact pixels.
    MCP structured `bbox={x1,y1,x2,y2}` and `point={x,y}` use integers 0-999
    on the first image only. Put the edit target first and rewrite bindings after
    reordering. Let the adapter add markup; never duplicate it in the prompt.
    Reject missing source images, inverted, degenerate or out-of-range boxes.
    Explicitly map a valid guide endpoint 1000 to 999 at the adapter boundary;
    recompute after cropping or reframing, not by silently clamping invalid input.

26. **Transparency intent and alpha.** Distinguish transparent canvas, opaque
    cutout, translucent material and interior holes. Verify exact-model support
    for creation versus extraction and compatible `background`/`output_format`
    settings. Decode actual alpha; a PNG extension or painted checkerboard is
    insufficient. Inspect fine edges, holes, halos and composites on light and
    dark backgrounds. Partial alpha alone does not prove correct translucency.

27. **Marked edits.** Use unique region numbers, move source/destination,
    operation order and replacement size/orientation. Remove visible markers.
    Inspect edited and unmarked areas; coordinates do not guarantee strict
    boundary compliance.

28. **Accepted-output edit chain.** Use the last approved output as the next
    input, one major delta per round. Each prompt is self-contained with protected
    features, not assumed conversational memory. Record accepted artifact/hash,
    prompt, reference order, exact model and settings. Reject drift and roll back
    to the last accepted image; successful generation is not approval.

29. **Channel adaptation.** Distinguish deterministic resize/crop from generative
    recomposition and capability-verified canvas extension. State target ratio
    and safe areas; do not stretch subjects. Inspect identity, proportions,
    crop, hierarchy, text, logo clearance, actual dimensions and required alpha.
    Preserve approved reference identity and the exact-copy finishing boundary.

30. **Information and layers.** Conceptual dashboards and decorative charts are
    not factual data graphics. Exact labels, values and units need deterministic
    charting/design with editable copy. Provider layer decomposition/OCR is
    unavailable through the current MCP tool; do not invent controls or layers.

---

## Seedream storyboard

Source skill: `seedream-storyboard`

### Core rules

1. **One frozen, decisive moment per panel.** Not a collage or multi-panel grid.

2. **Dynamic panel count.** When an upstream analysis (`seed_understand`,
   `scene-craft`, `film-production`, or a script/beat sheet) has identified
   N scenes/shots, the board defaults to one panel per identified scene/shot —
   not a fixed budget. A user-specified smaller count is honored only when
   explicit, with omitted shots recorded as motion notes.

3. **Boards stay planning artifacts (`board.animatic_review_only`).** A board
   or panel is for planning and review only and is never bound to a Seedance
   request: panel numbers and the board's medium leak into video. The prompt
   does not promise a video handoff; staging moves into the Seedance prompt
   text and identity comes from element references. A board's style is a
   creative choice for the board alone.

4. **Explicit canon.** Recurring identities, locations, props, and style are in an
   explicit canon section.

5. **Canonical Element sheets attached.** When matching Element sheets exist, they are
   attached to the generation request — not substituted with text descriptions.

6. **Screen direction and geography.** Treated as sequence-level constraints.

7. **Natural language.** Coherent natural language, not comma-heavy keyword piles.

8. **References bound by role and target.** Every reference bound with exact `@Image N`
   tokens.

9. **Production notes outside image.** Arrows, labels, dialogue, timing, and production
   notes are outside the generated image unless visible story-world text is required.

### Panel prompt structure

10. **References.** Each reference labeled with role (character identity, location
    geometry, prop identity, composition control, approved style).

11. **Panel purpose.** The new story information or emotion this panel communicates.

12. **Subject and decisive moment.** One frozen moment. Every visible subject, pose,
    expression, action, and prop named. Identity and prop references bound inline.

13. **Setting and state.** Location, time, weather, persistent landmarks, visible
    object state. Location reference bound inline.

14. **Staging and continuity.** Screen-left/right positions, foreground/midground/
    background, eyelines, distances, overlaps, travel direction, entrances/exits, and
    what must match the previous panel.

15. **Style.** Medium, realism level, palette, stable treatment. Style reference bound
    inline when provided.

16. **Lighting.** Source, direction, quality, color, and atmosphere.

17. **Composition.** Aspect ratio, shot size, camera height/angle, lens intent,
    framing, depth, and focus priority. Composition guide bound inline when provided.

18. **Constraints.** Appropriate quality (draft or final), preservation (approved
    identity, geometry, pose, state, style), exclusion (only material faults — no text
    overlays, labels, storyboard borders, watermarks, unintended subjects, duplicated
    faces, control-guide marks).

### Sequential generation

19. **Sequence contract.** Cohesive ordered set of N separate images, one per panel.
    Recurring identity, wardrobe, location geometry, prop design, palette, and
    rendering style kept consistent.

20. **Each image is one moment.** Not a collage or multi-panel grid.

21. **Global visual canon.** Stable identity, location, prop, style, aspect ratio, and
    lighting rules stated before individual panels.

### Revisions

22. **Local edits preferred.** After a composition is approved, prefer local edits over
    full re-generation.

23. **Seeds for tracking.** Used for experiment tracking, not as the identity system.

### Status

24. **Review on generation.** Technically successful generation enters `review`.

25. **Mode-authorized choice.** A passing hash-bound review and validated agent
    decision in `approve_for_me`, or an explicit user choice in
    `ask_for_approval`, sets `selected_variant` and `approved`.
