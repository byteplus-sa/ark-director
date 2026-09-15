---
name: html-graphic-render
description: >-
  Author and render deterministic static graphics from one project-local HTML
  entrypoint with CSS/SVG dependencies into exact-size PNGs with exact typography,
  approved local assets, optional
  transparency, and hash-bound provenance. Use for posters, title or end cards,
  product grids, UI/screens, price and CTA treatments, lower-thirds, and static
  overlays when copy and layout must be exact. Use a hybrid when generated or
  acquired imagery needs deterministic type and composition. Do not use for
  invented photographic or illustrative imagery, semantic image edits,
  animation/video, or production review galleries.
---

# HTML Graphic Render

Create a versioned static graphic from one project-local HTML entrypoint with
local CSS/SVG dependencies and render it to an exact-size PNG. Standalone CSS or
SVG is not an accepted entrypoint. This is a leaf capability: it does not acquire assets,
generate imagery, animate, update the production canvas, or approve a result.

## Route before authoring

| Requirement | Route |
| --- | --- |
| Exact copy, typography, logo, price, CTA, UI, grid, packshot placement, simple vector/gradient geometry | This deterministic route |
| Invented person, location, photograph, illustration, material study, or expressive texture | Generative image route |
| Generated or acquired image with exact copy/layout | Hybrid: select the image first, then finish here |
| Animation, timed overlay, or video composition | Motion/video compositor |
| Gallery, comparison, selection, or lifecycle review | Production canvas |

Do not use a generative model merely to reproduce typography or geometry that
an HTML entrypoint with local CSS/SVG can render exactly. Do not force HTML to
synthesize photographic or illustrative content that benefits from a generative
image model.

## Inputs and source rules

Before rendering, establish:

- one project-contained HTML source and one versioned PNG output;
- exact integer canvas dimensions and intended aspect ratio;
- `opaque` or `transparent` background intent;
- every exact string, represented as plain text inside a unique
  `data-copy-key` element;
- approved local logos, product packshots, imagery, and font files;
- safe areas, reading order, hierarchy, and required product order.

Use a fixed canvas and reset browser defaults. Keep all images, fonts, CSS, and
SVG project-local; inline CSS and inline SVG are allowed, but data URLs and
nested documents are not. Use explicit font families and locally available
fallbacks. Avoid JavaScript, active SVG, temporal media, remote URLs, CSS
animations, transitions, random values, time-dependent content, and responsive
breakpoints that change the requested composition.

When a particular typeface is part of acceptance, provide a project-local web
font and pass its declared family through `--require-local-font 'Family Name'`.
The renderer waits for browser font/image readiness and fails if that family is
not declared, loaded from an audited local font URL, and used by an exact-copy
node. CSS `local()` font sources are rejected under this policy. Platform fonts
are allowed only when the caller accepts platform-specific fallback rendering.
In every case, inspect the actual raster for font fallback and line-wrap drift.

For transparent overlays, author a truly transparent page and render with
`--transparent`. Never use a white matte as a fake alpha channel. A white or
solid-background derivative prepared for a model reference is a separate asset
from the transparent delivery graphic.

For product cutouts, use a true alpha-preserving packshot. Never remove a white
background by global color-keying when that would erase white labels, highlights,
or parts of the product itself.

## Author the composition

Use CSS custom properties for the small set of design tokens that should remain
consistent: canvas size, safe area, palette, type scale, spacing, and radii.
Prefer Grid and Flexbox for explicit alignment. Preserve exact copy as DOM or
SVG text rather than rasterizing it into a generated image.

For an exact-copy node, keep the text plain and un-nested:

```html
<h1 data-copy-key="headline">PICK YOUR POWER</h1>
```

Keep one declared product asset per intended product slot. Use
`object-fit: contain` so the packshot remains whole. Inspect at delivery size
and thumbnail size; a technically correct poster can still fail if the product,
headline, or CTA is obscured or illegible.

## Render

Use the bundled renderer from the repository root:

```bash
uv run python .agents/skills/html-graphic-render/scripts/render_html.py \
  projects/example/elements/end-card/card_end-logo_v01.html \
  projects/example/elements/end-card/card_end-logo_v01.png \
  --asset-root projects/example \
  --width 1080 \
  --height 1920 \
  --require-local-font 'Brand Sans' \
  --copy 'headline=PICK YOUR POWER'
```

Add `--transparent` for an alpha-enabled overlay. The renderer:

- confines source, output, CSS, fonts, and images to `--asset-root`;
- rejects remote/data resources, active or nested documents, scripts, inline
  handlers, active SVG, temporal media, and CSS/SVG animation;
- serves immutable snapshots of hash-audited project files through a loopback
  allowlist, injects a restrictive content-security policy, and rejects
  unaudited requests;
- verifies requested `KEY=TEXT` values against `data-copy-key` nodes without
  case, punctuation, whitespace, or Unicode normalization;
- refuses to overwrite an existing output unless `--overwrite` is explicit;
- refuses any source, input, output, or render-record path collision even with
  `--overwrite`;
- serializes concurrent renders that share an output or record target and
  rejects interleaved target edits before promotion;
- captures a fixed Chrome/Chromium/Edge viewport in sRGB;
- decodes every audited visual asset, waits for font readiness, verifies the
  requested font family and its audited URL when supplied, and checks that no
  browser animation is active;
- verifies the PNG signature, exact raster dimensions, and requested alpha
  channel;
- writes `render_<output-stem>.json` with source/input hashes, exact copy,
  browser version, viewport, input fingerprint, output hash, and byte count.
- validates that record against
  [render-record.schema.json](references/render-record.schema.json) before
  rehashing current inputs and promoting the PNG and JSON through a recoverable
  two-file transaction.

Treat `--overwrite` as a repair tool, not normal versioning. When source or
inputs materially change, create a new `vNN` instead of replacing reviewed
evidence.

## Production metadata

Record deterministic assets as:

```yaml
source: deterministic_render
generation: deterministic_html
renderer: html-graphic-render
render_record: render_card_end-logo_v01.json
selected_variant: null
status: review
```

Do not create a model prompt snapshot or provider task record. Deterministic
graphics skip prompt-review and the default three-sample generative image set.
If the composition includes a generated base image, that upstream asset keeps
its own prompt, review, task, selection, and hash evidence.

## Review gate

Before returning the result, verify:

1. Exact copy, product count/order, logo choice, and CTA match the brief.
2. Fonts visibly loaded; no unintended fallback changed hierarchy or line wrap.
3. No text, product, or logo clips, overlaps, or breaches the safe area.
4. Opaque or transparent behavior matches intent; alpha edges have no white
   matte, halo, or holes in internal product whites.
5. Output dimensions, source/input hashes, and PNG hash match the render record.
6. The design remains readable at thumbnail size and the focal subject is not
   blocked by a central poster panel or oversized copy.
7. The calling production workflow lists the source, raster, provenance, and
   review state on its canvas.

A successful render enters `review`. Only the user can select or approve it.
