import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = "seed-audio-15-prompt"
BUNDLE = ROOT / ".agents/skills" / NAME
EXPECTED_FILES = {
    "SKILL.md",
    "references/api-rules.md",
    "references/sound-writing-guide.md",
    "references/troubleshooting.md",
}


class SeedAudio15PromptTests(unittest.TestCase):
    def test_complete_prompt_only_bundle_is_installed(self):
        actual = {
            str(path.relative_to(BUNDLE))
            for path in BUNDLE.rglob("*") if path.is_file()
        }
        self.assertEqual(actual, EXPECTED_FILES)

    def test_metadata_scopes_the_skill_to_explicit_audio_15_requests(self):
        text = (BUNDLE / "SKILL.md").read_text()
        self.assertRegex(text, rf"(?m)^name: {NAME}$")
        description = re.search(r"(?m)^description: (.+)$", text)
        self.assertIsNotNone(description)
        self.assertIn("explicitly selected 1.5", description.group(1))
        self.assertIn('skill_version: "1.4.2"', text)
        self.assertIn("source_skill_name: seedaudio-prompt-optimizer", text)

    def test_prompt_use_never_runs_an_updater_or_claims_asset_inspection(self):
        text = (BUNDLE / "SKILL.md").read_text()
        self.assertNotRegex(text, r"\bnpx\b|skills@|seed-audio-1-5-pe")
        self.assertIn("Do not run package managers", text)
        self.assertIn("Optimize text only: do not call APIs", text)
        self.assertIn("Never claim to have watched a video or listened", text)
        self.assertIn("not independently", text)

    def test_references_are_self_contained_and_no_private_urls_are_shipped(self):
        documents = sorted(BUNDLE.rglob("*.md"))
        self.assertEqual(len(documents), 4)
        for document in documents:
            text = document.read_text()
            with self.subTest(document=document.name):
                self.assertNotRegex(
                    text, r"(?:larkoffice|larksuite|feishu)\.(?:com|cn)|/(?:Users|home)/"
                )
                for target in re.findall(r"\]\(([^)]+)\)", text):
                    if "://" in target or target.startswith("#"):
                        continue
                    destination = (document.parent / target.split("#")[0]).resolve()
                    self.assertTrue(destination.is_relative_to(BUNDLE.resolve()))
                    self.assertTrue(destination.is_file(), target)

    def test_provisional_limits_and_preservation_failure_cases_remain_explicit(self):
        rules = (BUNDLE / "references/api-rules.md").read_text()
        troubleshooting = (BUNDLE / "references/troubleshooting.md").read_text()
        self.assertIn("not independently verified", rules)
        self.assertIn("360 seconds", rules)
        self.assertNotIn("The user has explicitly confirmed", rules)
        for concept in (
            "Missing core content",
            "Hard timing conflict",
            "quote anchors",
            "do not silently drop reference seven",
            "locked punctuation",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept.lower(), troubleshooting.lower() + rules.lower())

    def test_routing_keeps_existing_audio_defaults_and_manual_maintenance(self):
        agents = " ".join((ROOT / "AGENTS.md").read_text().split())
        readme = (ROOT / "README.md").read_text()
        self.assertIn(f"`{NAME}` only for explicitly selected Seed Audio 1.5", agents)
        self.assertIn("existing audio skills and defaults unchanged", agents)
        self.assertIn("outside automated sync allowlists", agents)
        self.assertEqual(len(re.findall(rf"(?m)^\| \*\*{NAME}\*\* \|", readme)), 1)
        self.assertIn("| **seed-audio-prompt** |", readme)
        self.assertTrue((ROOT / ".agents/skills/seed-audio-prompt/SKILL.md").is_file())

    def test_claude_alias_resolves_to_the_project_bundle(self):
        alias = ROOT / ".claude/skills" / NAME
        self.assertTrue(alias.is_symlink())
        self.assertEqual(str(alias.readlink()), f"../../.agents/skills/{NAME}")
        self.assertEqual(alias.resolve(), BUNDLE.resolve())
        self.assertTrue((alias / "SKILL.md").is_file())

    def test_production_catalogs_record_the_adaptation_and_bundle_hashes(self):
        catalog_path = ROOT / ".agents/catalog/skills.json"
        if not catalog_path.exists():
            self.skipTest("Prompt-only workspace has no production catalog")
        catalog = json.loads(catalog_path.read_text())["skills"][NAME]
        lock = json.loads((ROOT / "skills-lock.json").read_text())["skills"][NAME]
        inventory = json.loads((ROOT / ".agents/catalog/integrity.json").read_text())["files"]
        self.assertEqual(catalog["kind"], "leaf")
        self.assertEqual(catalog["dependencies"], [])
        self.assertIn("user-supplied", lock["sourceNotes"])
        self.assertIn("1.4.2", lock["sourceNotes"])
        self.assertEqual(lock["skillPath"], f".agents/skills/{NAME}/SKILL.md")
        self.assertEqual(lock["computedHash"], hashlib.sha256((BUNDLE / "SKILL.md").read_bytes()).hexdigest())
        for relative in EXPECTED_FILES:
            path = BUNDLE / relative
            self.assertEqual(
                inventory[str(path.relative_to(ROOT))],
                hashlib.sha256(path.read_bytes()).hexdigest(),
            )


if __name__ == "__main__":
    unittest.main()
