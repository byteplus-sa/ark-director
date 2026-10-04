from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents/skills/seedance-frame-break/scripts/measure_frame_break.py"
SPEC = importlib.util.spec_from_file_location("measure_frame_break", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

FFMPEG_AVAILABLE = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))
WIDTH, HEIGHT = 640, 360


def box(x: str, y: str, w: str, h: str, colour: str, enable: str = "") -> str:
    suffix = f":enable='{enable}'" if enable else ""
    return f"drawbox=x={x}:y={y}:w={w}:h={h}:color={colour}:t=fill{suffix}"


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    width, height = struct.unpack(">II", data[16:24])
    return width, height


@unittest.skipUnless(
    FFMPEG_AVAILABLE, "ffmpeg and ffprobe are required for frame-break measurement tests"
)
class FrameBreakMeasureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory(prefix="frame-break-test-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def clip(
        self,
        name: str,
        filters: list[str],
        duration: int = 3,
        rate: int = 10,
        codec: tuple[str, ...] = ("-c:v", "ffv1"),
    ) -> Path:
        path = self.root / name
        subprocess.run(
            [
                "ffmpeg", "-v", "error", "-y", "-f", "lavfi",
                "-i", f"color=c=0x3a7bd5:s={WIDTH}x{HEIGHT}:r={rate}:d={duration}",
                "-vf", ",".join(filters), "-pix_fmt", "yuv420p", *codec, str(path),
            ],
            check=True,
        )
        return path

    def args(self, video: Path, **values: object) -> argparse.Namespace:
        namespace = MODULE.parser().parse_args([str(video)])
        for key, value in values.items():
            setattr(namespace, key, value)
        return namespace

    def measure(self, video: Path, **values: object) -> dict[str, Any]:
        return MODULE.measure(self.args(video, **values))

    def bars(self, top: int, bottom: int, extra: list[str] | None = None) -> list[str]:
        return [
            box("0", "0", "iw", str(top), "black"),
            box("0", f"ih-{bottom}", "iw", str(bottom), "black"),
            *(extra or []),
        ]

    def kinds(self, result: dict[str, Any], bar: str, key: str = "violations") -> set[str]:
        return {v["kind"] for v in result["summary"][bar][key]}

    def gate(self, result: dict[str, Any]) -> dict[str, Any]:
        return result["summary"]["static_bar_gate"]

    def test_static_equal_bars_without_overlap_pass_the_gate(self) -> None:
        result = self.measure(self.clip("static.mkv", self.bars(43, 43)))
        summary = result["summary"]
        self.assertEqual(result["height"], HEIGHT)
        self.assertEqual(result["sample_fps"], 10)
        self.assertEqual(summary["frames_scanned"], 30)
        for name in ("top", "bottom"):
            self.assertEqual(summary[name]["thickness_px"]["median"], 43)
            self.assertAlmostEqual(summary[name]["thickness_pct"]["median"], 11.944, places=2)
            self.assertEqual(summary[name]["status"], "pass")
            self.assertEqual(summary[name]["max_far_encroach_px"], 0)
            self.assertEqual(summary[name]["max_far_retreat_px"], 0)
            self.assertEqual(summary[name]["static_tilt_px"], 0)
            self.assertEqual(summary[name]["frames_with_overlap"], 0)
        self.assertTrue(summary["bars_detected"])
        self.assertEqual(self.gate(result)["status"], "pass")
        self.assertEqual(self.gate(result)["violations"], [])
        self.assertEqual(self.gate(result)["inspect"], [])
        self.assertFalse(summary["top_bottom_differ"])
        self.assertEqual(result["overlap_intervals"], [])
        self.assertEqual(summary["break_out_gate"]["status"], "absent")
        self.assertEqual(summary["verdict"]["status"], "fail")
        self.assertFalse(summary["verdict"]["passed"])
        self.assertIn("no_overlap", summary["flags"])
        self.assertIn("top_bar_never_crossed", summary["flags"])

    def test_default_scans_every_native_frame(self) -> None:
        video = self.clip("native.mkv", self.bars(43, 43), duration=2, rate=24)
        result = self.measure(video)
        self.assertEqual(result["native_fps"], 24)
        self.assertEqual(result["sample_fps"], 24)
        self.assertEqual(result["summary"]["frames_scanned"], 48)
        coarse = self.measure(video, fps=4)
        self.assertEqual(coarse["summary"]["frames_scanned"], 8)

    def test_h264_clip_passes_the_gate(self) -> None:
        video = self.clip(
            "static.mp4", self.bars(43, 43), codec=("-c:v", "libx264", "-crf", "14")
        )
        result = self.measure(video)
        for name in ("top", "bottom"):
            self.assertLessEqual(abs(result["summary"][name]["thickness_px"]["median"] - 43), 1)
        self.assertEqual(self.gate(result)["status"], "pass", self.gate(result))

    def test_subject_covering_a_bar_with_static_far_columns_passes(self) -> None:
        crossing = box("240", "20", "160", "100", "red", "between(t,1,1.95)")
        result = self.measure(self.clip("overlap.mkv", self.bars(43, 43, [crossing])))
        self.assertEqual(len(result["overlap_intervals"]), 1)
        interval = result["overlap_intervals"][0]
        self.assertEqual(interval["bar"], "top")
        self.assertAlmostEqual(interval["start_s"], 1.0, places=2)
        self.assertAlmostEqual(interval["end_s"], 1.9, places=2)
        self.assertEqual(interval["frames"], 10)
        self.assertGreater(interval["peak_fraction"], 0.1)
        summary = result["summary"]
        self.assertEqual(summary["top"]["frames_with_overlap"], 10)
        self.assertEqual(summary["bottom"]["frames_with_overlap"], 0)
        self.assertNotIn("top_bar_never_crossed", summary["flags"])
        self.assertIn("bottom_bar_never_crossed", summary["flags"])
        self.assertEqual(self.gate(result)["status"], "pass", self.gate(result))
        self.assertTrue(self.gate(result)["passed"])
        self.assertFalse(self.gate(result)["needs_review"])
        verdict = result["summary"]["verdict"]
        self.assertEqual(verdict["status"], "pass")
        self.assertTrue(verdict["passed"])
        self.assertFalse(verdict["needs_review"])
        before = [f for f in result["frames"] if f["time_s"] < 1.0]
        self.assertTrue(all(f["top"]["overlap_fraction"] == 0 for f in before))
        self.assertEqual(summary["break_out_gate"]["status"], "pass")

    def test_dark_subject_over_the_bar_does_not_fail(self) -> None:
        dark = box("200", "30", "240", "90", "black", "between(t,1,1.95)")
        result = self.measure(self.clip("dark.mkv", self.bars(43, 43, [dark])))
        self.assertNotEqual(self.gate(result)["status"], "fail", self.gate(result))
        self.assertEqual(self.gate(result)["violations"], [])

    def test_narrow_dark_block_merging_with_the_bar_is_inspect_not_fail(self) -> None:
        merge = box("300", "ih-103", "40", "60", "black", "between(t,1,1.95)")
        result = self.measure(self.clip("merge.mkv", self.bars(43, 43, [merge])))
        gate = self.gate(result)
        self.assertEqual(gate["status"], "inspect", gate)
        self.assertFalse(gate["passed"])
        self.assertTrue(gate["needs_review"])
        self.assertEqual(self.kinds(result, "bottom", "inspect"), {"dark_merge"})
        record = result["summary"]["bottom"]["inspect"][0]
        self.assertAlmostEqual(record["start_s"], 1.0, places=2)
        self.assertGreaterEqual(record["peak_px"], 50)

    def test_subject_over_a_far_column_is_inspect_not_fail(self) -> None:
        cover = box("0", "ih-60", "90", "50", "red", "between(t,1,1.95)")
        result = self.measure(self.clip("far.mkv", self.bars(43, 43, [cover])))
        gate = self.gate(result)
        self.assertEqual(gate["status"], "inspect", gate)
        self.assertFalse(gate["passed"])
        self.assertTrue(gate["needs_review"])
        self.assertIn("far_retreat", self.kinds(result, "bottom", "inspect"))
        self.assertEqual(gate["violations"], [])
        self.assertFalse(result["summary"]["verdict"]["passed"])

    def test_whole_edge_encroaching_into_the_window_fails(self) -> None:
        grow = box("0", "ih-62", "iw", "19", "black", "between(t,1,1.95)")
        result = self.measure(self.clip("grow.mkv", self.bars(43, 43, [grow])))
        gate = self.gate(result)
        self.assertEqual(gate["status"], "fail")
        self.assertFalse(gate["passed"])
        self.assertTrue({"encroach", "jump"} <= self.kinds(result, "bottom"))
        encroach = [v for v in result["summary"]["bottom"]["violations"] if v["kind"] == "encroach"]
        self.assertEqual(len(encroach), 1)
        self.assertAlmostEqual(encroach[0]["start_s"], 1.0, places=2)
        self.assertAlmostEqual(encroach[0]["end_s"], 1.9, places=2)
        self.assertEqual(encroach[0]["peak_px"], 19)
        self.assertTrue(result["summary"]["top"]["status"] == "pass")
        self.assertIn("bottom_bar_moves", result["summary"]["flags"])
        self.assertNotIn("top_bar_moves", result["summary"]["flags"])

    def test_smooth_interior_bow_with_static_far_columns_fails(self) -> None:
        bow = "geq=lum='if(gt(Y,H-43-14*max(0,1-pow((X-W/2)/(0.4*W),2))),16,lum(X,Y))':cb=128:cr=128"
        result = self.measure(self.clip("bow.mkv", [*self.bars(43, 43), bow]))
        summary = result["summary"]
        self.assertEqual(summary["bottom"]["max_far_encroach_px"], 0)
        self.assertGreaterEqual(summary["bottom"]["max_interior_encroach_px"], 12)
        self.assertEqual(self.kinds(result, "bottom"), {"bow_in"})
        self.assertEqual(self.gate(result)["status"], "fail")
        self.assertEqual(summary["top"]["status"], "pass")

    def test_narrow_interior_step_is_not_a_bar_shape(self) -> None:
        step = box("iw/3", "ih-53", "iw/6", "10", "black")
        result = self.measure(self.clip("step.mkv", self.bars(43, 43, [step])))
        self.assertEqual(self.gate(result)["status"], "inspect")
        self.assertEqual(self.kinds(result, "bottom", "inspect"), {"dark_merge"})
        self.assertFalse(self.gate(result)["passed"])

    def test_left_half_thickening_reports_its_interval(self) -> None:
        tilt = box("0", "ih-62", "iw/2", "19", "black", "between(t,1,1.95)")
        result = self.measure(self.clip("timed_tilt.mkv", self.bars(43, 43, [tilt])))
        records = [v for v in result["summary"]["bottom"]["violations"] if v["kind"] == "encroach"]
        self.assertEqual(len(records), 1)
        self.assertAlmostEqual(records[0]["start_s"], 1.0, places=2)
        self.assertAlmostEqual(records[0]["end_s"], 1.9, places=2)
        self.assertEqual(records[0]["peak_px"], 19)
        self.assertFalse(self.gate(result)["passed"])

    def test_static_sloped_bar_is_inspect_not_fail(self) -> None:
        slope = "geq=lum='if(gt(Y,H-43-18*X/W),16,lum(X,Y))':cb=128:cr=128"
        result = self.measure(self.clip("tilt.mkv", [box("0", "0", "iw", "43", "black"), slope]))
        bottom = result["summary"]["bottom"]
        self.assertLessEqual(abs(result["frames"][0]["bottom"]["left_px"] - 43), 1)
        self.assertGreaterEqual(result["frames"][0]["bottom"]["right_px"], 60)
        self.assertGreaterEqual(abs(bottom["static_tilt_px"]), 16)
        self.assertEqual(self.kinds(result, "bottom", "inspect"), {"static_tilt"})
        self.assertEqual(bottom["violations"], [])
        self.assertEqual(self.gate(result)["status"], "inspect")
        self.assertFalse(self.gate(result)["passed"])

    def test_six_frame_edge_jump_at_24_fps_is_caught(self) -> None:
        jump = box("0", "ih-62", "iw", "19", "black", "between(t,1.5,1.74)")
        video = self.clip("jump.mkv", self.bars(43, 43, [jump]), duration=3, rate=24)
        result = self.measure(video)
        bottom = result["summary"]["bottom"]
        self.assertEqual(bottom["status"], "fail")
        self.assertEqual(bottom["thickness_px"]["min"], 43)
        self.assertEqual(bottom["thickness_px"]["max"], 62)
        encroach = [v for v in bottom["violations"] if v["kind"] == "encroach"]
        self.assertEqual(len(encroach), 1)
        self.assertEqual(encroach[0]["frames"], 6)
        self.assertAlmostEqual(encroach[0]["start_s"], 1.5, places=3)
        self.assertAlmostEqual(encroach[0]["end_s"], 1.7083, places=3)
        jumps = [v for v in bottom["violations"] if v["kind"] == "jump"]
        self.assertEqual(len(jumps), 2)
        self.assertEqual(jumps[0]["peak_px"], 19)
        self.assertIn("bottom_bar_moves", result["summary"]["flags"])
        self.assertNotIn("top_bar_moves", result["summary"]["flags"])
        self.assertFalse(self.gate(result)["passed"])
        coarse = self.measure(video, fps=1)
        self.assertEqual(coarse["summary"]["bottom"]["status"], "pass")

    def test_tolerances_can_be_relaxed(self) -> None:
        jump = box("0", "ih-47", "iw", "4", "black", "between(t,1,1.5)")
        video = self.clip("small_jump.mkv", self.bars(43, 43, [jump]))
        self.assertFalse(self.gate(self.measure(video))["passed"])
        relaxed = self.measure(video, edge_tolerance_px=5.0, jump_threshold_px=5.0)
        self.assertTrue(self.gate(relaxed)["passed"])

    def test_thin_bars_are_flagged(self) -> None:
        result = self.measure(self.clip("thin.mkv", self.bars(14, 14)))
        summary = result["summary"]
        self.assertEqual(summary["top"]["thickness_px"]["median"], 14)
        self.assertTrue(summary["bars_detected"])
        self.assertIn("bars_thin", summary["flags"])

    def test_missing_bars_are_reported(self) -> None:
        result = self.measure(self.clip("plain.mkv", ["null"]))
        summary = result["summary"]
        self.assertFalse(summary["bars_detected"])
        self.assertFalse(self.gate(result)["passed"])
        self.assertEqual(summary["break_out_gate"]["status"], "not_applicable")
        self.assertIn("bars_not_detected", summary["flags"])

    def test_unequal_bars_are_flagged(self) -> None:
        video = self.clip("unequal.mkv", self.bars(43, 72))
        result = self.measure(video)
        summary = result["summary"]
        self.assertEqual(summary["top"]["thickness_px"]["median"], 43)
        self.assertEqual(summary["bottom"]["thickness_px"]["median"], 72)
        self.assertAlmostEqual(summary["top_bottom_difference_pct"], 8.056, places=2)
        self.assertTrue(summary["top_bottom_differ"])
        self.assertIn("top_bottom_unequal", summary["flags"])
        self.assertEqual(self.gate(result)["status"], "pass")
        relaxed = self.measure(video, top_bottom_tolerance_pct=10.0)
        self.assertFalse(relaxed["summary"]["top_bottom_differ"])

    def test_overlap_on_both_bars_gives_two_intervals(self) -> None:
        crossing = [
            box("200", "10", "200", "60", "red", "between(t,0.5,1)"),
            box("200", "ih-70", "200", "60", "yellow", "between(t,2,2.5)"),
        ]
        result = self.measure(self.clip("both.mkv", self.bars(43, 43, crossing)))
        bars = sorted(item["bar"] for item in result["overlap_intervals"])
        self.assertEqual(bars, ["bottom", "top"])
        self.assertEqual(result["summary"]["overlap_intervals"], 2)
        self.assertEqual(result["summary"]["break_out_gate"]["status"], "pass")

    def test_small_overlap_below_threshold_is_ignored(self) -> None:
        crossing = box("300", "10", "10", "10", "red")
        result = self.measure(self.clip("speck.mkv", self.bars(43, 43, [crossing])))
        self.assertEqual(result["overlap_intervals"], [])

    def test_subject_inside_at_start_and_intermittent_passes_break_out_gate(self) -> None:
        crossings = [
            box("200", "ih-60", "240", "50", "red", "between(t,0.8,1.2)"),
            box("200", "10", "240", "50", "yellow", "between(t,1.8,2.2)"),
        ]
        result = self.measure(self.clip("events.mkv", self.bars(43, 43, crossings)))
        gate = result["summary"]["break_out_gate"]
        self.assertEqual(gate["status"], "pass", gate)
        self.assertEqual(gate["start_overlap"]["bottom"], 0)
        self.assertEqual(gate["start_overlap"]["top"], 0)
        self.assertLess(gate["overlap_duty"]["overall"], 0.5)
        self.assertEqual(gate["violations"], [])

    def test_subject_over_a_bar_from_frame_zero_for_most_frames_fails(self) -> None:
        stay = box("200", "ih-60", "240", "50", "red", "between(t,0,2.5)")
        result = self.measure(self.clip("stays.mkv", self.bars(43, 43, [stay])))
        gate = result["summary"]["break_out_gate"]
        self.assertEqual(gate["status"], "fail")
        self.assertFalse(gate["passed"])
        kinds = {v["kind"] for v in gate["violations"]}
        self.assertEqual(kinds, {"starts_overlapping", "overlap_too_continuous"})
        start = next(v for v in gate["violations"] if v["kind"] == "starts_overlapping")
        self.assertEqual(start["bar"], "bottom")
        self.assertEqual(start["start_s"], 0.0)
        self.assertGreater(start["peak_fraction"], 0.1)
        duty = next(v for v in gate["violations"] if v["kind"] == "overlap_too_continuous")
        self.assertGreater(duty["duty"], 0.7)
        self.assertEqual(duty["intervals"][0]["bar"], "bottom")
        self.assertIn("starts_overlapping", result["summary"]["flags"])
        self.assertEqual(self.gate(result)["status"], "pass")
        relaxed = self.measure(
            self.root / "stays.mkv", start_overlap_tolerance=0.9, max_overlap_duty=1.0
        )
        self.assertEqual(relaxed["summary"]["break_out_gate"]["status"], "pass")

    def test_late_but_continuous_overlap_fails_only_the_duty_limit(self) -> None:
        stay = box("200", "ih-60", "240", "50", "red", "between(t,0.5,3)")
        result = self.measure(self.clip("late.mkv", self.bars(43, 43, [stay])))
        gate = result["summary"]["break_out_gate"]
        self.assertEqual({v["kind"] for v in gate["violations"]}, {"overlap_too_continuous"})
        self.assertEqual(gate["status"], "fail")

    def opening(self, side: str) -> list[str]:
        x, w = {"both": ("0", "iw"), "left": ("0", "iw/2")}[side]
        filters = []
        for k in range(1, 11):
            enable = f"between(t,{3 + 0.1 * (k - 1):.1f},4.01)"
            filters.append(box(x, "ih-43", w, str(2 * k), "0x3a7bd5", enable))
            filters.append(box(x, str(43 - 2 * k), w, str(2 * k), "0x3a7bd5", enable))
        return self.bars(43, 43, filters)

    def test_both_bars_opening_without_a_subject_is_not_a_pass_or_a_break_out(self) -> None:
        result = self.measure(self.clip("opening.mkv", self.opening("both"), duration=4))
        summary = result["summary"]
        gate = self.gate(result)
        self.assertEqual(gate["status"], "inspect", gate)
        self.assertFalse(gate["passed"])
        self.assertTrue(gate["needs_review"])
        self.assertIn("bar_opening", {v["kind"] for v in gate["inspect"]})
        record = next(v for v in gate["inspect"] if v["kind"] == "bar_opening")
        self.assertGreaterEqual(record["start_s"], 3.0)
        self.assertGreaterEqual(record["peak_px"], 18)
        self.assertEqual(result["overlap_intervals"], [])
        self.assertEqual(summary["break_out_gate"]["status"], "absent")
        self.assertFalse(summary["break_out_gate"]["passed"])
        self.assertEqual(summary["verdict"]["status"], "fail")
        self.assertFalse(summary["verdict"]["passed"])
        last = result["frames"][-1]["bottom"]
        self.assertTrue(last["bar_opening"])
        self.assertGreater(last["raw_overlap_fraction"], 0.05)
        self.assertEqual(last["overlap_fraction"], 0.0)

    def test_bar_opening_on_one_side_needs_review(self) -> None:
        result = self.measure(self.clip("opening_left.mkv", self.opening("left"), duration=4))
        gate = self.gate(result)
        self.assertEqual(gate["status"], "inspect", gate)
        self.assertFalse(gate["passed"])
        self.assertTrue(gate["needs_review"])
        self.assertIn("far_retreat", {v["kind"] for v in gate["inspect"]})
        self.assertNotIn("bar_opening", {v["kind"] for v in gate["inspect"]})
        verdict = result["summary"]["verdict"]
        self.assertFalse(verdict["passed"])
        self.assertNotEqual(verdict["status"], "pass")

    def test_opening_bar_does_not_hide_a_real_break_out(self) -> None:
        crossing = box("240", "20", "160", "100", "red", "between(t,1,1.95)")
        result = self.measure(
            self.clip("opening_and_subject.mkv", [*self.opening("both"), crossing], duration=4)
        )
        intervals = result["overlap_intervals"]
        self.assertEqual([item["bar"] for item in intervals], ["top"])
        self.assertAlmostEqual(intervals[0]["start_s"], 1.0, places=2)
        self.assertLess(intervals[0]["end_s"], 2.0)
        self.assertFalse(self.gate(result)["passed"])

    def test_output_paths_may_not_alias_the_input(self) -> None:
        video = self.clip("victim.mkv", self.bars(43, 43), duration=1)
        before = video.read_bytes()
        link = self.root / "alias.mkv"
        link.symlink_to(video)
        hard = self.root / "hard.mkv"
        hard.hardlink_to(video)
        for alias in (video, link, hard):
            for option in ("--output", "--contact-sheet"):
                code, document = self.run_cli(str(video), option, str(alias), "--overwrite")
                self.assertEqual(code, 1)
                self.assertIn("input video", document["error"])
        self.assertEqual(video.read_bytes(), before)
        relative = Path("victim.mkv")
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), str(relative), "--output", "./victim.mkv", "--overwrite"],
            capture_output=True, text=True, check=False, cwd=self.root,
        )
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(video.read_bytes(), before)

    def run_cli(self, *arguments: str) -> tuple[int, dict[str, Any]]:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            capture_output=True, text=True, check=False,
        )
        return completed.returncode, json.loads(completed.stdout)

    def test_cli_writes_json_and_contact_sheet(self) -> None:
        video = self.clip("cli.mkv", self.bars(43, 43))
        report = self.root / "report.json"
        sheet = self.root / "sheet.png"
        code, printed = self.run_cli(
            str(video), "--fps", "2", "--summary-only", "--output", str(report),
            "--contact-sheet", str(sheet), "--contact-columns", "3",
        )
        self.assertEqual(code, 0, printed)
        self.assertNotIn("frames", printed)
        saved = json.loads(report.read_text())
        self.assertEqual(len(saved["frames"]), 6)
        self.assertEqual(saved["contact_sheet"], str(sheet))
        self.assertGreater(sheet.stat().st_size, 1000)
        self.assertEqual(png_size(sheet)[0], 3 * 480 + 2 * 4)
        code, document = self.run_cli(str(video), "--output", str(report))
        self.assertEqual(code, 1)
        self.assertIn("--overwrite", document["error"])

    def test_window_contact_sheet_defaults_to_12_fps(self) -> None:
        video = self.clip("window.mkv", self.bars(43, 43), duration=3, rate=24)
        sheet = self.root / "window.png"
        code, printed = self.run_cli(
            str(video), "--summary-only", "--contact-sheet", str(sheet), "--window", "1", "2",
        )
        self.assertEqual(code, 0, printed)
        width, height = png_size(sheet)
        self.assertEqual(width, 6 * 320 + 5 * 4)
        self.assertEqual(height, 2 * 180 + 1 * 4)

    def test_window_errors_are_clear(self) -> None:
        video = self.clip("window_bad.mkv", self.bars(43, 43), duration=2)
        sheet = self.root / "bad.png"
        code, document = self.run_cli(str(video), "--window", "0", "1")
        self.assertEqual(code, 1)
        self.assertIn("--contact-sheet", document["error"])
        code, document = self.run_cli(str(video), "--contact-sheet", str(sheet), "--window", "1", "5")
        self.assertEqual(code, 1)
        self.assertIn("after the clip duration", document["error"])
        code, document = self.run_cli(str(video), "--contact-sheet", str(sheet), "--window", "1", "0.5")
        self.assertEqual(code, 1)
        self.assertIn("--window", document["error"])
        code, document = self.run_cli(
            str(video), "--contact-sheet", str(sheet), "--window", "0", "2", "--max-tiles", "10",
        )
        self.assertEqual(code, 1)
        self.assertIn("tiles", document["error"])
        self.assertFalse(sheet.exists())

    def test_missing_file_fails_clearly(self) -> None:
        code, document = self.run_cli(str(self.root / "absent.mp4"))
        self.assertEqual(code, 1)
        self.assertIn("not found", document["error"])

    def test_directory_fails_clearly(self) -> None:
        code, document = self.run_cli(str(self.root))
        self.assertEqual(code, 1)
        self.assertIn("not found", document["error"])

    def test_text_file_fails_clearly(self) -> None:
        path = self.root / "notes.mp4"
        path.write_text("not a video")
        code, document = self.run_cli(str(path))
        self.assertEqual(code, 1)
        self.assertIn("Not a readable media file", document["error"])

    def test_audio_only_file_fails_clearly(self) -> None:
        path = self.root / "tone.wav"
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "sine=d=1", str(path)],
            check=True,
        )
        code, document = self.run_cli(str(path))
        self.assertEqual(code, 1)
        self.assertIn("No video stream", document["error"])

    def test_out_of_range_options_fail_clearly(self) -> None:
        video = self.clip("range.mkv", self.bars(43, 43), duration=1)
        for option, value in (
            ("--fps", "0"), ("--centre-span", "1.5"), ("--contact-columns", "0"),
            ("--interior-columns", "0"), ("--jump-threshold-px", "-1"), ("--max-overlap-duty", "0"),
        ):
            code, document = self.run_cli(str(video), option, value)
            self.assertEqual(code, 1)
            self.assertIn(option, document["error"])


if __name__ == "__main__":
    unittest.main()
