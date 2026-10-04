from __future__ import annotations

import argparse
import json
import math
import shutil
import statistics
import subprocess
import sys
import tempfile
from collections.abc import Iterator
from itertools import pairwise
from pathlib import Path
from typing import Any, BinaryIO


class MeasureError(Exception):
    pass


def require_binary(name: str) -> str:
    found = shutil.which(name)
    if not found:
        raise MeasureError(f"{name} was not found on PATH")
    return found


def parse_rate(value: str) -> float:
    try:
        numerator, _, denominator = value.partition("/")
        rate = float(numerator) / float(denominator or 1)
    except (ValueError, ZeroDivisionError):
        return 0.0
    return rate if math.isfinite(rate) else 0.0


def probe(path: Path) -> dict[str, Any]:
    result = subprocess.run(
        [
            require_binary("ffprobe"),
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,avg_frame_rate,r_frame_rate:format=duration",
            "-of",
            "json",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip().splitlines()
        raise MeasureError(
            f"Not a readable media file: {path} ({detail[-1] if detail else 'ffprobe failed'})"
        )
    document = json.loads(result.stdout or "{}")
    streams = document.get("streams") or []
    if not streams or not streams[0].get("width") or not streams[0].get("height"):
        raise MeasureError(f"No video stream found in {path}")
    stream = streams[0]
    try:
        duration = float(document.get("format", {}).get("duration", 0.0))
    except (TypeError, ValueError):
        duration = 0.0
    native = parse_rate(stream.get("avg_frame_rate", "")) or parse_rate(
        stream.get("r_frame_rate", "")
    )
    return {
        "width": int(stream["width"]),
        "height": int(stream["height"]),
        "duration_s": duration,
        "native_fps": native,
    }


def read_frames(
    path: Path, fps: float, width: int, height: int
) -> Iterator[bytes]:
    size = width * height
    with tempfile.TemporaryFile() as errors:
        process = subprocess.Popen(
            [
                require_binary("ffmpeg"),
                "-v",
                "error",
                "-nostdin",
                "-noautorotate",
                "-i",
                str(path),
                "-an",
                "-vf",
                f"fps={fps},format=gray",
                "-f",
                "rawvideo",
                "-pix_fmt",
                "gray",
                "pipe:1",
            ],
            stdout=subprocess.PIPE,
            stderr=errors,
        )
        stdout: BinaryIO = process.stdout  # type: ignore[assignment]
        try:
            while True:
                frame = stdout.read(size)
                if len(frame) < size:
                    break
                yield frame
        finally:
            stdout.close()
            code = process.wait()
        if code != 0:
            errors.seek(0)
            detail = errors.read().decode(errors="replace").strip().splitlines()
            raise MeasureError(
                f"ffmpeg could not decode {path} ({detail[-1] if detail else code})"
            )


def dark_run(
    frame: bytes,
    width: int,
    height: int,
    x0: int,
    columns: int,
    level: int,
    from_bottom: bool,
) -> int:
    count = 0
    for step in range(height // 2):
        row = height - 1 - step if from_bottom else step
        start = row * width + x0
        if sum(frame[start : start + columns]) / columns > level:
            break
        count += 1
    return count


def bright_fraction(
    frame: bytes, width: int, x0: int, x1: int, rows: range, table: bytes
) -> float:
    if not rows or x1 <= x0:
        return 0.0
    bright = 0
    for row in rows:
        bright += frame[row * width + x0 : row * width + x1].translate(table).count(1)
    return bright / (len(rows) * (x1 - x0))


def sample_columns(width: int, columns: int, count: int) -> list[int]:
    if count == 1:
        return [(width - columns) // 2]
    return [
        round(width * (0.05 + 0.9 * index / (count - 1)) - columns / 2)
        for index in range(count)
    ]


def far_runs(
    path: Path, fps: float, width: int, height: int, settings: dict[str, Any]
) -> dict[str, list[tuple[int, int]]]:
    columns = settings["edge_columns"]
    level = settings["black_level"]
    runs: dict[str, list[tuple[int, int]]] = {"top": [], "bottom": []}
    for frame in read_frames(path, fps, width, height):
        for bar, from_bottom in (("top", False), ("bottom", True)):
            runs[bar].append(
                (
                    dark_run(frame, width, height, 0, columns, level, from_bottom),
                    dark_run(
                        frame, width, height, width - columns, columns, level, from_bottom
                    ),
                )
            )
    return runs


def measure_bar(
    frame: bytes,
    width: int,
    height: int,
    settings: dict[str, Any],
    reference: tuple[float, float],
    from_bottom: bool,
) -> dict[str, Any]:
    columns = settings["edge_columns"]
    level = settings["black_level"]
    left = dark_run(frame, width, height, 0, columns, level, from_bottom)
    right = dark_run(frame, width, height, width - columns, columns, level, from_bottom)
    runs: list[int] = []
    excess: list[float] = []
    for x0 in settings["interior"]:
        run = dark_run(frame, width, height, x0, columns, level, from_bottom)
        position = (x0 + columns / 2) / width
        runs.append(run)
        excess.append(run - (reference[0] + (reference[1] - reference[0]) * position))
    edge = round((reference[0] + reference[1]) / 2)
    margin = settings["edge_margin"]
    if from_bottom:
        rows = range(height - edge + margin, height)
    else:
        rows = range(max(0, edge - margin))
    overlap = bright_fraction(
        frame,
        width,
        settings["centre_x0"],
        settings["centre_x1"],
        rows,
        settings["table"],
    )
    thickness = (left + right) / 2
    return {
        "left_px": left,
        "right_px": right,
        "runs_px": runs,
        "excess_px": [round(value, 1) for value in excess],
        "thickness_px": thickness,
        "thickness_pct": round(thickness / height * 100, 3),
        "tilt_px": left - right,
        "overlap_fraction": round(overlap, 5),
    }


def contiguous_groups(values: list[float], tolerance: float) -> list[list[int]]:
    groups: list[list[int]] = []
    current: list[int] = []
    for index, value in enumerate(values):
        if value > tolerance:
            current.append(index)
        elif current:
            groups.append(current)
            current = []
    if current:
        groups.append(current)
    return groups


def classify_interior(
    excess: list[float], settings: dict[str, Any]
) -> tuple[str, float]:
    tolerance = settings["encroach_tolerance_px"]
    minimum = math.ceil(settings["bar_shape_fraction"] * len(excess))
    bow = 0.0
    merge = 0.0
    for group in contiguous_groups(excess, tolerance):
        values = [excess[index] for index in group]
        peak = max(values)
        steps = [abs(b - a) for a, b in pairwise(values)]
        smooth = max(steps, default=0.0) <= max(3.0, 0.25 * peak)
        if len(group) >= minimum and smooth:
            bow = max(bow, peak)
        else:
            merge = max(merge, peak)
    if bow:
        return "bow_in", bow
    if merge:
        return "dark_merge", merge
    return "", 0.0


def frame_events(
    frames: list[dict[str, Any]],
    bar: str,
    reference: tuple[float, float],
    settings: dict[str, Any],
) -> list[tuple[int, str, str, float]]:
    events: list[tuple[int, str, str, float]] = []
    edge_tolerance = settings["edge_tolerance_px"]
    previous: tuple[int, int] | None = None
    for index, frame in enumerate(frames):
        record = frame[bar]
        left, right = record["left_px"], record["right_px"]
        grow = max(left - reference[0], right - reference[1])
        shrink = max(reference[0] - left, reference[1] - right)
        if grow > edge_tolerance:
            events.append((index, "fail", "encroach", grow))
        elif shrink > edge_tolerance:
            events.append((index, "inspect", "far_retreat", shrink))
        tilt = abs(record["tilt_px"] - (reference[0] - reference[1]))
        if tilt > settings["tilt_tolerance_px"] and grow <= edge_tolerance:
            events.append((index, "inspect", "tilt", tilt))
        if previous is not None:
            step = (abs(left - previous[0]), abs(right - previous[1]))
            if min(step) > settings["jump_threshold_px"]:
                events.append((index, "fail", "jump", float(min(step))))
        previous = (left, right)
        kind, peak = classify_interior(record["excess_px"], settings)
        if kind == "bow_in":
            events.append((index, "fail", "bow_in", peak))
        elif kind:
            events.append((index, "inspect", "dark_merge", peak))
    return events


def merge_events(
    frames: list[dict[str, Any]],
    bar: str,
    events: list[tuple[int, str, str, float]],
    gap_s: float,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for index, severity, kind, value in events:
        time = frames[index]["time_s"]
        last = next(
            (
                item
                for item in reversed(records)
                if item["kind"] == kind and item["severity"] == severity
            ),
            None,
        )
        if last is not None and time - last["end_s"] <= gap_s:
            last["end_s"] = time
            last["frames"] += 1
            last["peak_px"] = max(last["peak_px"], round(value, 2))
        else:
            records.append(
                {
                    "bar": bar,
                    "severity": severity,
                    "kind": kind,
                    "start_s": time,
                    "end_s": time,
                    "frames": 1,
                    "peak_px": round(value, 2),
                }
            )
    return records


def overlap_intervals(
    frames: list[dict[str, Any]], bar: str, threshold: float
) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for frame in frames:
        fraction = frame[bar]["overlap_fraction"]
        if fraction > threshold:
            if current is None:
                current = {
                    "bar": bar,
                    "start_s": frame["time_s"],
                    "end_s": frame["time_s"],
                    "frames": 0,
                    "peak_fraction": 0.0,
                }
                found.append(current)
            current["end_s"] = frame["time_s"]
            current["frames"] += 1
            current["peak_fraction"] = max(current["peak_fraction"], fraction)
        else:
            current = None
    return found


def break_out_gate(
    frames: list[dict[str, Any]],
    detected: bool,
    intervals: list[dict[str, Any]],
    args: argparse.Namespace,
) -> dict[str, Any]:
    count = len(frames)
    threshold = args.overlap_threshold
    early = [frame for frame in frames if frame["time_s"] < args.start_window_s]
    start = {
        bar: max((frame[bar]["overlap_fraction"] for frame in early), default=0.0)
        for bar in ("top", "bottom")
    }
    duty = {
        bar: round(
            sum(1 for frame in frames if frame[bar]["overlap_fraction"] > threshold)
            / count,
            4,
        )
        for bar in ("top", "bottom")
    }
    overlapping = [
        frame
        for frame in frames
        if max(frame["top"]["overlap_fraction"], frame["bottom"]["overlap_fraction"])
        > threshold
    ]
    duty["overall"] = round(len(overlapping) / count, 4)
    violations: list[dict[str, Any]] = []
    for bar in ("top", "bottom"):
        if start[bar] > args.start_overlap_tolerance:
            offending = [
                frame["time_s"]
                for frame in early
                if frame[bar]["overlap_fraction"] > args.start_overlap_tolerance
            ]
            violations.append(
                {
                    "kind": "starts_overlapping",
                    "bar": bar,
                    "start_s": offending[0],
                    "end_s": offending[-1],
                    "peak_fraction": start[bar],
                }
            )
    if duty["overall"] > args.max_overlap_duty:
        violations.append(
            {
                "kind": "overlap_too_continuous",
                "bar": "either",
                "duty": duty["overall"],
                "limit": args.max_overlap_duty,
                "intervals": [
                    {"bar": item["bar"], "start_s": item["start_s"], "end_s": item["end_s"]}
                    for item in intervals
                ],
            }
        )
    if not detected:
        status = "not_applicable"
    elif not overlapping:
        status = "absent"
    else:
        status = "fail" if violations else "pass"
    return {
        "status": status,
        "passed": status == "pass",
        "start_window_s": args.start_window_s,
        "start_overlap": {**start, "tolerance": args.start_overlap_tolerance},
        "overlap_duty": {**duty, "limit": args.max_overlap_duty},
        "violations": violations,
    }


def bar_summary(
    frames: list[dict[str, Any]],
    bar: str,
    height: int,
    reference: tuple[float, float],
    detected: bool,
    settings: dict[str, Any],
) -> dict[str, Any]:
    thickness = [frame[bar]["thickness_px"] for frame in frames]
    median = statistics.median(thickness)
    records: list[dict[str, Any]] = []
    if detected:
        events = frame_events(frames, bar, reference, settings)
        records = merge_events(frames, bar, events, settings["merge_gap_s"])
        if abs(reference[0] - reference[1]) > settings["tilt_tolerance_px"]:
            records.append(
                {
                    "bar": bar,
                    "severity": "inspect",
                    "kind": "static_tilt",
                    "start_s": frames[0]["time_s"],
                    "end_s": frames[-1]["time_s"],
                    "frames": len(frames),
                    "peak_px": round(abs(reference[0] - reference[1]), 2),
                }
            )
    records.sort(key=lambda item: (item["start_s"], item["kind"]))
    failures = [item for item in records if item["severity"] == "fail"]
    notes = [item for item in records if item["severity"] == "inspect"]
    status = "fail" if failures else "inspect" if notes else "pass"
    return {
        "thickness_pct": {
            "median": round(median / height * 100, 3),
            "min": round(min(thickness) / height * 100, 3),
            "max": round(max(thickness) / height * 100, 3),
        },
        "thickness_px": {
            "median": median,
            "min": min(thickness),
            "max": max(thickness),
        },
        "median_edge_px": {"left": reference[0], "right": reference[1]},
        "static_tilt_px": reference[0] - reference[1],
        "max_far_encroach_px": max(
            max(f[bar]["left_px"] - reference[0], f[bar]["right_px"] - reference[1])
            for f in frames
        ),
        "max_far_retreat_px": max(
            max(reference[0] - f[bar]["left_px"], reference[1] - f[bar]["right_px"])
            for f in frames
        ),
        "max_interior_encroach_px": max(max(f[bar]["excess_px"]) for f in frames),
        "static": status != "fail",
        "status": status,
        "violations": failures,
        "inspect": notes,
        "frames_with_overlap": sum(
            1
            for frame in frames
            if frame[bar]["overlap_fraction"] > settings["overlap_threshold"]
        ),
        "max_overlap_fraction": max(frame[bar]["overlap_fraction"] for frame in frames),
    }


def build_flags(summary: dict[str, Any], thin_pct: float) -> list[str]:
    flags: list[str] = []
    if not summary["bars_detected"]:
        flags.append("bars_not_detected")
    elif (
        min(
            summary["top"]["thickness_pct"]["median"],
            summary["bottom"]["thickness_pct"]["median"],
        )
        < thin_pct
    ):
        flags.append("bars_thin")
    if summary["top_bottom_differ"]:
        flags.append("top_bottom_unequal")
    for name in ("top", "bottom"):
        if summary[name]["status"] == "fail":
            flags.append(f"{name}_bar_moves")
        elif summary[name]["status"] == "inspect":
            flags.append(f"{name}_bar_inspect")
        if summary[name]["frames_with_overlap"] == 0:
            flags.append(f"{name}_bar_never_crossed")
    gate = summary["break_out_gate"]
    if gate["status"] == "absent":
        flags.append("no_overlap")
    for item in gate["violations"]:
        flags.append(item["kind"])
    return flags


def measure(args: argparse.Namespace) -> dict[str, Any]:
    path: Path = args.video
    if not path.is_file():
        raise MeasureError(f"Input file not found: {path}")
    info = probe(path)
    width, height = info["width"], info["height"]
    if height < 16 or width < 16:
        raise MeasureError(f"Frame size {width}x{height} is too small to measure")
    fps = args.fps if args.fps is not None else info["native_fps"]
    if not 0 < fps <= 120:
        raise MeasureError("Could not determine a sampling rate; pass --fps")
    columns = max(2, round(width * args.edge_fraction))
    span = args.centre_span
    settings: dict[str, Any] = {
        "edge_columns": columns,
        "black_level": args.black_level,
        "edge_margin": args.edge_margin,
        "interior": sample_columns(width, columns, args.interior_columns),
        "centre_x0": round(width * (1 - span) / 2),
        "centre_x1": round(width * (1 + span) / 2),
        "table": bytes(1 if value > args.black_level else 0 for value in range(256)),
        "overlap_threshold": args.overlap_threshold,
        "edge_tolerance_px": args.edge_tolerance_px,
        "tilt_tolerance_px": args.tilt_tolerance_px,
        "encroach_tolerance_px": args.encroach_tolerance_px,
        "bar_shape_fraction": args.bar_shape_fraction,
        "jump_threshold_px": args.jump_threshold_px,
        "merge_gap_s": args.merge_gap_s,
    }
    first = far_runs(path, fps, width, height, settings)
    if not first["top"]:
        raise MeasureError(f"No frames could be decoded from {path}")
    references = {
        bar: (
            float(statistics.median(left for left, _ in runs)),
            float(statistics.median(right for _, right in runs)),
        )
        for bar, runs in first.items()
    }
    frames: list[dict[str, Any]] = []
    for index, frame in enumerate(read_frames(path, fps, width, height)):
        frames.append(
            {
                "index": index,
                "time_s": round(index / fps, 4),
                "top": measure_bar(frame, width, height, settings, references["top"], False),
                "bottom": measure_bar(
                    frame, width, height, settings, references["bottom"], True
                ),
            }
        )
    top_pct = sum(references["top"]) / 2 / height * 100
    bottom_pct = sum(references["bottom"]) / 2 / height * 100
    detected = min(top_pct, bottom_pct) >= args.min_bar_pct
    intervals = overlap_intervals(frames, "top", args.overlap_threshold)
    intervals += overlap_intervals(frames, "bottom", args.overlap_threshold)
    intervals.sort(key=lambda item: (item["start_s"], item["bar"]))
    summary: dict[str, Any] = {
        "top": bar_summary(frames, "top", height, references["top"], detected, settings),
        "bottom": bar_summary(
            frames, "bottom", height, references["bottom"], detected, settings
        ),
    }
    top_median = summary["top"]["thickness_pct"]["median"]
    bottom_median = summary["bottom"]["thickness_pct"]["median"]
    summary["bars_detected"] = detected
    summary["top_bottom_difference_pct"] = round(abs(top_median - bottom_median), 3)
    summary["top_bottom_differ"] = (
        summary["top_bottom_difference_pct"] > args.top_bottom_tolerance_pct
    )
    statuses = (summary["top"]["status"], summary["bottom"]["status"])
    status = (
        "fail"
        if not detected or "fail" in statuses
        else "inspect"
        if "inspect" in statuses
        else "pass"
    )
    summary["static_bar_gate"] = {
        "status": status,
        "passed": status != "fail",
        "tolerances_px": {
            "far_edge": args.edge_tolerance_px,
            "tilt": args.tilt_tolerance_px,
            "interior_encroach": args.encroach_tolerance_px,
            "jump": args.jump_threshold_px,
        },
        "violations": summary["top"]["violations"] + summary["bottom"]["violations"],
        "inspect": summary["top"]["inspect"] + summary["bottom"]["inspect"],
    }
    summary["break_out_gate"] = break_out_gate(frames, detected, intervals, args)
    summary["frames_scanned"] = len(frames)
    summary["overlap_intervals"] = len(intervals)
    summary["flags"] = build_flags(summary, args.thin_pct)
    return {
        "input": str(path),
        "width": width,
        "height": height,
        "duration_s": round(info["duration_s"], 3),
        "native_fps": round(info["native_fps"], 3),
        "sample_fps": fps,
        "parameters": {
            "black_level": args.black_level,
            "edge_columns_px": columns,
            "interior_columns_px": settings["interior"],
            "centre_span": span,
            "edge_margin_px": args.edge_margin,
            "overlap_threshold": args.overlap_threshold,
            "top_bottom_tolerance_pct": args.top_bottom_tolerance_pct,
            "bar_shape_fraction": args.bar_shape_fraction,
            "start_window_s": args.start_window_s,
        },
        "frames": frames,
        "overlap_intervals": intervals,
        "summary": summary,
    }


def sheet_settings(args: argparse.Namespace) -> tuple[float, int, int]:
    windowed = args.window is not None
    fps = args.contact_fps if args.contact_fps is not None else (12.0 if windowed else 2.0)
    columns = args.contact_columns or (6 if windowed else 4)
    width = args.contact_width or (320 if windowed else 480)
    return fps, columns, width


def contact_sheet(args: argparse.Namespace, duration: float) -> None:
    fps, columns, tile_width = sheet_settings(args)
    start, length = 0.0, duration
    if args.window is not None:
        start = args.window[0]
        length = args.window[1] - args.window[0]
    count = max(1, math.ceil(length * fps))
    if count > args.max_tiles:
        raise MeasureError(
            f"The sheet would need {count} tiles (limit {args.max_tiles}); "
            "narrow --window or lower --contact-fps"
        )
    rows = math.ceil(count / columns)
    command = [require_binary("ffmpeg"), "-v", "error", "-nostdin", "-y"]
    if args.window is not None:
        command += ["-ss", f"{start}", "-t", f"{length}"]
    command += [
        "-i",
        str(args.video),
        "-an",
        "-vf",
        f"fps={fps},scale={tile_width}:-2,tile={columns}x{rows}:padding=4:color=white",
        "-frames:v",
        "1",
        str(args.contact_sheet),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0 or not args.contact_sheet.is_file():
        detail = result.stderr.strip().splitlines()
        raise MeasureError(
            f"Contact sheet failed ({detail[-1] if detail else result.returncode})"
        )


def check_outputs(args: argparse.Namespace) -> None:
    for option in (args.output, args.contact_sheet):
        if option is None:
            continue
        if option.exists() and not args.overwrite:
            raise MeasureError(f"{option} exists; pass --overwrite to replace it")
        if not option.parent.is_dir():
            raise MeasureError(f"Output directory does not exist: {option.parent}")


def check_ranges(args: argparse.Namespace) -> None:
    rules = (
        ("--fps", args.fps is None or 0 < args.fps <= 120),
        ("--black-level", 0 <= args.black_level <= 128),
        ("--edge-fraction", 0 < args.edge_fraction <= 0.1),
        ("--centre-span", 0 < args.centre_span <= 0.95),
        ("--edge-margin", 0 <= args.edge_margin <= 64),
        ("--interior-columns", 3 <= args.interior_columns <= 61),
        ("--bar-shape-fraction", 0 < args.bar_shape_fraction <= 1),
        ("--merge-gap-s", args.merge_gap_s >= 0),
        ("--start-window-s", 0 < args.start_window_s <= 5),
        ("--start-overlap-tolerance", 0 <= args.start_overlap_tolerance < 1),
        ("--max-overlap-duty", 0 < args.max_overlap_duty <= 1),
        ("--overlap-threshold", 0 <= args.overlap_threshold < 1),
        ("--edge-tolerance-px", args.edge_tolerance_px >= 0),
        ("--tilt-tolerance-px", args.tilt_tolerance_px >= 0),
        ("--encroach-tolerance-px", args.encroach_tolerance_px >= 0),
        ("--jump-threshold-px", args.jump_threshold_px >= 0),
        ("--top-bottom-tolerance-pct", args.top_bottom_tolerance_pct >= 0),
        ("--min-bar-pct", 0 <= args.min_bar_pct < 50),
        ("--thin-pct", 0 <= args.thin_pct < 50),
        ("--contact-fps", args.contact_fps is None or 0 < args.contact_fps <= 30),
        ("--contact-columns", args.contact_columns is None or 1 <= args.contact_columns <= 12),
        ("--contact-width", args.contact_width is None or 64 <= args.contact_width <= 1920),
        ("--max-tiles", 1 <= args.max_tiles <= 400),
    )
    for name, valid in rules:
        if not valid:
            raise MeasureError(f"{name} is out of range")
    if args.window is not None:
        start, end = args.window
        if not 0 <= start < end:
            raise MeasureError("--window needs 0 <= START < END")
        if args.contact_sheet is None:
            raise MeasureError("--window needs --contact-sheet")


def check_window(args: argparse.Namespace) -> None:
    if not args.video.is_file():
        raise MeasureError(f"Input file not found: {args.video}")
    duration = probe(args.video)["duration_s"]
    if args.window[1] > duration + 0.05:
        raise MeasureError(f"--window ends after the clip duration ({duration:.3f} s)")


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(
        description="Measure frame-break bar motion and subject overlap in a 16:9 clip"
    )
    value.add_argument("video", type=Path)
    value.add_argument("--fps", type=float, default=None, help="sampling rate; default is the clip's native frame rate so every frame is scanned")
    value.add_argument("--black-level", type=int, default=8, help="luma at or below this counts as black; keep it below dark picture content")
    value.add_argument("--edge-fraction", type=float, default=0.01, help="width fraction of each column strip")
    value.add_argument("--centre-span", type=float, default=0.7, help="central width fraction scanned for overlap")
    value.add_argument("--edge-margin", type=int, default=4, help="rows excluded next to the bar edge when scanning overlap")
    value.add_argument("--interior-columns", type=int, default=19, help="columns sampled between 5 and 95 percent of the width")
    value.add_argument("--overlap-threshold", type=float, default=0.05, help="non-black fraction of a bar band that counts as overlap")
    value.add_argument("--edge-tolerance-px", type=float, default=2.0, help="allowed growth or shrink of each far-edge row against its median")
    value.add_argument("--tilt-tolerance-px", type=float, default=3.0, help="allowed change of the left-versus-right edge difference")
    value.add_argument("--encroach-tolerance-px", type=float, default=8.0, help="allowed interior growth over the median left-right chord")
    value.add_argument("--bar-shape-fraction", type=float, default=0.4, help="smooth interior encroachment this wide (fraction of sampled columns) counts as bar motion")
    value.add_argument("--merge-gap-s", type=float, default=0.2, help="events of one kind closer than this are merged")
    value.add_argument("--jump-threshold-px", type=float, default=3.0, help="frame-to-frame change of both far edges that counts as a jump")
    value.add_argument("--start-window-s", type=float, default=0.25, help="opening window in which the subject must sit inside the central window")
    value.add_argument("--start-overlap-tolerance", type=float, default=0.02, help="largest non-black bar-band fraction allowed in the opening window")
    value.add_argument("--max-overlap-duty", type=float, default=0.7, help="largest fraction of frames with overlap in either bar; break-outs are events, not a state")
    value.add_argument("--top-bottom-tolerance-pct", type=float, default=1.0, help="allowed median thickness difference, percentage points of frame height")
    value.add_argument("--min-bar-pct", type=float, default=1.0)
    value.add_argument("--thin-pct", type=float, default=8.0)
    value.add_argument("--output", type=Path, help="also write the full JSON here")
    value.add_argument("--summary-only", action="store_true", help="omit per-frame data from stdout")
    value.add_argument("--contact-sheet", type=Path, help="write a tiled PNG of sampled frames")
    value.add_argument("--window", type=float, nargs=2, metavar=("START", "END"), help="seconds; the contact sheet covers only this window at 12 fps by default")
    value.add_argument("--contact-fps", type=float, default=None, help="default 2, or 12 with --window")
    value.add_argument("--contact-columns", type=int, default=None, help="default 4, or 6 with --window")
    value.add_argument("--contact-width", type=int, default=None, help="tile width in px; default 480, or 320 with --window")
    value.add_argument("--max-tiles", type=int, default=120)
    value.add_argument("--overwrite", action="store_true")
    return value


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        check_ranges(args)
        check_outputs(args)
        if args.window is not None:
            check_window(args)
        document = measure(args)
        if args.contact_sheet:
            contact_sheet(args, document["duration_s"])
            document["contact_sheet"] = str(args.contact_sheet)
        if args.output:
            args.output.write_text(json.dumps(document, indent=2) + "\n")
        shown = (
            {key: value for key, value in document.items() if key != "frames"}
            if args.summary_only
            else document
        )
        print(json.dumps(shown, indent=2))
        return 0
    except MeasureError as error:
        print(json.dumps({"error": str(error)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
