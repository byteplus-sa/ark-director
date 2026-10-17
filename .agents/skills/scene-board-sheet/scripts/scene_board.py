from __future__ import annotations

import argparse
import copy
import hashlib
import html
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = (
    Path(__file__).resolve().parents[3] / "contracts/schemas/scene-board.schema.json"
)
TEMPLATE_DIR = SKILL_ROOT / "templates"

LEVELS = ("L1", "L2", "L3")
DEFAULT_LEVEL = "L2"
DEFAULT_SUB_BEATS = ("anticipation", "contact", "consequence", "reaction")
STYLES = ("pencil", "ink", "charcoal", "limited-palette", "full-colour")
PANELS_PER_PAGE = 6
SHEET_WIDTH = 3840
SHEET_HEIGHT = 2160
MAX_PANELS_PER_CLIP = 99
MAX_VERSION = 99
TWO_EDIT_LIMIT = 2
COPY_LIMITS = {"move": 120, "dialogue": 160, "lens_intent": 100, "light": 100}
CARRIED_FIELDS = (
    "framing",
    "featured",
    "size",
    "angle",
    "move",
    "lens_intent",
    "light",
    "dialogue",
    "sound_cue",
    "transition_in",
    "screen_direction",
    "continuity_carry",
    "elements",
)
PLAN_AGREEMENT_FIELDS = (
    "size",
    "angle",
    "framing",
    "featured",
    "move",
    "lens_intent",
    "light",
)
PANEL_FILE = re.compile(r"^(s\d{2}_sh\d{3}_p\d{3})_t(\d{2})_v(\d{2})\.png$")
SHOT_ID = re.compile(r"^(s\d{2}_sh\d{3})(?:_[a-z]+)?$")
BBOX_PATTERN = re.compile(r"^\d{1,3}(,\d{1,3}){3}$")
BEAT_NAME = re.compile(r"^[a-z][a-z0-9-]*$")


class BoardError(Exception):
    pass


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    message: str
    path: str = ""

    def as_dict(self) -> dict[str, str]:
        return {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "message": self.message,
            "path": self.path,
        }


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_json(value: Any) -> str:
    return sha256_bytes(json.dumps(value, sort_keys=True, ensure_ascii=False).encode())


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise BoardError(f"Cannot read JSON record {path.name}: {error}") from error


def yaml_loader() -> YAML:
    return YAML(typ="safe")


def dump_yaml(value: Any) -> str:
    yaml = YAML(typ="safe")
    yaml.default_flow_style = False
    yaml.width = 100
    yaml.sort_base_mapping_type_on_output = False  # type: ignore[assignment]
    buffer = io.StringIO()
    yaml.dump(value, buffer)
    return buffer.getvalue()


def project_root(value: str | Path) -> Path:
    root = Path(value).resolve()
    if not root.is_dir():
        raise BoardError(f"Project directory not found: {value}")
    return root


def contained(root: Path, relative: str) -> Path:
    if (
        not isinstance(relative, str)
        or not relative
        or Path(relative).is_absolute()
        or ".." in Path(relative).parts
    ):
        raise BoardError(
            f"Path must be relative and stay inside the project: {relative!r}"
        )
    resolved = (root / relative).resolve()
    if root != resolved and root not in resolved.parents:
        raise BoardError(f"Path escapes the project: {relative}")
    return resolved


def relative_to(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root).as_posix()


def safe_directory(root: Path, relative: str) -> Path:
    contained(root, relative)
    current = root
    for part in Path(relative).parts:
        current = current / part
        if current.is_symlink():
            raise BoardError(f"Refusing to write through a symlink: {relative}")
    current.mkdir(parents=True, exist_ok=True)
    return contained(root, relative)


def write_text_atomic(root: Path, path: Path, text: str) -> None:
    target = path.parent.resolve() / path.name
    if root not in target.parents:
        raise BoardError(f"Refusing to write outside the project: {path}")
    if path.is_symlink():
        raise BoardError(f"Refusing to write through a symlink: {path.name}")
    descriptor, name = tempfile.mkstemp(prefix=".board-", dir=target.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text)
        os.replace(name, target)
    finally:
        Path(name).unlink(missing_ok=True)


def write_json(root: Path, path: Path, value: Any) -> None:
    write_text_atomic(
        root,
        path,
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
    )


def normalize_scene(value: str) -> str:
    match = re.fullmatch(r"(?:scene-)?(\d{1,2})", value.strip())
    if not match:
        raise BoardError(f"Scene must look like scene-02 or 02: {value!r}")
    return f"scene-{int(match.group(1)):02d}"


def scene_prefix(scene: str) -> str:
    return f"s{scene.split('-')[1]}"


def scene_dir(root: Path, scene: str) -> Path:
    return contained(root, f"scenes/{scene}")


def split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    match = re.match(r"\A---\s*\n(.*?)\n---[ \t]*(?:\n|\Z)(.*)\Z", text, re.DOTALL)
    if not match:
        raise BoardError("Missing YAML front matter")
    try:
        data = yaml_loader().load(match.group(1))
    except YAMLError as error:
        raise BoardError(f"Invalid front matter: {error}") from error
    if not isinstance(data, dict):
        raise BoardError("Front matter must be a mapping")
    return data, match.group(2)


def shot_plan_section(text: str) -> str:
    lines = text.splitlines()
    start = next(
        (
            index
            for index, line in enumerate(lines)
            if re.match(r"^##\s+Shot plan\s*$", line)
        ),
        None,
    )
    if start is None:
        raise BoardError("scene.md has no '## Shot plan' section")
    end = next(
        (
            index
            for index in range(start + 1, len(lines))
            if re.match(r"^##\s+\S", lines[index])
        ),
        len(lines),
    )
    return "\n".join(lines[start:end]).strip()


def load_shot_plan(section: str, scene: str) -> dict[str, Any]:
    match = re.search(r"```ya?ml\s*\n(.*?)\n```", section, re.DOTALL)
    if not match:
        raise BoardError("The '## Shot plan' section has no fenced yaml block")
    try:
        data = yaml_loader().load(match.group(1))
    except YAMLError as error:
        raise BoardError(f"Invalid shot plan yaml: {error}") from error
    plan = data.get("shot_plan") if isinstance(data, dict) else None
    if not isinstance(plan, dict) or not isinstance(plan.get("shots"), list):
        raise BoardError(
            "The yaml block must hold a shot_plan mapping with a shots list"
        )
    seen: set[str] = set()
    for shot in plan["shots"]:
        identifier = str(shot.get("id", "")) if isinstance(shot, dict) else ""
        if not SHOT_ID.match(identifier):
            raise BoardError(f"Shot id does not match sNN_shNNN[_x]: {shot!r}")
        if not identifier.startswith(scene_prefix(scene) + "_"):
            raise BoardError(f"Shot {identifier} does not belong to {scene}")
        if identifier in seen:
            raise BoardError(f"Duplicate shot id in the shot plan: {identifier}")
        seen.add(identifier)
        duration = shot.get("duration_s")
        if (
            not isinstance(duration, (int, float))
            or isinstance(duration, bool)
            or duration <= 0
        ):
            raise BoardError(f"Shot {identifier} needs a positive duration_s")
    return plan


@dataclass(frozen=True)
class SceneSource:
    scene: str
    directory: Path
    plan: dict[str, Any]
    plan_sha256: str


def load_scene_source(root: Path, scene: str) -> SceneSource:
    directory = scene_dir(root, scene)
    scene_file = directory / "scene.md"
    if not scene_file.is_file():
        raise BoardError(f"Missing scenes/{scene}/scene.md")
    section = shot_plan_section(scene_file.read_text(encoding="utf-8"))
    plan = load_shot_plan(section, scene)
    return SceneSource(
        scene=scene, directory=directory, plan=plan, plan_sha256=sha256_json(plan)
    )


def is_static(shot: dict[str, Any]) -> bool:
    if shot.get("static_reason"):
        return True
    return str(shot.get("move", "static hold")).strip().lower().startswith("static")


def cue_shots(plan: dict[str, Any]) -> set[str]:
    named: set[str] = set()
    for source in plan.get("sources") or []:
        for cue in (source or {}).get("cues") or []:
            if isinstance(cue, dict) and cue.get("shot"):
                named.add(str(cue["shot"]))
    return named


def key_reasons(
    shot: dict[str, Any], plan: dict[str, Any], overridden: bool = False
) -> list[str]:
    reasons: list[str] = ["override"] if overridden else []
    if shot.get("turn") is True:
        reasons.append("turn")
    if not is_static(shot):
        reasons.append("move")
    if shot.get("blocking_change") is True:
        reasons.append("blocking_change")
    if shot.get("axis_crossed") is True:
        reasons.append("axis_crossed")
    if shot.get("state_change"):
        reasons.append("state_change")
    if str(shot["id"]) in cue_shots(plan):
        reasons.append("light_cue")
    return reasons


def sub_beat_names(shot: dict[str, Any]) -> list[str]:
    beats = shot.get("sub_beats")
    if not isinstance(beats, list) or not beats:
        return list(DEFAULT_SUB_BEATS)
    names = [str(beat).strip().lower().replace(" ", "-") for beat in beats]
    bad = [name for name in names if not BEAT_NAME.match(name)]
    if bad:
        raise BoardError(
            f"sub_beats of {shot['id']} must be lowercase words (letters, digits, hyphens): {bad}"
        )
    return names


def panel_states(level: str, shot: dict[str, Any], reasons: list[str]) -> list[str]:
    if level not in LEVELS:
        raise BoardError(f"Unknown level {level!r}")
    if level == "L1" or not reasons:
        return ["single"]
    if level == "L3":
        return sub_beat_names(shot)
    if {"override", "turn", "move", "axis_crossed", "light_cue"} & set(reasons):
        return ["start", "peak", "end"]
    return ["start", "end"]


def milliseconds(value: float) -> int:
    return round(float(value) * 1000)


def seconds(milliseconds_value: int) -> float:
    return round(milliseconds_value / 1000, 3)


def split_milliseconds(total_ms: int, count: int) -> list[int]:
    base = total_ms // count
    parts = [base] * count
    parts[-1] += total_ms - base * count
    return parts


def carried(shot: dict[str, Any]) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    if shot.get("job"):
        fields["beat"] = str(shot["job"])
    for name in CARRIED_FIELDS:
        if shot.get(name) in (None, "", []):
            continue
        fields[name] = copy.deepcopy(shot[name])
    return fields


def derive_panels(
    source: SceneSource, level: str, overrides: dict[str, tuple[str, str]]
) -> list[dict[str, Any]]:
    panels: list[dict[str, Any]] = []
    counters: dict[str, int] = {}
    for shot in source.plan["shots"]:
        shot_id = str(shot["id"])
        clip = SHOT_ID.match(shot_id).group(1)  # type: ignore[union-attr]
        shot_level, reason = overrides.get(shot_id, (level, ""))
        reasons = key_reasons(shot, source.plan, shot_id in overrides)
        states = panel_states(shot_level, shot, reasons)
        durations = split_milliseconds(milliseconds(shot["duration_s"]), len(states))
        for state, duration_ms in zip(states, durations, strict=True):
            counters[clip] = counters.get(clip, 0) + 10
            if counters[clip] > MAX_PANELS_PER_CLIP * 10:
                raise BoardError(
                    f"Clip {clip} has more than {MAX_PANELS_PER_CLIP} panels"
                )
            panel: dict[str, Any] = {
                "id": f"{clip}_p{counters[clip]:03d}",
                "clip": clip,
                "shot": shot_id,
                "state": state,
            }
            if shot_id in overrides:
                panel["shot_level"] = shot_level
                panel["shot_level_reason"] = reason
            panel.update(carried(shot))
            panel["duration_s"] = seconds(duration_ms)
            panel["status"] = "planned"
            panels.append(panel)
    return panels


def parse_override(value: str) -> tuple[str, tuple[str, str]]:
    parts = value.split("=", 2)
    if (
        len(parts) != 3
        or not parts[0]
        or parts[1] not in LEVELS
        or not parts[2].strip()
    ):
        raise BoardError(
            "Override must be SHOT=LEVEL=REASON, for example s01_sh010_a=L3=fight beat"
        )
    return parts[0], (parts[1], parts[2].strip())


def parse_overrides(values: list[str]) -> dict[str, tuple[str, str]]:
    overrides: dict[str, tuple[str, str]] = {}
    for value in values:
        shot, parsed = parse_override(value)
        if shot in overrides:
            raise BoardError(f"Shot {shot} has more than one override")
        overrides[shot] = parsed
    return overrides


def board_path(root: Path, scene: str) -> Path:
    return scene_dir(root, scene) / "board.md"


def read_board(root: Path, scene: str) -> tuple[dict[str, Any], str]:
    path = board_path(root, scene)
    if not path.is_file():
        raise BoardError(f"Missing scenes/{scene}/board.md; run init first")
    return split_front_matter(path.read_text(encoding="utf-8"))


def write_board(root: Path, scene: str, board: dict[str, Any], body: str) -> Path:
    path = board_path(root, scene)
    write_text_atomic(root, path, "---\n" + dump_yaml(board) + "---\n" + body)
    return path


def default_body(scene: str) -> str:
    number = int(scene.split("-")[1])
    return (
        f"\n# Scene {number} board\n\n"
        "Panel records are above. Change them through scene_board.py.\n"
    )


def plan_board_status(plan: dict[str, Any]) -> str:
    return "ready" if plan.get("status") == "ready" else "draft"


def initial_board(
    source: SceneSource,
    level: str,
    level_reason: str,
    overrides: dict[str, tuple[str, str]],
    style: str,
    aspect: str,
) -> dict[str, Any]:
    board: dict[str, Any] = {
        "schema_version": 1,
        "scene": source.scene,
        "status": plan_board_status(source.plan),
        "level": level,
        "level_reason": level_reason,
        "render_style": style,
        "aspect_ratio": aspect,
        "bind_to_seedance": False,
        "shot_plan_sha256": source.plan_sha256,
    }
    if overrides:
        board["overrides"] = [
            {"shot": shot, "level": value[0], "reason": value[1]}
            for shot, value in sorted(overrides.items())
        ]
    board["panels"] = derive_panels(source, level, overrides)
    return board


def validate_new_board(board: dict[str, Any]) -> None:
    problems = schema_findings(board)
    if problems:
        raise BoardError("; ".join(finding.message for finding in problems))


def has_panel_history(board: dict[str, Any]) -> bool:
    return any(
        panel.get("file") or panel.get("versions") for panel in board.get("panels", [])
    )


def init_board(
    root: Path,
    scene: str,
    level: str,
    level_reason: str,
    override_values: list[str],
    style: str,
    aspect: str,
    overwrite: bool,
) -> dict[str, Any]:
    if level not in LEVELS:
        raise BoardError(f"Level must be one of {', '.join(LEVELS)}")
    if not level_reason.strip():
        raise BoardError("A level reason is required")
    existing = board_path(root, scene)
    if existing.exists():
        if not overwrite:
            raise BoardError(
                f"scenes/{scene}/board.md exists; pass --overwrite to replace it"
            )
        if has_panel_history(read_board(root, scene)[0]):
            raise BoardError(
                "The board has registered panels; use rebase-plan to follow a changed "
                "shot plan without losing them"
            )
    overrides = parse_overrides(override_values)
    source = load_scene_source(root, scene)
    unknown = sorted(
        set(overrides) - {str(shot["id"]) for shot in source.plan["shots"]}
    )
    if unknown:
        raise BoardError(
            f"Overrides name shots that are not in the shot plan: {', '.join(unknown)}"
        )
    board = initial_board(source, level, level_reason.strip(), overrides, style, aspect)
    validate_new_board(board)
    path = write_board(root, scene, board, default_body(scene))
    return {
        "board": relative_to(root, path),
        "level": level,
        "panels": len(board["panels"]),
        "panels_per_shot": count_per_shot(board["panels"]),
    }


def count_per_shot(panels: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for panel in panels:
        counts[panel["shot"]] = counts.get(panel["shot"], 0) + 1
    return counts


def rebase_plan(root: Path, scene: str) -> dict[str, Any]:
    board, body = read_board(root, scene)
    source = load_scene_source(root, scene)
    overrides = {
        item["shot"]: (item["level"], item["reason"])
        for item in board.get("overrides", [])
    }
    derived = derive_panels(source, board["level"], overrides)
    previous = {panel["id"]: panel for panel in board["panels"]}
    carried_ids: set[str] = set()
    changed: list[str] = []
    for panel in derived:
        old = previous.get(panel["id"])
        if not old or old["shot"] != panel["shot"] or old["state"] != panel["state"]:
            continue
        carried_ids.add(panel["id"])
        for name in ("file", "sha256", "versions", "status", "decision"):
            if name in old:
                panel[name] = old[name]
        differs = any(
            old.get(name) != panel.get(name) for name in PLAN_AGREEMENT_FIELDS
        )
        if differs and panel.get("file"):
            panel["status"] = "needs_edit"
            panel.pop("decision", None)
            changed.append(panel["id"])
    orphaned = [
        {"panel": panel_id, "file": old.get("file")}
        for panel_id, old in previous.items()
        if panel_id not in carried_ids and old.get("file")
    ]
    board["panels"] = derived
    board["shot_plan_sha256"] = source.plan_sha256
    board["status"] = plan_board_status(source.plan)
    validate_new_board(board)
    write_board(root, scene, board, body)
    return {
        "panels": len(derived),
        "carried": sorted(carried_ids),
        "needs_edit": changed,
        "orphaned_files": orphaned,
        "new_panels": sorted(
            panel["id"] for panel in derived if panel["id"] not in carried_ids
        ),
    }


def schema_findings(board: dict[str, Any]) -> list[Finding]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        Finding(
            "board.schema",
            "error",
            f"{'/'.join(str(part) for part in error.absolute_path) or '(root)'}: {error.message}",
        )
        for error in sorted(
            validator.iter_errors(board), key=lambda item: list(item.absolute_path)
        )
    ]


def request_references(root: Path) -> list[dict[str, Any]]:
    registry = root / "task_ids.json"
    if not registry.is_file():
        return []
    try:
        data = json.loads(registry.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    tasks = data.get("tasks") if isinstance(data, dict) else None
    references: list[dict[str, Any]] = []
    for task in tasks if isinstance(tasks, list) else []:
        listed = task.get("references") if isinstance(task, dict) else None
        for reference in listed if isinstance(listed, list) else []:
            if isinstance(reference, dict):
                references.append(reference)
    return references


def board_artifact_paths(
    root: Path, scene: str, board: dict[str, Any]
) -> tuple[dict[str, str], set[str]]:
    hashes: dict[str, str] = {}
    paths: set[str] = set()
    for panel in board.get("panels", []):
        for version in panel.get("versions") or []:
            hashes[str(version["sha256"])] = str(version["file"])
            paths.add(str(version["file"]))
    directory = scene_dir(root, scene) / "board"
    if directory.is_dir():
        for path in directory.rglob("*"):
            if path.suffix in {".png", ".mp4"} and path.is_file():
                hashes[sha256_file(path)] = relative_to(root, path)
    return hashes, paths


def normalize_reference_path(value: str) -> str:
    parts = [part for part in Path(value.replace("\\", "/")).parts if part != "."]
    return "/".join(parts)


def check_board(root: Path, scene: str) -> list[Finding]:
    board, _ = read_board(root, scene)
    findings = schema_findings(board)
    if findings:
        return findings
    if board["scene"] != scene:
        findings.append(
            Finding(
                "board.scene",
                "error",
                f"board.md is for {board['scene']} but sits in {scene}",
            )
        )
    source = load_scene_source(root, scene)
    if board["shot_plan_sha256"] != source.plan_sha256:
        findings.append(
            Finding(
                "board.plan_stale",
                "error",
                "The shot plan changed after the board was derived; run rebase-plan and review the panels",
            )
        )
    plan_shots = {str(shot["id"]): shot for shot in source.plan["shots"]}
    panels = board["panels"]
    seen: set[str] = set()
    per_shot: dict[str, list[dict[str, Any]]] = {}
    for panel in panels:
        if panel["id"] in seen:
            findings.append(
                Finding("board.panel_id", "error", f"Duplicate panel id {panel['id']}")
            )
        seen.add(panel["id"])
        if panel["shot"] not in plan_shots:
            findings.append(
                Finding(
                    "board.shot_missing",
                    "error",
                    f"{panel['id']} names a shot that is not in the plan: {panel['shot']}",
                )
            )
            continue
        if SHOT_ID.match(panel["shot"]).group(1) != panel["clip"]:  # type: ignore[union-attr]
            findings.append(
                Finding(
                    "board.panel_id",
                    "error",
                    f"{panel['id']} clip does not match its shot",
                )
            )
        if not panel["id"].startswith(panel["clip"] + "_p"):
            findings.append(
                Finding(
                    "board.panel_id",
                    "error",
                    f"{panel['id']} does not belong to clip {panel['clip']}",
                )
            )
        per_shot.setdefault(panel["shot"], []).append(panel)
    for shot_id in plan_shots:
        if shot_id not in per_shot:
            findings.append(
                Finding("board.shot_missing", "error", f"Shot {shot_id} has no panel")
            )
    overrides = {item["shot"]: item for item in board.get("overrides", [])}
    for shot_id in overrides:
        if shot_id not in plan_shots:
            findings.append(
                Finding(
                    "board.shot_missing",
                    "error",
                    f"Override names unknown shot {shot_id}",
                )
            )
    for shot_id, shot_panels in per_shot.items():
        findings.extend(
            check_shot_panels(
                shot_id, shot_panels, plan_shots[shot_id], source, board, overrides
            )
        )
    hashes, version_paths = board_artifact_paths(root, scene, board)
    for panel in panels:
        if panel.get("shot_level") is not None and not panel.get("shot_level_reason"):
            findings.append(
                Finding(
                    "board.override_reason",
                    "error",
                    f"{panel['id']} overrides the level without a reason",
                )
            )
        findings.extend(check_panel_record(root, panel))
    prefix = f"scenes/{scene}/board/"
    for reference in request_references(root):
        digest = str(reference.get("sha256", ""))
        path = normalize_reference_path(str(reference.get("path", "")))
        if digest in hashes or path in version_paths or path.startswith(prefix):
            findings.append(
                Finding(
                    "board.bound_to_request",
                    "error",
                    f"{hashes.get(digest, path)} is bound as a request reference; boards are never Seedance inputs",
                    path,
                )
            )
    return findings


def check_shot_panels(
    shot_id: str,
    shot_panels: list[dict[str, Any]],
    shot: dict[str, Any],
    source: SceneSource,
    board: dict[str, Any],
    overrides: dict[str, dict[str, Any]],
) -> list[Finding]:
    findings: list[Finding] = []
    total = sum(milliseconds(panel["duration_s"]) for panel in shot_panels)
    if total != milliseconds(shot["duration_s"]):
        findings.append(
            Finding(
                "board.duration_sum",
                "error",
                f"{shot_id} panels sum to {seconds(total)} s but the shot plan says {shot['duration_s']} s",
            )
        )
    for panel in shot_panels:
        for name in PLAN_AGREEMENT_FIELDS:
            if name in panel and name in shot and panel[name] != shot[name]:
                findings.append(
                    Finding(
                        "board.field_mismatch",
                        "error",
                        f"{panel['id']} {name} differs from the shot plan",
                    )
                )
            elif name in shot and name not in panel:
                findings.append(
                    Finding(
                        "board.field_missing",
                        "warning",
                        f"{panel['id']} lacks {name}, which the shot plan sets",
                    )
                )
    level = overrides[shot_id]["level"] if shot_id in overrides else board["level"]
    expected = panel_states(
        level, shot, key_reasons(shot, source.plan, shot_id in overrides)
    )
    if [panel["state"] for panel in shot_panels] != expected:
        findings.append(
            Finding(
                "board.level_mismatch",
                "warning",
                f"{shot_id} panels differ from what level {level} derives ({', '.join(expected)})",
            )
        )
    return findings


def check_panel_record(root: Path, panel: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    versions = panel.get("versions") or []
    if panel["status"] in {"review", "needs_edit", "approved"}:
        findings.extend(check_panel_file(root, panel))
    if versions and (
        panel.get("file") != versions[-1]["file"]
        or panel.get("sha256") != versions[-1]["sha256"]
    ):
        findings.append(
            Finding(
                "board.version_head",
                "error",
                f"{panel['id']} file and sha256 do not match its newest version",
            )
        )
    for version in versions[:-1]:
        try:
            if not contained(root, version["file"]).is_file():
                findings.append(
                    Finding(
                        "board.version_missing",
                        "warning",
                        f"{panel['id']} earlier version is gone: {version['file']}",
                    )
                )
        except BoardError as error:
            findings.append(Finding("board.version_missing", "error", str(error)))
    if panel["status"] == "approved" and not panel.get("decision"):
        findings.append(
            Finding(
                "board.approved_without_decision",
                "error",
                f"{panel['id']} is approved without a decision record",
            )
        )
    decision = panel.get("decision")
    if decision:
        findings.extend(check_decision(root, panel, decision))
    return findings


def check_decision(
    root: Path, panel: dict[str, Any], decision: dict[str, Any]
) -> list[Finding]:
    try:
        path = contained(root, decision["path"])
    except BoardError as error:
        return [Finding("board.decision_stale", "error", str(error))]
    if not path.is_file() or sha256_file(path) != decision["sha256"]:
        return [
            Finding(
                "board.decision_stale",
                "error",
                f"{panel['id']} decision file is missing or changed",
            )
        ]
    if decision["panel_sha256"] != panel.get("sha256"):
        return [
            Finding(
                "board.decision_stale",
                "error",
                f"{panel['id']} changed after it was approved",
            )
        ]
    return []


def check_panel_file(root: Path, panel: dict[str, Any]) -> list[Finding]:
    name = panel.get("file")
    if not name:
        return [
            Finding(
                "board.file_missing",
                "error",
                f"{panel['id']} is {panel['status']} but has no file",
            )
        ]
    try:
        path = contained(root, name)
    except BoardError as error:
        return [Finding("board.file_missing", "error", str(error))]
    if not path.is_file():
        return [
            Finding(
                "board.file_missing",
                "error",
                f"{panel['id']} file not found: {name}",
            )
        ]
    match = PANEL_FILE.match(path.name)
    if not match or match.group(1) != panel["id"]:
        return [
            Finding(
                "board.file_name",
                "error",
                f"{panel['id']} file name does not follow the panel naming contract: {path.name}",
            )
        ]
    if sha256_file(path) != panel.get("sha256"):
        return [
            Finding(
                "board.hash_mismatch",
                "error",
                f"{panel['id']} file changed after it was registered: {name}",
            )
        ]
    return []


def find_panel(board: dict[str, Any], panel_id: str) -> dict[str, Any]:
    for panel in board["panels"]:
        if panel["id"] == panel_id:
            return panel
    raise BoardError(f"Unknown panel {panel_id}")


def parse_bbox(value: str) -> list[int]:
    if not BBOX_PATTERN.match(value):
        raise BoardError("bbox must be x1,y1,x2,y2 in 0-999")
    x1, y1, x2, y2 = (int(part) for part in value.split(","))
    if max(x1, y1, x2, y2) > 999 or x1 >= x2 or y1 >= y2:
        raise BoardError(
            "bbox must satisfy 0 <= x1 < x2 <= 999 and 0 <= y1 < y2 <= 999"
        )
    return [x1, y1, x2, y2]


def register_panel(
    root: Path,
    scene: str,
    panel_id: str,
    file: str,
    edit_of: str | None,
    dimension: str | None,
    bbox: str | None,
    prompt_file: str | None,
    task_id: str | None,
) -> dict[str, Any]:
    board, body = read_board(root, scene)
    panel = find_panel(board, panel_id)
    path = contained(root, file)
    if not path.is_file():
        raise BoardError(f"File not found: {file}")
    match = PANEL_FILE.match(path.name)
    if not match or match.group(1) != panel_id:
        raise BoardError(f"File name must be {panel_id}_tNN_vNN.png: {path.name}")
    expected_directory = scene_dir(root, scene) / panel["clip"]
    if path.parent != expected_directory:
        raise BoardError(f"Panel files live in {relative_to(root, expected_directory)}")
    digest = sha256_file(path)
    versions = panel.setdefault("versions", [])
    if any(version["file"] == relative_to(root, path) for version in versions):
        raise BoardError(
            f"{path.name} is already registered; edits save a new version number"
        )
    version: dict[str, Any] = {
        "file": relative_to(root, path),
        "sha256": digest,
        "operation": "edit" if edit_of else "generate",
    }
    if edit_of:
        parent_name = relative_to(root, contained(root, edit_of))
        parent = next((item for item in versions if item["file"] == parent_name), None)
        if parent is None:
            raise BoardError(
                f"{edit_of} is not a registered version of {panel_id}; an edit must name the file it edited"
            )
        if parent["sha256"] == digest:
            raise BoardError(
                "The edited file is identical to the file it was edited from"
            )
        version["parent_file"] = parent["file"]
        version["parent_sha256"] = parent["sha256"]
        parent["rejected"] = True
        if dimension:
            version["dimension"] = dimension
        if bbox:
            version["bbox"] = parse_bbox(bbox)
    else:
        for earlier in versions:
            earlier["rejected"] = True
    if prompt_file:
        if not contained(root, prompt_file).is_file():
            raise BoardError(f"Prompt snapshot not found: {prompt_file}")
        version["prompt_file"] = prompt_file
    if task_id:
        version["task_id"] = task_id
    versions.append(version)
    panel["file"] = version["file"]
    panel["sha256"] = digest
    panel["status"] = "review"
    panel.pop("decision", None)
    validate_new_board(board)
    write_board(root, scene, board, body)
    return {
        "panel": panel_id,
        "file": version["file"],
        "operation": version["operation"],
        "sha256": digest,
    }


def mark_panel(
    root: Path, scene: str, panel_id: str, status: str, decision: str | None
) -> dict[str, Any]:
    board, body = read_board(root, scene)
    panel = find_panel(board, panel_id)
    if status not in {"review", "needs_edit", "rejected", "approved"}:
        raise BoardError("Status must be review, needs_edit, rejected or approved")
    if not panel.get("file"):
        raise BoardError("A panel without a registered file has nothing to mark")
    if status == "approved":
        if not decision:
            raise BoardError(
                "Approval needs --decision pointing at the recorded decision file"
            )
        if panel["status"] != "review":
            raise BoardError("Only a panel in review can be approved")
        if check_panel_file(root, panel):
            raise BoardError("The panel file changed since it was registered")
        decision_path = contained(root, decision)
        if not decision_path.is_file():
            raise BoardError(f"Decision file not found: {decision}")
        panel["decision"] = {
            "path": relative_to(root, decision_path),
            "sha256": sha256_file(decision_path),
            "panel_sha256": panel["sha256"],
        }
    else:
        panel.pop("decision", None)
    panel["status"] = status
    write_board(root, scene, board, body)
    return {"panel": panel_id, "status": status}


def derived_path(root: Path, scene: str, kind: str) -> Path:
    return scene_dir(root, scene) / "board" / kind


def derived_directory(root: Path, scene: str, kind: str) -> Path:
    return safe_directory(root, f"scenes/{scene}/board/{kind}")


def next_version(directory: Path, stem: str, suffix: str) -> int:
    pattern = re.compile(re.escape(stem) + r"_v(\d{2})" + re.escape(suffix) + r"$")
    numbers = [
        int(match.group(1))
        for path in directory.glob(f"{stem}_v*{suffix}")
        if (match := pattern.match(path.name))
    ]
    version = max(numbers, default=0) + 1
    if version > MAX_VERSION:
        raise BoardError(f"{stem} already has {MAX_VERSION} versions")
    return version


def short(text: str, limit: int) -> str:
    collapsed = " ".join(str(text).split())
    return (
        collapsed if len(collapsed) <= limit else collapsed[: limit - 1].rstrip() + "…"
    )


def format_light(light: Any) -> str:
    if isinstance(light, dict):
        parts = [str(light.get("source", "")), str(light.get("key_side", ""))]
        return " / ".join(part for part in parts if part)
    return str(light or "")


def annotation_values(panel: dict[str, Any]) -> dict[str, str]:
    values = {
        "id": panel["id"],
        "shot": panel["shot"],
        "state": panel["state"],
        "status": panel["status"],
        "framing": str(panel.get("framing", "")),
        "size": str(panel.get("size", "")),
        "angle": str(panel.get("angle", "")),
        "move": short(panel.get("move", ""), COPY_LIMITS["move"]),
        "lens_intent": short(panel.get("lens_intent", ""), COPY_LIMITS["lens_intent"]),
        "light": short(format_light(panel.get("light")), COPY_LIMITS["light"]),
        "duration": f"{panel['duration_s']:g} s",
        "transition_in": str(panel.get("transition_in", "cut")),
        "dialogue": short(panel.get("dialogue") or "", COPY_LIMITS["dialogue"]),
        "sound_cue": short(panel.get("sound_cue") or "", 80),
    }
    return {name: value for name, value in values.items() if value}


LABELS = {
    "id": "Panel",
    "shot": "Shot",
    "state": "State",
    "status": "Status",
    "framing": "Framing",
    "size": "Size",
    "angle": "Angle",
    "move": "Move",
    "lens_intent": "Lens",
    "light": "Light",
    "duration": "Time",
    "transition_in": "In",
    "dialogue": "Line",
    "sound_cue": "Sound",
}


def panel_fields_hash(panel: dict[str, Any]) -> str:
    return sha256_json(
        {"values": annotation_values(panel), "sha256": panel.get("sha256")}
    )


def page_groups(panels: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    return [
        panels[index : index + PANELS_PER_PAGE]
        for index in range(0, len(panels), PANELS_PER_PAGE)
    ] or [[]]


def relative_url(target: Path, start: Path) -> str:
    return Path(os.path.relpath(target, start)).as_posix()


def cut_points(panels: list[dict[str, Any]]) -> list[float]:
    cuts: list[float] = []
    elapsed = 0
    previous_shot = None
    for panel in panels:
        if previous_shot is not None and panel["shot"] != previous_shot:
            cuts.append(seconds(elapsed))
        elapsed += milliseconds(panel["duration_s"])
        previous_shot = panel["shot"]
    return cuts


def sheet_page_html(
    root: Path,
    html_directory: Path,
    board: dict[str, Any],
    panels: list[dict[str, Any]],
    page: int,
    pages: int,
    footer_text: str,
) -> tuple[str, list[tuple[str, str]]]:
    copies: list[tuple[str, str]] = []

    def text_element(tag: str, key: str, value: str, css: str) -> str:
        copies.append((key, value))
        return (
            f'<{tag} class="{css}" data-copy-key="{html.escape(key)}">'
            f"{html.escape(value)}</{tag}>"
        )

    number = int(board["scene"].split("-")[1])
    head = [
        text_element("h1", "scene-title", f"Scene {number} board", "title"),
        text_element(
            "p",
            "scene-meta",
            f"Level {board['level']} · {board['render_style']} · {board['status']}",
            "meta",
        ),
        text_element(
            "p",
            "plan-meta",
            f"Shot plan {board['shot_plan_sha256'][:12]}",
            "meta",
        ),
        text_element("p", "page-meta", f"Page {page} of {pages}", "meta"),
    ]
    cells: list[str] = []
    for panel in panels:
        if panel.get("file"):
            reference = relative_url(contained(root, panel["file"]), html_directory)
            picture = f'<img class="panel-image" src="{html.escape(reference)}" alt="">'
        else:
            picture = text_element(
                "div", f"panel-{panel['id']}-empty", "No panel yet", "panel-empty"
            )
        rows = []
        for name, value in annotation_values(panel).items():
            key = f"panel-{panel['id']}-{name}"
            copies.append((key, value))
            rows.append(
                f'<div class="row"><dt>{html.escape(LABELS[name])}</dt>'
                f'<dd data-copy-key="{html.escape(key)}">{html.escape(value)}</dd></div>'
            )
        cells.append(
            f'<article class="cell"><div class="frame">{picture}</div>'
            f'<dl class="strip">{"".join(rows)}</dl></article>'
        )
    foot = text_element("p", "scene-time", footer_text, "meta")
    document = (
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        f"<title>Scene {number} board page {page}</title>"
        '<link rel="stylesheet" href="sheet.css"></head><body>'
        f'<header>{"".join(head)}</header><main class="grid">{"".join(cells)}</main>'
        f"<footer>{foot}</footer></body></html>\n"
    )
    return document, copies


def render_arguments(
    html_path: Path,
    png_path: Path,
    copies: list[tuple[str, str]],
    root: Path,
    width: int,
    height: int,
    font: str | None,
) -> list[str]:
    arguments = [
        str(html_path),
        str(png_path),
        "--width",
        str(width),
        "--height",
        str(height),
        "--asset-root",
        str(root),
        "--record",
        str(png_path.with_suffix(".render.json")),
    ]
    for key, value in copies:
        arguments.extend(["--copy", f"{key}={value}"])
    if font:
        arguments.extend(["--require-local-font", font])
    return arguments


def footer_for(panels: list[dict[str, Any]]) -> str:
    total = sum(milliseconds(panel["duration_s"]) for panel in panels)
    cuts = ", ".join(f"{cut:g}" for cut in cut_points(panels))
    text = f"Running time {seconds(total):g} s"
    return short(f"{text} · cuts at {cuts} s" if cuts else text, 220)


def build_sheet(
    root: Path, scene: str, font: str | None, pages: list[int] | None = None
) -> dict[str, Any]:
    board, _ = read_board(root, scene)
    validate_new_board(board)
    panels = board["panels"]
    groups = page_groups(panels)
    wanted = pages or list(range(1, len(groups) + 1))
    bad = [page for page in wanted if page < 1 or page > len(groups)]
    if bad:
        raise BoardError(f"Pages {bad} are not in the board; it has {len(groups)}")
    directory = derived_directory(root, scene, "sheet")
    stylesheet = directory / "sheet.css"
    write_text_atomic(
        root, stylesheet, (TEMPLATE_DIR / "sheet.css").read_text(encoding="utf-8")
    )
    prefix = scene_prefix(scene)
    footer = footer_for(panels)
    output: list[dict[str, Any]] = []
    for number in wanted:
        stem = f"{prefix}_sheet_pg{number:02d}"
        version = next_version(directory, stem, ".html")
        name = f"{stem}_v{version:02d}"
        document, copies = sheet_page_html(
            root, directory, board, groups[number - 1], number, len(groups), footer
        )
        html_path = directory / f"{name}.html"
        write_text_atomic(root, html_path, document)
        png_path = directory / f"{name}.png"
        sidecar = {
            "kind": "sheet",
            "scene": scene,
            "page": number,
            "version": version,
            "html": relative_to(root, html_path),
            "png": relative_to(root, png_path),
            "stylesheet_sha256": sha256_file(stylesheet),
            "panels": {
                panel["id"]: panel_fields_hash(panel) for panel in groups[number - 1]
            },
            "bind_to_seedance": False,
            "render_arguments": render_arguments(
                html_path, png_path, copies, root, SHEET_WIDTH, SHEET_HEIGHT, font
            ),
        }
        sidecar_path = directory / f"{name}.sheet.json"
        write_json(root, sidecar_path, sidecar)
        output.append(
            {
                "page": number,
                "html": sidecar["html"],
                "png": sidecar["png"],
                "sidecar": relative_to(root, sidecar_path),
            }
        )
    return {"pages": output, "panels": len(panels)}


def latest_sidecars(directory: Path, kind: str) -> list[Path]:
    latest: dict[int, tuple[int, Path]] = {}
    for path in sorted(directory.glob(f"*.{kind}.json")):
        data = read_json(path)
        number, version = int(data.get("page", 1)), int(data["version"])
        if number not in latest or version > latest[number][0]:
            latest[number] = (version, path)
    return [latest[number][1] for number in sorted(latest)]


def run_renderer(renderer: Path, sidecar_path: Path) -> dict[str, Any]:
    sidecar = read_json(sidecar_path)
    command = [
        sys.executable,
        str(renderer),
        *sidecar["render_arguments"],
        "--overwrite",
    ]
    completed = subprocess.run(
        command, capture_output=True, text=True, check=False, timeout=300
    )
    lines = completed.stdout.strip().splitlines()
    if completed.returncode != 0 or not lines:
        raise BoardError(
            f"Renderer failed for {sidecar_path.name}: "
            f"{completed.stderr.strip() or completed.stdout.strip() or 'no output'}"
        )
    try:
        return json.loads(lines[-1])
    except ValueError as error:
        raise BoardError(f"Renderer printed no JSON for {sidecar_path.name}") from error


def render_sheet(
    root: Path, scene: str, renderer: str, pages: list[int] | None
) -> dict[str, Any]:
    renderer_path = Path(renderer).resolve()
    if not renderer_path.is_file():
        raise BoardError(f"Renderer not found: {renderer}")
    board, _ = read_board(root, scene)
    page_count = len(page_groups(board["panels"]))
    bad = [page for page in pages or [] if page < 1 or page > page_count]
    if bad:
        raise BoardError(f"Pages {bad} are not in the board; it has {page_count}")
    directory = derived_path(root, scene, "sheet")
    rendered: list[dict[str, Any]] = []
    sidecars = latest_sidecars(directory, "sheet") if directory.is_dir() else []
    for sidecar_path in sidecars:
        sidecar = read_json(sidecar_path)
        if sidecar["page"] > page_count or (pages and sidecar["page"] not in pages):
            continue
        run_renderer(renderer_path, sidecar_path)
        rendered.append({"page": sidecar["page"], "png": sidecar["png"]})
    if not rendered:
        raise BoardError("No sheet pages to render; run sheet first")
    return {"rendered": rendered}


def overview_html(board: dict[str, Any]) -> tuple[str, list[tuple[str, str]]]:
    layout = board["layout"]
    room = layout["room"]
    unit = room.get("unit", "m")
    scale = 600 / max(room["width"], room["depth"])
    width = max(1, round(room["width"] * scale))
    depth = max(1, round(room["depth"] * scale))

    def x(value: float) -> float:
        return round(value * scale, 1)

    shapes = [f'<rect x="0" y="0" width="{width}" height="{depth}" class="room"/>']
    axis = layout.get("axis")
    if axis:
        shapes.append(
            f'<line x1="{x(axis["from"][0])}" y1="{x(axis["from"][1])}" '
            f'x2="{x(axis["to"][0])}" y2="{x(axis["to"][1])}" class="axis"/>'
        )
    for light in layout.get("lights", []):
        shapes.append(
            f'<circle cx="{x(light["at"][0])}" cy="{x(light["at"][1])}" r="9" class="light"/>'
            f'<text x="{x(light["at"][0]) + 14}" y="{x(light["at"][1]) + 5}" class="mark">'
            f"{html.escape(str(light['id']))}</text>"
        )
    for figure in layout.get("figures", []):
        shapes.append(
            f'<circle cx="{x(figure["at"][0])}" cy="{x(figure["at"][1])}" r="14" class="figure"/>'
            f'<text x="{x(figure["at"][0])}" y="{x(figure["at"][1]) + 6}" class="letter">'
            f"{html.escape(str(figure['id']))}</text>"
        )
    copies: list[tuple[str, str]] = []
    rows: list[str] = []

    def row(key: str, kind: str, text: str) -> None:
        copies.append((key, text))
        rows.append(
            f'<li><span class="kind">{html.escape(kind)}</span> '
            f'<span data-copy-key="{html.escape(key)}">{html.escape(text)}</span></li>'
        )

    if axis:
        row("axis", "Axis", axis.get("note") or "Camera stays on one side of the axis")
    for light in layout.get("lights", []):
        detail = ", ".join(
            part
            for part in (light.get("direction"), light.get("switched_on_by"))
            if part
        )
        row(
            f"light-{light['id']}",
            "Light",
            f"{light['id']}: {detail}" if detail else str(light["id"]),
        )
    for figure in layout.get("figures", []):
        row(f"figure-{figure['id']}", "Figure", f"{figure['id']}: {figure['label']}")
    number = int(board["scene"].split("-")[1])
    title = f"Scene {number} floor plan, {room['width']:g} × {room['depth']:g} {unit}"
    copies.append(("overview-title", title))
    document = (
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        f"<title>Scene {number} overview</title>"
        '<link rel="stylesheet" href="overview.css"></head><body>'
        f'<h1 data-copy-key="overview-title">{html.escape(title)}</h1>'
        f'<svg viewBox="0 0 {width} {depth}" width="{width * 1.5:g}" height="{depth * 1.5:g}" '
        f'xmlns="http://www.w3.org/2000/svg">{"".join(shapes)}</svg>'
        f'<ul class="legend">{"".join(rows)}</ul></body></html>\n'
    )
    return document, copies


def build_overview(root: Path, scene: str) -> dict[str, Any]:
    board, _ = read_board(root, scene)
    if "layout" not in board:
        return {"skipped": "board.md has no layout block"}
    directory = derived_directory(root, scene, "overview")
    stylesheet = directory / "overview.css"
    write_text_atomic(
        root, stylesheet, (TEMPLATE_DIR / "overview.css").read_text(encoding="utf-8")
    )
    stem = f"{scene_prefix(scene)}_overview"
    version = next_version(directory, stem, ".html")
    html_path = directory / f"{stem}_v{version:02d}.html"
    document, copies = overview_html(board)
    write_text_atomic(root, html_path, document)
    png_path = html_path.with_suffix(".png")
    sidecar = {
        "kind": "overview",
        "scene": scene,
        "page": 1,
        "version": version,
        "html": relative_to(root, html_path),
        "png": relative_to(root, png_path),
        "layout_sha256": sha256_json(board["layout"]),
        "bind_to_seedance": False,
        "render_arguments": render_arguments(
            html_path, png_path, copies, root, 1920, 1080, None
        ),
    }
    sidecar_path = html_path.with_suffix(".overview.json")
    write_json(root, sidecar_path, sidecar)
    return {
        "html": sidecar["html"],
        "png": sidecar["png"],
        "sidecar": relative_to(root, sidecar_path),
    }


def ffmpeg_binary() -> str:
    found = shutil.which("ffmpeg")
    if not found:
        raise BoardError("ffmpeg is required to build the animatic")
    return found


def default_animatic_size(aspect: str) -> str:
    width, height = (int(part) for part in aspect.split(":"))
    if width >= height:
        return f"1920x{round(1920 * height / width / 2) * 2}"
    return f"{round(1920 * width / height / 2) * 2}x1920"


def build_animatic(
    root: Path, scene: str, size: str | None, audio: str | None
) -> dict[str, Any]:
    board, _ = read_board(root, scene)
    size = size or default_animatic_size(board["aspect_ratio"])
    if not re.fullmatch(r"\d{3,4}x\d{3,4}", size):
        raise BoardError("Size must look like 1920x1080")
    segments: list[dict[str, Any]] = []
    for panel in board["panels"]:
        if not panel.get("file"):
            raise BoardError(f"{panel['id']} has no registered panel file")
        path = contained(root, panel["file"])
        if not path.is_file():
            raise BoardError(f"{panel['id']} file not found: {panel['file']}")
        if any(character in str(path) for character in "'\n\r\\"):
            raise BoardError(
                f"Panel path has a character the concat list cannot hold: {path.name}"
            )
        segments.append(
            {
                "panel": panel["id"],
                "file": panel["file"],
                "sha256": sha256_file(path),
                "duration_ms": milliseconds(panel["duration_s"]),
            }
        )
    if not segments:
        raise BoardError("The board has no panels")
    audio_path: Path | None = None
    if audio:
        audio_path = contained(root, audio)
        if not audio_path.is_file():
            raise BoardError(f"Audio not found: {audio}")
    directory = derived_directory(root, scene, "animatic")
    stem = f"{scene_prefix(scene)}_animatic"
    version = next_version(directory, stem, ".mp4")
    output = directory / f"{stem}_v{version:02d}.mp4"
    if output.is_symlink():
        raise BoardError("Refusing to write through a symlink")
    total_ms = sum(segment["duration_ms"] for segment in segments)
    width, height = size.split("x")
    lines: list[str] = []
    for segment in segments:
        lines.append(f"file '{contained(root, segment['file'])}'")
        lines.append(f"duration {segment['duration_ms'] / 1000:.3f}")
    lines.append(f"file '{contained(root, segments[-1]['file'])}'")
    video_filter = (
        f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,format=yuv420p"
    )
    with tempfile.TemporaryDirectory(prefix="scene-board-animatic-") as temporary:
        listing = Path(temporary) / "segments.txt"
        listing.write_text("\n".join(lines) + "\n", encoding="utf-8")
        command = [
            ffmpeg_binary(),
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(listing),
        ]
        if audio_path:
            command.extend(
                [
                    "-i",
                    str(audio_path),
                    "-map",
                    "0:v",
                    "-map",
                    "1:a",
                    "-af",
                    "apad",
                    "-c:a",
                    "aac",
                ]
            )
        command.extend(
            [
                "-vf",
                video_filter,
                "-r",
                "24",
                "-t",
                f"{total_ms / 1000:.3f}",
                "-c:v",
                "libx264",
                "-crf",
                "18",
                "-movflags",
                "+faststart",
                str(output),
            ]
        )
        completed = subprocess.run(
            command, capture_output=True, text=True, check=False, timeout=600
        )
    if completed.returncode != 0:
        raise BoardError(f"ffmpeg failed: {completed.stderr.strip()}")
    record = {
        "kind": "animatic",
        "scene": scene,
        "version": version,
        "file": relative_to(root, output),
        "sha256": sha256_file(output),
        "size": size,
        "duration_ms": total_ms,
        "segments": segments,
        "audio": relative_to(root, audio_path) if audio_path else None,
        "audio_sha256": sha256_file(audio_path) if audio_path else None,
        "bind_to_seedance": False,
    }
    record_path = output.with_suffix(".animatic.json")
    write_json(root, record_path, record)
    return {
        "file": record["file"],
        "duration_s": total_ms / 1000,
        "segments": len(segments),
        "record": relative_to(root, record_path),
    }


def latest_record(directory: Path, pattern: str) -> Path | None:
    candidates = sorted(directory.glob(pattern)) if directory.is_dir() else []
    return candidates[-1] if candidates else None


def sheet_status(
    root: Path, scene: str, board: dict[str, Any], plan_stale: bool
) -> list[dict[str, Any]]:
    expected = page_groups(board["panels"])
    directory = derived_path(root, scene, "sheet")
    sidecars = latest_sidecars(directory, "sheet") if directory.is_dir() else []
    recorded = {read_json(path)["page"]: path for path in sidecars}
    stale: list[dict[str, Any]] = []
    for number, group in enumerate(expected, start=1):
        if number not in recorded:
            stale.append({"page": number, "reason": "page has not been built"})
            continue
        data = read_json(recorded[number])
        if not contained(root, data["png"]).is_file():
            stale.append({"page": number, "reason": "page is built but not rendered"})
            continue
        current = {panel["id"]: panel_fields_hash(panel) for panel in group}
        changed = sorted(
            panel_id
            for panel_id in set(current) | set(data["panels"])
            if current.get(panel_id) != data["panels"].get(panel_id)
        )
        if changed:
            stale.append(
                {"page": number, "reason": "panels changed", "panels": changed}
            )
        elif plan_stale:
            stale.append({"page": number, "reason": "shot plan changed"})
    for number in sorted(set(recorded) - set(range(1, len(expected) + 1))):
        stale.append({"page": number, "reason": "page no longer exists"})
    return stale


def animatic_status(
    root: Path, scene: str, board: dict[str, Any], plan_stale: bool
) -> dict[str, Any]:
    record_path = latest_record(
        derived_path(root, scene, "animatic"), "*.animatic.json"
    )
    if not record_path:
        return {"state": "not built"}
    record = read_json(record_path)
    current = {
        panel["id"]: (panel.get("sha256"), milliseconds(panel["duration_s"]))
        for panel in board["panels"]
    }
    recorded = {
        segment["panel"]: (segment["sha256"], segment["duration_ms"])
        for segment in record["segments"]
    }
    changed = sorted(
        panel_id
        for panel_id in set(current) | set(recorded)
        if current.get(panel_id) != recorded.get(panel_id)
    )
    audio_changed = False
    if record.get("audio"):
        audio_file = contained(root, record["audio"])
        audio_changed = not audio_file.is_file() or sha256_file(
            audio_file
        ) != record.get("audio_sha256")
    stale = bool(changed) or audio_changed or plan_stale
    report: dict[str, Any] = {
        "state": "stale" if stale else "current",
        "panels": changed,
    }
    if audio_changed:
        report["audio"] = "changed"
    if plan_stale:
        report["reason"] = "shot plan changed"
    return report


def overview_status(root: Path, scene: str, board: dict[str, Any]) -> dict[str, Any]:
    if "layout" not in board:
        return {"state": "no layout"}
    path = latest_record(derived_path(root, scene, "overview"), "*.overview.json")
    if not path:
        return {"state": "not built"}
    current = read_json(path)["layout_sha256"] == sha256_json(board["layout"])
    return {"state": "current" if current else "stale"}


def status_report(root: Path, scene: str) -> dict[str, Any]:
    board, _ = read_board(root, scene)
    plan_stale = board["shot_plan_sha256"] != load_scene_source(root, scene).plan_sha256
    return {
        "scene": scene,
        "level": board["level"],
        "plan_stale": plan_stale,
        "panels": {panel["id"]: panel["status"] for panel in board["panels"]},
        "stale_sheet_pages": sheet_status(root, scene, board, plan_stale),
        "animatic": animatic_status(root, scene, board, plan_stale),
        "overview": overview_status(root, scene, board),
    }


def prior_failed_edits(panel: dict[str, Any], dimension: str) -> int:
    failed = 0
    for version in reversed(panel.get("versions") or []):
        if version["operation"] == "generate":
            break
        if version.get("dimension") != dimension:
            continue
        is_current = version["file"] == panel.get("file")
        if version.get("rejected") or (
            is_current and panel.get("status") in {"needs_edit", "rejected"}
        ):
            failed += 1
    return failed


def revision_contract(
    panel: dict[str, Any],
    dimension: str,
    delta: str,
    accept: list[str],
    bbox: str | None,
    rejected: list[str],
) -> str:
    locked = [
        f"{name}: {format_light(panel[name]) if name == 'light' else panel[name]}"
        for name in (
            "size",
            "angle",
            "framing",
            "move",
            "lens_intent",
            "light",
            "screen_direction",
        )
        if panel.get(name)
    ]
    for name in ("featured", "continuity_carry"):
        if panel.get(name):
            locked.append(f"{name}: {', '.join(panel[name])}")
    lines = [
        f"# Revision contract: {panel['id']}",
        "",
        "Planning artifact: bind_to_seedance is false.",
        "",
        f"Failed dimension: {dimension}",
        f"Requested delta: {delta}",
        f"Region: {'bounding box ' + bbox if bbox else 'whole image'}",
        "",
        "## Locked decisions",
        "",
        *[f"- {item}" for item in locked],
        "- every unmarked subject, prop and the background geometry",
        "",
        "## Acceptance criteria",
        "",
        *[f"- {item}" for item in accept],
        "",
        "## Known rejections",
        "",
        *([f"- {item}" for item in rejected] or ["- none recorded"]),
        "",
        "## Edit request",
        "",
        "```text",
        "References:",
        "@Image 1: base storyboard panel to edit",
        "@Image 2: approved element sheet for the corrected subject (when identity or a prop changes)",
        "",
        "Task:",
        "Image Editing — local storyboard correction",
        "",
        "Edit instructions:",
        f"In @Image 1, {delta}. Preserve the camera, composition, pose, screen direction,",
        "background geometry, lighting, line style and all unmarked subjects and props.",
        "",
        "Constraints:",
        "No new subjects, no wardrobe change, no background redesign, no text, no",
        "watermark, and no changes outside the target region.",
        "```",
        "",
        "The edit saves a new version number of the same panel; register it with",
        "`scene_board.py register-panel --edit-of <previous file>`.",
        "",
    ]
    return "\n".join(lines)


def next_panel_version(panel: dict[str, Any]) -> str:
    match = PANEL_FILE.match(Path(str(panel.get("file", ""))).name)
    if not match:
        return ""
    return f"{match.group(1)}_t{match.group(2)}_v{int(match.group(3)) + 1:02d}.png"


def plan_repair(
    root: Path,
    scene: str,
    panel_ids: list[str],
    cause: str,
    dimension: str,
    delta: str,
    accept: list[str],
    bbox: str | None,
) -> dict[str, Any]:
    ordered = list(dict.fromkeys(panel_ids))
    if not ordered:
        raise BoardError("Name at least one panel")
    if cause not in {"local", "beat", "shared"}:
        raise BoardError("Cause must be local, beat or shared")
    if bbox:
        parse_bbox(bbox)
    board, _ = read_board(root, scene)
    by_shot: dict[str, list[dict[str, Any]]] = {}
    for panel in board["panels"]:
        by_shot.setdefault(panel["shot"], []).append(panel)
    failed = [find_panel(board, panel_id) for panel_id in ordered]
    failed_by_shot: dict[str, list[str]] = {}
    for panel in failed:
        failed_by_shot.setdefault(panel["shot"], []).append(panel["id"])
    actions: list[dict[str, Any]] = []
    regenerate_shots: set[str] = set()
    for shot_id, ids in sorted(failed_by_shot.items()):
        siblings = by_shot[shot_id]
        if cause == "shared":
            reason = "shared cause: fix the element sheet, shot plan or prompt first"
        elif len(siblings) >= 3 and len(ids) * 2 > len(siblings):
            reason = "most panels of the shot failed"
        else:
            continue
        regenerate_shots.add(shot_id)
        actions.append(
            {
                "action": "regenerate_shot",
                "shot": shot_id,
                "panels": [panel["id"] for panel in siblings],
                "reason": reason,
            }
        )
    edits: list[tuple[dict[str, Any], list[str]]] = []
    for panel in failed:
        if panel["shot"] in regenerate_shots:
            continue
        if cause == "beat":
            actions.append(
                {
                    "action": "regenerate_panel",
                    "panel": panel["id"],
                    "reason": "wrong beat, geography or axis is structural",
                }
            )
            continue
        if not dimension.strip():
            raise BoardError(
                "An edit needs --dimension naming the one failed dimension"
            )
        if prior_failed_edits(panel, dimension) >= TWO_EDIT_LIMIT:
            actions.append(
                {
                    "action": "regenerate_panel",
                    "panel": panel["id"],
                    "reason": f"two edits on '{dimension}' already failed",
                }
            )
            continue
        if not panel.get("file"):
            raise BoardError(f"{panel['id']} has no registered file to edit")
        if not delta.strip() or not accept:
            raise BoardError(
                "An edit needs --delta and at least one --accept criterion"
            )
        rejected = [
            f"{version['file']} (sha256 {version['sha256'][:12]})"
            for version in panel.get("versions") or []
            if version.get("rejected")
        ]
        edits.append((panel, rejected))
    if edits:
        directory = derived_directory(root, scene, "repair")
        for panel, rejected in edits:
            number = next_version(directory, f"{panel['id']}_edit", ".md")
            contract_path = directory / f"{panel['id']}_edit_v{number:02d}.md"
            write_text_atomic(
                root,
                contract_path,
                revision_contract(
                    panel, dimension, delta.strip(), accept, bbox, rejected
                ),
            )
            actions.append(
                {
                    "action": "edit",
                    "panel": panel["id"],
                    "file": panel["file"],
                    "contract": relative_to(root, contract_path),
                    "tool": "seedream_edit_image",
                    "needs_https_url": True,
                    "next_version": next_panel_version(panel),
                }
            )
    affected = {panel["id"] for panel in failed}
    for shot_id in regenerate_shots:
        affected.update(panel["id"] for panel in by_shot[shot_id])
    return {
        "actions": actions,
        "untouched_panels": sorted(
            {panel["id"] for panel in board["panels"]} - affected
        ),
        "stale": stale_for(board, affected),
    }


def stale_for(board: dict[str, Any], affected: set[str]) -> dict[str, Any]:
    pages = sorted(
        {
            index // PANELS_PER_PAGE + 1
            for index, panel in enumerate(board["panels"])
            if panel["id"] in affected
        }
    )
    return {
        "sheet_pages": pages,
        "animatic_segments": sorted(affected),
        "overview": False,
    }


def build_review_page(root: Path, scene: str) -> dict[str, Any]:
    board, _ = read_board(root, scene)
    review_directory = safe_directory(root, "review")
    stylesheet = review_directory / "scene-board.css"
    write_text_atomic(
        root, stylesheet, (TEMPLATE_DIR / "review.css").read_text(encoding="utf-8")
    )
    page_path = review_directory / f"{scene}-board.html"
    status = status_report(root, scene)
    pieces: list[str] = []
    sheet_dir = derived_path(root, scene, "sheet")
    for path in latest_sidecars(sheet_dir, "sheet") if sheet_dir.is_dir() else []:
        data = read_json(path)
        png = contained(root, data["png"])
        heading = f"Sheet page {int(data['page'])} (v{int(data['version']):02d})"
        if png.is_file():
            pieces.append(
                f"<section><h2>{html.escape(heading)}</h2>"
                f'<img src="{html.escape(relative_url(png, review_directory))}" alt="{html.escape(heading)}">'
                f'<p class="hash">sha256 {sha256_file(png)}</p></section>'
            )
        else:
            pieces.append(
                f'<section><h2>{html.escape(heading)}</h2><p class="warn">Not rendered yet.</p></section>'
            )
    overview_path = latest_record(
        derived_path(root, scene, "overview"), "*.overview.json"
    )
    if overview_path:
        png = contained(root, read_json(overview_path)["png"])
        if png.is_file():
            pieces.append(
                f'<section><h2>Overview</h2><img src="{html.escape(relative_url(png, review_directory))}" alt="Overview"></section>'
            )
    animatic_path = latest_record(
        derived_path(root, scene, "animatic"), "*.animatic.json"
    )
    if animatic_path:
        data = read_json(animatic_path)
        video = contained(root, data["file"])
        if video.is_file():
            pieces.append(
                f"<section><h2>Animatic ({int(data['duration_ms']) / 1000:g} s)</h2>"
                f'<video controls src="{html.escape(relative_url(video, review_directory))}"></video>'
                f'<p class="hash">sha256 {html.escape(str(data["sha256"]))}</p></section>'
            )
    rows = "".join(
        f"<tr><td>{html.escape(panel['id'])}</td><td>{html.escape(panel['state'])}</td>"
        f"<td>{html.escape(panel['status'])}</td></tr>"
        for panel in board["panels"]
    )
    notes = ""
    if status["plan_stale"]:
        notes += (
            '<p class="warn">The shot plan changed after this board was derived.</p>'
        )
    if status["stale_sheet_pages"]:
        pages = ", ".join(str(item["page"]) for item in status["stale_sheet_pages"])
        notes += (
            f'<p class="warn">Stale or unrendered sheet pages: {html.escape(pages)}</p>'
        )
    number = int(scene.split("-")[1])
    document = (
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        f"<title>Scene {number} board review</title>"
        '<link rel="stylesheet" href="scene-board.css"></head><body>'
        f"<h1>Scene {number} board review</h1>"
        f"<p>Level {html.escape(board['level'])} · {html.escape(board['render_style'])} · "
        "planning artifact, never a Seedance reference · this page is a visual aid and decides nothing.</p>"
        f"{notes}<table><thead><tr><th>Panel</th><th>State</th><th>Status</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>{''.join(pieces)}</body></html>\n"
    )
    write_text_atomic(root, page_path, document)
    return {"page": relative_to(root, page_path)}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scene board records, sheets, animatic and panel repair planning"
    )
    commands = parser.add_subparsers(dest="command", required=True)

    def common(name: str, help_text: str) -> argparse.ArgumentParser:
        command = commands.add_parser(name, help=help_text)
        command.add_argument("project")
        command.add_argument("scene")
        return command

    init = common("init", "Derive board.md from the scene's shot plan")
    init.add_argument("--level", choices=LEVELS, default=DEFAULT_LEVEL)
    init.add_argument("--level-reason", default="default level for a standard scene")
    init.add_argument(
        "--override", action="append", default=[], help="SHOT=LEVEL=REASON"
    )
    init.add_argument("--style", default="pencil", choices=STYLES)
    init.add_argument("--aspect", default="16:9")
    init.add_argument("--overwrite", action="store_true")
    common("rebase-plan", "Follow a changed shot plan and keep registered panels")
    common("check", "Validate the board against the schema and the shot plan")
    common("status", "Show panel states and stale derived artifacts")
    register = common("register-panel", "Record a generated or edited panel file")
    register.add_argument("panel")
    register.add_argument("--file", required=True)
    register.add_argument("--edit-of")
    register.add_argument("--dimension")
    register.add_argument("--bbox")
    register.add_argument("--prompt-file")
    register.add_argument("--task-id")
    mark = common("mark", "Set a panel status")
    mark.add_argument("panel")
    mark.add_argument(
        "--status",
        required=True,
        choices=["review", "needs_edit", "rejected", "approved"],
    )
    mark.add_argument("--decision")
    repair = common(
        "repair-plan", "Choose the repair scope and write revision contracts"
    )
    repair.add_argument("--panels", required=True)
    repair.add_argument("--cause", default="local", choices=["local", "beat", "shared"])
    repair.add_argument("--dimension", default="")
    repair.add_argument("--delta", default="")
    repair.add_argument("--accept", action="append", default=[])
    repair.add_argument("--bbox")
    sheet = common("sheet", "Write sheet page sources and render plans")
    sheet.add_argument("--font", help="Declared local font family to require")
    sheet.add_argument("--pages", help="Comma-separated page numbers to write")
    render = common(
        "render-sheet", "Render sheet pages with a renderer script you name"
    )
    render.add_argument("--renderer", required=True)
    render.add_argument("--pages", help="Comma-separated page numbers")
    common("overview", "Write the floor plan sources from the layout block")
    animatic = common("animatic", "Build the timed review animatic with FFmpeg")
    animatic.add_argument("--size", help="WxH; default follows the board aspect ratio")
    animatic.add_argument("--audio")
    common("review-page", "Write the static review page")
    return parser


def parse_pages(value: str | None) -> list[int] | None:
    if not value:
        return None
    try:
        return sorted({int(item) for item in value.split(",") if item.strip()})
    except ValueError as error:
        raise BoardError("Pages must be comma-separated integers") from error


def execute(arguments: argparse.Namespace) -> tuple[dict[str, Any], int]:
    root = project_root(arguments.project)
    scene = normalize_scene(arguments.scene)
    command = arguments.command
    if command == "init":
        return (
            init_board(
                root,
                scene,
                arguments.level,
                arguments.level_reason,
                arguments.override,
                arguments.style,
                arguments.aspect,
                arguments.overwrite,
            ),
            0,
        )
    if command == "rebase-plan":
        return rebase_plan(root, scene), 0
    if command == "check":
        findings = check_board(root, scene)
        errors = [item for item in findings if item.severity == "error"]
        return {
            "ok": not errors,
            "findings": [item.as_dict() for item in findings],
        }, 1 if errors else 0
    if command == "status":
        return status_report(root, scene), 0
    if command == "register-panel":
        return (
            register_panel(
                root,
                scene,
                arguments.panel,
                arguments.file,
                arguments.edit_of,
                arguments.dimension,
                arguments.bbox,
                arguments.prompt_file,
                arguments.task_id,
            ),
            0,
        )
    if command == "mark":
        return mark_panel(
            root, scene, arguments.panel, arguments.status, arguments.decision
        ), 0
    if command == "repair-plan":
        ids = [item.strip() for item in arguments.panels.split(",") if item.strip()]
        return (
            plan_repair(
                root,
                scene,
                ids,
                arguments.cause,
                arguments.dimension,
                arguments.delta,
                arguments.accept,
                arguments.bbox,
            ),
            0,
        )
    if command == "sheet":
        return build_sheet(root, scene, arguments.font, parse_pages(arguments.pages)), 0
    if command == "render-sheet":
        return (
            render_sheet(root, scene, arguments.renderer, parse_pages(arguments.pages)),
            0,
        )
    if command == "overview":
        return build_overview(root, scene), 0
    if command == "animatic":
        return build_animatic(root, scene, arguments.size, arguments.audio), 0
    return build_review_page(root, scene), 0


def main() -> int:
    try:
        result, code = execute(build_parser().parse_args())
    except (BoardError, OSError, ValueError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        return 2
    except (KeyError, TypeError, IndexError, AttributeError) as error:
        print(f"Malformed record: {error!r}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
