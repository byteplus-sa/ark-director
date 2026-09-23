---
name: seedream-storyboard
description: Create, revise, and optionally generate production-ready cinematic storyboards—from one hero panel with alternatives to a multi-panel continuity sequence—with BytePlus Seedream. Supports two delivery modes — single-image grid (one image containing all panels, default) and separate images (one image per panel). Use whenever the user asks for storyboards, shot boards, continuity boards, storyboard frames, visual sequences, previsualization, scene panels, or image planning for film, advertising, animation, games, or AI video.
---

# Seedream Storyboard

Create storyboards that make narrative, shot, staging, and continuity decisions
clear before expensive production. A storyboard is a sequence-level decision
artifact, not merely a collection of attractive images.


## Input and output contract

Input: scene beats, delivery mode, relevant approved Elements, panel geography, and reference hashes.

Output: panel/grid prompts, provenance, candidate outputs when authorized, and unresolved review requirements.

## Procedure and reference loading

Read context-and-preflight, then panel-and-grid-prompts for authoring. Read generation-and-persistence only when generation is authorized; review-and-selection for promotion, and editing-failed-panels only for a requested revision.

Read only the mode-specific resources needed for the request. Reference paths
mentioned in prose are relative to this skill directory unless a link says otherwise.

- [Context And Preflight](references/context-and-preflight.md) — 1. Inspect existing project context; 2. Lock the brief; 3. Break the scene into observable beats; 4. Decide panel density; 5. Preflight every reference; 6. Establish geography and continuity; 7. Build the panel plan.
- [Panel And Grid Prompts](references/panel-and-grid-prompts.md) — 8. Write the exact prompt for each panel; 9. Write the multi-panel prompt; 9c. Prompt length budget; 9d. Prompt-review gate.
- [Generation And Persistence](references/generation-and-persistence.md) — 10. Generate variants when requested or authorized; 11. Persist every generated result locally; Downloading artifacts; Manifest and metadata.
- [Review And Selection](references/review-and-selection.md) — 12. Review the board; 13. Present variants and capture selection.
- [Editing Failed Panels](references/editing-failed-panels.md) — Edit pattern for a failed panel; HTTPS URL requirement for edits; Grid-to-bbox coordinate mapping; Revision contract.

## Submission boundary and failure behavior

The caller owns production authorization, the exact request preflight, and the
complete hash-bound prompt review. A leaf returns its prompt package without
loading sibling skills. An explicitly declared orchestrator may coordinate the
review and submission stages. Missing required inputs remain unresolved; a draft
or technical success does not establish approval. Preserve optional timing,
the three-image sampling default where applicable, and the requested delta.

## Source authority

Follow the official [capability matrix](https://docs.byteplus.com/en/docs/ModelArk/1824121),
[prompt guide](https://docs.byteplus.com/en/docs/ModelArk/1829186), and
[interactive editing guide](https://docs.byteplus.com/en/docs/ModelArk/2582775).
If live documentation conflicts with a detail below, use it and state the
changed capability.

## What this produces

Depending on the request, produce a beat and panel plan, reference inventory,
spatial and continuity contract, exact prompts and parameters, generated panel
variants, immutable prompt snapshots and metadata, an ordered review package,
and a selection record after a mode-authorized choice.

Keep these artifacts distinct:

- **Storyboard panel:** communicates a decisive story and staging state.
- **Look frame:** locks style, palette, lighting, and materials.
- **Video keyframe:** a polished image promoted as a generation anchor.

A storyboard panel may later become a keyframe, but only after it passes both
storyboard and visual-anchor review.

## Core rules

- Optimize for instant story clarity before polish.
- Describe one frozen, decisive moment per panel.
- **Always use available Elements.** Before writing any prompt, check
  `elements/` for approved character, location, and prop sheets. A storyboard
  must bind every visible Element by its canonical reference so identity,
  geometry, materials, and wardrobe stay on point across panels. A text
  description or an earlier storyboard panel is not a substitute for a
  canonical Element sheet. If an Element has no selected sheet, use the best
  available approved reference; if none exists, record the asset as
  `unresolved` and keep the output as an unlocked draft.
- Honor an explicit panel budget. When the user requests one panel, select the
  strongest representative moment instead of silently expanding the board.
- Without an explicit panel budget, add a panel when visual information or
  state materially changes.
- Keep recurring identities, locations, props, and style in an explicit canon.
- When matching canonical Element sheets exist, attach the selected character,
  location, and visible-prop sheets to the live generation request.
- Treat screen direction and location geography as sequence-level constraints.
- Use coherent natural language, not comma-heavy keyword piles.
- Bind every reference by role and target with exact `@Image N` tokens.
- Prefer local edits to full re-generation after a composition is approved.
- Use seeds for experiment tracking, not as the identity system.
- Put arrows, labels, dialogue, timing, and production notes outside the
  generated image unless visible story-world text is required. Exception: in
  single-image grid mode, thin dividers and panel numbers are part of the
  layout, not annotations — they belong inside the image.
- A technically successful generation enters `review`. A validated agent
  decision in `approve_for_me` or an explicit user choice in
  `ask_for_approval` may set `selected_variant` and `approved` only after a
  passing hash-bound panel review.

## Panel delivery mode

A multi-panel storyboard can be delivered in one of two modes. The choice
affects prompt structure, model selection, output file count, and how panels
are reviewed and promoted.

| Mode | Output | Default? | Best for |
|---|---|---|---|
| **Single-image grid** | One image containing all panels arranged in a grid | Yes | Quick overview, pitch boards, editorial review, sharing a whole scene at a glance |
| **Separate images** | One image per panel (N files) | No | High-resolution per-panel detail, individual editing, video keyframe promotion, continuity-critical sequences |

### When to use each

- **Default to single-image grid** for multi-panel boards unless the user asks
  for separate images or the downstream workflow requires individual panels.
- **Switch to separate images** when: the user requests per-panel editing,
  panels need to be promoted individually to video keyframes, the panel count is
  small and each panel needs high-fidelity detail, or the user explicitly says
  "one image per panel" or "separate panels."
- **A single-image grid cannot be directly promoted to a video keyframe.** To
  promote a panel from a grid, crop it or re-generate that panel as a
  standalone image using the same canon and the panel's recorded prompt.
- **Keep a sketch grid control-only by default.** Translate its composition,
  shot order, and blocking into prompt text. Bind the whole grid to Seedance
  only after a mode-authorized conditioning selection, its current hash
  and manifest selection are recorded, the live mode supports its
  `reference_image` role, and artifact-specific QA is planned. Promotion makes
  it an intentional conditioning input; disabling review or changing
  `control_only` alone does not make it eligible.
- **A one-panel board is always a single image** regardless of mode — the mode
  distinction applies only when the board has two or more narrative panels.

### Grid layout

For single-image grid mode, arrange panels in a reading-order grid. Choose the
smallest grid that fits the panel count:

| Panels | Grid | Reading order |
|---|---|---|
| 2 | 1×2 or 2×1 | match aspect ratio — horizontal for 16:9, vertical for 9:16 |
| 3 | 1×3 or 3×1 | match aspect ratio |
| 4 | 2×2 | left-to-right, top-to-bottom |
| 5–6 | 2×3 or 3×2 | left-to-right, top-to-bottom |
| 7–9 | 3×3 | left-to-right, top-to-bottom |
| 10–12 | 3×4 or 4×3 | left-to-right, top-to-bottom |

Use thin divider lines between panels. Place a small panel number in the
top-left corner of each cell. Do not add speech bubbles, captions outside panel
numbers, watermarks, or decorative borders.

## Render style

A storyboard is a decision artifact, not a finished frame. Its job is to
communicate staging, blocking, composition, eyelines, continuity, and story
beat — not polished color rendering.

**Default to sketch style.** Unless the user requests full color, write
storyboard prompts in a monochrome or limited-palette sketch style. This keeps
generation fast, cheap, and focused on structure rather than surface polish.

| Style | When to use | Prompt keywords |
|---|---|---|
| **Pencil sketch** (default) | Most boards — editorial, continuity, pitch | "rough pencil sketch storyboard, monochrome graphite lines on white, loose shading, no color" |
| **Ink / brush sketch** | When the user wants bolder contrast or cleaner lines | "bold ink storyboard sketch, black brush lines on off-white, minimal cross-hatching, no color" |
| **Charcoal / tonal** | When lighting direction and contrast matter more than detail | "charcoal storyboard sketch, monochrome tonal shading, soft gradients, no color" |
| **Limited palette** | When color coding is part of the staging (e.g. character A warm, character B cool) | "storyboard sketch with limited color: [list only the colors that carry meaning], otherwise monochrome" |
| **Full color** | Only when the user explicitly asks for color, look frames, or style exploration | "full color cinematic storyboard, [palette and lighting]" |

### Sketch and Elements are not in conflict

Sketch style does not mean abandoning canonical Element references. Even in a
pencil sketch, bind approved character, location, and prop sheets as
`@Image N` inputs so the sketch preserves the correct face shape, body type,
costume silhouette, location geometry, and prop form. The sketch simplifies
surface detail — it does not invent a different identity.

In the prompt, pair the sketch style with an explicit binding instruction:

```text
Use the face shape, hair silhouette, and wardrobe cut from @Image 1 for Mara,
rendered as a loose pencil sketch. Preserve the room geometry and doorway
position from @Image 2. Render all surfaces as monochrome graphite — no color,
no texture detail, no material finishes.
```

## Model selection

Choose the path according to the production need.

| Need | Preferred path | Important limits |
|---|---|---|
| Single-image grid storyboard (multiple panels in one image) | Seedream 5.0 Pro, `dola-seedream-5-0-pro-260628` | Single-image output; up to 10 references; 1K/2K; works because the grid is one image |
| Precise single panel, local correction, marked-region edit | Seedream 5.0 Pro, `dola-seedream-5-0-pro-260628` | Single-image output; up to 10 references; 1K/2K; interactive editing |
| Coordinated multi-panel sequence as separate images in one request | Seedream 5.0 Lite or configured 4.x binding | Supports multiple outputs; input references + outputs must stay within the live model limit |
| Three alternatives for one panel | Parallel variation generation | Each output is a candidate, not an ordered story sequence |
| No configured sequence-capable model | Pro, one panel at a time from the same canon | Reuse the same approved anchors and continuity record |

Never invent a model binding. If Lite or 4.x is not configured, either generate
individual Pro panels or deliver the sequence prompt and state what binding is
needed.

Use the delivery aspect ratio from the brief. If absent:

- `16:9` for landscape film, television, presentation, and horizontal ads;
- `9:16` for vertical short-form work;
- use another ratio only when the intended delivery format requires it.

For rough Pro panels, prefer the smallest valid size that preserves the target
ratio, such as `1280x720` for 16:9. Increase resolution only after composition
and continuity are accepted.

## Workflow

## Default response structure

For a one-panel request, return a compact hero-beat decision, one `p010` panel
plan, reference inventory, exact prompt, three variant records, video-handoff
recommendation, review checklist, and selection needed. For a multi-panel plan
or prompt package, return the panel delivery mode (single-image grid or
separate images), render style (sketch default or full color), assumptions and
locks, reference inventory, beat and panel plan, spatial and continuity
contract, generation setup, exact panel prompts, review checklist, and open
decisions. When images were actually generated, add generated variants and the
technical record.

Do not claim that a storyboard, asset, or variant exists unless it was actually
generated and saved.

## Compose with other skills

- Compose with `seedream-character-sheet` / `seedream-location-asset` (and prop
  sheets via `seedream-prompt`) for canonical Element references in every panel.
