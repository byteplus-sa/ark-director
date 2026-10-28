from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents/skills"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


class CreativeDefaultsTests(unittest.TestCase):
    def test_compilers_and_review_do_not_soften_body_energy_or_cap_bursts(self):
        paths = (
            "seedance-prompt-25/references/scene-action.md",
            "seedance-prompt-20/SKILL.md",
            "prompt-review/references/checklist-seedance-25.md",
            "prompt-review/references/checklist-seedance-legacy.md",
        )
        for relative in paths:
            with self.subTest(path=relative):
                text = normalized(SKILLS / relative)
                self.assertNotRegex(text, r"prefer(?:s)? slow, (?:gentle, )?continuous")
                self.assertNotIn("appears at most once per shot", text)
                self.assertNotIn("write one burst with a still hold", text)
                self.assertIn("interruptions", text)
                self.assertIn("recovery", text)

    def test_speech_does_not_automatically_exclude_kinetic_coverage(self):
        paths = (
            "seedance-shot-design/SKILL.md",
            "seedance-shot-design/references/coverage-patterns.md",
            "seedance-prompt-25/references/shot-staging.md",
            "prompt-review/references/checklist-seedance-25.md",
            "micro-drama/SKILL.md",
        )
        for relative in paths:
            with self.subTest(path=relative):
                text = normalized(SKILLS / relative)
                self.assertNotRegex(text, r"(?:only|kinetic is) for shots without spoken")
                self.assertNotRegex(text, r"keep (?:their )?moves (?:quiet|slow)")
                self.assertNotIn("large moves there are minor", text)
                self.assertNotIn("no silhouette on a shot with spoken lines", text)
                self.assertIn("readability", text)

    def test_coverage_rules_do_not_require_contrast_angles_or_wow_counts(self):
        paths = (
            "seedance-shot-design/SKILL.md",
            "seedance-shot-design/references/shot-plan-format.md",
            "seedance-shot-design/evals/evals.json",
            "seedance-prompt-25/evals/evals.json",
            "prompt-review/references/checklist-seedance-legacy.md",
            "tests/fixtures/creative_quality_shot_design_cases.json",
        )
        for relative in paths:
            path = ROOT / relative if relative.startswith("tests/") else SKILLS / relative
            with self.subTest(path=relative):
                text = normalized(path)
                self.assertNotRegex(text, r"adjacent shots (?:still )?differ in at least two")
                self.assertNotIn("at least one shot per scene is not plain eye level", text)
                self.assertNotIn("`true` on one shot per clip", text)
                self.assertNotIn("flags exactly one wow", text)
                self.assertNotIn("exactly one shot is flagged as the turn", text)
                self.assertNotIn("and neighboring shots differ", text)

    def test_cadence_is_not_an_automatic_ad_acceptance_recipe(self):
        names = ("brief-intake", "film-production", "seedance-prompt-25",
                 "seedance-shot-design", "seedance-pacing-presets", "ugc-ad-modes",
                 "seedance-music-video")
        forbidden = (
            r"build a 30 s spot as about",
            r"build a 30 s spot from about six",
            r"ads and tvcs group shots into sequences of about 5",
            r"give every sequence \*\*one",
            r"each sequence has 2-3 shots, one action per shot and one",
            r"plans about six 5 s sequences",
            r"proposes about six 5 s sequences",
            r"cinematic bar is a 30 s section built from about six",
            r"builds the 30 s section from roughly six",
        )
        for name in names:
            for path in (SKILLS / name).rglob("*"):
                if path.is_file() and path.suffix in {".md", ".json"}:
                    with self.subTest(path=str(path.relative_to(ROOT))):
                        for pattern in forbidden:
                            self.assertNotRegex(normalized(path), pattern)

    def test_episode_template_does_not_override_a_supplied_held_scene(self):
        text = normalized(SKILLS / "micro-drama/SKILL.md")
        self.assertNotIn("the hook lands within the first 3 s", text)
        self.assertIn("optional hook", text)

    def test_framing_size_follows_readability_not_automatic_importance(self):
        text = normalized(SKILLS / "seedance-shot-design/references/framing.md")
        self.assertNotIn("how large a subject is signals how much it matters", text)
        self.assertNotIn("size follows importance as a default", text)
        self.assertNotIn("the more a subject matters to the beat, the larger", text)
        self.assertIn("required action", text)
        self.assertIn("distance may be the intended meaning", text)

    def test_oth_does_not_invent_height_or_power_differences(self):
        text = normalized(SKILLS / "seedance-shot-design/references/framing.md")
        self.assertNotIn("stage the height difference", text)
        self.assertNotIn("it gives no power imbalance", text)
        self.assertIn("preserve approved blocking", text)
        self.assertIn("power imbalance is not required", text)

    def test_cuts_may_retain_light_side_across_skill_and_reference(self):
        paths = (
            "seedance-shot-design/SKILL.md",
            "seedance-prompt-25/references/shot-staging.md",
        )
        for relative in paths:
            with self.subTest(path=relative):
                text = normalized(SKILLS / relative)
                self.assertNotIn("a cut changes which side of a source", text)
                self.assertRegex(text, r"a cut may (?:retain|preserve) or change")
                self.assertRegex(text, r"(?:motivated|stated) event")

    def test_episode_draft_count_follows_independent_planned_clips(self):
        paths = (
            "micro-drama/SKILL.md",
            "micro-drama/references/production-recipe.md",
        )
        for relative in paths:
            with self.subTest(path=relative):
                text = normalized(SKILLS / relative)
                self.assertNotIn("draft the three clips of an episode", text)
                self.assertIn("independent planned clips in parallel", text)
                self.assertIn("480p native draft", text)

    def test_board_review_preserves_equal_timing_and_optional_turns(self):
        text = normalized(SKILLS / "scene-board-sheet/SKILL.md")
        self.assertNotIn("the turn shot differs in length", text)
        self.assertIn("equal durations", text)
        self.assertIn("no turn", text)

    def test_camera_presets_and_framing_do_not_require_extra_coverage(self):
        paths = (
            "seedance-camera-presets/SKILL.md",
            "seedance-shot-design/references/framing.md",
            "seedance-shot-design/references/coverage-patterns.md",
        )
        for relative in paths:
            with self.subTest(path=relative):
                text = normalized(SKILLS / relative)
                self.assertNotIn("use only when the two characters are at different heights", text)
                self.assertNotIn("cover it with a shot of the looker before it", text)
                self.assertNotIn("keep a pov shot adjacent", text)
                self.assertIn("preserve approved blocking", text)
                self.assertIn("look/reaction shots are optional", text)
        evaluations = normalized(SKILLS / "seedance-camera-presets/evals/evals.json")
        self.assertNotIn("should sit beside a shot of ana looking", evaluations)
        self.assertNotIn("with advice to cover the pov", evaluations)

    def test_two_move_heuristic_preserves_explicit_coherent_choreography(self):
        paths = (
            "seedance-camera-presets/SKILL.md",
            "seedance-shot-design/SKILL.md",
            "seedance-shot-design/references/coverage-patterns.md",
            "seedance-prompt-25/references/shot-staging.md",
            "prompt-review/references/checklist-seedance-25.md",
        )
        for relative in paths:
            with self.subTest(path=relative):
                text = normalized(SKILLS / relative)
                self.assertIn("heuristic", text)
                self.assertIn("explicitly requested coherent choreography", text)
                self.assertNotIn("`stack` is 2 or fewer", text)
                self.assertNotIn("**at most 2 per shot.**", text)
        contract = normalized(ROOT / ".agents/contracts/seedance-reference.md")
        self.assertNotIn("keep \u22642 moves per shot", contract)
        self.assertNotIn("scene, and 1\u20132 camera moves per shot", contract)
        self.assertIn("explicitly requested coherent choreography", contract)
        rubric = normalized(ROOT / "tests/fixtures/creative_quality_shot_design_cases.json")
        self.assertNotIn("each shot has one primary move and at most one secondary", rubric)

    def test_ugc_flags_distinguish_creative_cautions_from_provider_limits(self):
        text = normalized(SKILLS / "ugc-motion-presets/SKILL.md")
        self.assertNotIn("flags encode real provider constraints, not style advice", text)
        self.assertIn("creative heuristics", text)
        self.assertIn("source intent", text)
        constraints = normalized(
            SKILLS / "ugc-motion-presets/references/execution-constraints.md",
        )
        self.assertNotIn("jumps use described, moderate dynamics", constraints)
        self.assertIn("not a provider limit", constraints)
        self.assertIn("recovery", constraints)
        self.assertIn("readability", constraints)

    def test_camera_and_pacing_do_not_restore_numeric_move_caps(self):
        paths = (
            "seedance-camera-presets/SKILL.md",
            "seedance-camera-presets/evals/evals.json",
            "seedance-pacing-presets/SKILL.md",
        )
        for relative in paths:
            with self.subTest(path=relative):
                text = normalized(SKILLS / relative)
                for phrase in (
                    "count it toward the move limit",
                    "at or below 2",
                    "each with at most two moves",
                    "no more than two simultaneous moves",
                    "keep simultaneous moves to at most two",
                ):
                    self.assertNotIn(phrase, text)
                self.assertIn("coherent", text)

    def test_cut_timing_guidance_is_provisional_and_preserves_requested_timing(self):
        paths = (
            "seedance-pacing-presets/SKILL.md",
            "seedance-pacing-presets/references/assembly-cuts.md",
            "seedance-pacing-presets/references/cut-transitions.md",
            "seedance-shot-design/SKILL.md",
            "seedance-shot-design/references/coverage-patterns.md",
            "prompt-review/references/checklist-seedance-25.md",
            "prompt-review/references/author-self-check.md",
        )
        for relative in paths:
            with self.subTest(path=relative):
                text = normalized(SKILLS / relative)
                for phrase in (
                    "0.8 s are merged or dropped",
                    "0.8 s is merged or dropped",
                    "0.8 s merge inside one clip",
                    "none shorter than about 0.8 s",
                    "no shot inside one clip is shorter",
                    "respect the shot ceiling",
                    "clip-level cap is the shot ceiling",
                    "hard cuts leave at least about 0.8 s",
                    "shorter cuts merge",
                ):
                    self.assertNotIn(phrase, text)
                self.assertIn("provisional", text)
                self.assertIn("preserve requested timing", text)
                self.assertIn("conflict", text)

    def test_progressive_change_does_not_force_slow_crossings_or_fixed_intervals(self):
        paths = (
            "seedance-pacing-presets/SKILL.md",
            "prompt-review/references/checklist-seedance-25.md",
        )
        for relative in paths:
            with self.subTest(path=relative):
                text = normalized(SKILLS / relative)
                self.assertNotIn("slow the movement so the crossing takes", text)
                self.assertNotIn("slow enough that the crossing lasts", text)
                self.assertNotIn("a slowed crossing", text)
                self.assertIn("1.5 s", text)
                self.assertIn("0.4 s", text)
                self.assertIn("optional", text)
                self.assertIn("not provider limits", text)
                self.assertIn("unbroken", text)

    def test_direct_timing_consumers_preserve_provisional_authority(self):
        paths = (
            "seedance-prompt-25/SKILL.md",
            "seedance-prompt-25/references/shot-staging.md",
            "film-production/references/production-defaults.md",
            "film-production/references/stage-contracts.md",
            "seedance-music-video/SKILL.md",
            "seedance-music-video/references/music-video-recipes.md",
            "seedance-motion-design/SKILL.md",
            "seedance-animation-styles/SKILL.md",
            "seedance-vfx-prompt/SKILL.md",
            "seedance-graybox-world/SKILL.md",
            "template-factory/references/long-pins-and-multi-clip.md",
            "ugc-ad-modes/SKILL.md",
        )
        for relative in paths:
            with self.subTest(path=relative):
                text = normalized(SKILLS / relative)
                for phrase in (
                    "shots shorter than about 0.8 s merge",
                    "shots under about 0.8 s merge",
                    "seedance merges shots",
                    "seedance merges shorter shots",
                    "the model merges shorter shots",
                    "no in-clip shot is shorter",
                    "no shot inside one generation is shorter",
                    "no planned in-generation shot is shorter",
                    "keep every shot inside one clip at about 0.8 s or longer",
                    "at most about 6\u20137 shots",
                    "about 7 shots at most",
                    "fit the duration and the shot ceiling",
                    "plan faster cuts in assembly",
                ):
                    self.assertNotIn(phrase, text)
                self.assertIn("provisional", text)
                self.assertIn("preserve requested timing", text)
                self.assertIn("conflict", text)

    def test_direct_camera_consumers_do_not_reinstate_move_count_gates(self):
        paths = (
            "seedance-music-video/SKILL.md",
            "seedance-music-video/references/music-video-recipes.md",
            "seedance-graybox-world/SKILL.md",
            "seedance-vfx-prompt/references/seedance-25-edit.md",
            "template-factory/references/slot-mapping.md",
        )
        for relative in paths:
            with self.subTest(path=relative):
                text = normalized(SKILLS / relative)
                self.assertNotIn("at most two camera moves", text)
                self.assertNotIn("\u22642 moves per shot", text)
                self.assertNotIn("\u2264 2 moves in one take", text)
                self.assertNotIn("three or more reads as unstable", text)
                self.assertNotIn("more than two simultaneous moves per shot becomes unstable", text)
                self.assertIn("heuristic", text)
                self.assertIn("explicitly requested coherent choreography", text)
        effects = normalized(
            SKILLS / "seedance-effects-studio/references/effects-product-and-spectacle.md",
        )
        self.assertNotIn("two moves, the limit", effects)

    def test_speech_rule_retains_identity_but_not_numeric_artistic_gates(self):
        rules = json.loads((ROOT / ".agents/contracts/rules.json").read_text())["rules"]
        rule = next(item for item in rules if item["id"] == "dialogue.speech_budget")
        self.assertEqual(rule["severity"], "error")
        self.assertEqual(rule["applies_to"], ["narrative_video"])
        self.assertEqual(
            rule["owner_path"],
            ".agents/skills/seedance-prompt-25/references/shot-staging.md",
        )
        self.assertEqual(rule["exceptions"], [])
        text = rule["summary"].lower()
        for phrase in ("provisional", "onset", "tail", "not an artistic gate",
                       "measured", "locked words"):
            self.assertIn(phrase, text)
        self.assertNotIn("ends at least 0.4 s", text)
        self.assertNotIn("with at most two state changes", text)

    def test_speech_consumers_do_not_force_onset_tail_or_closing_density(self):
        paths = (
            "seedance-prompt-25/references/shot-staging.md",
            "seedance-prompt-20/SKILL.md",
            "seedance-shot-design/SKILL.md",
            "prompt-review/references/checklist-seedance-25.md",
            "prompt-review/references/checklist-seedance-legacy.md",
            "micro-drama/references/production-recipe.md",
            "micro-drama/references/episode-structure.md",
            "film-production/references/production-defaults.md",
            "ugc-ad-modes/SKILL.md",
            "seedance-avatar-news/references/script-formula.md",
        )
        for relative in paths:
            with self.subTest(path=relative):
                text = normalized(SKILLS / relative)
                for phrase in (
                    "end the last line at least 0.4 s",
                    "keep the final 3 s to at most two state changes",
                    "more than two visible state changes in the clip's last 3 s",
                    "avoid three state changes",
                    "keep the last 3 s to one or two state changes",
                    "speech starts 0.5-1.5 s",
                    "lines land 0.5\u20131.5 s late",
                    "keep the last 3 s to the closer and a held smile",
                ):
                    self.assertNotIn(phrase, text)
                self.assertIn("provisional", text)
                self.assertRegex(text, r"(?:measured|measurement|actual)")
        review = normalized(SKILLS / "prompt-review/references/checklist-seedance-25.md")
        self.assertIn("demonstrated duration conflict is major", review)
        self.assertIn("not an artistic gate", review)

    def test_consumer_evals_do_not_reward_duplicate_caps(self):
        required = {
            "seedance-motion-design": {2},
            "seedance-animation-styles": {7},
            "seedance-music-video": {10, 16},
            "seedance-shot-design": {14, 15},
            "micro-drama": {6},
            "seedance-avatar-news": {1},
        }
        for name, identifiers in required.items():
            cases = json.loads((SKILLS / name / "evals/evals.json").read_text())["evals"]
            self.assertTrue(identifiers <= {case["id"] for case in cases})
            for case in cases:
                if case["id"] not in identifiers:
                    continue
                with self.subTest(skill=name, case=case["id"]):
                    text = " ".join([
                        case["expected_output"],
                        *case.get("expectations", case.get("assertions", [])),
                    ]).lower()
                    for phrase in (
                        "no shot inside the clip is shorter than about 0.8 s",
                        "shots of at least about 0.8 s",
                        "shots of at least about 1 s",
                        "shots shorter than about 0.8 s merge",
                        "at most two camera moves",
                        "sub-second cuts are planned for assembly",
                        "ends the last line at least 0.4 s",
                        "at least 0.4 s of tail",
                        "flags the insufficient tail",
                    ):
                        self.assertNotIn(phrase, text)

    def test_pacing_evals_preserve_timing_and_cover_conflicts_and_missing_evidence(self):
        data = json.loads((SKILLS / "seedance-pacing-presets/evals/evals.json").read_text())
        cases = {case["id"]: case for case in data["evals"]}
        self.assertEqual(len(cases), len(data["evals"]))
        self.assertTrue({9, 10, 11, 12, 13} <= cases.keys())
        for identifier in (7, 9, 10, 11, 12, 13):
            with self.subTest(case=identifier):
                case = cases[identifier]
                text = " ".join([case["expected_output"], *case["expectations"]]).lower()
                self.assertNotIn("crossing lasts about 1.5 s", text)
                self.assertNotIn("are merged or dropped", text)
                self.assertNotIn("cut list has fewer shots", text)
                self.assertTrue(case["prompt"].strip())
                self.assertGreaterEqual(len(case["expectations"]), 3)
                self.assertNotIn("observed_result", case)
        self.assertIn("0.6", cases[11]["prompt"])
        self.assertIn("conflict", cases[12]["expected_output"].lower())
        self.assertIn("unresolved", cases[13]["expected_output"].lower())

    def test_residual_conflict_evals_cover_preservation_and_failure_boundaries(self):
        required = {
            "scene-board-sheet": {11},
            "seedance-camera-presets": {10, 13, 14, 15},
            "seedance-shot-design": {18},
            "ugc-motion-presets": {10, 11},
            "micro-drama": {9, 10, 11},
        }
        for name, identifiers in required.items():
            with self.subTest(skill=name):
                data = json.loads((SKILLS / name / "evals/evals.json").read_text())
                cases = {case["id"]: case for case in data["evals"]}
                self.assertEqual(len(cases), len(data["evals"]))
                self.assertTrue(identifiers <= cases.keys())
                for identifier in identifiers:
                    case = cases[identifier]
                    self.assertTrue(case["prompt"].strip())
                    self.assertTrue(case["expected_output"].strip())
                    criteria = case.get("assertions", case.get("expectations", []))
                    self.assertGreaterEqual(len(criteria), 3)
                    self.assertTrue(all(value.strip() for value in criteria))
                    self.assertNotIn("observed_result", case)

    def test_existing_rubric_does_not_reward_unrequested_emphasis_or_motion(self):
        text = normalized(ROOT / "tests/fixtures/creative_quality_shot_design_cases.json")
        self.assertNotIn("clip's most emphasized moment", text)
        self.assertNotIn("each short shot has a distinct camera setup and move", text)
        evaluations = normalized(SKILLS / "seedance-shot-design/evals/evals.json")
        self.assertNotIn("the angle changes at the turn", evaluations)
        self.assertNotIn("rather than three separate singles", evaluations)
        self.assertNotIn("at least one shot features the boy alone", evaluations)
        staging = normalized(SKILLS / "seedance-prompt-25/references/shot-staging.md")
        self.assertNotIn("a cut changes which side of a source", staging)
        repairs = normalized(SKILLS / "seedance-shot-design/references/worked-repairs.md")
        self.assertNotIn("s, the turn", repairs)

    def test_turn_label_does_not_make_missing_camera_move_a_hard_failure(self):
        paths = (
            ROOT / ".agents/contracts/production-policy.md",
            SKILLS / "film-production/SKILL.md",
            SKILLS / "micro-drama/references/production-recipe.md",
        )
        for path in paths:
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertNotRegex(
                    normalized(path),
                    r"missing (?:planned )?move or light on (?:the shot flagged as the turn|the turn shot)",
                )
                self.assertIn("critical", normalized(path))

    def test_premise_sound_and_acceptance_reach_both_orchestrators(self):
        paths = (
            ROOT / "AGENTS.md",
            ROOT / ".agents/contracts/production-policy.md",
            SKILLS / "brief-intake/SKILL.md",
            SKILLS / "film-production/SKILL.md",
            SKILLS / "film-production/references/stage-contracts.md",
            SKILLS / "micro-drama/SKILL.md",
        )
        for path in paths:
            with self.subTest(path=str(path.relative_to(ROOT))):
                text = normalized(path)
                for concept in ("audience response", "attention", "ending",
                                "sound", "editorial", "project-specific"):
                    self.assertIn(concept, text)
        contract = normalized(ROOT / ".agents/contracts/performance-direction.md")
        for concept in ("project-specific", "timestamps", "listening", "final"):
            self.assertIn(concept, contract)

    def test_behavioral_cases_cover_success_boundaries_and_missing_evidence(self):
        path = ROOT / "tests/fixtures/creative_quality_shot_design_cases.json"
        cases = json.loads(path.read_text())["cases"]
        by_id = {case["id"]: case for case in cases}
        self.assertEqual(len(by_id), len(cases))
        required = {
            "energetic_dialogue", "repeated_equal_holds", "multiple_bursts",
            "sound_led_reveal", "unresolved_premise", "missing_playback",
            "source_preserving_energy", "wordless_product_hold",
        }
        self.assertTrue(required <= by_id.keys(), required - by_id.keys())
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertTrue((SKILLS / case["skill"] / "SKILL.md").is_file())
                self.assertTrue(case["prompt"].strip())
                self.assertGreaterEqual(len(case["criteria"]), 2)
                self.assertTrue(all(value.strip() for value in case["criteria"].values()))
                self.assertNotIn("observed_result", case)
        self.assertRegex(by_id["missing_playback"]["criteria"]["evidence"], re.compile(
            r"unresolved|incomplete", re.IGNORECASE,
        ))


if __name__ == "__main__":
    unittest.main()
