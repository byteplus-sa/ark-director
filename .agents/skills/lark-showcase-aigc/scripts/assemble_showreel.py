#!/usr/bin/env python3
"""Assemble clips into one web-ready showreel with crossfades and locked A/V sync."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


class ShowreelError(Exception):
    pass


def probe(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ShowreelError(f"input not found: {path}")
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries",
            "stream=codec_type,width,height,r_frame_rate,duration",
            "-show_entries", "format=duration", "-of", "json", str(path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise ShowreelError(f"ffprobe failed for {path}: {result.stderr.strip()}")
    data = json.loads(result.stdout)
    video = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
    if video is None:
        raise ShowreelError(f"no video stream in {path}")
    has_audio = any(s.get("codec_type") == "audio" for s in data["streams"])
    duration = float(video.get("duration") or data["format"]["duration"])
    return {"duration": duration, "has_audio": has_audio, "width": int(video["width"]), "height": int(video["height"])}


def plan(durations: list[float], crossfade: float, fade: float) -> dict[str, Any]:
    if len(durations) < 2:
        raise ShowreelError("at least two clips are required")
    if crossfade <= 0 or any(d <= crossfade * 2 for d in durations):
        raise ShowreelError("crossfade must be positive and shorter than half of every clip")
    cumulative = durations[0]
    offsets = []
    for duration in durations[1:]:
        offsets.append(round(cumulative - crossfade, 6))
        cumulative = cumulative - crossfade + duration
    total = round(cumulative, 6)
    if fade * 2 >= total:
        raise ShowreelError("fade is too long for the total duration")
    return {"offsets": offsets, "total": total, "fade_out_start": round(total - fade, 6)}


def build_filter(info: list[dict[str, Any]], crossfade: float, fade: float, fps: int, size: tuple[int, int]) -> tuple[str, dict[str, Any]]:
    durations = [i["duration"] for i in info]
    schedule = plan(durations, crossfade, fade)
    width, height = size
    parts: list[str] = []
    for index, item in enumerate(info):
        duration = item["duration"]
        parts.append(
            f"[{index}:v]settb=AVTB,fps={fps},scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p[v{index}]"
        )
        source = f"[{index}:a]" if item["has_audio"] else None
        if source is None:
            parts.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{duration},asetpts=PTS-STARTPTS[a{index}]")
        else:
            parts.append(f"{source}aresample=48000,atrim=0:{duration},asetpts=PTS-STARTPTS,apad=whole_dur={duration}[a{index}]")
    video_prev, audio_prev = "v0", "a0"
    for index, offset in enumerate(schedule["offsets"], start=1):
        parts.append(f"[{video_prev}][v{index}]xfade=transition=fade:duration={crossfade}:offset={offset}[vx{index}]")
        parts.append(f"[{audio_prev}][a{index}]acrossfade=d={crossfade}:c1=tri:c2=tri[ax{index}]")
        video_prev, audio_prev = f"vx{index}", f"ax{index}"
    start = schedule["fade_out_start"]
    parts.append(f"[{video_prev}]fade=t=in:st=0:d={fade},fade=t=out:st={start}:d={fade}[vout]")
    parts.append(f"[{audio_prev}]afade=t=in:st=0:d={fade},afade=t=out:st={start}:d={fade}[aout]")
    return ";".join(parts), schedule


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def moov_offset(path: Path) -> int:
    return path.read_bytes().find(b"moov")


def assemble(clips: list[Path], out: Path, crossfade: float, fade: float, crf: int, dry_run: bool) -> dict[str, Any]:
    info = [probe(clip) for clip in clips]
    first = info[0]
    fps = 24
    size = (first["width"], first["height"])
    graph, schedule = build_filter(info, crossfade, fade, fps, size)
    command = ["ffmpeg", "-v", "error", "-y"]
    for clip in clips:
        command += ["-i", str(clip)]
    command += [
        "-filter_complex", graph, "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", str(crf),
        "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-movflags", "+faststart", str(out),
    ]
    record: dict[str, Any] = {
        "inputs": [str(c) for c in clips],
        "output": str(out),
        "crossfade_s": crossfade,
        "fade_s": fade,
        "expected_duration_s": schedule["total"],
        "offsets": schedule["offsets"],
        "size": list(size),
    }
    if dry_run:
        record["command"] = command
        return record
    out.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise ShowreelError(f"ffmpeg failed: {result.stderr.strip()[:500]}")
    record["sha256"] = sha256(out)
    record["moov_offset"] = moov_offset(out)
    record["bytes"] = out.stat().st_size
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("clips", nargs="+", type=Path, help="clips in play order")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--crossfade", type=float, default=0.4)
    parser.add_argument("--fade", type=float, default=0.5)
    parser.add_argument("--crf", type=int, default=21)
    parser.add_argument("--record", type=Path, help="write the assembly record JSON here")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        record = assemble(args.clips, args.out, args.crossfade, args.fade, args.crf, args.dry_run)
    except ShowreelError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    text = json.dumps(record, indent=2)
    if args.record:
        args.record.write_text(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
