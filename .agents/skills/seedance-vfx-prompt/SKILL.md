---
name: seedance-vfx-prompt
description: >-
  Write prompts for edits to existing footage: background replacement, creature
  or object integration, product, wardrobe, prop, or single-character swaps,
  world changes, relighting, weather, dialogue, and timed camera effects.
  Default to Seedance 2.5 structured edit-goal grammar; retain legacy 2.0
  headings and compact VFX recipes for explicitly selected supported paths. Use
  source inspection, ordered @Video N/@Image N bindings, a declared
  may-change/must-preserve contract, physical lighting, layered space, timing,
  audio, and face-fidelity QA. Exclude new T2V/I2V shots, still-image creation,
  whole-cast motion recasts, and task submission; the caller owns the
  generation lifecycle.
---

# Seedance VFX Prompt

Write production-grade prompts for BytePlus Seedance 2.0 **video-to-video VFX
editing**. This skill is for editing **existing footage** — not text-to-video
generation. The source clip is the anchor; the prompt describes what to change.

Use this skill when the user wants to:
- **replace a background or location** in an existing video clip
- **add or modify an element** in-frame (creature, object, effect)
- **rebuild the entire environment** around a moving-camera shot
- apply any **footage-driven visual effect** with Seedance
- chain VFX shots where the last frame of one becomes the first frame of the next

Do **not** use this skill for:
- text-to-video generation from a blank prompt (use `seedance-prompt-25` for 2.5, `seedance-prompt-20` for 2.0)
- image-to-video from a still frame (use `seedance-prompt-25` for 2.5, `seedance-prompt-20` for 2.0)
- character sheet or location still generation (use Seedream skills)
- rebuilding the whole cast, wardrobe and world while keeping only the source
  motion, camera and timing — that is a motion-recast task
  (`seedance-motion-recast`), not this skill

> **Version note**: This skill covers **both** Seedance generations. The core
> methodology (sections 1–11) is written for Seedance 2.0. For Seedance 2.5
> video-to-video editing — the preferred path for full-duration edits — see
> [Seedance 2.5 editing](references/seedance-25-edit.md#seedance-25-editing) below; the `seedance-prompt-25`
> skill remains the authority for 2.5 T2V/R2V and native extension. For 2.0
> T2V/R2V prompts, use `seedance-prompt-20`.

> **2.5 resolution guard**: Seedance 2.5 supports 480p/720p/1080p output. The
> 4K face-protection methodology below is 2.0-only. For face-critical structured
> edits on 2.5, weigh 1080p fidelity against 2.0's 4K path. For 4K output,
> stay on 2.0.

This skill is designed to partner with:
- `seedance-vfx-pipeline` for the end-to-end submission, poll, and save pipeline
- `seedance-prompt-20` for Seedance 2.0 text-to-video and image-to-video generation
- `seedance-prompt-25` for Seedance 2.5 text-to-video, R2V, and structured editing
- `seedream-*` skills for generating reference images used in VFX prompts


## Input and output contract

Input: an inspected source clip, model and edit operation, and may_change/must_preserve contract.

Output: a mode-appropriate VFX prompt with ordered source/Element bindings.

## Procedure and reference loading

Use seedance-25-edit for the default 2.5 branch. Legacy source/change, integration, and compact references apply only to an explicitly selected supported 2.0 path; the legacy 4K examples never set 2.5 parameters.

Read only the mode-specific resources needed for the request. Reference paths
mentioned in prose are relative to this skill directory unless a link says otherwise.

- [Legacy Source And Change](references/legacy-source-and-change.md) — 1. Asset preparation (always first); 2. Subject definitions; 3. Prompt and task type; 4. Locks; 5. Change; 6. New world.
- [Integration And Timing](references/integration-and-timing.md) — 7. Lighting (embedded); 8. Space (layered); 9. Timing (if applicable); 10. Audio (diegetic only); 11. Quality and constraints.
- [Legacy Vfx Levels](references/legacy-vfx-levels.md) — The three VFX levels.
- [Fidelity And Continuity](references/fidelity-and-continuity.md) — Resolution: model and operation first; Photoreal creature / element integration; Duration discipline; Integrating with project elements; Chaining VFX shots.
- [Compact Legacy](references/compact-legacy.md) — Alternative: compact format; Structure patterns (quick reference); Seedance 2.0 input limits (reference).
- [Seedance 25 Edit](references/seedance-25-edit.md) — Seedance 2.5 editing.
- [Object Swap](references/object-swap.md) — Seedance 2.5 product, wardrobe, prop, or single-character swap: object count, Timeline Inheritance, residual-original guard, contact and occlusion, worked example, swap QA.

## Submission boundary and failure behavior

The caller owns production authorization, the exact request preflight, and the
complete hash-bound prompt review. A leaf returns its prompt package without
loading sibling skills. An explicitly declared orchestrator may coordinate the
review and submission stages. Missing required inputs remain unresolved; a draft
or technical success does not establish user approval. Preserve optional timing,
the three-image sampling default where applicable, and the requested delta.

## Source authority

The VFX methodology in this skill is sourced from:
- [Dreamina Seedance 2.0 prompt guide](https://docs.byteplus.com/en/docs/ModelArk/2222480)
- [Seedance video generation API](https://docs.byteplus.com/en/docs/ModelArk/1520757)
- Project conventions for asset structure and `@tag` references (characters, locations, props live under `elements/<element-id>/` and are referenced by `@tag` in prompts)

When the official guide is updated, prefer the live page over this skill where
they conflict.

## Core principle: the source clip is the lock

In VFX editing, the source video is the **identity anchor**. The prompt must
preserve what the model should keep (subject identity, performance, camera
motion) and describe only what should change. Never write a VFX prompt that
re-describes the entire scene from scratch — that tells the model to ignore the
source footage.

The `@Video N` source-clip binding plus the `Locks:` heading enforce this
discipline. VFX prompts use the same natural-language heading style as the
general `seedance-prompt-20` skill — short descriptive words followed by a colon,
never decorative delimiters.

A VFX prompt is only as good as the source footage. **Shoot each clip already
knowing the effect you want** — stable, well-lit, single-subject footage with a
clear, describable camera motion locks more reliably than improvised footage.
That one habit makes every downstream prompt easier to write and more likely to
hold.

## Recommended prompt structure — VFX Edit

Legacy Seedance 2.0 VFX prompts follow the same heading convention as the general
`seedance-prompt-20` skill: short natural-language headings with a colon, no
decorative delimiters. Assemble in this order. Omit a heading only when it does
not apply to the task.

```text
Asset preparation:
@Video 1: source clip — [subject, action, camera motion, duration]
@Image 1: [element reference] — [role: character/location/prop sheet]
@Image 2: [texture reference] — [role: texture only, ignore background/lighting]

Subject definitions:
Define the [2-3 core static features] in @Video 1 as [Subject_Label]

Prompt:
Task type: Video Editing
Strictly edit @Video 1, and modify [what changes] at [timestamp]. Preserve [locks].

[New world — full description of the replacement or added environment/element]

Lighting: [lighting that lives inside the world, never a pasted-on layer]

Space: [foreground, midground, background depth]

Timing: [when the change triggers, how it progresses — if applicable]

Audio: [diegetic sound that physically exists in the new world]

Quality and constraints:
Quality: photoreal, 4K, [look/grade]
Constraints: [NON-IP, face protection, no-warp, camera-motion lock, etc.]
```

## Iteration discipline

The user iterates fast and in small steps: "softer light," "from the right,"
"bigger snowier mountains," "make the chimp huge," "a beat before the zoom,"
"keep the original runtime." Change **only the named thing** and keep the rest
of the prompt stable — re-rolling the whole prompt loses what already worked.

When refining a generated still or frame, edit the chosen result (pass it back
as the base) and fix only what is off, rather than starting over.

## Voice

Write in a terse, kinetic, physically precise director's voice within each
heading section. Name exact materials, behaviors, scale, lenses, angles, and
moves. Avoid generic adjectives — no "beautiful," "stunning," "amazing,"
"cinematic" — use texture words instead. Don't inflate, don't soften, don't
explain what things "represent."

## VFX prompt checklist

For a supported legacy 2.0 VFX prompt, verify the items below. For 2.5 editing,
use the checklist in [the 2.5 edit reference](references/seedance-25-edit.md);
do not impose legacy headings or 4K parameters on that branch.

- [ ] **`Asset preparation:` is first** — `@Video 1` is the source clip, with
      subject, action, camera motion, and duration in the role description
- [ ] **Source inspected** — duration, fps, aspect probed; `@Video 1` role built
      from footage, not from a one-line summary
- [ ] **`Subject definitions:`** — subjects defined with `Define ... in @Video 1
      as <Label>`, 2-3 static features each
- [ ] **`Prompt: Task type: Video Editing`** — `Strictly edit @Video 1` declared
- [ ] **`Locks:`** — identity, performance, and camera motion are locked, using
      `<Label>@Video 1` binding
- [ ] **Change named with timestamp** — `At 0:NN` for localized changes
- [ ] **`New world:`** — the replacement/added element is fully described
- [ ] **`Lighting:`** — light sources are physical, not pasted
- [ ] **Lighting fork decided** — preserve-subject vs relight-all chosen
      explicitly
- [ ] **Integration recipe applied** — light direction, environmental bounce,
      optics/atmosphere, edges/grounding (if subject composited into new world)
- [ ] **`Space:`** — foreground, midground, background depth
- [ ] **`Timing:`** — sequential changes have timestamps (if applicable)
- [ ] **Timed moves dual-anchored** — semantic + numeric cues (if camera move
      synced to dialogue)
- [ ] **Lip-sync window checked** — quoted line fits the surviving dialogue
      window (if lip-sync is the payoff)
- [ ] **`Audio:`** — every sound has a physical source; `SFX [and source
      dialogue] only` declared
- [ ] **`Quality and constraints:`** — applicable rights, visible face detail,
      source locks, and quality criteria included
- [ ] **Supported resolution** — validated for the selected model and operation;
      faces require output QA rather than an automatic switch to 4K
- [ ] **`@tag` references** — project elements referenced by tag and bound to
      `@Image N`, not re-described
- [ ] **Creature realism demanded** — wildlife-doc realism, species behavior,
      scale explicit (if creature added)
- [ ] **Texture `@Image N` reference** — second input added if CG still reads
      fake (if creature added)
- [ ] **Living micro-movements** — added for static creature holds
- [ ] **Prepended-intro budget computed** — `total − intro = surviving window`
      (if intro prepended)
- [ ] **Iteration discipline** — only the named change applied, rest of prompt
      stable (if iterating)
