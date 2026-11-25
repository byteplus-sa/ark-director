import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ArkMcpGlobalSkillTests(unittest.TestCase):
    def test_workspace_does_not_shadow_the_global_skill(self):
        for directory in (".agents", ".claude", ".trae", ".codex", ".opencode"):
            path = ROOT / directory / "skills/ark-mcp"
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertFalse(path.exists())
                self.assertFalse(path.is_symlink())

    def test_local_metadata_does_not_claim_the_global_bundle(self):
        for relative in ("skills-lock.json", ".agents/catalog/skills.json"):
            path = ROOT / relative
            if not path.is_file():
                continue
            with self.subTest(path=relative):
                self.assertNotIn("ark-mcp", json.loads(path.read_text())["skills"])
        inventory = ROOT / ".agents/catalog/integrity.json"
        if inventory.is_file():
            self.assertFalse(any(
                path.startswith(".agents/skills/ark-mcp/")
                for path in json.loads(inventory.read_text())["files"]
            ))
        self.assertFalse((ROOT / ".agents/catalog/ark-mcp-LICENSE").exists())

    def test_global_guidance_preserves_repository_authority_and_missing_skill_handling(self):
        for relative in ("AGENTS.md", "README.md"):
            with self.subTest(path=relative):
                text = " ".join((ROOT / relative).read_text().split())
                self.assertIn("~/.agents/skills/ark-mcp/SKILL.md", text)
                self.assertIn("Repository contracts remain authoritative", text)
                self.assertIn("If the global skill is missing", text)
                self.assertIn("does not configure or connect", text)
                self.assertNotIn("| **ark-mcp** |", text)

    def test_remaining_project_skills_keep_resolving_claude_aliases(self):
        for alias in sorted((ROOT / ".claude/skills").iterdir()):
            with self.subTest(skill=alias.name):
                self.assertTrue(alias.is_symlink())
                self.assertEqual(alias.resolve(), (ROOT / ".agents/skills" / alias.name).resolve())
                self.assertTrue((alias / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
