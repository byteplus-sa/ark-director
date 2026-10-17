import contextlib
import io
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import test_showcase_selection as fixtures

showcase = fixtures.showcase
REVIEW_SHEET = (
    Path(__file__).resolve().parents[1]
    / ".agents/skills/showcase-html/assets/review-page.css"
)


class QuickReviewPlainPageTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="quick-review-test-")
        self.addCleanup(self.directory.cleanup)
        self.base = Path(self.directory.name)
        self.media = self.base / "project/elements/mira"
        self.media.mkdir(parents=True)
        self.image = self.media / "char_mira_turnaround_v03.png"
        self.image.write_bytes(b"png bytes")
        self.audio = self.base / "project/library/sfx_door_v01.wav"
        self.audio.parent.mkdir(parents=True)
        self.audio.write_bytes(b"wav bytes")
        self.video = self.base / "project/scenes/s01_sh010_t01_v01.mp4"
        self.video.parent.mkdir(parents=True)
        self.video.write_bytes(b"not a real video")
        self.out = self.base / "project/review/compare.html"
        self.out.parent.mkdir()

    def build(self, paths, **kwargs):
        with contextlib.redirect_stdout(io.StringIO()):
            return showcase.quick_review(
                [str(path) for path in paths], out_path=str(self.out), **kwargs
            )

    def test_writes_plain_html_with_a_css_file_beside_it(self):
        self.build([self.image, self.audio, self.video])
        page = self.out.read_text()
        stylesheet = self.out.with_suffix(".css")
        self.assertTrue(stylesheet.is_file())
        self.assertIn('<link rel="stylesheet" href="compare.css">', page)
        self.assertNotIn("<script", page)
        self.assertNotIn("http://", page)
        self.assertIn("<img", page)
        self.assertIn("<audio", page)
        self.assertIn("<video", page)

    def test_stylesheet_is_the_shared_offline_review_sheet(self):
        self.build([self.image])
        stylesheet = self.out.with_suffix(".css").read_text()
        self.assertEqual(stylesheet, REVIEW_SHEET.read_text())
        self.assertNotIn("@import", stylesheet)
        self.assertNotIn("url(", stylesheet)

    def test_every_class_on_the_page_has_a_selector_in_the_sheet(self):
        second_take = self.video.with_name("s01_sh010_t02_v01.mp4")
        second_take.write_bytes(b"not a real video")
        self.build([self.image, self.audio, self.video, second_take])
        page = self.out.read_text()
        selectors = set(re.findall(r"\.([A-Za-z][\w-]*)", REVIEW_SHEET.read_text()))
        classes = {
            name
            for value in re.findall(r'class="([^"]+)"', page)
            for name in value.split()
        }
        self.assertTrue(classes)
        self.assertEqual(classes - selectors, set())

    def test_media_links_are_relative_to_the_page_and_never_file_uris(self):
        self.build([self.image, self.audio, self.video])
        page = self.out.read_text()
        self.assertNotIn("file://", page)
        self.assertNotIn(str(self.base), page)
        self.assertIn('src="../elements/mira/char_mira_turnaround_v03.png"', page)
        self.assertIn('src="../library/sfx_door_v01.wav"', page)

    def test_media_outside_the_page_tree_still_links_relatively(self):
        outside = tempfile.TemporaryDirectory(prefix="quick-review-out-")
        self.addCleanup(outside.cleanup)
        self.out = Path(outside.name) / "page.html"
        self.build([self.image])
        page = self.out.read_text()
        self.assertIn('src="../', page)
        self.assertNotIn(str(self.base), page)

    def test_filenames_are_escaped_and_links_are_url_quoted(self):
        tricky = self.media / "a b <i>.png"
        tricky.write_bytes(b"png")
        self.build([tricky])
        page = self.out.read_text()
        self.assertNotIn("<i>", page)
        self.assertIn("a%20b%20%3Ci%3E.png", page)
        self.assertIn("a b &lt;i&gt;", page)

    def test_missing_file_is_skipped_but_other_media_is_kept(self):
        self.build([self.base / "missing.png", self.image])
        self.assertIn("char_mira_turnaround_v03.png", self.out.read_text())

    def test_all_files_missing_exits_without_writing(self):
        with self.assertRaises(SystemExit):
            self.build([self.base / "missing.png"])
        self.assertFalse(self.out.exists())

    def test_does_not_open_a_browser_unless_asked(self):
        with patch.object(showcase.webbrowser, "open") as opened:
            self.build([self.image])
            opened.assert_not_called()
            self.build([self.image], open_browser=True)
            opened.assert_called_once()

    def test_cli_quick_mode_does_not_open_a_browser_by_default(self):
        argv = [
            "generate_showcase.py",
            "--quick",
            str(self.image),
            "--out",
            str(self.out),
        ]
        with (
            patch.object(sys, "argv", argv),
            patch.object(showcase.webbrowser, "open") as opened,
            contextlib.redirect_stdout(io.StringIO()),
        ):
            showcase.main()
        opened.assert_not_called()
        self.assertTrue(self.out.is_file())
        self.assertTrue(self.out.with_suffix(".css").is_file())


if __name__ == "__main__":
    unittest.main()
