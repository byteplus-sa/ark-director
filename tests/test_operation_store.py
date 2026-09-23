import json
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

import test_request_validation as fixtures

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".agents/scripts"))
import operation_store


class OperationStoreTests(unittest.TestCase):
    def setUp(self):
        fixture = fixtures.RequestValidationTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.root, self.request, self.caps = fixture.root, fixture.request, fixture.caps
        self.review = {
            "schema_version": 1,
            "request_sha256": self.request["request_sha256"],
            "reviewer_status": "complete",
            "checks": [
                {
                    "rule_id": "asset.visible_consistency",
                    "status": "pass",
                    "evidence": "Fixture inspected",
                }
            ],
        }

    def prepare(self):
        return operation_store.prepare_operation(
            self.root,
            self.request,
            self.caps,
            self.review,
            ["asset.visible_consistency"],
        )

    def test_prepared_operation_is_durable_and_unique(self):
        self.prepare()
        self.assertEqual(
            json.loads((self.root / "task_ids.json").read_text())["tasks"][0],
            self.request,
        )
        with self.assertRaises(ValueError):
            self.prepare()
        self.assertEqual(
            len(json.loads((self.root / "task_ids.json").read_text())["tasks"]), 1
        )

    def test_invalid_preflight_never_creates_registry(self):
        self.request["references"][0]["sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            self.prepare()
        self.assertFalse((self.root / "task_ids.json").exists())

    def test_versioned_canvas_rejects_new_or_pending_version_one_operation(self):
        canvas = {"canvas": {"approvalContractVersion": 1}}
        (self.root / "showcase.json").write_text(json.dumps(canvas))
        with self.assertRaisesRegex(ValueError, "version-2 generation request"):
            self.prepare()
        self.assertFalse((self.root / "task_ids.json").exists())
        (self.root / "showcase.json").unlink()
        self.prepare()
        (self.root / "showcase.json").write_text(json.dumps(canvas))
        with self.assertRaisesRegex(ValueError, "version-2 generation request"):
            operation_store.transition_operation(
                self.root, "fixture-operation", "prepared", "submitting"
            )

    def test_unknown_outcome_cannot_return_to_prepared(self):
        self.prepare()
        operation_store.transition_operation(
            self.root, "fixture-operation", "prepared", "submitting"
        )
        operation_store.transition_operation(
            self.root, "fixture-operation", "submitting", "submission_unknown"
        )
        with self.assertRaises(ValueError):
            operation_store.transition_operation(
                self.root, "fixture-operation", "submission_unknown", "prepared"
            )
        operation_store.transition_operation(
            self.root,
            "fixture-operation",
            "submission_unknown",
            "acknowledged",
            provider_task_id="provider-1",
        )
        data = json.loads((self.root / "task_ids.json").read_text())["tasks"][0]
        self.assertEqual(data["provider_task_id"], "provider-1")
        self.assertEqual(data["review_status"], "not_started")

    def test_concurrent_duplicate_prepare_has_one_winner(self):
        def attempt():
            try:
                self.prepare()
                return True
            except ValueError:
                return False

        with ThreadPoolExecutor(max_workers=2) as workers:
            outcomes = list(workers.map(lambda _: attempt(), range(2)))
        self.assertEqual(sorted(outcomes), [False, True])
        self.assertEqual(
            len(json.loads((self.root / "task_ids.json").read_text())["tasks"]), 1
        )

    def test_failed_atomic_write_preserves_existing_registry(self):
        self.prepare()
        before = (self.root / "task_ids.json").read_bytes()
        with (
            patch.object(
                operation_store.os,
                "replace",
                side_effect=OSError("injected write failure"),
            ),
            self.assertRaises(OSError),
        ):
            operation_store.transition_operation(
                self.root, "fixture-operation", "prepared", "submitting"
            )
        self.assertEqual((self.root / "task_ids.json").read_bytes(), before)
        self.assertEqual(list(self.root.glob(".task_ids-*.tmp")), [])

    def test_stale_transition_and_legacy_registry_are_preserved(self):
        self.prepare()
        before = (self.root / "task_ids.json").read_bytes()
        with self.assertRaises(ValueError):
            operation_store.transition_operation(
                self.root, "fixture-operation", "submitting", "submission_unknown"
            )
        self.assertEqual((self.root / "task_ids.json").read_bytes(), before)
        legacy = {"tasks": [{"task_id": "keep-existing"}]}
        (self.root / "task_ids.json").write_text(json.dumps(legacy))
        with self.assertRaises(ValueError):
            self.prepare()
        self.assertEqual(json.loads((self.root / "task_ids.json").read_text()), legacy)

    def test_v2_operation_preparation_and_submission_recheck_project_mode(self):
        fixture = fixtures.RequestValidationTests()
        fixture.root, fixture.request = self.root, self.request
        fixture.prepare_v2()
        self.review["request_sha256"] = self.request["request_sha256"]
        self.prepare()
        record = json.loads((self.root / "task_ids.json").read_text())["tasks"][0]
        self.assertEqual(record["schema_version"], 2)
        (self.root / "project.md").write_text(
            "---\napproval_mode: ask_for_approval\n---\n"
        )
        with self.assertRaisesRegex(ValueError, "approval mode or project.md changed"):
            operation_store.transition_operation(
                self.root, "fixture-operation", "prepared", "submitting"
            )
        self.assertEqual(
            json.loads((self.root / "task_ids.json").read_text())["tasks"][0][
                "submission_status"
            ],
            "prepared",
        )

    def test_v2_stale_project_blocks_preparation_without_writing_registry(self):
        fixture = fixtures.RequestValidationTests()
        fixture.root, fixture.request = self.root, self.request
        fixture.prepare_v2()
        self.review["request_sha256"] = self.request["request_sha256"]
        (self.root / "project.md").write_text(
            "---\napproval_mode: ask_for_approval\n---\n"
        )
        with self.assertRaises(ValueError):
            self.prepare()
        self.assertFalse((self.root / "task_ids.json").exists())

    def test_v2_changed_selection_after_prepare_blocks_submission(self):
        fixture = fixtures.RequestValidationTests()
        fixture.root, fixture.request = self.root, self.request
        fixture.prepare_v2()
        self.review["request_sha256"] = self.request["request_sha256"]
        self.prepare()
        (self.root / "image.png").write_bytes(b"changed after preparation")
        with self.assertRaisesRegex(ValueError, "Reference content changed"):
            operation_store.transition_operation(
                self.root, "fixture-operation", "prepared", "submitting"
            )
        self.assertEqual(
            json.loads((self.root / "task_ids.json").read_text())["tasks"][0][
                "submission_status"
            ],
            "prepared",
        )


if __name__ == "__main__":
    unittest.main()
