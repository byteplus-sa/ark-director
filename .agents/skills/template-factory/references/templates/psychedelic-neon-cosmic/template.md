# Template — Psychedelic Neon Cosmic Journey

Optional named style recipe with illustrative synthetic components, not measured
observations or experimental proof. Select it only when the current brief calls
for this neon treatment. [template.json](template.json) is recipe version 1.1
with schema version 1.0 under the [template schema](../../template-schema.json);
it separates locked grammar from replaceable inputs and adaptation rules.
Use only current-brief inputs and explicitly selected canon; inspect and obtain
selection for the current project's references before production use.

## Style

- **Grade:** high-saturation neon, strong chromatic aberration, retro
  vaporwave/synthwave palette, analog film grain + CRT scanlines
- **Lighting:** all emissive neon; self-illuminated subjects; no natural
  directional light; high contrast vs dark starfields
- **Lens:** wide-angle for expansive travel beats, standard for subject tableaux, soft
  glow bloom on bright neon
- **Film look:** low-fi retro digital animation, film grain, color shifting,
  analog distortion

## Camera

Use static framing for held tableaux, with motion from elements and light.
Contrast these with fast travel beats using a forward dolly, parallax, or
scrolling geometry chosen for the current environment. Use hard cuts between
distinct graphic environments.

## Reusable recipe

Keep the emissive neon style, centered graphic compositions, continuous
element/light motion, hard-cut transitions, and alternation between held
tableaux and fast travel beats. Replace the central subject, product,
environment details, palette, and audio for each run through newly approved
project canon.

- For another duration, preserve the relative held-versus-travel rhythm and
  split at shot boundaries when one clip cannot contain the sequence.
- For another aspect ratio, recompose each centered graphic arrangement for the
  new frame rather than cropping a layout designed for another ratio.
- For another shot count, merge or expand beats while retaining the pattern of
  tableau, transition, travel, and resolved final state.
- For audio, preserve synchronization between the strongest light/color change
  and beat transitions; a silent run marks audio preparation skipped.

## Motion grammar (illustrative synthetic components)

These are optional construction examples, not a required object list or shot
sequence. Choose components for the current subject and environment; set motion
speed, cycle length, amplitude, and phase from the approved beat durations and
readability checks, not fixed frequencies.

- Suspended geometric subject: slow vertical oscillation with a readable silhouette
- Emissive contour layers: continuous hue travel within the selected palette
- Peripheral ribbons: slow out-of-phase sway behind a stable central composition
- Nested geometric shells: counter-rotation with coordinated layer phases
- Depth markers: scrolling near and far layers to suggest forward movement
- Abstract passage: fast forward dolly with geometry passing toward frame edges
- Moving silhouettes: subject-appropriate action cycles with optional distortion
  as they cross light fields
- Global treatment: subtle pulsing chromatic aberration and soft edge distortion,
  scaled to preserve subject readability

## Audio

An optional synthetic sound design could use a synthwave pulse with accents on
major visual transitions and a clear opening-to-ending dynamic arc. Choose
genre, instruments, tempo, and cues from the current brief; no soundtrack is
implied. The template defaults to `generate_audio: false`. For a requested
score or ambience, supply the `audio` slot and plan post-production audio;
enable `generate_audio: true` only for requested native audio after verifying
the selected operation's support. Keep a silent run silent.

## Key parameters

| Setting | Value |
|---|---|
| Model | Resolve the current live binding and operation for the brief; the JSON model value is not capability evidence |
| Native Draft | Every new Seedance 2.5 request uses `resolution: "480p"` and boolean `draft: true` in every review mode; resolve capability or transport conflicts without plain-480p fallback. New generations have no skip-draft override |
| Ratio | Current brief's supported ratio; JSON proposes 1:1 when no ratio is selected |
| Duration | Sum of current planned shot durations; fit each request to verified clip limits and assemble as needed |
| Storyboard | Sketch by default, one panel per current beat unless a panel budget is specified, 3 variants unless overridden, QA and selection under the current approval mode |
| watermark | false only when supported and not overridden by the user |

## Reuse contract

The centered graphic composition, continuously moving layers, hard-cut
transitions, and alternating tableau/travel rhythm are locked grammar. The
subject, environments, palette, and optional audio are replaceable inputs. For
new ratios or durations, recompose around the central silhouette and preserve
relative beat rhythm; split long sequences at shot boundaries rather than
compressing all motion into one unsupported clip.
