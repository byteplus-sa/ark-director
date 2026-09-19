---
name: color-grade-palettes
description: >
  Map a named color grade palette or film look into a canonical grade sentence
  for the Seedance 2.5 Visual Style slot or the Seedream Style: section, with
  an optional matching FFmpeg filter graph for cross-shot matching. Use this
  skill for color grading, palette selection, look and grade choices, teal and
  orange, bleach bypass, film looks, LUT-style grades, and cinematic grades.
  The prompt grade is the source of truth; FFmpeg is only for matching in the
  mix step. Golden hour here means the warm grade palette; for golden-hour
  physical lighting (sun position and light), use seedance-lighting-presets.
---

# Color Grade Palettes

This skill turns a named color grade palette or film look into a **canonical
grade sentence** that drops into the **Seedance 2.5 Visual Style slot** of the
six-part formula, or into the **Seedream `Style:` section**. It is
**prompt-composition only** — it does not call any MCP or API tools, and it
never runs a generation. When `post_grade` is requested it also emits a short
**FFmpeg filter graph**, used for cross-shot matching in the mix step only.

> **The prompt grade is the source of truth.** The grade is baked into the
> prompt at generation time. An FFmpeg re-grade is never an alternative to the
> prompt grade — it only matches or refines a baked-in grade so separate takes
> of the same palette line up in the mix.

## Source authority

The grammar this skill composes into is defined by the canonical prompt skills
`seedance-prompt-25` and `seedream-prompt`. Official sources, accessed
**2026-08-13**:

- [Seedance 2.5 Prompt Guide (Lark)](https://bytedance.larkoffice.com/docx/A88jd0B47oAd8zxWp5ycZFMfnxh)
- [Seedance 2.5 Prompt Guide (ModelArk)](https://docs.byteplus.com/en/docs/ModelArk/2607689)
- [Seedream 4.0-4.5 Prompt Guide](https://docs.byteplus.com/en/docs/ModelArk/1829186)
- [Seedream 5.0 Pro official blog](https://seed.bytedance.com/en/blog/beyond-generation-it-understands-design-introducing-seedream-5-0-pro)

When the official guides are updated, prefer the live pages over this skill
where they conflict. The base prompt grammar lives in `seedance-prompt-25` and
`seedream-prompt`; compose with the relevant one when composing a full prompt.

## Palette bank

Each entry has a **canonical grade sentence** (drop-in, natural inside a
prompt) and a one-line **tonal recipe** describing the intent. Use the sentence
verbatim for reproducibility; adjust only the visible specifics (e.g. which
highlights) when the scene requires it.

### Core palettes (9)

| Palette | Canonical grade sentence | Tonal recipe |
|---|---|---|
| Auto | *(no grade sentence — omit the grade, render naturally)* | No forced grade; keep neutral rendering |
| Naturalistic Clean | `naturalistic, clean grade: faithful skin tones, neutral whites, subtle contrast, no visible color cast` | True-to-life, minimal stylization |
| Bleached Warm | `bleached warm grade: lifted hazy highlights, warm amber tint, soft low contrast, creamy shadows` | Faded, sun-soaked memory-film warmth |
| Hyper Neon | `hyper-neon grade: saturated cyan and magenta, glowing neon accents, deep dark shadows, electric color pop` | Aggressive saturated city-pop look |
| Teal & Orange Epic | `teal-and-orange cinematic grade: deep teal shadows, rich orange highlights, warm skin glow` | Blockbuster cool-shadow / warm-skin contrast |
| Sodium Decay | `sodium-decay grade: desaturated deep blues and greens, lonely sodium-vapor orange pools, high contrast, gritty` | Streetlight amber over decayed cool shadows |
| Cold Steel | `cold-steel grade: desaturated cool blue-gray palette, hard neutral highlights, clinical crisp shadows` | Industrial, neutral-cool precision |
| Bleach Bypass | `bleach-bypass look: hard contrast, blown highlights, desaturated silvery sheen` | Crushed blacks, silvered highlights, gritty film |
| Classic B&W | `classic black-and-white grade: deep rich blacks, bright clean whites, pronounced silver mid-tones, fine film grain` | Timeless monochrome with full tonal range |

### Film stocks

| Palette | Canonical grade sentence | Tonal recipe |
|---|---|---|
| Kodak Portra 400 | `Kodak Portra 400 film stock aesthetic: soft warm skin tones, gentle low contrast, creamy smooth highlights, subtle grain` | Soft, warm, flattering analog portrait look |
| Fujifilm Superia 400 | `Fujifilm Superia 400 film stock aesthetic: punchy greens, cool neutral cast, crisp saturated colors, fine grain` | Snappy, slightly cool consumer-film look |
| Ilford HP5 | `Ilford HP5 black-and-white film: deep blacks, rich silver gray mid-tones, strong visible grain, documentary texture` | Gritty monochrome documentary film |
| CineStill 800T | `CineStill 800T tungsten film: warm amber highlights with halation glow, cool blue shadows, halos around bright sources, pronounced grain` | Tungsten motion-picture halation look |

### Common looks

| Palette | Canonical grade sentence | Tonal recipe |
|---|---|---|
| Golden hour | `golden-hour grade: warm low-angle amber light, long soft shadows, rose-gold highlights, gentle orange-tinted shadows` | Sun-kissed warm moment |
| Low-key noir | `low-key noir grade: deep crushed shadows, high contrast, small highlight area, single strong key, moody darkness` | High-contrast, moody darkness |
| High-key soft | `high-key soft grade: bright even exposure, lifted shadows, minimal contrast, soft pastel palette, airy clean whites` | Bright, airy, low-contrast optimism |
| Desaturated / muted | `desaturated muted grade: reduced saturation, softened tones, gentle contrast, understated earthy neutrality` | Subdued, restrained, toned-down realism |
| Morandi | `Morandi palette: muted earthy tones, dusty sage and clay, soft grayed colors, low saturation, calm harmonious neutrals` | Soft muted earth-and-dust harmony |
| VHS / retro | `VHS retro grade: soft blur, chromatic aberration, oversaturated low-fi colors, scanlines, slight flicker, dated tape look` | Degraded 80s videotape nostalgia |

## Parameter schema

| Parameter | Type | Meaning |
|---|---|---|
| `palette` | string (required) | A palette name from the bank, or a plain descriptive grade with no invented film name |
| `target_model` | `seedance` \| `seedream` \| `both` | Where the grade sentence lands: Visual Style slot, `Style:` section, or both |
| `reference` | optional string | A style-reference image; the grade is expressed as `use the muted palette, soft grain, diffused highlights of @Image N` |
| `post_grade` | optional bool | When true, also emit a matching FFmpeg filter graph for the mix step |

## Output grammar

### Seedance — Visual Style slot

The grade sentence is one clause inside the Visual Style part of the six-part
formula:

> **Subject + Action or Event + Scene and Environment (optional) + Visual Style (optional) + Camera Movement/Cut (optional) + Audio (optional)**

Only Subject + Action is required. The grade belongs in the **Visual Style**
slot and nowhere else — never in the subject, action, or scene line.

Worked example, teal-and-orange on a night scene:

```
A detective parks his car beside a rain-soaked city street at night and walks toward the
entrance of a noodle shop, coat collar up.
The visuals feature teal-and-orange cinematic grade: deep teal shadows, rich orange highlights,
warm skin glow, wet asphalt reflections.
Use a medium tracking shot following him from the side, then push in as he reaches the door.
Audio includes rain pattering, distant traffic, and low jazz from inside the shop.
```

### Seedream — `Style:` section

For image generation, the same sentence sits inside the `Style:` line, usually
with the film-stock keyword if one was chosen.

Worked example, Kodak Portra 400 portrait:

```
Task:
Text-to-Image (T2I)

Subject:
A woman in her early 30s, visible pores and subtle freckles across the nose, windswept dark hair,
laughing softly while holding a coffee cup, slightly rumpled linen shirt.

Setting:
A sunlit sidewalk cafe at mid-morning, warm light through a striped awning, softly blurred
pedestrians behind.

Style:
Cinematic, photorealistic, Kodak Portra 400 film stock aesthetic: soft warm skin tones, gentle low
contrast, creamy smooth highlights, subtle grain.

Lighting:
Soft diffused window light from camera-left, gentle warm fill, shallow depth of field.

Composition:
Close-up, eye level, rule of thirds — subject on the right third, background softly blurred.

Constraints:
Quality: 4K, rich textures, natural skin texture
Negative: no plastic skin, no over-smoothing, no watermarks, no text overlays
```

### Style-reference grade

When `reference` is set, bind the image with the reference-role syntax and
translate its look into prompt language:

```
@Image 1 defines the color grade. Use the muted palette, soft grain, and diffused highlights of
@Image 1 in the final visuals.
```

The grade words it contributes still live in the Visual Style slot (Seedance)
or `Style:` section (Seedream).

### Optional FFmpeg filter graph (post_grade)

Emitted only when `post_grade` is true, and **only for cross-shot matching in
the mix step — never re-grade against a baked-in prompt grade**. The prompt
grade is canonical; these graphs nudge separately generated takes of the same
palette to match each other. The FFmpeg filter graphs can be executed with the
`ffmpeg` skill at the caller's discretion in the mix step.

Teal & Orange Epic:

```
ffmpeg -i in.mp4 -vf "colorbalance=rs=.05:bs=.06,eq=contrast=1.06:saturation=1.12,vignette=angle=PI/5" -c:a copy out.mp4
```

Bleach Bypass:

```
ffmpeg -i in.mp4 -vf "curves=all='0/0 0.5/0.62 1/1',eq=saturation=0.55:contrast=1.15,noise=alls=8:allf=t" -c:a copy out.mp4
```

Kodak Portra 400:

```
ffmpeg -i in.mp4 -vf "eq=contrast=0.95:saturation=1.02,colorbalance=rs=.03:bm=-.03,noise=alls=5:allf=t" -c:a copy out.mp4
```

## Edge cases / guardrails

- **Never stack two conflicting grades in one prompt.** One grade direction
  per prompt; a teal-and-orange sentence plus a warm-golden sentence fights the
  model and reads muddy.
- **Enforce one project-wide palette.** The same palette is used in every scene
  of a project for cross-shot consistency. Record it in `project.md` / `scene.md`
  alongside the grade language so later scenes reuse the identical phrase.
- **B&W needs explicit language.** "Black and white" alone is not enough —
  use contrast, silver mid-tones, and grain phrasing (e.g. Classic B&W or
  Ilford HP5) so the result is not flat gray.
- **Prompt grade is the source of truth.** An FFmpeg re-grade is only for
  matching/refinement in the mix step, never a substitute for the prompt grade
  and never applied against a differently graded take.
- **Film-stock words belong in `Style:` / visual style**, not in the subject
  line. Put the grade sentence in its slot and keep subject descriptions
  observational.
- **Watermark false by default.** Set `watermark: false` on all image, video,
  and audio generation unless the user explicitly requests the AIGC watermark.
- **Chained scene sequences repeat the same grade phrase.** When scenes chain
  via `return_last_frame` / `first_frame`, repeat the exact same grade sentence
  in every scene so continuity holds across the chain.
- **Do not invent film names.** If the palette is not from the bank, write a
  plain descriptive grade (e.g. "cool desaturated blue-gray") instead of
  inventing a brand or stock that does not exist.

## Self-check checklist

1. Palette is from the bank, or a plain descriptive grade with no invented film name.
2. Exactly one grade direction is present; no second or conflicting palette words.
3. The grade sentence is placed in the Visual Style slot (Seedance) or `Style:` section (Seedream), not in the subject or action line.
4. No conflicting color words appear elsewhere in the prompt.
5. B&W palettes include explicit contrast / silver / grain language, not just "black and white".
6. Film-stock keywords appear only in `Style:` / visual style, never in the subject description.
7. An FFmpeg filter graph appears only when `post_grade` is requested, and it is labeled as matching-only in the mix step.
8. When grading across a chained scene sequence, the same grade phrase repeats verbatim in every scene.
