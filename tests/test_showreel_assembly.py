import contextlib
import importlib.util
import io
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents/skills/lark-showcase-aigc/scripts/assemble_showreel.py"

spec = importlib.util.spec_from_file_location("assemble_showreel", SCRIPT)
assert spec and spec.loader
showreel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(showreel)


def make_clip(path: Path, seconds: float, audio: bool = True, size: str = "320x180") -> None:
    command = ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"testsrc=size={size}:rate=24:duration={seconds}"]
    if audio:
        command += ["-f", "lavfi", "-i", f"sine=frequency=440:duration={seconds + 0.03}"]
    command += ["-c:v", "libx264", "-pix_fmt", "yuv420p"]
    if audio:
        command += ["-c:a", "aac", "-shortest"]
    command.append(str(path))
    subprocess.run(command, check=True)


def stream_durations(path: Path) -> dict[str, float]:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,duration", "-of", "json", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return {s["codec_type"]: float(s["duration"]) for s in json.loads(result.stdout)["streams"]}


class PlanTests(unittest.TestCase):
    def test_offsets_walk_the_timeline(self) -> None:
        schedule = showreel.plan([8.0, 8.0, 9.5], 0.4, 0.5)
        self.assertEqual(schedule["offsets"], [7.6, 15.2])
        self.assertAlmostEqual(schedule["total"], 24.7)
        self.assertAlmostEqual(schedule["fade_out_start"], 24.2)

    def test_single_clip_is_rejected(self) -> None:
        with self.assertRaises(showreel.ShowreelError):
            showreel.plan([8.0], 0.4, 0.5)

    def test_crossfade_longer_than_half_a_clip_is_rejected(self) -> None:
        with self.assertRaises(showreel.ShowreelError):
            showreel.plan([0.7, 8.0], 0.4, 0.5)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg is not installed")
class AssemblyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def test_assembles_with_locked_sync_and_faststart(self) -> None:
        clips = []
        for index, seconds in enumerate([2.0, 2.0, 3.0]):
            clip = self.tmp / f"c{index}.mp4"
            make_clip(clip, seconds)
            clips.append(clip)
        out = self.tmp / "reel.mp4"
        record = showreel.assemble(clips, out, 0.3, 0.3, 28, dry_run=False)
        durations = stream_durations(out)
        self.assertAlmostEqual(durations["video"], 6.4, delta=0.1)
        self.assertAlmostEqual(durations["audio"], durations["video"], delta=0.05)
        self.assertLess(record["moov_offset"], 100)
        self.assertEqual(len(record["sha256"]), 64)
        decode = subprocess.run(["ffmpeg", "-v", "error", "-i", str(out), "-f", "null", "-"], capture_output=True, text=True, check=False)
        self.assertEqual(decode.stderr.strip(), "")

    def test_clip_without_audio_gets_silence(self) -> None:
        loud = self.tmp / "loud.mp4"
        mute = self.tmp / "mute.mp4"
        make_clip(loud, 2.0)
        make_clip(mute, 2.0, audio=False)
        out = self.tmp / "reel.mp4"
        showreel.assemble([loud, mute], out, 0.3, 0.3, 28, dry_run=False)
        durations = stream_durations(out)
        self.assertIn("audio", durations)
        self.assertAlmostEqual(durations["audio"], durations["video"], delta=0.05)

    def test_dry_run_writes_nothing(self) -> None:
        clips = []
        for index in range(2):
            clip = self.tmp / f"c{index}.mp4"
            make_clip(clip, 2.0)
            clips.append(clip)
        out = self.tmp / "reel.mp4"
        record = showreel.assemble(clips, out, 0.3, 0.3, 28, dry_run=True)
        self.assertFalse(out.exists())
        self.assertIn("-movflags", record["command"])

    def test_missing_input_is_a_clear_error(self) -> None:
        with self.assertRaises(showreel.ShowreelError) as caught:
            showreel.assemble([self.tmp / "nope.mp4", self.tmp / "nope2.mp4"], self.tmp / "o.mp4", 0.3, 0.3, 28, dry_run=True)
        self.assertIn("not found", str(caught.exception))

    def test_existing_output_is_refused_without_overwrite(self) -> None:
        clips = []
        for index in range(2):
            clip = self.tmp / f"c{index}.mp4"
            make_clip(clip, 2.0)
            clips.append(clip)
        out = self.tmp / "reel.mp4"
        out.write_bytes(b"keep me")
        with self.assertRaises(showreel.ShowreelError) as caught:
            showreel.assemble(clips, out, 0.3, 0.3, 28, dry_run=False)
        self.assertIn("--overwrite", str(caught.exception))
        self.assertEqual(out.read_bytes(), b"keep me")
        showreel.assemble(clips, out, 0.3, 0.3, 28, dry_run=False, overwrite=True)
        self.assertGreater(out.stat().st_size, 100)

    def test_record_in_a_new_directory_is_created(self) -> None:
        clips = []
        for index in range(2):
            clip = self.tmp / f"c{index}.mp4"
            make_clip(clip, 2.0)
            clips.append(clip)
        record = self.tmp / "nested" / "deeper" / "record.json"
        args = [str(clips[0]), str(clips[1]), "--out", str(self.tmp / "o.mp4"), "--crossfade", "0.3", "--fade", "0.3", "--crf", "28", "--record", str(record)]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(showreel.main(args), 0)
        self.assertEqual(json.loads(record.read_text())["crossfade_s"], 0.3)

    def test_missing_ffmpeg_is_a_clear_error(self) -> None:
        original = showreel.shutil.which
        showreel.shutil.which = lambda name: None
        try:
            with self.assertRaises(showreel.ShowreelError) as caught:
                showreel.assemble([self.tmp / "a.mp4", self.tmp / "b.mp4"], self.tmp / "o.mp4", 0.3, 0.3, 28, dry_run=True)
        finally:
            showreel.shutil.which = original
        self.assertIn("PATH", str(caught.exception))

    def test_cli_returns_error_code_for_bad_input(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()):
            code = showreel.main([str(self.tmp / "a.mp4"), str(self.tmp / "b.mp4"), "--out", str(self.tmp / "o.mp4")])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
