"""Build a portfolio page (and optional full-episode showreel) from several projects.

Each project contributes its final-master lock from showcase.json. A project
without a final_master lock is shown as in production. With --showreel, the
locked masters are joined back to back with hard cuts and per-project gain to
one loudness target, and a build record is written beside the video.

Usage:
  portfolio.py OUT_DIR PROJECT [PROJECT ...] [--title T] [--showreel]
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frontmatter(project: Path) -> dict[str, Any]:
    path = project / "project.md"
    if not path.is_file():
        return {}
    match = re.match(r"\A---\s*\n(.*?)\n---", path.read_text(), re.DOTALL)
    data = YAML(typ="safe").load(match.group(1)) if match else None
    return data if isinstance(data, dict) else {}


def inside(project: Path, relative: str) -> Path:
    path = (project / relative).resolve()
    if not path.is_relative_to(project.resolve()) or not path.is_file():
        raise ValueError(f"{project.name}: missing or escaping file {relative}")
    return path


def project_entry(project: Path) -> dict[str, Any]:
    meta = frontmatter(project)
    entry: dict[str, Any] = {
        "slug": project.name,
        "title": str(meta.get("title") or project.name),
        "logline": str(meta.get("logline") or ""),
        "canvas": project / "index.html",
        "master": None,
        "subtitles": None,
    }
    showcase = json.loads((project / "showcase.json").read_text())
    stages = {stage["id"]: stage for stage in showcase.get("canvas", {}).get("stages", [])}
    delivery = stages.get("delivery", {})
    lock = (delivery.get("locks") or {}).get("final_master")
    if not lock or lock.get("result") != "approved":
        return entry
    master = inside(project, lock["artifact_path"])
    if sha256(master) != lock["artifact_sha256"]:
        raise ValueError(f"{project.name}: final master changed after its lock")
    entry["master"] = master
    entry["master_sha256"] = lock["artifact_sha256"]
    srts = [s["path"] for s in delivery.get("sources", []) if str(s.get("path", "")).endswith(".srt")]
    stem = master.stem
    srts.sort(key=lambda path: (not Path(path).name.startswith(stem), path))
    if srts:
        entry["subtitles"] = inside(project, srts[0])
    return entry


def duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout)


def integrated_lufs(path: Path) -> float:
    log = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
        capture_output=True, text=True, check=True,
    ).stderr
    values = re.findall(r"I:\s+(-?[\d.]+) LUFS", log)
    if not values:
        raise ValueError(f"no loudness reading for {path}")
    return float(values[-1])


def srt_to_vtt(source: Path, target: Path) -> None:
    text = source.read_text(encoding="utf-8-sig")
    target.write_text("WEBVTT\n\n" + re.sub(r"(\d\d:\d\d:\d\d),(\d\d\d)", r"\1.\2", text), encoding="utf-8")


def build_showreel(entries: list[dict[str, Any]], out: Path, target_lufs: float, limit: float) -> dict[str, Any]:
    masters = [entry["master"] for entry in entries]
    gains = [round(target_lufs - integrated_lufs(path), 2) for path in masters]
    inputs: list[str] = []
    parts: list[str] = []
    labels = ""
    for index, (path, gain) in enumerate(zip(masters, gains)):
        inputs += ["-i", str(path)]
        parts.append(f"[{index}:v]setpts=PTS-STARTPTS,format=yuv420p[v{index}]")
        parts.append(f"[{index}:a]asetpts=PTS-STARTPTS,volume={gain}dB,alimiter=limit={limit}:level=false[a{index}]")
        labels += f"[v{index}][a{index}]"
    parts.append(f"{labels}concat=n={len(masters)}:v=1:a=1[v][a]")
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(parts),
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-profile:v", "high", "-preset", "slow",
         "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
         "-movflags", "+faststart", str(out)],
        check=True,
    )
    starts, cursor = [], 0.0
    for path in masters:
        starts.append(round(cursor, 3))
        cursor += duration(path)
    record = {
        "output": out.name,
        "output_sha256": sha256(out),
        "duration_s": duration(out),
        "target_lufs": target_lufs,
        "limiter_linear": limit,
        "transitions": "hard cuts between complete episodes",
        "inputs": [
            {"project": entry["slug"], "path": str(entry["master"]), "sha256": entry["master_sha256"], "gain_db": gain, "start_s": start}
            for entry, gain, start in zip(entries, gains, starts)
        ],
    }
    out.with_suffix(".json").write_text(json.dumps(record, indent=2) + "\n")
    return record


def page(title: str, subtitle: str, cards: list[str], showreel: str | None) -> str:
    reel = ""
    if showreel:
        reel = (f'<section class="reel"><h2>Showreel</h2><video controls preload="metadata" playsinline>'
                f'<source src="{html.escape(showreel)}" type="video/mp4"></video></section>')
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<style>
:root{{--bg:#f6f2ee;--card:#fff;--ink:#1d1715;--muted:#6d625b;--accent:#9a5b12}}
@media (prefers-color-scheme:dark){{:root{{--bg:#140d0d;--card:#221616;--ink:#f6ece4;--muted:#bba99c;--accent:#e0b35a}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}
header,.reel{{padding:24px 16px 8px;max-width:1500px;margin:auto}}h1{{margin:0;font-size:28px}}header p{{color:var(--muted);margin:6px 0 0}}
.reel video{{width:min(360px,100%);aspect-ratio:9/16;background:#000;border-radius:14px;display:block}}
main{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:20px;padding:20px 16px 48px;max-width:1500px;margin:auto}}
article{{background:var(--card);border-radius:14px;overflow:hidden;display:flex;flex-direction:column}}
article video,.pending{{width:100%;aspect-ratio:9/16;background:#000;display:block}}
.pending{{display:flex;align-items:center;justify-content:center;color:var(--accent);font-weight:600}}
.meta{{padding:14px 16px 18px}}h2{{margin:4px 0 6px;font-size:20px}}.meta p{{margin:0 0 10px;color:var(--muted)}}a{{color:var(--accent)}}
</style></head><body>
<header><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></header>
{reel}
<main>
{chr(10).join(cards)}
</main></body></html>
"""


def build(out_dir: Path, projects: list[Path], title: str, subtitle: str, showreel: bool,
          target_lufs: float, limit: float) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_dir = out_dir.resolve()
    entries = [project_entry(project.resolve()) for project in projects]
    cards = []
    for entry in entries:
        canvas = os.path.relpath(entry["canvas"], out_dir)
        if entry["master"] is None:
            media = '<div class="pending">In production</div>'
        else:
            poster = out_dir / f"poster_{entry['slug']}.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(min(6.0, duration(entry["master"]) / 2)),
                            "-i", str(entry["master"]), "-frames:v", "1", "-vf", "scale=540:-1", str(poster)], check=True)
            track = ""
            if entry["subtitles"] is not None:
                vtt = out_dir / f"{entry['slug']}.en.vtt"
                srt_to_vtt(entry["subtitles"], vtt)
                track = f'<track kind="subtitles" srclang="en" label="English" src="{vtt.name}">'
            source = os.path.relpath(entry["master"], out_dir)
            media = (f'<video controls preload="metadata" playsinline poster="{poster.name}">'
                     f'<source src="{html.escape(source)}" type="video/mp4">{track}</video>')
        logline = f"<p>{html.escape(entry['logline'])}</p>" if entry["logline"] else ""
        cards.append(f'<article>{media}<div class="meta"><h2>{html.escape(entry["title"])}</h2>{logline}'
                     f'<a href="{html.escape(canvas)}">Production canvas &rarr;</a></div></article>')
    reel_record = None
    reel_name = None
    if showreel:
        locked = [entry for entry in entries if entry["master"] is not None]
        if len(locked) != len(entries):
            missing = [entry["slug"] for entry in entries if entry["master"] is None]
            raise ValueError(f"showreel needs a final_master lock for every project; missing: {', '.join(missing)}")
        reel_name = "showreel.mp4"
        reel_record = build_showreel(locked, out_dir / reel_name, target_lufs, limit)
    (out_dir / "index.html").write_text(page(title, subtitle, cards, reel_name), encoding="utf-8")
    manifest = {
        "title": title,
        "projects": [
            {"slug": e["slug"], "title": e["title"], "master": str(e["master"]) if e["master"] else None,
             "master_sha256": e.get("master_sha256")}
            for e in entries
        ],
        "showreel": reel_record,
    }
    (out_dir / "portfolio.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("out_dir")
    parser.add_argument("projects", nargs="+")
    parser.add_argument("--title", default="Portfolio")
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--showreel", action="store_true")
    parser.add_argument("--target-lufs", type=float, default=-16.0)
    parser.add_argument("--limit", type=float, default=0.79, help="limiter ceiling as linear gain (0.79 is about -2 dBFS)")
    args = parser.parse_args(argv)
    try:
        manifest = build(Path(args.out_dir), [Path(p) for p in args.projects], args.title, args.subtitle,
                         args.showreel, args.target_lufs, args.limit)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(json.dumps({"ok": False, "error": str(error)}), file=sys.stderr)
        return 1
    print(json.dumps({"ok": True, **manifest}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
