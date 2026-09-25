from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".agents/scripts"))
SPEC = importlib.util.spec_from_file_location(
    "prepare_request", ROOT / ".agents/scripts/prepare_request.py"
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)
validation = sys.modules["validate_request"]

CAPABILITIES = {
    "model": "dreamina-seedance-2-5-260628",
    "source": "fixture tool schema",
    "verified_at": "2026-09-24T00:00:00Z",
    "operations": ["generate"],
    "parameters": {
        "resolution": {"enum": ["720p"]},
        "ratio": {"enum": ["9:16"]},
        "duration": {"type": "integer", "minimum": 4, "maximum": 30},
        "generate_audio": {"type": "boolean"},
    },
    "required_parameters": ["resolution", "ratio", "duration"],
    "reference_roles": ["reference_image", "reference_video"],
    "max_references": 5,
    "supports_first_frame_with_reference_images": False,
}


def sha(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


class PrepareRequestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory(prefix="prepare-request-test-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name) / "demo"
        element = self.root / "elements/hero"
        element.mkdir(parents=True)
        (self.root / "project.md").write_text(
            "# Demo\n\nLegacy brief without an explicit approval mode.\n"
        )
        (element / "char_hero_v01.png").write_bytes(b"hero image")
        (element / "vid_hero_motion_v01.mp4").write_bytes(b"hero video")
        (element / "prop_hero_v01.png").write_bytes(b"prop image")
        (element / "character.md").write_text(
            "---\nselected_variant: char_hero_v01.png\n---\n"
        )
        (element / "motion.md").write_text(
            "---\nselected_variant: vid_hero_motion_v01.mp4\n---\n"
        )
        (element / "prop.md").write_text(
            "---\nselected_variant: prop_hero_v01.png\n---\n"
        )
        shot = self.root / "scenes/scene-01/s01_sh010"
        shot.mkdir(parents=True)
        self.prompt = "scenes/scene-01/s01_sh010/prompt_s01_sh010_t01_v01.md"
        (self.root / self.prompt).write_text(
            "@Image 1 walks as in @Video 1 and lifts @Image 2.\n"
        )
        (self.root / "capabilities").mkdir()
        (self.root / "capabilities/seedance-2-5.json").write_text(
            json.dumps(CAPABILITIES)
        )

    def argv(self, *extra: str) -> list[str]:
        return [
            "--project",
            str(self.root),
            "--asset",
            "s01_sh010_t01_v01",
            "--prompt",
            self.prompt,
            "--model",
            "dreamina-seedance-2-5-260628",
            "--operation",
            "generate",
            "--param",
            "resolution=720p",
            "--param",
            "ratio=9:16",
            "--param",
            "duration=8",
            "--param",
            "generate_audio=true",
            "--ref",
            "elements/hero/char_hero_v01.png:reference_image:elements/hero/character.md",
            "--ref",
            "elements/hero/vid_hero_motion_v01.mp4:reference_video:elements/hero/motion.md",
            "--ref",
            "elements/hero/prop_hero_v01.png:reference_image:elements/hero/prop.md:selected_variant",
            "--expected-output",
            "scenes/scene-01/s01_sh010/vid_s01_sh010_t01_v01.mp4",
            *extra,
        ]

    def run_cli(self, argv: list[str]) -> tuple[int, dict[str, Any]]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = MODULE.main(argv)
        return code, json.loads(output.getvalue())

    def write_review(self, request_hash: str) -> None:
        (self.root / "reviews").mkdir(exist_ok=True)
        (self.root / "reviews/review_s01_sh010_t01_v01.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "request_sha256": request_hash,
                    "reviewer_status": "complete",
                    "checks": [
                        {
                            "rule_id": "references.ordered_bindings",
                            "status": "pass",
                            "evidence": "Bindings match inputs",
                        }
                    ],
                }
            )
        )

    def test_dry_run_builds_valid_request_and_writes_nothing(self) -> None:
        code, result = self.run_cli(self.argv())
        self.assertEqual(code, 0, result)
        request = result["request"]
        self.assertEqual(
            validation.schema_findings(request, "generation-request.schema.json"), []
        )
        self.assertEqual(
            request["operation_id"],
            "seedance25-s01-sh010-t01-v01-" + datetime.now(UTC).strftime("%Y%m%d"),
        )
        self.assertEqual(request["submission_status"], "prepared")
        self.assertIsNone(request["provider_task_id"])
        self.assertEqual(
            request["extensions"]["expected_output"],
            "scenes/scene-01/s01_sh010/vid_s01_sh010_t01_v01.mp4",
        )
        self.assertFalse((self.root / "requests").exists())
        self.assertFalse((self.root / "task_ids.json").exists())

    def test_hash_is_deterministic_and_matches_validator(self) -> None:
        _, first = self.run_cli(self.argv())
        _, second = self.run_cli(self.argv())
        self.assertEqual(first["request_sha256"], second["request_sha256"])
        request = first["request"]
        expected = validation.compute_request_hash(
            (self.root / self.prompt).read_bytes(),
            request["references"],
            request["model"],
            request["operation"],
            request["params"],
        )
        self.assertEqual(request["request_sha256"], expected)
        self.assertEqual(first["request_sha256"], expected)

    def test_bindings_follow_order_and_media_kind(self) -> None:
        _, result = self.run_cli(self.argv())
        references = result["request"]["references"]
        self.assertEqual(
            [ref["binding"] for ref in references],
            ["@Image 1", "@Video 1", "@Image 2"],
        )
        self.assertEqual(references[0]["sha256"], sha(b"hero image"))
        self.assertEqual(
            references[1]["approval_evidence"],
            {"manifest": "elements/hero/motion.md", "field": "selected_variant"},
        )

    def test_param_typing(self) -> None:
        params = MODULE.parse_params(
            [
                "ratio=9:16",
                "duration=8",
                "audio=true",
                "res=720p",
                'label="8"',
                "x=null",
            ]
        )
        self.assertEqual(
            params,
            {
                "ratio": "9:16",
                "duration": 8,
                "audio": True,
                "res": "720p",
                "label": "8",
                "x": None,
            },
        )
        self.assertEqual(MODULE.parse_params(["v=NaN"]), {"v": "NaN"})
        with self.assertRaises(ValueError):
            MODULE.parse_params(["a=1", "a=2"])

    def test_rejects_traversal_and_absolute_paths(self) -> None:
        outside = Path(self.directory.name) / "outside.png"
        outside.write_bytes(b"outside")
        for ref in (
            "../outside.png:reference_image:elements/hero/character.md",
            f"{outside}:reference_image:elements/hero/character.md",
        ):
            argv = self.argv()
            argv[argv.index("--ref") + 1] = ref
            code, result = self.run_cli(argv + ["--write"])
            self.assertEqual(code, 1)
            self.assertFalse(result["ok"])
        argv = self.argv()
        argv[argv.index("--prompt") + 1] = "../prompt.md"
        code, _ = self.run_cli(argv)
        self.assertEqual(code, 1)
        self.assertFalse((self.root / "requests").exists())

    def test_unselected_reference_blocks_write(self) -> None:
        (self.root / "elements/hero/prop.md").write_text(
            "---\nselected_variant: auto\n---\n"
        )
        code, result = self.run_cli(self.argv("--write"))
        self.assertEqual(code, 1)
        self.assertIn(
            "approval.explicit_choice", [f["rule_id"] for f in result["findings"]]
        )
        self.assertFalse((self.root / "requests").exists())

    def test_write_refuses_to_overwrite_different_request(self) -> None:
        code, result = self.run_cli(self.argv("--write"))
        self.assertEqual(code, 0, result)
        path = self.root / "requests/request_s01_sh010_t01_v01.json"
        self.assertEqual(result["path"], "requests/request_s01_sh010_t01_v01.json")
        written = json.loads(path.read_text())
        self.assertEqual(written["request_sha256"], result["request_sha256"])
        code, _ = self.run_cli(self.argv("--write"))
        self.assertEqual(code, 0)
        original = path.read_bytes()
        argv = self.argv("--write")
        argv[argv.index("duration=8")] = "duration=10"
        code, result = self.run_cli(argv)
        self.assertEqual(code, 1)
        self.assertIn("overwrite", result["findings"][0]["message"])
        self.assertEqual(path.read_bytes(), original)

    def test_register_appends_once(self) -> None:
        _, dry = self.run_cli(self.argv())
        self.write_review(dry["request_sha256"])
        register = (
            "--write",
            "--register",
            "--review",
            "reviews/review_s01_sh010_t01_v01.json",
            "--capabilities",
            "capabilities/seedance-2-5.json",
            "--required-rule",
            "references.ordered_bindings",
        )
        code, result = self.run_cli(self.argv(*register))
        self.assertEqual(code, 0, result)
        self.assertEqual(result["registered"], dry["request"]["operation_id"])
        tasks = json.loads((self.root / "task_ids.json").read_text())["tasks"]
        self.assertEqual(tasks, [dry["request"]])
        code, result = self.run_cli(self.argv(*register))
        self.assertEqual(code, 1)
        self.assertEqual(result["findings"][0]["rule_id"], "registry.prepare")
        tasks = json.loads((self.root / "task_ids.json").read_text())["tasks"]
        self.assertEqual(len(tasks), 1)

    def test_register_rejects_stale_review_before_writing(self) -> None:
        self.write_review("0" * 64)
        code, result = self.run_cli(
            self.argv(
                "--write",
                "--register",
                "--review",
                "reviews/review_s01_sh010_t01_v01.json",
                "--capabilities",
                "capabilities/seedance-2-5.json",
            )
        )
        self.assertEqual(code, 1)
        self.assertIn(
            "review.complete_evidence", [f["rule_id"] for f in result["findings"]]
        )
        self.assertFalse((self.root / "requests").exists())
        self.assertFalse((self.root / "task_ids.json").exists())

    def test_text_only_request_and_model_family(self) -> None:
        (self.root / "library").mkdir()
        (self.root / "library/prompt_amb_market_v01.md").write_text(
            "Market ambience.\n"
        )
        code, result = self.run_cli(
            [
                "--project",
                str(self.root),
                "--asset",
                "amb_market_v01",
                "--prompt",
                "library/prompt_amb_market_v01.md",
                "--model",
                "seed-audio-1.0",
                "--operation",
                "generate",
                "--expected-output",
                "library/amb_market_v01.wav",
                "--operation-id",
                "seedaudio-amb-market-v01",
            ]
        )
        self.assertEqual(code, 0, result)
        self.assertEqual(result["request"]["references"], [])
        self.assertEqual(result["request"]["operation_id"], "seedaudio-amb-market-v01")
        self.assertEqual(
            MODULE.model_family("dola-seedream-5-0-pro-260628"), "seedream50pro"
        )

    def v2_argv(self, *extra: str) -> list[str]:
        (self.root / self.prompt).write_text("@Image 1 waves.\n")
        argv = self.argv(*extra)
        for _ in range(2):
            index = argv.index("--ref", argv.index("--ref") + 1)
            del argv[index : index + 2]
        return argv

    def record_selection(self) -> None:
        (self.root / "project.md").write_text(
            "---\napproval_mode: approve_for_me\n---\n# Demo\n"
        )
        generator = ROOT / ".agents/skills/showcase-html/scripts/generate_showcase.py"
        initialized = subprocess.run(
            [sys.executable, str(generator), str(self.root), "--init"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            initialized.returncode, 0, initialized.stdout + initialized.stderr
        )
        image = "elements/hero/char_hero_v01.png"
        project_sha = sha((self.root / "project.md").read_bytes())
        review = {
            "schema_version": 1,
            "artifact_path": image,
            "artifact_sha256": sha(b"hero image"),
            "status": "pass",
            "inspection_method": "direct image inspection",
            "coverage": "full image",
            "checks": [
                {"criterion": "identity", "status": "pass", "evidence": "Clear"}
            ],
            "observations": ["Complete"],
            "limitations": [],
            "recommendation": "Select",
        }
        (self.root / "reviews").mkdir(exist_ok=True)
        review_bytes = json.dumps(review).encode()
        (self.root / "reviews/candidate_hero.json").write_bytes(review_bytes)
        decision = {
            "schema_version": 1,
            "decision_id": "hero-select",
            "decision_type": "variant_selection",
            "asset_id": "char_hero",
            "subject_path": image,
            "selected_variant": "char_hero_v01.png",
            "selected_sha256": sha(b"hero image"),
            "actor": "agent",
            "approval_mode": "approve_for_me",
            "project_sha256": project_sha,
            "result": "approved",
            "review_path": "reviews/candidate_hero.json",
            "review_sha256": sha(review_bytes),
            "upstream_sha256": {},
            "reason": "Passing option",
            "decided_at": "2026-09-24T00:00:00Z",
        }
        (self.root / "decisions").mkdir()
        decision_bytes = json.dumps(decision).encode()
        (self.root / "decisions/hero-select.json").write_bytes(decision_bytes)
        evidence = {
            "decision_id": "hero-select",
            "decision_path": "decisions/hero-select.json",
            "decision_sha256": sha(decision_bytes),
            "review_path": "reviews/candidate_hero.json",
            "review_sha256": sha(review_bytes),
            "selected_sha256": sha(b"hero image"),
            "actor": "agent",
            "approval_mode": "approve_for_me",
        }
        (self.root / "elements/hero/character.md").write_text(
            "---\nselected_variant: char_hero_v01.png\nstatus: approved\n"
            "selection_evidence:\n"
            + "".join(f"  {key}: {value}\n" for key, value in evidence.items())
            + "---\n"
        )

    def test_v2_build_uses_canvas_contract_and_manifest_evidence(self) -> None:
        self.record_selection()
        code, result = self.run_cli(self.v2_argv())
        self.assertEqual(code, 0, result)
        request = result["request"]
        self.assertEqual(request["schema_version"], 2)
        self.assertEqual(request["approval_mode"], "approve_for_me")
        self.assertEqual(
            request["project_sha256"], sha((self.root / "project.md").read_bytes())
        )
        evidence = request["references"][0]["approval_evidence"]
        self.assertEqual(evidence["decision_path"], "decisions/hero-select.json")
        self.assertEqual(evidence["selected_sha256"], sha(b"hero image"))
        self.assertEqual(
            request["request_sha256"],
            validation.compute_request_hash(
                (self.root / self.prompt).read_bytes(),
                request["references"],
                request["model"],
                request["operation"],
                request["params"],
                approval_mode=request["approval_mode"],
                project_sha256=request["project_sha256"],
            ),
        )
        code, result = self.run_cli(self.v2_argv("--schema-version", "1"))
        self.assertEqual(code, 0, result)
        self.assertEqual(result["request"]["schema_version"], 1)

    def test_v2_register_on_canvas_v1_project(self) -> None:
        self.record_selection()
        _, dry = self.run_cli(self.v2_argv())
        self.write_review(dry["request_sha256"])
        code, result = self.run_cli(
            self.v2_argv(
                "--write",
                "--register",
                "--review",
                "reviews/review_s01_sh010_t01_v01.json",
                "--capabilities",
                "capabilities/seedance-2-5.json",
                "--required-rule",
                "references.ordered_bindings",
            )
        )
        self.assertEqual(code, 0, result)
        tasks = json.loads((self.root / "task_ids.json").read_text())["tasks"]
        self.assertEqual(tasks, [dry["request"]])
        self.assertEqual(tasks[0]["schema_version"], 2)

    def register_argv(self) -> list[str]:
        return self.v2_argv(
            "--write",
            "--register",
            "--review",
            "reviews/review_s01_sh010_t01_v01.json",
            "--capabilities",
            "capabilities/seedance-2-5.json",
        )

    def test_stale_canvas_blocks_register_with_regeneration_hint(self) -> None:
        self.record_selection()
        _, dry = self.run_cli(self.v2_argv())
        self.write_review(dry["request_sha256"])
        (self.root / "index.html").unlink()
        code, result = self.run_cli(self.register_argv())
        self.assertEqual(code, 1)
        canvas = [
            f for f in result["findings"] if f["rule_id"] == "approval.current_canvas"
        ]
        self.assertEqual(len(canvas), 1, result)
        self.assertIn("--stage brief-development", canvas[0]["message"])
        self.assertFalse((self.root / "requests").exists())
        self.assertFalse((self.root / "task_ids.json").exists())

    def test_explicit_project_mode_selects_v2(self) -> None:
        self.record_selection()
        (self.root / "showcase.json").unlink()
        code, result = self.run_cli(self.v2_argv())
        self.assertEqual(code, 0, result)
        self.assertEqual(result["request"]["schema_version"], 2)
        _, dry = self.run_cli(self.v2_argv())
        self.write_review(dry["request_sha256"])
        code, result = self.run_cli(self.register_argv())
        self.assertEqual(code, 1)
        self.assertIn(
            "approval.current_canvas", [f["rule_id"] for f in result["findings"]]
        )
        self.assertIn("--init", result["findings"][-1]["message"])

    def test_v2_missing_selection_evidence_is_actionable(self) -> None:
        (self.root / "project.md").write_text(
            "---\napproval_mode: ask_for_approval\n---\n# Demo\n"
        )
        code, result = self.run_cli(self.v2_argv("--write"))
        self.assertEqual(code, 1)
        message = result["findings"][0]["message"]
        self.assertIn("elements/hero/character.md has no structured", message)
        self.assertIn("--ref-legacy elements/hero/char_hero_v01.png=", message)
        self.assertFalse((self.root / "requests").exists())

    def test_v2_legacy_selection_uses_audit_log(self) -> None:
        (self.root / "showcase.json").write_text(
            json.dumps({"canvas": {"approvalContractVersion": 1}})
        )
        (self.root / "elements/hero/character.md").write_text(
            "---\nselected_variant: char_hero_v01.png\nstatus: approved\n---\n"
        )
        (self.root / "selection.log").write_text(
            json.dumps({"selections": {"char_hero": "char_hero_v01.png"}}) + "\n"
        )
        code, result = self.run_cli(
            self.v2_argv("--ref-legacy", "elements/hero/char_hero_v01.png=char_hero")
        )
        self.assertEqual(code, 0, result)
        evidence = result["request"]["references"][0]["approval_evidence"]
        self.assertEqual(evidence["evidence_type"], "legacy")
        self.assertEqual(
            evidence["audit_sha256"],
            sha((self.root / "selection.log").read_bytes()),
        )


if __name__ == "__main__":
    unittest.main()
