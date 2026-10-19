from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents/skills/html-graphic-render/scripts/typography_series.py"
SPEC = importlib.util.spec_from_file_location("typography_series", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.root = {}
        self.words = []
        self.in_word = False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        if tag == "html":
            self.root = dict(attrs)
        if tag == "p":
            self.in_word = True

    def handle_endtag(self, tag):
        if tag == "p":
            self.in_word = False

    def handle_data(self, data):
        if self.in_word:
            self.words.append(data)


class TypographySeriesTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.font = self.root / "\u5b57\u4f53 ' (1).ttf"
        self.font.write_bytes(b"synthetic-font")
        self.output = self.root / "cards"
        self.commands = []

    def arguments(self, words, *extra):
        return [
            str(SCRIPT), "--out-dir", str(self.output), "--prefix", "card",
            "--words", words, "--width", "640", "--height", "360",
            "--font-file", str(self.font), "--font-family", "\u5b57\u4f53",
            "--font-size", "36", *extra,
        ]

    def render(self, command, **kwargs):
        self.commands.append(command)
        Path(command[3]).write_bytes(
            b"\x89PNG\r\n\x1a\n" + b"\0" * 8 + struct.pack(">II", 640, 360)
        )
        return subprocess.CompletedProcess(command, 0)

    def run_series(self, words, *extra):
        with (
            mock.patch.object(sys, "argv", self.arguments(words, *extra)),
            mock.patch.object(MODULE.subprocess, "run", side_effect=self.render),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            self.assertEqual(MODULE.main(), 0)
        return sorted(self.output.glob("*.html"))

    def test_unicode_mixed_duplicate_and_punctuation_copy_get_distinct_stable_ids(self):
        words = [
            "\u4f60\u597d", "\u0645\u0631\u062d\u0628\u0627", "Brand \u4f60\u597d",
            "Brand \u0645\u0631\u062d\u0628\u0627", "A-B", "A B", "A B", "!!!",
            "e\u0301", "\u00e9", "<script>& |",
        ]
        files = self.run_series(",".join(words))
        self.assertEqual(len(files), len(words))
        self.assertEqual(
            [Document(path.read_text(encoding="utf-8")).words[0] for path in files], words
        )
        for path in files:
            self.assertRegex(path.name, r"^card_[0-9]{3,}_v01\.html$")
        second = self.root / "again"
        original = self.output
        self.output = second
        repeated = self.run_series(",".join(words))
        self.assertEqual([path.name for path in files], [path.name for path in repeated])
        self.assertEqual(
            (original / "manifest.md").read_bytes(), (second / "manifest.md").read_bytes()
        )

    def test_default_omits_language_and_direction(self):
        document = Document(self.run_series("Hello")[0].read_text())
        self.assertNotIn("lang", document.root)
        self.assertNotIn("dir", document.root)

    def test_explicit_language_and_direction_are_preserved(self):
        for language, direction in (("ar", "rtl"), ("zh-Hant", "ltr"), ("und", "auto")):
            with self.subTest(language=language):
                files = self.run_series(
                    "Hello", "--language", language, "--direction", direction, "--overwrite"
                )
                document = Document(files[0].read_text())
                self.assertEqual(document.root, {"lang": language, "dir": direction})
                self.assertIn("--overwrite", self.commands[-1])

    def test_font_names_never_become_css_or_url_syntax(self):
        family = 'Display"; } @import url("https://invalid.example"); /*'
        self.run_series("Hello", "--font-family", family)
        css = (self.output / "card_series.css").read_text()
        self.assertNotIn(family, css)
        self.assertNotIn("@import", css)
        self.assertNotIn(self.font.name, css)
        self.assertIn("font-family: 'series-font'", css)
        copied = list((self.output / "fonts").glob("*.ttf"))
        self.assertEqual(len(copied), 1)
        self.assertEqual(copied[0].read_bytes(), self.font.read_bytes())
        self.assertEqual(
            self.commands[0][self.commands[0].index("--require-local-font") + 1],
            "series-font",
        )

    def test_invalid_locale_or_prefix_fails_before_writes(self):
        for flag, value in (
            ("--prefix", "../escape"), ("--prefix", 'x" onload="x'),
            ("--language", 'ar" onload="x'), ("--direction", "sideways"),
        ):
            with self.subTest(flag=flag, value=value), self.assertRaises(SystemExit):
                self.run_series("Hello", flag, value)
            self.assertFalse(self.output.exists())

    def test_empty_words_and_missing_font_fail_before_writes(self):
        for words in ("", " , , "):
            with self.assertRaises(SystemExit):
                self.run_series(words)
        self.font.unlink()
        with self.assertRaises(SystemExit):
            self.run_series("Hello")
        self.assertFalse(self.output.exists())

    def test_output_root_and_symlink_escapes_fail_before_writes(self):
        with self.assertRaises(SystemExit):
            self.run_series("Hello", "--asset-root", str(self.root / "elsewhere"))
        self.assertFalse(self.output.exists())
        self.output.mkdir()
        outside = self.root / "outside"
        outside.mkdir()
        (self.output / "fonts").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(SystemExit):
            self.run_series("Hello")
        self.assertEqual(list(outside.iterdir()), [])

    @unittest.skipUnless(os.environ.get("PORTABILITY_FONT"), "set PORTABILITY_FONT for local render")
    def test_local_font_render_smoke(self):
        shutil.copyfile(os.environ["PORTABILITY_FONT"], self.font)
        result = subprocess.run(
            [sys.executable, *self.arguments(
                "\u4f60\u597d,\u0645\u0631\u062d\u0628\u0627,Brand 123",
                "--direction", "auto",
            )],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        records = sorted(self.output.glob("render_*.json"))
        self.assertEqual(len(records), 3)
        for path in records:
            record = json.loads(path.read_text())
            self.assertEqual(record["renderer"]["font_policy"], "project_local_required")
        for path in self.output.glob("*.png"):
            self.assertEqual(MODULE.png_dimensions(path), (640, 360))


if __name__ == "__main__":
    unittest.main()
