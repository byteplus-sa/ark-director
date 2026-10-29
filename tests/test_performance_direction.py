"""Integration contracts and synthetic review gates, not generated-media QA."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents/skills"
sys.path.insert(0, str(ROOT / ".agents/scripts"))

import operation_store
import validate_request as validation
import validate_workspace as workspace

RENAMES = {"tig-scene-engine": "scene-craft", "tig-blocking-map": "blocking-map"}
NEW_SKILLS = ("acting-direction", "seedance-fight-choreography")
RULES = ("acting.plan_bound", "fight.readable_exchange")


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def prose(relative: str) -> str:
    return " ".join(read(relative).split()).lower()


class PerformanceIntegrationTests(unittest.TestCase):
    def test_performance_applicability_is_independent_of_review_depth(self):
        contract = prose(".agents/contracts/performance-direction.md")
        self.assertIn("both review modes", contract)
        self.assertIn("default", contract)
        self.assertIn("strict", contract)
        self.assertIn("--required-rule", contract)

    def test_metadata_adapters_and_relative_symlinks_use_current_names(self):
        catalog = json.loads(read(".agents/catalog/skills.json"))["skills"]
        lock = json.loads(read("skills-lock.json"))["skills"]
        rows = dict(re.findall(
            r"^\| \*\*([^*]+)\*\* \| (.*) \|$", read("README.md"), re.MULTILINE,
        ))
        for old in RENAMES:
            self.assertNotIn(old, catalog)
            self.assertNotIn(old, lock)
            for parent in (SKILLS, ROOT / ".claude/skills"):
                self.assertFalse((parent / old).exists())
                self.assertFalse((parent / old).is_symlink())
        for name in (*RENAMES.values(), *NEW_SKILLS, "seedance-acting-console"):
            with self.subTest(skill=name):
                entry = SKILLS / name / "SKILL.md"
                metadata, findings = workspace.validate_skill(entry)
                self.assertEqual(findings, [])
                self.assertEqual(metadata["name"], name)
                self.assertEqual(catalog[name]["description"], metadata["description"])
                self.assertEqual(catalog[name]["kind"], "leaf")
                self.assertEqual(catalog[name]["source_revision"], "workspace")
                self.assertIsNone(catalog[name]["upstream_hash"])
                self.assertEqual(catalog[name]["dependencies"], [])
                self.assertEqual(lock[name]["source"], "./local")
                self.assertEqual(lock[name]["sourceType"], "local")
                self.assertEqual(lock[name]["skillPath"], str(entry.relative_to(ROOT)))
                self.assertEqual(rows[name], catalog[name]["readme_summary"])
                link = ROOT / ".claude/skills" / name
                self.assertTrue(link.is_symlink())
                self.assertEqual(link.readlink(), Path("../../.agents/skills") / name)
                self.assertEqual(link.resolve(), entry.parent)
                adapter = YAML(typ="safe").load((entry.parent / "agents/openai.yaml").read_text())
                self.assertIn(f"${name}", adapter["interface"]["default_prompt"])
                eval_path = entry.parent / "evals/evals.json"
                self.assertEqual(json.loads(eval_path.read_text())["skill_name"], name)
                self.assertTrue(workspace.load_evaluations(eval_path))

    def test_new_skill_sources_are_attributed_without_external_hash_claims(self):
        lock = json.loads(read("skills-lock.json"))["skills"]
        sources = {
            "acting-direction": "higgsfield-acting-skill.skill",
            "seedance-fight-choreography": "higgsfield-fight-scene.skill",
        }
        for name, source in sources.items():
            with self.subTest(skill=name):
                self.assertIn(source, lock[name]["sourceNotes"])
                self.assertIn("prompt-only", lock[name]["sourceNotes"])
                self.assertRegex(lock[name]["computedHash"], r"^[0-9a-f]{64}$")
                self.assertNotIn("upstreamHash", lock[name])
        self.assertIn("Tigran", lock["acting-direction"]["sourceNotes"])

    def test_old_names_are_absent_from_runtime_routes(self):
        paths = [ROOT / "AGENTS.md", ROOT / "README.md"]
        for directory in (".agents/skills", ".agents/contracts", ".agents/scripts"):
            paths.extend(
                path for path in (ROOT / directory).rglob("*")
                if path.is_file() and path.suffix in {".md", ".py", ".yaml", ".json"}
                and path.name != "source-notes.md"
            )
        stale = [
            f"{path.relative_to(ROOT)}:{number}: {old}"
            for path in paths
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
            for old in RENAMES if old in line
        ]
        self.assertEqual(stale, [], "\n".join(stale))

    def test_ark_ugc_motion_and_production_tools_remain_available(self):
        retained = {
            "ugc-ad-modes", "ugc-motion-presets", "seedance-motion-design",
            "seedance-motion-recast", "seedance-music-video", "seedance-effects-studio",
            "seedance-vfx-pipeline", "blender-to-seedance", "general-video",
        }
        for path in (".agents/catalog/skills.json", "skills-lock.json"):
            self.assertTrue(retained <= set(json.loads(read(path))["skills"]))
        for name in retained:
            self.assertTrue((SKILLS / name / "SKILL.md").is_file())

    def test_ark_spanish_timing_case_and_cinema_plan_case_have_unique_ids(self):
        cases = workspace.load_evaluations(SKILLS / "seedance-acting-console/evals/evals.json")
        self.assertEqual(len(cases), len({case["id"] for case in cases}))
        spanish = next(case for case in cases if case["id"] == 12)
        self.assertIn("3.4 s", spanish["prompt"])
        self.assertIn("1.1 s tail", spanish["expected_output"])
        handoff = next(case for case in cases if "Encode only shot sh030" in case["prompt"])
        self.assertNotEqual(handoff["id"], 12)

    def test_motion_ratios_and_repeated_holds_are_not_compulsory(self):
        design = prose(".agents/skills/seedance-shot-design/SKILL.md")
        self.assertIn("motion ratios are optional planning aids, not quotas", design)
        self.assertIn("repeated stillness is valid", design)
        checklist = prose(".agents/skills/prompt-review/references/checklist-seedance-25.md")
        self.assertNotIn("at most one `performance_hold`", checklist)
        self.assertNotIn("more than a third of the shots is major", checklist)
        self.assertIn("intentional stillness", checklist)
        repairs = prose(".agents/skills/seedance-shot-design/references/coverage-patterns.md")
        self.assertIn("none of these shapes is a defect by itself", repairs)
        self.assertNotIn("uneven durations; give the turn", repairs)
        cases = workspace.load_evaluations(SKILLS / "seedance-shot-design/evals/evals.json")
        for case in cases:
            expectations = " ".join(case["assertions"]).lower()
            self.assertNotIn("shot lengths are uneven (not all within 20%", expectations)
            self.assertNotIn("flags one shot as the turn", expectations)

    def test_both_orchestrators_route_performance_and_require_semantic_checks(self):
        for name in ("film-production", "micro-drama"):
            with self.subTest(orchestrator=name):
                document = read(f".agents/skills/{name}/SKILL.md")
                for skill in (*NEW_SKILLS, "scene-craft", "seedance-acting-console"):
                    self.assertIn(f"`{skill}`", document)
                for rule in RULES:
                    self.assertIn(f"`{rule}`", document)
                self.assertIn("## Performance plan", document)
                self.assertIn("performance-direction.md", document)
                self.assertRegex(
                    " ".join(document.split()),
                    r"`acting-direction`.{0,100}before (?:shot design|coverage)",
                )
        policy = read(".agents/contracts/production-policy.md")
        for token in (*NEW_SKILLS, *RULES, "performance-direction.md"):
            self.assertIn(token, policy)

    def test_semantic_rules_have_valid_owners_and_checklist_entries(self):
        rules = json.loads(read(".agents/contracts/rules.json"))["rules"]
        checklist = read(".agents/skills/prompt-review/references/checklist-seedance-25.md")
        contract = read(".agents/contracts/performance-direction.md")
        for rule_id in RULES:
            with self.subTest(rule=rule_id):
                matches = [rule for rule in rules if rule["id"] == rule_id]
                self.assertEqual(len(matches), 1)
                rule = matches[0]
                self.assertEqual(rule["severity"], "error")
                self.assertIn("narrative_video", rule["applies_to"])
                self.assertEqual(rule["owner_path"], ".agents/contracts/performance-direction.md")
                self.assertTrue((ROOT / rule["owner_path"]).is_file())
                self.assertTrue(rule["exceptions"])
                self.assertIn(f"`{rule_id}`", checklist)
                self.assertIn(f"`{rule_id}`", contract)
        self.assertIn("--required-rule", contract)

    def test_framework_restraint_and_preservation_are_explicit_contracts(self):
        scene = prose(".agents/skills/scene-craft/SKILL.md")
        self.assertRegex(scene, r"five definitions.{0,100}only when.{0,30}selected")
        self.assertRegex(scene, r"missing engine elements.{0,40}not universal")
        self.assertRegex(scene, r"preserve.{0,60}quiet holds")
        self.assertRegex(scene, r"without imposing.{0,120}mandatory reaction close-up")
        contract = prose(".agents/contracts/performance-direction.md")
        self.assertRegex(contract, r"source-preserving edits inherit performance")
        self.assertIn("`may_change`", contract)
        self.assertRegex(contract, r"non-response.{0,100}instead of requiring")
        self.assertRegex(contract, r"static images.{0,100}do not need an acting plan")
        console = prose(".agents/skills/seedance-acting-console/SKILL.md")
        self.assertRegex(console, r"fewer cues.{0,60}minimal action")
        self.assertRegex(console, r"preserve the framing.{0,40}do not uncover")

    def test_eval_specs_retain_optional_framework_and_preservation_scenarios(self):
        coverage = {
            "scene-craft": (r"observational", r"not picked.{0,30}framework"),
            "acting-direction": (r"observational", r"relight.{0,100}unchanged"),
            "seedance-acting-console": (r"source-preserving", r"unconscious"),
        }
        for name, scenarios in coverage.items():
            cases = workspace.load_evaluations(SKILLS / name / "evals/evals.json")
            for scenario in scenarios:
                with self.subTest(skill=name, scenario=scenario):
                    matches = [
                        case for case in cases
                        if re.search(scenario, case["prompt"], re.IGNORECASE)
                    ]
                    self.assertTrue(matches)
                    for case in matches:
                        self.assertTrue(case["expected_output"])
                        self.assertTrue(case["assertions"])


class PerformanceReviewGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="performance-gate-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "studio").mkdir()
        (self.root / "project.md").write_text("---\napproval_mode: approve_for_me\n---\n")
        prompt = b"Fictional A steps aside; B stops and waits in a held wide shot.\n"
        (self.root / "prompt.md").write_bytes(prompt)
        self.request = {
            "schema_version": 2,
            "operation_id": "performance-fixture-v01",
            "asset_id": "s01_sh010_t01_v01",
            "transport": "ark-mcp",
            "model": "dreamina-seedance-2-5-260628",
            "operation": "generate",
            "approval_mode": "approve_for_me",
            "project_sha256": hashlib.sha256((self.root / "project.md").read_bytes()).hexdigest(),
            "prompt_file": "prompt.md",
            "prompt_sha256": hashlib.sha256(prompt).hexdigest(),
            "references": [],
            "params": {"resolution": "480p", "draft": True, "duration": 5},
            "submission_status": "prepared",
            "provider_task_id": None,
            "provider_status": None,
            "review_status": "not_started",
            "cost": {"estimated": None, "confirmed": None, "currency": "USD"},
        }
        self.request["request_sha256"] = validation.compute_request_hash(
            prompt, [], self.request["model"], "generate", self.request["params"],
            approval_mode=self.request["approval_mode"],
            project_sha256=self.request["project_sha256"],
        )
        self.caps = {
            "model": self.request["model"],
            "source": "synthetic test schema, not live capability evidence",
            "verified_at": "2026-10-27T00:00:00Z",
            "operations": ["generate"],
            "parameters": {
                "resolution": {"enum": ["480p"]},
                "draft": {"const": True},
                "duration": {"type": "integer"},
            },
            "reference_roles": [],
            "max_references": 0,
        }
        self.review = {
            "schema_version": 1,
            "request_sha256": self.request["request_sha256"],
            "reviewer_status": "complete",
            "checks": [
                {"rule_id": rule, "status": "pass", "evidence": "Synthetic declared check."}
                for rule in RULES
            ],
        }
        self.assertEqual(validation.validate_request(self.root, self.request, self.caps), [])

    def prepare(self, review):
        operation_store.prepare_operation(
            self.root, self.request, self.caps, review, list(RULES),
        )

    def test_applicable_checks_are_binding_in_all_review_and_approval_modes(self):
        for review_mode in ("default", "strict"):
            for approval_mode in ("approve_for_me", "ask_for_approval"):
                with self.subTest(review=review_mode, approval=approval_mode):
                    (self.root / "project.md").write_text(
                        f"---\napproval_mode: {approval_mode}\n"
                        f"review_mode: {review_mode}\n---\n"
                    )
                    self.request.update(
                        approval_mode=approval_mode,
                        project_sha256=hashlib.sha256(
                            (self.root / "project.md").read_bytes()
                        ).hexdigest(),
                    )
                    self.request["request_sha256"] = validation.compute_request_hash(
                        (self.root / "prompt.md").read_bytes(), [],
                        self.request["model"], "generate", self.request["params"],
                        approval_mode=approval_mode,
                        project_sha256=self.request["project_sha256"],
                    )
                    self.review["request_sha256"] = self.request["request_sha256"]
                    reports = [None, dict(self.review, checks=[])]
                    for status in ("fail", "not_applicable"):
                        reports.append(dict(
                            self.review,
                            checks=[dict(check, status=status) for check in self.review["checks"]],
                        ))
                    for report in reports:
                        with self.assertRaises(ValueError):
                            self.prepare(report)
                        self.assertFalse((self.root / "task_ids.json").exists())
                    self.prepare(self.review)
                    record = operation_store.read_registry(
                        self.root / "task_ids.json"
                    )["tasks"][0]
                    self.assertEqual(record["approval_mode"], approval_mode)
                    self.assertEqual(record["submission_status"], "prepared")
                    self.assertEqual(record["review_status"], "not_started")
                    (self.root / "task_ids.json").unlink()

    def test_required_performance_checks_pass_real_registration_without_submission(self):
        before = copy.deepcopy(self.request)
        self.assertEqual(
            validation.validate_review(self.review, self.request["request_sha256"], list(RULES)),
            [],
        )
        self.prepare(self.review)
        tasks = json.loads((self.root / "task_ids.json").read_text())["tasks"]
        self.assertEqual(tasks, [before])
        self.assertEqual(self.request, before)
        self.assertEqual(tasks[0]["submission_status"], "prepared")
        self.assertIsNone(tasks[0]["provider_task_id"])

    def test_missing_failed_skipped_or_empty_required_checks_block_registration(self):
        for index, rule in enumerate(RULES):
            for defect in ("missing", "fail", "not_applicable", "empty"):
                with self.subTest(rule=rule, defect=defect):
                    review = copy.deepcopy(self.review)
                    if defect == "missing":
                        review["checks"].pop(index)
                    elif defect == "empty":
                        review["checks"][index]["evidence"] = " "
                    else:
                        review["checks"][index]["status"] = defect
                    findings = validation.validate_review(
                        review, self.request["request_sha256"], list(RULES),
                    )
                    self.assertTrue(findings)
                    if defect == "missing":
                        self.assertTrue(any(
                            finding.rule_id == "review.complete_evidence"
                            and rule in finding.message for finding in findings
                        ))
                    else:
                        self.assertIn(rule, {finding.rule_id for finding in findings})
                    with self.assertRaises(ValueError):
                        self.prepare(review)
                    self.assertFalse((self.root / "task_ids.json").exists())

    def test_stale_incomplete_or_duplicate_review_cannot_register(self):
        for defect in ("stale", "incomplete", "duplicate"):
            with self.subTest(defect=defect):
                review = copy.deepcopy(self.review)
                if defect == "stale":
                    review["request_sha256"] = "0" * 64
                elif defect == "incomplete":
                    review["reviewer_status"] = "incomplete"
                else:
                    review["checks"].append(copy.deepcopy(review["checks"][0]))
                with self.assertRaises(ValueError):
                    self.prepare(review)
                self.assertFalse((self.root / "task_ids.json").exists())

    def test_non_applicable_checks_pass_only_when_not_required(self):
        for check in self.review["checks"]:
            check.update(
                status="not_applicable",
                evidence="Preservation-only relight; existing performance and exchange retained.",
            )
        self.assertEqual(
            validation.validate_review(self.review, self.request["request_sha256"], []),
            [],
        )
        self.assertEqual(
            {finding.rule_id for finding in validation.validate_review(
                self.review, self.request["request_sha256"], list(RULES),
            )},
            set(RULES),
        )


if __name__ == "__main__":
    unittest.main()
