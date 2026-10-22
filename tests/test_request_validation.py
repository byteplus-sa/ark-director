import copy
import hashlib
import importlib.util
import json
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

DRAFT_MODEL = "dreamina-seedance-2-5-260628"


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
            approval_mode=self.request.get("approval_mode"),
            project_sha256=self.request.get("project_sha256"),
        )

    def prepare_v2(self):
        (self.root / "project.md").write_text(
            "---\napproval_mode: approve_for_me\n---\n"
        )
        self.request["schema_version"] = 2
        self.request["approval_mode"] = "approve_for_me"
        self.request["project_sha256"] = self.hash("project.md")
        review = {
            "schema_version": 1,
            "artifact_path": "image.png",
            "artifact_sha256": self.hash("image.png"),
            "status": "pass",
            "inspection_method": "direct image inspection",
            "coverage": "full image at original resolution",
            "checks": [
                {
                    "criterion": "visible identity",
                    "status": "pass",
                    "evidence": "Matches source",
                }
            ],
            "observations": ["Image is complete"],
            "limitations": [],
            "recommendation": "Select this image",
        }
        (self.root / "review.json").write_text(json.dumps(review))
        decision = {
            "schema_version": 1,
            "decision_id": "choice-1",
            "decision_type": "variant_selection",
            "asset_id": "fixture",
            "subject_path": "image.png",
            "selected_variant": "image.png",
            "selected_sha256": self.hash("image.png"),
            "actor": "agent",
            "approval_mode": "approve_for_me",
            "project_sha256": self.hash("project.md"),
            "result": "approved",
            "review_path": "review.json",
            "review_sha256": self.hash("review.json"),
            "upstream_sha256": {},
            "reason": "Best passing option",
            "decided_at": "2026-09-23T00:00:00Z",
        }
        (self.root / "decisions").mkdir()
        (self.root / "decisions/choice-1.json").write_text(json.dumps(decision))
        evidence = {
            "manifest": "character.md",
            "field": "selected_variant",
            "decision_id": "choice-1",
            "decision_path": "decisions/choice-1.json",
            "decision_sha256": self.hash("decisions/choice-1.json"),
            "review_path": "review.json",
            "review_sha256": self.hash("review.json"),
            "selected_sha256": self.hash("image.png"),
        }
        self.request["references"][0]["approval_evidence"] = evidence
        (self.root / "character.md").write_text(
            "---\nselected_variant: image.png\nstatus: approved\nselection_evidence:\n"
            + "".join(
                f"  {key}: {value}\n"
                for key, value in evidence.items()
                if key not in ("manifest", "field")
            )
            + "  actor: agent\n  approval_mode: approve_for_me\n---\n"
        )
        self.rehash()
        return review, decision

    def findings(self):
        return validation.validate_request(self.root, self.request, self.caps)

    def test_valid_request_passes_without_mutation(self):
        before = copy.deepcopy(self.request)
        self.assertEqual(self.findings(), [])
        self.assertEqual(self.request, before)

    def test_v2_valid_approved_decision_passes(self):
        self.prepare_v2()
        self.assertEqual(self.findings(), [])

    def test_v2_selected_variants_evidence_uses_matching_key(self):
        self.prepare_v2()
        evidence = self.request["references"][0]["approval_evidence"]
        evidence["field"] = "selected_variants"
        evidence["key"] = "hero"
        (self.root / "character.md").write_text(
            "---\nselected_variants:\n  hero: image.png\nstatus: review\nselection_evidence:\n  hero:\n"
            + "".join(
                f"    {key}: {value}\n"
                for key, value in evidence.items()
                if key not in ("manifest", "field", "key")
            )
            + "    actor: agent\n    approval_mode: approve_for_me\n---\n"
        )
        self.rehash()
        self.assertEqual(self.findings(), [])
        evidence["key"] = "other"
        self.rehash()
        self.assertIn(
            "approval.selected_variant",
            {finding.rule_id for finding in self.findings()},
        )

    def test_v2_missing_or_failing_review_blocks_reference(self):
        review, decision = self.prepare_v2()
        review["status"] = "fail"
        (self.root / "review.json").write_text(json.dumps(review))
        ids = {finding.rule_id for finding in self.findings()}
        self.assertIn("approval.review_hash", ids)
        decision["review_sha256"] = self.hash("review.json")
        self.assertIn(
            "approval.passing_review",
            {
                finding.rule_id
                for finding in validation.decision_findings(self.root, decision)
            },
        )

    def test_v2_changed_selected_file_or_decision_blocks_reference(self):
        self.prepare_v2()
        (self.root / "image.png").write_bytes(b"changed")
        self.assertIn(
            "approval.selected_hash", {finding.rule_id for finding in self.findings()}
        )
        (self.root / "decisions/choice-1.json").write_text("{}")
        self.assertIn(
            "approval.decision_hash", {finding.rule_id for finding in self.findings()}
        )

    def test_v2_mode_change_blocks_preflight(self):
        self.prepare_v2()
        (self.root / "project.md").write_text(
            "---\napproval_mode: ask_for_approval\n---\n"
        )
        self.assertIn(
            "approval.current_mode", {finding.rule_id for finding in self.findings()}
        )

    def test_v2_plain_text_legacy_project_uses_bound_default_mode(self):
        self.prepare_v2()
        (self.root / "project.md").write_text(
            "Legacy project brief without frontmatter.\n"
        )
        self.request["project_sha256"] = self.hash("project.md")
        self.rehash()
        self.assertEqual(validation.project_mode_findings(self.root, self.request), [])
        (self.root / "project.md").write_text("---\ninvalid frontmatter")
        self.assertIn(
            "approval.current_mode",
            {
                finding.rule_id
                for finding in validation.project_mode_findings(self.root, self.request)
            },
        )

    def test_v2_rejects_agent_decision_in_ask_mode(self):
        self.prepare_v2()
        decision_path = self.root / "decisions/choice-1.json"
        decision = json.loads(decision_path.read_text())
        decision["approval_mode"] = "ask_for_approval"
        self.assertTrue(validation.decision_findings(self.root, decision))

    def test_v2_tagged_legacy_selection_requires_matching_audit(self):
        self.prepare_v2()
        (self.root / "selection.log").write_text(
            json.dumps({"event": "save", "selections": {"fixture": "image.png"}}) + "\n"
        )
        (self.root / "character.md").write_text(
            "---\nselected_variant: image.png\nstatus: approved\n---\n"
        )
        self.request["references"][0]["approval_evidence"] = {
            "manifest": "character.md",
            "field": "selected_variant",
            "selected_sha256": self.hash("image.png"),
            "evidence_type": "legacy",
            "legacy_asset_id": "fixture",
            "audit_path": "selection.log",
            "audit_sha256": self.hash("selection.log"),
        }
        self.rehash()
        self.assertEqual(self.findings(), [])
        (self.root / "selection.log").write_text(
            json.dumps({"event": "save", "selections": {"fixture": "other.png"}}) + "\n"
        )
        self.assertIn(
            "approval.legacy_audit", {finding.rule_id for finding in self.findings()}
        )

    def test_stage_lock_decision_requires_valid_review_and_user_authorization(self):
        _, decision = self.prepare_v2()
        decision.pop("asset_id")
        decision.pop("selected_variant")
        decision["subject_sha256"] = decision.pop("selected_sha256")
        decision["decision_type"] = "stage_lock"
        decision["stage_id"] = "assembly-review"
        decision["lock_kind"] = "picture"
        decision["actor"] = "user"
        decision["approval_mode"] = "ask_for_approval"
        self.assertTrue(validation.decision_findings(self.root, decision))
        decision["authorization"] = {
            "source": "chat",
            "evidence": "User chose picture lock",
        }
        self.assertIn(
            "approval.authorization",
            {
                finding.rule_id
                for finding in validation.decision_findings(self.root, decision)
            },
        )
        (self.root / "studio").mkdir()
        self.assertNotIn(
            "approval.authorization",
            {
                finding.rule_id
                for finding in validation.decision_findings(self.root, decision)
            },
        )
        (self.root / "showcase.json").write_text("{}")
        self.assertIn(
            "approval.authorization",
            {
                finding.rule_id
                for finding in validation.decision_findings(self.root, decision)
            },
        )
        (self.root / "showcase.json").unlink()
        (self.root / "studio").rmdir()
        decision["authorization"] = {
            "source": "local_ui",
            "evidence": "local_review_ui",
        }
        self.assertEqual(validation.decision_findings(self.root, decision), [])

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

    def use_reference_at(self, relative: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"board fixture")
        self.request["references"][0]["path"] = relative
        self.request["references"][0]["sha256"] = self.hash(relative)

    def test_storyboard_artifacts_are_rejected_as_references(self):
        for relative in [
            "scenes/scene-02/s02_sh010/s02_sh010_p010_t01_v01.png",
            "scenes/scene-02/s02_sh010/s02_sh010_board_t01_v01.png",
            "scenes/scene-02/board/sheet/anything.png",
            "scenes/scene-02/board/animatic/s02_animatic_v01.mp4",
            "elsewhere/s02_sheet_pg01_v01.png",
            "elsewhere/s02_overview_v02.png",
        ]:
            with self.subTest(relative=relative):
                self.use_reference_at(relative)
                self.assertIn(
                    "board.animatic_review_only",
                    {f.rule_id for f in self.findings()},
                )

    def test_board_guard_catches_path_spellings_that_resolve_to_a_board(self):
        for relative in [
            "scenes/scene-02//board/sheet/x.png",
            "scenes/scene-02/./board/sheet/x.png",
            "Scenes/Scene-02/Board/sheet/x.png",
            "scenes/scene-02/s02_sh010/s02_sh010_p010_t01_v01.JPG",
            "scenes/scene-02/s02_sh010/s02_sh010_board_t01_v01.webp",
        ]:
            with self.subTest(relative=relative):
                path = self.root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"board fixture")
                self.request["references"][0]["path"] = relative
                self.request["references"][0]["sha256"] = self.hash(
                    relative.replace("//", "/").replace("/./", "/")
                )
                self.assertIn(
                    "board.animatic_review_only",
                    {f.rule_id for f in self.findings()},
                )

    def test_board_guard_follows_a_symlink_to_a_board_file(self):
        target = self.root / "scenes/scene-02/board/sheet/x.png"
        target.parent.mkdir(parents=True)
        target.write_bytes(b"board fixture")
        (self.root / "innocent.png").symlink_to(target)
        self.request["references"][0]["path"] = "innocent.png"
        self.request["references"][0]["sha256"] = self.hash("innocent.png")
        self.assertIn(
            "board.animatic_review_only", {f.rule_id for f in self.findings()}
        )

    def test_board_guard_skips_seedream_edits_and_adoption(self):
        relative = "scenes/scene-02/s02_sh010/s02_sh010_p010_t01_v01.png"
        self.use_reference_at(relative)
        references = self.request["references"]
        prompt = (self.root / "prompt.md").read_text()
        self.assertIn(
            "board.animatic_review_only",
            {
                f.rule_id
                for f in validation.reference_findings(
                    self.root, references, prompt, model="dreamina-seedance-2-5"
                )
            },
        )
        for tricky in ("seedance-2-5-via-seedream", "ep-20260910224412-hcwv7", ""):
            self.assertIn(
                "board.animatic_review_only",
                {
                    f.rule_id
                    for f in validation.reference_findings(
                        self.root, references, prompt, model=tricky
                    )
                },
                tricky,
            )
        self.assertNotIn(
            "board.animatic_review_only",
            {
                f.rule_id
                for f in validation.reference_findings(
                    self.root, references, prompt, model="dola-seedream-5-0-pro"
                )
            },
        )
        self.assertNotIn(
            "board.animatic_review_only",
            {
                f.rule_id
                for f in validation.reference_findings(
                    self.root,
                    references,
                    prompt,
                    model="dreamina-seedance-2-5",
                    allow_board_references=True,
                )
            },
        )

    def test_board_guard_reports_even_when_containment_fails(self):
        self.request["references"][0]["path"] = "../scenes/scene-02/board/x.png"
        rules = {f.rule_id for f in self.findings()}
        self.assertIn("board.animatic_review_only", rules)
        self.assertIn("path.containment", rules)

    def test_element_sheets_and_keyframes_are_not_taken_for_boards(self):
        for relative in [
            "elements/gloria/char_gloria_turnaround_v01.png",
            "scenes/scene-02/s02_kf01_v01.png",
            "scenes/scene-02/s02_sh010/s02_sh010_t01_v01.mp4",
            "projects/board/photo.png",
            "my_scenes/scene-02/board.png",
        ]:
            with self.subTest(relative=relative):
                self.use_reference_at(relative)
                self.assertNotIn(
                    "board.animatic_review_only",
                    {f.rule_id for f in self.findings()},
                )

    def test_board_path_detection_handles_separators_and_nesting(self):
        self.assertTrue(
            validation.is_board_artifact("a\\scenes\\scene-01\\board\\x.png")
        )
        self.assertTrue(
            validation.is_board_artifact("p/scenes/scene-01/board/overview/x.png")
        )
        self.assertFalse(
            validation.is_board_artifact("scenes/scene-01/s01_sh010/x.mp4")
        )
        self.assertFalse(validation.is_board_artifact(""))

    def register_draft(self, **changes):
        draft = copy.deepcopy(self.request)
        draft.update(
            operation_id="fixture-draft",
            asset_id="fixture_draft",
            model=DRAFT_MODEL,
            params={"draft": True, "resolution": "480p", "duration": 5},
            submission_status="terminal",
            provider_task_id="cgt-draft-1",
            provider_status="succeeded",
            review_status="approved",
            extensions={"expected_output": "draft.mp4"},
        )
        draft.update(changes)
        (self.root / "task_ids.json").write_text(
            json.dumps({"schema_version": 1, "tasks": [draft]})
        )
        return draft

    def promote(self, task_id="cgt-draft-1", **draft_changes):
        self.register_draft(**draft_changes)
        self.request["model"] = self.caps["model"] = DRAFT_MODEL
        self.request["references"] = []
        self.request["params"] = {"draft_task_id": task_id, "resolution": "1080p"}
        self.caps["parameters"] = {
            "draft_task_id": {"type": "string"},
            "resolution": {"enum": ["1080p"]},
        }
        self.rehash()

    def promotion_findings(self):
        return [
            finding
            for finding in self.findings()
            if finding.rule_id == "seedance.draft_promotion_source"
        ]

    def select_draft_take(self):
        (self.root / "draft.mp4").write_bytes(b"fixture draft video")
        review = {
            "schema_version": 1,
            "artifact_path": "draft.mp4",
            "artifact_sha256": self.hash("draft.mp4"),
            "status": "pass",
            "inspection_method": "full playback with sound",
            "coverage": "every frame of the draft",
            "checks": [
                {
                    "criterion": "motion and speech timing",
                    "status": "pass",
                    "evidence": "Walk and line land on their beats",
                }
            ],
            "observations": ["Draft is complete"],
            "limitations": [],
            "recommendation": "Promote this draft",
        }
        (self.root / "draft_review.json").write_text(json.dumps(review))
        decision = {
            "schema_version": 1,
            "decision_id": "draft-choice",
            "decision_type": "variant_selection",
            "asset_id": "fixture_draft",
            "subject_path": "draft.mp4",
            "selected_variant": "draft.mp4",
            "selected_sha256": self.hash("draft.mp4"),
            "actor": "agent",
            "approval_mode": "approve_for_me",
            "project_sha256": "0" * 64,
            "result": "approved",
            "review_path": "draft_review.json",
            "review_sha256": self.hash("draft_review.json"),
            "upstream_sha256": {},
            "reason": "Best passing draft",
            "decided_at": "2026-10-17T00:00:00Z",
        }
        (self.root / "decisions").mkdir(exist_ok=True)
        (self.root / "decisions/draft-choice.json").write_text(json.dumps(decision))

    def ordered_binding_findings(self):
        return [
            finding
            for finding in self.findings()
            if finding.rule_id == "references.ordered_bindings"
        ]

    def test_draft_promotion_without_references_accepts_inherited_bindings(self):
        self.promote()
        self.assertEqual(self.findings(), [])

    def test_promotion_rejects_creative_parameters_even_when_capabilities_allow(self):
        creative_params = {
            "prompt": "A different scene",
            "duration": 10,
            "ratio": "9:16",
            "generate_audio": False,
            "seed": 42,
            "draft": False,
            "images": [],
            "videos": [],
            "audios": [],
            "omni_reference_task_type": "edit",
            "unknown_parameter": "value",
        }
        for name, value in creative_params.items():
            with self.subTest(parameter=name):
                self.promote()
                self.request["params"][name] = value
                self.caps["parameters"][name] = {}
                self.rehash()
                self.assertEqual(
                    validation.capability_findings(self.request, self.caps), []
                )
                self.assertTrue(self.promotion_findings())

    def test_promotion_accepts_only_supported_output_settings_without_mutation(self):
        self.promote()
        output_settings = {
            "watermark": False,
            "return_last_frame": True,
            "execution_expires_after": 3600,
            "priority": 1,
            "safety_identifier": "fixture-safety",
        }
        self.request["params"].update(output_settings)
        self.caps["parameters"].update({name: {} for name in output_settings})
        self.rehash()
        before = copy.deepcopy(self.request)
        self.assertEqual(self.findings(), [])
        self.assertEqual(self.request, before)
        del self.caps["parameters"]["priority"]
        self.assertIn("model.supported_mode", {f.rule_id for f in self.findings()})

    def test_promotion_rejects_changed_reference_with_valid_hash_and_approval(self):
        reference = copy.deepcopy(self.request["references"][0])
        self.promote()
        (self.root / "image.png").write_bytes(b"new approved reference image")
        reference["sha256"] = self.hash("image.png")
        self.request["references"] = [reference]
        self.rehash()
        self.assertEqual(validation.capability_findings(self.request, self.caps), [])
        self.assertEqual(
            {f.rule_id for f in self.findings()}, {"seedance.draft_promotion_source"}
        )

    def test_promotion_rejects_changed_reference_role_with_valid_capabilities(self):
        reference = copy.deepcopy(self.request["references"][0])
        self.promote()
        reference["role"] = "first_frame"
        self.request["references"] = [reference]
        self.rehash()
        self.assertEqual(validation.capability_findings(self.request, self.caps), [])
        self.assertTrue(self.promotion_findings())

    def test_request_without_references_still_fails_prompt_bindings(self):
        self.request["references"] = []
        self.rehash()
        self.assertTrue(self.ordered_binding_findings())

    def test_blank_draft_task_id_is_not_a_promotion(self):
        self.promote(task_id="  ")
        self.assertTrue(self.ordered_binding_findings())

    def test_promotion_with_partial_references_still_fails_bindings(self):
        reference = copy.deepcopy(self.request["references"][0])
        (self.root / "prompt.md").write_text("Walks past @Image 1 and @Image 2.\n")
        self.request["prompt_sha256"] = self.hash("prompt.md")
        self.promote()
        self.request["references"] = [reference]
        self.caps["parameters"]["draft_task_id"] = {"type": "string"}
        self.rehash()
        self.assertTrue(self.ordered_binding_findings())

    def test_promotion_with_recorded_references_still_checks_their_hashes(self):
        reference = copy.deepcopy(self.request["references"][0])
        self.promote()
        self.request["references"] = [reference]
        self.rehash()
        self.assertEqual(self.findings(), [])
        (self.root / "image.png").write_bytes(b"changed image")
        self.assertIn("references.current_hashes", {f.rule_id for f in self.findings()})

    def test_promotion_of_draft_selected_by_decision_passes(self):
        self.promote(review_status="review")
        self.select_draft_take()
        self.assertEqual(self.findings(), [])

    def test_promotion_of_unknown_draft_id_is_refused(self):
        self.promote(task_id="cgt-draft-typo")
        self.assertTrue(self.promotion_findings())
        self.assertTrue(self.ordered_binding_findings())

    def test_promotion_without_task_registry_is_refused(self):
        self.promote()
        (self.root / "task_ids.json").unlink()
        self.assertTrue(self.promotion_findings())

    def test_promotion_with_invalid_registry_reports_a_finding(self):
        self.promote()
        for content in ["not json", "[]", '{"schema_version": 1, "tasks": [{}]}']:
            with self.subTest(content=content):
                (self.root / "task_ids.json").write_text(content)
                self.assertTrue(self.promotion_findings())

    def test_promotion_of_non_draft_task_is_refused(self):
        cases = {
            "final render": {"params": {"resolution": "1080p", "duration": 5}},
            "720p draft": {"params": {"draft": True, "resolution": "720p"}},
            "draft flag as text": {"params": {"draft": "true", "resolution": "480p"}},
            "other model": {"model": "dreamina-seedance-2-0-260128"},
            "other 2.5 variant": {"model": "dreamina-seedance-2-5-premium-260915"},
        }
        for name, changes in cases.items():
            with self.subTest(name):
                self.promote(**changes)
                self.assertTrue(self.promotion_findings())
                self.assertTrue(self.ordered_binding_findings())

    def test_promotion_of_unreviewed_draft_is_refused(self):
        for status in ["not_started", "review", "rejected"]:
            with self.subTest(status=status):
                self.promote(review_status=status)
                self.assertTrue(self.promotion_findings())

    def test_promotion_of_draft_with_stale_selection_is_refused(self):
        self.promote(review_status="review")
        self.select_draft_take()
        (self.root / "draft.mp4").write_bytes(b"replaced draft video")
        self.assertTrue(self.promotion_findings())

    def test_selection_of_another_take_does_not_approve_the_draft(self):
        self.promote(
            review_status="review", extensions={"expected_output": "other.mp4"}
        )
        self.select_draft_take()
        self.assertTrue(self.promotion_findings())

    def test_promotion_prompt_must_match_the_draft_prompt(self):
        self.promote()
        (self.root / "prompt.md").write_text("A performer runs beside @Image 1.\n")
        self.request["prompt_sha256"] = self.hash("prompt.md")
        self.rehash()
        rules = {finding.rule_id for finding in self.findings()}
        self.assertIn("seedance.draft_promotion_source", rules)
        self.assertNotIn("prompt.current_hash", rules)

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
