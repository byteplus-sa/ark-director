import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".agents/scripts"))
from validate_workspace import validate_skill

SKILLS = ROOT / ".agents/skills"
PROMPT = SKILLS / "seedance-prompt"
RETIRED = ("seedance-prompt-20", "seedance-prompt-25")
RETIRED_PATTERN = re.compile(r"seedance-prompt-(?:20|25)(?![\w-])")


class PromptConsolidationTests(unittest.TestCase):
    def test_public_summaries_cover_consolidated_modes_without_edit_exclusion(self):
        catalog = json.loads((ROOT / ".agents/catalog/skills.json").read_text())
        summary = catalog["skills"]["seedance-prompt"]["readme_summary"]
        readme = (ROOT / "README.md").read_text()
        interface = YAML(typ="safe").load(
            (PROMPT / "agents/openai.yaml").read_text()
        )["interface"]
        for text in (summary, interface["short_description"]):
            for term in ("2.5-based", "edits", "extensions"):
                self.assertIn(term, text)
        self.assertIn(f"| **seedance-prompt** | {summary} |", readme)
        self.assertIn("reference", interface["default_prompt"])
        self.assertNotIn(
            "Do not use for image prompts, media execution, source-video edits",
            catalog["skills"]["seedance-prompt"]["description"],
        )

    def test_review_consumers_do_not_restore_retired_grammar_quotas(self):
        review = SKILLS / "prompt-review/references"
        legacy = (review / "checklist-seedance-legacy.md").read_text()
        for text in (
            legacy.split("## Seedance VFX", 1)[0],
            (review / "checklist-seedance-25.md").read_text(),
        ):
            self.assertNotIn("At most 3 major action beats", text)
            self.assertNotIn("Prompt assembles in this order", text)
            self.assertNotIn("in this order when present (MINOR)", text)
            self.assertIn("convention", text.lower())
            self.assertIn("exact model", text.lower())

    def test_callers_do_not_attribute_fixed_stage_quotas_to_generic_skill(self):
        for name in ("seedance-motion-design", "seedance-graybox-world"):
            text = " ".join((SKILLS / name / "SKILL.md").read_text().split())
            self.assertNotRegex(text, r"(?:one primary event|full motion grammar)")
            self.assertNotIn("<one event and visible end state>", text)

    def test_review_does_not_authorize_reference_substitution_or_fixed_duration(self):
        text = " ".join(
            (SKILLS / "prompt-review/references/checklist-seedance-25.md")
            .read_text().split()
        )
        self.assertNotIn("use the full sheet or a first frame", text)
        self.assertNotIn("natural length (4-30 s)", text)
        self.assertIn("independent", text)
        self.assertIn("authorization", text)
        self.assertIn("selected exact", text)

    def test_migrated_evaluations_keep_format_and_look_optional(self):
        document = json.loads((PROMPT / "evals/evals.json").read_text())
        cases = {case["id"]: case for case in document["evals"]}
        self.assertNotIn("includes a [Timeline Inheritance] section", json.dumps(cases[3]))
        self.assertNotIn("one grade", json.dumps(cases[8]))
        self.assertIn("locked", json.dumps(cases[8]))

    def test_progressive_change_reference_keeps_sibling_selection_caller_owned(self):
        text = (PROMPT / "references/scene-action.md").read_text().split(
            "## Progressive change", 1
        )[1]
        self.assertNotIn("compose with it", text)
        self.assertIn("caller", text)
        self.assertIn("does not load", text)

    def test_board_policy_is_local_and_preserves_planning_lineage(self):
        for name in ("keyframes-storyboards-blockouts", "parameter-reference"):
            with self.subTest(reference=name):
                text = " ".join(
                    (PROMPT / "references" / f"{name}.md").read_text().lower().split()
                )
                self.assertIn("workspace policy", text)
                self.assertIn("not", text)
                self.assertNotIn("output-copyright rejections rose", text)
                self.assertNotIn("output-copyright rejections rise", text)
        text = " ".join(
            (PROMPT / "references/keyframes-storyboards-blockouts.md").read_text().split()
        )
        self.assertIn("planning origin", text)
        self.assertIn("independently authored", text)

    def test_reference_guidance_keeps_structure_and_exclusions_optional(self):
        action = (PROMPT / "references/scene-action.md").read_text()
        staging = (PROMPT / "references/shot-staging.md").read_text()
        audio = (PROMPT / "references/audio-performance-camera.md").read_text()
        self.assertNotIn("Use stages by default", action)
        self.assertIn("Summarize", action)
        self.assertIn("once", action)
        self.assertIn("optional", staging.lower())
        self.assertNotIn("never what it should not show", audio)
        self.assertIn("Necessary exclusions", audio)

    def test_readme_skill_count_matches_installed_bundles(self):
        text = (ROOT / "README.md").read_text()
        declared = re.search(r"ships with \*\*(\d+) skills\*\*", text)
        self.assertIsNotNone(declared)
        self.assertEqual(int(declared.group(1)), len(list(SKILLS.glob("*/SKILL.md"))))

    def test_metadata_validation_rejects_retired_entrypoints_but_keeps_specialists(self):
        for name in (*RETIRED, "seedance-prompt", "seedance-prompt-25-filipino"):
            with self.subTest(skill=name), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / name / "SKILL.md"
                path.parent.mkdir()
                path.write_text(f"---\nname: {name}\ndescription: Prompt helper.\n---\n")
                _, findings = validate_skill(path)
                self.assertEqual(
                    any(finding.rule_id == "metadata.retired" for finding in findings),
                    name in RETIRED,
                )

    def test_only_general_entrypoint_and_resolving_alias_remain(self):
        for name in RETIRED:
            with self.subTest(skill=name):
                self.assertFalse((SKILLS / name).exists())
                self.assertFalse((ROOT / ".claude/skills" / name).is_symlink())
        alias = ROOT / ".claude/skills/seedance-prompt"
        self.assertTrue(alias.is_symlink())
        self.assertEqual(alias.resolve(), PROMPT)
        self.assertTrue((SKILLS / "seedance-prompt-25-filipino/SKILL.md").is_file())

    def test_current_catalog_lock_and_callers_have_no_retired_routes(self):
        paths = [ROOT / "AGENTS.md", ROOT / "README.md", ROOT / "skills-lock.json"]
        for directory in (ROOT / ".agents/catalog", ROOT / ".agents/contracts"):
            paths.extend(directory.rglob("*.json"))
            paths.extend(directory.rglob("*.md"))
        paths.extend(SKILLS.rglob("*.md"))
        paths.extend(SKILLS.rglob("*.json"))
        paths.extend(SKILLS.rglob("*.yaml"))
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIsNone(RETIRED_PATTERN.search(path.read_text()))

    def test_all_prompt_modes_ship_as_same_skill_references(self):
        names = (
            "audio-performance-camera", "keyframes-storyboards-blockouts",
            "parameter-reference", "reference-inputs", "repair-examples",
            "scene-action", "shot-staging", "transitions-and-one-click",
            "video-editing", "video-extension", "worked-examples",
        )
        for name in names:
            with self.subTest(reference=name):
                path = PROMPT / "references" / f"{name}.md"
                self.assertTrue(path.is_file())
                self.assertGreater(len(path.read_text()), 500)
                self.assertIn(
                    f"(references/{name}.md)", (PROMPT / "SKILL.md").read_text()
                )

    def test_evals_preserve_all_three_bundles_with_unique_identifiers(self):
        document = json.loads((PROMPT / "evals/evals.json").read_text())
        self.assertEqual(document["skill_name"], "seedance-prompt")
        cases = document["evals"]
        self.assertEqual(len(cases), 36)
        self.assertEqual(len({case["id"] for case in cases}), len(cases))
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(case["prompt"])
                self.assertTrue(case["expected_output"])
                self.assertTrue(case["expectations"])
        for scenario in ("tree line", "Timeline Inheritance", "backward",
                         "empty", "Flash", "7.37", "three hand actions"):
            self.assertIn(scenario, json.dumps(cases))
        creative = json.loads((PROMPT / "evals/creative-freedom.json").read_text())
        self.assertEqual(creative["skill_name"], "seedance-prompt")
        self.assertEqual({case["id"] for case in creative["evals"]}, set(range(201, 211)))
        self.assertFalse({case["id"] for case in creative["evals"]}
                         & {case["id"] for case in cases})

    def test_edit_guidance_preserves_fractional_timing_and_authorization(self):
        text = " ".join((PROMPT / "references/video-editing.md").read_text().lower().split())
        for concept in ("sole editing master", "occlusion", "fractional", "audio tail",
                        "no trimming", "authorization", "unknown", "exact model"):
            self.assertIn(concept, text)

    def test_reference_limits_and_language_are_not_generic_guarantees(self):
        for name in ("reference-inputs", "audio-performance-camera",
                     "transitions-and-one-click", "keyframes-storyboards-blockouts"):
            with self.subTest(reference=name):
                text = (PROMPT / "references" / f"{name}.md").read_text().lower()
                self.assertIn("exact model", text)
                self.assertIn("convention", text)
        parameters = (PROMPT / "references/parameter-reference.md").read_text()
        self.assertNotIn("Fall back to", parameters)
        self.assertNotIn("Prototype on Mini", parameters)
        self.assertNotIn("10+ languages supported natively", parameters)
        self.assertNotIn("For 4K output follow", parameters)
        self.assertNotIn("For other models without native Draft support", parameters)
        self.assertIn("preview resolution", parameters)
        self.assertIn("does not select", parameters)


if __name__ == "__main__":
    unittest.main()
