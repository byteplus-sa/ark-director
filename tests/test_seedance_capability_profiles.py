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
        self.references = copy.deepcopy(self.request["references"])
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

    def test_empty_conditions_accept_ordinary_native_and_audio_parameters(self):
        for operation, native in (("generate", False), ("generate", True),
                                  ("generate_audio", False)):
            with self.subTest(operation=operation, native=native):
                self.evidence = profile(native)
                self.evidence["conditional_parameters"] = []
                self.evidence["operation"] = operation
                self.evidence["operations"] = [operation]
                self.request["operation"] = operation
                self.request["params"] = {
                    "duration": 5.125, "resolution": "480p",
                    **({"draft": True} if native else {}),
                }
                if operation == "generate_audio":
                    del self.request["params"]["resolution"]
                    self.evidence["preview"] = {
                        "native_draft": None, "promotion": None, "parameters": {},
                    }
                self.bind()
                before = copy.deepcopy((self.request, self.evidence))
                self.assertEqual(validation.schema_findings(
                    self.evidence, "capability-evidence.schema.json"), [])
                self.assertEqual(self.findings(), [])
                self.assertEqual((self.request, self.evidence), before)

    def test_empty_conditions_preserve_boundaries_required_and_unknown_parameters(self):
        self.evidence["conditional_parameters"] = []
        self.evidence["required_parameters"] = ["duration"]
        for duration in (2, 30):
            with self.subTest(duration=duration):
                self.request["params"]["duration"] = duration
                self.bind()
                self.assertEqual(self.findings(), [])
        for params in ({"resolution": "480p"},
                       {"resolution": "480p", "duration": None},
                       {"resolution": "480p", "duration": 1.999},
                       {"resolution": "480p", "duration": 30.001},
                       {"resolution": "480p", "duration": "5"},
                       {"resolution": "480p", "duration": 5, "unknown": True}):
            with self.subTest(params=params):
                self.request["params"] = params
                self.bind()
                before = copy.deepcopy(self.request)
                self.assertIn("model.supported_mode",
                              {item.rule_id for item in self.findings()})
                with self.assertRaises(ValueError):
                    store.prepare_operation(self.root, self.request, self.evidence, None, [])
                self.assertFalse((self.root / "task_ids.json").exists())
                self.assertEqual(self.request, before)

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

    def test_recursive_conditional_schemas_return_findings_without_registry_writes(self):
        for constraint in (
            {"$ref": "#"},
            {"$defs": {"loop": {"$ref": "#/allOf/0/$defs/loop"}},
             "$ref": "#/allOf/0/$defs/loop"},
            {"if": {"$ref": "#"}, "then": {}},
        ):
            with self.subTest(constraint=constraint):
                self.evidence["conditional_parameters"] = [constraint]
                self.bind()
                self.assertIn("model.supported_mode",
                              {item.rule_id for item in self.findings()})
                with self.assertRaises(ValueError):
                    store.prepare_operation(self.root, self.request, self.evidence, None, [])
                self.assertFalse((self.root / "task_ids.json").exists())

    def test_schema_literals_are_data_but_actual_constraints_still_apply(self):
        for literal in (
            {"$ref": "https://invalid.example/literal"},
            {"$ref": "#"},
            {"$dynamicRef": "#missing"},
            {"properties": {"literal": {"$ref": "https://invalid.example/data"}}},
        ):
            for keyword in ("const", "enum"):
                with self.subTest(literal=literal, keyword=keyword):
                    self.evidence["parameters"]["label"] = {
                        keyword: [literal] if keyword == "enum" else literal,
                        "default": {"$ref": "https://invalid.example/default"},
                        "examples": [{"$ref": "#"}],
                    }
                    self.request["params"]["label"] = copy.deepcopy(literal)
                    self.bind()
                    self.assertEqual(self.findings(), [])
                    self.request["params"]["label"] = "mismatch"
                    self.bind()
                    self.assertIn("model.supported_mode",
                                  {item.rule_id for item in self.findings()})

    def test_local_pointer_boolean_and_empty_schema_controls_remain_valid(self):
        self.evidence["parameters"]["duration"] = {
            "$ref": "#/allOf/0/$defs/span~1seconds~0",
        }
        self.evidence["parameters"]["label"] = True
        self.evidence["conditional_parameters"] = [{
            "$defs": {"span/seconds~": {"type": "number", "minimum": 2}},
            "if": True,
            "then": {"properties": {"resolution": {"enum": ["480p", "720p"]}}},
            "else": False,
        }, {}]
        self.bind()
        self.assertEqual(self.findings(), [])
        self.request["params"]["duration"] = 1
        self.bind()
        self.assertTrue(self.findings())

    def test_deep_schema_is_bounded_without_traversing_deep_literal_data(self):
        literal = {"$ref": "https://invalid.example/data"}
        for _ in range(80):
            literal = {"const": literal}
        self.evidence["parameters"]["label"] = {"const": literal}
        self.request["params"]["label"] = literal
        self.bind()
        self.assertEqual(self.findings(), [])
        schema = {"type": "number"}
        for _ in range(80):
            schema = {"allOf": [schema]}
        self.evidence["parameters"]["duration"] = schema
        self.bind()
        self.assertIn("model.supported_mode", {item.rule_id for item in self.findings()})

    def test_schema_node_budget_returns_findings_without_store_writes(self):
        self.evidence["parameters"]["duration"] = {"allOf": [True] * 5000}
        self.bind()
        self.assertIn("model.supported_mode", {item.rule_id for item in self.findings()})
        with self.assertRaises(ValueError):
            store.prepare_operation(self.root, self.request, self.evidence, None, [])
        self.assertFalse((self.root / "task_ids.json").exists())

    def test_local_pointer_to_literal_cannot_trigger_remote_retrieval(self):
        self.evidence["parameters"]["duration"] = {
            "default": {"$ref": "https://invalid.example/schema"},
            "$ref": "#/properties/duration/default",
        }
        self.bind()
        with patch("urllib.request.urlopen", side_effect=AssertionError("No network")):
            self.assertIn("model.supported_mode",
                          {item.rule_id for item in self.findings()})

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

    def nonlegacy_native(self, controls):
        self.request["references"] = copy.deepcopy(self.references)
        self.request["operation"] = "generate"
        self.evidence = profile(True)
        self.evidence["model"] = self.request["model"] = (
            "dreamina-seedance-native-offline-fixture"
        )
        self.evidence["conditional_parameters"] = [{}]
        self.evidence["parameters"]["preview_mode"] = {"enum": ["native", "final"]}
        self.evidence["preview"]["parameters"] = controls
        self.evidence["source"] = (
            "Synthetic offline operation contract: draft=true or preview_mode=native "
            "as specified in preview.parameters creates a native preview eligible "
            "for draft_task_id promotion. Not live provider verification."
        )
        self.request["params"] = {"duration": 5.125, **controls}
        self.bind()

    def nonlegacy_promotion(self, controls):
        self.nonlegacy_native(controls)
        draft = copy.deepcopy(self.request)
        draft.update(operation_id="selected-native", asset_id="selected-native",
                     submission_status="terminal", provider_status="succeeded",
                     provider_task_id="native-task", review_status="approved")
        (self.root / "task_ids.json").write_text(json.dumps(
            {"schema_version": 1, "tasks": [draft]}))
        self.request["params"] = {"draft_task_id": "native-task", "resolution": "1080p"}
        self.request["references"] = []
        self.bind()
        return draft

    def test_nonlegacy_native_preview_matches_evidenced_controls_without_legacy_fallback(self):
        for controls in ({"draft": True, "resolution": "720p"},
                         {"preview_mode": "native", "resolution": "720p"}):
            with self.subTest(controls=controls):
                self.nonlegacy_native(controls)
                before = copy.deepcopy(self.request)
                self.assertEqual(self.findings(), [])
                self.assertEqual(self.request, before)
                self.request["params"]["resolution"] = "480p"
                self.bind()
                self.assertIn("model.preview_controls",
                              {item.rule_id for item in self.findings()})

    def test_nonlegacy_native_controls_require_present_exact_json_values(self):
        for controls, params in (
            ({"preview_mode": None, "resolution": "720p"}, {"resolution": "720p"}),
            ({"draft": True, "resolution": "720p"}, {"draft": 1, "resolution": "720p"}),
        ):
            with self.subTest(controls=controls):
                self.nonlegacy_native(controls)
                self.evidence["parameters"].update(draft={}, preview_mode={})
                self.evidence["source"] = (
                    "Synthetic offline native-control semantics: the explicit null "
                    "preview_mode or boolean draft=true in preview.parameters creates "
                    "a native preview; missing fields and numeric draft=1 do not. "
                    "Not live provider verification."
                )
                self.bind()
                self.assertEqual(self.findings(), [])
                self.request["params"] = params
                self.bind()
                self.assertEqual(validation.capability_findings(
                    self.request, self.evidence), [])
                self.assertIn("model.preview_controls",
                              {item.rule_id for item in self.findings()})

    def test_nonlegacy_native_promotion_accepts_only_verified_selected_source(self):
        for controls in ({"draft": True, "resolution": "720p"},
                         {"preview_mode": "native", "resolution": "720p"}):
            with self.subTest(controls=controls):
                draft = self.nonlegacy_promotion(controls)
                self.assertEqual(validation.draft_input_findings(self.root, draft), [])
                before = copy.deepcopy((self.request, draft))
                self.assertEqual(self.findings(), [])
                self.assertEqual((self.request, draft), before)

    def test_nonlegacy_native_promotion_preserves_source_identity_state_and_expiry_guards(self):
        for change in ("hash", "prompt", "reference", "failed", "pending",
                       "unselected", "transport", "missing_profile", "destination",
                       "expiry", "ordinary", "unknown", "audio", "creative"):
            with self.subTest(change=change):
                draft = self.nonlegacy_promotion(
                    {"preview_mode": "native", "resolution": "720p"})
                self.assertEqual(self.findings(), [])
                bound = validation.request_profile(draft)
                if change == "hash":
                    draft["request_sha256"] = "0" * 64
                elif change == "prompt":
                    draft["prompt_sha256"] = "0" * 64
                elif change == "reference":
                    draft["references"][0]["sha256"] = "0" * 64
                elif change == "failed":
                    draft["provider_status"] = "failed"
                elif change == "pending":
                    draft["submission_status"] = "acknowledged"
                elif change == "unselected":
                    draft["review_status"] = "not_started"
                elif change == "transport":
                    draft["transport"] = "curl"
                elif change == "missing_profile":
                    del draft["extensions"]["capability_profile"]
                elif change == "destination":
                    bound["expected"]["provider"] = "other-provider"
                elif change in ("expiry", "ordinary", "unknown", "audio"):
                    if change == "expiry":
                        self.evidence["valid_until"] = (
                            datetime.now(UTC) - timedelta(seconds=1)).isoformat()
                    elif change == "ordinary":
                        self.evidence["preview"].update(native_draft=False, promotion=False)
                    elif change == "unknown":
                        self.evidence["preview"]["promotion"] = None
                    else:
                        self.evidence.update(operation="generate_audio",
                                             operations=["generate_audio"])
                        self.request["operation"] = draft["operation"] = "generate_audio"
                    self.bind()
                    draft["extensions"]["capability_profile"] = copy.deepcopy(
                        validation.request_profile(self.request))
                    draft["request_sha256"] = validation.compute_request_hash(
                        (self.root / "prompt.md").read_bytes(), draft["references"],
                        draft["model"], draft["operation"], draft["params"],
                        capability_profile=validation.request_profile(draft),
                    )
                else:
                    self.request["params"]["duration"] = 9
                    self.bind()
                path = self.root / "task_ids.json"
                path.write_text(json.dumps({"schema_version": 1, "tasks": [draft]}))
                before = path.read_bytes()
                self.assertTrue(validation.draft_promotion_findings(self.root, self.request))
                with self.assertRaises(ValueError):
                    store.prepare_operation(self.root, self.request, self.evidence, None, [])
                self.assertEqual(path.read_bytes(), before)

    def test_nonlegacy_native_promotion_rechecks_source_controls_even_with_current_hash(self):
        for params in ({"preview_mode": "final", "resolution": "720p"},
                       {"preview_mode": "native", "resolution": "480p"},
                       {"resolution": "720p"},
                       {"draft_task_id": "older-task", "resolution": "1080p"}):
            with self.subTest(params=params):
                draft = self.nonlegacy_promotion(
                    {"preview_mode": "native", "resolution": "720p"})
                draft["params"] = params
                draft["request_sha256"] = validation.compute_request_hash(
                    (self.root / "prompt.md").read_bytes(), draft["references"],
                    draft["model"], draft["operation"], draft["params"],
                    capability_profile=validation.request_profile(draft),
                )
                self.assertEqual(validation.persisted_profile_findings(draft), [])
                self.assertEqual(validation.draft_input_findings(self.root, draft), [])
                path = self.root / "task_ids.json"
                path.write_text(json.dumps({"schema_version": 1, "tasks": [draft]}))
                before = path.read_bytes()
                self.assertTrue(validation.draft_promotion_findings(self.root, self.request))
                with self.assertRaises(ValueError):
                    store.prepare_operation(self.root, self.request, self.evidence, None, [])
                self.assertEqual(path.read_bytes(), before)

    def test_legacy_profile_promotion_still_rejects_non_480p_native_sources(self):
        for model in sorted(validation.NATIVE_DRAFT_MODELS):
            with self.subTest(model=model):
                self.nonlegacy_native({"draft": True, "resolution": "720p"})
                self.request["model"] = self.evidence["model"] = model
                self.bind()
                draft = copy.deepcopy(self.request)
                draft.update(operation_id="selected-legacy", asset_id="selected-legacy",
                             submission_status="terminal", provider_status="succeeded",
                             provider_task_id="native-task", review_status="approved")
                self.assertEqual(validation.persisted_profile_findings(draft), [])
                self.assertEqual(validation.draft_input_findings(self.root, draft), [])
                path = self.root / "task_ids.json"
                path.write_text(json.dumps({"schema_version": 1, "tasks": [draft]}))
                self.request["params"] = {
                    "draft_task_id": "native-task", "resolution": "1080p"}
                self.request["references"] = []
                self.bind()
                before = path.read_bytes()
                findings = validation.draft_promotion_findings(self.root, self.request)
                self.assertTrue(any("not a 480p draft" in item.message for item in findings))
                with self.assertRaises(ValueError):
                    store.prepare_operation(self.root, self.request, self.evidence, None, [])
                self.assertEqual(path.read_bytes(), before)

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

    def test_recursive_schema_real_cli_returns_json_and_preserves_files(self):
        self.evidence["conditional_parameters"] = [{"$ref": "#"}]
        (self.root / "caps.json").write_text(json.dumps(self.evidence))
        before = {path.relative_to(self.root): path.read_bytes()
                  for path in self.root.rglob("*") if path.is_file()}
        result = subprocess.run(self.command(), capture_output=True, text=True,
                                check=False, timeout=20)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("model.supported_mode",
                      {item["rule_id"] for item in json.loads(result.stdout)["findings"]})
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(before, {path.relative_to(self.root): path.read_bytes()
                                 for path in self.root.rglob("*") if path.is_file()})

    def test_empty_conditions_cli_write_and_invalid_params_preserve_files(self):
        self.evidence["conditional_parameters"] = []
        (self.root / "caps.json").write_text(json.dumps(self.evidence))
        command = self.command()
        command.insert(1, "-B")
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        before = {path.relative_to(self.root): path.read_bytes()
                  for path in self.root.rglob("*") if path.is_file()}
        command[command.index("duration=8")] = "duration=null"
        result = subprocess.run(command + ["--replace-unregistered"],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("model.supported_mode", result.stdout)
        self.assertEqual(before, {path.relative_to(self.root): path.read_bytes()
                                 for path in self.root.rglob("*") if path.is_file()})


class OrdinaryFinalTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.RequestValidationTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root
        self.fixture.prepare_v2()
        (self.root / "studio").mkdir()
        self.source = copy.deepcopy(self.fixture.request)
        self.evidence = profile()
        self.evidence["preview"]["parameters"] = {"resolution": "720p"}
        self.source.update(model=MODEL, operation_id="ordinary-preview",
                           asset_id="ordinary-preview",
                           params={"duration": 5.125, "resolution": "720p"})
        self.source["extensions"] = {
            "expected_output": "preview.mp4",
            "capability_profile": {
                "expected": {"provider": "fixture-provider",
                             "tool_schema_revision": "fixture-revision-1"},
                "evidence": copy.deepcopy(self.evidence),
                "sha256": validation.capability_digest(self.evidence),
            },
        }
        self.rehash(self.source)
        self.source.update(submission_status="terminal", provider_status="succeeded",
                           provider_task_id="ordinary-task", review_status="approved")
        self.fixture.select_draft_take()
        (self.root / "preview.mp4").write_bytes(b"synthetic preview, not real playback")
        review = json.loads((self.root / "draft_review.json").read_text())
        review.update(artifact_path="preview.mp4",
                      artifact_sha256=self.fixture.hash("preview.mp4"))
        (self.root / "preview_review.json").write_text(json.dumps(review))
        decision = json.loads((self.root / "decisions/draft-choice.json").read_text())
        decision.update(decision_id="preview-choice", asset_id="ordinary-preview",
                        subject_path="preview.mp4", selected_variant="preview.mp4",
                        selected_sha256=self.fixture.hash("preview.mp4"),
                        project_sha256=self.fixture.hash("project.md"),
                        review_path="preview_review.json",
                        review_sha256=self.fixture.hash("preview_review.json"))
        (self.root / "decisions/preview-choice.json").write_text(json.dumps(decision))
        self.selection = {
            "manifest": "preview.md", "field": "selected_variant",
            "decision_id": "preview-choice",
            "decision_path": "decisions/preview-choice.json",
            "decision_sha256": self.fixture.hash("decisions/preview-choice.json"),
            "review_path": "preview_review.json",
            "review_sha256": self.fixture.hash("preview_review.json"),
            "selected_sha256": self.fixture.hash("preview.mp4"),
        }
        (self.root / "preview.md").write_text(
            "---\nselected_variant: preview.mp4\nstatus: approved\nselection_evidence:\n"
            + "".join(f"  {key}: {value}\n" for key, value in self.selection.items()
                      if key not in ("manifest", "field"))
            + "  actor: agent\n  approval_mode: approve_for_me\n---\n")
        self.write_source()
        self.request = copy.deepcopy(self.source)
        self.request.update(operation_id="ordinary-final", asset_id="ordinary-final",
                            submission_status="prepared", provider_status=None,
                            provider_task_id=None, review_status="not_started")
        self.request["params"]["resolution"] = "1080p"
        self.request["extensions"]["expected_output"] = "final.mp4"
        self.request["extensions"]["capability_profile"]["ordinary_final"] = {
            "source_operation_id": self.source["operation_id"],
            "source_request_sha256": self.source["request_sha256"],
            "selection": copy.deepcopy(self.selection),
        }
        self.rehash(self.request)

    def rehash(self, request):
        request["request_sha256"] = validation.compute_request_hash(
            (self.root / request["prompt_file"]).read_bytes(), request["references"],
            request["model"], request["operation"], request["params"],
            approval_mode=request.get("approval_mode"),
            project_sha256=request.get("project_sha256"),
            capability_profile=validation.request_profile(request),
        )

    def write_source(self):
        (self.root / "task_ids.json").write_text(json.dumps(
            {"schema_version": 1, "tasks": [self.source]}))

    def findings(self):
        return validation.validate_request(self.root, self.request, self.evidence)

    def test_selected_successful_ordinary_preview_can_prepare_fresh_final(self):
        before = copy.deepcopy((self.request, self.source))
        self.assertEqual(validation.capability_findings(self.request, self.evidence), [])
        self.assertEqual(self.findings(), [])
        store.prepare_operation(self.root, self.request, self.evidence, None, [])
        store.transition_operation(self.root, "ordinary-final", "prepared", "submitting")
        records = store.read_registry(self.root / "task_ids.json")["tasks"]
        self.assertEqual(records[0], self.source)
        self.assertEqual(records[1]["submission_status"], "submitting")
        self.assertEqual((self.request, self.source), before)

    def test_missing_malformed_or_unbound_intent_never_authorizes_final(self):
        for intent in (None, {}, "final", [], {"source_operation_id": "ordinary-preview"}):
            with self.subTest(intent=intent):
                self.request["extensions"]["capability_profile"]["ordinary_final"] = intent
                self.rehash(self.request)
                self.assertTrue(self.findings())
        del self.request["extensions"]["capability_profile"]["ordinary_final"]
        self.rehash(self.request)
        self.assertIn("model.preview_controls", {item.rule_id for item in self.findings()})

    def test_intent_tampering_invalidates_existing_request_hash(self):
        self.assertEqual(self.findings(), [])
        intent = self.request["extensions"]["capability_profile"]["ordinary_final"]
        intent["source_request_sha256"] = "0" * 64
        self.assertIn("request.current_hash", {item.rule_id for item in self.findings()})

    def test_final_rejects_changed_creative_inputs_and_draft_controls(self):
        for params in (
            {"duration": 5.126, "resolution": "1080p"},
            {"resolution": "1080p"},
            {"duration": 5.125, "resolution": "1080p", "draft": False},
            {"duration": 5.125, "resolution": "1080p", "draft_task_id": "ordinary-task"},
        ):
            with self.subTest(params=params):
                self.request["params"] = params
                self.rehash(self.request)
                before = (self.root / "task_ids.json").read_bytes()
                with self.assertRaises(ValueError):
                    store.prepare_operation(self.root, self.request, self.evidence, None, [])
                self.assertEqual((self.root / "task_ids.json").read_bytes(), before)

    def test_stale_source_selection_fails_without_registration_writes(self):
        for field, value in (("submission_status", "acknowledged"),
                             ("provider_status", "failed"),
                             ("request_sha256", "0" * 64),
                             ("transport", "curl"), ("operation", "edit"),
                             ("provider_task_id", None)):
            with self.subTest(field=field):
                original = self.source[field]
                self.source[field] = value
                self.write_source()
                before = (self.root / "task_ids.json").read_bytes()
                self.assertTrue(self.findings())
                with self.assertRaises(ValueError):
                    store.prepare_operation(self.root, self.request, self.evidence, None, [])
                self.assertEqual((self.root / "task_ids.json").read_bytes(), before)
                self.source[field] = original
        self.write_source()
        (self.root / "preview.md").write_text(
            "---\nselected_variant: auto\nstatus: review\n---\n")
        self.assertTrue(self.findings())

    def test_selection_rechecked_after_final_registration(self):
        store.prepare_operation(self.root, self.request, self.evidence, None, [])
        before = (self.root / "task_ids.json").read_bytes()
        (self.root / "preview.mp4").write_bytes(b"changed preview")
        with self.assertRaises(ValueError):
            store.transition_operation(self.root, "ordinary-final", "prepared", "submitting")
        self.assertEqual((self.root / "task_ids.json").read_bytes(), before)

    def test_source_cannot_be_native_or_already_a_final(self):
        for native in (True, None):
            with self.subTest(native=native):
                self.source["extensions"]["capability_profile"]["evidence"]["preview"][
                    "native_draft"] = native
                self.write_source()
                self.assertTrue(self.findings())
        self.source["extensions"]["capability_profile"] = copy.deepcopy(
            self.request["extensions"]["capability_profile"])
        self.write_source()
        self.assertTrue(self.findings())

    def test_rehashed_source_with_wrong_preview_controls_still_fails(self):
        self.source["params"]["resolution"] = "1080p"
        self.rehash(self.source)
        self.request["extensions"]["capability_profile"]["ordinary_final"][
            "source_request_sha256"] = self.source["request_sha256"]
        self.rehash(self.request)
        self.write_source()
        self.assertTrue(self.findings())

    def test_creative_parameter_json_types_and_reference_order_are_exact(self):
        self.evidence["parameters"]["creative"] = {}
        for request in (self.source, self.request):
            validation.request_profile(request)["evidence"] = copy.deepcopy(self.evidence)
            validation.request_profile(request)["sha256"] = validation.capability_digest(self.evidence)
            request["params"]["creative"] = True
            self.rehash(request)
        self.request["extensions"]["capability_profile"]["ordinary_final"][
            "source_request_sha256"] = self.source["request_sha256"]
        self.rehash(self.request)
        self.write_source()
        self.assertEqual(self.findings(), [])
        self.request["params"]["creative"] = 1
        self.rehash(self.request)
        self.assertTrue(self.findings())
        self.request["params"]["creative"] = True
        self.request["references"] = []
        self.rehash(self.request)
        self.assertTrue(self.findings())

    def test_output_only_changes_are_supported_but_new_identities_are_required(self):
        self.evidence["parameters"]["watermark"] = {"type": "boolean"}
        for request in (self.source, self.request):
            validation.request_profile(request)["evidence"] = copy.deepcopy(self.evidence)
            validation.request_profile(request)["sha256"] = validation.capability_digest(self.evidence)
        self.rehash(self.source)
        self.request["extensions"]["capability_profile"]["ordinary_final"][
            "source_request_sha256"] = self.source["request_sha256"]
        self.request["params"]["watermark"] = False
        self.rehash(self.request)
        self.write_source()
        self.assertEqual(self.findings(), [])
        for field in ("asset_id", "operation_id"):
            with self.subTest(field=field):
                original = self.request[field]
                self.request[field] = self.source[field]
                self.assertTrue(self.findings())
                self.request[field] = original
        self.request["extensions"]["expected_output"] = "preview.mp4"
        self.assertTrue(self.findings())

    def test_final_output_identity_rejects_malformed_paths_and_preview_aliases(self):
        (self.root / "preview-alias.mp4").symlink_to("preview.mp4")
        (self.root / "preview-hardlink.mp4").hardlink_to(self.root / "preview.mp4")
        (self.root / "outside-output.mp4").symlink_to("/outside-final.mp4")
        for output in (None, "", {}, [], "/outside.mp4", "../final.mp4", ".",
                       "./preview.mp4", "preview-alias.mp4", "preview-hardlink.mp4",
                       "outside-output.mp4"):
            with self.subTest(output=output):
                self.request["extensions"]["expected_output"] = output
                self.assertIn("seedance.ordinary_final",
                              {item.rule_id for item in self.findings()})
                before = (self.root / "task_ids.json").read_bytes()
                with self.assertRaises(ValueError):
                    store.prepare_operation(self.root, self.request, self.evidence, None, [])
                self.assertEqual((self.root / "task_ids.json").read_bytes(), before)
        del self.request["extensions"]["expected_output"]
        self.assertTrue(self.findings())

    def test_final_selection_decision_requires_current_authorization_and_review(self):
        path = self.root / "decisions/preview-choice.json"
        original = json.loads(path.read_text())
        manifest = self.root / "preview.md"
        original_manifest = manifest.read_text()
        original_digest = self.selection["decision_sha256"]
        for changes in (
            {"asset_id": "other-asset"},
            {"project_sha256": "0" * 64},
            {"actor": "user"},
            {"result": "rejected"},
            {"review_sha256": "0" * 64},
        ):
            with self.subTest(changes=changes):
                path.write_text(json.dumps({**original, **changes}))
                digest = self.fixture.hash("decisions/preview-choice.json")
                manifest.write_text(original_manifest.replace(original_digest, digest))
                self.request["extensions"]["capability_profile"]["ordinary_final"][
                    "selection"]["decision_sha256"] = digest
                self.rehash(self.request)
                self.assertTrue(self.findings())
        path.write_text(json.dumps(original))
        manifest.write_text(original_manifest)
        self.request["extensions"]["capability_profile"]["ordinary_final"][
            "selection"]["decision_sha256"] = original_digest
        self.rehash(self.request)
        self.assertEqual(self.findings(), [])
        (self.root / "preview_review.json").write_text("{}")
        self.assertTrue(self.findings())

    def test_reordered_valid_preview_references_fail_exact_final_lineage(self):
        prompt = b"Use @Image 1 and @Image 2 as the approved visual authorities."
        (self.root / "prompt.md").write_bytes(prompt)
        second = {**copy.deepcopy(self.source["references"][0]), "binding": "@Image 2"}
        for request in (self.source, self.request):
            request["references"].append(copy.deepcopy(second))
            request["prompt_sha256"] = hashlib.sha256(prompt).hexdigest()
        self.rehash(self.source)
        self.request["extensions"]["capability_profile"]["ordinary_final"][
            "source_request_sha256"] = self.source["request_sha256"]
        self.rehash(self.request)
        self.write_source()
        self.assertEqual(self.findings(), [])
        self.request["references"].reverse()
        self.rehash(self.request)
        self.assertIn("seedance.ordinary_final", {item.rule_id for item in self.findings()})

    def test_profile_expiry_blocks_registered_final_without_registry_mutation(self):
        store.prepare_operation(self.root, self.request, self.evidence, None, [])
        before = (self.root / "task_ids.json").read_bytes()
        with patch.object(validation, "datetime", wraps=datetime) as clock:
            clock.now.return_value = datetime.now(UTC) + timedelta(hours=2)
            with self.assertRaises(ValueError):
                store.transition_operation(self.root, "ordinary-final", "prepared", "submitting")
        self.assertEqual((self.root / "task_ids.json").read_bytes(), before)

    def final_command(self, *extra):
        (self.root / "caps.json").write_text(json.dumps(self.evidence))
        return [
            sys.executable, "-B", str(preparation.ROOT / ".agents/scripts/prepare_request.py"),
            "--project", str(self.root), "--asset", "ordinary-final",
            "--operation-id", "ordinary-final", "--prompt", "prompt.md",
            "--model", MODEL, "--operation", "generate",
            "--param", "duration=5.125", "--param", "resolution=1080p",
            "--ref", "image.png:reference_image:character.md",
            "--expected-output", "final.mp4", "--capabilities", "caps.json",
            "--provider", "fixture-provider", "--tool-schema-revision", "fixture-revision-1",
            "--ordinary-final-source", "ordinary-preview",
            "--ordinary-final-selection", "preview.md", *extra,
        ]

    def cli(self, command):
        result = subprocess.run(command, capture_output=True, text=True,
                                check=False, timeout=20)
        self.assertNotIn("Traceback", result.stderr)
        return result.returncode, json.loads(result.stdout)

    def test_real_final_prepare_recorder_validator_and_store_smoke(self):
        for mode in ("default", "strict"):
            with self.subTest(mode=mode):
                command = self.final_command("--write")
                if mode == "strict":
                    (self.root / "project.md").write_text(
                        "---\napproval_mode: approve_for_me\nreview_mode: strict\n---\n")
                    decision_path = self.root / "decisions/preview-choice.json"
                    decision = json.loads(decision_path.read_text())
                    decision["project_sha256"] = self.fixture.hash("project.md")
                    decision_path.write_text(json.dumps(decision))
                    self.selection["decision_sha256"] = self.fixture.hash(
                        "decisions/preview-choice.json")
                    (self.root / "preview.md").write_text(
                        "---\nselected_variant: preview.mp4\nstatus: approved\nselection_evidence:\n"
                        + "".join(f"  {key}: {value}\n" for key, value in self.selection.items()
                                  if key not in ("manifest", "field"))
                        + "  actor: agent\n  approval_mode: approve_for_me\n---\n")
                    self.write_source()
                    (self.root / "requests/request_ordinary-final.json").unlink()
                    (self.root / "reviews/review_ordinary-final.json").unlink()
                code, output = self.cli(command)
                self.assertEqual(code, 0, output)
                request_path = self.root / output["path"]
                final = json.loads(request_path.read_text())
                review = {
                    "schema_version": 1, "request_sha256": final["request_sha256"],
                    "reviewer_status": "complete",
                    "checks": [{"rule_id": "fixture.offline", "status": "pass",
                                "evidence": "Synthetic request checks only, no real media QA"}],
                }
                (self.root / "review-input.json").write_text(json.dumps(review))
                code, output = self.cli([
                    sys.executable, "-B", str(preparation.ROOT /
                        ".agents/skills/prompt-review/scripts/record_review.py"),
                    "--project", str(self.root), "--request", "requests/request_ordinary-final.json",
                    "--input", str(self.root / "review-input.json"), "--write",
                ])
                self.assertEqual(code, 0, output)
                review_path = output["path"]
                code, output = self.cli(self.final_command(
                    "--write", "--register", "--review", review_path))
                self.assertEqual(code, 0, output)
                code, output = self.cli([
                    sys.executable, "-B", str(preparation.ROOT / ".agents/scripts/validate_request.py"),
                    "--project", str(self.root), "--request", str(request_path),
                    "--capabilities", str(self.root / "caps.json"),
                    "--review", str(self.root / review_path),
                ])
                self.assertEqual(code, 0, output)
                store.transition_operation(self.root, "ordinary-final", "prepared", "submitting")
                self.assertEqual(store.read_registry(self.root / "task_ids.json")["tasks"][-1][
                    "submission_status"], "submitting")
                code, output = self.cli(self.final_command(
                    "--write", "--register", "--review", review_path))
                self.assertEqual(code, 1, output)
                self.assertIn("registry.prepare",
                              {item["rule_id"] for item in output["findings"]})

    def test_cli_missing_stale_selection_or_changed_creative_inputs_write_nothing(self):
        for change in ("missing_source", "missing_selection", "duration", "destination", "selection"):
            with self.subTest(change=change):
                command = self.final_command("--write", "--register")
                if change in ("missing_source", "missing_selection"):
                    flag = "--ordinary-final-source" if change == "missing_source" else (
                        "--ordinary-final-selection")
                    index = command.index(flag)
                    del command[index:index + 2]
                elif change == "duration":
                    command[command.index("duration=5.125")] = "duration=6"
                elif change == "destination":
                    command[command.index("--provider") + 1] = "wrong-provider"
                else:
                    (self.root / "preview.md").write_text(
                        "---\nselected_variant: auto\nstatus: review\n---\n")
                before = {path.relative_to(self.root): path.read_bytes()
                          for path in self.root.rglob("*") if path.is_file()}
                code, output = self.cli(command)
                self.assertEqual(code, 1, output)
                self.assertEqual(before, {path.relative_to(self.root): path.read_bytes()
                                         for path in self.root.rglob("*") if path.is_file()})


if __name__ == "__main__":
    unittest.main()
