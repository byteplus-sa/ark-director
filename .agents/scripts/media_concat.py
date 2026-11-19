from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any


def stream_signature(path: Path) -> list[dict[str, Any]]:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries",
            ("stream=codec_type,codec_name,codec_tag_string,profile,width,height,"
             "pix_fmt,time_base,sample_rate,channels,channel_layout,extradata_hash"),
            "-show_data_hash", "sha256", "-of", "json", str(path),
        ],
        capture_output=True, text=True, check=True,
    )
    streams: list[dict[str, Any]] = json.loads(result.stdout)["streams"]
    if not any(stream.get("codec_type") == "video" for stream in streams):
        raise ValueError(f"no video stream in {path}")
    return streams


def concatenate(clips: list[Path], out: Path) -> None:
    if not clips:
        raise ValueError("at least one clip is required")
    paths = [clip.resolve(strict=True) for clip in clips]
    if out.resolve() in paths:
        raise ValueError("output must not overwrite a source")
    signatures = [stream_signature(path) for path in paths]
    if any(signature != signatures[0] for signature in signatures[1:]):
        raise ValueError(
            "stream-copy requires compatible streams; approve a separate "
            "codec or stream-layout adaptation before assembly"
        )
    if any("\n" in str(path) or "\r" in str(path) for path in paths):
        raise ValueError("input paths must not contain line breaks")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".ffconcat") as listing:
        listing.write("ffconcat version 1.0\n")
        for path in paths:
            escaped = str(path).replace("'", "'\\''")
            listing.write(f"file '{escaped}'\n")
        listing.flush()
        subprocess.run(
            [
                "ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                "-i", listing.name, "-map", "0", "-c", "copy",
                "-movflags", "+faststart", str(out),
            ],
            check=True,
        )
