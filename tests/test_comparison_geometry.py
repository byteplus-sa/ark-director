import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / ".agents/skills/ffmpeg-side-by-side-comparison/SKILL.md"


@unittest.skipUnless(shutil.which("ffmpeg"), "FFmpeg is required for comparison renders")
class ComparisonGeometryTests(unittest.TestCase):
    def test_review_tiles_preserve_display_geometry(self):
        section = SKILL.read_text().split("## Core recipe", 1)[1]
        command = section.split("```bash\n", 1)[1].split("\n```", 1)[0]
        cases = (
            ("180x320", "1/1", 40),
            ("320x180", "1/1", 40),
            ("180x320", "2/1", 20),
        )
        with tempfile.TemporaryDirectory() as folder:
            for before, after in ((0, 0), (0, 1), (1, 1), (2, 0)):
                size, sar, width = cases[before]
                with self.subTest(before=cases[before], after=cases[after]):
                    next_size, next_sar, next_width = cases[after]
                    for name, dimensions, ratio, box_width in (
                        ("before.mp4", size, sar, width),
                        ("after.mp4", next_size, next_sar, next_width),
                    ):
                        source = (
                            f"color=black:s={dimensions}:d=0.2,"
                            f"drawbox=x=60:y=60:w={box_width}:h=40:c=white:t=fill,setsar={ratio}"
                        )
                        subprocess.run(
                            ["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", source,
                             "-f", "lavfi", "-i", "anullsrc", "-t", "0.2", "-c:v", "libx264",
                             "-c:a", "aac", name], cwd=folder, check=True,
                        )
                    subprocess.run(["bash", "-ec", command], cwd=folder, check=True, capture_output=True)
                    frame = subprocess.check_output(
                        ["ffmpeg", "-loglevel", "error", "-i", "compare.mp4", "-frames:v", "1",
                         "-pix_fmt", "gray", "-f", "rawvideo", "-"], cwd=folder,
                    )
                    self.assertEqual(len(frame), 1280 * 360)
                    for left in (0, 640):
                        rows = [frame[start + left:start + left + 640] for start in range(0, len(frame), 1280)]
                        widths = [sum(value > 128 for value in row) for row in rows]
                        height = sum(width > 0 for width in widths)
                        self.assertGreater(height, 20)
                        self.assertLessEqual(abs(max(widths) - height), 2)
