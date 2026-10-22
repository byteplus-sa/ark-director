import copy
import json
import subprocess
import sys
import unittest

import test_prepare_request as preparation
import test_request_validation as validation_fixtures

operation_store = sys.modules["operation_store"]
validation = preparation.validation
MODEL = "dreamina-seedance-2-5-260628"


class NativeDraftTests(unittest.TestCase):
    def setUp(self):
        self.fixture = validation_fixtures.RequestValidationTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root
        self.request = self.fixture.request
        self.caps = self.fixture.caps
        self.request["model"] = self.caps["model"] = MODEL
        self.request["params"] = {"resolution": "480p", "draft": True}
        self.caps["parameters"] = {
            "resolution": {"enum": ["480p", "720p", "1080p", "4k"]},
            "draft": {"type": "boolean"},
        }
        self.fixture.rehash()

    def findings(self):
        self.fixture.rehash()
        return validation.validate_request(self.root, self.request, self.caps)

    def review(self):
        return {
            "schema_version": 1,
            "request_sha256": self.request["request_sha256"],
            "reviewer_status": "complete",
            "checks": [
                {
                    "rule_id": "seedance.draft_promotion",
                    "status": "pass",
                    "evidence": "Synthetic offline request review",
                }
            ],
        }

    def test_missing_false_and_non_boolean_draft_are_rejected(self):
        for value in ("missing", False, None, "true", "false", 1, 0, [], {}):
            with self.subTest(draft=value):
                self.request["params"] = {"resolution": "480p"}
                if value != "missing":
                    self.request["params"]["draft"] = value
                self.assertIn(
                    "seedance.draft_promotion",
                    {finding.rule_id for finding in self.findings()},
                )

    def test_missing_or_non_480p_resolution_is_rejected(self):
        for value in (None, "720p", "1080p", "4k", 480, "480P"):
            with self.subTest(resolution=value):
                self.request["params"] = {"draft": True}
                if value is not None:
                    self.request["params"]["resolution"] = value
                self.assertIn(
                    "seedance.draft_promotion",
                    {finding.rule_id for finding in self.findings()},
                )

    def test_native_draft_passes_without_mutation_in_all_existing_modes(self):
        self.request["references"] = []
        (self.root / "prompt.md").write_text("A ceramic cup turns on a shelf.\n")
        self.request["prompt_sha256"] = self.fixture.hash("prompt.md")
        for mode in ("approve_for_me", "ask_for_approval"):
            with self.subTest(mode=mode):
                self.request["params"]["draft"] = True
                (self.root / "project.md").write_text(
                    f"---\napproval_mode: {mode}\n---\n"
                )
                self.request.update(
                    schema_version=2,
                    approval_mode=mode,
                    project_sha256=self.fixture.hash("project.md"),
                )
                self.fixture.rehash()
                before = copy.deepcopy(self.request)
                self.assertEqual(self.findings(), [])
                self.assertEqual(self.request, before)
                del self.request["params"]["draft"]
                self.assertIn(
                    "seedance.draft_promotion",
                    {finding.rule_id for finding in self.findings()},
                )

    def test_edits_extensions_variations_and_premium_require_native_draft(self):
        for model in (MODEL, "dreamina-seedance-2-5-premium-260915"):
            for operation in ("generate", "edit", "extend", "generate_variations"):
                with self.subTest(model=model, operation=operation):
                    self.request["model"] = self.caps["model"] = model
                    self.request["operation"] = operation
                    self.caps["operations"] = [operation]
                    self.request["params"] = {"resolution": "480p", "draft": True}
                    self.assertEqual(self.findings(), [])
                    del self.request["params"]["draft"]
                    self.assertIn(
                        "seedance.draft_promotion",
                        {finding.rule_id for finding in self.findings()},
                    )

    def test_all_transports_require_the_same_native_draft(self):
        del self.request["params"]["draft"]
        for transport in ("ark-mcp", "arkcli", "curl"):
            with self.subTest(transport=transport):
                self.request["transport"] = transport
                self.assertIn(
                    "seedance.draft_promotion",
                    {finding.rule_id for finding in self.findings()},
                )

    def test_delivery_target_and_review_pass_do_not_authorize_plain_480p(self):
        self.request["extensions"] = {"delivery_resolution": "1080p"}
        del self.request["params"]["draft"]
        self.fixture.rehash()
        with self.assertRaisesRegex(ValueError, "draft"):
            operation_store.prepare_operation(
                self.root, self.request, self.caps, self.review(), []
            )
        self.assertFalse((self.root / "task_ids.json").exists())

    def test_schema_conflict_cannot_be_resolved_by_dropping_draft(self):
        del self.caps["parameters"]["draft"]
        findings = self.findings()
        self.assertIn("model.supported_mode", {item.rule_id for item in findings})
        self.assertTrue(any("transport" in item.message.lower() for item in findings))
        self.assertIs(self.request["params"]["draft"], True)
        del self.request["params"]["draft"]
        self.assertIn(
            "seedance.draft_promotion",
            {finding.rule_id for finding in self.findings()},
        )

    def test_other_models_accept_ordinary_480p_without_injected_draft(self):
        for model in ("dreamina-seedance-2-0-260128", "other-video-model"):
            with self.subTest(model=model):
                self.request["model"] = self.caps["model"] = model
                self.request["params"] = {"resolution": "480p"}
                self.assertEqual(self.findings(), [])
                self.assertNotIn("draft", self.request["params"])

    def test_empty_draft_task_id_does_not_bypass_native_draft(self):
        for value in ("", " ", None, False, 123):
            with self.subTest(task_id=value):
                self.request["params"] = {
                    "resolution": "480p",
                    "draft_task_id": value,
                }
                self.assertIn(
                    "seedance.draft_promotion",
                    {finding.rule_id for finding in self.findings()},
                )

    def test_creative_promotion_cannot_be_prepared_or_registered(self):
        self.fixture.promote()
        self.request["params"]["duration"] = 10
        self.caps["parameters"]["duration"] = {"type": "integer"}
        self.fixture.rehash()
        path = self.root / "task_ids.json"
        before = path.read_bytes()
        self.assertIn(
            "seedance.draft_promotion_source",
            {
                finding.rule_id
                for finding in validation.prepared_evidence_findings(
                    self.root, self.request
                )
            },
        )
        with self.assertRaisesRegex(ValueError, "creative inputs"):
            operation_store.prepare_operation(
                self.root, self.request, self.caps, self.review(), []
            )
        self.assertEqual(path.read_bytes(), before)

    def test_pending_creative_promotion_cannot_enter_submitting(self):
        self.fixture.promote()
        self.request["params"]["generate_audio"] = False
        self.fixture.rehash()
        path = self.root / "task_ids.json"
        registry = json.loads(path.read_text())
        registry["tasks"].append(self.request)
        path.write_text(json.dumps(registry))
        before = path.read_bytes()
        with self.assertRaisesRegex(ValueError, "creative inputs"):
            operation_store.transition_operation(
                self.root, self.request["operation_id"], "prepared", "submitting"
            )
        self.assertEqual(path.read_bytes(), before)

    def test_pending_plain_request_is_blocked_without_rewriting_history(self):
        self.request["params"] = {"resolution": "480p"}
        self.fixture.rehash()
        path = self.root / "task_ids.json"
        path.write_text(json.dumps({"schema_version": 1, "tasks": [self.request]}))
        before = path.read_bytes()
        self.assertEqual(operation_store.read_registry(path)["tasks"], [self.request])
        with self.assertRaisesRegex(ValueError, "draft"):
            operation_store.transition_operation(
                self.root, self.request["operation_id"], "prepared", "submitting"
            )
        self.assertEqual(path.read_bytes(), before)

    def test_existing_plain_submission_can_be_adopted_and_completed(self):
        self.request["params"] = {"resolution": "480p"}
        self.fixture.rehash()
        original = copy.deepcopy(self.request)
        operation_store.adopt_submitted_operation(
            self.root,
            self.request,
            self.caps,
            self.review(),
            [],
            "existing-provider-task",
            "running",
            False,
        )
        operation_store.transition_operation(
            self.root,
            self.request["operation_id"],
            "acknowledged",
            "terminal",
            provider_status="succeeded",
        )
        record = operation_store.read_registry(self.root / "task_ids.json")["tasks"][0]
        self.assertEqual(record["params"], original["params"])
        self.assertEqual(record["request_sha256"], original["request_sha256"])
        self.assertEqual(record["provider_task_id"], "existing-provider-task")
        self.assertEqual(record["submission_status"], "terminal")
        self.assertEqual(self.request, original)

    def test_legacy_hash_algorithm_is_unchanged(self):
        params = {"resolution": "480p"}
        digest = validation.compute_request_hash(
            b"legacy", [], MODEL, "generate", params
        )
        body = {
            "prompt_sha256": preparation.sha(b"legacy"),
            "model": MODEL,
            "operation": "generate",
            "params": params,
            "references": [],
        }
        self.assertEqual(
            digest,
            preparation.sha(
                json.dumps(
                    body,
                    sort_keys=True,
                    separators=(",", ":"),
                    ensure_ascii=False,
                    allow_nan=False,
                ).encode()
            ),
        )


class NativeDraftPreparationTests(unittest.TestCase):
    def setUp(self):
        self.fixture = preparation.PrepareRequestTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)

    def test_preparation_rejects_plain_480p_before_writing(self):
        argv = self.fixture.argv("--write")
        if "draft=true" in argv:
            index = argv.index("draft=true")
            del argv[index - 1 : index + 1]
        argv = [
            "resolution=480p" if value == "resolution=720p" else value for value in argv
        ]
        code, result = self.fixture.run_cli(argv)
        self.assertEqual(code, 1, result)
        self.assertIn(
            "seedance.draft_promotion",
            {finding["rule_id"] for finding in result["findings"]},
        )
        self.assertFalse((self.fixture.root / "requests").exists())
        self.assertFalse((self.fixture.root / "task_ids.json").exists())

    def test_cli_smoke_writes_native_draft_and_rejects_plain_480p(self):
        command = [
            sys.executable,
            str(preparation.ROOT / ".agents/scripts/prepare_request.py"),
            *self.fixture.argv("--write"),
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        document = json.loads(result.stdout)
        path = self.fixture.root / document["path"]
        request = json.loads(path.read_text())
        self.assertIs(request["params"]["draft"], True)
        self.assertEqual(request["params"]["resolution"], "480p")
        before = path.read_bytes()
        index = command.index("draft=true")
        del command[index - 1 : index + 1]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(
            "seedance.draft_promotion",
            {finding["rule_id"] for finding in json.loads(result.stdout)["findings"]},
        )
        self.assertEqual(path.read_bytes(), before)
        self.assertFalse((self.fixture.root / "task_ids.json").exists())


if __name__ == "__main__":
    unittest.main()
