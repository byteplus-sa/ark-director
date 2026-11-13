import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FamilyEvidenceTests(unittest.TestCase):
    def test_focus_tape_and_light_observations_are_scoped(self):
        for relative in (
            "seedance-lens-presets/SKILL.md",
            "seedance-lighting-presets/SKILL.md",
            "seedance-shot-design/SKILL.md",
            "seedance-prompt-25/references/audio-performance-camera.md",
        ):
            with self.subTest(path=relative):
                text = (ROOT / ".agents/skills" / relative).read_text()
                self.assertIn("historical", text.lower())
                self.assertIn("not a family", text.lower())
                self.assertIn("authorization", text.lower())
        lens = (ROOT / ".agents/skills/seedance-lens-presets/SKILL.md").read_text()
        self.assertNotIn("**Post only**", lens)

    def test_conform_guidance_is_artifact_specific_and_handles_unknown_tags(self):
        for relative in ("color-grade-palettes/SKILL.md",
                         "film-production/references/production-defaults.md"):
            with self.subTest(path=relative):
                text = (ROOT / ".agents/skills" / relative).read_text()
                for term in ("pixel format", "range", "primaries", "transfer", "matrix",
                             "unknown", "conflicting"):
                    self.assertIn(term, text.lower())
                self.assertNotIn("Seedance 2.5 finals are 10-bit HEVC", text)


if __name__ == "__main__":
    unittest.main()
