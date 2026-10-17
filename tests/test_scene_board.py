from __future__ import annotations

import importlib.util
import json
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents/skills/scene-board-sheet/scripts/scene_board.py"
RENDERER = ROOT / ".agents/skills/html-graphic-render/scripts/render_html.py"
SPEC = importlib.util.spec_from_file_location("scene_board", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

SCENE_MD = """---
scene_id: scene-02
title: Test
---

# Scene 2

## Shot plan

```yaml
shot_plan:
  scene: scene-02
  status: draft
  energy: standard
  sources:
    - id: sun
      position: south-east
      switched_on_by: always on
      cues:
        - {at_s: 5.0, change: dim, trigger: a cloud, shot: s02_sh020_a}
  shots:
    - id: s02_sh010_a
      duration_s: 3.5
      job: establish
      size: wide
      angle: low
      framing: group
      featured: [mother, boy]
      move: slow push-in on the plaza
      lens_intent: deep focus
      light: {source: sun, key_side: camera-right, quality: hard}
    - id: s02_sh010_b
      duration_s: 2.0
      job: reveal
      size: medium
      angle: eye level
      move: static hold on the boy
      static_reason: contrast_hold
      light: {source: sun, key_side: camera-right}
    - id: s02_sh020_a
      duration_s: 4.0
      turn: true
      job: escalate
      size: close-up
      angle: low
      move: static hold
      static_reason: performance_hold
      dialogue: "Noon today, <b>Mang</b> Ador."
      light: {source: sun, key_side: behind}
    - id: s02_sh030_a
      duration_s: 3.0
      job: hold
      size: medium
      angle: eye level
      move: static hold
      static_reason: contrast_hold
      blocking_change: true
      light: {source: sun, key_side: camera-left}
```

## Notes

nothing
"""


def write_png(path: Path, shade: int, width: int = 320, height: int = 180) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = b"".join(
        b"\x00" + bytes((shade, shade, shade)) * width for _ in range(height)
    )

    def chunk(kind: bytes, data: bytes) -> bytes:
        body = kind + data
        return (
            struct.pack(">I", len(data))
            + body
            + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)
        )

    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(rows))
        + chunk(b"IEND", b"")
    )


class BoardTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory(prefix="scene-board-test-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name).resolve()
        scene = self.root / "scenes/scene-02"
        scene.mkdir(parents=True)
        (scene / "scene.md").write_text(SCENE_MD, encoding="utf-8")

    def init(self, level: str = "L2", overrides: list[str] | None = None) -> dict:
        return MODULE.init_board(
            self.root,
            "scene-02",
            level,
            "test scene",
            overrides or [],
            "pencil",
            "16:9",
            True,
        )

    def board(self) -> dict:
        return MODULE.read_board(self.root, "scene-02")[0]

    def rewrite(self, board: dict) -> None:
        _, body = MODULE.read_board(self.root, "scene-02")
        MODULE.write_board(self.root, "scene-02", board, body)

    def panel_path(self, panel_id: str, take: int = 1, version: int = 1) -> Path:
        clip = panel_id.rsplit("_p", 1)[0]
        return (
            self.root
            / f"scenes/scene-02/{clip}/{panel_id}_t{take:02d}_v{version:02d}.png"
        )

    def register_all(self) -> None:
        for number, panel in enumerate(self.board()["panels"]):
            path = self.panel_path(panel["id"])
            write_png(path, 40 + number * 10)
            MODULE.register_panel(
                self.root,
                "scene-02",
                panel["id"],
                path.relative_to(self.root).as_posix(),
                None,
                None,
                None,
                None,
                None,
            )

    def write_decision(
        self,
        panel_id: str | None = None,
        name: str = "decision.json",
        **changes: object,
    ) -> str:
        panel = next(
            p for p in self.board()["panels"] if panel_id is None or p["id"] == panel_id
        )
        record = {
            "schema_version": 1,
            "decision_id": "select_panel",
            "decision_type": "variant_selection",
            "asset_id": panel["id"],
            "subject_path": panel["file"],
            "selected_variant": Path(panel["file"]).name,
            "selected_sha256": panel["sha256"],
            "actor": "agent",
            "approval_mode": "approve_for_me",
            "project_sha256": "a" * 64,
            "result": "approved",
            "review_path": "review.json",
            "review_sha256": "b" * 64,
            "upstream_sha256": {},
            "reason": "selected after inspection",
            "decided_at": "2026-10-17T00:00:00+00:00",
        }
        record.update(changes)
        (self.root / name).write_text(json.dumps(record), encoding="utf-8")
        return name

    def finding_ids(self) -> list[str]:
        return [
            finding.rule_id for finding in MODULE.check_board(self.root, "scene-02")
        ]


class DerivationTests(BoardTestCase):
    def counts(self, level: str, overrides: list[str] | None = None) -> dict[str, int]:
        return self.init(level, overrides)["panels_per_shot"]

    def test_l1_gives_one_panel_per_shot(self) -> None:
        self.assertEqual(
            self.counts("L1"),
            {"s02_sh010_a": 1, "s02_sh010_b": 1, "s02_sh020_a": 1, "s02_sh030_a": 1},
        )

    def test_l2_gives_start_peak_end_on_key_shots_and_one_elsewhere(self) -> None:
        counts = self.counts("L2")
        self.assertEqual(counts["s02_sh010_a"], 3)
        self.assertEqual(counts["s02_sh010_b"], 1)
        self.assertEqual(counts["s02_sh020_a"], 3)
        states = [
            p["state"] for p in self.board()["panels"] if p["shot"] == "s02_sh010_a"
        ]
        self.assertEqual(states, ["start", "peak", "end"])

    def test_blocking_change_alone_gives_start_and_end(self) -> None:
        self.init("L2")
        states = [
            p["state"] for p in self.board()["panels"] if p["shot"] == "s02_sh030_a"
        ]
        self.assertEqual(states, ["start", "end"])

    def test_l3_gives_sub_beats_on_key_shots(self) -> None:
        self.init("L3")
        states = [
            p["state"] for p in self.board()["panels"] if p["shot"] == "s02_sh010_a"
        ]
        self.assertEqual(states, ["anticipation", "contact", "consequence", "reaction"])

    def test_turn_shot_is_key_even_when_held(self) -> None:
        self.init("L2")
        shots = {p["shot"] for p in self.board()["panels"] if p["state"] == "peak"}
        self.assertIn("s02_sh020_a", shots)

    def test_light_cue_makes_a_shot_key(self) -> None:
        source = MODULE.load_scene_source(self.root, "scene-02")
        shot = next(
            item for item in source.plan["shots"] if item["id"] == "s02_sh020_a"
        )
        shot_without_turn = {**shot, "turn": False}
        self.assertIn("light_cue", MODULE.key_reasons(shot_without_turn, source.plan))

    def test_default_level_is_l2(self) -> None:
        arguments = MODULE.build_parser().parse_args(["init", str(self.root), "02"])
        self.assertEqual(arguments.level, "L2")

    def test_override_upgrades_a_held_shot_and_records_its_reason(self) -> None:
        counts = self.counts("L2", ["s02_sh010_b=L3=insert needs beats"])
        self.assertEqual(counts["s02_sh010_b"], 4)
        board = self.board()
        self.assertEqual(board["overrides"][0]["reason"], "insert needs beats")
        panel = next(p for p in board["panels"] if p["shot"] == "s02_sh010_b")
        self.assertEqual(panel["shot_level"], "L3")

    def test_override_without_reason_is_rejected(self) -> None:
        with self.assertRaises(MODULE.BoardError):
            MODULE.parse_override("s02_sh010_b=L3=")

    def test_override_for_unknown_shot_is_rejected(self) -> None:
        with self.assertRaises(MODULE.BoardError):
            self.init("L2", ["s09_sh010_a=L3=nope"])

    def test_custom_sub_beats_are_used_at_l3(self) -> None:
        text = (self.root / "scenes/scene-02/scene.md").read_text(encoding="utf-8")
        text = text.replace(
            "      job: establish\n",
            "      job: establish\n      sub_beats: [draw, strike]\n",
        )
        (self.root / "scenes/scene-02/scene.md").write_text(text, encoding="utf-8")
        self.init("L3")
        states = [
            p["state"] for p in self.board()["panels"] if p["shot"] == "s02_sh010_a"
        ]
        self.assertEqual(states, ["draw", "strike"])

    def test_durations_sum_exactly_to_the_shot_duration(self) -> None:
        self.init("L2")
        total = sum(
            MODULE.milliseconds(p["duration_s"])
            for p in self.board()["panels"]
            if p["shot"] == "s02_sh010_a"
        )
        self.assertEqual(total, 3500)

    def test_panel_ids_count_in_tens_within_a_clip(self) -> None:
        self.init("L2")
        ids = [p["id"] for p in self.board()["panels"] if p["clip"] == "s02_sh010"]
        self.assertEqual(
            ids, [f"s02_sh010_p{n:03d}" for n in range(10, 10 * len(ids) + 1, 10)]
        )

    def test_refuses_to_replace_an_existing_board_without_overwrite(self) -> None:
        self.init("L2")
        with self.assertRaises(MODULE.BoardError):
            MODULE.init_board(
                self.root, "scene-02", "L2", "x", [], "pencil", "16:9", False
            )

    def test_invalid_level_or_missing_reason_is_rejected(self) -> None:
        with self.assertRaises(MODULE.BoardError):
            MODULE.init_board(
                self.root, "scene-02", "L4", "x", [], "pencil", "16:9", True
            )
        with self.assertRaises(MODULE.BoardError):
            MODULE.init_board(
                self.root, "scene-02", "L2", " ", [], "pencil", "16:9", True
            )

    def test_scene_without_shot_plan_is_rejected(self) -> None:
        (self.root / "scenes/scene-02/scene.md").write_text(
            "# nothing\n", encoding="utf-8"
        )
        with self.assertRaises(MODULE.BoardError):
            self.init()

    def test_scene_names_normalize(self) -> None:
        self.assertEqual(MODULE.normalize_scene("2"), "scene-02")
        with self.assertRaises(MODULE.BoardError):
            MODULE.normalize_scene("../x")


class CheckTests(BoardTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.init("L2")

    def test_fresh_board_passes(self) -> None:
        self.assertEqual(self.finding_ids(), [])

    def test_changed_shot_plan_marks_the_board_stale(self) -> None:
        scene = self.root / "scenes/scene-02/scene.md"
        scene.write_text(
            scene.read_text(encoding="utf-8").replace("hard", "soft"), encoding="utf-8"
        )
        self.assertIn("board.plan_stale", self.finding_ids())

    def test_panel_duration_that_disagrees_with_the_plan_is_reported(self) -> None:
        board = self.board()
        board["panels"][0]["duration_s"] = 0.5
        self.rewrite(board)
        self.assertIn("board.duration_sum", self.finding_ids())

    def test_field_that_contradicts_the_shot_plan_is_reported(self) -> None:
        board = self.board()
        board["panels"][0]["size"] = "close-up"
        self.rewrite(board)
        self.assertIn("board.field_mismatch", self.finding_ids())

    def test_unknown_shot_and_missing_shot_are_reported(self) -> None:
        board = self.board()
        board["panels"][0]["shot"] = "s02_sh099_a"
        self.rewrite(board)
        self.assertIn("board.shot_missing", self.finding_ids())

    def test_duplicate_panel_id_is_reported(self) -> None:
        board = self.board()
        board["panels"][1]["id"] = board["panels"][0]["id"]
        self.rewrite(board)
        self.assertIn("board.panel_id", self.finding_ids())

    def test_schema_violation_is_reported(self) -> None:
        board = self.board()
        board["level"] = "L9"
        self.rewrite(board)
        self.assertEqual(self.finding_ids(), ["board.schema"])

    def test_extra_panels_differ_from_level_as_a_warning(self) -> None:
        board = self.board()
        board["level"] = "L1"
        self.rewrite(board)
        findings = MODULE.check_board(self.root, "scene-02")
        self.assertTrue(findings)
        self.assertTrue(all(item.severity == "warning" for item in findings))

    def test_registered_file_changed_on_disk_is_reported(self) -> None:
        self.register_all()
        self.assertEqual(self.finding_ids(), [])
        write_png(self.panel_path(self.board()["panels"][0]["id"]), 250)
        self.assertIn("board.hash_mismatch", self.finding_ids())

    def test_registered_file_removed_is_reported(self) -> None:
        self.register_all()
        self.panel_path(self.board()["panels"][0]["id"]).unlink()
        self.assertIn("board.file_missing", self.finding_ids())

    def test_approval_needs_a_decision_record(self) -> None:
        self.register_all()
        board = self.board()
        board["panels"][0]["status"] = "approved"
        self.rewrite(board)
        self.assertIn("board.approved_without_decision", self.finding_ids())

    def test_changed_decision_file_is_reported(self) -> None:
        self.register_all()
        panel_id = self.board()["panels"][0]["id"]
        decision = self.root / self.write_decision(panel_id)
        MODULE.mark_panel(self.root, "scene-02", panel_id, "approved", "decision.json")
        self.assertEqual(self.finding_ids(), [])
        decision.write_text('{"changed": true}', encoding="utf-8")
        self.assertIn("board.decision_stale", self.finding_ids())

    def test_board_file_bound_as_a_request_reference_is_reported(self) -> None:
        self.register_all()
        panel = self.board()["panels"][0]
        (self.root / "task_ids.json").write_text(
            json.dumps(
                {
                    "tasks": [
                        {
                            "references": [
                                {"path": panel["file"], "sha256": panel["sha256"]}
                            ]
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        self.assertIn("board.animatic_review_only", self.finding_ids())

    def test_unrelated_request_reference_is_not_reported(self) -> None:
        self.register_all()
        (self.root / "task_ids.json").write_text(
            json.dumps(
                {
                    "tasks": [
                        {"references": [{"path": "elements/x.png", "sha256": "a" * 64}]}
                    ]
                }
            ),
            encoding="utf-8",
        )
        self.assertEqual(self.finding_ids(), [])


class RegisterTests(BoardTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.init("L2")
        self.panel_id = self.board()["panels"][0]["id"]

    def register(self, path: Path, **values: object) -> dict:
        defaults: dict = {
            "edit_of": None,
            "dimension": None,
            "bbox": None,
            "prompt_file": None,
            "task_id": None,
        }
        defaults.update(values)
        return MODULE.register_panel(
            self.root,
            "scene-02",
            self.panel_id,
            path.relative_to(self.root).as_posix(),
            **defaults,
        )

    def test_first_registration_sets_review_and_records_the_hash(self) -> None:
        path = self.panel_path(self.panel_id)
        write_png(path, 90)
        result = self.register(path)
        self.assertEqual(result["operation"], "generate")
        panel = self.board()["panels"][0]
        self.assertEqual(panel["status"], "review")
        self.assertEqual(panel["sha256"], MODULE.sha256_file(path))

    def test_edit_saves_a_new_version_and_keeps_the_parent_hash(self) -> None:
        first = self.panel_path(self.panel_id)
        write_png(first, 90)
        self.register(first)
        edited = self.panel_path(self.panel_id, version=2)
        write_png(edited, 120)
        self.register(
            edited,
            edit_of=first.relative_to(self.root).as_posix(),
            dimension="prop count",
            bbox="10,20,300,400",
        )
        panel = self.board()["panels"][0]
        self.assertEqual(len(panel["versions"]), 2)
        self.assertTrue(panel["versions"][0]["rejected"])
        self.assertEqual(
            panel["versions"][1]["parent_sha256"], MODULE.sha256_file(first)
        )
        self.assertEqual(panel["versions"][1]["bbox"], [10, 20, 300, 400])
        self.assertTrue(first.is_file())

    def test_editing_resets_an_approval(self) -> None:
        first = self.panel_path(self.panel_id)
        write_png(first, 90)
        self.register(first)
        self.write_decision(self.panel_id)
        MODULE.mark_panel(
            self.root, "scene-02", self.panel_id, "approved", "decision.json"
        )
        edited = self.panel_path(self.panel_id, version=2)
        write_png(edited, 120)
        self.register(edited, edit_of=first.relative_to(self.root).as_posix())
        panel = self.board()["panels"][0]
        self.assertEqual(panel["status"], "review")
        self.assertNotIn("decision", panel)

    def test_identical_edit_is_rejected(self) -> None:
        first = self.panel_path(self.panel_id)
        write_png(first, 90)
        self.register(first)
        copy = self.panel_path(self.panel_id, version=2)
        shutil.copyfile(first, copy)
        with self.assertRaises(MODULE.BoardError):
            self.register(copy, edit_of=first.relative_to(self.root).as_posix())

    def test_registering_the_same_file_twice_is_rejected(self) -> None:
        path = self.panel_path(self.panel_id)
        write_png(path, 90)
        self.register(path)
        with self.assertRaises(MODULE.BoardError):
            self.register(path)

    def test_file_name_must_follow_the_naming_contract(self) -> None:
        wrong = self.root / f"scenes/scene-02/s02_sh010/{self.panel_id}.png"
        write_png(wrong, 90)
        with self.assertRaises(MODULE.BoardError):
            self.register(wrong)

    def test_file_for_another_panel_is_rejected(self) -> None:
        other = self.board()["panels"][1]["id"]
        path = self.panel_path(other)
        write_png(path, 90)
        with self.assertRaises(MODULE.BoardError):
            self.register(path)

    def test_file_outside_the_clip_directory_is_rejected(self) -> None:
        stray = self.root / f"scenes/scene-02/{self.panel_id}_t01_v01.png"
        write_png(stray, 90)
        with self.assertRaises(MODULE.BoardError):
            self.register(stray)

    def test_bad_bbox_and_missing_prompt_snapshot_are_rejected(self) -> None:
        first = self.panel_path(self.panel_id)
        write_png(first, 90)
        self.register(first)
        edited = self.panel_path(self.panel_id, version=2)
        write_png(edited, 120)
        with self.assertRaises(MODULE.BoardError):
            self.register(
                edited, edit_of=first.relative_to(self.root).as_posix(), bbox="1,2,3"
            )
        with self.assertRaises(MODULE.BoardError):
            self.register(
                edited,
                edit_of=first.relative_to(self.root).as_posix(),
                prompt_file="nope.md",
            )

    def test_paths_cannot_escape_the_project(self) -> None:
        with self.assertRaises(MODULE.BoardError):
            MODULE.contained(self.root, "../outside.png")
        with self.assertRaises(MODULE.BoardError):
            MODULE.contained(self.root, "/etc/passwd")
        outside = Path(tempfile.mkdtemp(prefix="scene-board-outside-"))
        self.addCleanup(shutil.rmtree, outside)
        (self.root / "link").symlink_to(outside)
        with self.assertRaises(MODULE.BoardError):
            MODULE.contained(self.root, "link/file.png")

    def test_mark_requires_a_file_and_a_decision_for_approval(self) -> None:
        with self.assertRaises(MODULE.BoardError):
            MODULE.mark_panel(self.root, "scene-02", self.panel_id, "needs_edit", None)
        path = self.panel_path(self.panel_id)
        write_png(path, 90)
        self.register(path)
        with self.assertRaises(MODULE.BoardError):
            MODULE.mark_panel(self.root, "scene-02", self.panel_id, "approved", None)
        MODULE.mark_panel(self.root, "scene-02", self.panel_id, "needs_edit", None)
        self.assertEqual(self.board()["panels"][0]["status"], "needs_edit")


class RepairTests(BoardTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.init("L2")
        self.register_all()

    def plan(self, panels: list[str], **values: object) -> dict:
        defaults: dict = {
            "cause": "local",
            "dimension": "prop count",
            "delta": "remove the duplicated jar on the bench",
            "accept": ["exactly one jar on the bench"],
            "bbox": None,
        }
        defaults.update(values)
        return MODULE.plan_repair(self.root, "scene-02", panels, **defaults)

    def test_local_defect_is_repaired_by_editing_only_that_panel(self) -> None:
        result = self.plan(["s02_sh010_p020"])
        action = result["actions"][0]
        self.assertEqual(action["action"], "edit")
        self.assertEqual(action["tool"], "seedream_edit_image")
        self.assertEqual(action["next_version"], "s02_sh010_p020_t01_v02.png")
        self.assertNotIn("s02_sh010_p020", result["untouched_panels"])
        self.assertIn("s02_sh010_p010", result["untouched_panels"])
        contract = (self.root / action["contract"]).read_text(encoding="utf-8")
        self.assertIn("remove the duplicated jar", contract)
        self.assertIn("Locked decisions", contract)

    def test_only_the_affected_sheet_page_and_segment_go_stale(self) -> None:
        result = self.plan(["s02_sh010_p020"])
        self.assertEqual(result["stale"]["sheet_pages"], [1])
        self.assertEqual(result["stale"]["animatic_segments"], ["s02_sh010_p020"])

    def fail_edit(self, panel_id: str, dimension: str, version: int) -> None:
        previous = self.panel_path(panel_id, version=version - 1)
        edited = self.panel_path(panel_id, version=version)
        write_png(edited, 100 + version)
        MODULE.register_panel(
            self.root,
            "scene-02",
            panel_id,
            edited.relative_to(self.root).as_posix(),
            previous.relative_to(self.root).as_posix(),
            dimension,
            None,
            None,
            None,
        )
        MODULE.mark_panel(self.root, "scene-02", panel_id, "needs_edit", None)

    def test_two_failed_edits_on_one_dimension_escalate_to_regeneration(self) -> None:
        panel_id = "s02_sh010_p020"
        MODULE.mark_panel(self.root, "scene-02", panel_id, "needs_edit", None)
        self.assertEqual(self.plan([panel_id])["actions"][0]["action"], "edit")
        self.fail_edit(panel_id, "prop count", 2)
        self.assertEqual(self.plan([panel_id])["actions"][0]["action"], "edit")
        self.fail_edit(panel_id, "prop count", 3)
        self.assertEqual(
            self.plan([panel_id])["actions"][0]["action"], "regenerate_panel"
        )

    def test_a_regenerated_panel_starts_its_edit_count_again(self) -> None:
        panel_id = "s02_sh010_p020"
        self.fail_edit(panel_id, "prop count", 2)
        self.fail_edit(panel_id, "prop count", 3)
        regenerated = self.root / f"scenes/scene-02/s02_sh010/{panel_id}_t02_v01.png"
        write_png(regenerated, 33)
        MODULE.register_panel(
            self.root,
            "scene-02",
            panel_id,
            regenerated.relative_to(self.root).as_posix(),
            None,
            None,
            None,
            None,
            None,
        )
        MODULE.mark_panel(self.root, "scene-02", panel_id, "needs_edit", None)
        self.assertEqual(self.plan([panel_id])["actions"][0]["action"], "edit")

    def test_a_different_dimension_still_edits(self) -> None:
        panel_id = "s02_sh010_p020"
        previous = self.panel_path(panel_id)
        edited = self.panel_path(panel_id, version=2)
        write_png(edited, 130)
        MODULE.register_panel(
            self.root,
            "scene-02",
            panel_id,
            edited.relative_to(self.root).as_posix(),
            previous.relative_to(self.root).as_posix(),
            "prop count",
            None,
            None,
            None,
        )
        result = self.plan([panel_id], dimension="hand position")
        self.assertEqual(result["actions"][0]["action"], "edit")

    def test_wrong_beat_regenerates_the_panel_not_the_scene(self) -> None:
        result = self.plan(["s02_sh020_p020"], cause="beat")
        self.assertEqual([a["action"] for a in result["actions"]], ["regenerate_panel"])
        self.assertIn("s02_sh010_p010", result["untouched_panels"])

    def test_shared_cause_regenerates_that_shots_panels_only(self) -> None:
        result = self.plan(["s02_sh010_p010"], cause="shared")
        action = result["actions"][0]
        self.assertEqual(action["action"], "regenerate_shot")
        self.assertEqual(
            action["panels"], ["s02_sh010_p010", "s02_sh010_p020", "s02_sh010_p030"]
        )
        self.assertIn("s02_sh020_p010", result["untouched_panels"])

    def test_majority_failure_in_a_shot_regenerates_the_shot(self) -> None:
        result = self.plan(["s02_sh010_p010", "s02_sh010_p020"])
        self.assertEqual(result["actions"][0]["action"], "regenerate_shot")

    def test_minority_failure_in_a_shot_keeps_the_edit_path(self) -> None:
        result = self.plan(["s02_sh010_p010"])
        self.assertEqual(result["actions"][0]["action"], "edit")

    def test_edit_needs_a_delta_and_acceptance_criteria(self) -> None:
        with self.assertRaises(MODULE.BoardError):
            self.plan(["s02_sh010_p010"], delta="")
        with self.assertRaises(MODULE.BoardError):
            self.plan(["s02_sh010_p010"], accept=[])

    def test_unknown_panel_cause_and_bbox_are_rejected(self) -> None:
        with self.assertRaises(MODULE.BoardError):
            self.plan(["s02_sh010_p999"])
        with self.assertRaises(MODULE.BoardError):
            self.plan(["s02_sh010_p010"], cause="whim")
        with self.assertRaises(MODULE.BoardError):
            self.plan(["s02_sh010_p010"], bbox="1,2")
        with self.assertRaises(MODULE.BoardError):
            self.plan([])

    def test_panel_without_a_file_cannot_be_edited(self) -> None:
        board = self.board()
        board["panels"][0].update({"file": None, "sha256": None, "status": "planned"})
        self.rewrite(board)
        with self.assertRaises(MODULE.BoardError):
            self.plan([board["panels"][0]["id"]])

    def test_sibling_panels_keep_their_files_and_hashes_through_an_edit(self) -> None:
        before = {p["id"]: p["sha256"] for p in self.board()["panels"]}
        panel_id = "s02_sh010_p020"
        previous = self.panel_path(panel_id)
        edited = self.panel_path(panel_id, version=2)
        write_png(edited, 77)
        MODULE.register_panel(
            self.root,
            "scene-02",
            panel_id,
            edited.relative_to(self.root).as_posix(),
            previous.relative_to(self.root).as_posix(),
            "prop count",
            None,
            None,
            None,
        )
        after = {p["id"]: p["sha256"] for p in self.board()["panels"]}
        changed = [key for key in before if before[key] != after[key]]
        self.assertEqual(changed, [panel_id])


class SheetTests(BoardTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.init("L2")
        self.register_all()

    def pretend_rendered(self) -> None:
        directory = self.root / "scenes/scene-02/board/sheet"
        for sidecar in MODULE.latest_sidecars(directory, "sheet"):
            data = json.loads(sidecar.read_text(encoding="utf-8"))
            write_png(self.root / data["png"], 99)

    def test_sheet_paginates_and_writes_exact_copy_keys(self) -> None:
        result = MODULE.build_sheet(self.root, "scene-02", None)
        self.assertEqual(len(result["pages"]), 2)
        first = (self.root / result["pages"][0]["html"]).read_text(encoding="utf-8")
        self.assertIn('data-copy-key="panel-s02_sh010_p010-framing"', first)
        self.assertIn("sheet.css", first)
        sidecar = json.loads(
            (self.root / result["pages"][0]["sidecar"]).read_text(encoding="utf-8")
        )
        self.assertFalse(sidecar["bind_to_seedance"])
        self.assertIn("--copy", sidecar["render_arguments"])
        self.assertEqual(len(sidecar["panels"]), 6)

    def test_text_is_escaped_and_long_text_is_shortened(self) -> None:
        result = MODULE.build_sheet(self.root, "scene-02", None)
        pages = "".join(
            (self.root / page["html"]).read_text(encoding="utf-8")
            for page in result["pages"]
        )
        self.assertIn("&lt;b&gt;Mang&lt;/b&gt;", pages)
        self.assertNotIn("<b>Mang</b>", pages)
        self.assertEqual(len(MODULE.short("x" * 300, 120)), 120)
        self.assertEqual(MODULE.short("a  b\n c", 50), "a b c")

    def test_panel_without_a_file_shows_a_placeholder(self) -> None:
        board = self.board()
        board["panels"][0].update(
            {"file": None, "sha256": None, "status": "planned", "versions": []}
        )
        self.rewrite(board)
        result = MODULE.build_sheet(self.root, "scene-02", None)
        page = (self.root / result["pages"][0]["html"]).read_text(encoding="utf-8")
        self.assertIn("No panel yet", page)

    def test_rebuilding_writes_a_new_version_and_keeps_the_old_one(self) -> None:
        first = MODULE.build_sheet(self.root, "scene-02", None)
        second = MODULE.build_sheet(self.root, "scene-02", None)
        self.assertIn("_v01.", first["pages"][0]["html"])
        self.assertIn("_v02.", second["pages"][0]["html"])
        self.assertTrue((self.root / first["pages"][0]["html"]).is_file())

    def test_rejected_panels_stay_on_the_sheet_with_their_status(self) -> None:
        panel_id = self.board()["panels"][0]["id"]
        MODULE.mark_panel(self.root, "scene-02", panel_id, "rejected", None)
        result = MODULE.build_sheet(self.root, "scene-02", None)
        self.assertEqual(result["panels"], len(self.board()["panels"]))
        page = (self.root / result["pages"][0]["html"]).read_text(encoding="utf-8")
        self.assertIn(">rejected<", page)

    def test_status_reports_only_the_changed_panels_page_stale(self) -> None:
        MODULE.build_sheet(self.root, "scene-02", None)
        self.pretend_rendered()
        self.assertEqual(
            MODULE.status_report(self.root, "scene-02")["stale_sheet_pages"], []
        )
        panel_id = "s02_sh010_p020"
        previous = self.panel_path(panel_id)
        edited = self.panel_path(panel_id, version=2)
        write_png(edited, 210)
        MODULE.register_panel(
            self.root,
            "scene-02",
            panel_id,
            edited.relative_to(self.root).as_posix(),
            previous.relative_to(self.root).as_posix(),
            None,
            None,
            None,
            None,
        )
        stale = MODULE.status_report(self.root, "scene-02")["stale_sheet_pages"]
        self.assertEqual([item["page"] for item in stale], [1])
        self.assertEqual(stale[0]["panels"], [panel_id])

    def test_review_page_is_static_and_decides_nothing(self) -> None:
        MODULE.build_sheet(self.root, "scene-02", None)
        result = MODULE.build_review_page(self.root, "scene-02")
        page = (self.root / result["page"]).read_text(encoding="utf-8")
        self.assertNotIn("<script", page)
        self.assertIn("decides nothing", page)
        self.assertTrue((self.root / "review/scene-board.css").is_file())

    def test_render_needs_an_existing_renderer(self) -> None:
        MODULE.build_sheet(self.root, "scene-02", None)
        with self.assertRaises(MODULE.BoardError):
            MODULE.render_sheet(
                self.root, "scene-02", str(self.root / "missing.py"), None
            )

    def test_render_without_built_pages_is_rejected(self) -> None:
        with self.assertRaises(MODULE.BoardError):
            MODULE.render_sheet(self.root, "scene-02", str(RENDERER), None)

    @unittest.skipUnless(
        shutil.which("google-chrome")
        or Path("/Applications/Google Chrome.app").exists(),
        "Chrome is required",
    )
    def test_sheet_page_renders_to_an_exact_size_png(self) -> None:
        MODULE.build_sheet(self.root, "scene-02", None)
        result = MODULE.render_sheet(self.root, "scene-02", str(RENDERER), [1])
        png = self.root / result["rendered"][0]["png"]
        self.assertTrue(png.is_file())
        width, height = struct.unpack(">II", png.read_bytes()[16:24])
        self.assertEqual((width, height), (3840, 2160))


class OverviewTests(BoardTestCase):
    def test_overview_is_skipped_without_a_layout_block(self) -> None:
        self.init("L2")
        self.assertIn("skipped", MODULE.build_overview(self.root, "scene-02"))

    def test_overview_writes_floor_plan_sources(self) -> None:
        self.init("L2")
        board = self.board()
        board["layout"] = {
            "room": {"width": 8, "depth": 6, "unit": "m"},
            "axis": {"from": [0, 3], "to": [8, 3], "note": "mother and aunt stay left"},
            "lights": [{"id": "window", "at": [0, 1], "direction": "east"}],
            "figures": [{"id": "A", "label": "mother", "at": [3, 3]}],
        }
        self.rewrite(board)
        result = MODULE.build_overview(self.root, "scene-02")
        page = (self.root / result["html"]).read_text(encoding="utf-8")
        self.assertIn("<svg", page)
        self.assertIn("A: mother", page)
        self.assertEqual(
            MODULE.status_report(self.root, "scene-02")["overview"]["state"], "current"
        )
        board["layout"]["room"]["width"] = 9
        self.rewrite(board)
        self.assertEqual(
            MODULE.status_report(self.root, "scene-02")["overview"]["state"], "stale"
        )

    def test_invalid_layout_is_a_schema_finding(self) -> None:
        self.init("L2")
        board = self.board()
        board["layout"] = {"room": {"width": -1, "depth": 6}}
        self.rewrite(board)
        self.assertEqual(self.finding_ids(), ["board.schema"])


@unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg is required")
class AnimaticTests(BoardTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.init("L1")
        self.register_all()

    def duration(self, path: Path) -> float:
        completed = subprocess.run(
            ["ffmpeg", "-hide_banner", "-i", str(path), "-f", "null", "-"],
            capture_output=True,
            text=True,
            check=False,
        )
        stamp = [line for line in completed.stderr.splitlines() if "time=" in line][-1]
        clock = stamp.split("time=")[1].split()[0]
        hours, minutes, secs = clock.split(":")
        return int(hours) * 3600 + int(minutes) * 60 + float(secs)

    def test_animatic_duration_equals_the_sum_of_panel_durations(self) -> None:
        result = MODULE.build_animatic(self.root, "scene-02", "640x360", None)
        self.assertAlmostEqual(result["duration_s"], 12.5)
        self.assertAlmostEqual(
            self.duration(self.root / result["file"]), 12.5, delta=0.2
        )
        record = json.loads((self.root / result["record"]).read_text(encoding="utf-8"))
        self.assertFalse(record["bind_to_seedance"])
        self.assertEqual(len(record["segments"]), 4)

    def test_animatic_goes_stale_only_for_the_changed_segment(self) -> None:
        MODULE.build_animatic(self.root, "scene-02", "640x360", None)
        self.assertEqual(
            MODULE.status_report(self.root, "scene-02")["animatic"]["state"], "current"
        )
        panel_id = "s02_sh020_p010"
        previous = self.panel_path(panel_id)
        edited = self.panel_path(panel_id, version=2)
        write_png(edited, 220)
        MODULE.register_panel(
            self.root,
            "scene-02",
            panel_id,
            edited.relative_to(self.root).as_posix(),
            previous.relative_to(self.root).as_posix(),
            None,
            None,
            None,
            None,
        )
        report = MODULE.status_report(self.root, "scene-02")["animatic"]
        self.assertEqual(report, {"state": "stale", "panels": [panel_id]})

    def test_animatic_needs_a_file_for_every_panel(self) -> None:
        board = self.board()
        board["panels"][0].update(
            {"file": None, "sha256": None, "status": "planned", "versions": []}
        )
        self.rewrite(board)
        with self.assertRaises(MODULE.BoardError):
            MODULE.build_animatic(self.root, "scene-02", "640x360", None)

    def test_animatic_rejects_a_bad_size_and_missing_audio(self) -> None:
        with self.assertRaises(MODULE.BoardError):
            MODULE.build_animatic(self.root, "scene-02", "big", None)
        with self.assertRaises(MODULE.BoardError):
            MODULE.build_animatic(self.root, "scene-02", "640x360", "missing.wav")


class CommandLineTests(BoardTestCase):
    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_init_then_check_succeeds_and_reports_json(self) -> None:
        init = self.run_cli("init", str(self.root), "scene-02", "--overwrite")
        self.assertEqual(init.returncode, 0, init.stderr)
        self.assertEqual(json.loads(init.stdout)["level"], "L2")
        check = self.run_cli("check", str(self.root), "02")
        self.assertEqual(check.returncode, 0, check.stderr)
        self.assertTrue(json.loads(check.stdout)["ok"])

    def test_check_exits_non_zero_when_the_plan_changed(self) -> None:
        self.run_cli("init", str(self.root), "02", "--overwrite")
        scene = self.root / "scenes/scene-02/scene.md"
        scene.write_text(
            scene.read_text(encoding="utf-8").replace("hard", "soft"), encoding="utf-8"
        )
        check = self.run_cli("check", str(self.root), "02")
        self.assertEqual(check.returncode, 1)
        self.assertFalse(json.loads(check.stdout)["ok"])

    def test_errors_exit_two_with_a_message(self) -> None:
        missing = self.run_cli("check", str(self.root), "07")
        self.assertEqual(missing.returncode, 2)
        self.assertTrue(missing.stderr.strip())
        absent = self.run_cli("status", str(self.root / "nope"), "02")
        self.assertEqual(absent.returncode, 2)


class ReviewFixTests(BoardTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.init("L2")
        self.register_all()

    def change_plan(self, old: str, new: str) -> None:
        scene = self.root / "scenes/scene-02/scene.md"
        scene.write_text(
            scene.read_text(encoding="utf-8").replace(old, new), encoding="utf-8"
        )

    def test_status_reports_a_changed_shot_plan_and_marks_derived_files_stale(
        self,
    ) -> None:
        MODULE.build_sheet(self.root, "scene-02", None)
        sheet_dir = self.root / "scenes/scene-02/board/sheet"
        for sidecar in MODULE.latest_sidecars(sheet_dir, "sheet"):
            write_png(self.root / json.loads(sidecar.read_text())["png"], 90)
        self.change_plan("hard", "soft")
        report = MODULE.status_report(self.root, "scene-02")
        self.assertTrue(report["plan_stale"])
        self.assertEqual(
            {item["reason"] for item in report["stale_sheet_pages"]},
            {"shot plan changed"},
        )

    def test_plan_hash_ignores_comments_and_whitespace_outside_the_yaml(self) -> None:
        self.change_plan("## Shot plan\n", "## Shot plan\n\nA note for people.\n\n")
        self.assertEqual(self.finding_ids(), [])

    def test_overwrite_is_refused_when_panels_are_registered(self) -> None:
        with self.assertRaises(MODULE.BoardError) as raised:
            MODULE.init_board(
                self.root, "scene-02", "L2", "x", [], "pencil", "16:9", True
            )
        self.assertIn("rebase-plan", str(raised.exception))

    def test_rebase_keeps_registered_panels_and_flags_changed_ones(self) -> None:
        before = {p["id"]: p["sha256"] for p in self.board()["panels"]}
        self.change_plan("size: wide", "size: close-up")
        result = MODULE.rebase_plan(self.root, "scene-02")
        board = self.board()
        self.assertEqual({p["id"]: p["sha256"] for p in board["panels"]}, before)
        self.assertIn("s02_sh010_p010", result["needs_edit"])
        panel = next(p for p in board["panels"] if p["id"] == "s02_sh010_p010")
        self.assertEqual(panel["status"], "needs_edit")
        self.assertEqual(panel["size"], "close-up")
        self.assertNotIn("board.plan_stale", self.finding_ids())

    def test_rebase_reports_orphaned_files_when_panels_disappear(self) -> None:
        self.change_plan(
            "      move: slow push-in on the plaza\n",
            "      move: static hold on the plaza\n      static_reason: contrast_hold\n",
        )
        result = MODULE.rebase_plan(self.root, "scene-02")
        self.assertTrue(result["orphaned_files"])
        self.assertEqual(len(self.board()["panels"]), 7)

    def test_sheet_can_write_only_chosen_pages(self) -> None:
        result = MODULE.build_sheet(self.root, "scene-02", None, [2])
        self.assertEqual([page["page"] for page in result["pages"]], [2])
        with self.assertRaises(MODULE.BoardError):
            MODULE.build_sheet(self.root, "scene-02", None, [9])

    def test_unrendered_page_is_stale_and_the_review_page_says_so(self) -> None:
        MODULE.build_sheet(self.root, "scene-02", None)
        stale = MODULE.status_report(self.root, "scene-02")["stale_sheet_pages"]
        self.assertEqual(
            {item["reason"] for item in stale}, {"page is built but not rendered"}
        )
        page = (
            self.root / MODULE.build_review_page(self.root, "scene-02")["page"]
        ).read_text(encoding="utf-8")
        self.assertIn("Not rendered yet", page)

    def test_render_rejects_pages_outside_the_board(self) -> None:
        MODULE.build_sheet(self.root, "scene-02", None)
        with self.assertRaises(MODULE.BoardError):
            MODULE.render_sheet(self.root, "scene-02", str(RENDERER), [9])

    def test_derived_directory_symlink_is_refused(self) -> None:
        outside = Path(tempfile.mkdtemp(prefix="scene-board-outside-"))
        self.addCleanup(shutil.rmtree, outside)
        (self.root / "scenes/scene-02/board").symlink_to(outside)
        with self.assertRaises(MODULE.BoardError):
            MODULE.build_sheet(self.root, "scene-02", None)
        self.assertEqual(list(outside.iterdir()), [])

    def test_symlinked_board_file_is_not_rewritten(self) -> None:
        outside = Path(tempfile.mkdtemp(prefix="scene-board-outside-"))
        self.addCleanup(shutil.rmtree, outside)
        target = outside / "board.md"
        board_file = self.root / "scenes/scene-02/board.md"
        shutil.move(str(board_file), target)
        board_file.symlink_to(target)
        before = target.read_text(encoding="utf-8")
        with self.assertRaises(MODULE.BoardError):
            MODULE.mark_panel(
                self.root, "scene-02", "s02_sh010_p010", "needs_edit", None
            )
        self.assertEqual(target.read_text(encoding="utf-8"), before)

    def test_light_ids_with_markup_are_rejected_by_the_schema(self) -> None:
        board = self.board()
        board["layout"] = {
            "room": {"width": 4, "depth": 4},
            "lights": [{"id": 'x" onmouseover="alert(1)', "at": [1, 1]}],
        }
        self.rewrite(board)
        self.assertEqual(self.finding_ids(), ["board.schema"])

    def test_overview_labels_every_marker(self) -> None:
        board = self.board()
        board["layout"] = {
            "room": {"width": 8, "depth": 6},
            "lights": [{"id": "window", "at": [0, 1]}],
            "figures": [{"id": "A", "label": "mother <b>", "at": [3, 3]}],
        }
        self.rewrite(board)
        page = (
            self.root / MODULE.build_overview(self.root, "scene-02")["html"]
        ).read_text(encoding="utf-8")
        self.assertIn(">window</text>", page)
        self.assertIn(">A</text>", page)
        self.assertIn("mother &lt;b&gt;", page)

    def test_repair_plan_ignores_duplicate_panel_ids(self) -> None:
        result = MODULE.plan_repair(
            self.root,
            "scene-02",
            ["s02_sh010_p010"] * 3,
            "local",
            "prop count",
            "remove the jar",
            ["one jar"],
            None,
        )
        self.assertEqual(result["actions"][0]["action"], "edit")

    def test_repair_plan_needs_a_dimension_and_leaves_no_files_on_error(self) -> None:
        with self.assertRaises(MODULE.BoardError):
            MODULE.plan_repair(
                self.root,
                "scene-02",
                ["s02_sh010_p010"],
                "local",
                "",
                "remove the jar",
                ["one jar"],
                None,
            )
        board = self.board()
        board["panels"][3].update(
            {"file": None, "sha256": None, "status": "planned", "versions": []}
        )
        self.rewrite(board)
        with self.assertRaises(MODULE.BoardError):
            MODULE.plan_repair(
                self.root,
                "scene-02",
                ["s02_sh010_p010", board["panels"][3]["id"]],
                "local",
                "prop count",
                "remove the jar",
                ["one jar"],
                None,
            )
        self.assertFalse((self.root / "scenes/scene-02/board/repair").exists())

    def test_edit_of_must_be_a_registered_version_of_the_same_panel(self) -> None:
        panels = self.board()["panels"]
        other = self.root / panels[1]["file"]
        edited = self.panel_path(panels[0]["id"], version=2)
        write_png(edited, 15)
        with self.assertRaises(MODULE.BoardError):
            MODULE.register_panel(
                self.root,
                "scene-02",
                panels[0]["id"],
                edited.relative_to(self.root).as_posix(),
                other.relative_to(self.root).as_posix(),
                None,
                None,
                None,
                None,
            )

    def test_edit_records_the_parent_file_and_a_bbox_must_be_ordered(self) -> None:
        panel = self.board()["panels"][0]
        edited = self.panel_path(panel["id"], version=2)
        write_png(edited, 15)
        for bbox in ("300,0,10,50", "0,0,1000,50"):
            with self.assertRaises(MODULE.BoardError):
                MODULE.register_panel(
                    self.root,
                    "scene-02",
                    panel["id"],
                    edited.relative_to(self.root).as_posix(),
                    panel["file"],
                    None,
                    bbox,
                    None,
                    None,
                )
        MODULE.register_panel(
            self.root,
            "scene-02",
            panel["id"],
            edited.relative_to(self.root).as_posix(),
            panel["file"],
            "prop count",
            "0,0,10,50",
            None,
            None,
        )
        newest = self.board()["panels"][0]["versions"][-1]
        self.assertEqual(newest["parent_file"], panel["file"])

    def test_approval_is_bound_to_the_panel_file_and_needs_review_state(self) -> None:
        panel_id = self.board()["panels"][0]["id"]
        self.write_decision(panel_id)
        MODULE.mark_panel(self.root, "scene-02", panel_id, "needs_edit", None)
        with self.assertRaises(MODULE.BoardError):
            MODULE.mark_panel(
                self.root, "scene-02", panel_id, "approved", "decision.json"
            )
        MODULE.mark_panel(self.root, "scene-02", panel_id, "review", None)
        write_png(self.panel_path(panel_id), 250)
        with self.assertRaises(MODULE.BoardError):
            MODULE.mark_panel(
                self.root, "scene-02", panel_id, "approved", "decision.json"
            )

    def test_a_panel_that_changes_after_approval_is_reported(self) -> None:
        panel_id = self.board()["panels"][0]["id"]
        self.write_decision(panel_id)
        MODULE.mark_panel(self.root, "scene-02", panel_id, "approved", "decision.json")
        board = self.board()
        board["panels"][0]["sha256"] = "f" * 64
        board["panels"][0]["versions"][-1]["sha256"] = "f" * 64
        self.rewrite(board)
        self.assertIn("board.decision_stale", self.finding_ids())

    def test_version_head_must_match_the_newest_version(self) -> None:
        board = self.board()
        board["panels"][0]["file"] = board["panels"][1]["file"]
        self.rewrite(board)
        self.assertIn("board.version_head", self.finding_ids())

    def test_board_files_are_flagged_by_path_even_with_another_hash(self) -> None:
        panel = self.board()["panels"][0]
        (self.root / "task_ids.json").write_text(
            json.dumps(
                {
                    "tasks": [
                        {
                            "references": [
                                {"path": "./" + panel["file"], "sha256": "b" * 64}
                            ]
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        self.assertIn("board.animatic_review_only", self.finding_ids())

    def test_a_registered_seedream_edit_of_a_panel_is_not_reported(self) -> None:
        panel = self.board()["panels"][0]
        reference = {"path": panel["file"], "sha256": panel["sha256"]}
        (self.root / "task_ids.json").write_text(
            json.dumps(
                {
                    "tasks": [
                        {
                            "model": "dola-seedream-5-0-pro-260628",
                            "references": [reference],
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        self.assertEqual(self.finding_ids(), [])
        (self.root / "task_ids.json").write_text(
            json.dumps(
                {
                    "tasks": [
                        {
                            "model": "dreamina-seedance-2-5-260628",
                            "references": [reference],
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        self.assertIn("board.animatic_review_only", self.finding_ids())

    def test_malformed_task_registry_does_not_crash_check(self) -> None:
        for content in (
            '{"tasks": null}',
            '{"tasks": {"a": 1}}',
            '{"tasks": ["x"]}',
            '{"tasks": [{"references": 5}]}',
            "not json",
        ):
            (self.root / "task_ids.json").write_text(content, encoding="utf-8")
            self.assertEqual(self.finding_ids(), [], content)

    def test_board_for_another_scene_and_foreign_shot_ids_are_reported(self) -> None:
        board = self.board()
        board["scene"] = "scene-03"
        self.rewrite(board)
        self.assertIn("board.scene", self.finding_ids())
        text = (self.root / "scenes/scene-02/scene.md").read_text(encoding="utf-8")
        (self.root / "scenes/scene-02/scene.md").write_text(
            text.replace("s02_sh030_a", "s03_sh030_a"), encoding="utf-8"
        )
        with self.assertRaises(MODULE.BoardError):
            MODULE.load_scene_source(self.root, "scene-02")

    def test_duplicate_shot_ids_in_the_plan_are_rejected(self) -> None:
        text = (self.root / "scenes/scene-02/scene.md").read_text(encoding="utf-8")
        (self.root / "scenes/scene-02/scene.md").write_text(
            text.replace("s02_sh030_a", "s02_sh020_a"), encoding="utf-8"
        )
        with self.assertRaises(MODULE.BoardError):
            MODULE.load_scene_source(self.root, "scene-02")

    def test_a_missing_plan_field_on_a_panel_is_a_warning(self) -> None:
        board = self.board()
        del board["panels"][0]["lens_intent"]
        self.rewrite(board)
        findings = [
            f
            for f in MODULE.check_board(self.root, "scene-02")
            if f.rule_id == "board.field_missing"
        ]
        self.assertEqual([f.severity for f in findings], ["warning"])

    def test_invalid_sub_beat_names_and_duplicate_overrides_are_rejected(self) -> None:
        text = (self.root / "scenes/scene-02/scene.md").read_text(encoding="utf-8")
        (self.root / "scenes/scene-02/scene.md").write_text(
            text.replace(
                "      job: establish\n",
                "      job: establish\n      sub_beats: [Draw Fast, 'a/b']\n",
            ),
            encoding="utf-8",
        )
        with self.assertRaises(MODULE.BoardError):
            MODULE.derive_panels(
                MODULE.load_scene_source(self.root, "scene-02"), "L3", {}
            )
        with self.assertRaises(MODULE.BoardError):
            MODULE.parse_overrides(["s02_sh010_a=L3=a", "s02_sh010_a=L1=b"])

    def test_board_status_follows_the_plan_status(self) -> None:
        self.assertEqual(self.board()["status"], "draft")
        self.change_plan("status: draft", "status: ready")
        MODULE.rebase_plan(self.root, "scene-02")
        self.assertEqual(self.board()["status"], "ready")

    def test_board_record_states_it_is_not_a_seedance_input(self) -> None:
        self.assertIs(self.board()["bind_to_seedance"], False)
        board = self.board()
        board["bind_to_seedance"] = True
        self.rewrite(board)
        self.assertEqual(self.finding_ids(), ["board.schema"])

    def test_animatic_size_follows_the_board_aspect_ratio(self) -> None:
        self.assertEqual(MODULE.default_animatic_size("16:9"), "1920x1080")
        self.assertEqual(MODULE.default_animatic_size("9:16"), "1080x1920")
        self.assertEqual(MODULE.default_animatic_size("21:9"), "1920x822")


class MalformedRecordTests(BoardTestCase):
    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_a_broken_sidecar_exits_two_instead_of_crashing(self) -> None:
        self.init("L2")
        self.register_all()
        MODULE.build_sheet(self.root, "scene-02", None)
        sidecar = next((self.root / "scenes/scene-02/board/sheet").glob("*.sheet.json"))
        sidecar.write_text("{not json", encoding="utf-8")
        result = self.run_cli("status", str(self.root), "02")
        self.assertEqual(result.returncode, 2)
        self.assertTrue(result.stderr.strip())

    def test_a_sidecar_missing_a_key_exits_two(self) -> None:
        self.init("L2")
        self.register_all()
        MODULE.build_sheet(self.root, "scene-02", None)
        sidecar = next((self.root / "scenes/scene-02/board/sheet").glob("*.sheet.json"))
        sidecar.write_text('{"version": 1}', encoding="utf-8")
        self.assertEqual(self.run_cli("status", str(self.root), "02").returncode, 2)

    def test_a_malformed_board_file_exits_two(self) -> None:
        self.init("L2")
        (self.root / "scenes/scene-02/board.md").write_text(
            "no front matter", encoding="utf-8"
        )
        self.assertEqual(self.run_cli("check", str(self.root), "02").returncode, 2)

    def test_every_command_runs_from_the_command_line(self) -> None:
        self.assertEqual(self.run_cli("init", str(self.root), "02").returncode, 0)
        board = self.board()
        panel = board["panels"][0]
        path = self.panel_path(panel["id"])
        write_png(path, 80)
        relative = path.relative_to(self.root).as_posix()
        self.assertEqual(
            self.run_cli(
                "register-panel", str(self.root), "02", panel["id"], "--file", relative
            ).returncode,
            0,
        )
        self.assertEqual(
            self.run_cli(
                "mark", str(self.root), "02", panel["id"], "--status", "needs_edit"
            ).returncode,
            0,
        )
        repair = self.run_cli(
            "repair-plan",
            str(self.root),
            "02",
            "--panels",
            panel["id"],
            "--dimension",
            "prop count",
            "--delta",
            "remove the jar",
            "--accept",
            "one jar",
        )
        self.assertEqual(repair.returncode, 0, repair.stderr)
        self.assertEqual(json.loads(repair.stdout)["actions"][0]["action"], "edit")
        self.assertEqual(
            self.run_cli("sheet", str(self.root), "02", "--pages", "1").returncode, 0
        )
        self.assertEqual(
            self.run_cli("review-page", str(self.root), "02").returncode, 0
        )
        self.assertEqual(self.run_cli("overview", str(self.root), "02").returncode, 0)
        self.assertEqual(
            self.run_cli("rebase-plan", str(self.root), "02").returncode, 0
        )


@unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg is required")
class AnimaticAudioTests(BoardTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.init("L1")
        self.register_all()

    def write_wav(self, name: str, seconds_long: float) -> str:
        import wave

        path = self.root / name
        with wave.open(str(path), "wb") as handle:
            handle.setnchannels(1)
            handle.setsampwidth(2)
            handle.setframerate(8000)
            handle.writeframes(b"\x00\x00" * int(8000 * seconds_long))
        return name

    def test_short_audio_is_padded_so_the_video_keeps_its_full_length(self) -> None:
        audio = self.write_wav("scratch.wav", 3)
        result = MODULE.build_animatic(self.root, "scene-02", "640x360", audio)
        self.assertAlmostEqual(result["duration_s"], 12.5)
        probe = subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-i",
                str(self.root / result["file"]),
                "-f",
                "null",
                "-",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        clock = (
            [line for line in probe.stderr.splitlines() if "time=" in line][-1]
            .split("time=")[1]
            .split()[0]
        )
        hours, minutes, secs = clock.split(":")
        self.assertAlmostEqual(
            int(hours) * 3600 + int(minutes) * 60 + float(secs), 12.5, delta=0.3
        )

    def test_changing_the_audio_marks_the_animatic_stale(self) -> None:
        audio = self.write_wav("scratch.wav", 3)
        MODULE.build_animatic(self.root, "scene-02", "640x360", audio)
        self.assertEqual(
            MODULE.status_report(self.root, "scene-02")["animatic"]["state"], "current"
        )
        self.write_wav("scratch.wav", 4)
        report = MODULE.status_report(self.root, "scene-02")["animatic"]
        self.assertEqual(report["state"], "stale")
        self.assertEqual(report["audio"], "changed")

    def test_rejected_panels_still_count_toward_the_animatic_length(self) -> None:
        MODULE.mark_panel(
            self.root, "scene-02", self.board()["panels"][0]["id"], "rejected", None
        )
        self.assertAlmostEqual(
            MODULE.build_animatic(self.root, "scene-02", "640x360", None)["duration_s"],
            12.5,
        )


class EditSourceTests(BoardTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.init("L2")
        self.register_all()
        self.panel = self.board()["panels"][0]
        (self.root / "project.md").write_text(
            "---\napproval_mode: approve_for_me\n---\n\n# Project\n", encoding="utf-8"
        )

    def write_review(self, **changes: object) -> str:
        record = {
            "schema_version": 1,
            "artifact_path": self.panel["file"],
            "artifact_sha256": self.panel["sha256"],
            "status": "pass",
            "inspection_method": "direct visual inspection of the full-resolution image",
            "coverage": "the whole panel image",
            "checks": [
                {
                    "criterion": "usable as the edit source",
                    "status": "pass",
                    "evidence": "fine",
                }
            ],
            "observations": ["Known defect to repair: an extra jar"],
            "limitations": ["Approved only as the input of one repair edit"],
            "recommendation": "Use as the edit source",
        }
        record.update(changes)
        path = self.root / "review_edit_source.json"
        path.write_text(json.dumps(record), encoding="utf-8")
        return "review_edit_source.json"

    def run_source(
        self, review: str | None = None, user_words: str | None = None
    ) -> dict:
        return MODULE.edit_source(
            self.root,
            "scene-02",
            self.panel["id"],
            review or self.write_review(),
            "approved only as the repair edit source",
            user_words,
        )

    def test_agent_decision_and_manifest_are_written_for_approve_for_me(self) -> None:
        result = self.run_source()
        decision = json.loads(
            (self.root / result["decision"]).read_text(encoding="utf-8")
        )
        self.assertEqual(decision["actor"], "agent")
        self.assertEqual(decision["selected_sha256"], self.panel["sha256"])
        self.assertNotIn("authorization", decision)
        manifest = (self.root / result["manifest"]).read_text(encoding="utf-8")
        self.assertIn("status: approved", manifest)
        self.assertEqual(result["panel_status"], "review")
        self.assertTrue(
            result["ref"].endswith(f":reference_image:{result['manifest']}")
        )

    def test_written_evidence_satisfies_the_request_validator(self) -> None:
        spec = importlib.util.spec_from_file_location(
            "request_validation_for_edit_source",
            ROOT / ".agents/scripts/validate_request.py",
        )
        assert spec is not None and spec.loader is not None
        validator = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = validator
        spec.loader.exec_module(validator)
        result = self.run_source()
        manifest = MODULE.split_front_matter(
            (self.root / result["manifest"]).read_text(encoding="utf-8")
        )[0]
        evidence = manifest["selection_evidence"]
        reference = {
            "path": self.panel["file"],
            "sha256": self.panel["sha256"],
            "role": "reference_image",
            "binding": "@Image 1",
            "approval_evidence": {
                "manifest": result["manifest"],
                "field": "selected_variant",
                **{
                    key: evidence[key]
                    for key in (
                        "decision_id",
                        "decision_path",
                        "decision_sha256",
                        "review_path",
                        "review_sha256",
                        "selected_sha256",
                    )
                },
            },
        }
        findings = validator.approval_decision_findings(
            self.root, reference, self.root / self.panel["file"]
        )
        self.assertEqual(findings, [])

    def test_ask_for_approval_needs_the_users_words(self) -> None:
        (self.root / "project.md").write_text(
            "---\napproval_mode: ask_for_approval\n---\n", encoding="utf-8"
        )
        (self.root / "studio").mkdir()
        with self.assertRaisesRegex(MODULE.BoardError, "user-words"):
            self.run_source()
        result = self.run_source(user_words="Yes, use that one for the fix")
        decision = json.loads(
            (self.root / result["decision"]).read_text(encoding="utf-8")
        )
        self.assertEqual(decision["actor"], "user")
        self.assertEqual(decision["authorization"]["source"], "chat")

    def test_stale_failing_or_mismatched_reviews_are_refused(self) -> None:
        for changes in (
            {"artifact_sha256": "0" * 64},
            {"status": "fail"},
            {"artifact_path": "scenes/scene-02/other.png"},
            {"checks": [{"criterion": "x", "status": "incomplete", "evidence": "x"}]},
        ):
            with self.subTest(changes=changes), self.assertRaises(MODULE.BoardError):
                self.run_source(self.write_review(**changes))

    def test_review_that_breaks_the_schema_is_refused(self) -> None:
        path = self.root / "bad_review.json"
        path.write_text('{"schema_version": 1}', encoding="utf-8")
        with self.assertRaises(MODULE.BoardError):
            self.run_source("bad_review.json")

    def test_changed_panel_missing_project_and_missing_review_are_refused(self) -> None:
        review = self.write_review()
        write_png(self.root / self.panel["file"], 250)
        with self.assertRaises(MODULE.BoardError):
            self.run_source(review)
        write_png(self.root / self.panel["file"], 40)
        (self.root / "project.md").unlink()
        with self.assertRaises(MODULE.BoardError):
            self.run_source(review)
        (self.root / "project.md").write_text(
            "---\napproval_mode: approve_for_me\n---\n"
        )
        with self.assertRaises(MODULE.BoardError):
            self.run_source("missing_review.json")

    def test_repair_plan_defaults_to_a_full_frame_bounding_box(self) -> None:
        result = MODULE.plan_repair(
            self.root,
            "scene-02",
            [self.panel["id"]],
            "local",
            "prop count",
            "remove it",
            ["gone"],
            None,
        )
        action = result["actions"][0]
        self.assertEqual(action["bbox"], "0,0,999,999")
        contract = (self.root / action["contract"]).read_text(encoding="utf-8")
        self.assertIn("full-frame bounding box 0,0,999,999", contract)

    def test_repair_plan_keeps_an_explicit_bounding_box(self) -> None:
        result = MODULE.plan_repair(
            self.root,
            "scene-02",
            [self.panel["id"]],
            "local",
            "prop count",
            "remove it",
            ["gone"],
            "10,20,300,400",
        )
        self.assertEqual(result["actions"][0]["bbox"], "10,20,300,400")

    def test_a_user_decision_from_chat_needs_a_studio_project_and_real_words(
        self,
    ) -> None:
        with self.assertRaisesRegex(MODULE.BoardError, "Studio"):
            self.run_source(user_words="Yes, use that one for the fix")
        (self.root / "studio").mkdir()
        with self.assertRaisesRegex(MODULE.BoardError, "own words"):
            self.run_source(user_words="ok")

    def test_user_words_make_a_user_decision_even_under_approve_for_me(self) -> None:
        (self.root / "studio").mkdir()
        result = self.run_source(user_words="Use this one for the fix")
        decision = json.loads(
            (self.root / result["decision"]).read_text(encoding="utf-8")
        )
        self.assertEqual(decision["actor"], "user")
        self.assertEqual(decision["approval_mode"], "approve_for_me")
        self.assertEqual(
            decision["authorization"],
            {"source": "chat", "evidence": "Use this one for the fix"},
        )

    def test_rerunning_with_the_same_inputs_keeps_the_decision_hash(self) -> None:
        first = self.run_source()
        before = (self.root / first["decision"]).read_bytes()
        second = self.run_source()
        self.assertEqual(before, (self.root / second["decision"]).read_bytes())

    def test_a_different_decision_for_the_same_panel_file_cannot_replace_it(
        self,
    ) -> None:
        first = self.run_source()
        before = (self.root / first["decision"]).read_bytes()
        (self.root / "project.md").write_text(
            "---\napproval_mode: approve_for_me\n---\n\nchanged\n", encoding="utf-8"
        )
        with self.assertRaisesRegex(MODULE.BoardError, "cannot be replaced"):
            self.run_source()
        self.assertEqual(before, (self.root / first["decision"]).read_bytes())

    def test_an_existing_manifest_keeps_its_other_front_matter_and_body(self) -> None:
        clip = self.panel["clip"]
        manifest = self.root / f"scenes/scene-02/{clip}/panel_{self.panel['id']}.md"
        manifest.write_text(
            "---\nowner: keep me\n---\n\nUser notes stay.\n", encoding="utf-8"
        )
        self.run_source()
        text = manifest.read_text(encoding="utf-8")
        self.assertIn("owner: keep me", text)
        self.assertIn("User notes stay.", text)
        self.assertIn("status: approved", text)

    def test_an_edit_source_decision_cannot_approve_the_final_panel(self) -> None:
        result = self.run_source()
        with self.assertRaisesRegex(MODULE.BoardError, "edit-source"):
            MODULE.mark_panel(
                self.root, "scene-02", self.panel["id"], "approved", result["decision"]
            )
        self.assertEqual(self.board()["panels"][0]["status"], "review")

    def test_a_final_approval_must_be_an_approved_selection_of_this_panel(self) -> None:
        panel_id = self.panel["id"]
        for changes in (
            {"result": "rejected"},
            {"selected_sha256": "c" * 64},
            {"subject_path": "scenes/scene-02/other.png"},
            {"decision_type": "stage_lock"},
        ):
            with self.subTest(changes=changes), self.assertRaises(MODULE.BoardError):
                MODULE.mark_panel(
                    self.root,
                    "scene-02",
                    panel_id,
                    "approved",
                    self.write_decision(panel_id, **changes),
                )

    def test_a_malformed_project_file_is_a_board_error(self) -> None:
        (self.root / "project.md").write_bytes(b"---\n\xff\xfe\n---\n")
        with self.assertRaises(MODULE.BoardError):
            self.run_source()
        (self.root / "project.md").write_text(
            "---\napproval_mode: [a]\n---\n", encoding="utf-8"
        )
        with self.assertRaises(MODULE.BoardError):
            self.run_source()

    def test_a_symlinked_manifest_is_refused_before_anything_is_written(self) -> None:
        outside = Path(tempfile.mkdtemp(prefix="scene-board-outside-"))
        self.addCleanup(shutil.rmtree, outside)
        clip = self.panel["clip"]
        manifest = self.root / f"scenes/scene-02/{clip}/panel_{self.panel['id']}.md"
        manifest.symlink_to(outside / "target.md")
        with self.assertRaisesRegex(MODULE.BoardError, "symlink"):
            self.run_source()
        self.assertEqual(list((self.root / "decisions").glob("*.json")), [])

    def test_the_full_frame_default_warns_and_an_explicit_box_does_not(self) -> None:
        default = MODULE.plan_repair(
            self.root,
            "scene-02",
            [self.panel["id"]],
            "local",
            "prop count",
            "remove it",
            ["gone"],
            None,
        )["actions"][0]
        self.assertIn("full-frame", default["warning"])
        self.assertEqual(
            default["bbox_request_format"], {"x1": 0, "y1": 0, "x2": 999, "y2": 999}
        )
        explicit = MODULE.plan_repair(
            self.root,
            "scene-02",
            [self.panel["id"]],
            "local",
            "prop count",
            "remove it",
            ["gone"],
            "010,20,300,400",
        )["actions"][0]
        self.assertIsNone(explicit["warning"])
        self.assertEqual(explicit["bbox"], "10,20,300,400")
        contract = (self.root / explicit["contract"]).read_text(encoding="utf-8")
        self.assertIn("bounding box 10,20,300,400", contract)

    def test_command_line_runs_edit_source(self) -> None:
        review = self.write_review()
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "edit-source",
                str(self.root),
                "02",
                self.panel["id"],
                "--review",
                review,
                "--reason",
                "edit source",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("ref", json.loads(completed.stdout))


if __name__ == "__main__":
    unittest.main()
