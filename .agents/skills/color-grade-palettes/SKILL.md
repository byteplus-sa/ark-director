---
name: color-grade-palettes
description: Compose palette sentences and post-look graphs. Use for requested grading or delegated art direction, including custom looks. Preserve ungraded conform and source locks. Not physical lighting.
---

# Color Grade Palettes

**Resolve look authority before choosing a palette.** Delegated creative
authorship permits a custom palette or capture-format look proposal without a
named preset. Describe its visible purpose and proposed route; a proposal is
not user approval. Preserve approved palettes and explicit locks under the
existing approval mode. Neutral, muted, monochrome and saturated treatments
are choices, not saturation or intensity quotas.

For technical conform or source-preserving edits, retain original colours,
with no added grade, grain, halation or vignette unless the look is authorized
to change. Explicit ungraded delivery wins over broad creative delegation.
Preserve the untouched master. Golden hour here is a grade, not physical
lighting. This skill composes prompt text and FFmpeg filter graphs only;
it does not call any MCP or API tool and never runs a generation.

For a requested or in-scope proposed look, disclose the route:

| Route | When | Output |
|---|---|---|
| `none` | Preservation/conform without look changes, explicit ungraded delivery, or a creative choice to remain ungraded | No grade sentence; ungraded assembly with the correct colour decode |
| `post` (default for a requested video look) | Footage exists or will be approved first; texture/format looks; one look shared by many clips | FFmpeg post look applied to a copy of the untouched master |
| `prompt` | The user wants the look rendered at generation time, or the target is a Seedream still | Grade sentence in the Seedance Visual Style slot or Seedream `Style:` section |
| `both` | A prompt grade is requested and separate takes must be matched | Grade sentence plus a light FFmpeg matching graph |

The post route is reversible and leaves the approved picture untouched; the
prompt route bakes the look into the take, so a later "use the original
colours" request needs a new generation.

## Correct colour decode (every route)

Seedance 2.5 finals are 10-bit HEVC. Decode them as ordinary **limited-range
BT.709**; a full-range reading lifts blacks and no longer matches the
approved drafts. Tag the output BT.709, keep any look inside a high-bit-depth
chain, and dither once to 8-bit at the end. Apply this chain in the single
final encode (or the Studio render input), not as a lossy per-clip pass; keep
per-clip intermediates lossless. Ungraded conform for that final encode:

```
ffmpeg -i master.mp4 -vf "scale=in_range=limited:out_range=limited:in_color_matrix=bt709:out_color_matrix=bt709:sws_dither=ed,format=yuv420p,setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709" -c:v libx264 -crf 16 -preset slow -c:a copy out.mp4
```

Do **not** use FFmpeg's `vignette` or `eq` filters in a high-bit-depth chain:
both accept only 8-bit input, so FFmpeg silently drops the chain to 8-bit YUV
and hues shift. Use `curves` for contrast, `hue=s=` or `vibrance` for
saturation and `colorbalance` for tint; all three stay at 10-bit or above.

## Source authority

The grammar this skill composes into is defined by the canonical prompt skills
`seedance-prompt-25` and `seedream-prompt`. Official sources, accessed
**2026-08-13**:

- [Seedance 2.5 Prompt Guide (ModelArk)](https://docs.byteplus.com/en/docs/ModelArk/2607689)
- [Seedream 4.0-4.5 Prompt Guide](https://docs.byteplus.com/en/docs/ModelArk/1829186)
- [Seedream 5.0 Pro official blog](https://seed.bytedance.com/en/blog/beyond-generation-it-understands-design-introducing-seedream-5-0-pro)

When the official guides are updated, prefer the live pages over this skill
where they conflict. The base prompt grammar lives in `seedance-prompt-25` and
`seedream-prompt`; compose with the relevant one when composing a full prompt.
The FFmpeg filter behaviour below was checked locally on 10-bit HEVC test
media; the look values are starting points to judge by eye, not calibrated
LUTs.

## Palette bank

Each entry has a **canonical grade sentence** (drop-in, natural inside a
prompt) and a one-line **tonal recipe** describing the intent. The bank is an
optional starting point: adapt it or propose a custom descriptive look for
delegated authorship. Reuse an approved sentence or graph verbatim when its
look is locked. The tonal recipe also guides the post look on the prompt-free
route; it does not limit the available palettes.

**Texture and format looks are post treatments for video.** Grain, halation,
scanlines, tape noise, camcorder or MiniDV texture and vignettes are built in
the edit. Format words in a Seedance prompt do not reliably produce the
format texture; the colour part of such a look may
still go in the prompt when the prompt route is requested. Seedream stills may
carry the full sentence.

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
| VHS / retro | `VHS retro grade: soft blur, chromatic aberration, oversaturated low-fi colors, scanlines, slight flicker, dated tape look` | Degraded 80s videotape nostalgia; for video, a post treatment (see below) |

## Parameter schema

| Parameter | Type | Meaning |
|---|---|---|
| `palette` | optional string | A named palette or custom descriptive proposal, never an invented real film stock. May be derived under delegated authorship; unset after that decision means no grade. |
| `route` | `none` \| `post` \| `prompt` \| `both` | See the route table. Use `none` for ungraded scope; default a video look to `post`, a Seedream look to `prompt`. Disclose proposals before selection. |
| `target_model` | `seedance` \| `seedream` \| `both` | Where a prompt-route sentence lands: Visual Style slot, `Style:` section, or both |
| `reference` | optional string | A style-reference image; the grade is expressed as `use the muted palette, soft grain, diffused highlights of @Image N` |

## Output grammar

The Seedance, Seedream and style-reference sections apply on route `prompt` or
`both`; the post look section applies on route `post` or `both`.

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
Light comes from the shop's warm doorway glow ahead of him and cyan neon signs behind.
Use a medium tracking shot on a 35mm lens following him from the side, then a slow push-in as he reaches the door.
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

### Post look (route `post` or `both`)

Apply the look to a copy of the untouched master, after conform and before
captions, end cards or other overlays (overlay text stays ungraded). Apply the
same graph to every clip that shares the palette. On route `both`, use a much
lighter version of the graph only to match takes to each other, never to
stack a second grade on a baked-in prompt grade.

Wrap every `<LOOK>` in the decode and dither stages:

```
ffmpeg -i master.mp4 -vf "scale=in_range=limited:out_range=limited:in_color_matrix=bt709:out_color_matrix=bt709,format=yuv420p10le,<LOOK>,scale=in_color_matrix=bt709:out_color_matrix=bt709:out_range=limited:sws_dither=ed,format=yuv420p,setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709" -c:v libx264 -crf 16 -preset slow -c:a copy out.mp4
```

For a 10-bit delivery, end the chain with `format=yuv420p10le` and a 10-bit
encoder instead of the 8-bit dither stage.

Teal & Orange Epic:

```
colorbalance=rs=-0.06:gs=0.02:bs=0.06:rh=0.06:gh=0.01:bh=-0.05,curves=all='0/0 0.25/0.22 0.75/0.78 1/1',hue=s=1.1
```

Bleach Bypass (grain only because the look calls for it):

```
curves=all='0/0 0.25/0.17 0.75/0.85 1/1',hue=s=0.55,format=yuv444p16le,noise=alls=8:allf=t
```

Kodak Portra 400:

```
curves=all='0/0.03 0.5/0.5 1/0.97',colorbalance=rs=0.03:bm=-0.03,hue=s=1.02,format=yuv444p16le,noise=alls=5:allf=t
```

The explicit `format=yuv444p16le` before `noise` keeps it at 16-bit
predictably instead of leaving the format to negotiation. Grain strength at 16-bit is a starting value; compare a frame
against the ungraded master at 100 percent. A camcorder or VHS look (downscale
round trip, chroma smear, tape noise, an overlay frame) is built the same way
on the post route; render any on-screen recorder graphics as a separate
overlay layer.

## Edge cases / guardrails

- **Preservation is not open authorship.** Conform/source-preserving work adds
  no look outside authorized changes. Keep original colours, explicit ungraded
  delivery and the correct limited-range BT.709 decode.
- **Resolve actual colour conflicts.** Compatible ingredients or ordered
  per-scene looks may form one coherent treatment. Name their spatial or temporal
  scope; do not apply contradictory instructions to the same region and interval.
- **Preserve approved look scope.** Record the palette, route and exact sentence
  or graph for reuse where locked. Delegated authorship may propose deliberate
  look transitions; do not silently change a project-wide palette lock.
- **B&W needs tonal intent.** Describe the requested contrast and mid-tones.
  Grain, deep blacks and bright whites are options, not requirements for every
  monochrome image; preserve a requested low-contrast or grain-free look.
- **Do not grade twice.** A take with a baked-in prompt grade gets at most a
  light matching graph; a post look is applied to ungraded masters only.
- **Film-stock words belong in `Style:` / visual style**, not in the subject
  line. Put the grade sentence in its slot and keep subject descriptions
  observational.
- **Chained scenes preserve the intended look continuity.** For an unchanged
  look, repeat its exact sentence or graph. For an authorized transition,
  describe the boundary and endpoint; inspect continuity in the actual output.
- **Do not invent film names.** If the palette is not from the bank, write a
  plain descriptive grade (e.g. "cool desaturated blue-gray") instead of
  inventing a brand or stock that does not exist.

## Self-check checklist

1. Look authority is clear: delegated authorship may propose a look; preservation/conform and explicit ungraded delivery add no unauthorized look. Keep the limited-range BT.709 decode.
2. Palette is from the bank, or a plain descriptive grade with no invented film name.
3. Look ingredients and ordered changes are coherent within their scope; no contradictory same-region, same-interval instructions.
4. On the prompt route, the grade sentence is placed in the Visual Style slot (Seedance) or `Style:` section (Seedream), not in the subject or action line.
5. No conflicting color words appear elsewhere in the prompt.
6. B&W tonal intent is explicit; grain and contrast follow the requested look, not a quota.
7. Film-stock keywords appear only in `Style:` / visual style, never in the subject description.
8. Texture or format looks (grain, halation, VHS, camcorder) for video are on the post route, not prompt words.
9. A post look appears only on route `post` or `both`, sits inside the decode-and-dither wrapper, uses no `vignette` or `eq`, and is applied before overlays; on `both` it is labelled matching-only.
10. Chained scenes repeat locked looks verbatim or carry authorized transition boundaries, not accidental palette drift.
