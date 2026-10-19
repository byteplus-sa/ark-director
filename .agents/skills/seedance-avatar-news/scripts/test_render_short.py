import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

SPEC = importlib.util.spec_from_file_location(
    "render_short", Path(__file__).with_name("render_short.py")
)
renderer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(renderer)


class CaptionPortabilityTests(unittest.TestCase):
    def test_cues_preserve_approved_case_and_language(self):
        for text in ("iPhone", "stra\u00dfe", "\u0130stanbul", "\u65e5\u672c\u8a9e", ""):
            with self.subTest(text=text):
                config = {
                    "segments": [{"start": 0, "end": 2, "layout": "full_m"}],
                    "end": 2,
                    "chunks": [[0, 0, text]],
                }
                cues = renderer.build_cues(config, [["word", 100, 900]])
                self.assertEqual(cues[0]["text"], text)
                self.assertEqual((cues[0]["start"], cues[0]["end"]), (0.1, 1.35))

    def test_font_uses_only_explicit_path_and_face(self):
        with (
            tempfile.NamedTemporaryFile() as selected,
            patch.object(renderer.ImageFont, "truetype") as load,
        ):
            self.assertIs(renderer.font(64, selected.name, 2), load.return_value)
            load.assert_called_once_with(selected.name, 64, index=2)

    def test_missing_empty_and_invalid_fonts_fail_without_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            invalid = Path(directory, "invalid.ttf")
            invalid.write_bytes(b"not a font")
            for path in (None, "", str(Path(directory, "missing.ttf")), str(invalid)):
                with (
                    self.subTest(path=path),
                    patch.object(renderer.ImageFont, "load_default") as fallback,
                ):
                    with self.assertRaises((ValueError, OSError)):
                        renderer.font(64, path)
                    fallback.assert_not_called()

    def test_font_path_resolves_relative_to_edl(self):
        config = {"font": "fonts/approved.ttf", "segments": []}
        renderer.resolve_paths(config, "/example/video")
        self.assertEqual(config["font"], "/example/video/fonts/approved.ttf")

    def test_badges_render_approved_copy_without_english_prefix(self):
        config = {
            "font": "approved.ttf",
            "sources_label": "Fuentes: Marca",
            "channel_label": "Canal Mixto",
        }
        with (
            tempfile.TemporaryDirectory() as directory,
            patch.object(renderer, "font"),
            patch.object(renderer, "pill", return_value=Image.new("RGBA", (10, 10))) as pill,
        ):
            paths, header = renderer.build_graphics(config, [], directory)
        self.assertEqual(paths, [])
        self.assertTrue(header.endswith("header.png"))
        self.assertEqual(
            [call.args[0] for call in pill.call_args_list],
            ["Fuentes: Marca", "Canal Mixto"],
        )


if __name__ == "__main__":
    unittest.main()
