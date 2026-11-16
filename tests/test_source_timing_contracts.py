import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"
TIMING_CLAUSES = {
    "measurement": (
        "preserve the full measured source", "fractional duration", "frame count",
        "fps", "timestamps", "cuts", "final word", "audio tails",
    ),
    "missing_measurement": ("missing or malformed timing", "stop", "never guess"),
    "adaptation": (
        "current provider requirement", "selected model, operation and transport",
        "explicit derivative adaptation approval", "approve_for_me", "does not",
    ),
    "denied_adaptation": (
        "denied or missing adaptation approval", "unchanged", "no derivative",
    ),
    "derivative_record": (
        "source sha-256", "derivative sha-256", "exact window", "timing delta",
        "audio consequences",
    ),
    "no_recipe": ("no automatic", "8n+1", "whole-second", "trim", "pad", "retime"),
    "reference_precedence": (
        "timing rules govern referenced recipes", "do not authorize",
        "adaptations", "extra probes",
    ),
    "output_mismatch": ("output mismatch", "unresolved", "never", "-shortest"),
    "optional_probe": (
        "optional partial probe", "needs-based", "explicit approval",
        "not delivery", "full-duration native draft",
    ),
    "draft": (
        'resolution: "480p"', "draft: true", "every review mode",
        "missing native draft", "stop", "never drop",
    ),
}
UNSAFE_RECIPES = (
    r"trim to an\s+8n\+1",
    r"trimmed to an\s+8n\+1",
    r"trim the source to whole seconds",
    r"duration.{0,30}to the whole-second source length",
    r"trim or pad to the picture",
    r"first rung is a 480p probe",
    r"first submission proposed is a 480p probe",
    r"run the route probe on the first variant",
    r"submit the key-beat probe \(4",
)
EVAL_CLAUSES = {
    101: ("14.375", "fractional", "final word", "audio tails", "full", "480p", "draft: true"),
    102: ("denied", "unchanged", "no derivative"),
    103: (
        "current provider requirement", "explicit derivative adaptation approval",
        "source sha-256", "derivative sha-256", "exact window", "timing delta",
    ),
    104: ("missing", "malformed", "stop", "never guess"),
    105: ("fractional", "unsupported", "approval", "no derivative"),
    106: (
        "partial probe", "explicit approval", "not delivery",
        "full-duration", "draft: true",
    ),
    107: ("shorter", "final word", "unresolved", "-shortest"),
    108: ("missing native draft", "stop", "never drop", "draft"),
}


def timing_contract_errors(document: object) -> list[str]:
    if not isinstance(document, str) or not document.strip():
        return ["missing timing advice"]
    heading = "## Source timing"
    if document.count(heading) != 1:
        return ["missing or ambiguous source timing section"]
    section = document.split(heading, 1)[1].split("\n## ", 1)[0]
    paragraphs = [
        " ".join(paragraph.lower().split())
        for paragraph in section.strip().split("\n\n")
    ]
    return [
        name for name, clauses in TIMING_CLAUSES.items()
        if not any(all(clause in paragraph for clause in clauses) for paragraph in paragraphs)
    ]


class SourceTimingContractsTests(unittest.TestCase):
    def documents(self) -> list[Path]:
        paths = [SKILLS / "seedance-motion-recast" / "SKILL.md"]
        if ROOT.name in {"ark-director", "seed-marketing-studio"}:
            paths.append(SKILLS / "seedance-restoration" / "SKILL.md")
        if ROOT.name == "ark-director":
            paths.append(
                SKILLS / "seedance-vfx-pipeline" / "references" / "recast-and-variants.md"
            )
        return paths

    def test_shipped_instructions_cover_all_timing_and_approval_branches(self) -> None:
        for path in self.documents():
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertEqual(timing_contract_errors(path.read_text()), [])

    def test_no_mandatory_frame_rounding_mux_padding_or_extra_probe_recipe(self) -> None:
        for path in self.documents():
            text = " ".join(path.read_text().lower().split())
            for pattern in UNSAFE_RECIPES:
                with self.subTest(path=path.relative_to(ROOT), pattern=pattern):
                    self.assertNotRegex(text, pattern)

    def test_multi_clip_assembly_preserves_independent_spans_and_offsets(self) -> None:
        path = SKILLS / "template-factory/references/long-pins-and-multi-clip.md"
        text = " ".join(path.read_text().lower().split())
        for term in ("generation headroom", "locked final timing", "whole-frame",
                     "fractional", "independent picture and sound spans", "offsets",
                     "longer or shorter", "final word", "audio tails",
                     "explicit derivative adaptation approval", "unresolved",
                     "source sha-256", "derivative sha-256", "-shortest"):
            self.assertIn(term, text)
        self.assertNotIn("pad or trim its audio to the same length", text)
        self.assertNotIn("integer durations from the pin spans, rounded up", text)

    def test_empty_malformed_or_missing_timing_advice_is_rejected(self) -> None:
        invalid_advice: tuple[object, ...] = (
            None, {}, [], 14.375, "", " ", "Preserve timing.", "## Source timing",
        )
        for advice in invalid_advice:
            with self.subTest(advice=advice):
                self.assertTrue(timing_contract_errors(advice))

    def test_removing_any_required_branch_is_rejected(self) -> None:
        for path in self.documents():
            document = path.read_text()
            self.assertEqual(timing_contract_errors(document), [])
            for name, clauses in TIMING_CLAUSES.items():
                with self.subTest(path=path.relative_to(ROOT), branch=name):
                    changed = re.sub(
                        re.escape(clauses[0]), "", document, count=1, flags=re.IGNORECASE
                    )
                    self.assertIn(name, timing_contract_errors(changed))

    def test_malformed_approval_and_draft_branches_are_rejected(self) -> None:
        mutations = (
            ("adaptation", r"plus explicit derivative adaptation\s+approval", "or creative approval"),
            ("adaptation", r"`approve_for_me` does not", "`approve_for_me` does"),
            ("denied_adaptation", r"Denied or missing adaptation approval", "Creative approval"),
            ("optional_probe", r"requiring explicit approval", "requiring no approval"),
            ("draft", r"`draft: true`", '`draft: "true"`'),
        )
        for path in self.documents():
            document = path.read_text()
            for name, pattern, replacement in mutations:
                with self.subTest(path=path.relative_to(ROOT), branch=name, pattern=pattern):
                    changed, count = re.subn(pattern, replacement, document, count=1)
                    self.assertEqual(count, 1)
                    self.assertIn(name, timing_contract_errors(changed))

    def test_ambiguous_duplicate_timing_sections_are_rejected(self) -> None:
        document = self.documents()[0].read_text()
        self.assertTrue(timing_contract_errors(document + "\n## Source timing\n"))

    def test_evals_cover_fractional_tails_approval_and_failure_paths(self) -> None:
        for path in self.documents():
            if path.name != "SKILL.md":
                continue
            eval_path = path.parent / "evals" / "evals.json"
            data = json.loads(eval_path.read_text())
            self.assertEqual(data["skill_name"], path.parent.name)
            cases = {case["id"]: case for case in data["evals"]}
            self.assertEqual(len(cases), len(data["evals"]))
            for case_id, clauses in EVAL_CLAUSES.items():
                with self.subTest(skill=path.parent.name, case=case_id):
                    self.assertIn(case_id, cases)
                    case = cases[case_id]
                    self.assertTrue(case["prompt"].strip())
                    self.assertEqual(case["files"], [])
                    assertions = " ".join(" ".join(case["assertions"]).lower().split())
                    self.assertIn("no media or generation", assertions)
                    for clause in clauses:
                        self.assertIn(clause, assertions)
                    self.assertTrue(case["expected_output"].strip())

    def test_legacy_evals_no_longer_reward_destructive_recipes(self) -> None:
        for path in self.documents():
            if path.name != "SKILL.md":
                continue
            data = json.loads((path.parent / "evals" / "evals.json").read_text())
            for case in data["evals"]:
                text = " ".join(
                    (case["expected_output"] + " " + " ".join(case["assertions"])).lower().split()
                )
                for pattern in UNSAFE_RECIPES:
                    with self.subTest(skill=path.parent.name, case=case["id"], pattern=pattern):
                        self.assertNotRegex(text, pattern)


if __name__ == "__main__":
    unittest.main()
