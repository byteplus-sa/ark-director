import json
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / ".agents/skills/seedance-music-video"


def normalized(path):
    return " ".join(path.read_text(encoding="utf-8").lower().split())


class MusicCreativeFreedomPolicyTests(unittest.TestCase):
    def test_policy_has_no_universal_recipe_lock(self):
        forbidden = (
            r"genre lock",
            r"use one genre recipe",
            r"single recipe, not a mixture",
            r"pick one; never mix two",
            r"use this only when no preset matches",
            r"second genre's palette",
        )
        for path in sorted(SKILL.rglob("*.md")):
            with self.subTest(path=path.name):
                for pattern in forbidden:
                    self.assertNotRegex(normalized(path), pattern)

    def test_authoring_surfaces_allow_custom_hybrids_and_optional_summary(self):
        for relative in (
            "SKILL.md",
            "references/music-video-recipes.md",
            "references/output-templates.md",
            "references/specialized-formats.md",
        ):
            with self.subTest(path=relative):
                text = normalized(SKILL / relative)
                for term in ("brief", "custom", "hybrid", "transition", "optional"):
                    self.assertIn(term, text)
        text = normalized(SKILL / "SKILL.md")
        self.assertIn("source locks", text)
        self.assertIn("preservation-only", text)
        self.assertIn("incompatible", text)

    def test_templates_do_not_impose_numeric_shot_minima(self):
        for relative in (
            "references/output-templates.md",
            "references/specialized-formats.md",
        ):
            with self.subTest(path=relative):
                text = normalized(SKILL / relative)
                self.assertNotRegex(
                    text, r"at least\s*~?\s*\d+(?:\.\d+)?\s*s|roughly 1[\u2013-]3s"
                )
        self.assertIn("no numeric shot-duration floor",
                      normalized(SKILL / "references/output-templates.md"))

    def test_lyric_cadence_follows_phrase_instead_of_chorus_label(self):
        text = normalized(SKILL / "references/specialized-formats.md")
        self.assertNotIn("faster and tighter in the chorus", text)
        self.assertIn("cadence follows the actual phrase", text)
        self.assertIn("does not automatically require faster motion", text)

    def test_evaluations_are_structured_proposals_not_observed_results(self):
        data = json.loads((SKILL / "evals/evals.json").read_text())
        self.assertEqual(data["skill_name"], "seedance-music-video")
        cases = {case["id"]: case for case in data["evals"]}
        self.assertEqual(len(cases), len(data["evals"]))
        for case in cases.values():
            with self.subTest(case=case["id"]):
                self.assertTrue(case["prompt"].strip())
                self.assertTrue(case["expected_output"].strip())
                self.assertEqual(case["files"], [])
                self.assertGreaterEqual(len(case["expectations"]), 3)
                self.assertTrue(all(item.strip() for item in case["expectations"]))
                self.assertNotIn("observed_result", case)
                text = " ".join([case["expected_output"], *case["expectations"]])
                self.assertNotRegex(text.lower(), r"genre lock|single recipe")
                self.assertNotIn("/Users/", case["prompt"])

    def test_eval_coverage_pairs_freedom_with_preservation_and_input_errors(self):
        cases = {
            case["id"]: case
            for case in json.loads((SKILL / "evals/evals.json").read_text())["evals"]
        }
        required = {
            21: ("bright daylight", "rap", "rough"),
            22: ("acoustic", "kinetic", "choreography"),
            23: ("documentary", "surreal", "transition"),
            24: ("preserve", "camera", "mouth", "master"),
            25: ("no audio", "lyrics", "unresolved"),
            26: ("same interval", "static", "orbit", "conflict"),
            27: ("0.4", "cuts", "timing"),
        }
        self.assertTrue(required.keys() <= cases.keys())
        for identifier, terms in required.items():
            with self.subTest(case=identifier):
                case = cases[identifier]
                text = " ".join(
                    [case["prompt"], case["expected_output"], *case["expectations"]]
                ).lower()
                for term in terms:
                    self.assertIn(term, text)
                self.assertIn("no generation", case["prompt"].lower())

    def test_authorization_audio_and_timing_checks_remain(self):
        text = normalized(SKILL / "SKILL.md")
        for term in ("written consent", "master", "verbatim", "unresolved",
                     "raw", "timing", "verify", "lip-sync", "supported"):
            self.assertIn(term, text)
        self.assertRegex(text, r"(?:preserve|retain).{0,100}master")


if __name__ == "__main__":
    unittest.main()
