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
import html
import json
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
<html{locale}>
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


def output_path(directory: Path, name: str) -> Path:
    path = directory / name
    if path.is_symlink() or not path.resolve().is_relative_to(directory.resolve()):
        raise SystemExit(f"output path escapes the series directory or is a symlink: {path}")
    return path


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
    p.add_argument("--language", help="optional BCP 47 language tag; no language is assumed")
    p.add_argument("--direction", choices=("ltr", "rtl", "auto"),
                   help="optional text direction; auto follows each card's text")
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
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}", args.prefix):
        raise SystemExit("--prefix must be a filename token of at most 64 ASCII characters")
    if args.language is not None and not re.fullmatch(
        r"[A-Za-z]{1,8}(?:-[A-Za-z0-9]{1,8})*", args.language
    ):
        raise SystemExit("--language must be a BCP 47 language tag")
    if not args.font_family.strip():
        raise SystemExit("--font-family must not be empty")
    if not args.font_file.is_file():
        raise SystemExit(f"font file not found: {args.font_file}")
    if not font_format(args.font_file):
        raise SystemExit(f"unsupported font type: {args.font_file.suffix}")

    out_dir = args.out_dir.resolve()
    asset_root = (args.asset_root or out_dir).resolve()
    if not out_dir.is_relative_to(asset_root):
        raise SystemExit("--out-dir must be inside --asset-root")
    fonts_dir = output_path(out_dir, "fonts")
    font_name = f"font-{sha256(args.font_file)}{args.font_file.suffix.lower()}"
    font_dest = output_path(out_dir, f"fonts/{font_name}")
    license_dest = output_path(out_dir, "fonts/LICENSE.txt")
    if args.font_license and not args.font_license.is_file():
        raise SystemExit(f"font license not found: {args.font_license}")
    css_name = f"{args.prefix}_series.css"
    css_path = output_path(out_dir, css_name)
    manifest = output_path(out_dir, "manifest.md")
    stems = [f"{args.prefix}_{index:03d}_v01" for index in range(1, len(words) + 1)]
    targets = [css_path, manifest]
    for stem in stems:
        targets.extend(output_path(out_dir, f"{stem}.{suffix}") for suffix in ("html", "png"))
        targets.append(output_path(out_dir, f"render_{stem}.json"))
    if not args.overwrite:
        for target in targets:
            if target.exists():
                raise SystemExit(f"refusing to overwrite existing {target}; pass --overwrite to repair")
    out_dir.mkdir(parents=True, exist_ok=True)
    fonts_dir.mkdir(exist_ok=True)
    if not font_dest.exists():
        shutil.copy2(args.font_file, font_dest)
    elif sha256(font_dest) != sha256(args.font_file):
        raise SystemExit(f"copied font hash mismatch: {font_dest}")
    if args.font_license and args.font_license.resolve() != license_dest:
        shutil.copy2(args.font_license, license_dest)

    background = "transparent" if args.transparent else args.background
    css = CSS_TEMPLATE.format(
        family="series-font",
        font_name=font_name,
        format=font_format(args.font_file),
        background=background,
        text_color=args.text_color,
        font_size=args.font_size,
        letter_spacing=args.letter_spacing,
        position=args.position,
        width=args.width,
        height=args.height,
    )
    css_path.write_text(css, encoding="utf-8")
    locale = ""
    if args.language is not None:
        locale += f' lang="{html.escape(args.language, quote=True)}"'
    if args.direction is not None:
        locale += f' dir="{args.direction}"'

    rows = []
    for word, stem in zip(words, stems):
        html_path = out_dir / f"{stem}.html"
        png_path = out_dir / f"{stem}.png"
        html_path.write_text(
            HTML_TEMPLATE.format(css_name=css_name, word=H_escaped(word), locale=locale),
            encoding="utf-8",
        )
        cmd = [
            sys.executable, str(RENDERER),
            str(html_path), str(png_path),
            "--width", str(args.width),
            "--height", str(args.height),
            "--asset-root", str(asset_root),
            "--require-local-font", "series-font",
            "--copy", f"word={word}",
        ]
        if args.transparent:
            cmd.append("--transparent")
        if args.overwrite:
            cmd.append("--overwrite")
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

    lines = [
        "---",
        "type: typography-card-series",
        "generation: deterministic_html",
        "source: deterministic_render",
        "renderer: html-graphic-render (scripts/typography_series.py)",
        f"canvas: {args.width}x{args.height}",
        f"font_family: {json.dumps(args.font_family, ensure_ascii=False)}",
        "font_alias: series-font",
        f"font_file: fonts/{font_name}",
        f"language: {json.dumps(args.language)}",
        f"direction: {json.dumps(args.direction)}",
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
        display = html.escape(word).replace("|", "&#124;").replace("\n", "&#10;").replace("\r", "&#13;")
        lines.append(f"| {display} | `{stem}.png` | {w}x{h} | {sha256(png_path)} |")
    lines.append("")
    manifest.write_text("\n".join(lines), encoding="utf-8")
    print(f"manifest: {manifest}")
    return 0


def H_escaped(word: str) -> str:
    return word.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


if __name__ == "__main__":
    sys.exit(main())
