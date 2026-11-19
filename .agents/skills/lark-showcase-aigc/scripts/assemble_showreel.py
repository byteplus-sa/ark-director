#!/usr/bin/env python3
"""Assemble compatible clips unchanged, or apply explicitly requested fades."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from media_concat import concatenate


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
    audio = next((s for s in data["streams"] if s.get("codec_type") == "audio"), None)
    has_audio = audio is not None
    duration = float(video.get("duration") or data["format"]["duration"])
    audio_duration = float(audio["duration"]) if audio and audio.get("duration") else None
    return {"duration": duration, "audio_duration": audio_duration, "has_audio": has_audio, "width": int(video["width"]), "height": int(video["height"])}


def plan(durations: list[float], crossfade: float, fade: float) -> dict[str, Any]:
    if len(durations) < 2:
        raise ShowreelError("at least two clips are required")
    if not all(math.isfinite(value) for value in [*durations, crossfade, fade]):
        raise ShowreelError("durations and fades must be finite")
    if crossfade < 0 or fade < 0 or any(d <= crossfade * 2 for d in durations):
        raise ShowreelError("fades must be nonnegative and crossfade shorter than half of every clip")
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
            audio_duration = item.get("audio_duration")
            if audio_duration is None or abs(audio_duration - duration) > 0.05:
                raise ShowreelError("audio/video spans differ or are unknown; approve a separate timing edit before fades")
            parts.append(f"{source}aresample=48000,asetpts=PTS-STARTPTS[a{index}]")
    video_prev, audio_prev = "v0", "a0"
    for index, offset in enumerate(schedule["offsets"], start=1):
        if crossfade:
            parts.append(f"[{video_prev}][v{index}]xfade=transition=fade:duration={crossfade}:offset={offset}[vx{index}]")
            parts.append(f"[{audio_prev}][a{index}]acrossfade=d={crossfade}:c1=tri:c2=tri[ax{index}]")
        else:
            parts.append(f"[{video_prev}][{audio_prev}][v{index}][a{index}]concat=n=2:v=1:a=1[vx{index}][ax{index}]")
        video_prev, audio_prev = f"vx{index}", f"ax{index}"
    start = schedule["fade_out_start"]
    if fade:
        parts.append(f"[{video_prev}]fade=t=in:st=0:d={fade},fade=t=out:st={start}:d={fade}[vout]")
        parts.append(f"[{audio_prev}]afade=t=in:st=0:d={fade},afade=t=out:st={start}:d={fade}[aout]")
    else:
        parts.extend([f"[{video_prev}]null[vout]", f"[{audio_prev}]anull[aout]"])
    return ";".join(parts), schedule


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def moov_offset(path: Path) -> int:
    return path.read_bytes().find(b"moov")


def assemble(clips: list[Path], out: Path, crossfade: float, fade: float, crf: int, dry_run: bool, overwrite: bool = False) -> dict[str, Any]:
    for tool in ("ffmpeg", "ffprobe"):
        if shutil.which(tool) is None:
            raise ShowreelError(f"{tool} was not found on PATH")
    if out.exists() and not overwrite and not dry_run:
        raise ShowreelError(f"output already exists: {out} (pass --overwrite to replace it)")
    if out.resolve() in [clip.resolve() for clip in clips]:
        raise ShowreelError("output must not overwrite a source")
    info = [probe(clip) for clip in clips]
    schedule = plan([item["duration"] for item in info], crossfade, fade)
    if not crossfade and not fade:
        record: dict[str, Any] = {
            "inputs": [str(clip) for clip in clips], "output": str(out),
            "crossfade_s": 0, "fade_s": 0, "audio": "stream-copy",
            "assembly": "hard cuts with independent source audio tails",
        }
        if dry_run:
            return record
        out.parent.mkdir(parents=True, exist_ok=True)
        concatenate(clips, out)
        record.update(sha256=sha256(out), moov_offset=moov_offset(out), bytes=out.stat().st_size)
        return record
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
    record = {
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
    parser.add_argument("--crossfade", type=float, default=0, help="explicit audio/video crossfade duration")
    parser.add_argument("--fade", type=float, default=0, help="explicit audio/video opening and closing fade duration")
    parser.add_argument("--crf", type=int, default=21)
    parser.add_argument("--record", type=Path, help="write the assembly record JSON here")
    parser.add_argument("--overwrite", action="store_true", help="replace an existing output file")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.record:
            args.record.parent.mkdir(parents=True, exist_ok=True)
        record = assemble(args.clips, args.out, args.crossfade, args.fade, args.crf, args.dry_run, args.overwrite)
    except (ShowreelError, OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    text = json.dumps(record, indent=2)
    if args.record:
        try:
            args.record.write_text(text + "\n")
        except OSError as error:
            print(f"error: could not write record: {error}", file=sys.stderr)
            return 2
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
