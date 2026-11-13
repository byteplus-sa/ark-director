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

    def test_delegated_sound_routes_preserve_all_selected_owners(self):
        for name in ("slot-mapping.md", "long-pins-and-multi-clip.md"):
            with self.subTest(reference=name):
                text = " ".join((SKILLS / "template-factory/references" / name)
                                .read_text().lower().split())
                for owner in ("native", "post", "exact-master", "mixed", "silent"):
                    self.assertIn(f"| {owner} |", text)
                for term in ("wordless", "synchronized clicks", "purposeful silence",
                             "unresolved", "listening", "separate sound is opt-in"):
                    self.assertIn(term, text)
                self.assertNotIn("native only for on-camera dialogue", text)
                self.assertNotIn("score-led or ambient, generate picture with", text)

    def test_strict_restyle_review_accepts_words_only_without_probe_or_rounding(self):
        text = " ".join((SKILLS / "prompt-review/references/checklist-seedance-edits.md")
                        .read_text().lower().split())
        for term in ("words-only", "optional", "same place", "full-frame",
                     "fractional", "denied", "unresolved", "explicit approval"):
            self.assertIn(term, text)
        self.assertNotIn("the request is a 480p probe", text)
        self.assertNotIn("route a uses 1–5 images", text)
        self.assertNotIn("whole-second source duration", text)
        self.assertNotIn("restyled through an environment image of that place, or left", text)

    def test_delegated_scenarios_cover_sound_tails_and_strict_restyle(self):
        cases_by_skill = {
            "template-factory": {
                16: ("native", "wordless", "synchronized clicks", "listening"),
                17: ("mixed", "exact-master", "offsets", "post"),
                18: ("silent", "purposeful silence", "no bed"),
                19: ("5.125", "5.600", "tail", "approval"),
                20: ("shorter", "offsets", "unchanged", "approval"),
            },
            "seedance-vfx-pipeline": {
                5: ("strict", "words-only", "same place", "fractional", "denied"),
                6: ("unresolved", "no probe", "unknown", "prompt-only"),
                7: ("optional", "environment", "selected", "photographic"),
            },
        }
        for name, cases in cases_by_skill.items():
            document = json.loads((SKILLS / name / "evals/evals.json").read_text())
            by_id = {case["id"]: case for case in document["evals"]}
            for case_id, terms in cases.items():
                with self.subTest(skill=name, case=case_id):
                    self.assertIn(case_id, by_id)
                    case = by_id[case_id]
                    text = " ".join((" ".join(case["assertions"]) + " "
                                     + case["expected_output"]).lower().split())
                    for term in terms:
                        self.assertIn(term, text)
                    self.assertIn("no media or generation", text)
                    self.assertEqual(case["files"], [])

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
