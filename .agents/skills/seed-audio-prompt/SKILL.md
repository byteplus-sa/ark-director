---
name: seed-audio-prompt
description: Write structured Seed Audio 1.0 prompts for full-soundscape audio generation including dialogue, music, SFX, and ambience. Supports text-to-audio (T2A) and text-plus-audio-to-audio (TA2A) with voice cloning. Invoke when the user asks to generate Seed Audio 1.0 prompts, write audio prompts for BytePlus audio generation, create audiobook/dialogue/soundscape scripts, or design multi-character audio scenes.
---

# Seed Audio Prompt

Write production-grade prompts for BytePlus Seed Audio 1.0 (model ID `seed-audio-1.0`), a multimodal full-soundscape generator that produces dialogue, background music, sound effects, and ambience in a single pass. Unlike traditional TTS, Seed Audio 1.0 is an "audio director" that interprets scene descriptions, character voice profiles, and script content simultaneously.


## Input and output contract

Input: audio purpose, exact dialogue where present, sound layers, output configuration, and optional voice references.

Output: a complete T2A or TA2A soundscape prompt and explicit ordered bindings.

## Procedure and reference loading

Read references-and-modes plus soundscape-arrangement. Add dialogue-and-voices only for speaking/singing characters. Music, ambience, and SFX beds do not require dialogue or narrative obstacles. Timestamp control is optional when timing is not requested.

Read only the mode-specific resources needed for the request. Reference paths
mentioned in prose are relative to this skill directory unless a link says otherwise.

- [References And Modes](references/references-and-modes.md) — Input references; Generation mode.
- [Soundscape Arrangement](references/soundscape-arrangement.md) — Full-soundscape composition workflow; Scene transitions and dynamic arcs; Scene and atmosphere.
- [Dialogue And Voices](references/dialogue-and-voices.md) — Characters and dialogue.
- [Templates And Quality](references/templates-and-quality.md) — Reusable full-soundscape template; Creative and quality constraints; Conversational voiceover recipe (T2A); Brand-name pronunciation; hypothetical crowded-soundscape repair.
- [Worked Examples](references/worked-examples.md) — Full example: T2A — Sci-fi news broadcast; Full example: TA2A — Multi-character fantasy battle dialogue; Full example: T2A — Timestamp control.
- [Api Reference](references/api-reference.md) — Quick reference card; Model identity; Request body; Response fields; Limits; Output configuration (`audio_config`); Watermark (`watermark` object); Pricing; Long-form pattern; Prompt language.

## Submission boundary and failure behavior

The caller owns production authorization, the exact request preflight, and the
complete hash-bound prompt review. The caller reviews inline by default and
uses a sub-agent only when the user explicitly requests sub-agent prompt review
for the project or specific generation. A leaf returns its prompt package without
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

The public API reference is the authoritative source of truth for request fields and limits. Prompt-writing conventions originate from the internal Seed Audio 1.0 prompting guide and are labeled where they are not defined in the public API.
- [Seed Audio 1.0 API Reference](https://docs.byteplus.com/en/docs/byteplusvoice/seedaudio-01) — authoritative
- [Seed Audio 1.0 Prompting Guide](https://bytedance.larkoffice.com/wiki/WgU4wFVQ8iZgvjkHHdbcDmhCnug) — T2A/TA2A prompting conventions and examples, modified July 23, 2026
- [Seed Audio 1.0 Pricing](https://docs.byteplus.com/en/docs/byteplusvoice/audiopricing) — authoritative

Seed Audio 1.0 is in early access. Applications for early access are open via a whitelist form; confirm current access status before building.

When the official API reference is updated, prefer the live page over this skill where they conflict.

## Prompt assembly

Build the shortest prompt that clearly communicates the requested result. Use plain-language headings only when they improve readability, and omit sections that do not apply.

For full-soundscape generation, cover the five ingredients recommended by the prompting guide:

1. The environment: location, weather, context, and acoustic space
2. Background music and sound effects
3. Character actions or appearance when they affect the performance
4. Each character's voice: age, gender, accent, emotion, tone, speed, and timbre as relevant
5. The exact dialogue

Arrange those ingredients as one chronological audio scene, not as unrelated inventories. A typical prompt follows this order:

1. Input references, only when the request includes reference audio
2. Opening environment, ambience, and music
3. Dialogue, actions, and sound effects in the order they occur
4. Ending behavior: resolve, fade, sustain, or cut
5. Creative or quality constraints, only when the user supplies them

Generation mode and request limits belong in request metadata or validation, not in model-facing prompt boilerplate.

## Ideal use cases

- **Audiobooks**: Prototype narration, dialogue and sound design. Human performance, editing and cost comparisons depend on the project; no universal replacement or savings claim is implied.
- **Video dubbing**: Generate character voices from text descriptions or reference audio. Human voice + SFX + background music in a single pass.
- **Gaming**: Generate character voices and environmental sound effects for immersive player experiences.
- **Podcast and radio drama**: Multi-character dialogue with full sound design from a single prompt.
- **Language learning content**: Generate audio in multiple languages, with per-sentence timestamp guidance for precise timing control.

## What makes Seed Audio 1.0 different from normal TTS

| Feature | Audio 1.0 | Normal TTS |
|---|---|---|
| Text-to-Speech | ✅ | ✅ |
| Voice Cloning | ✅ | ✅ |
| Text Prompt to Audio (T2A) — describe voice, atmosphere, BGM, SFX in free text | ✅ | ❌ |
| Text Prompt + Audio to Audio (TA2A) — reference audio + text prompt for voice/emotion reference | ✅ | ❌ |
| Multimodal soundscape (dialogue + music + SFX + ambience in one pass) | ✅ | ❌ |
| Prompting-guide time control per sentence (`[start_time:end_time]`) | ✅ | ❌ |
| Multilingual generation | ✅ | Varies |

## Related skills

- `seed-audio-commercial` — dramatic, story-driven audio commercials
- `audio-dubbing` — dubbing pipeline with voice cloning (TA2A)
- `audio-split` — reference audio segmentation for ≤30s clips
