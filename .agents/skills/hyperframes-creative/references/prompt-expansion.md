# Prompt Expansion

Use expansion to resolve production details that are missing from the brief, not to lengthen it or add visual activity. Ground the user's intent against the design spec (`frame.md` or `design.md`) and applicable `house-style.md` guidance, producing a consistent intermediate that downstream agents read the same way. A complete brief can pass through unchanged.

Runs AFTER design direction is established (Step 1). The expansion consumes the design spec (`frame.md` or `design.md`, if present) and produces output that cites its exact values.

## Prerequisites

Read before generating:

- the design spec — `frame.md` → `design.md` → `DESIGN.md` (read the first that exists) — extract brand colors, fonts, mood, and constraints. The expansion cites these exact values (hex codes, font names); it does not invent new ones.
- `references/beat-direction.md` — per-beat planning format (concept, mood, choreography verbs, transitions, depth layers, rhythm). The expansion outputs each scene using this format.
- `references/video-composition.md` — video-medium guidance for density, scale, and color presence. Apply it in service of the brief and readability, not as a density quota.
- `house-style.md` — optional background, color, motion and typography choices. Preserve locked brand tokens; recipes do not override intentional sparse frames or stillness.

If no design spec (`frame.md` or `design.md`) exists yet, run Step 1 (Design system) first. Expansion without a design context produces generic scene breakdowns that later agents ignore.

## When to expand

Expand unresolved details into a buildable per-scene production spec. Preserve source scope, exact copy, locked brand values, scene count and timing already supplied. Do not treat a detailed brief as permission to embellish it.

Consider only the details the treatment needs:

- **Atmosphere and micro-details** — optional glows, grain, rules or thematic decoration when they serve the concept. There is no minimum layer or decorative count; zero decoration is valid. Do not invent claims, labels or other source content to fill space.
- **Motion or stillness** — keep static elements static when directed. Add ambient motion only when it contributes to the brief, never simply because an element is decorative.
- **Transitions** — preserve a requested hard cut, simple crossfade or uninterrupted hold. For a chosen animated transition, specify duration, ease and any source/target needed for implementation; an object morph is optional.
- **Pacing** — preserve supplied holds and timing; resolve only missing details that affect the intended rhythm.
- **Exact hex values and typography parameters** from the design spec, and ease choices where motion is selected. Ask about missing required source inputs rather than inventing approved values.

Rich, energetic treatments remain valid when requested, just as sparse frames and deliberate stillness do. Expansion clarifies the chosen treatment rather than imposing a richer one. Keep readability and deterministic, seekable runtime behavior intact for both moving and held elements.

For a complete multi-scene brief, confirm the supplied decisions without adding atmosphere, motion or micro-details. Single-scene compositions and trivial edits need only the relevant details.

## What to generate

Expand into a full production prompt with these sections:

1. **Title + style block** — cite the design spec's exact hex values, font names, and mood. Do NOT invent a palette — quote what the design provides.

2. **Rhythm declaration** — name the intended scene rhythm, preserving supplied timing and holds. Example: `hold-cut-hold` or `hook-PUNCH-breathe-CTA`. Use `references/beat-direction.md` to derive rhythm from the brief, not a video-type quota.

3. **Global rules** — source and brand locks, readability, selected motion or stillness, and transition intent. Parallax, micro-motion and accent transitions are optional; keep any chosen motion deterministic and seekable.

4. **Per-scene beats** — for each scene, use the beat-direction format:
   - **Concept** — the big idea in 2-3 sentences. What visual WORLD? What metaphor? What should the viewer FEEL?
   - **Mood direction** — cultural/design references, not hex codes. ("Bauhaus color studies", "cinematic title sequence", "editorial calm")
   - **Depth layers** — BG treatment, MG content, and FG accents or structural details as the concept needs. Use `video-composition.md` to choose density; do not force an element count or invent content to fill one.
   - **Animation choreography or hold** — describe selected actions with specific verbs and timing, or record a static state and hold duration. Motion is not required for every element.
   - **Transition out** — specify the chosen handoff and applicable parameters, including a hard cut, simple crossfade or no transition. Do not replace a supplied handoff just to add complexity.

5. **Recurring motifs, if useful** — optional visual threads across scenes within the brand constraints.

6. **Negative prompt** — what to avoid, informed by the design spec's constraints if present.

## Output

Write the production breakdown to `.hyperframes/expanded-prompt.md` in the project directory. Keep it as concise as the brief allows; there is no target length.

Tell the user:

> "I've expanded your prompt into a full production breakdown. Review it here: `.hyperframes/expanded-prompt.md`
>
> It has [N] scenes across [duration] seconds with specific visual elements, transitions, and pacing. Edit anything you want, then let me know when you're ready to proceed."

Only move to construction after the user approves or says to continue.
