import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents/skills"


class FamilyContractTests(unittest.TestCase):
    def test_wordless_sound_ownership_is_explicit_in_each_consumer(self):
        for name in ("film-production", "template-factory", "ugc-ad-modes",
                     "ugc-motion-presets", "seedance-music-video"):
            with self.subTest(skill=name):
                text = (SKILLS / name / "SKILL.md").read_text()
                self.assertIn("sound ownership", text)
                self.assertIn("purposeful silence", text.lower())
                self.assertNotIn("or ambience-only result set", text)

    def test_motion_design_does_not_bind_board_panels(self):
        text = (SKILLS / "seedance-motion-design/SKILL.md").read_text()
        self.assertNotIn("<approved storyboard / keyframe>", text)
        self.assertNotIn("Approved storyboard panels / keyframes", text)
        for term in ("planning-only", "clean keyframe", "current hash", "ordered"):
            self.assertIn(term, text)

    def test_voice_material_remains_local_until_active_authorization(self):
        text = (SKILLS / "seedance-ai-avatar/references/voice-reference.md").read_text()
        self.assertIn("local onboarding/QA", text)
        self.assertIn("Active", text)
        self.assertIn("not a Seedance request fallback", " ".join(text.split()))
        self.assertNotIn("@Audio 1 defines", text)

    def test_partial_probes_are_optional_and_full_timing_is_preserved(self):
        text = (SKILLS / "seedance-vfx-pipeline/SKILL.md").read_text()
        self.assertNotIn("a 480p key-beat probe before each final", text)
        self.assertIn("explicit span and generation-scope approval", text)
        reference = (SKILLS / "seedance-vfx-pipeline/references/recast-and-variants.md").read_text()
        for term in ("fractional", "final word", "audio tail", "optional"):
            self.assertIn(term, reference)
        self.assertIn("words-only", reference)

    def test_authored_evals_include_failure_and_scope_cases(self):
        for name in ("film-production", "template-factory", "seedance-motion-design",
                     "seedance-ai-avatar", "seedance-vfx-pipeline"):
            with self.subTest(skill=name):
                document = json.loads((SKILLS / name / "evals/evals.json").read_text())
                cases = document["evals"]
                self.assertEqual(len({case["id"] for case in cases}), len(cases))
                self.assertTrue(all(case["prompt"] and case["expected_output"] for case in cases))
                self.assertTrue(any("unresolved" in case["expected_output"].lower()
                                    or "reject" in case["expected_output"].lower()
                                    or "stop" in case["expected_output"].lower()
                                    for case in cases))


if __name__ == "__main__":
    unittest.main()
