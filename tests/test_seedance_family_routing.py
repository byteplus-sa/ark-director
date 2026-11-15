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

    def test_consolidated_skill_preserves_exact_model_boundaries(self):
        text = (ROOT / ".agents/skills/seedance-prompt/SKILL.md").read_text()
        self.assertIn("name: seedance-prompt", text)
        self.assertIn("exact model", text.lower())
        self.assertIn("model-boundaries.md", text)
        boundaries = (ROOT / ".agents/skills/seedance-prompt/references/model-boundaries.md")
        self.assertIn("unknown", boundaries.read_text().lower())

    def test_family_leaf_remains_prompt_only_for_unknown_and_image_requests(self):
        text = " ".join(
            (ROOT / ".agents/skills/seedance-prompt/SKILL.md").read_text().split()
        )
        for term in ("image prompts", "unknown"):
            self.assertIn(term.lower(), text.lower())
        self.assertRegex(text.lower(), r"does not[^.]*\bsubmit\b")
        self.assertTrue((ROOT / ".claude/skills/seedance-prompt").is_symlink())


if __name__ == "__main__":
    unittest.main()
