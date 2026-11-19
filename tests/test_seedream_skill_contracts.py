import json
import re
import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[1] / ".agents" / "skills"
SCENARIOS = {
    "plain-text-to-image",
    "transparent-asset",
    "photograph-to-cutout",
    "translucent-material-and-hole",
    "conflicting-references",
    "numbered-region-edits",
    "bbox-boundary",
    "invalid-edit-input",
    "expressive-title",
    "delivery-critical-copy",
    "accepted-output-edit-chain",
    "channel-adaptation",
    "unsupported-layer-splitting",
    "explicit-model-pin",
    "prompt-only",
}


class SeedreamSkillContractsTests(unittest.TestCase):
    def text(self, skill, relative="SKILL.md"):
        return (SKILLS / skill / relative).read_text(encoding="utf-8")

    def assert_concepts(self, text, *patterns):
        normalized = " ".join(text.lower().replace("\u2013", "-").split())
        for pattern in patterns:
            with self.subTest(concept=pattern):
                self.assertIsNotNone(
                    re.search(pattern, normalized), f"Missing contract concept: {pattern}"
                )

    def optional_skill_text(self, skill, relative="SKILL.md"):
        if not (SKILLS / skill).exists():
            self.skipTest(f"{skill} is not installed in this workspace")
        return self.text(skill, relative)

    def seedream_review(self):
        relative = "references/checklist-seedream.md"
        if not (SKILLS / "prompt-review" / relative).exists():
            relative = "references/review-checklists.md"
        text = self.text("prompt-review", relative)
        section = re.search(
            r"(?ms)^## Seedream image generation[^\n]*\n(.*?)(?=^## |\Z)",
            text,
        )
        if section is None:
            self.fail("Seedream image review section is missing")
        return section.group(1)

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

    def test_optional_edit_support_is_not_family_wide(self):
        edit = self.optional_skill_text("seedream-edit")
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

    def test_marketing_storyboard_fast_mode_is_capability_gated(self):
        if not (SKILLS / "seedream-product-shot").exists():
            self.skipTest("Marketing product-shot capability is not installed")
        text = self.text("seedream-storyboard", "references/generation-and-persistence.md")
        self.assertIn("verified", text)
        self.assertNotIn("Use prompt optimization `standard` unless", text)

    def test_prompt_only_and_unknown_submission_are_not_generation_permission(self):
        text = self.text("seedream-storyboard")
        self.assertIn("prompt-only", text.lower())
        self.assertIn("reconcil", text.lower())
        self.assertIn("do not submit", text.lower())

    def test_product_selection_respects_review_mode_and_explicit_count(self):
        text = self.optional_skill_text("seedream-product-shot")
        self.assertNotIn("Default to **three stochastic samples**", text)
        for concept in ("default", "strict", "explicit", "Preserve the selected model"):
            self.assertIn(concept, text)

    def test_marketing_persistence_distinguishes_job_and_native_task(self):
        if not (SKILLS / "seedream-product-shot").exists():
            self.skipTest("Marketing product-shot capability is not installed")
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

    def test_focused_references_are_linked_and_shipped(self):
        entrypoint = self.text("seedream-prompt")
        for filename in ("transparent-assets.md", "layout-and-typography.md"):
            with self.subTest(reference=filename):
                self.assertIsNotNone(
                    re.search(rf"\]\(references/{re.escape(filename)}(?:#[^)]+)?\)", entrypoint),
                    f"Entrypoint must link references/{filename}",
                )
                path = SKILLS / "seedream-prompt" / "references" / filename
                self.assertTrue(path.is_file(), f"Missing linked reference: {filename}")
                self.assertTrue(path.read_text(encoding="utf-8").strip())

    def test_prompt_and_structured_coordinate_conventions_are_distinct(self):
        for relative in ("references/image-editing.md", "references/layout-and-typography.md"):
            with self.subTest(reference=relative):
                self.assert_concepts(
                    self.text("seedream-prompt", relative),
                    r"(?:prompt|guide).{0,160}0-1000|0-1000.{0,160}(?:prompt|guide)",
                    r"(?:structured|adapter|mcp).{0,160}0-999|0-999.{0,160}(?:structured|adapter|mcp)",
                )

    def test_structured_edit_targets_first_image_without_duplicate_markup(self):
        text = self.text("seedream-prompt", "references/image-editing.md")
        self.assert_concepts(
            text,
            r"first (?:input |reference )?image|image 1 only|only.{0,40}image 1|images\[0\]",
            r"(?:adapter|tool|wrapper).{0,100}(?:insert|add|construct|prepend|suppl)",
            r"(?:do not|never|avoid|no).{0,100}(?:duplicat|hand.{0,10}(?:write|written)|raw markup|"
            r"(?:add|insert|write).{0,80}(?:markup|<point>|<bbox>))",
            r"reorder.{0,160}(?:bind|label|index|indices)|(?:bind|label|index|indices).{0,160}reorder",
        )

    def test_invalid_boxes_and_changed_source_geometry_are_not_silently_repaired(self):
        text = self.text("seedream-prompt", "references/image-editing.md")
        self.assertIsNotNone(
            re.search(r"\]\(layout-and-typography\.md(?:#[^)]+)?\)", text),
            "Editing guidance must link its detailed coordinate validation reference",
        )
        text += "\n" + self.text("seedream-prompt", "references/layout-and-typography.md")
        self.assert_concepts(
            text,
            r"reject|invalid|unresolved",
            r"inverted|reversed",
            r"degenerate|zero.area",
            r"out.of.range",
            r"missing.{0,80}(?:image|source)|(?:image|source).{0,80}missing",
            r"(?:crop|refram).{0,180}(?:recomput|recalcul)|(?:recomput|recalcul).{0,180}(?:crop|refram)",
            r"1000.{0,120}999|999.{0,120}1000",
        )

    def test_transparency_requires_decoded_alpha_and_composite_inspection(self):
        text = self.text("seedream-prompt", "references/transparent-assets.md")
        self.assert_concepts(
            text,
            r"opaque",
            r"translucen",
            r"(?:interior|internal).{0,30}(?:hole|opening)|hole",
            r"decod.{0,100}alpha|alpha.{0,100}decod",
            r"light.{0,100}dark|dark.{0,100}light",
            r"edge",
            r"halo|fring",
            r"(?:extension|suffix|filename|png).{0,100}(?:not|insufficient|alone)",
            r"background",
            r"output_format",
        )

    def test_reference_roles_include_exclusions_and_conflict_precedence(self):
        text = self.text("seedream-prompt", "references/image-generation.md")
        self.assert_concepts(
            text,
            r"role",
            r"target",
            r"preserv|protect",
            r"exclud|do not (?:inherit|borrow|copy)|ignore",
            r"precedence|conflict.{0,100}priorit|priorit.{0,100}conflict",
            r"identity|silhouette|shape",
            r"material|texture",
            r"environment",
            r"input order|ordered input|order.{0,80}(?:reference|image)",
        )

    def test_edit_chains_use_accepted_artifacts_and_self_contained_locks(self):
        text = self.text("seedream-prompt", "references/image-editing.md")
        self.assert_concepts(
            text,
            r"(?:last|latest|most recent).{0,50}(?:accepted|approved).{0,60}(?:image|output|artifact)",
            r"self.contained",
            r"one.{0,25}(?:major|primary).{0,25}(?:delta|change)",
            r"preserv|protect",
            r"memory|conversation",
            r"rollback|roll back|revert|reject",
            r"drift",
            r"hash",
            r"prompt",
            r"reference order|ordered reference",
            r"model",
            r"settings|parameters",
        )

    def test_adaptation_separates_resize_from_recomposition_and_exact_copy(self):
        text = self.text("seedream-prompt", "references/layout-and-typography.md")
        self.assert_concepts(
            text,
            r"deterministic",
            r"resiz",
            r"crop",
            r"recompos",
            r"extension|outpaint",
            r"verif|capabilit",
            r"(?:no|never|without|avoid|not).{0,30}stretch",
            r"safe.{0,20}(?:area|margin|zone)",
            r"proportion",
            r"exact.{0,25}(?:copy|text)|delivery.critical",
            r"proofread|every character",
            r"line.break",
        )

    def test_edit_leaf_uses_current_caller_owned_tool_contract(self):
        text = self.optional_skill_text("seedream-edit")
        self.assertIsNone(
            re.search(r"\bseedream_(?:edit_image|generate_image_variations)\b", text),
            "Retired editing or variations tool name remains in seedream-edit",
        )
        self.assert_concepts(
            text,
            r"seedream_generate_image",
            r"ark_job_submit",
            r"variations",
            r"caller",
            r"first (?:input |reference )?image|image 1 only|only.{0,40}image 1|images\[0\]",
            r"0-999|0 to 999",
            r"(?:do not|never|avoid|no).{0,100}(?:duplicat|hand.{0,10}(?:write|written)|raw markup|"
            r"(?:add|insert|write).{0,80}(?:markup|<point>|<bbox>))",
        )

    def test_seedream_review_does_not_claim_positional_weighting(self):
        text = " ".join(self.seedream_review().lower().split())
        self.assertIsNone(
            re.search(
                r"earlier (?:concepts|words|tokens) "
                r"(?:carry|have|receive).{0,30}(?:more|greater|higher) weight", text
            ),
            "Seedream review still claims positional weighting",
        )

    def test_seedream_specialists_do_not_reference_retired_tools(self):
        for skill in sorted(SKILLS.glob("seedream-*")):
            for path in sorted(skill.rglob("*.md")):
                with self.subTest(path=path.relative_to(SKILLS)):
                    self.assertIsNone(
                        re.search(
                            r"\bseedream_(?:edit_image|generate_image_variations)\b",
                            path.read_text(),
                        ),
                        f"Retired tool referenced by {path.relative_to(SKILLS)}",
                    )

    def test_seedream_review_covers_new_output_acceptance_contracts(self):
        self.assert_concepts(
            self.seedream_review(),
            r"alpha",
            r"hole|edge",
            r"0-1000",
            r"0-999",
            r"precedence|conflict",
            r"accepted|approved",
            r"drift",
            r"recompos|adapt",
            r"deterministic",
            r"proofread|every character",
        )

    def test_upgrade_evals_cover_all_scenarios_with_portable_behavioral_checks(self):
        data = json.loads(self.text("seedream-prompt", "evals/evals.json"))
        self.assertEqual(data["skill_name"], "seedream-prompt")
        identifiers = [case["id"] for case in data["evals"]]
        self.assertEqual(len(identifiers), len(set(identifiers)))
        cases = [case for case in data["evals"] if case.get("category") == "seedream-55-upgrade"]
        self.assertEqual(SCENARIOS - {case.get("scenario") for case in cases}, set())
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(case["prompt"].strip())
                self.assertTrue(case["expected_output"].strip())
                self.assertEqual(case["files"], [])
                self.assertGreaterEqual(len(case["expectations"]), 3)
                self.assertTrue(all(isinstance(item, str) and item.strip()
                                    for item in case["expectations"]))
                self.assertNotRegex(
                    json.dumps(case),
                    r"https?://|file://|/Users/|/home/|[A-Za-z]:\\\\",
                )


if __name__ == "__main__":
    unittest.main()
