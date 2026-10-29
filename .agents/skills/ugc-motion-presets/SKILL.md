---
name: ugc-motion-presets
description: >
  Turn a named UGC motion preset into a canonical Seedance 2.5 prompt block.
  Use when the user names one of the 45 presets (Atomic, Outfit Switch,
  Eating Zoom, Group Photo, Yacht, ...) or asks for
  preset-style UGC motion — reaction, selfie, fashion, eating, VFX spectacle,
  action, timelapse, or multi-shot formats. Persuasion angle, claims, and CTA
  belong to ugc-ad-modes; prompt grammar belongs to seedance-prompt-25. Presets
  with a locked-off camera block record `format_static_by_design`; multi-shot
  presets take a shot plan. Never generates media.
---

# UGC Motion Presets

This skill turns a named UGC motion preset into a canonical, drop-in
prompt block for Seedance 2.5: the preset's motion grammar (timestamped action,
camera treatment, audio direction) plus reference bindings, duration, and
constraint flags. It is a **prompt-composition-only** skill: it never calls MCP
tools or the Ark API, and it never runs generation. The base grammar — the
six-part formula, `@Image N` / `@Video N` reference-role syntax, `At Ns`
timestamp syntax, and audio bracket syntax — is defined in
`seedance-prompt-25` and is **not redefined here**.

The recipes are **optional creative heuristics**. They are not platform
ranking rules, API requirements, or demonstrated conversion gains. No preset
outperforms another by any measured claim in this bundle.

## Preset index

Resolve the user's request to one preset, then read **only its category
section** in the recipe file listed for it. The shared recipe rules sit at the
top of [motion-presets.md](references/motion-presets.md).

| Category | Presets | Recipe file |
|---|---|---|
| Emotion / reaction | Angry Mode, Crying, Happy, Happy Mode, Shocked, Saint Glow, Sunglasses | [motion-presets.md](references/motion-presets.md) |
| Selfie / posing | Selfie, Selfie Outfit, Selfie Posing, Static Posing, Fix and pose, Group Photo | [motion-presets.md](references/motion-presets.md) |
| Outfit / fashion | Outfit Check, Outfit Switch, Clothes Rain, Hair Style, Sand Cut | [motion-presets.md](references/motion-presets.md) |
| Eating / product | Eating, Eating Zoom, Plate Check | [motion-presets.md](references/motion-presets.md) |
| VFX spectacle | Atomic, Explosion, Firework, Northern Lights, Aquarium, Color Rain, Money Rain, Pizza Fall, Cotton Cloud, Gas Transformation, Beast Appearance, Giant Grab | [motion-presets-spectacle.md](references/motion-presets-spectacle.md) |
| Action / movement | Handheld Run, Pool Jump, Ballet, Motor Ride, Beach Ride, Train Rush, Peak Moment | [motion-presets-action-story.md](references/motion-presets-action-story.md) |
| Lifestyle / timelapse | Morning routine, Timelapse Glam, Timelapse Human | [motion-presets-action-story.md](references/motion-presets-action-story.md) |
| Multi-shot story | Yacht, BTS | [motion-presets-action-story.md](references/motion-presets-action-story.md) |

## Resolve the preset

1. **Exact name** — match case-insensitively to the index.
2. **Description without a name** ("that mushroom cloud selfie one") — resolve
   to the closest preset and state the assumption in one line before the
   prompt block.
3. **No fit** — say no preset matches; do not invent one. Offer the nearest
   preset or a custom direction composed from `seedance-prompt-25` grammar.
4. **Persuasion content requested** (claims, CTA, script, hook strategy) —
   deliver the preset block and route angle/claims/CTA to `ugc-ad-modes` in
   one line. Do not write persuasion copy here.

## Recipe schema

Every recipe in the three recipe files provides:

| Field | Use |
|---|---|
| `id` | Lowercase kebab-case preset ID |
| Category | The section heading the recipe sits under (one of the eight index categories) |
| Grammar | single-pass R2V, structured edit, chained, or one-click |
| References | Role bindings and counts for the user's media |
| Ratio | Default 9:16 unless the request says otherwise |
| Motion block | Timestamped, cue-level action — fills the Action slot |
| Camera block | Named technique — fills the Camera slot |
| Audio | Native audio direction |
| Duration | Integer seconds, 4–30 single-pass |
| Flags | Provider constraints, QA cautions or creative heuristics, labeled by kind in the output notes |
| Persuasion hint | Optional one-line hook idea; angle/CTA stay with `ugc-ad-modes` |

## Composition rules

- Recipe audio is native ambience. For an ambience-only or music-free result,
  set `generate_audio: false` and add a Seed Audio bed in post (not
  frame-synced); native audio can leak music or speech despite the line.
- Recipes fill the six-part formula slots; the caller assembles the full
  prompt per `seedance-prompt-25` and owns `prompt-review`, submission, and
  showcase sync.
- Bind the user's character, wardrobe, or product media using the recipe's
  reference roles. A held or worn product visible in frame follows the
  workspace element policy — canonical props get locked references, incidental
  generics may be described.
- Keep every Flag visible in the composed prompt or the pre-submission notes;
  distinguish provider constraints from QA cautions and creative heuristics.
  Creative heuristics yield to source intent; do not turn a preset's moderate
  speed, burst caution or hold into a provider limit or universal energy cap.
- Duration, resolution, ratio, and watermark are generation parameters — they
  stay in the API call, never in the prompt text.
- Acting intensity is expressed through observable physical cues, never degree
  adjectives; compose with `seedance-acting-console` when the emotion needs
  deeper cue work.
- Every composed prompt carries the generation-safe flags: exact counts and
  positions at every timestamp, hands named by anatomy plus frame side,
  unreferenced props described plain with nothing printed, and native audio
  checked for leaked music or speech.
- Structured edits and `extend` of footage that shows a person need that
  person as an `asset://` asset and a muted source; otherwise use the recipe's
  fresh-generation variant.
- Deeper execution constraints — parameter map, task-type enum, cross-cutting
  QA and the four flagged presets — live in
  [execution-constraints.md](references/execution-constraints.md).

## Delivery guardrails

Defaults for UGC placement, stated as defaults rather than rules:

- **9:16 vertical** unless the request specifies another ratio.
- **Design for sound-off legibility.** Captions, CTAs, logos as graphics and
  end cards are a finishing layer (FFmpeg or HyperFrames) — never baked into
  generated video.
- **Brand or product visible early** in the first seconds of the cut.
- **Platform AIGC disclosure** (an upload-time tag or the platform's own
  labeling) is a delivery reminder for the caller. Do not burn "AI-generated"
  or "fictional" labels into the video by default.
- **A synthetic presenter is never framed as a real customer.** Generated
  imagery illustrates a concept; it is not testimony. Generated talking heads
  do not claim personal purchase or use histories.
- **No performance ranking between presets.** Traction claims about formats
  stay out of prompt deliverables.

## Self-check

1. The resolved preset exists in the index; ambiguous resolutions state the
   assumption; unknown requests are not invented.
2. The output is a prompt block (motion, camera, audio, reference bindings,
   duration, flags) — not a full persuasion script.
3. Motion direction is timestamped, cue-level, and physically observable; no
   degree adjectives carry intensity.
4. Reference roles match the recipe and the user's supplied media.
5. All recipe flags survive into the output with their kind distinguished;
   creative cautions do not override source intent or justify invented API limits.
6. 9:16 and sound-off defaults are respected or explicitly overridden.
7. Claims, CTA, and testimony requests were routed to `ugc-ad-modes`, not
   answered here.
8. Duration, resolution, ratio, and watermark appear only as generation
   parameters, never in prompt text.
9. Counts, hand sides and plain-prop wording are explicit; footage edits with
   people name their `asset://` binding or fall back to fresh generation.
