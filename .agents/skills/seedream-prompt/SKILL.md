---
name: seedream-prompt
description: Write structured Seedream 5.0 Pro/Lite image generation prompts with input reference labeling, subject definitions, style and composition control, interactive image editing (local edits, sketch rendering, layer separation, multi-image fusion, color/material replacement), high-density infographics, sequential generation, and constraints. Invoke when the user asks for a Seedream prompt, generated or edited imagery, infographics, or expressive poster/UI/brand artwork. Do not use it to reproduce exact static typography, pricing, CTA, product-grid, logo, or pixel-layout geometry that deterministic HTML-entrypoint graphics can render.
---

# Seedream Prompt

Write production-grade prompts for BytePlus Seedream 5.0 Pro (`dola-seedream-5-0-pro-260628`) and Seedream 5.0 Lite. Seedream 5.0 Pro is a multimodal image creation model that goes beyond generation — it understands design intent, supports interactive precision editing, produces high-density infographics, natively renders text in 14 languages, and delivers cinematic realism with accurate lighting and materials.


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

The prompt structure and rules in this skill are sourced from:
- [Seedream 5.0 Pro official blog](https://seed.bytedance.com/en/blog/beyond-generation-it-understands-design-introducing-seedream-5-0-pro) (2026-07-08)
- [Seedream 4.0-5.0 API Tutorial](https://docs.byteplus.com/en/docs/ModelArk/1824121)
- [Seedream 4.0-4.5 Prompt Guide](https://docs.byteplus.com/en/docs/ModelArk/1829186)
- Seedream 5.0 Pro User Manual (Lark wiki, internal)

When the official guide is updated, prefer the live page over this skill where they conflict.

## Character-sheet routing

For character sheets, identity sheets, turnaround sheets, or Seedance-facing
character references, prefer the sibling `seedream-character-sheet` skill rather
than embedding that workflow here.

If the generated character sheet later needs duplicate-face cleanup, optionally
compose with the companion `seedream-character-sheet-cleanup` skill.

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

### What Seedream 5.0 Pro is good at
- Precise local editing through interactive controls
- Multi-image fusion of objects, styles, and materials
- High-density information visualization when exact text and layout fidelity are
  not delivery requirements
- Expressive poster, presentation, branding, and e-commerce image layers that
  will be finished deterministically when exact graphics are required
- Multilingual model-rendered text when the user expressly accepts it as
  non-exact; use deterministic finishing for delivery-critical copy
- Cinematic imagery: high-fidelity narrative scenes and portrait retouching

### What Seedream 5.0 Pro is not suited for
- Fully replacing professional designer judgment
- Highly complex layouts requiring precise typographic control
- Generating non-compliant or infringing content
- UI design requiring pixel-level precision
- Delivery-critical copy or layout that must match exactly
- Small text may still be unstable — deterministic finishing is required when
  fidelity matters
