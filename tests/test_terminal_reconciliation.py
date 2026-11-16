from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

import test_prepare_request as fixtures

ROOT = Path(__file__).resolve().parents[1]
operation_store = sys.modules["operation_store"]
TERMINAL_RESULTS = ("succeeded", "failed", "cancelled", "canceled", "expired", "moderation_rejected")


class TerminalReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.PrepareRequestTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root
        code, dry = self.fixture.run_cli(self.fixture.argv())
        self.assertEqual(code, 0, dry)
        self.request = dry["request"]
        self.fixture.write_review(self.request["request_sha256"])
        self.registry_path = self.root / "task_ids.json"
        self.receipt_path = self.root / "requests/request_s01_sh010_t01_v01.json"
        self.evidence_path = self.root / "provider-result.json"
        self.evidence_path.write_text(json.dumps({"task_id": "job-123", "status": "succeeded"}))

    def adopt_args(self, status):
        extra = [] if status is None else ["--adopt-provider-status", status]
        return self.fixture.register_args(
            "--adopt-provider-task-id", "job-123", "--adopt-terminal", *extra
        )

    def adopt(self, status):
        code, result = self.fixture.run_cli(self.adopt_args(status))
        self.assertEqual(code, 0, result)
        return json.loads(self.registry_path.read_text())["tasks"][0]

    def historical(self, **changes):
        code, result = self.fixture.run_cli(self.fixture.argv("--write"))
        self.assertEqual(code, 0, result)
        record = copy.deepcopy(self.request)
        record.update(
            submission_status="terminal", provider_task_id="job-123",
            provider_status="completed", **changes,
        )
        other = copy.deepcopy(record)
        other.update(operation_id="unrelated-history", asset_id="other", provider_task_id="other-job")
        self.registry_path.write_text(json.dumps({"schema_version": 1, "tasks": [record, other]}))
        return record

    def reconcile(self, **changes):
        arguments = {
            "root": self.root,
            "operation_id": self.request["operation_id"],
            "expected_request_sha256": self.request["request_sha256"],
            "provider_result": "provider-result.json",
            **changes,
        }
        operation_store.reconcile_terminal_operation(**arguments)

    def select_draft(self):
        output = self.request["extensions"]["expected_output"]
        (self.root / output).write_bytes(b"synthetic draft output")
        digest = hashlib.sha256((self.root / output).read_bytes()).hexdigest()
        review = {
            "schema_version": 1, "artifact_path": output, "artifact_sha256": digest,
            "status": "pass", "inspection_method": "synthetic temporal inspection",
            "coverage": "entire fixture", "checks": [
                {"criterion": "fixture selection", "status": "pass", "evidence": "Synthetic fixture"}
            ],
            "observations": ["Test-only selection"], "limitations": ["No real media"],
            "recommendation": "Select fixture",
        }
        (self.root / "draft-review.json").write_text(json.dumps(review))
        decision = {
            "schema_version": 1, "decision_id": "draft-selection",
            "decision_type": "variant_selection", "asset_id": self.request["asset_id"],
            "subject_path": output, "selected_variant": Path(output).name,
            "selected_sha256": digest, "actor": "agent", "approval_mode": "approve_for_me",
            "project_sha256": hashlib.sha256((self.root / "project.md").read_bytes()).hexdigest(),
            "result": "approved", "review_path": "draft-review.json",
            "review_sha256": hashlib.sha256((self.root / "draft-review.json").read_bytes()).hexdigest(),
            "upstream_sha256": {}, "reason": "Synthetic selection",
            "decided_at": "2026-11-16T00:00:00Z",
        }
        (self.root / "decisions").mkdir(exist_ok=True)
        (self.root / "decisions/draft-selection.json").write_text(json.dumps(decision))
        self.assertEqual(fixtures.validation.decision_findings(self.root, decision), [])

    def promotion(self):
        capabilities = copy.deepcopy(fixtures.CAPABILITIES)
        capabilities["parameters"]["resolution"]["enum"].append("1080p")
        capabilities["parameters"]["draft_task_id"] = {"type": "string"}
        capabilities["required_parameters"] = ["resolution"]
        (self.root / "promotion-capabilities.json").write_text(json.dumps(capabilities))
        return self.fixture.run_cli(self.fixture.promotion_argv("job-123") + [
            "--capabilities", "promotion-capabilities.json",
        ])

    def test_terminal_adoption_requires_explicit_definitive_result_before_writes(self):
        for status in (None, "", " ", "completed", "unknown", "running", "submitted", "SUCCEEDED"):
            with self.subTest(status=status):
                before = {p.relative_to(self.root): p.read_bytes()
                          for p in self.root.rglob("*") if p.is_file()}
                code, result = self.fixture.run_cli(self.adopt_args(status))
                self.assertEqual(code, 1, result)
                self.assertIn("terminal", str(result).lower())
                self.assertEqual(
                    {p.relative_to(self.root): p.read_bytes()
                     for p in self.root.rglob("*") if p.is_file()}, before,
                )

    def test_invalid_adoption_cannot_replace_an_unregistered_receipt(self):
        self.fixture.run_cli(self.fixture.argv("--write"))
        before = self.receipt_path.read_bytes()
        (self.root / self.fixture.prompt).write_text("@Image 1 pauses near @Video 1 and @Image 2.\n")
        code, result = self.fixture.run_cli(self.adopt_args(None) + ["--replace-unregistered"])
        self.assertEqual(code, 1, result)
        self.assertEqual(self.receipt_path.read_bytes(), before)
        self.assertFalse(self.registry_path.exists())

    def test_direct_adoption_api_rejects_invalid_terminal_results_before_registration(self):
        for status in (None, "", " ", "completed", "unknown", "running", 1, [], {}):
            with self.subTest(status=status), self.assertRaises(ValueError):
                operation_store.adopt_submitted_operation(
                    self.root, self.request, fixtures.CAPABILITIES, None, [],
                    "job-123", status, True,
                )
            self.assertFalse(self.registry_path.exists())

    def test_terminal_adoption_rejects_blank_task_identity_before_writes(self):
        arguments = self.adopt_args("succeeded")
        arguments[arguments.index("job-123")] = " "
        code, result = self.fixture.run_cli(arguments)
        self.assertEqual(code, 1, result)
        self.assertFalse(self.receipt_path.exists())
        self.assertFalse(self.registry_path.exists())

    def test_successful_adoption_with_structured_selection_passes_full_promotion_validation(self):
        record = self.adopt("succeeded")
        self.assertEqual(record["provider_status"], "succeeded")
        self.assertEqual(record["review_status"], "not_started")
        self.select_draft()
        code, result = self.promotion()
        self.assertEqual(code, 0, result)
        self.assertEqual(result["findings"], [])

    def test_explicit_terminal_failures_are_recorded_truthfully_and_cannot_promote(self):
        self.select_draft()
        for status in TERMINAL_RESULTS[1:]:
            with self.subTest(status=status):
                record = self.adopt(status)
                self.assertEqual(record["provider_status"], status)
                self.assertEqual(record["review_status"], "not_started")
                code, result = self.promotion()
                self.assertEqual(code, 1, result)
                self.assertIn("seedance.draft_promotion_source", str(result))
                self.registry_path.unlink()

    def test_adopting_the_same_terminal_task_twice_does_not_duplicate_or_rewrite_it(self):
        self.adopt("succeeded")
        before = self.registry_path.read_bytes()
        code, result = self.fixture.run_cli(self.adopt_args("succeeded"))
        self.assertEqual(code, 1, result)
        self.assertIn("already exists", str(result))
        self.assertEqual(self.registry_path.read_bytes(), before)

    def test_historical_completed_correction_preserves_request_history_and_enables_selected_promotion(self):
        historical = self.historical()
        historical["extensions"]["existing_history"] = [{"event": "keep"}]
        document = json.loads(self.registry_path.read_text())
        document["tasks"][0] = historical
        self.registry_path.write_text(json.dumps(document))
        receipt = self.receipt_path.read_bytes()
        self.select_draft()
        self.assertEqual(self.promotion()[0], 1)
        self.reconcile()
        tasks = json.loads(self.registry_path.read_text())["tasks"]
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[1], document["tasks"][1])
        record = tasks[0]
        audit = record["extensions"].pop("terminal_reconciliation")
        self.assertEqual(record, {**historical, "provider_status": "succeeded"})
        self.assertEqual(audit["previous_provider_status"], "completed")
        self.assertEqual(audit["provider_status"], "succeeded")
        self.assertEqual(audit["provider_task_id"], "job-123")
        self.assertEqual(audit["request_sha256"], historical["request_sha256"])
        self.assertEqual(audit["evidence_path"], "provider-result.json")
        self.assertEqual(audit["evidence_sha256"], hashlib.sha256(self.evidence_path.read_bytes()).hexdigest())
        self.assertEqual(self.receipt_path.read_bytes(), receipt)
        code, result = self.promotion()
        self.assertEqual(code, 0, result)

    def test_historical_correction_records_failure_without_authorizing_promotion(self):
        self.historical()
        self.select_draft()
        self.evidence_path.write_text(json.dumps({"task_id": "job-123", "status": "failed"}))
        self.reconcile()
        self.assertEqual(json.loads(self.registry_path.read_text())["tasks"][0]["provider_status"], "failed")
        code, result = self.promotion()
        self.assertEqual(code, 1, result)
        self.assertIn("successful terminal", str(result))

    def test_v2_historical_correction_preserves_frozen_inputs_after_project_changes(self):
        self.fixture.record_selection()
        code, result = self.fixture.run_cli(self.fixture.v2_argv("--write"))
        self.assertEqual(code, 0, result)
        receipt = self.receipt_path.read_bytes()
        self.request = json.loads(receipt)
        self.assertEqual(self.request["schema_version"], 2)
        historical = {
            **self.request, "submission_status": "terminal",
            "provider_task_id": "job-123", "provider_status": "completed",
        }
        self.registry_path.write_text(json.dumps({"schema_version": 1, "tasks": [historical]}))
        (self.root / "project.md").write_text("# Subsequent project state\n")
        (self.root / self.fixture.prompt).write_text("A subsequently edited prompt.\n")
        self.reconcile()
        record = json.loads(self.registry_path.read_text())["tasks"][0]
        record["extensions"].pop("terminal_reconciliation")
        self.assertEqual(record, {**historical, "provider_status": "succeeded"})
        self.assertEqual(self.receipt_path.read_bytes(), receipt)

    def test_correction_does_not_invent_selection(self):
        self.historical()
        self.reconcile()
        code, result = self.promotion()
        self.assertEqual(code, 1, result)
        self.assertIn("no approved review or selection", str(result))

    def test_missing_invalid_ambiguous_or_mismatched_provider_evidence_preserves_history(self):
        self.historical()
        before = self.registry_path.read_bytes()
        for value in (
            None, [], {}, {"status": "succeeded"}, {"task_id": "job-123"},
            {"task_id": "other-job", "status": "succeeded"},
            *({"task_id": "job-123", "status": status}
              for status in (None, "", "completed", "unknown", "running", "SUCCEEDED", [], 1)),
        ):
            with self.subTest(value=value):
                self.evidence_path.write_text(json.dumps(value))
                with self.assertRaises((TypeError, ValueError)):
                    self.reconcile()
                self.assertEqual(self.registry_path.read_bytes(), before)
        self.evidence_path.write_text("{")
        with self.assertRaises(ValueError):
            self.reconcile()
        self.evidence_path.unlink()
        with self.assertRaises((OSError, ValueError)):
            self.reconcile()
        self.assertEqual(self.registry_path.read_bytes(), before)

    def test_evidence_path_must_stay_inside_project(self):
        self.historical()
        before = self.registry_path.read_bytes()
        outside = self.root.parent / "outside-result.json"
        outside.write_bytes(self.evidence_path.read_bytes())
        (self.root / "escaped-result.json").symlink_to(outside)
        for path in ("../outside-result.json", str(outside), "escaped-result.json", ""):
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.reconcile(provider_result=path)
            self.assertEqual(self.registry_path.read_bytes(), before)

    def test_correction_requires_matching_operation_request_and_completed_terminal_state(self):
        self.historical()
        baseline = json.loads(self.registry_path.read_text())
        for changes in (
            {"provider_status": "succeeded"}, {"provider_status": "failed"},
            {"provider_status": None}, {"provider_status": "unknown"},
            {"submission_status": "acknowledged"}, {"submission_status": "prepared"},
            {"provider_task_id": None}, {"provider_task_id": "other-job"},
        ):
            with self.subTest(changes=changes):
                document = copy.deepcopy(baseline)
                document["tasks"][0].update(changes)
                self.registry_path.write_text(json.dumps(document))
                before = self.registry_path.read_bytes()
                with self.assertRaises(ValueError):
                    self.reconcile()
                self.assertEqual(self.registry_path.read_bytes(), before)
        self.registry_path.write_text(json.dumps(baseline))
        before = self.registry_path.read_bytes()
        for changes in ({"operation_id": "missing"}, {"expected_request_sha256": "0" * 64}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.reconcile(**changes)
            self.assertEqual(self.registry_path.read_bytes(), before)

    def test_existing_correction_audit_is_never_overwritten(self):
        self.historical()
        document = json.loads(self.registry_path.read_text())
        document["tasks"][0]["extensions"]["terminal_reconciliation"] = {"original": "keep"}
        self.registry_path.write_text(json.dumps(document))
        before = self.registry_path.read_bytes()
        with self.assertRaises(ValueError):
            self.reconcile()
        self.assertEqual(self.registry_path.read_bytes(), before)

    def test_legacy_invalid_or_duplicate_registry_is_preserved(self):
        historical = self.historical()
        for document in (
            {"tasks": [{"task_id": "legacy-job"}]},
            {"schema_version": 1, "tasks": [historical, historical]},
            {"schema_version": 1, "tasks": []},
        ):
            with self.subTest(document=document):
                self.registry_path.write_text(json.dumps(document))
                before = self.registry_path.read_bytes()
                with self.assertRaises(ValueError):
                    self.reconcile()
                self.assertEqual(self.registry_path.read_bytes(), before)

    def test_competing_corrections_have_one_winner_and_preserve_the_result(self):
        self.historical()
        (self.root / "failed-result.json").write_text(json.dumps({"task_id": "job-123", "status": "failed"}))

        def attempt(path):
            try:
                self.reconcile(provider_result=path)
                return True
            except ValueError:
                return False

        with ThreadPoolExecutor(max_workers=2) as workers:
            outcomes = list(workers.map(attempt, ("provider-result.json", "failed-result.json")))
        self.assertEqual(sorted(outcomes), [False, True])
        record = json.loads(self.registry_path.read_text())["tasks"][0]
        self.assertIn(record["provider_status"], ("succeeded", "failed"))
        self.assertEqual(record["extensions"]["terminal_reconciliation"]["provider_status"], record["provider_status"])
        before = self.registry_path.read_bytes()
        with self.assertRaises(ValueError):
            self.reconcile()
        self.assertEqual(self.registry_path.read_bytes(), before)

    def test_correction_write_failure_preserves_registry_and_cleans_temporary_file(self):
        self.historical()
        before = self.registry_path.read_bytes()
        with (
            patch.object(operation_store.os, "replace", side_effect=OSError("injected failure")),
            self.assertRaises(OSError),
        ):
            self.reconcile()
        self.assertEqual(self.registry_path.read_bytes(), before)
        self.assertEqual(list(self.root.glob(".task_ids-*.tmp")), [])

    def test_correction_never_reopens_terminal_state_or_allows_readoption(self):
        self.historical()
        self.reconcile()
        before = self.registry_path.read_bytes()
        for state in ("prepared", "submitting", "acknowledged", "terminal"):
            with self.subTest(state=state), self.assertRaises(ValueError):
                operation_store.transition_operation(
                    self.root, self.request["operation_id"], "terminal", state,
                    provider_status="succeeded",
                )
        code, result = self.fixture.run_cli(self.adopt_args("succeeded"))
        self.assertEqual(code, 1, result)
        self.assertEqual(self.registry_path.read_bytes(), before)

    def test_reconciliation_cli_corrects_once_and_reports_conflict_without_changes(self):
        self.historical()
        command = [
            sys.executable, str(ROOT / ".agents/scripts/operation_store.py"),
            "reconcile-terminal", "--project", str(self.root),
            "--operation-id", self.request["operation_id"],
            "--expected-request-sha256", self.request["request_sha256"],
            "--provider-result", "provider-result.json",
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(json.loads(result.stdout)["ok"])
        before = self.registry_path.read_bytes()
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertFalse(json.loads(result.stdout)["ok"])
        self.assertEqual(self.registry_path.read_bytes(), before)

    def test_reconciliation_cli_missing_or_invalid_evidence_does_not_write(self):
        self.historical()
        before = self.registry_path.read_bytes()
        for content in (None, "{", "[]", '{"task_id":"job-123","status":"unknown"}'):
            with self.subTest(content=content):
                if content is None:
                    self.evidence_path.unlink()
                else:
                    self.evidence_path.write_text(content)
                result = subprocess.run([
                    sys.executable, str(ROOT / ".agents/scripts/operation_store.py"),
                    "reconcile-terminal", "--project", str(self.root),
                    "--operation-id", self.request["operation_id"],
                    "--expected-request-sha256", self.request["request_sha256"],
                    "--provider-result", "provider-result.json",
                ], capture_output=True, text=True, check=False)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertFalse(json.loads(result.stdout)["ok"])
                self.assertEqual(self.registry_path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
