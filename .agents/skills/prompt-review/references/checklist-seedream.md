# Seedream Checklist

Seedream image generation and storyboard prompts. Apply the universal items in
[the index](review-checklists.md#universal--all-prompts) first.

## Seedream image generation

Source skill: `seedream-prompt`

### Structure

1. **Section order.** Subject > Setting > Style > Lighting > Composition > Technical.
   Order matters — earlier concepts carry more weight.

2. **Most important subject first.** The primary subject appears before secondary
   subjects.

3. **Reference labeling.** `@Image 1`, `@Image 2`, ... sequential numbering with `@`.

4. **Reference list is inventory.** Each reference is also bound again where it affects
   output — not just listed in the reference section.

5. **Exact tokens.** Uses exact `@Image N` token every time. Does not drop `@` or
   replace with ambiguous phrase.

### Reference limits

6. **Seedream 5.0 Pro.** ≤ 10 input images.
7. **Lite.** Refs + outputs ≤ 15.

### Task type

8. **Correct task type.** T2I, I2I, Image Editing, Sequential Generation, or
   Infographic/Information Visualization.

9. **Sequential generation.** NOT supported on 5.0 Pro. Requires Lite/4.5/4.0.

### Subject

10. **2-3 stable attributes.** Each subject defined with 2-3 stable attributes.

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
    surface is described; quoting does not establish pixel-exact output.

21. **Instability disclosed.** Small text may still be unstable and the prompt
    does not claim deterministic fidelity.

### Constraints

22. **Inline only.** All constraints in the text prompt. No separate `negative_prompt`.

23. **Quality directives and negative constraints.** Only those that materially affect
    output.

### Prompt length

24. **30-100 words.** For standard images. Infographics and complex scenes can go
    longer but stay focused.

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
