from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from validate_request import (
    contained_path,
    parse_frontmatter,
    project_mode_snapshot,
    schema_findings,
)

HYPERFRAMES_VERSION = "0.8.141"
GSAP_URL = "https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"
STUDIO_DIRNAME = "studio"
FRAMES_MARKER = "<!-- hf-studio-frames -->"
DEFAULT_FPS = 24
LENGTH_TOLERANCE_S = 0.25
CHECK_TIMEOUT_S = 900
RENDER_TIMEOUT_S = 7200
PROBE_TIMEOUT_S = 120
MEDIA_SUFFIXES = {".mp4", ".mov", ".webm", ".m4v"}
SHOT_ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")
RESERVED_SHOT_IDS = {"main", "root"}
NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
FILENAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
ASSET_PATTERN = re.compile(r"^(.+)__([0-9a-f]{12})(\.[A-Za-z0-9]+)$")
HYPERFRAMES_ENV = {
    "HYPERFRAMES_SKIP_SKILLS": "1",
    "HYPERFRAMES_NO_UPDATE_CHECK": "1",
    "HYPERFRAMES_NO_TELEMETRY": "1",
    "DO_NOT_TRACK": "1",
}
ENV_ALLOWED_KEYS = {
    "PATH",
    "HOME",
    "USER",
    "LOGNAME",
    "SHELL",
    "TMPDIR",
    "LANG",
    "TERM",
    "TZ",
    "SSL_CERT_FILE",
    "SSL_CERT_DIR",
}
ENV_ALLOWED_PREFIXES = (
    "LC_",
    "NODE_",
    "NPM_",
    "NVM_",
    "XDG_",
    "PRODUCER_",
    "PUPPETEER_",
    "npm_config_",
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "NO_PROXY",
    "ALL_PROXY",
    "http_proxy",
    "https_proxy",
    "no_proxy",
    "all_proxy",
)
STAGES = (
    "brief-development",
    "scene-breakdown",
    "canon-elements",
    "storyboard-visual-plan",
    "audio-preparation",
    "shot-generation",
    "assembly-review",
    "delivery",
)
OPTIONAL_STAGES = {"storyboard-visual-plan", "audio-preparation"}
STAGE_LOCKS = {
    "picture": "assembly-review",
    "audio": "assembly-review",
    "final_master": "delivery",
}
LOCK_FIELDS = (
    "decision_id",
    "decision_sha256",
    "result",
    "artifact_path",
    "artifact_sha256",
    "review_path",
    "review_sha256",
    "actor",
    "reason",
)
FRAME_STAGES = {"shot-generation", "assembly-review", "delivery"}
SELECTION_STAGES = {"assembly-review", "delivery"}
DONE_STATUSES = {"complete", "skipped"}
RENDER_QUALITIES = {"draft", "looks", "standard", "delivery", "high"}
DELIVERY_QUALITIES = {"standard", "delivery", "high"}
BLOCKING_CODES = {
    "asset_missing",
    "asset_modified",
    "unmanaged_asset",
    "take_changed",
    "placed_differs_from_selection",
    "not_on_timeline",
    "frame_missing",
    "no_frame",
}
SELECTION_CODE = "selection_pending"
SAFE_HF_COMMANDS = {
    "preview",
    "lint",
    "snapshot",
    "add",
    "catalog",
    "compositions",
    "info",
    "doctor",
    "keyframes",
    "compare",
}
ATTRIBUTE_PATTERN = re.compile(r"""([A-Za-z][\w-]*)=(?:"([^"]*)"|'([^']*)')""")
HOST_PATTERN = re.compile(r"""<div\b[^>]*\bdata-composition-src=["'][^"']*["'][^>]*>""")
ROOT_PATTERN = re.compile(r"""<div\b[^>]*\bdata-composition-id=["']main["'][^>]*>""")
VIDEO_SRC_PATTERN = re.compile(r"""<video\b[^>]*\bsrc=["']assets/([^"']+)["']""")
BULLET_PATTERN = re.compile(
    r"^\s*[-*]\s*(ratio|aspect|resolution)\s*:\s*[`\"']?([^\s`\"']+)",
    re.MULTILINE | re.IGNORECASE,
)
SHOT_GLOBS = ("scenes/scene-*/*/shot.md", "scenes/*/shot.md")
SECTION_START = re.compile(r"(?m)^(?=## Frame \d+)")

Runner = Callable[..., subprocess.CompletedProcess[str]]
Probe = Callable[[Path], float | None]
SizeProbe = Callable[[Path], tuple[int, int] | None]


class StudioError(ValueError):
    pass


@dataclass(frozen=True)
class Shot:
    shot_id: str
    manifest: str
    directory: str
    title: str
    duration_s: float | None
    aspect: str
    resolution: str
    status: str
    selected_variant: str | None
    active_take: str | None
    recommended_take: str | None
    size_declared: bool
    takes: dict[str, dict[str, Any]]
    narrative: str


@dataclass
class SyncReport:
    added: list[str] = field(default_factory=list)
    preserved: list[str] = field(default_factory=list)
    outlined: list[str] = field(default_factory=list)
    skipped: list[dict[str, str]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class PreparedFrame:
    shot: Shot
    filename: str
    sha: str
    asset: str
    duration: float


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".studio-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o644)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def write_checked(path: Path, value: dict[str, Any], schema: str) -> None:
    findings = schema_findings(value, schema)
    if findings:
        raise StudioError(f"{path.name} failed {schema}: {findings[0].message}")
    atomic_write(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def studio_root(project: Path) -> Path:
    project = project.resolve()
    if (project / "showcase.json").exists():
        raise StudioError(
            "This project has a showcase.json canvas; Studio is for projects without one"
        )
    root = project / STUDIO_DIRNAME
    if root.is_symlink() or (
        root.exists() and not root.resolve().is_relative_to(project)
    ):
        raise StudioError("studio directory must be a real directory in the project")
    return root


def studio_path(project: Path, *parts: str) -> Path:
    root = studio_root(project)
    path = root.joinpath(*parts)
    if not path.resolve().is_relative_to(root.resolve()):
        raise StudioError(f"{'/'.join(parts)} must stay inside the studio directory")
    return path


def dimensions(aspect: str, resolution: str) -> tuple[int, int]:
    match = re.fullmatch(r"(\d+):(\d+)", aspect)
    height_match = re.fullmatch(r"(\d+)p", resolution)
    if not match or not height_match:
        raise StudioError(f"Unsupported aspect or resolution: {aspect} {resolution}")
    ratio_w, ratio_h = int(match[1]), int(match[2])
    short = int(height_match[1])
    if ratio_w >= ratio_h:
        width, height = round(short * ratio_w / ratio_h), short
    else:
        width, height = short, round(short * ratio_h / ratio_w)
    return width + width % 2, height + height % 2


def number(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".")


def shot_narrative(body: str) -> str:
    action = re.search(r"^## Action\s*\n(.+?)(?=^#|\Z)", body, re.MULTILINE | re.DOTALL)
    if action:
        text = action[1]
    else:
        after = re.split(r"^# .+$", body, maxsplit=1, flags=re.MULTILINE)[-1]
        text = after.split("\n## ")[0]
    prose = [
        " ".join(part.split())
        for part in text.split("\n\n")
        if part.strip()
        and not all(
            line.lstrip().startswith(("-", "*", "|"))
            for line in part.splitlines()
            if line.strip()
        )
    ]
    return prose[0][:600] if prose else ""


def read_shot(project: Path, manifest: Path) -> Shot:
    relative = manifest.relative_to(project).as_posix()
    text = read_text(manifest)
    meta = parse_frontmatter(text)
    identifier = meta.get("shot_id") or meta.get("shot") or meta.get("id")
    shot_id = str(identifier or manifest.parent.name)
    if not SHOT_ID_PATTERN.match(shot_id) or shot_id in RESERVED_SHOT_IDS:
        raise StudioError(f"{relative}: invalid or reserved shot id {shot_id!r}")
    body = text.split("---", 2)[-1]
    heading = re.search(r"^# (.+)$", body, re.MULTILINE)
    bullets = {key.lower(): value for key, value in BULLET_PATTERN.findall(body)}
    duration = meta.get("duration_s", meta.get("duration"))
    listed = meta.get("takes")
    takes = {
        str(take["filename"]): take
        for take in (listed if isinstance(listed, list) else [])
        if isinstance(take, dict) and take.get("filename")
    }
    aspect = (
        meta.get("aspect")
        or meta.get("ratio")
        or bullets.get("aspect")
        or bullets.get("ratio")
    )
    resolution = meta.get("resolution") or bullets.get("resolution")
    return Shot(
        shot_id=shot_id,
        manifest=relative,
        directory=manifest.parent.relative_to(project).as_posix(),
        title=str(meta.get("title") or (heading[1].strip() if heading else shot_id)),
        duration_s=float(duration) if isinstance(duration, int | float) else None,
        aspect=str(aspect or "16:9"),
        resolution=str(resolution or "720p"),
        status=str(meta.get("status", "")),
        selected_variant=meta.get("selected_variant") or meta.get("selected_take"),
        active_take=meta.get("active_take"),
        recommended_take=meta.get("recommended_take"),
        size_declared=bool(aspect and resolution),
        takes=takes,
        narrative=shot_narrative(body),
    )


def discover_shots(project: Path) -> list[Shot]:
    project = project.resolve()
    shots: list[Shot] = []
    seen: dict[str, str] = {}
    manifests = sorted(
        {path for pattern in SHOT_GLOBS for path in project.glob(pattern)}
    )
    for manifest in manifests:
        shot = read_shot(project, manifest)
        key = shot.shot_id.lower()
        if key in seen:
            raise StudioError(
                f"Duplicate shot id {shot.shot_id!r} in {seen[key]} and {shot.manifest}"
            )
        seen[key] = shot.manifest
        shots.append(shot)
    return shots


def take_path(shot: Shot, filename: str) -> str:
    if (
        not FILENAME_PATTERN.match(filename)
        or Path(filename).suffix not in MEDIA_SUFFIXES
    ):
        raise StudioError(f"{shot.shot_id}: invalid take filename {filename!r}")
    return f"{shot.directory}/{filename}"


def choose_take(project: Path, shot: Shot, requested: dict[str, str]) -> str | None:
    if shot.shot_id in requested:
        return requested[shot.shot_id]
    if shot.selected_variant:
        return str(shot.selected_variant)
    if shot.active_take:
        matches = [
            name for name in shot.takes if name.endswith(f"_{shot.active_take}.mp4")
        ]
        if len(matches) == 1:
            return matches[0]
    recommended = shot.recommended_take
    if recommended and (project / shot.directory / str(recommended)).is_file():
        return str(recommended)
    return None


def asset_name(sha: str, filename: str) -> str:
    path = Path(filename)
    return f"{path.stem}__{sha[:12]}{path.suffix}"


def split_asset(asset: str) -> tuple[str, str]:
    match = ASSET_PATTERN.match(asset)
    return (match[2], match[1] + match[3]) if match else ("", asset)


def duration_for(shot: Shot, filename: str) -> float:
    entry = shot.takes.get(filename, {})
    value = entry.get("duration_s", shot.duration_s)
    if not isinstance(value, int | float) or value <= 0:
        raise StudioError(f"{shot.shot_id}: no duration recorded for {filename}")
    return float(value)


def probe_duration(path: Path, runner: Runner = subprocess.run) -> float | None:
    try:
        completed = runner(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "json",
                str(path),
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=PROBE_TIMEOUT_S,
        )
        value = float(json.loads(completed.stdout)["format"]["duration"])
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired):
        return None
    return value if completed.returncode == 0 and value > 0 else None


def probe_size(path: Path, runner: Runner = subprocess.run) -> tuple[int, int] | None:
    try:
        completed = runner(
            [
                "ffprobe",
                "-v",
                "error",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream=width,height",
                "-of",
                "json",
                str(path),
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=PROBE_TIMEOUT_S,
        )
        stream = json.loads(completed.stdout)["streams"][0]
        width, height = int(stream["width"]), int(stream["height"])
    except (
        OSError,
        ValueError,
        KeyError,
        IndexError,
        TypeError,
        subprocess.TimeoutExpired,
    ):
        return None
    ok = completed.returncode == 0 and width > 0 and height > 0
    return (width + width % 2, height + height % 2) if ok else None


def root_html(width: int, height: int, fps: int) -> str:
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={width}, height={height}" />
    <script src="{GSAP_URL}"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {width}px; height: {height}px; overflow: hidden; background: #000; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="1" data-fps="{fps}" data-width="{width}" data-height="{height}">
      {FRAMES_MARKER}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""


def frame_html(
    shot_id: str, asset: str, duration: float, track: int, width: int, height: int
) -> str:
    return f"""<!doctype html>
<html>
  <head><meta charset="UTF-8" /></head>
  <body>
    <template>
      <style>
        #root {{ position: absolute; inset: 0; background: #000; }}
        #{shot_id}-video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain; }}
      </style>
      <div id="root" data-composition-id="{shot_id}" data-width="{width}" data-height="{height}">
        <video id="{shot_id}-video" src="assets/{asset}" data-start="0" data-duration="{number(duration)}" data-track-index="{track}" data-has-audio="true" playsinline></video>
      </div>
      <script>
        window.__timelines = window.__timelines || {{}};
        window.__timelines["{shot_id}"] = gsap.timeline({{ paused: true }});
      </script>
    </template>
  </body>
</html>
"""


def host_html(
    shot_id: str, start: float, duration: float, width: int, height: int
) -> str:
    return (
        f'<div id="{shot_id}" data-composition-id="{shot_id}" '
        f'data-composition-src="compositions/{shot_id}.html" data-start="{number(start)}" '
        f'data-duration="{number(duration)}" data-track-index="1" data-track-kind="graphics" '
        f'data-width="{width}" data-height="{height}"></div>'
    )


def attributes(tag: str) -> dict[str, str]:
    return {match[1]: match[2] or match[3] for match in ATTRIBUTE_PATTERN.finditer(tag)}


def host_tags(html: str) -> list[dict[str, str]]:
    return [attributes(tag) for tag in HOST_PATTERN.findall(html)]


def timing(value: str | None, label: str) -> float:
    try:
        result = float(value if value is not None else 0)
    except ValueError:
        result = math.nan
    if not math.isfinite(result):
        raise StudioError(
            f"{label} uses relative or invalid timing {value!r}; set a numeric data-start and data-duration in Studio"
        )
    return result


def timeline_end(html: str) -> float:
    return max(
        (
            timing(tag.get("data-start"), tag.get("id", "a host"))
            + timing(tag.get("data-duration"), tag.get("id", "a host"))
            for tag in host_tags(html)
        ),
        default=0.0,
    )


def hosted_ids(html: str) -> set[str]:
    return {
        tag["data-composition-id"]
        for tag in host_tags(html)
        if "data-composition-id" in tag
    }


def root_duration(html: str) -> float:
    match = ROOT_PATTERN.search(html)
    if not match:
        raise StudioError("index.html has no root composition with id 'main'")
    try:
        return float(attributes(match[0]).get("data-duration", 0))
    except ValueError:
        return 0.0


def with_root_duration(html: str, total: float) -> str:
    match = ROOT_PATTERN.search(html)
    if not match:
        raise StudioError("index.html has no root composition with id 'main'")
    if re.search(r"data-duration=", match[0]):
        tag = re.sub(
            r"""data-duration=(?:"[^"]*"|'[^']*')""",
            f'data-duration="{number(total)}"',
            match[0],
        )
    else:
        tag = match[0][:-1] + f' data-duration="{number(total)}">'
    return html[: match.start()] + tag + html[match.end() :]


def root_dimensions(html: str) -> tuple[int, int] | None:
    match = ROOT_PATTERN.search(html)
    if not match:
        return None
    found = attributes(match[0])
    try:
        return int(found["data-width"]), int(found["data-height"])
    except (KeyError, ValueError):
        return None


def canvas_dimensions(project: Path) -> tuple[int, int]:
    index = studio_path(project, "index.html")
    found = root_dimensions(read_text(index)) if index.is_file() else None
    return found or dimensions("16:9", "720p")


def init_studio(
    project: Path,
    aspect: str = "16:9",
    resolution: str = "720p",
    fps: int = DEFAULT_FPS,
    size: tuple[int, int] | None = None,
) -> Path:
    root = studio_root(project)
    width, height = size or dimensions(aspect, resolution)
    for name in ("assets", "compositions", "renders"):
        directory = studio_path(project, name)
        if directory.is_symlink():
            raise StudioError(f"{name} must be a real directory")
        directory.mkdir(parents=True, exist_ok=True)
    config = root / "hyperframes.json"
    if not config.exists():
        atomic_write(
            config,
            json.dumps(
                {
                    "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
                    "paths": {
                        "blocks": "compositions",
                        "components": "compositions/components",
                        "assets": "assets",
                    },
                    "media": {"autoProxy": True},
                },
                indent=2,
            )
            + "\n",
        )
    index = root / "index.html"
    if not index.exists():
        atomic_write(index, root_html(width, height, fps))
    return root


def placed_asset(project: Path, shot_id: str) -> str | None:
    composition = studio_path(project, "compositions", f"{shot_id}.html")
    if not composition.is_file():
        return None
    match = VIDEO_SRC_PATTERN.search(read_text(composition))
    return match[1] if match else None


def split_storyboard(
    existing: str | None, width: int, height: int
) -> tuple[str, list[str]]:
    if not existing:
        return f"---\nformat: {width}x{height}\n---\n\n# Storyboard\n\n", []
    header, *sections = SECTION_START.split(existing)
    return header, sections


def section_shot(section: str) -> str | None:
    match = re.search(r"^- shot: (\S+)", section, re.MULTILINE)
    return match[1] if match else None


def section_narrative(section: str) -> str:
    lines = section.split("\n")[1:]
    index = 0
    while index < len(lines) and lines[index].startswith("- "):
        index += 1
    return "\n".join(lines[index:]).strip()


def frame_section(
    frame_number: int,
    shot: Shot,
    frame_status: str,
    narrative: str,
    take: tuple[str, str, float] | None = None,
) -> str:
    title = " ".join(shot.title.split())
    lines = [f"## Frame {frame_number} — {shot.shot_id}", f"- status: {frame_status}"]
    if take:
        lines.append(f"- src: compositions/{shot.shot_id}.html")
    duration = take[2] if take else shot.duration_s
    if duration:
        lines.append(f"- duration: {number(duration)}s")
    lines += ["- transition_in: cut", f"- scene: {title}", f"- shot: {shot.shot_id}"]
    if take:
        lines += [f"- take: {take[0]}", f"- sha256: {take[1]}"]
    lines.append(f"- approval: {shot.status or 'review'}")
    return "\n".join(lines) + "\n\n" + (narrative + "\n\n" if narrative else "")


def upsert_frame(
    sections: list[str], shot: Shot, take: tuple[str, str, float] | None = None
) -> bool:
    for index, section in enumerate(sections):
        if section_shot(section) != shot.shot_id:
            continue
        if take is None or "- status: outline" not in section:
            return False
        heading = re.match(r"## Frame (\d+)", section)
        frame_number = int(heading[1]) if heading else index + 1
        sections[index] = frame_section(
            frame_number, shot, "built", section_narrative(section), take
        )
        return True
    sections.append(
        frame_section(
            len(sections) + 1,
            shot,
            "built" if take else "outline",
            shot.narrative,
            take,
        )
    )
    return True


def replace_line(section: str, key: str, value: str) -> str:
    lines = section.split("\n")
    for index, text in enumerate(lines):
        if text.startswith(f"- {key}: "):
            lines[index] = f"- {key}: {value}"
            break
    return "\n".join(lines)


def refresh_section_lines(sections: list[str], shots: list[Shot]) -> bool:
    by_id = {shot.shot_id: shot for shot in shots}
    changed = False
    for index, section in enumerate(sections):
        shot = by_id.get(section_shot(section) or "")
        if shot is None:
            continue
        updated = replace_line(section, "approval", shot.status or "review")
        if updated != section:
            sections[index] = updated
            changed = True
    return changed


def set_section_take(
    sections: list[str], shot_id: str, filename: str, sha: str
) -> None:
    for index, section in enumerate(sections):
        if section_shot(section) == shot_id:
            section = replace_line(section, "take", filename)
            sections[index] = replace_line(section, "sha256", sha)


def read_storyboard(
    project: Path, width: int, height: int
) -> tuple[Path, str, list[str]]:
    path = studio_path(project, "STORYBOARD.md")
    header, sections = split_storyboard(
        read_text(path) if path.exists() else None, width, height
    )
    return path, header, sections


def provenance(project: Path, shots: list[Shot]) -> dict[str, Any]:
    frames = []
    for shot in shots:
        asset = placed_asset(project, shot.shot_id)
        prefix, filename = split_asset(asset or "")
        if asset is None or not prefix:
            continue
        path = studio_path(project, "assets", asset)
        frames.append(
            {
                "shot_id": shot.shot_id,
                "composition": f"compositions/{shot.shot_id}.html",
                "asset": asset,
                "asset_sha256": sha256_file(path) if path.is_file() else prefix,
                "take": filename,
                "manifest": shot.manifest,
                "manifest_sha256": sha256_file(project.resolve() / shot.manifest),
            }
        )
    return {
        "schema_version": 1,
        "hyperframes_version": HYPERFRAMES_VERSION,
        "frames": frames,
    }


def write_provenance(project: Path, shots: list[Shot]) -> None:
    write_checked(
        studio_path(project, "provenance.json"),
        provenance(project, shots),
        "studio-provenance.schema.json",
    )


def prepare_frame(
    project: Path, shot: Shot, filename: str, probe: Probe, report: SyncReport
) -> PreparedFrame:
    source = contained_path(project, take_path(shot, filename))
    sha = sha256_file(source)
    asset = asset_name(sha, filename)
    target = studio_path(project, "assets", asset)
    if not target.exists():
        shutil.copy2(source, target)
    measured = probe(source)
    try:
        declared: float | None = duration_for(shot, filename)
    except StudioError:
        declared = None
    if measured is None and declared is None:
        raise StudioError(
            f"{shot.shot_id}: no duration recorded for {filename} and ffprobe could not measure it"
        )
    duration = measured if measured is not None else float(declared or 0)
    if (
        measured is not None
        and declared is not None
        and abs(measured - declared) > LENGTH_TOLERANCE_S
    ):
        report.warnings.append(
            f"{shot.shot_id}: {filename} is {number(measured)}s but the manifest says "
            f"{number(declared)}s; the frame uses the measured length"
        )
    return PreparedFrame(shot, filename, sha, asset, duration)


def frame_state(project: Path, shot: Shot, hosted: set[str]) -> str:
    has_composition = studio_path(
        project, "compositions", f"{shot.shot_id}.html"
    ).exists()
    on_timeline = shot.shot_id in hosted
    if has_composition and on_timeline:
        return "placed"
    if has_composition:
        return "not_on_timeline"
    return "frame_missing" if on_timeline else "absent"


def canvas_size(
    project: Path,
    shots: list[Shot],
    requested: dict[str, str],
    size_probe: SizeProbe,
) -> tuple[int, int]:
    for shot in shots:
        if shot.size_declared:
            return dimensions(shot.aspect, shot.resolution)
    for shot in shots:
        name = choose_take(project, shot, requested)
        if name is None:
            continue
        measured = size_probe(contained_path(project, take_path(shot, name)))
        if measured:
            return measured
    return dimensions(shots[0].aspect, shots[0].resolution)


def sync(
    project: Path,
    requested: dict[str, str] | None = None,
    probe: Probe = probe_duration,
    size_probe: SizeProbe = probe_size,
) -> SyncReport:
    project = project.resolve()
    requested = requested or {}
    shots = discover_shots(project)
    if not shots:
        raise StudioError(
            "No shot manifests found under scenes/scene-*/*/shot.md or scenes/*/shot.md"
        )
    unknown = sorted(set(requested) - {shot.shot_id for shot in shots})
    if unknown:
        raise StudioError(f"--take names unknown shots: {', '.join(unknown)}")
    first = shots[0]
    size = (
        None
        if studio_path(project, "index.html").exists()
        else canvas_size(project, shots, requested, size_probe)
    )
    init_studio(project, first.aspect, first.resolution, size=size)
    index_path = studio_path(project, "index.html")
    html = read_text(index_path)
    width, height = root_dimensions(html) or dimensions(first.aspect, first.resolution)
    if FRAMES_MARKER not in html:
        raise StudioError(
            f"index.html lost the {FRAMES_MARKER} marker; add it back inside the root composition"
        )
    storyboard_path, header, sections = read_storyboard(project, width, height)
    report = SyncReport()
    for shot in shots:
        declared = shot.size_declared
        if declared and dimensions(shot.aspect, shot.resolution) != (width, height):
            report.warnings.append(
                f"{shot.shot_id}: {shot.aspect} {shot.resolution} differs from the project canvas {width}x{height}"
            )
    hosted = hosted_ids(html)
    pending: list[PreparedFrame] = []
    storyboard_changed = refresh_section_lines(sections, shots)
    for shot in shots:
        state = frame_state(project, shot, hosted)
        if state != "absent":
            report.preserved.append(shot.shot_id)
            if shot.shot_id in requested:
                report.warnings.append(
                    f"{shot.shot_id}: --take ignored; the frame already exists (use place)"
                )
            if state != "placed":
                report.warnings.append(
                    f"{shot.shot_id}: {state}; fix it in Studio or remove the leftover"
                )
            continue
        filename = choose_take(project, shot, requested)
        if filename is None:
            report.skipped.append(
                {"shot_id": shot.shot_id, "reason": "no selected or active take"}
            )
            if upsert_frame(sections, shot):
                report.outlined.append(shot.shot_id)
                storyboard_changed = True
            continue
        pending.append(prepare_frame(project, shot, filename, probe, report))
    cursor = timeline_end(html)
    for ordinal, frame in enumerate(pending):
        atomic_write(
            studio_path(project, "compositions", f"{frame.shot.shot_id}.html"),
            frame_html(
                frame.shot.shot_id,
                frame.asset,
                frame.duration,
                len(hosted) + ordinal,
                width,
                height,
            ),
        )
        html = html.replace(
            FRAMES_MARKER,
            host_html(frame.shot.shot_id, cursor, frame.duration, width, height)
            + "\n      "
            + FRAMES_MARKER,
        )
        cursor += frame.duration
        upsert_frame(sections, frame.shot, (frame.filename, frame.sha, frame.duration))
        storyboard_changed = True
        report.added.append(frame.shot.shot_id)
    if storyboard_changed:
        atomic_write(storyboard_path, header + "".join(sections))
    if pending:
        atomic_write(
            index_path, with_root_duration(html, max(root_duration(html), cursor))
        )
    write_provenance(project, shots)
    return report


def issue(shot_id: str, code: str, detail: str) -> dict[str, str]:
    return {"shot_id": shot_id, "code": code, "detail": detail}


def frame_issues(project: Path, shot: Shot, asset: str) -> list[dict[str, str]]:
    prefix, filename = split_asset(asset)
    if not prefix:
        return [
            issue(
                shot.shot_id,
                "unmanaged_asset",
                f"{asset} was not placed by studio_project",
            )
        ]
    path = studio_path(project, "assets", asset)
    if not path.is_file():
        return [issue(shot.shot_id, "asset_missing", asset)]
    found = []
    if not sha256_file(path).startswith(prefix):
        found.append(issue(shot.shot_id, "asset_modified", asset))
    source = project / shot.directory / filename
    if source.is_file() and not sha256_file(source).startswith(prefix):
        found.append(
            issue(
                shot.shot_id, "take_changed", f"{filename} changed after it was copied"
            )
        )
    if shot.selected_variant and shot.selected_variant != filename:
        found.append(
            issue(
                shot.shot_id,
                "placed_differs_from_selection",
                f"placed {filename}, manifest selects {shot.selected_variant}",
            )
        )
    elif not shot.selected_variant:
        found.append(
            issue(
                shot.shot_id, SELECTION_CODE, f"{filename} is placed but not selected"
            )
        )
    return found


def status(project: Path) -> dict[str, Any]:
    project = project.resolve()
    root = studio_root(project)
    shots = discover_shots(project)
    index = root / "index.html"
    hosted = hosted_ids(read_text(index)) if index.is_file() else set()
    issues: list[dict[str, str]] = []
    frames = []
    for shot in shots:
        state = frame_state(project, shot, hosted)
        if state == "absent":
            if shot.selected_variant or shot.active_take:
                issues.append(
                    issue(
                        shot.shot_id, "no_frame", "shot has a take but no Studio frame"
                    )
                )
            continue
        if state != "placed":
            issues.append(
                issue(shot.shot_id, state, "the frame and the timeline host disagree")
            )
        asset = placed_asset(project, shot.shot_id)
        if asset is None:
            continue
        _, filename = split_asset(asset)
        frames.append(
            {
                "shot_id": shot.shot_id,
                "asset": asset,
                "take": filename,
                "selected_variant": shot.selected_variant,
                "on_timeline": state == "placed",
            }
        )
        issues += frame_issues(project, shot, asset)
    compositions = studio_path(project, "compositions")
    known = {shot.shot_id for shot in shots}
    for composition in (
        sorted(compositions.glob("*.html")) if compositions.is_dir() else []
    ):
        if composition.stem not in known:
            issues.append(
                issue(
                    composition.stem,
                    "orphan_frame",
                    "extra composition without a shot manifest (not a shot frame)",
                )
            )
    blocking = [item for item in issues if item["code"] in BLOCKING_CODES]
    return {"ok": not blocking, "frames": frames, "issues": issues}


def blocking_issues(
    result: dict[str, Any], include_selection: bool
) -> list[dict[str, str]]:
    codes = BLOCKING_CODES | ({SELECTION_CODE} if include_selection else set())
    return [item for item in result["issues"] if item["code"] in codes]


def copy_take(project: Path, shot: Shot, filename: str) -> tuple[str, str]:
    source = contained_path(project, take_path(shot, filename))
    sha = sha256_file(source)
    asset = asset_name(sha, filename)
    target = studio_path(project, "assets", asset)
    if not target.exists():
        shutil.copy2(source, target)
    return asset, sha


def find_shot(project: Path, shot_id: str) -> Shot:
    for shot in discover_shots(project):
        if shot.shot_id == shot_id:
            return shot
    raise StudioError(f"Unknown shot {shot_id}")


def candidates(project: Path, shot_id: str) -> dict[str, Any]:
    project = project.resolve()
    shot = find_shot(project, shot_id)
    init_studio(project, shot.aspect, shot.resolution)
    names = sorted(
        path.name
        for path in (project / shot.directory).iterdir()
        if path.suffix in MEDIA_SUFFIXES and FILENAME_PATTERN.match(path.name)
    )
    assets: list[str] = []
    skipped: list[dict[str, str]] = []
    for name in names:
        try:
            assets.append(copy_take(project, shot, name)[0])
        except (StudioError, ValueError, OSError) as error:
            skipped.append({"filename": name, "reason": str(error)})
    return {"assets": assets, "skipped": skipped}


def place_take(
    project: Path, shot_id: str, filename: str, probe: Probe = probe_duration
) -> dict[str, str]:
    project = project.resolve()
    shot = find_shot(project, shot_id)
    current = placed_asset(project, shot_id)
    if current is None:
        raise StudioError(f"{shot_id} has no frame yet; run sync first")
    composition = studio_path(project, "compositions", f"{shot_id}.html")
    text = read_text(composition)
    clip = re.search(r"""<video\b[^>]*\bdata-duration=["']([^"']+)["']""", text)
    measured = probe(contained_path(project, take_path(shot, filename)))
    if measured is None:
        measured = duration_for(shot, filename)
    if clip and abs(measured - timing(clip[1], shot_id)) > LENGTH_TOLERANCE_S:
        raise StudioError(
            f"{filename} is {number(measured)}s but the frame clip is {clip[1]}s; retime it in Studio instead"
        )
    asset, sha = copy_take(project, shot, filename)
    atomic_write(composition, text.replace(f"assets/{current}", f"assets/{asset}", 1))
    storyboard_path, header, sections = read_storyboard(
        project, *canvas_dimensions(project)
    )
    set_section_take(sections, shot_id, filename, sha)
    atomic_write(storyboard_path, header + "".join(sections))
    write_provenance(project, discover_shots(project))
    return {"shot_id": shot_id, "placed": filename, "asset": asset}


def hyperframes_argv(*arguments: str) -> list[str]:
    return ["npx", "--yes", f"hyperframes@{HYPERFRAMES_VERSION}", *arguments]


def hyperframes_environment() -> dict[str, str]:
    inherited = {
        key: value
        for key, value in os.environ.items()
        if key in ENV_ALLOWED_KEYS or key.startswith(ENV_ALLOWED_PREFIXES)
    }
    return {**inherited, **HYPERFRAMES_ENV}


def run_hyperframes(
    project: Path,
    arguments: list[str],
    runner: Runner = subprocess.run,
    timeout: int = CHECK_TIMEOUT_S,
) -> subprocess.CompletedProcess[str]:
    root = studio_root(project)
    if not (root / "index.html").is_file():
        raise StudioError("No Studio project; run studio_project.py sync first")
    try:
        return runner(
            hyperframes_argv(arguments[0], str(root), *arguments[1:]),
            capture_output=True,
            text=True,
            env=hyperframes_environment(),
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        raise StudioError(
            f"hyperframes {arguments[0]} timed out after {timeout}s"
        ) from None


def hf_command(
    project: Path,
    arguments: list[str],
    runner: Runner = subprocess.run,
    timeout: int = CHECK_TIMEOUT_S,
) -> subprocess.CompletedProcess[str]:
    if not arguments or arguments[0] not in SAFE_HF_COMMANDS:
        raise StudioError(f"hf runs only {sorted(SAFE_HF_COMMANDS)}")
    root = studio_root(project)
    if not (root / "index.html").is_file():
        raise StudioError("No Studio project; run studio_project.py sync first")
    try:
        return runner(
            hyperframes_argv(*arguments),
            capture_output=True,
            text=True,
            env=hyperframes_environment(),
            cwd=root,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        raise StudioError(
            f"hyperframes {arguments[0]} timed out after {timeout}s"
        ) from None


def check_passed(completed: subprocess.CompletedProcess[str]) -> bool:
    if completed.returncode != 0:
        return False
    try:
        report = json.loads(completed.stdout)
    except (ValueError, TypeError):
        return False
    return report.get("ok") is True and report.get("browserSkipped") is False


def probe_media(path: Path, runner: Runner = subprocess.run) -> dict[str, Any]:
    try:
        completed = runner(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_format",
                "-show_streams",
                "-of",
                "json",
                str(path),
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=PROBE_TIMEOUT_S,
        )
    except subprocess.TimeoutExpired:
        raise StudioError("ffprobe timed out") from None
    if completed.returncode != 0:
        raise StudioError(f"ffprobe failed: {completed.stderr.strip()[:200]}")
    data = json.loads(completed.stdout)
    keys = (
        "codec_type",
        "codec_name",
        "width",
        "height",
        "pix_fmt",
        "r_frame_rate",
        "color_range",
        "color_space",
        "sample_rate",
        "channels",
    )
    return {
        "duration_s": float(data["format"]["duration"]),
        "streams": [
            {key: stream[key] for key in keys if key in stream}
            for stream in data["streams"]
        ],
    }


def tree_digest(project: Path) -> str:
    root = studio_root(project)
    files = [root / "index.html", root / "hyperframes.json"]
    for name in ("compositions", "assets"):
        directory = studio_path(project, name)
        if directory.is_dir():
            files += sorted(path for path in directory.rglob("*") if path.is_file())
    digest = hashlib.sha256()
    for path in files:
        digest.update(
            f"{path.relative_to(root).as_posix()}\0{sha256_file(path)}\n".encode()
        )
    return digest.hexdigest()


def record_render(
    project: Path,
    render_file: Path,
    arguments: list[str],
    runner: Runner = subprocess.run,
    produced_by: str = "manual",
    inputs_digest: str | None = None,
) -> Path:
    project = project.resolve()
    renders = studio_path(project, "renders").resolve()
    output = render_file.resolve()
    if not output.is_file() or not output.is_relative_to(renders):
        raise StudioError("Render must be an existing file inside studio/renders")
    record = {
        "schema_version": 1,
        "produced_by": produced_by,
        "created_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "output": {
            "path": output.relative_to(project).as_posix(),
            "sha256": sha256_file(output),
            "bytes": output.stat().st_size,
            "probe": probe_media(output, runner),
        },
        "hyperframes": {"version": HYPERFRAMES_VERSION, "arguments": arguments},
        "inputs": {
            "index_sha256": sha256_file(studio_path(project, "index.html")),
            "config_sha256": sha256_file(studio_path(project, "hyperframes.json")),
            "studio_sha256": inputs_digest or tree_digest(project),
        },
        "frames": provenance(project, discover_shots(project))["frames"],
    }
    sidecar = output.with_name(output.name + ".render.json")
    write_checked(sidecar, record, "studio-render-record.schema.json")
    return sidecar


def render(
    project: Path,
    name: str = "final",
    quality: str = "delivery",
    runner: Runner = subprocess.run,
) -> Path:
    project = project.resolve()
    if not NAME_PATTERN.match(name):
        raise StudioError(f"Invalid render name {name!r}")
    if quality not in RENDER_QUALITIES:
        raise StudioError(f"Quality must be one of {sorted(RENDER_QUALITIES)}")
    if quality in DELIVERY_QUALITIES:
        blocking = blocking_issues(status(project), include_selection=True)
        if blocking:
            raise StudioError(
                f"{quality} renders need a clean status; first issue: "
                f"{blocking[0]['shot_id']} {blocking[0]['code']}"
            )
    output = studio_path(project, "renders", f"{name}.mp4")
    if output.exists():
        raise StudioError(
            f"{output.name} already exists; choose a new --name instead of overwriting"
        )
    before = tree_digest(project)
    try:
        completed = run_hyperframes(
            project,
            ["render", "--quality", quality, "--output", str(output)],
            runner,
            RENDER_TIMEOUT_S,
        )
        if completed.returncode != 0 or not output.is_file():
            detail = (completed.stderr or completed.stdout)[-400:].strip()
            raise StudioError(f"hyperframes render failed: {detail}")
        if tree_digest(project) != before:
            raise StudioError(
                "the Studio project changed during the render; render again"
            )
        return record_render(
            project, output, ["render", "--quality", quality], runner, "render", before
        )
    except BaseException:
        output.unlink(missing_ok=True)
        raise


def default_stages() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "current_stage": STAGES[0],
        "stages": [{"id": stage, "status": "pending"} for stage in STAGES],
    }


def read_stages(project: Path) -> dict[str, Any]:
    path = studio_path(project, "stages.json")
    if not path.is_file():
        return default_stages()
    value = json.loads(read_text(path))
    findings = schema_findings(value, "studio-stages.schema.json")
    if (
        findings
        or [item["id"] for item in value["stages"]] != list(STAGES)
        or value["current_stage"] not in STAGES
    ):
        raise StudioError("stages.json is invalid; do not edit it by hand")
    return value  # type: ignore[no-any-return]


def write_stages(project: Path, value: dict[str, Any]) -> None:
    root = studio_root(project)
    root.mkdir(parents=True, exist_ok=True)
    write_checked(root / "stages.json", value, "studio-stages.schema.json")


def stage_entry(value: dict[str, Any], stage_id: str) -> dict[str, Any]:
    if stage_id not in STAGES:
        raise StudioError(f"Unknown stage {stage_id!r}; expected one of {list(STAGES)}")
    return next(item for item in value["stages"] if item["id"] == stage_id)


def require_earlier_done(value: dict[str, Any], stage_id: str, action: str) -> None:
    for earlier in STAGES[: STAGES.index(stage_id)]:
        if stage_entry(value, earlier)["status"] not in DONE_STATUSES:
            raise StudioError(f"Complete {earlier} before {action} {stage_id}")


def advance(value: dict[str, Any], stage_id: str) -> None:
    following = STAGES.index(stage_id) + 1
    if following < len(STAGES) and following > STAGES.index(value["current_stage"]):
        value["current_stage"] = STAGES[following]


def start_stage(project: Path, stage_id: str) -> dict[str, Any]:
    value = read_stages(project)
    entry = stage_entry(value, stage_id)
    require_earlier_done(value, stage_id, "starting")
    if entry["status"] in DONE_STATUSES:
        raise StudioError(f"{stage_id} is already {entry['status']}")
    entry["status"] = "review"
    value["current_stage"] = stage_id
    write_stages(project, value)
    return value


def skip_stage(project: Path, stage_id: str, reason: str) -> dict[str, Any]:
    value = read_stages(project)
    entry = stage_entry(value, stage_id)
    if stage_id not in OPTIONAL_STAGES:
        raise StudioError(f"Only {sorted(OPTIONAL_STAGES)} can be skipped")
    if not reason.strip():
        raise StudioError("Skipping a stage needs a reason")
    require_earlier_done(value, stage_id, "skipping")
    if entry["status"] == "complete":
        raise StudioError(f"{stage_id} is already complete")
    entry.update(
        status="skipped",
        reason=reason.strip(),
        completed_at=datetime.now(UTC).isoformat(timespec="seconds"),
    )
    entry.pop("evidence", None)
    advance(value, stage_id)
    write_stages(project, value)
    return value


def reopen_stage(project: Path, stage_id: str) -> dict[str, Any]:
    value = read_stages(project)
    stage_entry(value, stage_id)
    for item in value["stages"][STAGES.index(stage_id) :]:
        item.pop("locks", None)
        if item["status"] == "complete":
            item["status"] = "review"
            item.pop("completed_at", None)
            item.pop("evidence", None)
    value["current_stage"] = stage_id
    write_stages(project, value)
    return value


def read_render_records(project: Path) -> list[tuple[Path, dict[str, Any]]]:
    records = []
    for path in sorted(studio_path(project, "renders").glob("*.render.json")):
        try:
            record = json.loads(read_text(path))
        except (OSError, ValueError):
            continue
        valid = isinstance(record, dict) and not schema_findings(
            record, "studio-render-record.schema.json"
        )
        if valid:
            records.append((path, record))
    return records


def render_quality(arguments: list[str]) -> str:
    if "--quality" not in arguments:
        return ""
    position = arguments.index("--quality") + 1
    return arguments[position] if position < len(arguments) else ""


def delivery_failures(project: Path, shots: list[Shot]) -> tuple[list[str], str | None]:
    candidates_ = [
        (path, record)
        for path, record in read_render_records(project)
        if record["produced_by"] == "render"
        and render_quality(record["hyperframes"]["arguments"]) in DELIVERY_QUALITIES
    ]
    if not candidates_:
        return [
            "no render made by studio_project.py render at standard or higher quality; run studio_project.py render"
        ], None
    path, record = max(
        candidates_, key=lambda item: (item[1]["created_at"], item[0].name)
    )
    name = path.name
    failures = []
    output = project / record["output"]["path"]
    if not output.is_file() or sha256_file(output) != record["output"]["sha256"]:
        failures.append(f"{name} no longer matches its recorded file")
    if record["inputs"]["studio_sha256"] != tree_digest(project):
        failures.append(
            f"the Studio project changed after {name} was rendered; render again"
        )
    rendered = {(frame["shot_id"], frame["asset_sha256"]) for frame in record["frames"]}
    current = {
        (frame["shot_id"], frame["asset_sha256"])
        for frame in provenance(project, shots)["frames"]
    }
    if rendered != current:
        failures.append(f"{name} does not match the placed takes; render again")
    return failures, path.relative_to(project).as_posix()


def required_locks(ledger: dict[str, Any], stage_id: str) -> list[str]:
    if stage_id == "assembly-review":
        audio = stage_entry(ledger, "audio-preparation")["status"] != "skipped"
        return ["picture", "audio"] if audio else ["picture"]
    return ["final_master"] if stage_id == "delivery" else []


def lock_failures(
    project: Path, ledger: dict[str, Any], stage_id: str, delivery_record: str | None
) -> list[str]:
    locks = stage_entry(ledger, stage_id).get("locks", {})
    failures = []
    for kind in required_locks(ledger, stage_id):
        lock = locks.get(kind)
        if lock is None:
            failures.append(f"{kind} lock is required before stage exit")
            continue
        for key, relative in (
            ("artifact_sha256", lock["artifact_path"]),
            ("review_sha256", lock["review_path"]),
            ("decision_sha256", f"decisions/{lock['decision_id']}.json"),
        ):
            path = project / relative
            if not path.is_file() or sha256_file(path) != lock[key]:
                failures.append(f"{kind} lock is stale: {relative} changed")
        if kind == "final_master" and delivery_record:
            record = json.loads(read_text(project / delivery_record))
            if lock["artifact_path"] != record["output"]["path"]:
                failures.append("the final master lock is not for the delivery render")
    return failures


def stage_gate(
    project: Path,
    stage_id: str,
    runner: Runner = subprocess.run,
    ledger: dict[str, Any] | None = None,
) -> tuple[list[str], dict[str, Any]]:
    project = project.resolve()
    ledger = ledger or read_stages(project)
    failures: list[str] = []
    evidence: dict[str, Any] = {
        "status_ok": True,
        "check_ran": False,
        "check_ok": False,
        "provenance_sha256": None,
        "index_sha256": None,
    }
    if stage_id == "brief-development":
        try:
            project_mode_snapshot(project)
        except (ValueError, TypeError, OSError) as error:
            failures.append(f"project.md is not a valid brief record: {error}")
        return failures, evidence
    root = studio_root(project)
    if not (root / "index.html").is_file():
        return ["No Studio project; run studio_project.py sync first"], evidence
    shots = discover_shots(project)
    result = status(project)
    blocking = blocking_issues(result, stage_id in SELECTION_STAGES)
    evidence["status_ok"] = not blocking
    failures += [f"{item['shot_id']}: {item['code']}" for item in blocking]
    if stage_id in FRAME_STAGES:
        on_timeline = {
            frame["shot_id"] for frame in result["frames"] if frame["on_timeline"]
        }
        failures += [
            f"{shot.shot_id}: no placed take"
            for shot in shots
            if shot.shot_id not in on_timeline
        ]
        evidence["check_ran"] = True
        evidence["check_ok"] = check_passed(
            run_hyperframes(project, ["check", "--json"], runner)
        )
        if not evidence["check_ok"]:
            failures.append("hyperframes check failed")
    provenance_path = root / "provenance.json"
    if provenance_path.is_file():
        evidence["provenance_sha256"] = sha256_file(provenance_path)
    evidence["index_sha256"] = sha256_file(root / "index.html")
    if stage_id == "delivery":
        problems, record = delivery_failures(project, shots)
        failures += problems
        if record:
            evidence["render_record"] = record
    failures += lock_failures(project, ledger, stage_id, evidence.get("render_record"))
    return failures, evidence


def complete_stage(
    project: Path, stage_id: str, runner: Runner = subprocess.run
) -> dict[str, Any]:
    value = read_stages(project)
    entry = stage_entry(value, stage_id)
    require_earlier_done(value, stage_id, "completing")
    failures, evidence = stage_gate(project, stage_id, runner, value)
    if failures:
        raise StudioError(f"{stage_id} cannot exit: " + "; ".join(failures))
    entry.update(
        status="complete",
        completed_at=datetime.now(UTC).isoformat(timespec="seconds"),
        evidence=evidence,
    )
    entry.pop("reason", None)
    advance(value, stage_id)
    write_stages(project, value)
    return value


def selection_service() -> Any:
    scripts = Path(__file__).resolve().parents[1] / "skills/showcase-html/scripts"
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    return importlib.import_module("selection_service")


def selection_registry(project: Path, shot: Shot) -> dict[str, Any]:
    variants = {
        path.name: path.relative_to(project).as_posix()
        for path in sorted((project / shot.directory).iterdir())
        if path.suffix in MEDIA_SUFFIXES
    }
    return {
        shot.shot_id: {
            "manifest": shot.manifest,
            "field": "selected_variant",
            "key": None,
            "stage": None,
            "variants": variants,
            "reviews": {},
        }
    }


def require_authorized(decision: dict[str, Any], mode: str) -> None:
    actor = decision.get("actor")
    if actor == "agent":
        if mode != "approve_for_me":
            raise StudioError(
                "An agent decision is only valid when project.md sets approval_mode: approve_for_me"
            )
        return
    if actor != "user":
        raise StudioError("A decision's actor must be agent or user")
    authorization = decision.get("authorization")
    evidence = (
        authorization.get("evidence") if isinstance(authorization, dict) else None
    )
    chat = isinstance(authorization, dict) and authorization.get("source") == "chat"
    if not chat or not isinstance(evidence, str) or len(evidence.strip()) < 3:
        raise StudioError(
            'A user decision needs authorization {"source": "chat", "evidence": '
            "<the user's own words choosing this take>}"
        )


def record_selection(
    project: Path, shot_id: str, decision: dict[str, Any]
) -> dict[str, Any]:
    project = project.resolve()
    if not isinstance(decision, dict):
        raise StudioError("A decision file must contain one JSON object")
    mode, _ = project_mode_snapshot(project)
    require_authorized(decision, mode)
    shot = find_shot(project, shot_id)
    asset = placed_asset(project, shot_id)
    if asset is None:
        raise StudioError(f"{shot_id} has no placed take in Studio")
    prefix, filename = split_asset(asset)
    if decision.get("selected_variant") != filename:
        raise StudioError(
            f"Decision selects {decision.get('selected_variant')!r} but Studio has {filename!r} placed"
        )
    copy = studio_path(project, "assets", asset)
    source = project / take_path(shot, filename)
    for path in (copy, source):
        if not prefix or not path.is_file() or not sha256_file(path).startswith(prefix):
            raise StudioError(f"Placed asset no longer matches {filename}")
    registry = selection_registry(project, shot)
    service = selection_service()
    result = service.apply_selection_batch(
        project,
        {"registry": registry, "selections": {shot_id: filename}},
        service.revision(project, registry),
        decisions={shot_id: decision},
        allow_chat=True,
    )
    shots = discover_shots(project)
    storyboard_path, header, sections = read_storyboard(
        project, *canvas_dimensions(project)
    )
    if refresh_section_lines(sections, shots):
        atomic_write(storyboard_path, header + "".join(sections))
    write_provenance(project, shots)
    return result  # type: ignore[no-any-return]


def lock_subject_problem(project: Path, kind: str, subject: str) -> str | None:
    if kind == "audio":
        return None
    for _, record in read_render_records(project):
        if record["output"]["path"] != subject:
            continue
        quality = render_quality(record["hyperframes"]["arguments"])
        if record["produced_by"] != "render":
            return "the lock subject was not made by studio_project.py render"
        if kind == "final_master" and quality not in DELIVERY_QUALITIES:
            return "a final master lock needs a standard-or-higher render"
        return None
    return "the lock subject is not a recorded render"


def record_lock(project: Path, decision: dict[str, Any]) -> dict[str, Any]:
    project = project.resolve()
    if not isinstance(decision, dict) or decision.get("decision_type") != "stage_lock":
        raise StudioError("A lock needs one stage_lock decision object")
    mode, _ = project_mode_snapshot(project)
    require_authorized(decision, mode)
    kind, stage_id = decision.get("lock_kind"), decision.get("stage_id")
    if STAGE_LOCKS.get(str(kind)) != stage_id:
        raise StudioError(
            f"A {kind} lock belongs to {STAGE_LOCKS.get(str(kind))}, not {stage_id}"
        )
    ledger = read_stages(project)
    entry = stage_entry(ledger, str(stage_id))
    if ledger["current_stage"] != stage_id or entry["status"] != "review":
        raise StudioError(f"Start {stage_id} before recording its {kind} lock")
    subject = decision.get("subject_path")
    if not isinstance(subject, str):
        raise StudioError("A lock decision needs a subject_path")
    problem = lock_subject_problem(project, str(kind), subject)
    if problem:
        raise StudioError(problem)
    service = selection_service()
    artifact = service.contained_path(project, subject)
    subject_sha = service.sha256(artifact)
    if decision.get("subject_sha256") != subject_sha:
        raise StudioError("The lock decision's subject_sha256 does not match the file")
    existing = entry.get("locks", {}).get(kind)
    if decision["actor"] == "agent" and existing and existing["actor"] != "agent":
        raise StudioError("An agent cannot replace a user stage lock")
    path, content, digest = service.validated_decision(
        project, decision, subject, subject_sha, mode, None, True
    )
    review = service.validated_review(
        project,
        decision["review_path"],
        decision["review_sha256"],
        subject,
        subject_sha,
    )
    audio_required = (
        kind == "final_master"
        and stage_entry(ledger, "audio-preparation")["status"] != "skipped"
    )
    service.validate_stage_media(
        project, kind, subject, review, audio_required=audio_required
    )
    entry.setdefault("locks", {})[kind] = {
        "decision_id": decision["decision_id"],
        "decision_sha256": digest,
        "result": decision["result"],
        "artifact_path": subject,
        "artifact_sha256": subject_sha,
        "review_path": decision["review_path"],
        "review_sha256": decision["review_sha256"],
        "actor": decision["actor"],
        "reason": decision["reason"],
    }
    findings = schema_findings(ledger, "studio-stages.schema.json")
    if findings:
        raise StudioError(f"stages.json failed its schema: {findings[0].message}")
    with service.writer_lock(project):
        service.recover_selection(project)
        service.commit_targets(
            project,
            {
                path: content,
                "studio/stages.json": json.dumps(ledger, indent=2, ensure_ascii=False)
                + "\n",
            },
        )
    return {"decision_id": decision["decision_id"], "decision_path": path, "lock": kind}


def parse_requested(values: list[str]) -> dict[str, str]:
    requested = {}
    for value in values:
        shot_id, separator, filename = value.partition("=")
        if (
            not separator
            or not SHOT_ID_PATTERN.match(shot_id)
            or not FILENAME_PATTERN.match(filename)
        ):
            raise StudioError(f"Expected --take SHOT=FILENAME, got {value!r}")
        requested[shot_id] = filename
    return requested


COMMANDS = (
    "init",
    "sync",
    "candidates",
    "place",
    "status",
    "check",
    "render",
    "stage",
    "record-selection",
    "record-lock",
    "record-render",
    "hf",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Bridge shot manifests to a HyperFrames Studio project"
    )
    commands = parser.add_subparsers(dest="command", required=True)
    for name in COMMANDS:
        sub = commands.add_parser(name)
        sub.add_argument("project", type=Path)
        if name == "init":
            sub.add_argument("--aspect")
            sub.add_argument("--resolution")
        if name == "sync":
            sub.add_argument(
                "--take", action="append", default=[], metavar="SHOT=FILENAME"
            )
        if name in {"candidates", "place", "record-selection"}:
            sub.add_argument("shot_id")
        if name == "place":
            sub.add_argument("filename")
        if name in {"record-selection", "record-lock"}:
            sub.add_argument("--decision", type=Path, required=True)
        if name == "render":
            sub.add_argument("--name", default="final")
            sub.add_argument(
                "--quality", default="delivery", choices=sorted(RENDER_QUALITIES)
            )
        if name == "stage":
            sub.add_argument(
                "action", choices=["show", "start", "complete", "reopen", "skip"]
            )
            sub.add_argument("stage_id", nargs="?")
            sub.add_argument("--reason", default="")
        if name == "record-render":
            sub.add_argument("render_file", type=Path)
            sub.add_argument("hyperframes_arguments", nargs=argparse.REMAINDER)
        if name == "hf":
            sub.add_argument("hyperframes_arguments", nargs=argparse.REMAINDER)
    return parser


def run_stage(args: argparse.Namespace) -> dict[str, Any]:
    if args.action == "show":
        return read_stages(args.project)
    if not args.stage_id:
        raise StudioError("stage start, complete, reopen and skip need a stage id")
    if args.action == "skip":
        return skip_stage(args.project, args.stage_id, args.reason)
    actions = {"start": start_stage, "complete": complete_stage, "reopen": reopen_stage}
    return actions[args.action](args.project, args.stage_id)


def run(args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    project: Path = args.project
    command = args.command
    if command == "init":
        shots = discover_shots(project)
        aspect = args.aspect or (shots[0].aspect if shots else "16:9")
        resolution = args.resolution or (shots[0].resolution if shots else "720p")
        return {"ok": True, "studio": str(init_studio(project, aspect, resolution))}, 0
    if command == "sync":
        report = sync(project, parse_requested(args.take))
        return {
            "ok": True,
            "added": report.added,
            "preserved": report.preserved,
            "outlined": report.outlined,
            "skipped": report.skipped,
            "warnings": report.warnings,
        }, 0
    if command == "candidates":
        return {"ok": True, **candidates(project, args.shot_id)}, 0
    if command == "place":
        return {"ok": True, **place_take(project, args.shot_id, args.filename)}, 0
    if command == "status":
        result = status(project)
        return result, 0 if result["ok"] else 3
    if command == "check":
        completed = run_hyperframes(project, ["check", "--json"])
        passed = check_passed(completed)
        return {"ok": passed, "output": completed.stdout[-4000:]}, int(not passed)
    if command == "render":
        return {"ok": True, "record": str(render(project, args.name, args.quality))}, 0
    if command == "stage":
        return {"ok": True, **run_stage(args)}, 0
    if command == "record-selection":
        decision = json.loads(read_text(args.decision))
        return {"ok": True, **record_selection(project, args.shot_id, decision)}, 0
    if command == "record-lock":
        decision = json.loads(read_text(args.decision))
        return {"ok": True, **record_lock(project, decision)}, 0
    if command == "hf":
        completed = hf_command(project, args.hyperframes_arguments)
        return {
            "ok": completed.returncode == 0,
            "returncode": completed.returncode,
            "stdout": completed.stdout[-8000:],
            "stderr": completed.stderr[-2000:],
        }, int(completed.returncode != 0)
    sidecar = record_render(project, args.render_file, args.hyperframes_arguments)
    return {"ok": True, "record": str(sidecar)}, 0


def main(argv: list[str] | None = None) -> int:
    try:
        result, code = run(build_parser().parse_args(argv))
    except (StudioError, ValueError, OSError, KeyError, TypeError) as error:
        print(json.dumps({"ok": False, "error": str(error)}))
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
