import copy
import hashlib
import json
import subprocess
import sys
import unittest
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import test_prepare_request as preparation
import test_request_validation as fixtures

validation = preparation.validation
store = sys.modules["operation_store"]
MODEL = "dreamina-seedance-2-5-flash-261115"


def profile(native=False):
    now = datetime.now(UTC)
    return {
        "schema_version": 2,
        "profile_id": "synthetic-offline-profile",
        "provider": "fixture-provider",
        "model": MODEL,
        "operation": "generate",
        "transport": "ark-mcp",
        "tool_schema_revision": "fixture-revision-1",
        "source": "Synthetic test schema, not live provider verification",
        "verified_at": (now - timedelta(hours=1)).isoformat(),
        "valid_from": (now - timedelta(hours=1)).isoformat(),
        "valid_until": (now + timedelta(hours=1)).isoformat(),
        "operations": ["generate"],
        "parameters": {
            "duration": {"type": "number", "minimum": 2, "maximum": 30},
            "resolution": {"enum": ["480p", "720p", "1080p"]},
            "draft": {"type": "boolean"},
            "draft_task_id": {"type": "string", "minLength": 1},
        },
        "reference_roles": ["reference_image", "reference_video", "reference_audio"],
        "max_references": 5,
        "per_modality_limits": {"image": 2, "video": 1, "audio": 1},
        "supports_first_frame_with_reference_images": False,
        "conditional_parameters": [
            {"if": {"properties": {"draft": {"const": True}}, "required": ["draft"]},
             "then": {"properties": {"resolution": {"const": "480p"}}}}
        ],
        "preview": {
            "native_draft": native,
            "promotion": native,
            "parameters": {"resolution": "480p", **({"draft": True} if native else {})},
        },
    }


class CapabilityProfileTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.RequestValidationTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root
        self.request = self.fixture.request
        self.request["model"] = MODEL
        self.request["params"] = {"duration": 5.125, "resolution": "480p"}
        self.evidence = profile()
        self.bind()

    def bind(self):
        self.request["extensions"] = {
            "capability_profile": {
                "expected": {"provider": "fixture-provider",
                             "tool_schema_revision": "fixture-revision-1"},
                "evidence": copy.deepcopy(self.evidence),
                "sha256": hashlib.sha256(json.dumps(
                    self.evidence, sort_keys=True, separators=(",", ":"),
                    ensure_ascii=False, allow_nan=False,
                ).encode()).hexdigest(),
            }
        }
        self.request["request_sha256"] = validation.compute_request_hash(
            (self.root / "prompt.md").read_bytes(), self.request["references"],
            self.request["model"], self.request["operation"], self.request["params"],
            capability_profile=self.request["extensions"]["capability_profile"],
        )

    def findings(self):
        return validation.validate_request(self.root, self.request, self.evidence)

    def test_verified_non_native_preview_passes_without_mutation(self):
        before = copy.deepcopy(self.request)
        self.assertEqual(self.findings(), [])
        self.assertEqual(self.request, before)
        self.assertNotIn("draft", self.request["params"])

    def test_verified_native_requires_its_preview_controls(self):
        self.evidence = profile(True)
        self.bind()
        self.assertTrue(self.findings())
        self.request["params"]["draft"] = True
        self.bind()
        self.assertEqual(self.findings(), [])

    def test_identity_expectations_are_not_copied_from_evidence(self):
        for field, wrong in (("provider", "wrong-provider"),
                             ("tool_schema_revision", "wrong-revision"),
                             ("transport", "curl"), ("model", "other-model"),
                             ("operation", "edit")):
            with self.subTest(field=field):
                self.evidence = profile()
                self.evidence[field] = wrong
                self.bind()
                self.assertTrue(self.findings())

    def test_missing_empty_and_unknown_preview_evidence_blocks(self):
        for value in (None, {}, {"native_draft": None, "promotion": None,
                               "parameters": {}}):
            with self.subTest(value=value):
                self.evidence = profile()
                self.evidence["preview"] = value
                self.bind()
                self.assertTrue(self.findings())

    def test_new_seedance_without_profile_blocks_prepared_transition(self):
        self.request.pop("extensions")
        self.fixture.rehash()
        self.assertTrue(validation.prepared_evidence_findings(self.root, self.request))
        path = self.root / "task_ids.json"
        path.write_text(json.dumps({"schema_version": 1, "tasks": [self.request]}))
        before = path.read_bytes()
        with self.assertRaises(ValueError):
            store.transition_operation(self.root, self.request["operation_id"],
                                       "prepared", "submitting")
        self.assertEqual(path.read_bytes(), before)

    def test_expired_future_and_invalid_dates_block(self):
        for field, value in (
            ("valid_until", (datetime.now(UTC) - timedelta(seconds=1)).isoformat()),
            ("valid_from", (datetime.now(UTC) + timedelta(hours=2)).isoformat()),
            ("valid_until", "not-a-date"),
            ("verified_at", (datetime.now(UTC) + timedelta(hours=2)).isoformat()),
        ):
            with self.subTest(field=field):
                self.evidence = profile()
                self.evidence[field] = value
                self.bind()
                self.assertTrue(self.findings())

    def test_remote_or_malformed_conditional_schema_is_refused(self):
        for schema in ({"$ref": "https://invalid.example/schema.json"},
                       {"type": "not-a-type"}):
            with self.subTest(schema=schema):
                self.evidence = profile()
                self.evidence["conditional_parameters"] = [schema]
                self.bind()
                self.assertTrue(self.findings())

    def test_unresolvable_local_schema_reference_returns_findings(self):
        self.evidence["parameters"]["duration"] = {"$ref": "#missing"}
        self.bind()
        self.assertTrue(self.findings())

    def test_per_modality_overflow_and_unknown_allowance_block(self):
        for limit in (0, None):
            with self.subTest(limit=limit):
                self.evidence["per_modality_limits"]["image"] = limit
                self.bind()
                self.assertTrue(self.findings())

    def test_conditional_parameter_failure_is_not_mutated(self):
        self.evidence = profile(True)
        self.request["params"] = {"draft": True, "resolution": "1080p"}
        self.bind()
        before = copy.deepcopy(self.request)
        self.assertTrue(self.findings())
        self.assertEqual(self.request, before)

    def test_digest_and_binding_tampering_blocks_submission_without_registry_write(self):
        for target in ("evidence", "expected", "sha256"):
            with self.subTest(target=target):
                self.evidence = profile()
                self.bind()
                bound = self.request["extensions"]["capability_profile"]
                if target == "evidence":
                    bound["evidence"]["preview"]["parameters"] = {}
                elif target == "expected":
                    bound["expected"]["provider"] = "wrong-provider"
                else:
                    bound["sha256"] = "0" * 64
                path = self.root / "task_ids.json"
                path.write_text(json.dumps({"schema_version": 1, "tasks": [self.request]}))
                before = path.read_bytes()
                with self.assertRaises(ValueError):
                    store.transition_operation(self.root, self.request["operation_id"],
                                               "prepared", "submitting")
                self.assertEqual(path.read_bytes(), before)

    def test_valid_profile_can_register_and_enter_submitting(self):
        store.prepare_operation(self.root, self.request, self.evidence, None, [])
        store.transition_operation(self.root, self.request["operation_id"],
                                   "prepared", "submitting")
        record = store.read_registry(self.root / "task_ids.json")["tasks"][0]
        self.assertEqual(record["submission_status"], "submitting")
        self.assertEqual(record["extensions"], self.request["extensions"])

    def test_changed_external_evidence_is_refused(self):
        external = copy.deepcopy(self.evidence)
        external["source"] = "changed schema"
        self.assertTrue(validation.validate_request(self.root, self.request, external))

    def promotion(self):
        self.evidence = profile(True)
        self.request["params"] = {"duration": 5.125, "resolution": "480p", "draft": True}
        self.bind()
        draft = copy.deepcopy(self.request)
        draft.update(operation_id="selected-draft", asset_id="selected-draft",
                     submission_status="terminal", provider_status="succeeded",
                     provider_task_id="native-task", review_status="approved")
        (self.root / "task_ids.json").write_text(json.dumps(
            {"schema_version": 1, "tasks": [draft]}))
        self.request["params"] = {"draft_task_id": "native-task", "resolution": "1080p"}
        self.request["references"] = []
        self.bind()
        return draft

    def test_profile_native_promotion_passes_with_exact_selected_successful_source(self):
        self.promotion()
        self.assertEqual(self.findings(), [])

    def test_promotion_rejects_changed_source_hash_and_stale_inherited_reference(self):
        for change in ("params", "reference"):
            with self.subTest(change=change):
                draft = self.promotion()
                if change == "params":
                    draft["params"]["duration"] = 6
                else:
                    (self.root / "image.png").write_bytes(b"changed image")
                (self.root / "task_ids.json").write_text(json.dumps(
                    {"schema_version": 1, "tasks": [draft]}))
                self.assertTrue(self.findings())
                (self.root / "image.png").write_bytes(b"fixture image")

    def test_promotion_rejects_nonterminal_unselected_transport_and_profile_changes(self):
        for field, value in (("submission_status", "acknowledged"),
                             ("review_status", "not_started"),
                             ("provider_status", "failed"), ("transport", "curl")):
            with self.subTest(field=field):
                draft = self.promotion()
                draft[field] = value
                (self.root / "task_ids.json").write_text(json.dumps(
                    {"schema_version": 1, "tasks": [draft]}))
                self.assertTrue(self.findings())
        self.promotion()
        self.evidence["profile_id"] = "different-profile"
        self.bind()
        self.assertTrue(self.findings())

    def test_expiry_after_registration_blocks_submitting_without_writes(self):
        store.prepare_operation(self.root, self.request, self.evidence, None, [])
        path = self.root / "task_ids.json"
        before = path.read_bytes()
        with patch.object(validation, "datetime", wraps=datetime) as clock:
            clock.now.return_value = datetime.now(UTC) + timedelta(hours=2)
            with self.assertRaises(ValueError):
                store.transition_operation(self.root, self.request["operation_id"],
                                           "prepared", "submitting")
        self.assertEqual(path.read_bytes(), before)

    def test_profile_hash_is_additive_and_legacy_hash_stays_exact(self):
        legacy = validation.compute_request_hash(b"legacy", [], "model", "generate", {})
        self.assertEqual(legacy, hashlib.sha256(json.dumps({
            "prompt_sha256": hashlib.sha256(b"legacy").hexdigest(), "model": "model",
            "operation": "generate", "params": {}, "references": [],
        }, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
            allow_nan=False).encode()).hexdigest())
        bound = self.request["extensions"]["capability_profile"]
        self.assertNotEqual(legacy, validation.compute_request_hash(
            b"legacy", [], "model", "generate", {}, capability_profile=bound))


class ProfilePreparationTests(unittest.TestCase):
    def setUp(self):
        self.fixture = preparation.PrepareRequestTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root
        self.evidence = profile()
        (self.root / "caps.json").write_text(json.dumps(self.evidence))

    def command(self):
        argv = self.fixture.argv("--write", "--capabilities", "caps.json",
                                 "--provider", "fixture-provider",
                                 "--tool-schema-revision", "fixture-revision-1")
        argv[argv.index("--model") + 1] = MODEL
        for value in ("draft=true", "ratio=9:16", "generate_audio=true"):
            index = argv.index(value)
            del argv[index - 1:index + 1]
        return [sys.executable, str(preparation.ROOT / ".agents/scripts/prepare_request.py"),
                *argv]

    def test_subprocess_profile_write_and_wrong_revision_no_write(self):
        command = self.command()
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        output = json.loads(result.stdout)
        request_path = self.root / output["path"]
        request = json.loads(request_path.read_text())
        self.assertEqual(request["extensions"]["capability_profile"]["expected"],
                         {"provider": "fixture-provider",
                          "tool_schema_revision": "fixture-revision-1"})
        before = {p.relative_to(self.root): p.read_bytes()
                  for p in self.root.rglob("*") if p.is_file()}
        command[command.index("--tool-schema-revision") + 1] = "wrong"
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        after = {p.relative_to(self.root): p.read_bytes()
                 for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(after, before)

    def test_unbound_profile_is_rejected_before_any_write(self):
        command = self.command()
        index = command.index("--provider")
        del command[index:index + 2]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / "requests").exists())
        self.assertFalse((self.root / "task_ids.json").exists())


if __name__ == "__main__":
    unittest.main()
