import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIGHTING = ROOT / ".agents/skills/seedance-lighting-presets"
ANAMORPHIC = ROOT / ".agents/skills/seedance-lens-presets/references/anamorphic-treatment.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").lower().split())


class DirectionPolicyConsumerTests(unittest.TestCase):
    def test_lighting_allows_scoped_sources_and_ordered_changes(self):
        text = normalized(LIGHTING / "SKILL.md")
        for obsolete in (
            "one dominant direction", "exactly one dominant lighting direction",
            "repeat the same lighting phrase verbatim in every scene",
            "pick one direction and compose", "not a new invented source",
        ):
            self.assertNotIn(obsolete, text)
        for concept in (
            "compatible", "backlight and overhead", "same interval",
            "ordered", "endpoints", "approved continuity",
        ):
            self.assertIn(concept, text)

    def test_lighting_allows_delegated_proposals_without_a_named_preset(self):
        text = normalized(LIGHTING / "SKILL.md")
        self.assertNotIn("added only when requested", text)
        for concept in ("delegated", "proposal", "custom", "new source", "texture"):
            self.assertIn(concept, text)

    def test_lighting_preserves_locks_and_authority(self):
        text = normalized(LIGHTING / "SKILL.md")
        for concept in (
            "source-preserving", "may_change", "conform", "ungraded",
            "grain-free", "practicals-only", "no hidden fill",
            "rights", "consent", "approval", "capabilit", "empty",
        ):
            self.assertIn(concept, text)

    def test_anamorphic_allows_delegated_optics_and_texture(self):
        text = normalized(ANAMORPHIC)
        for obsolete in (
            "if blur is requested,", "if bokeh is requested",
            "if a flare is requested,", "add them only when requested or approved",
            "if the brief did not request blur and flare",
        ):
            self.assertNotIn(obsolete, text)
        for concept in ("delegated", "proposal", "sharp", "horizontal", "vertically"):
            self.assertIn(concept, text)

    def test_anamorphic_preserves_narrow_request_and_source_locks(self):
        text = normalized(ANAMORPHIC)
        self.assertIn(
            "do not invent a focal length when the request asks only for lens character",
            text,
        )
        for concept in (
            "deep focus", "grain-free", "practicals-only", "source-preserving",
            "may_change", "ungraded", "rights", "consent", "approval",
            "capabilit", "do not silently add a lamp or sun",
            "preserve the selected model",
        ):
            self.assertIn(concept, text)

    def test_routing_allows_scoped_palette_transitions_without_move_caps(self):
        text = normalized(ROOT / ".agents/contracts/routing.md")
        axes = text.split("## directorial axes", 1)[1]
        for obsolete in (
            "keep one grade per clip", "one dominant lighting direction",
            "at most two camera moves", "unless the explicitly requested",
        ):
            self.assertNotIn(obsolete, axes)
        for concept in (
            "delegated", "compatible", "ordered", "palette", "same interval",
            "heuristic", "not a cap", "may_change", "approved", "locks",
            "rights", "consent", "capabilit",
        ):
            self.assertIn(concept, axes)

    def test_conflicting_time_of_day_eval_does_not_silently_choose_a_lock(self):
        data = json.loads((LIGHTING / "evals/evals.json").read_text())
        case = next(case for case in data["evals"] if case["id"] == 5)
        expected = " ".join([case["expected_output"], *case["expectations"]]).lower()
        self.assertNotIn("night neon, not golden hour", expected)
        for concept in ("clarif", "same interval", "transition"):
            self.assertIn(concept, expected)


if __name__ == "__main__":
    unittest.main()
