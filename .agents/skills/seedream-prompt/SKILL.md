---
name: seedream-prompt
description: Write Seedream image-generation and editing prompts with ordered references and composition control. Use for synthesized imagery, not exact typography, logo geometry, or deterministic layouts.
---

# Seedream Prompt

Write production-grade prompts for BytePlus Seedream. Keep creative guidance
model-neutral; preserve the selected model and resolve its exact model ID,
operation, and available transport before preparing executable settings.
Editing controls, text rendering, references, and output modes differ by model.
Unknown capability evidence stays unresolved, not assumed from a family name.


## Input and output contract

Input: image purpose, visible detail, model, size, ordered input roles, and
whether the user expressly accepts model-rendered text as expressive and
non-exact.

Output: an image-generation or edit prompt and its matching reference bindings.

## Procedure and reference loading

Use image-generation for new images and image-editing for edits. Add photographic-detail only when a photographic look is wanted. Worked examples are optional patterns, never automatic instructions to change identity or approval state.

Read only the mode-specific resources needed for the request. Reference paths
mentioned in prose are relative to this skill directory unless a link says otherwise.

- [Image Generation](references/image-generation.md) — Recommended prompt structure — Image generation.
- [Image Editing](references/image-editing.md) — Recommended prompt structure — Image Editing.
- [Worked Examples](references/worked-examples.md) — Full example: T2I — Cinematic scene; Full example: Infographic; Full example: Image Editing — Color & Material Replacement; Full example: Multi-image fusion.
- [Photographic Detail](references/photographic-detail.md) — Avoiding the AI look.
- [Quick Reference](references/quick-reference.md) — Quick reference card.

## Submission boundary and failure behavior

The caller owns production authorization, the exact request preflight, and
mode-appropriate review: minimal inline preflight in default mode, complete
hash-bound review in strict mode or when explicitly required. The caller reviews inline and
uses a sub-agent only when the user explicitly requests sub-agent prompt review
for the project or specific generation. A leaf returns its prompt package without
loading sibling skills. An explicitly declared orchestrator may coordinate the
review and submission stages. Missing required inputs remain unresolved; a draft
or technical success does not establish user approval. Preserve optional timing
and the requested delta. Use one image in default review, three stochastic
samples in strict review where applicable, and the explicit requested count in
either mode. Sampling advice does not authorize additional generation.

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

The prompt structure and rules in this skill are sourced from:
- [Seedream image API](https://ai.byteplus.com/ark/region:ap-southeast-1/docs/image-generation-api.md) and [Seedream 5.5 tutorial](https://docs.byteplus.com/docs/en/modelark/seedream-5-5.md)
- [Seedream 5.0 Pro official blog](https://seed.bytedance.com/en/blog/beyond-generation-it-understands-design-introducing-seedream-5-0-pro) (2026-07-08)
- [Seedream 4.0-5.0 API Tutorial](https://docs.byteplus.com/en/docs/ModelArk/1824121)
- [Seedream 4.0-4.5 Prompt Guide](https://docs.byteplus.com/en/docs/ModelArk/1829186)

When the official guide is updated, prefer the live page over this skill where they conflict.

## Identity-sheet routing

For character sheets, identity sheets, turnaround sheets, or Seedance-facing
character references, prefer the sibling `seedream-character-sheet` skill rather
than embedding that workflow here.

If the generated character sheet later needs duplicate-face cleanup, optionally
compose with the companion `seedream-character-sheet-cleanup` skill.

For reusable location sheets, prefer `seedream-location-asset`. For prop and
product identity sheets used as Seedance or storyboard references, prefer
`seedream-prop-asset`. This skill keeps product imagery that is not an identity
reference, such as a commercial scene or a clean isolated packshot.

Storyboards belong to `seedream-storyboard`; a board is planning material and
never a Seedance reference. An image-to-image edit re-composes the frame, so an
edited still is not a substitute for a change the video should show happening;
`seedream-edit` covers coordinate edits and that boundary.

## Deterministic graphic boundary

Use Seedream for synthesized photographic, illustrative, material, texture, or
expressive design content. When exact copy, data, UI, logo placement, pricing,
CTA, product order, or pixel geometry carries the deliverable, create or select
the text-free image layer here and finish the exact graphic through a
deterministic HTML-entrypoint route. Do not ask Seedream to recreate a layout that
the caller can render exactly. A hybrid keeps this generated layer's prompt,
review, task, selection, and hash evidence separately from the deterministic
render record.

## Usage tips

### Prompt formula
**Subject > Setting > Style > Lighting > Composition > Technical** is a readability convention. Lead with the requested result and omit irrelevant sections; do not claim a measured positional weighting law.

### Prompt length
- Recommended: 30-100 words for standard images.
- Infographics and complex scenes can go longer but stay focused.

### Use detail that changes the image
- Clearly describe subject appearance, state, motion, expression, and attire.
- Use style keywords to define artistic direction.
- Describe light direction, quality (hard/soft), color tone, and time of day.
- Specify shot type, viewing angle, and composition method.
- For multi-image fusion, style transfer, and outfit transfer, uploading reference images improves fidelity.

### Break complex tasks into steps
For multi-element composition or fine editing, step-by-step operation improves controllability.

### Seedream creative uses
Verify the selected model and operation before promising any capability below.
- Precise local editing through interactive controls
- Multi-image fusion of objects, styles, and materials
- High-density information visualization when exact text and layout fidelity are
  not delivery requirements
- Expressive poster, presentation, branding, and e-commerce image layers that
  will be finished deterministically when exact graphics are required
- Multilingual model-rendered text when the user expressly accepts it as
  non-exact; use deterministic finishing for delivery-critical copy
- Cinematic imagery: high-fidelity narrative scenes and portrait retouching

### Fidelity and safety boundaries
- Fully replacing professional designer judgment
- Highly complex layouts requiring precise typographic control
- Generating non-compliant or infringing content
- UI design requiring pixel-level precision
- Delivery-critical copy or layout that must match exactly
- Small text may still be unstable — deterministic finishing is required when
  fidelity matters
