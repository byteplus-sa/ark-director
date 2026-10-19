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
| `<prefix>_<ordinal>_v01.html` | one entrypoint per word, using a 1-based ordinal padded to at least three digits |
| `<prefix>_series.css` | one shared stylesheet: `@font-face`, palette tokens, shared size/position |
| `fonts/font-<sha256>.<ext>` (+ `LICENSE.txt`) | font copied under a content-based filename; project-local thereafter |
| `<prefix>_<ordinal>_v01.png` | rendered via `render_html.py` with `--require-local-font series-font` and copy verification |
| `render_<prefix>_<ordinal>_v01.json` | the renderer's hash-bound record per card |
| `manifest.md` | provenance block + per-card file/dimensions/SHA-256 table |

## Rules

- **Display text is not an identifier.** CJK, Arabic, mixed scripts, punctuation
  and duplicate strings are accepted. IDs such as `card_001_v01` follow input
  order and do not transliterate text. Existing CLI flags remain supported;
  consumers of the old word-slug filenames must use the manifest's file column.
  `--words` still splits on commas, trims surrounding whitespace and ignores
  empty entries; embedded commas require hand-authored cards.
- **Language and direction are optional, explicit inputs.** Pass `--language ar
  --direction rtl`, or `--language zh-Hant --direction ltr`, when specified by
  the brief. `--direction auto` lets each card's text determine direction. With
  neither flag, the HTML has neither attribute; no English language is assumed.
- **Font names are metadata.** Unicode family names and filenames are accepted.
  CSS uses the internal `series-font` alias and a hash-based local filename,
  never the supplied name as CSS syntax. Select a licensed font covering the
  requested scripts and inspect glyph coverage and shaping in the raster.
  An output path or font destination escaping the series directory is refused.
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
