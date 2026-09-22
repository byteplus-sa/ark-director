#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow>=10"]
# ///
"""Render a 1080x1920 avatar news short from a talking-head take, B-roll and an edit decision list."""

import argparse
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

W, H, HALF = 1080, 1920, 960
FPS_EXPR = "30000/1001"
FPS = 30000 / 1001
LAYOUTS = {"full_m", "full_mz", "full_b", "split", "card"}
CAPTION_Y = {"split": 960, "full": 1350, "card": 1500}
FONT_CANDIDATES = [
    ("/System/Library/Fonts/HelveticaNeue.ttc", 1),
    ("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 0),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 0),
]


def font(size):
    for path, index in FONT_CANDIDATES:
        if os.path.exists(path):
            return ImageFont.truetype(path, size, index=index)
    return ImageFont.load_default(size)


def pill(text, fnt, pad, fill, radius, outline=None):
    left, top, right, bottom = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), text, font=fnt)
    w, h = right - left + 2 * pad[0], bottom - top + 2 * pad[1]
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius if radius is not None else h // 2, fill=fill, outline=outline, width=2)
    d.text((pad[0] - left, pad[1] - top), text, font=fnt, fill=(255, 255, 255, 255))
    return im


def run(args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        check=True, capture_output=True, text=True,
    )
    return float(out.stdout.strip())


def frame_count(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", path],
        check=True, capture_output=True, text=True,
    )
    return int(out.stdout.strip())


def cover(w, h, fx=0.5, fy=0.5):
    return f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}:(iw-{w})*{fx}:(ih-{h})*{fy}"


def layout_class(layout):
    return "split" if layout == "split" else ("card" if layout == "card" else "full")


def validate(cfg, words):
    errors = []
    segs, end = cfg["segments"], cfg["end"]
    take_len = duration(cfg["take"])
    if end > take_len + 0.05:
        errors.append(f"end {end}s exceeds take length {take_len:.2f}s")
    cursor = 0.0
    for i, seg in enumerate(segs):
        if seg["layout"] not in LAYOUTS:
            errors.append(f"segment {i}: unknown layout {seg['layout']}")
        if abs(seg["start"] - cursor) > 1e-3:
            errors.append(f"segment {i}: starts at {seg['start']}s, expected {cursor:.3f}s (segments must tile 0 -> end)")
        if seg["end"] <= seg["start"]:
            errors.append(f"segment {i}: end must be after start")
        cursor = seg["end"]
        if seg["layout"] in ("split", "full_b"):
            clip = seg.get("clip")
            if not clip or not os.path.exists(clip):
                errors.append(f"segment {i}: clip not found: {clip}")
                continue
            need = seg.get("offset", 0) + (seg["end"] - seg["start"]) * seg.get("speed", 1)
            have = duration(clip)
            if need > have + 0.05:
                errors.append(f"segment {i}: clip {os.path.basename(clip)} is {have:.2f}s but needs {need:.2f}s (offset + duration x speed)")
    if abs(cursor - end) > 1e-3:
        errors.append(f"segments end at {cursor:.3f}s but end is {end}s")
    last = -1
    for k, (a, b, _) in enumerate(cfg["chunks"]):
        if not (0 <= a <= b < len(words)):
            errors.append(f"chunk {k}: word indices {a}-{b} outside 0-{len(words) - 1}")
        elif a <= last:
            errors.append(f"chunk {k}: word {a} overlaps the previous chunk")
        last = b
    return errors


def build_segments(cfg, work):
    take, fy = cfg["take"], cfg.get("take_focus_y", 0.3)
    sy = cfg.get("take_split_focus_y", 0.05)
    files = []
    for i, seg in enumerate(cfg["segments"]):
        f0, f1 = round(seg["start"] * FPS), round(seg["end"] * FPS)
        n, start = f1 - f0, f0 / FPS
        dur = n / FPS + 0.2
        out = os.path.join(work, f"seg_{i:02d}.mp4")
        enc = ["-frames:v", str(n), "-an", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", FPS_EXPR]
        take_in = ["-ss", f"{start:.3f}", "-t", f"{dur:.3f}", "-i", take]
        layout = seg["layout"]
        if layout in ("split", "full_b"):
            trim = seg.get("crop_bottom_frac", 0)
            pre = f"crop=iw:ih*{1 - trim}:0:0," if trim else ""
            speed = seg.get("speed", 1)
            retime = f"setpts=PTS/{speed}," if speed != 1 else ""
            clip_in = ["-ss", f"{seg.get('offset', 0):.3f}", "-t", f"{dur * speed:.3f}", "-i", seg["clip"]]
            fx = seg.get("focus_x", 0.5)
        if layout == "full_m":
            run(take_in + ["-vf", f"fps={FPS_EXPR},{cover(W, H, 0.5, fy)},setsar=1"] + enc + [out])
        elif layout == "full_mz":
            run(take_in + ["-vf", f"fps={FPS_EXPR},{cover(int(W * 1.12), int(H * 1.12), 0.5, fy)},crop={W}:{H},setsar=1"] + enc + [out])
        elif layout == "full_b":
            run(clip_in + ["-vf", f"{pre}{retime}fps={FPS_EXPR},{cover(W, H, fx)},setsar=1"] + enc + [out])
        elif layout == "split":
            graph = (
                f"[0:v]{pre}{retime}fps={FPS_EXPR},{cover(W, HALF, fx)},setsar=1[t];"
                f"[1:v]fps={FPS_EXPR},{cover(W, HALF, 0.5, sy)},setsar=1[b];[t][b]vstack=2[v]"
            )
            run(clip_in + take_in + ["-filter_complex", graph, "-map", "[v]"] + enc + [out])
        elif layout == "card":
            cw, ch = 920, 818
            mask = Image.new("L", (cw, ch), 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, cw - 1, ch - 1], radius=44, fill=255)
            mask_path = os.path.join(work, "card_mask.png")
            mask.save(mask_path)
            border = Image.new("RGBA", (cw + 12, ch + 12), (0, 0, 0, 0))
            ImageDraw.Draw(border).rounded_rectangle([0, 0, cw + 11, ch + 11], radius=50, outline=(255, 255, 255, 110), width=3)
            border_path = os.path.join(work, "card_border.png")
            border.save(border_path)
            x, y = (W - cw) // 2, (H - ch) // 2
            graph = (
                f"[0:v]fps={FPS_EXPR},{cover(cw, ch, 0.5, fy)},format=rgba[m];[m][1:v]alphamerge[c];"
                f"color=c=black:s={W}x{H}:r={FPS_EXPR}:d={dur:.3f}[bg];[bg][c]overlay={x}:{y}[x];"
                f"[x][2:v]overlay={x - 6}:{y - 6},format=yuv420p,setsar=1[v]"
            )
            run(take_in + ["-i", mask_path, "-i", border_path, "-filter_complex", graph, "-map", "[v]"] + enc + [out])
        got = frame_count(out)
        if got != n:
            raise RuntimeError(f"segment {i}: rendered {got} frames, expected {n}")
        files.append(out)
    listing = os.path.join(work, "list.txt")
    with open(listing, "w") as fh:
        fh.writelines(f"file '{f}'\n" for f in files)
    video = os.path.join(work, "video_nocap.mp4")
    run(["-f", "concat", "-safe", "0", "-i", listing, "-c", "copy", video])
    return video


def build_cues(cfg, words):
    segs, end = cfg["segments"], cfg["end"]
    chunks = cfg["chunks"]
    cues = []
    for k, (a, b, text) in enumerate(chunks):
        st, word_end = words[a][1] / 1000, words[b][2] / 1000
        nxt = words[chunks[k + 1][0]][1] / 1000 if k + 1 < len(chunks) else end
        en = min(nxt, word_end + 0.45) if nxt - word_end > 0.6 else nxt
        seg = next((s for s in segs if s["start"] <= st + 0.02 < s["end"]), segs[-1])
        following = [s for s in segs if s["start"] >= seg["end"] - 1e-6]
        if following and layout_class(following[0]["layout"]) != layout_class(seg["layout"]):
            en = min(en, seg["end"])
        cues.append({"text": text.upper(), "start": round(st, 3), "end": round(min(en, end), 3), "y": CAPTION_Y[layout_class(seg["layout"])]})
    return cues


def build_graphics(cfg, cues, work):
    big, small = font(64), font(26)
    paths = []
    for i, cue in enumerate(cues):
        p = os.path.join(work, f"cap_{i:03d}.png")
        pill(cue["text"], big, (30, 16), (10, 10, 12, 175), 22).save(p)
        paths.append(p)
    header = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    style = {"pad": (22, 12), "fill": (20, 20, 24, 120), "radius": None, "outline": (255, 255, 255, 70)}
    if cfg.get("sources_label"):
        header.alpha_composite(pill(f"Sources: {cfg['sources_label']}", small, **style), (48, 70))
    if cfg.get("channel_label"):
        right = pill(cfg["channel_label"], small, **style)
        header.alpha_composite(right, (W - 48 - right.width, 70))
    header_path = os.path.join(work, "header.png")
    header.save(header_path)
    return paths, header_path


def resolve_paths(cfg, base):
    for key in ("take", "stt", "out", "clips_dir"):
        if cfg.get(key):
            cfg[key] = os.path.normpath(os.path.join(base, cfg[key]))
    clips_dir = cfg.get("clips_dir") or base
    for seg in cfg["segments"]:
        if seg.get("clip"):
            seg["clip"] = os.path.normpath(os.path.join(clips_dir, seg["clip"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", help="Edit decision list JSON (see references/edit-recipes.md)")
    args = parser.parse_args()
    with open(args.config) as fh:
        cfg = json.load(fh)
    resolve_paths(cfg, os.path.dirname(os.path.abspath(args.config)))
    with open(cfg["stt"]) as fh:
        words = json.load(fh)["words"]
    errors = validate(cfg, words)
    if errors:
        sys.exit("Invalid EDL:\n  " + "\n  ".join(errors))
    with tempfile.TemporaryDirectory(prefix="avatar_short_") as work:
        video = build_segments(cfg, work)
        cues = build_cues(cfg, words)
        caps, header = build_graphics(cfg, cues, work)
        inputs = ["-i", video, "-i", cfg["take"], "-i", header]
        graph, prev = "[0:v][2:v]overlay=0:0[v0]", "v0"
        for i, (cue, cap) in enumerate(zip(cues, caps)):
            w, h = Image.open(cap).size
            inputs += ["-i", cap]
            graph += f";[{prev}][{i + 3}:v]overlay={(W - w) // 2}:{cue['y'] - h // 2}:enable='between(t,{cue['start']},{cue['end'] - 0.001})'[v{i + 1}]"
            prev = f"v{i + 1}"
        end = cfg["end"]
        run(inputs + [
            "-filter_complex", graph, "-map", f"[{prev}]", "-map", "1:a", "-t", str(end),
            "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", FPS_EXPR,
            "-af", f"loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={end - 0.25}:d=0.25",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", cfg["out"],
        ])
    with open(os.path.splitext(cfg["out"])[0] + "_cues.json", "w") as fh:
        json.dump(cues, fh, indent=1)
    print(cfg["out"])


if __name__ == "__main__":
    main()
