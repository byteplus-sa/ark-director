from __future__ import annotations

import argparse
import hashlib
import json
import re
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

SCHEMA_VERSION = 1
TOP_LEVEL_KEYS = {
    "schema_version",
    "base",
    "output",
    "duration",
    "layers",
    "fade_to_black",
    "audio",
    "loudnorm",
}
LAYER_KEYS = {
    "src",
    "start",
    "end",
    "x",
    "y",
    "width",
    "fade_in",
    "fade_out",
    "rise_px",
    "rise_s",
}
COLOR_PATTERN = re.compile(r"^(0x|#)?[0-9A-Fa-f]{6}$")
DEFAULT_BACKGROUND = "0x2A2A2A"
AUDIO_BITRATE = "192k"


@dataclass(frozen=True)
class MediaInfo:
    fps: str
    width: int
    height: int
    duration: float
    has_audio: bool


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def number(value: float) -> str:
    text = f"{round(float(value), 6):.6f}".rstrip("0").rstrip(".")
    return "0" if text in ("", "-0") else text


def project_path(project: Path, relative: str, label: str) -> Path:
    if not isinstance(relative, str) or not relative.strip():
        raise ValueError(f"{label} must be a non-empty project-relative path")
    pure = PurePosixPath(relative)
    if pure.is_absolute() or Path(relative).is_absolute() or ".." in pure.parts:
        raise ValueError(f"{label} must stay inside the project: {relative}")
    root = project.resolve()
    resolved = (root / relative).resolve()
    if not resolved.is_relative_to(root):
        raise ValueError(f"{label} escapes the project: {relative}")
    return resolved


def is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def non_negative(layer: dict[str, Any], key: str, default: float, label: str) -> float:
    value = layer.get(key, default)
    if not is_number(value) or value < 0:
        raise ValueError(f"{label}.{key} must be a non-negative number")
    return float(value)


def validate_layer(layer: object, index: int, duration: float) -> dict[str, Any]:
    label = f"layers[{index}]"
    if not isinstance(layer, dict):
        raise TypeError(f"{label} must be an object")
    unknown = set(layer) - LAYER_KEYS
    if unknown:
        raise ValueError(f"{label} has unknown keys: {sorted(unknown)}")
    if not isinstance(layer.get("src"), str):
        raise TypeError(f"{label}.src is required")
    start = non_negative(layer, "start", 0, label)
    end_value = layer.get("end")
    if end_value is not None and (not is_number(end_value) or end_value <= start):
        raise ValueError(f"{label}.end must be null or greater than start")
    end = None if end_value is None else float(end_value)
    fade_in = non_negative(layer, "fade_in", 0, label)
    fade_out = non_negative(layer, "fade_out", 0, label)
    if fade_out and end is None:
        raise ValueError(f"{label}.fade_out requires an end time")
    window = (end if end is not None else duration) - start
    if fade_in + fade_out > window + 1e-9:
        raise ValueError(f"{label} fades exceed the visible window")
    if start >= duration:
        raise ValueError(f"{label}.start is beyond the timeline duration")
    x = layer.get("x", 0)
    if x != "center" and (not isinstance(x, int) or isinstance(x, bool)):
        raise ValueError(f"{label}.x must be an integer or 'center'")
    y = layer.get("y", 0)
    if not isinstance(y, int) or isinstance(y, bool):
        raise TypeError(f"{label}.y must be an integer")
    width = layer.get("width")
    if width is not None and (
        not isinstance(width, int) or isinstance(width, bool) or width <= 0
    ):
        raise ValueError(f"{label}.width must be a positive integer")
    rise_px = layer.get("rise_px", 0)
    if not isinstance(rise_px, int) or isinstance(rise_px, bool):
        raise TypeError(f"{label}.rise_px must be an integer")
    rise_s = layer.get("rise_s", 0.15 if rise_px else 0)
    if not is_number(rise_s) or rise_s < 0 or (rise_px and rise_s <= 0):
        raise ValueError(f"{label}.rise_s must be positive when rise_px is set")
    return {
        "src": layer["src"],
        "start": start,
        "end": end,
        "x": x,
        "y": y,
        "width": width,
        "fade_in": fade_in,
        "fade_out": fade_out,
        "rise_px": rise_px,
        "rise_s": float(rise_s),
    }


def validate_timeline(timeline: object, base_duration: float) -> dict[str, Any]:
    if not isinstance(timeline, dict):
        raise TypeError("Timeline must be a JSON object")
    unknown = set(timeline) - TOP_LEVEL_KEYS
    if unknown:
        raise ValueError(f"Timeline has unknown keys: {sorted(unknown)}")
    if timeline.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"schema_version must be {SCHEMA_VERSION}")
    for key in ("base", "output"):
        if not isinstance(timeline.get(key), str):
            raise TypeError(f"Timeline {key} must be a project-relative path")
    duration = timeline.get("duration", base_duration)
    if not is_number(duration) or duration <= 0:
        raise ValueError("duration must be a positive number")
    layers = timeline.get("layers")
    if not isinstance(layers, list) or not layers:
        raise ValueError("layers must be a non-empty list")
    fade = timeline.get("fade_to_black")
    if fade is not None and (
        not isinstance(fade, dict)
        or set(fade) != {"start", "duration"}
        or not is_number(fade["start"])
        or not is_number(fade["duration"])
        or fade["start"] < 0
        or fade["duration"] <= 0
    ):
        raise ValueError("fade_to_black must be {start, duration} with positive duration")
    audio = timeline.get("audio", "copy")
    if audio not in ("copy", "none") and not (
        isinstance(audio, dict) and set(audio) == {"path"} and isinstance(audio["path"], str)
    ):
        raise ValueError("audio must be 'copy', 'none', or {\"path\": ...}")
    loudnorm = timeline.get("loudnorm")
    if loudnorm is not None:
        if (
            not isinstance(loudnorm, dict)
            or not set(loudnorm) <= {"i", "tp", "lra"}
            or not {"i", "tp"} <= set(loudnorm)
            or not all(is_number(value) for value in loudnorm.values())
        ):
            raise ValueError("loudnorm must be {i, tp[, lra]} numbers")
        if audio == "none":
            raise ValueError("loudnorm requires audio")
    return {
        "base": timeline["base"],
        "output": timeline["output"],
        "duration": float(duration),
        "layers": [
            validate_layer(layer, index, float(duration))
            for index, layer in enumerate(layers)
        ],
        "fade_to_black": fade,
        "audio": audio,
        "loudnorm": loudnorm,
    }


def enable_expression(layer: dict[str, Any]) -> str:
    if layer["end"] is None:
        return f"gte(t,{number(layer['start'])})"
    return f"between(t,{number(layer['start'])},{number(layer['end'])})"


def y_expression(layer: dict[str, Any]) -> str:
    if not layer["rise_px"]:
        return str(layer["y"])
    progress = (
        f"min(1,max(0,(t-{number(layer['start'])})/{number(layer['rise_s'])}))"
    )
    return f"{layer['y']}+{layer['rise_px']}*(1-{progress})"


def layer_chain(layer: dict[str, Any], stream: int, label: str) -> str:
    filters = ["format=rgba"]
    if layer["width"] is not None:
        filters.append(f"scale={layer['width']}:-1")
    if layer["fade_in"]:
        filters.append(
            f"fade=t=in:st={number(layer['start'])}:d={number(layer['fade_in'])}:alpha=1"
        )
    if layer["fade_out"]:
        start = layer["end"] - layer["fade_out"]
        filters.append(
            f"fade=t=out:st={number(start)}:d={number(layer['fade_out'])}:alpha=1"
        )
    return f"[{stream}:v]{','.join(filters)}[{label}]"


def overlay_filter(layer: dict[str, Any]) -> str:
    x = "(W-w)/2" if layer["x"] == "center" else str(layer["x"])
    return (
        f"overlay=x='{x}':y='{y_expression(layer)}'"
        f":enable='{enable_expression(layer)}':eval=frame"
    )


def filter_graph(timeline: dict[str, Any]) -> str:
    parts = []
    current = "0:v"
    for index, layer in enumerate(timeline["layers"]):
        label = f"l{index}"
        parts.append(layer_chain(layer, index + 1, label))
        target = f"v{index}"
        parts.append(f"[{current}][{label}]{overlay_filter(layer)}[{target}]")
        current = target
    tail = []
    fade = timeline["fade_to_black"]
    if fade is not None:
        tail.append(
            f"fade=t=out:st={number(fade['start'])}:d={number(fade['duration'])}"
        )
    tail.append("format=yuv420p")
    parts.append(f"[{current}]{','.join(tail)}[vout]")
    return ";".join(parts)


def layer_inputs(
    timeline: dict[str, Any], project: Path, info: MediaInfo
) -> list[str]:
    arguments: list[str] = []
    for index, layer in enumerate(timeline["layers"]):
        source = project_path(project, layer["src"], f"layers[{index}].src")
        arguments += [
            "-loop", "1",
            "-framerate", info.fps,
            "-t", number(timeline["duration"]),
            "-i", str(source),
        ]
    return arguments


def audio_arguments(
    timeline: dict[str, Any], project: Path, info: MediaInfo
) -> tuple[list[str], list[str]]:
    audio = timeline["audio"]
    if audio == "none":
        return [], ["-an"]
    loudnorm = timeline["loudnorm"]
    if isinstance(audio, dict):
        source = project_path(project, audio["path"], "audio.path")
        inputs = ["-i", str(source)]
        mapping = ["-map", f"{len(timeline['layers']) + 1}:a:0"]
    else:
        if not info.has_audio:
            return [], ["-an"]
        inputs = []
        mapping = ["-map", "0:a:0"]
    if loudnorm is None and audio == "copy":
        return inputs, mapping + ["-c:a", "copy"]
    codec = ["-c:a", "aac", "-b:a", AUDIO_BITRATE]
    if loudnorm is not None:
        parameters = f"loudnorm=I={number(loudnorm['i'])}:TP={number(loudnorm['tp'])}"
        if "lra" in loudnorm:
            parameters += f":LRA={number(loudnorm['lra'])}"
        codec = ["-af", parameters] + codec
    return inputs, mapping + codec


def build_command(
    timeline: dict[str, Any],
    project: Path,
    info: MediaInfo,
    overwrite: bool = False,
    ffmpeg: str = "ffmpeg",
) -> list[str]:
    base = project_path(project, timeline["base"], "base")
    output = project_path(project, timeline["output"], "output")
    audio_inputs, audio_output = audio_arguments(timeline, project, info)
    return [
        ffmpeg,
        "-hide_banner",
        "-loglevel", "error",
        "-y" if overwrite else "-n",
        "-i", str(base),
        *layer_inputs(timeline, project, info),
        *audio_inputs,
        "-filter_complex", filter_graph(timeline),
        "-map", "[vout]",
        *audio_output,
        "-c:v", "libx264",
        "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-t", number(timeline["duration"]),
        "-movflags", "+faststart",
        str(output),
    ]


def build_preview_command(
    timeline: dict[str, Any],
    project: Path,
    info: MediaInfo,
    output: Path,
    at: float,
    background: str | None,
    overwrite: bool = False,
    ffmpeg: str = "ffmpeg",
) -> list[str]:
    if background is None:
        base_input = ["-i", str(project_path(project, timeline["base"], "base"))]
    else:
        if not COLOR_PATTERN.match(background):
            raise ValueError("background must be a hex color such as 0x2A2A2A")
        color = "0x" + background[-6:]
        source = (
            f"color=c={color}:s={info.width}x{info.height}"
            f":r={info.fps}:d={number(timeline['duration'])}"
        )
        base_input = ["-f", "lavfi", "-i", source]
    return [
        ffmpeg,
        "-hide_banner",
        "-loglevel", "error",
        "-y" if overwrite else "-n",
        *base_input,
        *layer_inputs(timeline, project, info),
        "-filter_complex", filter_graph(timeline),
        "-map", "[vout]",
        "-ss", number(at),
        "-frames:v", "1",
        "-update", "1",
        str(output),
    ]


def require_tool(name: str) -> str:
    found = shutil.which(name)
    if found is None:
        raise RuntimeError(f"{name} is not available on PATH")
    return found


def ffprobe(path: Path) -> dict[str, Any]:
    result = subprocess.run(
        [
            require_tool("ffprobe"),
            "-v", "error",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(result.stdout)
    if not isinstance(data, dict):
        raise TypeError(f"Unexpected ffprobe output for {path}")
    return data


def media_info(path: Path) -> MediaInfo:
    if not path.is_file():
        raise ValueError(f"Base video does not exist: {path}")
    data = ffprobe(path)
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    if video is None:
        raise ValueError(f"Base has no video stream: {path}")
    fps = video.get("avg_frame_rate") or video.get("r_frame_rate")
    if not fps or fps.startswith("0/"):
        fps = video.get("r_frame_rate", "25/1")
    duration = float(data.get("format", {}).get("duration") or video.get("duration") or 0)
    return MediaInfo(
        fps=str(fps),
        width=int(video["width"]),
        height=int(video["height"]),
        duration=duration,
        has_audio=any(s.get("codec_type") == "audio" for s in streams),
    )


def ffmpeg_version(ffmpeg: str) -> str:
    result = subprocess.run(
        [ffmpeg, "-version"], check=True, capture_output=True, text=True
    )
    return result.stdout.splitlines()[0] if result.stdout else "unknown"


def sidecar_path(output: Path) -> Path:
    return output.with_name(f"overlay_{output.stem}.json")


def run_ffmpeg(arguments: list[str]) -> None:
    result = subprocess.run(arguments, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {result.stderr.strip()[-2000:]}")


def relative(path: Path, project: Path) -> str:
    return path.relative_to(project.resolve()).as_posix()


def render(
    timeline: dict[str, Any],
    timeline_file: Path,
    project: Path,
    info: MediaInfo,
    overwrite: bool,
) -> dict[str, Any]:
    ffmpeg = require_tool("ffmpeg")
    output = project_path(project, timeline["output"], "output")
    record_path = sidecar_path(output)
    if not overwrite and (output.exists() or record_path.exists()):
        raise ValueError(f"Output exists; pass --overwrite to replace: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    arguments = build_command(timeline, project, info, overwrite, ffmpeg)
    run_ffmpeg(arguments)
    base = project_path(project, timeline["base"], "base")
    produced = media_info(output)
    audio = timeline["audio"]
    audio_record: object = audio
    if isinstance(audio, dict):
        audio_path = project_path(project, audio["path"], "audio.path")
        audio_record = {"path": relative(audio_path, project), "sha256": sha256(audio_path)}
    record = {
        "schema_version": SCHEMA_VERSION,
        "tool": "html-graphic-render/overlay_timeline.py",
        "ffmpeg_version": ffmpeg_version(ffmpeg),
        "timeline": {
            "path": relative(timeline_file, project),
            "sha256": sha256(timeline_file),
        },
        "base": {"path": relative(base, project), "sha256": sha256(base)},
        "layers": [
            {
                "path": relative(path, project),
                "sha256": sha256(path),
                "start": layer["start"],
                "end": layer["end"],
            }
            for layer in timeline["layers"]
            for path in [project_path(project, layer["src"], "layer")]
        ],
        "audio": audio_record,
        "loudnorm": timeline["loudnorm"],
        "fade_to_black": timeline["fade_to_black"],
        "output": {
            "path": relative(output, project),
            "sha256": sha256(output),
            "bytes": output.stat().st_size,
            "duration_s": produced.duration,
            "width": produced.width,
            "height": produced.height,
            "fps": produced.fps,
            "has_audio": produced.has_audio,
        },
    }
    record_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"output": record["output"], "record": relative(record_path, project)}


def preview(
    timeline: dict[str, Any],
    project: Path,
    info: MediaInfo,
    target: str,
    at: float | None,
    background: str | None,
    overwrite: bool,
) -> dict[str, Any]:
    ffmpeg = require_tool("ffmpeg")
    output = project_path(project, target, "preview")
    if output.suffix.lower() != ".png":
        raise ValueError("Preview output must be a .png file")
    if output.exists() and not overwrite:
        raise ValueError(f"Preview exists; pass --overwrite to replace: {output}")
    moment = 0.0 if at is None else at
    if moment < 0 or moment >= timeline["duration"]:
        raise ValueError("--at must fall inside the timeline duration")
    if background is None and at is None:
        background = DEFAULT_BACKGROUND
    output.parent.mkdir(parents=True, exist_ok=True)
    run_ffmpeg(
        build_preview_command(
            timeline, project, info, output, moment, background, overwrite, ffmpeg
        )
    )
    if not output.is_file():
        raise RuntimeError("ffmpeg did not write the preview")
    return {"preview": relative(output, project), "at": moment, "sha256": sha256(output)}


def load_timeline(project: Path, relative_path: str) -> tuple[Path, dict[str, Any], MediaInfo]:
    timeline_file = project_path(project, relative_path, "timeline")
    raw = json.loads(timeline_file.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("base"), str):
        raise TypeError("Timeline base must be a project-relative path")
    info = media_info(project_path(project, raw["base"], "base"))
    return timeline_file, validate_timeline(raw, info.duration), info


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Composite timed PNG overlay layers onto a base video with ffmpeg."
    )
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--timeline", required=True, help="Project-relative JSON path")
    parser.add_argument("--run", action="store_true", help="Execute instead of printing")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--preview", help="Project-relative PNG path for one still")
    parser.add_argument("--at", type=float, help="Preview time in seconds")
    parser.add_argument("--background", help="Solid preview background, e.g. 0x2A2A2A")
    return parser


def execute(arguments: argparse.Namespace) -> dict[str, Any] | str:
    project = arguments.project
    if not project.is_dir():
        raise ValueError(f"Project directory does not exist: {project}")
    timeline_file, timeline, info = load_timeline(project, arguments.timeline)
    if arguments.preview:
        return preview(
            timeline,
            project,
            info,
            arguments.preview,
            arguments.at,
            arguments.background,
            arguments.overwrite,
        )
    if arguments.run:
        return render(timeline, timeline_file, project, info, arguments.overwrite)
    return shlex.join(build_command(timeline, project, info, arguments.overwrite))


def main() -> int:
    try:
        result = execute(build_parser().parse_args())
    except (
        OSError,
        RuntimeError,
        TypeError,
        ValueError,
        subprocess.SubprocessError,
    ) as error:
        print(str(error), file=sys.stderr)
        return 2
    print(result if isinstance(result, str) else json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
