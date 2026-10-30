import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"
OWNED = ("brief-intake", "seedance-camera-presets", "color-grade-palettes")


def normalized(path):
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


class DirectionCreativeFreedomStaticTests(unittest.TestCase):
    def test_reference_allows_delegated_direction_without_recipe_caps(self):
        text = normalized(ROOT / ".agents/contracts/seedance-reference.md")
        for phrase in (
            "exactly one grade per clip", "keep one project-wide palette",
            "one dominant lighting direction", "same physical light source",
            "keep ≤2 moves", "1–2 camera moves", "per-genre style lock",
            "use a preset skill only when the user asks",
        ):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, text)
        for concept in ("delegated", "custom", "compatible", "ordered",
                        "same interval", "heuristic", "not a cap"):
            self.assertIn(concept, text)

    def test_lens_allows_proposed_optics_and_coherent_transitions(self):
        text = normalized(SKILLS / "seedance-lens-presets/SKILL.md")
        for phrase in (
            "only supply authoring values the user asked for",
            "focal length the user never mentioned", "one lens intent per shot",
            "unless the user asks for the look", "only when requested",
            "vignette is added unless requested",
        ):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, text)
        for concept in ("delegated", "custom", "proposal", "compatible",
                        "ordered", "same interval"):
            self.assertIn(concept, text)

    def test_integration_preserves_source_authority_and_capabilities(self):
        for path in (
            ROOT / ".agents/contracts/seedance-reference.md",
            SKILLS / "seedance-lens-presets/SKILL.md",
        ):
            with self.subTest(path=path.relative_to(ROOT)):
                text = normalized(path)
                for concept in ("source-preserving", "may_change", "locks",
                                "ungraded", "rights", "consent", "capabilit"):
                    self.assertIn(concept, text)
        text = normalized(SKILLS / "seedance-lens-presets/SKILL.md")
        for phrase in ("not api arguments", "preserve the selected model",
                       "no optical physics promises", "deep-focus or flare-free"):
            self.assertIn(phrase, text)

    def test_intake_removes_spectacle_preference_and_image_ceiling(self):
        text = normalized(SKILLS / "brief-intake/SKILL.md")
        self.assertNotIn("prefer suggestion over spectacle", text)
        self.assertNotIn("keep one brief stylized image", text)
        for concept in ("delegated", "fictional", "source-preserving", "claims",
                        "locks", "lens", "custom", "quiet"):
            self.assertIn(concept, text)

    def test_camera_templates_parameterize_pace_and_preserve_quiet_styles(self):
        text = normalized(SKILLS / "seedance-camera-presets/SKILL.md")
        for name in ("pan left", "pan right", "dolly in", "dolly out"):
            match = re.search(rf"\| {name} \| ([^|]+)", text)
            if match is None:
                self.fail(f"Missing camera preset: {name}")
            row = match.group(1)
            self.assertIn("<speed>", row)
            self.assertNotRegex(row, r"\bslow(?:ly)?\b")
        self.assertRegex(text, r"\| dreamy flow \|[^|]*slow")
        self.assertRegex(text, r"\| intimate observer \|[^|]*gentle")
        for concept in ("compatible", "compound", "ordered", "same interval",
                        "custom", "intent", "locks"):
            self.assertIn(concept, text)

    def test_owned_guidance_has_no_purity_or_blanket_look_gate(self):
        forbidden = (
            "choose one style per prompt", "do not combine styles",
            "optional; one per prompt", "required; one preset",
            "reserve `gentle` and `subtle`", "a hold lands best after motion",
            "no look was requested", "only when the brief asks for one",
            "propose a grade or look only when requested",
            "leave a grade or film look out unless requested",
            "use the sentence verbatim", "the grade was never requested",
        )
        for name in OWNED:
            for path in (SKILLS / name).rglob("*.md"):
                with self.subTest(path=path.relative_to(ROOT)):
                    text = normalized(path)
                    for phrase in forbidden:
                        self.assertNotIn(phrase, text)

    def test_look_permission_preserves_conform_and_approved_palette(self):
        path = SKILLS / "color-grade-palettes/SKILL.md"
        if not path.exists():
            self.skipTest("This fork has no color-grade-palettes skill")
        text = normalized(path)
        for concept in ("delegated", "custom", "source-preserving", "conform",
                        "ungraded", "approved", "locks", "saturation"):
            self.assertIn(concept, text)

    def test_existing_evals_do_not_reward_automatic_restraint_or_speed(self):
        for name in OWNED:
            path = SKILLS / name / "evals/evals.json"
            if not path.exists():
                continue
            data = json.loads(path.read_text())
            for case in data["evals"]:
                text = " ".join([
                    case["expected_output"], *case.get("expectations", [])
                ]).lower()
                with self.subTest(skill=name, case=case["id"]):
                    self.assertNotIn("instead of vfx", text)
                    self.assertNotIn("rather than relying on literal effects", text)
                    self.assertNotIn("not 'gentle' or 'subtle'", text)
                    self.assertNotIn("hedged wording caused", text)

    def test_behavior_eval_definitions_are_valid_not_claimed_results(self):
        path = SKILLS / "brief-intake/evals/direction-creative-freedom.json"
        data = json.loads(path.read_text())
        self.assertEqual(data["status"], "not_run")
        cases = data["cases"]
        self.assertEqual(len({case["id"] for case in cases}), len(cases))
        required = {
            "maximalist", "quiet", "source_edit", "custom_look", "conform",
            "locked_palette", "style_transition", "compound", "conflict",
            "slow_style", "empty_brief", "missing_evidence",
        }
        self.assertTrue(required <= {case["id"] for case in cases})
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertTrue((SKILLS / case["skill"] / "SKILL.md").is_file())
                self.assertTrue(case["prompt"].strip())
                self.assertGreaterEqual(len(case["expectations"]), 3)
                self.assertTrue(all(value.strip() for value in case["expectations"]))
                self.assertNotIn("observed_result", case)


if __name__ == "__main__":
    unittest.main()
