import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents/skills/hyperframes-creative"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


class HyperframesCreativeFreedomTests(unittest.TestCase):
    def test_house_choices_do_not_override_brief_or_require_decoration(self):
        text = normalized(SKILL / "references/house-style.md")
        for phrase in (
            "tech, cinema, finance → dark",
            "one accent hue. same background across all scenes",
            "2-5 per scene",
            "a scene with 1 decorative is under-dressed",
            "all decoratives should have slow ambient",
        ):
            self.assertNotIn(phrase, text)
        for concept in ("brief", "optional", "sparse", "stillness", "brand"):
            self.assertIn(concept, text)

    def test_composition_and_motion_have_no_universal_aesthetic_quotas(self):
        for name in ("video-composition.md", "motion-principles.md"):
            with self.subTest(reference=name):
                text = normalized(SKILL / "references" / name)
                for phrase in (
                    "two focal points minimum",
                    "three layers minimum",
                    "every decorative element should have ambient motion",
                    "3+ different eases",
                    "no more than 2 independent tweens",
                    "slowest scene should be 3",
                    "every image must have motion treatment",
                    "every scene has three phases",
                ):
                    self.assertNotIn(phrase, text)
                self.assertIn("stillness", text)
                self.assertIn("brief", text)

    def test_expansion_and_beats_do_not_require_enrichment_or_motion(self):
        for name in ("prompt-expansion.md", "beat-direction.md"):
            text = normalized(SKILL / "references" / name)
            for phrase in (
                "background layer (2-5 decoratives)",
                "required 2–5",
                "secondary motion for every decorative",
                "a decorative without ambient motion feels dead",
                "the expansion is never pass-through",
                "every user prompt",
                "make it richer",
                "are added on top",
                "do not pass through",
                "micro-motion requirements",
                "every element gets a verb",
                "not yet designed",
                "every beat should have at least 2 layers",
            ):
                with self.subTest(reference=name, phrase=phrase):
                    self.assertFalse(phrase in text, f"Compulsory enrichment: {phrase}")

    def test_expansion_and_beats_preserve_intent_and_technical_safeguards(self):
        for name in ("prompt-expansion.md", "beat-direction.md"):
            text = normalized(SKILL / "references" / name)
            for concept in (
                "brief", "optional", "sparse", "stillness", "source scope",
                "locked brand", "readability", "seekable", "no minimum",
            ):
                with self.subTest(reference=name, concept=concept):
                    self.assertIn(concept, text)
        text = normalized(SKILL / "references/prompt-expansion.md")
        self.assertIn("does not invent new ones", text)
        self.assertIn("user approves or says to continue", text)

    def test_brand_locks_and_seekable_runtime_safeguards_remain(self):
        text = normalized(SKILL / "references/design-adherence.md")
        self.assertIn("font families and weights match", text)
        self.assertIn("no substitutions", text)
        self.assertIn("declared", text)
        self.assertNotIn("no per-scene color invention", text)
        runtime = normalized(SKILL / "references/motion-principles.md")
        for concept in (
            "never overlap conflicting transform tweens",
            "no iframes for captured content",
            "seekable",
            "hyperframes alone controls `.clip` lifecycle",
        ):
            self.assertIn(concept, runtime)

    def test_local_overlay_is_discoverable_before_house_references(self):
        text = normalized(SKILL / "SKILL.md")
        self.assertIn("local creative-policy overlay", text)
        self.assertIn("re-vendoring", text)
        self.assertIn("not acceptance gates", text)

    def test_behavior_fixtures_cover_freedom_locks_and_missing_input(self):
        path = ROOT / "tests/fixtures/hyperframes_creative_freedom.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["status"], "not_run")
        cases = data["evals"]
        required = {
            "sparse_title", "maximalist", "bright_technology", "dark_food",
            "brand_locked", "missing_spec", "palette_transition", "still_multiscene",
        }
        self.assertEqual(required, {case["id"] for case in cases})
        for case in cases:
            self.assertTrue(case["prompt"].strip())
            self.assertGreaterEqual(len(case["expectations"]), 3)
            self.assertNotIn("observed_result", case)


if __name__ == "__main__":
    unittest.main()
