from __future__ import annotations

import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

import test_seedance_capability_profiles as profiles

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents/skills/prompt-review/scripts/record_review.py"
SPEC = importlib.util.spec_from_file_location("record_review", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)
validation = MODULE.validation


class RecordReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory(prefix="record-review-test-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name) / "demo"
        (self.root / "elements/hero").mkdir(parents=True)
        (self.root / "requests").mkdir()
        (self.root / "project.md").write_text(
            "---\napproval_mode: approve_for_me\n---\n"
        )
        (self.root / "elements/hero/char_hero_v01.png").write_bytes(b"hero")
        (self.root / "prompt_s01_sh010_t01_v01.md").write_text("@Image 1 waves.\n")
        references = [
            {
                "path": "elements/hero/char_hero_v01.png",
                "sha256": hashlib.sha256(b"hero").hexdigest(),
                "role": "reference_image",
                "binding": "@Image 1",
                "approval_evidence": {
                    "manifest": "elements/hero/character.md",
                    "field": "selected_variant",
                },
            }
        ]
        prompt = (self.root / "prompt_s01_sh010_t01_v01.md").read_bytes()
        params = {"duration": 5}
        self.hash = validation.compute_request_hash(
            prompt, references, "fixture-model", "generate", params
        )
        request = {
            "schema_version": 1,
            "operation_id": "fixture-s01-sh010-t01-v01",
            "asset_id": "s01_sh010_t01_v01",
            "transport": "ark-mcp",
            "model": "fixture-model",
            "operation": "generate",
            "prompt_file": "prompt_s01_sh010_t01_v01.md",
            "prompt_sha256": hashlib.sha256(prompt).hexdigest(),
            "request_sha256": self.hash,
            "references": references,
            "params": params,
            "submission_status": "prepared",
            "provider_task_id": None,
            "provider_status": None,
            "review_status": "not_started",
            "cost": {"estimated": None, "confirmed": None, "currency": "USD"},
        }
        (self.root / "requests/request_s01_sh010_t01_v01.json").write_text(
            json.dumps(request)
        )
        self.input = Path(self.directory.name) / "reviewer.txt"

    def review(
        self, request_hash: str, rule: str = "asset.visible_consistency"
    ) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "request_sha256": request_hash,
            "reviewer_status": "complete",
            "checks": [{"rule_id": rule, "status": "pass", "evidence": "Checked"}],
        }

    def run_cli(self, *extra: str, text: str) -> tuple[int, dict[str, Any]]:
        self.input.write_text(text)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = MODULE.main(
                ["--project", str(self.root), "--input", str(self.input), *extra]
            )
        return code, json.loads(output.getvalue())

    def fenced(self, *reviews: dict[str, Any]) -> str:
        blocks = "\n".join(
            f"```json\n{json.dumps(review, indent=2)}\n```" for review in reviews
        )
        return f"Review notes {{brace}} follow.\n\n{blocks}\n\nNo CRITICAL findings.\n"

    def test_extracts_matching_review_from_fenced_prose(self) -> None:
        text = self.fenced(self.review("0" * 64), self.review(self.hash))
        code, result = self.run_cli(
            "--request",
            "requests/request_s01_sh010_t01_v01.json",
            "--required-rule",
            "asset.visible_consistency",
            text=text,
        )
        self.assertEqual(code, 0, result)
        self.assertEqual(result["review"], self.review(self.hash))
        self.assertFalse((self.root / "reviews").exists())

    def test_raw_json_input(self) -> None:
        review = self.review(self.hash)
        self.assertEqual(MODULE.extract_review(json.dumps(review), self.hash), review)

    def test_mismatched_hash_is_rejected(self) -> None:
        code, result = self.run_cli(
            "--request",
            "requests/request_s01_sh010_t01_v01.json",
            "--write",
            text=self.fenced(self.review("0" * 64)),
        )
        self.assertEqual(code, 1)
        self.assertIn("request hash", result["findings"][0]["message"])
        self.assertFalse((self.root / "reviews").exists())

    def test_missing_required_rule_is_rejected(self) -> None:
        code, result = self.run_cli(
            "--request",
            "requests/request_s01_sh010_t01_v01.json",
            "--required-rule",
            "references.ordered_bindings",
            "--write",
            text=self.fenced(self.review(self.hash)),
        )
        self.assertEqual(code, 1)
        self.assertIn(
            "Missing required rule: references.ordered_bindings",
            [finding["message"] for finding in result["findings"]],
        )
        self.assertFalse((self.root / "reviews").exists())

    def test_write_path_and_no_overwrite(self) -> None:
        args = ("--request", "requests/request_s01_sh010_t01_v01.json", "--write")
        code, result = self.run_cli(*args, text=self.fenced(self.review(self.hash)))
        self.assertEqual(code, 0, result)
        self.assertEqual(result["path"], "reviews/review_s01_sh010_t01_v01.json")
        path = self.root / result["path"]
        self.assertEqual(json.loads(path.read_text()), self.review(self.hash))
        self.assertEqual(
            result["review_sha256"], hashlib.sha256(path.read_bytes()).hexdigest()
        )
        code, _ = self.run_cli(*args, text=self.fenced(self.review(self.hash)))
        self.assertEqual(code, 0)
        original = path.read_bytes()
        code, result = self.run_cli(
            *args,
            text=self.fenced(self.review(self.hash, "narrative.observable_event")),
        )
        self.assertEqual(code, 1)
        self.assertIn("overwrite", result["findings"][0]["message"])
        self.assertEqual(path.read_bytes(), original)

    def test_stale_request_file_is_rejected(self) -> None:
        (self.root / "prompt_s01_sh010_t01_v01.md").write_text("@Image 1 bows.\n")
        code, result = self.run_cli(
            "--request",
            "requests/request_s01_sh010_t01_v01.json",
            text=self.fenced(self.review(self.hash)),
        )
        self.assertEqual(code, 1)
        self.assertIn("stale", result["findings"][0]["message"])

    def test_no_profile_v2_recorder_preserves_historical_hash_fields(self) -> None:
        path = self.root / "requests/request_s01_sh010_t01_v01.json"
        request = json.loads(path.read_text())
        prompt = b"A performer waves.\n"
        (self.root / request["prompt_file"]).write_bytes(prompt)
        request.update(schema_version=2, references=[], approval_mode="approve_for_me",
                       prompt_sha256=hashlib.sha256(prompt).hexdigest(),
                       project_sha256=hashlib.sha256(
                           (self.root / "project.md").read_bytes()).hexdigest())
        body = {key: request[key] for key in (
            "prompt_sha256", "model", "operation", "params", "references",
            "approval_mode", "project_sha256")}
        digest = hashlib.sha256(json.dumps(
            body, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
            allow_nan=False).encode()).hexdigest()
        request["request_sha256"] = digest
        path.write_text(json.dumps(request))
        code, result = self.run_cli(
            "--request", path.relative_to(self.root).as_posix(), "--write",
            text=self.fenced(self.review(digest)))
        self.assertEqual(code, 0, result)
        self.assertEqual(result["request_sha256"], digest)
        self.assertEqual(path.read_text(), json.dumps(request))

    def test_request_path_must_stay_in_project(self) -> None:
        code, _ = self.run_cli(
            "--request", "../outside.json", text=self.fenced(self.review(self.hash))
        )
        self.assertEqual(code, 1)

    def test_text_only_audio_by_hash_and_asset(self) -> None:
        audio_hash = "a" * 64
        code, result = self.run_cli(
            "--request-sha256",
            audio_hash,
            "--asset",
            "amb_market_v01",
            "--write",
            text=self.fenced(self.review(audio_hash)),
        )
        self.assertEqual(code, 0, result)
        self.assertTrue((self.root / "reviews/review_amb_market_v01.json").is_file())
        code, _ = self.run_cli(
            "--request-sha256",
            audio_hash,
            "--asset",
            "../escape",
            text=self.fenced(self.review(audio_hash)),
        )
        self.assertEqual(code, 1)


class PreparedProfileReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = profiles.ProfilePreparationTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root

    def prepare_command(self, version: int) -> list[str]:
        command = self.fixture.command()
        command.insert(1, "-B")
        command.extend(["--schema-version", str(version)])
        if version == 2:
            (self.root / "project.md").write_text(
                "---\napproval_mode: approve_for_me\nreview_mode: strict\n---\n"
            )
            (self.root / "studio").mkdir(exist_ok=True)
            while "--ref" in command:
                index = command.index("--ref")
                del command[index:index + 2]
            (self.root / self.fixture.fixture.prompt).write_text(
                "A performer walks through a quiet room.\n"
            )
        return command

    def execute(self, command: list[str], text: str | None = None) -> dict[str, Any]:
        result = subprocess.run(command, input=text, capture_output=True,
                                text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def recorder(self, request_path: str) -> list[str]:
        return [sys.executable, "-B", str(SCRIPT), "--project", str(self.root),
                "--request", request_path, "--input", "-",
                "--required-rule", "model.supported_mode", "--write"]

    def review(self, request_hash: str) -> dict[str, Any]:
        return {
            "schema_version": 1, "request_sha256": request_hash,
            "reviewer_status": "complete",
            "checks": [{"rule_id": "model.supported_mode", "status": "pass",
                        "evidence": "Checked synthetic offline profile controls and bindings"}],
        }

    def test_actual_profile_prepare_record_and_register_default_v1(self) -> None:
        self.prepare_record_register(1)

    def test_actual_profile_prepare_record_and_register_strict_v2(self) -> None:
        self.prepare_record_register(2)

    def prepare_record_register(self, version: int) -> None:
        command = self.prepare_command(version)
        prepared = self.execute(command)
        request = json.loads((self.root / prepared["path"]).read_text())
        self.assertEqual(request["schema_version"], version)
        self.assertEqual(validation.validate_request(
            self.root, request, self.fixture.evidence), [])
        review = self.review(request["request_sha256"])
        recorded = self.execute(self.recorder(prepared["path"]), json.dumps(review))
        self.assertEqual(json.loads((self.root / recorded["path"]).read_text()), review)
        registered = self.execute(command + [
            "--register", "--review", recorded["path"],
            "--required-rule", "model.supported_mode",
        ])
        registry = profiles.store.read_registry(self.root / "task_ids.json")
        self.assertEqual(registry["tasks"], [request])
        self.assertEqual(registered["registered"], request["operation_id"])
        profiles.store.transition_operation(
            self.root, request["operation_id"], "prepared", "submitting")
        self.assertEqual(profiles.store.read_registry(
            self.root / "task_ids.json")["tasks"][0]["submission_status"], "submitting")

    def test_profile_request_mutations_reject_recording_without_writes(self) -> None:
        prepared = self.execute(self.prepare_command(2))
        path = self.root / prepared["path"]
        original = json.loads(path.read_text())
        for change in ("params", "evidence", "expected", "digest", "missing", "project"):
            with self.subTest(change=change):
                request = copy.deepcopy(original)
                bound = request["extensions"]["capability_profile"]
                if change == "params":
                    request["params"]["duration"] = 9
                elif change == "evidence":
                    bound["evidence"]["source"] = "Changed offline evidence"
                elif change == "expected":
                    bound["expected"]["tool_schema_revision"] = "different-revision"
                elif change == "digest":
                    bound["sha256"] = "0" * 64
                elif change == "missing":
                    del request["extensions"]["capability_profile"]
                else:
                    request["project_sha256"] = "0" * 64
                path.write_text(json.dumps(request))
                before = {entry.relative_to(self.root): entry.read_bytes()
                          for entry in self.root.rglob("*") if entry.is_file()}
                result = subprocess.run(
                    self.recorder(prepared["path"]),
                    input=json.dumps(self.review(original["request_sha256"])),
                    capture_output=True, text=True, check=False,
                )
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("stale", result.stdout)
                self.assertEqual(before, {
                    entry.relative_to(self.root): entry.read_bytes()
                    for entry in self.root.rglob("*") if entry.is_file()
                })
                self.assertFalse((self.root / "reviews").exists())


if __name__ == "__main__":
    unittest.main()
