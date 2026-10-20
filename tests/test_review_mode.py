from __future__ import annotations

import contextlib
import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import test_request_validation as fixtures

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".agents/scripts"))
import operation_store
import validate_request as validation


class ReviewModeTests(unittest.TestCase):
    def setUp(self):
        fixture = fixtures.RequestValidationTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.fixture = fixture
        self.root, self.request, self.caps = fixture.root, fixture.request, fixture.caps
        self.review = {
            "schema_version": 1,
            "request_sha256": self.request["request_sha256"],
            "reviewer_status": "complete",
            "checks": [
                {
                    "rule_id": "references.ordered_bindings",
                    "status": "pass",
                    "evidence": "Fixture bindings match.",
                }
            ],
        }

    def set_mode(self, value, approval="approve_for_me"):
        (self.root / "project.md").write_text(
            f"---\napproval_mode: {approval}\nreview_mode: {value}\n---\n"
        )

    def make_v2(self, value="default", approval="approve_for_me"):
        self.fixture.prepare_v2()
        self.set_mode(value, approval)
        self.request["approval_mode"] = approval
        self.request["project_sha256"] = self.fixture.hash("project.md")
        self.fixture.rehash()
        self.review["request_sha256"] = self.request["request_sha256"]
        (self.root / "studio").mkdir()

    def prepare(self, review=None, rules=None):
        operation_store.prepare_operation(
            self.root, self.request, self.caps, review, rules or []
        )

    def test_absent_mode_registers_without_fabricating_review(self):
        before = copy.deepcopy(self.request)
        self.prepare()
        registry = json.loads((self.root / "task_ids.json").read_text())
        self.assertEqual(registry["tasks"], [before])
        self.assertEqual(self.request, before)
        self.assertEqual(list(self.root.glob("*review*")), [])
        self.assertEqual(registry["tasks"][0]["review_status"], "not_started")

    def test_default_is_independent_of_approval_mode(self):
        self.make_v2(approval="ask_for_approval")
        self.prepare()
        self.assertEqual(self.request["approval_mode"], "ask_for_approval")
        self.assertEqual(
            validation.decision_findings(
                self.root,
                json.loads((self.root / "decisions/choice-1.json").read_text()),
            ),
            [],
        )

    def test_strict_requires_report_but_accepts_real_matching_report(self):
        self.make_v2("strict")
        with self.assertRaisesRegex(ValueError, "review is required"):
            self.prepare()
        self.assertFalse((self.root / "task_ids.json").exists())
        self.prepare(self.review)

    def test_invalid_modes_fail_closed_even_with_report(self):
        for value in ('""', "null", "true", "[]", "{}", "fast", "DEFAULT"):
            with self.subTest(value=value):
                self.set_mode(value)
                with self.assertRaisesRegex(ValueError, "Invalid project review mode"):
                    self.prepare(self.review)
                self.assertFalse((self.root / "task_ids.json").exists())

    def test_required_rule_requires_real_applicable_matching_review(self):
        rules = ["references.ordered_bindings"]
        with self.assertRaisesRegex(ValueError, "review is required"):
            self.prepare(rules=rules)
        for change in (
            {"checks": []},
            {"request_sha256": "0" * 64},
            {"reviewer_status": "incomplete"},
            {"checks": [dict(self.review["checks"][0], status="not_applicable")]},
        ):
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.prepare(dict(self.review, **change), rules)
        self.assertFalse((self.root / "task_ids.json").exists())
        self.prepare(self.review, rules)

    def test_default_never_ignores_provided_failed_stale_or_malformed_review(self):
        for review in (
            dict(self.review, checks=[dict(self.review["checks"][0], status="fail")]),
            dict(self.review, request_sha256="0" * 64),
            dict(self.review, reviewer_status="incomplete"),
            {},
        ):
            with self.subTest(review=review), self.assertRaises(ValueError):
                self.prepare(review)
        self.assertFalse((self.root / "task_ids.json").exists())

    def test_mode_change_after_preparation_blocks_submission_without_mutation(self):
        self.make_v2()
        self.prepare()
        before = (self.root / "task_ids.json").read_bytes()
        self.set_mode("strict")
        with self.assertRaisesRegex(ValueError, "project.md changed"):
            operation_store.transition_operation(
                self.root, self.request["operation_id"], "prepared", "submitting"
            )
        self.assertEqual((self.root / "task_ids.json").read_bytes(), before)

    def test_explicit_review_mode_rejects_unbound_v1_preflight_and_contract(self):
        for mode in ("default", "strict"):
            with self.subTest(mode=mode):
                (self.root / "project.md").write_text(
                    f"---\nreview_mode: {mode}\n---\n"
                )
                findings = validation.project_mode_findings(self.root, self.request)
                self.assertTrue(findings)
                self.assertIn("version-2", findings[0].message)
                with self.assertRaisesRegex(ValueError, "version-2"):
                    operation_store.require_current_approval_contract(
                        self.root, self.request
                    )

    def test_adding_review_mode_to_prepared_v1_blocks_transition(self):
        self.prepare()
        before = (self.root / "task_ids.json").read_bytes()
        for mode in ("default", "strict"):
            with self.subTest(mode=mode):
                (self.root / "project.md").write_text(
                    f"---\nreview_mode: {mode}\n---\n"
                )
                with self.assertRaisesRegex(ValueError, "version-2"):
                    operation_store.transition_operation(
                        self.root,
                        self.request["operation_id"],
                        "prepared",
                        "submitting",
                    )
                self.assertEqual((self.root / "task_ids.json").read_bytes(), before)

    def test_mode_change_while_waiting_for_lock_blocks_registration(self):
        original_lock = operation_store.registry_lock

        @contextlib.contextmanager
        def changed_lock(root):
            with original_lock(root) as path:
                (root / "project.md").write_text("---\nreview_mode: strict\n---\n")
                yield path

        with (
            patch.object(operation_store, "registry_lock", changed_lock),
            self.assertRaisesRegex(ValueError, "review is required"),
        ):
            self.prepare()
        self.assertFalse((self.root / "task_ids.json").exists())

    def test_unreadable_or_malformed_project_mode_fails_closed(self):
        for content in ("---\nreview_mode: [\n---\n", "---\n[]\n---\n", "---\nbroken"):
            (self.root / "project.md").write_text(content)
            with self.subTest(content=content), self.assertRaises(ValueError):
                self.prepare()
        (self.root / "project.md").unlink()
        (self.root / "project.md").symlink_to(self.root.parent / "missing-project.md")
        with self.assertRaises(ValueError):
            self.prepare()

    def run_validator(self, *extra):
        (self.root / "request.json").write_text(json.dumps(self.request))
        (self.root / "capabilities.json").write_text(json.dumps(self.caps))
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / ".agents/scripts/validate_request.py"),
                "--project",
                str(self.root),
                "--request",
                str(self.root / "request.json"),
                "--capabilities",
                str(self.root / "capabilities.json"),
                *extra,
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode, json.loads(result.stdout)

    def test_validator_cli_default_and_strict_without_report(self):
        code, result = self.run_validator()
        self.assertEqual(code, 0, result)
        self.make_v2("strict")
        code, result = self.run_validator()
        self.assertEqual(code, 1, result)
        self.assertIn("review.complete_evidence", str(result))

    def test_validator_cli_required_rules_and_invalid_mode_fail(self):
        code, result = self.run_validator(
            "--required-rule", "references.ordered_bindings"
        )
        self.assertEqual(code, 1, result)
        self.set_mode("null")
        code, result = self.run_validator()
        self.assertEqual(code, 1, result)
        self.assertIn("Invalid project review mode", str(result))

    def run_prepare(self, mode="default", *extra, review_mode_only=False):
        self.set_mode(mode)
        if review_mode_only:
            (self.root / "project.md").write_text(f"---\nreview_mode: {mode}\n---\n")
        (self.root / "studio").mkdir()
        (self.root / "prompt.md").write_text("A quiet landscape.\n")
        (self.root / "capabilities.json").write_text(json.dumps(self.caps))
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / ".agents/scripts/prepare_request.py"),
                "--project",
                str(self.root),
                "--asset",
                "landscape",
                "--prompt",
                "prompt.md",
                "--model",
                "fixture-model",
                "--operation",
                "generate",
                "--expected-output",
                "landscape.png",
                "--write",
                "--register",
                "--capabilities",
                "capabilities.json",
                *extra,
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode, json.loads(result.stdout)

    def test_prepare_cli_default_registers_without_report(self):
        code, result = self.run_prepare()
        self.assertEqual(code, 0, result)
        record = json.loads((self.root / "task_ids.json").read_text())["tasks"][0]
        self.assertEqual(record["schema_version"], 2)
        self.assertEqual(record["review_status"], "not_started")
        self.assertFalse((self.root / "reviews").exists())

    def test_review_mode_only_project_registers_v2_and_binds_mode_changes(self):
        code, result = self.run_prepare(review_mode_only=True)
        self.assertEqual(code, 0, result)
        before = (self.root / "task_ids.json").read_bytes()
        record = json.loads(before)["tasks"][0]
        self.assertEqual(record["schema_version"], 2)
        self.assertEqual(record["approval_mode"], "approve_for_me")
        self.assertEqual(record["project_sha256"], self.fixture.hash("project.md"))
        (self.root / "project.md").write_text("---\nreview_mode: strict\n---\n")
        with self.assertRaisesRegex(ValueError, "project.md changed"):
            operation_store.transition_operation(
                self.root, record["operation_id"], "prepared", "submitting"
            )
        self.assertEqual((self.root / "task_ids.json").read_bytes(), before)

    def test_prepare_cli_strict_without_report_writes_nothing(self):
        code, result = self.run_prepare("strict")
        self.assertEqual(code, 1, result)
        self.assertIn("review.complete_evidence", str(result))
        self.assertFalse((self.root / "requests").exists())
        self.assertFalse((self.root / "task_ids.json").exists())

    def test_prepare_cli_null_report_is_not_treated_as_absent(self):
        (self.root / "null-review.json").write_text("null")
        code, result = self.run_prepare("default", "--review", "null-review.json")
        self.assertEqual(code, 1, result)
        self.assertFalse((self.root / "requests").exists())
        self.assertFalse((self.root / "task_ids.json").exists())

    def test_validator_cli_never_ignores_supplied_invalid_report(self):
        for review in (
            None,
            dict(self.review, request_sha256="0" * 64),
            dict(self.review, checks=[dict(self.review["checks"][0], status="fail")]),
        ):
            with self.subTest(review=review):
                path = self.root / "supplied-review.json"
                path.write_text(json.dumps(review))
                code, result = self.run_validator("--review", str(path))
                self.assertEqual(code, 1, result)


if __name__ == "__main__":
    unittest.main()
