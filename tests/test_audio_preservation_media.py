import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from test_audio_finalization import SKILLS, load_script

HAS_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


def make_clip(path, audio_duration=None, frequency=440, volume=1):
    command = [
        "ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
        "color=c=blue:s=96x160:r=24:d=1",
    ]
    if audio_duration is not None:
        command += [
            "-f", "lavfi", "-i", f"sine=frequency={frequency}:duration={audio_duration}",
            "-af", f"volume={volume}", "-c:a", "aac",
        ]
    subprocess.run(command + ["-c:v", "libx264", "-pix_fmt", "yuv420p", str(path)], check=True)


def audio_packets(path):
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-select_streams", "a:0", "-show_packets",
            "-show_data_hash", "sha256", "-show_entries", "packet=data_hash",
            "-of", "json", str(path),
        ],
        capture_output=True, text=True, check=True,
    )
    return [packet["data_hash"] for packet in json.loads(result.stdout)["packets"]]


def media_streams(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    )
    return {stream["codec_type"]: stream for stream in json.loads(result.stdout)["streams"]}


@unittest.skipUnless(HAS_FFMPEG, "ffmpeg and ffprobe are required")
class AudioPreservationMediaTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="ark-audio-", dir="/tmp")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.showreel = load_script("preservation_showreel", "lark-showcase-aigc/scripts/assemble_showreel.py")
        self.portfolio = load_script("preservation_portfolio", "showcase-html/scripts/portfolio.py")

    def test_both_showreels_keep_all_audio_packets_and_unequal_tails(self):
        for audio_duration in (0.6, 1.4):
            with self.subTest(audio_duration=audio_duration):
                clips = [self.root / f"input {audio_duration}-{index}'s.mp4" for index in range(2)]
                for index, clip in enumerate(clips):
                    make_clip(clip, audio_duration, frequency=440 + 100 * index, volume=0.1 + index)
                expected = audio_packets(clips[0]) + audio_packets(clips[1])
                out = self.root / f"reel-{audio_duration}.mp4"
                self.showreel.assemble(clips, out, 0, 0, 21, False)
                self.assertEqual(audio_packets(out), expected)
                entries = [
                    {"master": clip, "master_sha256": self.portfolio.sha256(clip), "slug": str(index)}
                    for index, clip in enumerate(clips)
                ]
                portfolio_out = self.root / f"portfolio-{audio_duration}.mp4"
                self.portfolio.build_showreel(entries, portfolio_out)
                self.assertEqual(audio_packets(portfolio_out), expected)
                for result in (out, portfolio_out):
                    subprocess.run(["ffmpeg", "-v", "error", "-i", str(result), "-f", "null", "-"], check=True)

    def test_silent_showreels_do_not_synthesize_audio(self):
        clips = [self.root / f"silent{index}.mp4" for index in range(2)]
        for clip in clips:
            make_clip(clip)
        out = self.root / "silent-reel.mp4"
        self.showreel.assemble(clips, out, 0, 0, 21, False)
        self.assertNotIn("audio", media_streams(out))
        entries = [
            {"master": clip, "master_sha256": self.portfolio.sha256(clip), "slug": str(index)}
            for index, clip in enumerate(clips)
        ]
        self.portfolio.build_showreel(entries, self.root / "silent-portfolio.mp4")
        self.assertNotIn("audio", media_streams(self.root / "silent-portfolio.mp4"))

    def test_mixed_stream_layout_requires_explicit_adaptation(self):
        audible, silent = self.root / "audible.mp4", self.root / "silent.mp4"
        make_clip(audible, 1)
        make_clip(silent)
        out = self.root / "mixed.mp4"
        with self.assertRaisesRegex(ValueError, "compatible streams"):
            self.showreel.assemble([audible, silent], out, 0, 0, 21, False)
        self.assertFalse(out.exists())

    def test_explicit_fades_do_not_authorize_padding_or_trimming(self):
        clips = [self.root / f"long{index}.mp4" for index in range(2)]
        for clip in clips:
            make_clip(clip, 1.4)
        with self.assertRaisesRegex(self.showreel.ShowreelError, "spans differ"):
            self.showreel.assemble(clips, self.root / "faded.mp4", 0.2, 0.1, 21, False)

    def test_empty_inputs_and_nonfinite_fades_fail_before_output(self):
        with self.assertRaisesRegex(self.showreel.ShowreelError, "at least two"):
            self.showreel.assemble([], self.root / "empty.mp4", 0, 0, 21, False)
        for value in (-1, float("nan"), float("inf")):
            with self.subTest(value=value), self.assertRaises(self.showreel.ShowreelError):
                self.showreel.plan([1, 1], value, 0)
            with self.subTest(fade=value), self.assertRaises(self.showreel.ShowreelError):
                self.showreel.plan([1, 1], 0, value)

    @unittest.skipUnless(importlib.util.find_spec("PIL"), "Pillow inline dependency is required")
    def test_avatar_cli_keeps_audio_packets_tail_and_silence(self):
        candidates = [
            os.environ.get("AUDIO_SMOKE_FONT", ""),
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
        font = next((path for path in candidates if Path(path).is_file()), None)
        if font is None:
            self.skipTest("set AUDIO_SMOKE_FONT to a readable font")
        for audio_duration in (None, 0.6, 1.4):
            with self.subTest(audio_duration=audio_duration):
                take = self.root / f"avatar-{audio_duration}.mp4"
                make_clip(take, audio_duration)
                out = self.root / f"delivery-{audio_duration}.mp4"
                words = self.root / "words.json"
                words.write_text('{"words":[]}')
                config = self.root / "edit.json"
                config.write_text(json.dumps({
                    "take": str(take), "stt": str(words), "out": str(out), "font": font,
                    "end": 1, "segments": [{"start": 0, "end": 1, "layout": "full_m"}],
                    "chunks": [],
                }))
                subprocess.run([
                    sys.executable, str(SKILLS / "seedance-avatar-news/scripts/render_short.py"),
                    str(config),
                ], capture_output=True, text=True, check=True)
                self.assertEqual(audio_packets(out), audio_packets(take))
                streams = media_streams(out)
                self.assertAlmostEqual(float(streams["video"]["duration"]), 1, delta=0.04)
                if audio_duration is None:
                    self.assertNotIn("audio", streams)
                else:
                    self.assertAlmostEqual(float(streams["audio"]["duration"]), audio_duration, delta=0.03)
                subprocess.run(["ffmpeg", "-v", "error", "-i", str(out), "-f", "null", "-"], check=True)


if __name__ == "__main__":
    unittest.main()
