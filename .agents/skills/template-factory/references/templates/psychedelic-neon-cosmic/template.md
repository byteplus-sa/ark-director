# Template — Psychedelic Neon Cosmic Journey

Reusable style recipe derived from a prior local reference experiment. The
machine contract is version 1.1 and separates locked grammar from replaceable
inputs and adaptation rules.
The local source assets and historical approval are not bundled; inspect and
obtain selection for the current project's references before production use.

## Style

- **Grade:** high-saturation neon, strong chromatic aberration, retro
  vaporwave/synthwave palette, analog film grain + CRT scanlines
- **Lighting:** all emissive neon; self-illuminated subjects; no natural
  directional light; high contrast vs dark starfields
- **Lens:** wide-angle for cosmic/road shots, standard for figure shots, soft
  glow bloom on bright neon
- **Film look:** low-fi retro digital animation, film grain, color shifting,
  analog distortion

## Camera

Static framing for most shots (motion comes from elements + light, not the
camera). Only the rainbow-road shot has a real forward dolly. All transitions
are hard cuts.

## Reusable recipe

Keep the emissive neon style, centered graphic compositions, continuous
element/light motion, hard-cut transitions, and alternation between held
tableaux and fast travel beats. Replace the central subject, product,
environment details, palette, and audio for each run through newly approved
project canon.

- For another duration, preserve the relative held-versus-travel rhythm and
  split at shot boundaries when one clip cannot contain the sequence.
- For another aspect ratio, recompose each centered graphic arrangement for the
  new frame rather than cropping the source layout.
- For another shot count, merge or expand beats while retaining the pattern of
  tableau, transition, travel, and resolved final state.
- For audio, preserve synchronization between the strongest light/color change
  and beat transitions; a silent run marks audio preparation skipped.

## Motion grammar (from the combined per-beat breakdown)

- Floating figure: slow sine bob (~0.5Hz), leaning pose
- Rainbow beams/heads/rings: continuous hue scroll (0.3–2s cycle)
- Palm fronds: out-of-phase slow sway (~0.4Hz)
- Ringed planets: counter-rotating, rings in sync (~3s cycle)
- Car: forward drive via scrolling lane markers + passing streetlights
- Rainbow road: fast first-person dolly, bands scroll toward viewer
- Walkers: outline-only figures, natural walk cycles, glitch distortion
  through light beams
- Global: subtle pulsing chromatic aberration (~1Hz) + soft edge distortion on
  all elements

## Audio

Source has a synthwave score. The reusable audio grammar places accents on
major visual transitions and preserves the opening-to-ending dynamic arc;
the source track, melody, and effects are not template assets. The factory
generates **no audio** by default
(`generate_audio: false`). Set `generate_audio: true` and supply the `audio`
slot to generate native audio.

## Key parameters

| Setting | Value |
|---|---|
| Historical default model | `dreamina-seedance-2-5-260628`; revalidate the live binding before use |
| Resolution | 720p |
| Ratio | 1:1 |
| Duration | sum of shot durations (source ≈ 16s) |
| Storyboard | sketch by default, one panel per source shot, 3 variants, human review |
| watermark | false |

## Reuse contract

The centered graphic composition, continuously moving layers, hard-cut
transitions, and alternating tableau/travel rhythm are locked grammar. The
subject, environments, palette, and optional audio are replaceable inputs. For
new ratios or durations, recompose around the central silhouette and preserve
relative beat rhythm; split long sequences at shot boundaries rather than
compressing all motion into one unsupported clip.
