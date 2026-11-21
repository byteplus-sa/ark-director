import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "workspace_validation", ROOT / ".agents/scripts/validate_workspace.py"
)
validation = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validation
SPEC.loader.exec_module(validation)


class WorkspaceValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / ".agents/skills/example/SKILL.md"
        self.skill.parent.mkdir(parents=True)
        self.skill.write_text(
            "---\nname: example\ndescription: A useful example.\n---\n# Example\n"
        )

    def test_valid_metadata_and_name(self):
        self.assertEqual(validation.validate_skill(self.skill)[1], [])

    def test_reviewed_integrity_matches_published_skill_files(self):
        portable_files = validation.read_inventory(ROOT, None)
        current = {
            relative: digest
            for relative, digest in validation.bundle_hashes(ROOT).items()
            if relative in portable_files
        }
        recorded = json.loads(
            (ROOT / ".agents/catalog/integrity.json").read_text()
        )["files"]
        mismatches = sorted(
            relative
            for relative in set(recorded) | set(current)
            if recorded.get(relative) != current.get(relative)
        )
        self.assertEqual(mismatches, [])

    def test_invalid_yaml_and_name_return_diagnostics(self):
        self.skill.write_text("---\nname: example\ndescription: invalid: value\n---\n")
        self.assertTrue(validation.validate_skill(self.skill)[1])
        self.skill.write_text("---\nname: different\ndescription: Example\n---\n")
        self.assertTrue(validation.validate_skill(self.skill)[1])

    def test_missing_and_untracked_runtime_reference_fail(self):
        doc = self.root / "AGENTS.md"
        doc.write_text("[Contract](.agents/contracts/policy.md)\n")
        findings = validation.validate_links(self.root, [doc], {"AGENTS.md"})
        self.assertTrue(findings)
        target = self.root / ".agents/contracts/policy.md"
        target.parent.mkdir(parents=True)
        target.write_text("# Policy\n")
        self.assertTrue(validation.validate_links(self.root, [doc], {"AGENTS.md"}))
        self.assertEqual(
            validation.validate_links(
                self.root, [doc], {"AGENTS.md", ".agents/contracts/policy.md"}
            ),
            [],
        )

    def test_example_code_links_are_not_runtime_dependencies(self):
        doc = self.root / "AGENTS.md"
        doc.write_text(
            "```markdown\n[Example](image_1)\n```\n[Web](https://example.com)\n"
        )
        self.assertEqual(validation.validate_links(self.root, [doc], {"AGENTS.md"}), [])

    def test_legacy_evaluation_expectations_load_without_rewriting(self):
        path = self.root / "evals.json"
        body = {
            "skill_name": "example",
            "evals": [{"id": 1, "prompt": "Do it", "expectations": ["Useful result"]}],
        }
        path.write_text(json.dumps(body))
        cases = validation.load_evaluations(path)
        self.assertEqual(cases[0]["assertions"], ["Useful result"])
        self.assertEqual(json.loads(path.read_text()), body)

    def test_invalid_eval_case_fails(self):
        path = self.root / "evals.json"
        path.write_text('{"evals": [{"id": 1, "prompt": ""}]}')
        with self.assertRaises(ValueError):
            validation.load_evaluations(path)


if __name__ == "__main__":
    unittest.main()
