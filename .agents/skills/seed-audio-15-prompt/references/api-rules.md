# API Documentation Rules Summary: 1.5 Installed Edition

Original material compiled: 2026-10-10; stem-separation and prompting strategies updated: 2026-11-04. The supplied bundle labels this edition “1.5”; that label is not a model selection or confirmation by the current user. Parts of the supplied demonstration/requirements documents use other version names; do not rename this edition or claim official API availability on that basis. This package is based on user-supplied requirements and practice documents. It summarizes prompt-expressible capabilities and provisional constraints, not a complete formal API specification; it neither invents API specifications nor calls APIs.

## Evidence and status

Private source URLs are omitted from this repository adaptation. The source
titles and compilation dates below describe the supplied bundle's provenance;
they do not imply independent source access or verification during installation.
Public links are retained as references, not as verified availability evidence.

- Best practices for audio-track separation prompts (supplied private source), read on 2026-11-04, document PE version 5.0: source-mix separation, positive targets, exact quote anchors, grouped tracks, singing ownership, and acoustic effect descriptions. The PE version does not rename this model-adapter edition.

- New product demonstrations, complex timelines, and track examples (supplied private source): primary basis for sound-control writing and demonstrated capabilities.
- User-provided new requirements document (supplied private source): provisional basis for input combinations, length, and extraction output counts. Requirements material is not a formal API guarantee.
- [Official Dreamina SeedAudio 1.5 introduction](https://dreamina.capcut.com/ai-model/seedaudio-1-5): supplementary product descriptions of audio references, video accompaniment, complex timing, and tracks; not evidence for formal API fields or launch status.

Shared files remain version-independent; this file sets the current package's boundaries at execution. Do not impose old public-API limits of 3000 characters and 3 audio references on this edition; equally, do not advertise tentative new limits as formal API commitments.

## Capabilities usable in optimization

- Natural-language joint creation of voices, music, ambience, and effects.
- Audio references for character timbre and expression: specify character, asset, and desired reference attributes. Users may request timbre, accent, emotion, style, or rhythm references, without a guarantee that arbitrary attributes are fully isolated.
- Video references for dubbing, scoring, and effects, optionally together with voice-reference audio. Let the model use the assets; this skill does not observe them or invent shots/actions.
- Complex time intervals to organize dialogue, music, ambience, and action effects, including meaningful concurrent sounds. Actual adherence has not been tested in this project.
- Specified sound extraction/separation from input source audio. Demonstrations include character vocals, music, ambience, and particular effects; precise source separation is not guaranteed.

**Track scope:** Support prompt writing for separation/extraction from an original mix: characters, all voices, instrumental music, music including singing, ambience/specific effects, or requested combinations. Organize source, track count, and positive target per track; identify complex speakers through supplied exact lines, not visual positions or invented timbres. See guide section 13. A request only for a well-layered mix remains about prominence; do not turn it into a separation task.

The practice document describes an audio-understanding/prompt-enhancement/extraction pipeline. This optimizer writes text only; it does not listen blind, detect speakers, extract audio, or claim completed track files. The document does not establish a single new-generation call simultaneously returning a mix and all independent tracks. For that explicit requirement, explain the host-workflow uncertainty and give a pending proposal rather than silently returning only a mix.

## Supplied planning duration and provisional input/output constraints

| Item | Rule in new materials | Optimization handling |
| --- | --- | --- |
| Generation duration | Supplied profile's planning ceiling: 6 minutes, or 360 seconds; not independently verified | Within this profile, total duration and every interval endpoint must be within 360 seconds. Clarify shortening or segmentation if exceeded; never truncate automatically. |
| Prompt | Requirements document text field: at most 10000 characters; longer text may be automatically truncated | Use 10000 as this package's provisional checking ceiling. Do not rely on truncation; clarify splitting if faithful compression still exceeds it. |
| Audio references | Up to 6; demonstrations describe a 6-minute audio-reference length capability | Provisionally organize at most 6 references. Do not infer generation-duration or total-asset-duration guarantees from that 6-minute reference rule; precise measurement boundaries await formal API confirmation. |
| Video references | Up to 1, usable together with audio references | Preserve user video tags and sound responsibilities; invent no asset properties. |
| Image references | Requirements document: up to 1, not simultaneous with audio/video inputs | Not a primary task; do not add proactively. Clarify explicit conflicting requests. |
| Source-audio extraction outputs | Requirements document: one or multiple tracks, up to 6 | Organize user-specified outputs when targets are clear. Clarify more than 6; do not silently combine targets. |
| Asset formats/sizes and reference fields | No complete formal API rules confirmable in this project | Do not inherit old parameters or invent new values. Do not question ordinary creative users merely because fields are unknown. |

The source bundle records a 6-minute (360-second) ceiling; retain it as this package's supplied planning rule, not current-user confirmation or a formal service guarantee. Before actual generation, the caller must independently verify the selected destination's limits and account access. Audio-reference length remains a separate asset rule and must not be confused with generation duration. Final prompts may contain creative total duration, but not this table's field names, limit explanations, or edition names.

## Timing feasibility check

Follow the shared guide: total duration and interval endpoints within 360 seconds; line capacity compatible with pace, pauses, and nonverbal performance; enough time for serial actions and explicit silence. Do not default unspecified duration to 6 minutes. Clarify segmentation only when content clearly cannot finish naturally within the maximum. Being below the maximum does not itself establish a feasible schedule.

## Reference principles

Examples refer to existing audio with `@音频1` etc. Normalize optimizer output to `@音频X`: normalize established references such as `{{Audio 1}}` or `@Audio1` to `@音频1`, preserving original number and role. This is this skill's output convention, not a claim that every entry point accepts only this syntax. Use `@音频1` for one known unnumbered audio asset; clarify multiple unnumbered assets with unclear relationships. Do not replace tags literally intended for speech within lines. Video tags retain references supplied by the user or host; invent no standardized video tag.

A timbre reference and source audio for extraction have different responsibilities. Preserve existing mappings; ask first when multiple assets and characters cannot be paired. A prompt does not substitute for actually supplying assets.

## Timeline form

Use the sources' `[start s:end s]` notation without spaces inside numerical labels, e.g. `[6.3s:10.5s]`. State an established total duration at the start. Continuous music/ambience may span multiple lines. Put intervals beside their sound objects; define roles in advance if useful.

Literal Chinese prompt example:

> 总时长 12 秒。阿宁的声音清亮，表达从迟疑转为坚定。
> [0.0s:12.0s] 轻柔钢琴在背景铺底，对白时保持较轻，最后两秒渐弱。
> [2.0s:5.0s] 阿宁说：“我会回来。”
> [4.5s:6.0s] 在台词末尾响起轻微衣料声，随后脚步渐远。

This example is not a universal default. Use time labels only when users supplied the corresponding time points/intervals or explicitly authorized timeline design. Total duration does not authorize segmentation. With total duration only, use natural-language total duration and event order, adding neither segment nor whole-piece labels. Local timing does not authorize filling other segments; relative pauses do not become calculated absolute intervals. Endpoints must not exceed an explicit total duration or this edition's 360-second ceiling. Preserve purposeful cross-layer overlap; resolve unreasonable simultaneous repeated speech by the same character. Interval start must precede end. Clarify conflicting user values rather than changing times yourself.

Special separators in isolated source examples have not been confirmed as mandatory syntax. Timestamps are creative control, not guarantees of frame/sample precision or fixed timing tolerance.

## Stem-separation / extraction form

“Extract three tracks from @音频1: ① all voices; ② background music; ③ all effects.” Use the input-appropriate language.

“Extract two voice tracks from @音频1: ① all vocal content of the speaker who said ‘Oh, yes. I like that’; ② all vocal content of other speakers.” Preserve the quote exactly, including punctuation; do not perform it again.

“Separate the original mix into three tracks: ① male spoken dialogue; ② the old lady's voice; ③ background music including male singing.” Preserve requested singing inclusion, grouped speakers, combined music/effects, and conditional BGM; do not force one track per character or a universal three-way split.

Use only supplied sources and audible traits, not clothing, color, screen position, or invented timbre. Missing crucial identification or an unclear retained target in a removal-only request requires a concrete clarification and pending draft. Keep explicit exclusions brief; define positive targets first without adding unrelated negative-source lists.

Preserve original content, order, and performance. Do not edit lines/quote anchors, redub, stylize, add new effects, or automatically prepend the 40kHz generation header. Output an optimized extraction prompt only. The new practice document does not establish a new universal track-count ceiling; retain the provisional limit above.

## Audio reference with bare dialogue

When one known timbre reference is bound to input dialogue, use the standard tag plus current-line performance and original line. Literal Chinese template: “说话者（@音频1）以诚恳的语气、自然语速说：‘原台词’”. Do not infer age, gender, identity, personality, or voice characteristics from text, or claim audio analysis. Invent no reference without existence/tag information. See the shared sound guide for details. These examples do not authorize translating input-language output.

## Quality cues and user-supplied delivery conditions

Users authorize an optional opening for generation: “Audio specification: sample rate approximately 40.00 kHz, stereo. Overall, a … style.” This is quality/style guidance, not mandatory for every prompt, an API field, a measured outcome, or an actual file guarantee. Original sample rate, mono/stereo, encoding, and aesthetic requirements take precedence; never override or append conflicting specifications. Actual file parameters depend on generation/export settings, and ordinary creative bodies need no configuration explanations or warnings. Extraction does not automatically use the header or remake source audio; preserve explicitly requested output specs. Clarify an explicitly unsupported condition only when alternatives are unacceptable; unknown configuration is no reason to delete a requirement. Independent-track counts and generation/extraction methods remain subject to this edition's boundaries.
