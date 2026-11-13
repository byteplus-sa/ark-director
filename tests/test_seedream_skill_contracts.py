import json
import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[1] / ".agents" / "skills"


class SeedreamSkillContractsTests(unittest.TestCase):
    def text(self, skill, relative="SKILL.md"):
        return (SKILLS / skill / relative).read_text()

    def test_prompt_routing_is_generic_not_a_closed_model_list(self):
        text = self.text("seedream-prompt")
        description = next(line for line in text.splitlines()
                           if line.startswith("description:"))
        self.assertIn("Seedream", description)
        self.assertNotRegex(description, r"5\.0|Pro/Lite|5\.5")
        self.assertIn("selected model", text)
        self.assertIn("exact model ID", text)

    def test_response_representation_is_distinct_from_image_encoding(self):
        text = self.text("seedream-prompt", "references/quick-reference.md")
        self.assertRegex(text, r"`response_format`[^\n]*`url`[^\n]*`b64_json`")
        self.assertRegex(text, r"`output_format`[^\n]*`png`[^\n]*`jpeg`")
        self.assertNotIn("`response_format`, `output_format`: png / jpeg", text)

    def test_decomposition_is_operation_scoped_not_a_fixed_image_count(self):
        for relative in ("references/quick-reference.md", "references/image-editing.md"):
            with self.subTest(relative=relative):
                text = self.text("seedream-prompt", relative)
                self.assertNotRegex(text, r"(?i)2-20 images")
                for concept in ("layer_decomposition", "exactly one", "base", "ceiling"):
                    self.assertIn(concept, text)
                self.assertIn("0-1000", text)
                self.assertIn("0-999", text)

    def test_existing_api_ids_remain_scoped_reference_data(self):
        text = self.text("seedream-prompt", "references/quick-reference.md")
        self.assertIn("dola-seedream-5-0-pro-260628", text)
        self.assertIn("dola-seedream-5-5-261028", text)
        self.assertIn("not a default", text)

    def test_asset_and_storyboard_defaults_preserve_selected_model(self):
        for skill in ("seedream-location-asset", "seedream-prop-asset", "seedream-storyboard"):
            with self.subTest(skill=skill):
                text = self.text(skill)
                self.assertIn("Preserve the selected model", text)
                self.assertIn("unknown", text.lower())
                self.assertIn("authorization", text.lower())

    def test_coordinate_edit_support_is_not_family_wide(self):
        text = self.text("seedream-prompt", "references/image-editing.md")
        self.assertNotIn("Precise coordinate location (Pro only)", text)
        self.assertIn("selected model", text)
        path = SKILLS / "seedream-edit" / "SKILL.md"
        if path.exists():
            edit = path.read_text()
            self.assertNotIn("The edit tool works with all Seedream models", edit)
            self.assertIn("unknown", edit.lower())
            self.assertIn("full-frame", edit)

    def test_storyboard_eval_covers_selected_model_and_unknown_schema(self):
        data = json.loads(self.text("seedream-storyboard", "evals/evals.json"))
        identifiers = [case["id"] for case in data["evals"]]
        self.assertEqual(len(identifiers), len(set(identifiers)))
        cases = [case for case in data["evals"] if case.get("category") == "model-preservation"]
        self.assertGreaterEqual(len(cases), 3)
        contents = json.dumps(cases).lower()
        for concept in ("5.5", "unknown", "authorization", "prompt-only", "future"):
            self.assertIn(concept, contents)

    def test_optional_seed_and_fast_mode_are_capability_gated(self):
        lighting = self.text("seedance-lighting-presets")
        self.assertIn("when the selected", lighting)
        self.assertNotIn("Always test presets as an A/B pair", lighting)
        path = SKILLS / "seedream-storyboard" / "references/generation-and-persistence.md"
        if SKILLS.parent.parent.name == "seed-marketing-studio" and path.exists():
            text = path.read_text()
            self.assertIn("verified", text)
            self.assertNotIn("Use prompt optimization `standard` unless", text)

    def test_prompt_only_and_unknown_submission_are_not_generation_permission(self):
        text = self.text("seedream-storyboard")
        self.assertIn("prompt-only", text.lower())
        self.assertIn("reconcil", text.lower())
        self.assertIn("do not submit", text.lower())

    def test_product_selection_respects_review_mode_and_explicit_count(self):
        path = SKILLS / "seedream-product-shot/SKILL.md"
        if not path.exists():
            return
        text = path.read_text()
        self.assertNotIn("Default to **three stochastic samples**", text)
        for concept in ("default", "strict", "explicit", "Preserve the selected model"):
            self.assertIn(concept, text)

    def test_marketing_persistence_distinguishes_job_and_native_task(self):
        if SKILLS.parent.parent.name != "seed-marketing-studio":
            return
        for skill, relative in (
            ("seedream-edit", "SKILL.md"),
            ("seedream-storyboard", "references/generation-and-persistence.md"),
        ):
            with self.subTest(skill=skill):
                text = self.text(skill, relative)
                for concept in ("ark_job_submit", "persistence_error", "terminal",
                                "seed_media_export_artifact", "confirmed native",
                                "hash", "Reconcile"):
                    self.assertIn(concept.lower(), text.lower())
                self.assertRegex(text, r"Do not pass `output_path` or `output_dir`")

    def test_mcp_image_controls_follow_discovery_and_wrapper_capabilities(self):
        text = self.text("ark-mcp", "references/tool-reference.md")
        limits = self.text("ark-mcp", "references/models-and-limits.md")
        for concept in ("seedream_generate_image", "point", "bbox",
                        "variations", "transparent", "b64_json",
                        "Decomposition/OCR inputs are rejected",
                        "not guaranteed identical pixels"):
            self.assertIn(concept, text)
        for concept in ("ark_list_models", "authoritative",
                        "requires account authorization"):
            self.assertIn(concept, limits)
        self.assertNotIn("seedream_generate_image_variations", text)


if __name__ == "__main__":
    unittest.main()
