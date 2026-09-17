import copy
import hashlib
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "request_validation", ROOT / ".agents/scripts/validate_request.py"
)
validation = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validation
SPEC.loader.exec_module(validation)


class RequestValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "prompt.md").write_text("A performer walks beside @Image 1.\n")
        (self.root / "image.png").write_bytes(b"fixture image")
        (self.root / "character.md").write_text(
            "---\nselected_variant: image.png\n---\nKeep this note.\n"
        )
        self.request = {
            "schema_version": 1,
            "operation_id": "fixture-operation",
            "asset_id": "fixture",
            "transport": "ark-mcp",
            "model": "fixture-model",
            "operation": "generate",
            "prompt_file": "prompt.md",
            "prompt_sha256": self.hash("prompt.md"),
            "request_sha256": "",
            "references": [
                {
                    "path": "image.png",
                    "sha256": self.hash("image.png"),
                    "role": "reference_image",
                    "binding": "@Image 1",
                    "approval_evidence": {
                        "manifest": "character.md",
                        "field": "selected_variant",
                    },
                }
            ],
            "params": {"duration": 5, "resolution": "720p"},
            "submission_status": "prepared",
            "provider_task_id": None,
            "provider_status": None,
            "review_status": "not_started",
            "cost": {"estimated": None, "confirmed": None, "currency": "USD"},
        }
        self.caps = {
            "model": "fixture-model",
            "source": "fixture tool schema",
            "verified_at": "2026-09-08T00:00:00Z",
            "operations": ["generate"],
            "parameters": {
                "duration": {"minimum": 4, "maximum": 15},
                "resolution": {"enum": ["720p", "1080p"]},
            },
            "reference_roles": ["reference_image", "first_frame"],
            "max_references": 3,
            "supports_first_frame_with_reference_images": False,
        }
        self.rehash()

    def hash(self, name):
        return hashlib.sha256((self.root / name).read_bytes()).hexdigest()

    def rehash(self):
        self.request["request_sha256"] = validation.compute_request_hash(
            (self.root / "prompt.md").read_bytes(),
            self.request["references"],
            self.request["model"],
            self.request["operation"],
            self.request["params"],
        )

    def findings(self):
        return validation.validate_request(self.root, self.request, self.caps)

    def test_valid_request_passes_without_mutation(self):
        before = copy.deepcopy(self.request)
        self.assertEqual(self.findings(), [])
        self.assertEqual(self.request, before)

    def test_changed_reference_and_prompt_are_rejected(self):
        (self.root / "image.png").write_bytes(b"changed")
        (self.root / "prompt.md").write_text("changed prompt")
        self.assertIn("references.current_hashes", {f.rule_id for f in self.findings()})
        self.assertIn("prompt.current_hash", {f.rule_id for f in self.findings()})

    def test_automatic_selection_cannot_authorize_reference(self):
        (self.root / "character.md").write_text(
            "---\nrecommended_variant: image.png\nselected_variant: auto\n---\n"
        )
        self.assertIn("approval.explicit_choice", {f.rule_id for f in self.findings()})

    def test_path_traversal_and_symlink_are_rejected(self):
        self.request["references"][0]["path"] = "../outside.png"
        self.assertTrue(self.findings())
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "image.png"
            target.write_bytes(b"outside")
            (self.root / "escape.png").symlink_to(target)
            self.request["references"][0]["path"] = "escape.png"
            self.assertIn("path.containment", {f.rule_id for f in self.findings()})

    def test_unsupported_parameter_and_model_fail(self):
        self.request["params"]["resolution"] = "4K"
        self.rehash()
        self.assertIn("model.supported_mode", {f.rule_id for f in self.findings()})
        self.request["model"] = "another-model"
        self.rehash()
        self.assertTrue(self.findings())

    def test_unknown_parameter_fails_closed(self):
        self.request["params"]["unverified"] = True
        self.rehash()
        self.assertTrue(self.findings())

    def test_control_reference_and_unbound_reference_fail(self):
        self.request["references"][0]["control_only"] = True
        self.assertIn("references.control_only", {f.rule_id for f in self.findings()})
        self.request["references"][0]["binding"] = "@Image 2"
        self.assertIn(
            "references.ordered_bindings", {f.rule_id for f in self.findings()}
        )

    def test_known_task_is_not_eligible_for_new_submission(self):
        self.request["submission_status"] = "acknowledged"
        self.request["provider_task_id"] = "existing"
        self.assertIn(
            "submission.reconcile_unknown", {f.rule_id for f in self.findings()}
        )

    def test_invalid_types_report_findings_not_exceptions(self):
        for value in [None, [], {}, {"schema_version": 1, "references": "bad"}]:
            with self.subTest(value=value):
                self.assertTrue(
                    validation.validate_request(self.root, value, self.caps)
                )

    def test_malformed_capability_evidence_and_external_schema_refs_fail(self):
        for bad in [
            None,
            [],
            {},
            dict(self.caps, operations=None),
            dict(self.caps, reference_roles="image"),
        ]:
            with self.subTest(evidence=bad):
                self.assertTrue(
                    validation.validate_request(self.root, self.request, bad)
                )
        self.caps["parameters"]["duration"] = {
            "$ref": "https://invalid.example/schema.json"
        }
        self.assertTrue(self.findings())

    def test_reference_order_affects_hash(self):
        other = dict(self.request["references"][0], binding="@Image 2")
        first = validation.compute_request_hash(
            b"p", [self.request["references"][0], other], "m", "generate", {}
        )
        second = validation.compute_request_hash(
            b"p", [other, self.request["references"][0]], "m", "generate", {}
        )
        self.assertNotEqual(first, second)

    def test_review_rejects_missing_checks_stale_hash_and_incomplete_reviewer(self):
        review = {
            "schema_version": 1,
            "request_sha256": "a" * 64,
            "reviewer_status": "complete",
            "checks": [
                {
                    "rule_id": "asset.visible_consistency",
                    "status": "pass",
                    "evidence": "Inspected the asset.",
                }
            ],
        }
        self.assertEqual(
            validation.validate_review(review, "a" * 64, ["asset.visible_consistency"]),
            [],
        )
        self.assertTrue(
            validation.validate_review(review, "b" * 64, ["asset.visible_consistency"])
        )
        self.assertTrue(
            validation.validate_review(review, "a" * 64, ["approval.explicit_choice"])
        )
        review["reviewer_status"] = "incomplete"
        self.assertTrue(
            validation.validate_review(review, "a" * 64, ["asset.visible_consistency"])
        )

    def test_recovery_never_resubmits(self):
        self.assertEqual(
            validation.reconcile_operation(
                {"submission_status": "submission_unknown"}, {}
            ).action,
            "hold",
        )
        self.assertEqual(
            validation.reconcile_operation({"provider_task_id": "existing"}, {}).action,
            "poll",
        )
        self.assertEqual(
            validation.reconcile_operation(
                {"provider_task_id": "existing"}, {"provider_status": "succeeded"}
            ).action,
            "download",
        )
        self.assertEqual(
            validation.reconcile_operation({}, {"provider_status": "failed"}).action,
            "review_failure",
        )


if __name__ == "__main__":
    unittest.main()
