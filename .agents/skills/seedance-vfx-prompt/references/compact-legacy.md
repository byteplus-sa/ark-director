# Compact Legacy

Focused reference for `seedance-vfx-prompt`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Alternative: compact format](#alternative-compact-format)
- [Structure patterns (quick reference)](#structure-patterns-quick-reference)
- [Seedance 2.0 input limits (reference)](#seedance-20-input-limits-reference)

## Alternative: compact format

The heading-based structure above is the primary format. For simpler edits or
when the user wants plain-text output, use this compact format instead.

**Output rules:** Plain text — no bold, no headers, no bullets inside the
prompt, no code blocks. A short label above each prompt (e.g. `Shot_2 · Variant
1 — Through the clouds`) is fine; the prompt body stays plain text.

**Compact declarations:**

```text
@source: Original <clip name> — <who/what is in it: subject, wardrobe, setting, action>. Preserve <identity, face, wardrobe, performance, framing, camera and motion> exactly; <what to change>.
@creature: Reference photo of a real <animal> — <fur / face / anatomy notes>. Appearance and fur/skin texture reference only; ignore the photo's background and lighting, do not use it for the environment.
```

**Compact specs line:**

```text
Photoreal. <aspect, default 16:9>. <duration — match the source clip>s. <look / grade>. NON-IP — generic <creature/design>, not based on any brand or character. <SFX only | SFX and source dialogue only>.
```

- Match the source runtime by default. Extend only when a payoff needs room,
  and say why.
- NON-IP guardrail belongs in the specs line whenever a creature, armor,
  vehicle, or character design is added.
- `SFX only` for added effects; `SFX and source dialogue only` when the source
  talk track must survive.

**Compact skeleton:**

```text
@source: ...
@creature: ...            (only if a texture reference is used)

Photoreal. 16:9. <N>s. <look/grade>. NON-IP — generic <X>. SFX [and source dialogue] only.

<Continuous shot, same framing as source. Preserved performance. The transformation, with physics and plate interaction. Any timed camera move with semantic + numeric anchor. Lock-down clause: face and identity unchanged; everything else identical to the source.>

SFX [and source dialogue] only: <specific, ordered sounds>.
```

## Structure patterns (quick reference)

- **Add-element:** `@source (preserve all, add effect)` → `specs + NON-IP + SFX only` → `continuous shot, preserved performance, effect igniting/creeping with plate interaction, subject unfazed` → `lock-down clause` → `SFX`.
- **Environment-swap:** `@source (preserve subject + vehicle + rig + motion, replace world)` → `specs + grade for the new world` → `continuous shot from the same rig, new world streaming past with parallax, relight to match or relight-all` → `lock-down` → `SFX`.
- **Creature-on-landmark with timed zoom:** `@source` + `@creature (texture ref)` → `specs + NON-IP + SFX and source dialogue only` → `continuous locked shot, giant photoreal creature integrated on the landmark, subject delivering to camera` → `at ~T / on the line "…", smooth push-in keeping the landmark in frame, creature turns to camera` → `lock-down` → `SFX and dialogue`.
- **Prepended reveal intro (transform + outward move + preserved performance):** `@source (preserve subject + performance + lip-sync + framing, add element on landmark, prepend a telephoto intro)` + `@creature (texture ref)` → `specs + NON-IP + SFX and source dialogue only` → `open tight/telephoto on the added element in isolation for the intro beat, hard or smooth zoom-out at ~T landing on a 100% match of the source composition, then the preserved take plays with exact lip-sync to the quoted line while the added element continues behind` → `budget check (intro + remaining = total)` → `lock-down` → `SFX and dialogue`.

## Seedance 2.0 input limits (reference)

Images ≤ 9; videos ≤ 3 items, total ≤ 15s; audio ≤ 3 MP3s, total ≤ 15s; total
mixed inputs ≤ 12; generation duration 4–15s. A source clip plus a
texture-reference photo fits easily. If a request needs more inputs than
allowed, flag it and say what to prioritize.

> **Seedance 2.5 limits**: 2.5 raises these to 30 images / 10 videos / 10
> audios and 30s generation duration. If your request exceeds the 2.0 limits
> above, route to `seedance-prompt-25` and use the 2.5 model
> (`dreamina-seedance-2-5-260628`) with `seedance_2_5_create_task`.
