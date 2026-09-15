from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = SKILL_ROOT / "references/blockout-manifest.schema.json"


@dataclass(frozen=True)
class Finding:
    rule_id: str
    path: str
    message: str


def finite_number(value: Any) -> float | None:
    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not math.isfinite(value)
    ):
        return None
    return float(value)


def schema_findings(value: Any) -> list[Finding]:
    schema = json.loads(SCHEMA_PATH.read_text())
    Draft202012Validator.check_schema(schema)
    return [
        Finding(
            "blockout.schema",
            ".".join(map(str, error.absolute_path)),
            error.message,
        )
        for error in Draft202012Validator(schema).iter_errors(value)
    ]


def valid_relative_path(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip() or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def duplicate_values(items: Any, field: str) -> set[str]:
    if not isinstance(items, list):
        return set()
    values: list[str] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        value = item.get(field)
        if isinstance(value, str):
            values.append(value)
    return {value for value in values if values.count(value) > 1}


def validate_timeline(value: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    timeline = value.get("timeline")
    if not isinstance(timeline, dict):
        return findings
    fps = finite_number(timeline.get("fps"))
    fps_base = finite_number(timeline.get("fps_base"))
    frame_start = timeline.get("frame_start")
    frame_end = timeline.get("frame_end")
    duration = finite_number(timeline.get("duration_seconds"))
    if fps is None or fps_base is None or fps_base <= 0:
        return findings
    effective_fps = fps / fps_base
    if abs(effective_fps - 24.0) > 1e-6:
        findings.append(
            Finding(
                "previz.timeline",
                "timeline.fps",
                "The Seedance previz master must have an effective frame rate of 24 fps",
            )
        )
    if (
        isinstance(frame_start, int)
        and not isinstance(frame_start, bool)
        and isinstance(frame_end, int)
        and not isinstance(frame_end, bool)
        and duration is not None
    ):
        if frame_end < frame_start:
            findings.append(
                Finding(
                    "previz.timeline",
                    "timeline.frame_end",
                    "Frame end must not precede frame start",
                )
            )
        else:
            measured = (frame_end - frame_start + 1) / effective_fps
            if abs(measured - duration) > 0.05:
                findings.append(
                    Finding(
                        "previz.timeline",
                        "timeline.duration_seconds",
                        "Duration must equal inclusive frame count divided by effective fps",
                    )
                )
    return findings


def validate_render(value: dict[str, Any]) -> list[Finding]:
    render = value.get("render")
    if not isinstance(render, dict):
        return []
    expected = {
        "width": 1920,
        "height": 1080,
        "resolution_percentage": 100,
        "container": "MPEG4",
        "codec": "H264",
    }
    return [
        Finding(
            "previz.render",
            f"render.{field}",
            f"Expected {field}={expected_value!r} for the Seedance previz master",
        )
        for field, expected_value in expected.items()
        if render.get(field) != expected_value
    ]


def validate_paths(value: dict[str, Any]) -> list[Finding]:
    paths = {
        "source.blend_path": (
            value.get("source", {}).get("blend_path")
            if isinstance(value.get("source"), dict)
            else None
        ),
        "render.previz_path": (
            value.get("render", {}).get("previz_path")
            if isinstance(value.get("render"), dict)
            else None
        ),
    }
    conditioning = value.get("conditioning")
    if isinstance(conditioning, dict) and not conditioning.get("control_only", True):
        paths["conditioning.selection_manifest"] = conditioning.get(
            "selection_manifest"
        )
    return [
        Finding(
            "blockout.paths",
            path,
            "Paths must be nonempty project-relative POSIX paths without parent traversal",
        )
        for path, candidate in paths.items()
        if not valid_relative_path(candidate)
    ]


def validate_subjects(value: dict[str, Any]) -> list[Finding]:
    subjects = value.get("subjects")
    duplicates = duplicate_values(subjects, "id") | duplicate_values(
        subjects, "object_name"
    )
    if not duplicates:
        return []
    return [
        Finding(
            "blockout.subjects",
            "subjects",
            f"Subject IDs and Blender object names must be unique: {', '.join(sorted(duplicates))}",
        )
    ]


def validate_cuts(value: dict[str, Any]) -> list[Finding]:
    cuts = value.get("cuts")
    cameras = value.get("cameras")
    timeline = value.get("timeline")
    if (
        not isinstance(cuts, list)
        or not isinstance(cameras, list)
        or not isinstance(timeline, dict)
    ):
        return []
    findings: list[Finding] = []
    camera_ids = {
        camera.get("id")
        for camera in cameras
        if isinstance(camera, dict) and isinstance(camera.get("id"), str)
    }
    if duplicate_values(cameras, "id") or duplicate_values(cameras, "object_name"):
        findings.append(
            Finding(
                "blockout.cuts",
                "cameras",
                "Camera IDs and Blender object names must be unique",
            )
        )
    valid_cuts = [cut for cut in cuts if isinstance(cut, dict)]
    frames = [cut.get("frame") for cut in valid_cuts]
    integer_frames = [
        frame
        for frame in frames
        if isinstance(frame, int) and not isinstance(frame, bool)
    ]
    frame_start = timeline.get("frame_start")
    frame_end = timeline.get("frame_end")
    if integer_frames and integer_frames[0] != frame_start:
        findings.append(
            Finding(
                "blockout.cuts",
                "cuts.0.frame",
                "The first camera assignment must begin at frame_start",
            )
        )
    if integer_frames != sorted(integer_frames) or len(integer_frames) != len(
        set(integer_frames)
    ):
        findings.append(
            Finding(
                "blockout.cuts",
                "cuts",
                "Cut frames must be strictly increasing and unique",
            )
        )
    for position, cut in enumerate(valid_cuts):
        frame = cut.get("frame")
        if cut.get("camera") not in camera_ids:
            findings.append(
                Finding(
                    "blockout.cuts",
                    f"cuts.{position}.camera",
                    "Cut references an unknown camera",
                )
            )
        if (
            isinstance(frame, int)
            and isinstance(frame_start, int)
            and isinstance(frame_end, int)
            and not frame_start <= frame <= frame_end
        ):
            findings.append(
                Finding(
                    "blockout.cuts",
                    f"cuts.{position}.frame",
                    "Cut frame falls outside the timeline",
                )
            )
    return findings


def motion_expectation_error(check: dict[str, Any]) -> str | None:
    check_type = check.get("type")
    target = check.get("target")
    expectation = check.get("expectation")
    if not isinstance(expectation, dict):
        return None
    if check_type == "world_displacement" and not (
        expectation.get("axis") in {"X", "Y", "Z"}
        and expectation.get("direction") in {"positive", "negative"}
        and finite_number(expectation.get("minimum_delta")) not in (None, 0.0)
    ):
        return "world_displacement requires axis, direction, and positive minimum_delta"
    if check_type == "distance_trend" and not (
        isinstance(target, str)
        and expectation.get("trend") in {"decreasing", "increasing", "stable"}
    ):
        return "distance_trend requires target and trend"
    if check_type == "ground_contact" and not (
        isinstance(target, str)
        and finite_number(expectation.get("maximum_gap")) is not None
    ):
        return "ground_contact requires target and nonnegative maximum_gap"
    if check_type == "rotation_from_travel" and not (
        isinstance(target, str)
        and finite_number(expectation.get("minimum_revolutions")) not in (None, 0.0)
    ):
        return "rotation_from_travel requires target and positive minimum_revolutions"
    if check_type == "screen_occupancy":
        minimum = finite_number(expectation.get("minimum_fraction"))
        maximum = finite_number(expectation.get("maximum_fraction"))
        if minimum is None or maximum is None or minimum > maximum:
            return "screen_occupancy requires ordered minimum_fraction and maximum_fraction"
    if check_type == "end_state" and not isinstance(
        expectation.get("terminal_relation"), str
    ):
        return "end_state requires terminal_relation"
    return None


def validate_motion(value: dict[str, Any]) -> list[Finding]:
    checks = value.get("motion_checks")
    subjects = value.get("subjects")
    timeline = value.get("timeline")
    if (
        not isinstance(checks, list)
        or not isinstance(subjects, list)
        or not isinstance(timeline, dict)
    ):
        return []
    findings: list[Finding] = []
    subject_ids = {
        subject.get("id")
        for subject in subjects
        if isinstance(subject, dict) and isinstance(subject.get("id"), str)
    }
    if duplicate_values(checks, "id"):
        findings.append(
            Finding(
                "blockout.motion",
                "motion_checks",
                "Motion-check IDs must be unique",
            )
        )
    frame_start = timeline.get("frame_start")
    frame_end = timeline.get("frame_end")
    for position, check in enumerate(checks):
        if not isinstance(check, dict):
            continue
        path = f"motion_checks.{position}"
        if check.get("subject") not in subject_ids:
            findings.append(
                Finding(
                    "blockout.motion",
                    f"{path}.subject",
                    "Motion check references an unknown subject",
                )
            )
        target = check.get("target")
        if target is not None and target not in subject_ids:
            findings.append(
                Finding(
                    "blockout.motion",
                    f"{path}.target",
                    "Motion check references an unknown target",
                )
            )
        start = check.get("start_frame")
        end = check.get("end_frame")
        if (
            isinstance(start, int)
            and isinstance(end, int)
            and isinstance(frame_start, int)
            and isinstance(frame_end, int)
            and not (frame_start <= start <= end <= frame_end)
        ):
            findings.append(
                Finding(
                    "blockout.motion",
                    path,
                    "Motion-check frame window must stay inside the timeline",
                )
            )
        expectation_error = motion_expectation_error(check)
        if expectation_error:
            findings.append(
                Finding(
                    "blockout.motion",
                    f"{path}.expectation",
                    expectation_error,
                )
            )
    return findings


def validate_conditioning(value: dict[str, Any]) -> list[Finding]:
    conditioning = value.get("conditioning")
    render = value.get("render")
    if (
        not isinstance(conditioning, dict)
        or conditioning.get("control_only", True)
        or not isinstance(render, dict)
    ):
        return []
    if conditioning.get("selected_previz_sha256") == render.get("previz_sha256"):
        return []
    return [
        Finding(
            "conditioning.source_current",
            "conditioning.selected_previz_sha256",
            "Selected conditioning evidence must identify the current previz bytes",
        )
    ]


def validate_manifest(value: Any) -> list[Finding]:
    findings = schema_findings(value)
    if not isinstance(value, dict):
        return findings
    findings.extend(validate_paths(value))
    findings.extend(validate_timeline(value))
    findings.extend(validate_render(value))
    findings.extend(validate_subjects(value))
    findings.extend(validate_cuts(value))
    findings.extend(validate_motion(value))
    findings.extend(validate_conditioning(value))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a Blender-to-Seedance blockout manifest"
    )
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        value = json.loads(args.manifest.read_text())
        findings = validate_manifest(value)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as error:
        findings = [Finding("input.readable", str(args.manifest), str(error))]
    print(
        json.dumps(
            {
                "ok": not findings,
                "findings": [asdict(finding) for finding in findings],
            },
            indent=2,
        )
    )
    return int(bool(findings))


if __name__ == "__main__":
    raise SystemExit(main())
