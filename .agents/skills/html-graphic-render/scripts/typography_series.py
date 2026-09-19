#!/usr/bin/env python3
"""Generate and render a deterministic typography-card series.

Produces one project-local HTML entrypoint per word sharing a single CSS file
and a single copied font, renders each card through render_html.py, and writes
a manifest with hashes. Deterministic: no network, no scripts, no animation.

Example:
    uv run python .agents/skills/html-graphic-render/scripts/typography_series.py \
      --out-dir projects/example/elements/day-text \
      --prefix day --words Monday,Tuesday,Wednesday,Thursday,Friday \
      --width 720 --height 1280 \
      --font-file path/to/PlayfairDisplay-VF.ttf \
      --font-family 'Playfair Display' \
      --font-license path/to/OFL.txt \
      --font-size 112 --position 44
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import struct
import subprocess
import sys
from pathlib import Path

RENDERER = Path(__file__).resolve().parent / "render_html.py"

CSS_TEMPLATE = """@font-face {{
  font-family: '{family}';
  src: url('./fonts/{font_name}') format('{format}');
  font-weight: 100 900;
  font-style: normal;
  font-display: block;
}}
:root {{
  --bg: {background};
  --ink: {text_color};
  --font-size: {font_size}px;
  --letter-spacing: {letter_spacing};
  --position: {position}%;
}}
html, body {{
  margin: 0;
  padding: 0;
  background: transparent;
}}
body {{
  width: {width}px;
  height: {height}px;
  overflow: hidden;
  font-family: '{family}', Didot, 'Bodoni MT', 'Times New Roman', serif;
}}
.card {{
  position: relative;
  width: {width}px;
  height: {height}px;
  background: var(--bg);
}}
.word {{
  position: absolute;
  top: var(--position);
  left: 0;
  right: 0;
  transform: translateY(-50%);
  margin: 0;
  text-align: center;
  color: var(--ink);
  font-size: var(--font-size);
  line-height: 1;
  letter-spacing: var(--letter-spacing);
  white-space: nowrap;
}}
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="./{css_name}">
</head>
<body>
<main class="card">
<p class="word" data-copy-key="word">{word}</p>
</main>
</body>
</html>
"""


def slug(word: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", word.lower()).strip("-")
    if not s:
        raise SystemExit(f"word does not slugify to a filename: {word!r}")
    return s


def font_format(font_file: Path) -> str:
    return {".ttf": "truetype", ".otf": "opentype", ".woff2": "woff2"}.get(font_file.suffix.lower(), "")


def png_dimensions(png: Path) -> tuple[int, int]:
    data = png.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit(f"not a PNG: {png}")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--prefix", required=True)
    p.add_argument("--words", required=True, help="comma-separated series words, e.g. Monday,Tuesday")
    p.add_argument("--width", type=int, required=True)
    p.add_argument("--height", type=int, required=True)
    p.add_argument("--font-file", type=Path, required=True)
    p.add_argument("--font-family", required=True)
    p.add_argument("--font-license", type=Path)
    p.add_argument("--text-color", default="#FFFFFF")
    p.add_argument("--background", default="#101014")
    p.add_argument("--font-size", type=int, required=True,
                   help="one shared size for the whole series; size it against the longest word")
    p.add_argument("--letter-spacing", default="0em")
    p.add_argument("--position", type=float, default=50.0,
                   help="vertical optical center of the word as a percentage of card height")
    p.add_argument("--transparent", action="store_true",
                   help="transparent card background for overlay use")
    p.add_argument("--asset-root", type=Path, help="defaults to --out-dir")
    p.add_argument("--overwrite", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    words = [w.strip() for w in args.words.split(",") if w.strip()]
    if not words:
        raise SystemExit("--words is empty")
    if len({slug(w) for w in words}) != len(words):
        raise SystemExit("words collide after slugification")
    if not args.font_file.is_file():
        raise SystemExit(f"font file not found: {args.font_file}")
    if not font_format(args.font_file):
        raise SystemExit(f"unsupported font type: {args.font_file.suffix}")

    out_dir = args.out_dir
    asset_root = (args.asset_root or out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    fonts_dir = out_dir / "fonts"
    fonts_dir.mkdir(exist_ok=True)
    font_dest = fonts_dir / args.font_file.name
    if not font_dest.exists():
        shutil.copy2(args.font_file, font_dest)
    if args.font_license:
        if not args.font_license.is_file():
            raise SystemExit(f"font license not found: {args.font_license}")
        shutil.copy2(args.font_license, fonts_dir / args.font_license.name)

    css_name = f"{args.prefix}_series.css"
    background = "transparent" if args.transparent else args.background
    css = CSS_TEMPLATE.format(
        family=args.font_family,
        font_name=args.font_file.name,
        format=font_format(args.font_file),
        background=background,
        text_color=args.text_color,
        font_size=args.font_size,
        letter_spacing=args.letter_spacing,
        position=args.position,
        width=args.width,
        height=args.height,
    )
    css_path = out_dir / css_name
    if css_path.exists() and not args.overwrite:
        raise SystemExit(f"refusing to overwrite existing {css_path}; pass --overwrite to repair")
    css_path.write_text(css)

    rows = []
    for word in words:
        stem = f"{args.prefix}_{slug(word)}_v01"
        html_path = out_dir / f"{stem}.html"
        png_path = out_dir / f"{stem}.png"
        html_path.write_text(
            HTML_TEMPLATE.format(css_name=css_name, word=H_escaped(word))
        )
        cmd = [
            sys.executable, str(RENDERER),
            str(html_path), str(png_path),
            "--width", str(args.width),
            "--height", str(args.height),
            "--asset-root", str(asset_root),
            "--require-local-font", args.font_family,
            "--copy", f"word={word}",
        ]
        if args.transparent:
            cmd.append("--transparent")
        result = subprocess.run(cmd, check=False)
        if result.returncode != 0:
            return result.returncode
        if not png_path.exists():
            raise SystemExit(f"renderer reported success but no PNG: {png_path}")
        w, h = png_dimensions(png_path)
        if (w, h) != (args.width, args.height):
            raise SystemExit(f"dimension mismatch for {png_path}: {(w, h)}")
        rows.append((word, stem, w, h, png_path))
        print(f"rendered {png_path.name} ({w}x{h})")

    manifest = out_dir / "manifest.md"
    lines = [
        "---",
        "type: typography-card-series",
        "generation: deterministic_html",
        "source: deterministic_render",
        "renderer: html-graphic-render (scripts/typography_series.py)",
        f"canvas: {args.width}x{args.height}",
        f"font_family: {args.font_family}",
        f"font_file: fonts/{args.font_file.name}",
        f"font_size_px: {args.font_size}",
        f"background: {background}",
        f"text_color: {args.text_color}",
        f"position_pct: {args.position}",
        "status: review",
        "---",
        "",
        f"# {args.prefix} typography series",
        "",
        f"{len(rows)} cards, one shared stylesheet (`{css_name}`) and one shared font.",
        "Same font size and position for every card; only the word differs.",
        "",
        "| Card | File | Dimensions | SHA-256 |",
        "| --- | --- | --- | --- |",
    ]
    for word, stem, w, h, png_path in rows:
        lines.append(f"| {word} | `{stem}.png` | {w}x{h} | {sha256(png_path)} |")
    lines.append("")
    manifest.write_text("\n".join(lines))
    print(f"manifest: {manifest}")
    return 0


def H_escaped(word: str) -> str:
    return word.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


if __name__ == "__main__":
    sys.exit(main())
