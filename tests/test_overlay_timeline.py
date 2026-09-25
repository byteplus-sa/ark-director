from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents/skills/html-graphic-render/scripts/overlay_timeline.py"
SPEC = importlib.util.spec_from_file_location("overlay_timeline", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

HAS_FFMPEG = shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None
INFO = MODULE.MediaInfo(fps="24/1", width=720, height=1280, duration=10.0, has_audio=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class OverlayTimelineArgumentTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory(prefix="overlay-timeline-test-")
        self.addCleanup(directory.cleanup)
        self.project = Path(directory.name)

    def timeline(self, **values: Any) -> dict[str, Any]:
        raw: dict[str, Any] = {
            "schema_version": 1,
            "base": "base.mp4",
            "output": "finish/fin_v01.mp4",
            "layers": [{"src": "o/a.png", "start": 0, "end": None}],
        }
        raw.update(values)
        return dict(MODULE.validate_timeline(raw, INFO.duration))

    def command(self, **values: Any) -> list[str]:
        return list(MODULE.build_command(self.timeline(**values), self.project, INFO))

    def graph(self, command: list[str]) -> str:
        return command[command.index("-filter_complex") + 1]

    def test_fades_and_enable_windows(self) -> None:
        graph = self.graph(
            self.command(
                layers=[
                    {"src": "o/a.png", "start": 0, "end": None},
                    {"src": "o/b.png", "start": 2.375, "end": 7.13, "fade_in": 0.08, "fade_out": 0.08},
                ]
            )
        )
        self.assertIn("enable='gte(t,0)'", graph)
        self.assertIn("enable='between(t,2.375,7.13)'", graph)
        self.assertIn("fade=t=in:st=2.375:d=0.08:alpha=1", graph)
        self.assertIn("fade=t=out:st=7.05:d=0.08:alpha=1", graph)
        self.assertIn("[v1]format=yuv420p[vout]", graph)

    def test_full_frame_defaults_to_origin(self) -> None:
        graph = self.graph(self.command())
        self.assertIn("overlay=x='0':y='0'", graph)
        self.assertNotIn("scale=", graph)

    def test_rise_expression(self) -> None:
        graph = self.graph(
            self.command(
                layers=[{"src": "o/a.png", "start": 7.45, "y": 900, "rise_px": 60, "rise_s": 0.15}]
            )
        )
        self.assertIn("y='900+60*(1-min(1,max(0,(t-7.45)/0.15)))'", graph)

    def test_center_and_width(self) -> None:
        graph = self.graph(
            self.command(
                layers=[{"src": "o/a.png", "start": 0, "end": None, "x": "center", "y": 24, "width": 250}]
            )
        )
        self.assertIn("scale=250:-1", graph)
        self.assertIn("overlay=x='(W-w)/2':y='24'", graph)

    def test_fade_to_black(self) -> None:
        graph = self.graph(self.command(fade_to_black={"start": 9.7, "duration": 0.3}))
        self.assertIn("fade=t=out:st=9.7:d=0.3,format=yuv420p[vout]", graph)

    def test_video_encoding_and_duration(self) -> None:
        command = self.command(duration=8.5)
        for fragment in (
            ["-c:v", "libx264"],
            ["-crf", "17"],
            ["-pix_fmt", "yuv420p"],
            ["-movflags", "+faststart"],
            ["-framerate", "24/1"],
            ["-t", "8.5"],
        ):
            joined = " ".join(command)
            self.assertIn(" ".join(fragment), joined)
        self.assertIn("-n", command)
        self.assertIn("-y", MODULE.build_command(self.timeline(), self.project, INFO, True))

    def test_audio_copy(self) -> None:
        command = " ".join(self.command())
        self.assertIn("-map 0:a:0 -c:a copy", command)

    def test_audio_copy_with_silent_base(self) -> None:
        silent = MODULE.MediaInfo("24/1", 720, 1280, 10.0, False)
        command = MODULE.build_command(self.timeline(), self.project, silent)
        self.assertIn("-an", command)

    def test_audio_none(self) -> None:
        command = self.command(audio="none")
        self.assertIn("-an", command)
        self.assertNotIn("0:a:0", command)

    def test_audio_path(self) -> None:
        command = " ".join(self.command(audio={"path": "audio/bed.wav"}))
        self.assertIn(str(self.project.resolve() / "audio/bed.wav"), command)
        self.assertIn("-map 2:a:0 -c:a aac -b:a 192k", command)

    def test_loudnorm(self) -> None:
        command = " ".join(self.command(loudnorm={"i": -14, "tp": -1.5}))
        self.assertIn("-map 0:a:0 -af loudnorm=I=-14:TP=-1.5 -c:a aac", command)
        with self.assertRaises(ValueError):
            self.timeline(audio="none", loudnorm={"i": -14, "tp": -1.5})

    def test_validation_errors(self) -> None:
        bad_layers: list[dict[str, Any]] = [
            {"src": "o/a.png", "start": 2, "end": 1},
            {"src": "o/a.png", "start": 0, "fade_out": 0.1},
            {"src": "o/a.png", "start": 0, "end": 0.1, "fade_in": 0.1, "fade_out": 0.1},
            {"src": "o/a.png", "start": 0, "x": "left"},
            {"src": "o/a.png", "start": 0, "width": 0},
            {"src": "o/a.png", "start": 0, "opacity": 1},
            {"src": "o/a.png", "start": 11},
        ]
        for layer in bad_layers:
            with self.subTest(layer=layer), self.assertRaises(ValueError):
                self.timeline(layers=[layer])
        with self.assertRaises(ValueError):
            self.timeline(audio="mix")
        with self.assertRaises(ValueError):
            self.timeline(schema_version=2)

    def test_containment_rejection(self) -> None:
        outside = tempfile.TemporaryDirectory(prefix="overlay-outside-")
        self.addCleanup(outside.cleanup)
        (self.project / "escape").symlink_to(outside.name)
        for value in ("../x.png", "/etc/passwd", "o/../../x.png", "escape/x.png", ""):
            with self.subTest(value=value), self.assertRaises(ValueError):
                MODULE.project_path(self.project, value, "layer")
        with self.assertRaises(ValueError):
            MODULE.build_command(
                self.timeline(layers=[{"src": "../x.png", "start": 0}]), self.project, INFO
            )
        with self.assertRaises(ValueError):
            MODULE.build_command(self.timeline(output="escape/fin.mp4"), self.project, INFO)


@unittest.skipUnless(HAS_FFMPEG, "ffmpeg/ffprobe unavailable")
class OverlayTimelineRenderTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory(prefix="overlay-timeline-render-")
        self.addCleanup(directory.cleanup)
        self.project = Path(directory.name)
        (self.project / "o").mkdir()
        self.ffmpeg(
            "-f", "lavfi", "-i", "testsrc=s=160x284:r=24:d=1.5",
            "-f", "lavfi", "-i", "sine=d=1.5",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest",
            str(self.project / "base.mp4"),
        )
        self.ffmpeg(
            "-f", "lavfi", "-i", "color=c=red@0.6:s=80x40,format=rgba",
            "-frames:v", "1", str(self.project / "o/layer.png"),
        )
        self.write_timeline(
            {
                "schema_version": 1,
                "base": "base.mp4",
                "output": "finish/fin_v01.mp4",
                "duration": 1.2,
                "layers": [
                    {"src": "o/layer.png", "start": 0, "end": None, "x": "center", "y": 8, "width": 60},
                    {"src": "o/layer.png", "start": 0.2, "end": 1.0, "fade_in": 0.1, "fade_out": 0.1},
                    {"src": "o/layer.png", "start": 0.4, "y": 120, "rise_px": 30, "rise_s": 0.2},
                ],
                "fade_to_black": {"start": 0.9, "duration": 0.3},
                "loudnorm": {"i": -14, "tp": -1.5},
            }
        )

    def ffmpeg(self, *arguments: str) -> None:
        subprocess.run(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *arguments],
            check=True,
            capture_output=True,
        )

    def write_timeline(self, data: dict[str, Any]) -> None:
        (self.project / "timeline.json").write_text(json.dumps(data), encoding="utf-8")

    def namespace(self, **values: object) -> argparse.Namespace:
        defaults: dict[str, object] = {
            "project": self.project,
            "timeline": "timeline.json",
            "run": False,
            "overwrite": False,
            "preview": None,
            "at": None,
            "background": None,
        }
        defaults.update(values)
        return argparse.Namespace(**defaults)

    def test_dry_run_prints_command_without_output(self) -> None:
        result = MODULE.execute(self.namespace())
        self.assertIsInstance(result, str)
        self.assertTrue(str(result).startswith("ffmpeg "))
        self.assertFalse((self.project / "finish").exists())

    def test_run_writes_output_and_sidecar(self) -> None:
        result = MODULE.execute(self.namespace(run=True))
        output = self.project / "finish/fin_v01.mp4"
        sidecar = self.project / "finish/overlay_fin_v01.json"
        self.assertTrue(output.is_file())
        self.assertEqual(result["record"], "finish/overlay_fin_v01.json")
        record = json.loads(sidecar.read_text(encoding="utf-8"))
        self.assertAlmostEqual(record["output"]["duration_s"], 1.2, delta=0.1)
        self.assertEqual(record["output"]["sha256"], sha256(output))
        self.assertEqual(record["output"]["bytes"], output.stat().st_size)
        self.assertEqual((record["output"]["width"], record["output"]["height"]), (160, 284))
        self.assertEqual(record["output"]["fps"], "24/1")
        self.assertTrue(record["output"]["has_audio"])
        self.assertEqual(record["base"]["sha256"], sha256(self.project / "base.mp4"))
        self.assertEqual(record["timeline"]["sha256"], sha256(self.project / "timeline.json"))
        self.assertEqual(
            [layer["sha256"] for layer in record["layers"]],
            [sha256(self.project / "o/layer.png")] * 3,
        )
        self.assertTrue(record["ffmpeg_version"].startswith("ffmpeg version"))

    def test_run_refuses_overwrite(self) -> None:
        MODULE.execute(self.namespace(run=True))
        output = self.project / "finish/fin_v01.mp4"
        before = sha256(output)
        with self.assertRaises(ValueError):
            MODULE.execute(self.namespace(run=True))
        self.assertEqual(sha256(output), before)
        MODULE.execute(self.namespace(run=True, overwrite=True))
        self.assertTrue(output.is_file())

    def test_preview_writes_png(self) -> None:
        for name, values in (
            ("pv_base.png", {"at": 0.5}),
            ("pv_solid.png", {"at": 0.5, "background": "0x2A2A2A"}),
            ("pv_default.png", {}),
        ):
            with self.subTest(name=name):
                result = MODULE.execute(self.namespace(preview=name, **values))
                target = self.project / name
                self.assertTrue(target.is_file())
                self.assertEqual(target.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
                self.assertEqual(result["sha256"], sha256(target))
        with self.assertRaises(ValueError):
            MODULE.execute(self.namespace(preview="pv_base.png", at=0.5))
        with self.assertRaises(ValueError):
            MODULE.execute(self.namespace(preview="../pv.png"))


if __name__ == "__main__":
    unittest.main()
