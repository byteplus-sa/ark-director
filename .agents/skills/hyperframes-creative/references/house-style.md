# House Style

Creative direction for compositions when no design spec (`frame.md` or `design.md`) is provided. These are starting points — override anything that doesn't serve the content. When a design spec exists, its brand values take precedence; house-style fills gaps.

## Before Writing HTML

1. **Interpret the prompt.** Generate real content. A recipe lists real ingredients. A HUD has real readouts.
2. **Pick a palette.** Light or dark? Declare bg, fg, accent before writing code.
3. **Pick typefaces.** Run the font discovery script in [typography.md](typography.md) — or pick a font you already know that fits the theme. The script broadens your options; it's not the only source.

## Lazy Defaults to Question

These patterns are AI design tells — the first thing every LLM reaches for. If you're about to use one, pause and ask: is this a deliberate choice for THIS content, or am I defaulting?

- Gradient text (`background-clip: text` + gradient)
- Left-edge accent stripes on cards/callouts
- Cyan-on-dark / purple-to-blue gradients / neon accents
- Pure `#000` or `#fff` (tint toward your accent hue instead)
- Identical card grids (same-size cards repeated)
- Everything centered with equal weight (lead the eye somewhere)
- Banned fonts (see [typography.md](typography.md) for full list)

If the content genuinely calls for one of these — centered layout for a solemn closing, cards for a real product UI mockup, a banned font because it's the perfect thematic match — use it. The goal is intentionality, not avoidance.

## Color

- Choose light, dark, monochrome or mixed palettes from the brief and intended audience response, not the industry label.
- A shared palette can provide continuity; multiple accents or planned scene-level changes can provide contrast. Preserve locked brand tokens.
- Tint neutrals when it serves the treatment; neutral gray, pure black and pure white are valid intentional choices.
- **Contrast:** enforced by `hyperframes check` (WCAG AA). Text must be readable with decoratives removed.
- Declare palette up front. Don't invent colors per-element.

## Background Layer

Choose depth and density to serve the concept. A sparse frame, flat field or single subject can carry the whole scene. Layering is optional, not evidence that a composition is finished.

Optional ingredients, with no minimum count:

- Radial glows (accent-tinted, low opacity, breathing scale)
- Ghost text (theme words at 3-8% opacity, very large, slow drift)
- Accent lines (hairline rules, subtle pulse)
- Grain/noise overlay, geometric shapes, grid patterns
- Thematic decoratives (orbit rings for space, vinyl grooves for music, grid lines for data)

Animate decoration only when movement contributes to attention, rhythm or meaning. Stillness and repeated motion can be deliberate; avoid adding loops just to keep the frame busy.

Respect the design spec's distinction between element count and motion count. Neither implies an unrequested minimum of the other.

## Motion

See [motion-principles.md](motion-principles.md) for expressive choices and technical safeguards. Derive pace, easing, repetition and stillness from the brief rather than a fixed entrance recipe.

## Typography

See [typography.md](typography.md) for font options and readability checks. Preserve approved type; choose scale and weight for the actual output size and viewing distance.

## Palettes

Declare the treatment's palette before writing HTML, including any intentional changes across scenes. The banks below are optional examples, not industry assignments or a limit on custom palettes.

| Category          | Use for                                       | File                                                          |
| ----------------- | --------------------------------------------- | ------------------------------------------------------------- |
| Bold / Energetic  | Product launches, social media, announcements | [palettes/bold-energetic.md](../palettes/bold-energetic.md)   |
| Warm / Editorial  | Storytelling, documentaries, case studies     | [palettes/warm-editorial.md](../palettes/warm-editorial.md)   |
| Dark / Premium    | Tech, finance, luxury, cinematic              | [palettes/dark-premium.md](../palettes/dark-premium.md)       |
| Clean / Corporate | Explainers, tutorials, presentations          | [palettes/clean-corporate.md](../palettes/clean-corporate.md) |
| Nature / Earth    | Sustainability, outdoor, organic              | [palettes/nature-earth.md](../palettes/nature-earth.md)       |
| Neon / Electric   | Gaming, tech, nightlife                       | [palettes/neon-electric.md](../palettes/neon-electric.md)     |
| Pastel / Soft     | Fashion, beauty, lifestyle, wellness          | [palettes/pastel-soft.md](../palettes/pastel-soft.md)         |
| Jewel / Rich      | Luxury, events, sophisticated                 | [palettes/jewel-rich.md](../palettes/jewel-rich.md)           |
| Monochrome        | Dramatic, typography-focused                  | [palettes/monochrome.md](../palettes/monochrome.md)           |

Or derive a custom palette from OKLCH, references or the creative premise. A single-hue palette is one option, not a requirement.
