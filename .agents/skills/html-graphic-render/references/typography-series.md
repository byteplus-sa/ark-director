# Typography card series (lettering templates)

Load this reference when the job is a **repeated-card text series** — weekday
labels (Monday–Friday), season names, time-of-day labels, price tiers,
category tags, or any set of cards where every card shares one canvas, one
typeface, one size, one position, and only the word changes.

## When to use this instead of hand-authoring

Hand-authoring N near-identical HTML entrypoints wastes time and drifts. The
series generator replaces that with one command that produces all entrypoints,
the shared stylesheet, the rendered PNGs, and the manifest in a single pass.

Use the generator when: one text element per card, identical layout across
cards, one font. For anything beyond that (logo lockups, images, multi-line
layout), hand-author per the main SKILL.md instead — or hand-author one card
as the design, then hand the remaining words to the generator with the same
tokens.

## Usage

```bash
uv run python .agents/skills/html-graphic-render/scripts/typography_series.py \
  --out-dir projects/example/elements/day-text \
  --prefix day \
  --words Monday,Tuesday,Wednesday,Thursday,Friday \
  --width 720 --height 1280 \
  --font-file projects/example/elements/day-text/fonts/PlayfairDisplay-VF.ttf \
  --font-family 'Playfair Display' \
  --font-size 112 --position 44
```

See `--help` for the exact argument list.

What one run produces inside `--out-dir`:

| Output | Rule |
| --- | --- |
| `<prefix>_<word>_v01.html` | one entrypoint per word, each with a `data-copy-key="word"` exact-copy node |
| `<prefix>_series.css` | one shared stylesheet: `@font-face`, palette tokens, shared size/position |
| `fonts/<font>` (+ license) | font copied once into the series directory; project-local thereafter |
| `<prefix>_<word>_v01.png` | rendered via `render_html.py` with `--require-local-font` and copy verification |
| `render_<prefix>_<word>_v01.json` | the renderer's hash-bound record per card |
| `manifest.md` | provenance block + per-card file/dimensions/SHA-256 table |

## Rules

- **One size, one position, whole series.** Size the font against the longest
  word (for a didone serif at 720px wide, ~112px lands a ~78% ink width for
  `Wednesday`-length words). Do not per-card shrink; the series must read as
  one system.
- **Optical centering** is set once via `--position` (percentage of card
  height for the word's vertical center; choose it by eye on one card). Letterform side bearings may leave 1–3px horizontal variation between
  words — that is font anatomy, not a defect.
- **Word spelling is exact by construction** (`data-copy-key` verification in
  the renderer), which is the entire reason day labels are rendered here
  instead of asked of the video model.
- **Use as a video reference vs overlay.** A dark-background card set works as
  a typography reference handed to the video model. For a true post overlay,
  re-run with `--transparent` into a separate versioned directory — a
  transparent delivery asset and a solid reference card are different assets
  with different alpha intent; never white-matte one into the other.
- **`v01` versioning and overwrite.** The generator always writes `_v01`. For
  changed design tokens, render into a new versioned directory (or a new
  prefix) rather than overwriting reviewed evidence; `--overwrite` is a repair
  tool for a failed render only.
- **Fonts stay project-local.** The generator copies the font and its license
  into the series directory; the renderer's remote/data policy then covers
  them like any other audited asset.
