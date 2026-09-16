---
name: ugc-motion-presets
description: >
  Turn a named Higgsfield UGC Builder motion preset into a canonical Seedance
  2.5 prompt block. Use when the user names one of the 45 UGC Builder presets
  (Atomic, Outfit Switch, Eating Zoom, Group Photo, Yacht, ...) or asks for
  preset-style UGC motion — reaction, selfie, fashion, eating, VFX spectacle,
  action, timelapse, or multi-shot formats. Persuasion angle, claims, and CTA
  belong to ugc-ad-modes; prompt grammar belongs to seedance-prompt-25. Never
  generates media.
---

# UGC Motion Presets

This skill turns a named UGC Builder motion preset into a canonical, drop-in
prompt block for Seedance 2.5: the preset's motion grammar (timestamped action,
camera treatment, audio direction) plus reference bindings, duration, and
constraint flags. It is a **prompt-composition-only** skill: it never calls MCP
tools or the Ark API, and it never runs generation. The base grammar — the
six-part formula, `@Image N` / `@Video N` reference-role syntax, `At Ns`
timestamp syntax, and audio bracket syntax — is defined in
`seedance-prompt-25` and is **not redefined here**.

The recipes are **optional creative heuristics** adapted from the Higgsfield
UGC Builder catalog. They are not platform ranking rules, API requirements, or
demonstrated conversion gains. No preset outperforms another by any measured
claim in this bundle.

## Source authority

- [Higgsfield UGC Builder](https://higgsfield.ai/ugc) — the 45 named motion
  presets and their demo behaviors (accessed 2026-09-16). Preset names and
  demo intents are Higgsfield's; every recipe here is an original Seedance 2.5
  direction.
- `seedance-prompt-25` — the prompt grammar and parameter contract these
  recipes fill. Not restated here.

## Preset index

Resolve the user's request to one preset, then read **only its category
section** in [motion-presets.md](references/motion-presets.md):

| Category | Presets |
|---|---|
| Emotion / reaction | Angry Mode, Crying, Happy, Happy Mode, Shocked, Saint Glow, Sunglasses |
| Selfie / posing | Selfie, Selfie Outfit, Selfie Posing, Static Posing, Fix and pose, Group Photo |
| Outfit / fashion | Outfit Check, Outfit Switch, Clothes Rain, Hair Style, Sand Cut |
| Eating / product | Eating, Eating Zoom, Plate Check |
| VFX spectacle | Atomic, Explosion, Firework, Northern Lights, Aquarium, Color Rain, Money Rain, Pizza Fall, Cotton Cloud, Gas Transformation, Beast Appearance, Giant Grab |
| Action / movement | Handheld Run, Pool Jump, Ballet, Motor Ride, Beach Ride, Train Rush, Peak Moment |
| Lifestyle / timelapse | Morning routine, Timelapse Glam, Timelapse Human |
| Multi-shot story | Yacht, BTS |

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

Every recipe in [motion-presets.md](references/motion-presets.md) provides:

| Field | Use |
|---|---|
| `id` | Lowercase kebab-case preset ID |
| Category | One of the eight index categories |
| Grammar | single-pass R2V, structured edit, chained, or one-click |
| References | Role bindings and counts for the user's media |
| Ratio | Default 9:16 unless the request says otherwise |
| Motion block | Timestamped, cue-level action — fills the Action slot |
| Camera block | Named technique — fills the Camera slot |
| Audio | Native audio direction |
| Duration | Integer seconds, 4–30 single-pass |
| Flags | Constraint warnings that must survive into the final prompt |
| Persuasion hint | Optional one-line hook idea; angle/CTA stay with `ugc-ad-modes` |

## Composition rules

- Recipes fill the six-part formula slots; the caller assembles the full
  prompt per `seedance-prompt-25` and owns `prompt-review`, submission, and
  showcase sync.
- Bind the user's character, wardrobe, or product media using the recipe's
  reference roles. A held or worn product visible in frame follows the
  workspace element policy — canonical props get locked references, incidental
  generics may be described.
- Keep every Flag visible in the composed prompt or the pre-submission notes;
  flags encode real provider constraints, not style advice.
- Duration, resolution, ratio, and watermark are generation parameters — they
  stay in the API call, never in the prompt text.
- Acting intensity is expressed through observable physical cues, never degree
  adjectives; compose with `seedance-acting-console` when the emotion needs
  deeper cue work.
- Deeper execution constraints — parameter map, task-type enum, and the four
  flagged presets — live in
  [execution-constraints.md](references/execution-constraints.md).

## Delivery guardrails

Defaults for UGC placement, stated as defaults rather than rules:

- **9:16 vertical** unless the request specifies another ratio.
- **Design for sound-off legibility.** Captions and on-screen text are a
  finishing layer (FFmpeg or HyperFrames) — never baked into generated video.
- **Brand or product visible early** in the first seconds of the cut.
- **AIGC disclosure** applies when delivering AI-generated content as ads
  (TikTok manual tag; Meta auto-labeling). Remind the caller at delivery.
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
5. All recipe flags survive into the output.
6. 9:16 and sound-off defaults are respected or explicitly overridden.
7. Claims, CTA, and testimony requests were routed to `ugc-ad-modes`, not
   answered here.
8. Duration, resolution, ratio, and watermark appear only as generation
   parameters, never in prompt text.
