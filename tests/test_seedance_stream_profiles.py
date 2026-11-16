import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class StreamProfileContractTests(unittest.TestCase):
    def setUp(self):
        self.text = (ROOT / ".agents/skills/color-grade-palettes/SKILL.md").read_text()
        self.decisions = {
            cells[1].strip(): cells[2].strip()
            for line in self.text.splitlines()
            if line.startswith("|")
            for cells in [line.split("|")]
            if len(cells) == 4
        }

    def test_synthetic_limited_full_and_hdr_profiles_have_distinct_decisions(self):
        fixtures = {
            "HEVC / yuv420p10le / limited / BT.709 matrix, primaries, transfer":
                "Matching BT.709 baseline",
            "HEVC / yuv420p10le / full / BT.709 matrix, primaries, transfer":
                "Preserve full-range interpretation",
            "HEVC / yuv420p10le / limited / BT.2020 matrix and primaries, PQ transfer":
                "Preserve HDR interpretation",
        }
        for measured, expected in fixtures.items():
            with self.subTest(profile=measured):
                self.assertIn(expected, self.decisions[measured])

    def test_unknown_and_conflicting_synthetic_profiles_remain_unresolved(self):
        for measured in (
            "Any codec / unknown pixel format or color tags",
            "Any codec / conflicting range, matrix, primaries or transfer evidence",
        ):
            with self.subTest(profile=measured):
                self.assertTrue(self.decisions[measured].startswith("Unresolved"))

    def test_source_master_and_no_grade_locks_are_preserved(self):
        self.assertIn("Preserve source/master bytes and color locks", self.text)
        self.assertIn("do not guess or relabel the master", self.text)
        self.assertIn("explicit ungraded delivery add no unauthorized look", self.text)


if __name__ == "__main__":
    unittest.main()
