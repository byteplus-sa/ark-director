import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FamilyRoutingTests(unittest.TestCase):
    def test_general_craft_callers_offer_neutral_creative_handoff(self):
        for name in ("scene-craft", "seedance-acting-console", "seedance-animation-styles",
                     "seedance-camera-presets", "seedance-motion-design",
                     "seedance-music-video", "seedance-pacing-presets", "seedance-shot-design"):
            with self.subTest(skill=name):
                text = (ROOT / ".agents/skills" / name / "SKILL.md").read_text()
                self.assertIn("`seedance-prompt`", text)
                self.assertIn("selected model", text)
                self.assertIn("caller", text.lower())

    def test_versioned_adapter_is_retained_with_exact_applicability(self):
        text = (ROOT / ".agents/skills/seedance-prompt-25/SKILL.md").read_text()
        self.assertIn("name: seedance-prompt-25", text)
        self.assertIn("versioned adapter", text)
        self.assertIn("not inherited", text)
        self.assertTrue((ROOT / ".agents/skills/seedance-prompt-20/SKILL.md").is_file())

    def test_family_leaf_remains_prompt_only_for_unknown_and_image_requests(self):
        text = (ROOT / ".agents/skills/seedance-prompt/SKILL.md").read_text()
        for term in ("image prompts", "unknown", "does not submit"):
            self.assertIn(term.lower(), text.lower())
        self.assertTrue((ROOT / ".claude/skills/seedance-prompt").is_symlink())


if __name__ == "__main__":
    unittest.main()
