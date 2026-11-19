import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents/skills"


def load_script(name, relative):
    spec = importlib.util.spec_from_file_location(name, SKILLS / relative)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AudioPolicyTests(unittest.TestCase):
    def test_native_audio_needs_no_finishing_pass(self):
        text = " ".join((ROOT / ".agents/contracts/audio-video-alignment.md").read_text().lower().split())
        for clause in (
            "Preserve generated or supplied audio unchanged",
            "Finalization alone does not authorize audio modification",
            "explicitly requests or approves",
            "read-only",
            "unresolved",
            "Studio",
        ):
            self.assertIn(clause.lower(), text)

    def test_active_policy_has_no_mandatory_audio_processing(self):
        patterns = (
            r"normalize every (?:delivered )?(?:master|episode)",
            r"carve by default",
            r"required whenever music plays under a voice",
            r"carve the bed before verifying",
            r"the bed is carved.{0,100}before verify",
            r"submit only a muted master",
            r"every recast submits the muted master",
            r"audio is always the silent line",
            r"native audio stays off unless requested",
            r"fix wrong words with word-scoped audio patches",
        )
        paths = [
            ROOT / "AGENTS.md",
            ROOT / "README.md",
            * (ROOT / ".agents/contracts").glob("*.md"),
            * SKILLS.rglob("*.md"),
            * SKILLS.glob("*/evals/*.json"),
        ]
        for path in paths:
            text = " ".join(path.read_text().lower().replace("**", "").split())
            for pattern in patterns:
                with self.subTest(path=path.relative_to(ROOT), pattern=pattern):
                    self.assertNotRegex(text, pattern)

    def test_source_audio_policy_is_capability_checked_not_a_mute_gate(self):
        text = (ROOT / ".agents/contracts/video-to-video-inputs.md").read_text()
        for clause in ("native", "exact supplied master", "explicit", "capability", "stream-copy"):
            self.assertIn(clause, text)
        rules = json.loads((ROOT / ".agents/contracts/rules.json").read_text())["rules"]
        self.assertNotIn("v2v.muted_source", [rule["id"] for rule in rules])
        self.assertFalse(any(
            re.search(r"binds the recorded muted source master", rule["summary"])
            for rule in rules
        ))

    def test_vendor_audio_overlay_is_recorded_without_replacing_upstream_hash(self):
        catalog = json.loads((ROOT / ".agents/catalog/skills.json").read_text())
        entry = catalog["skills"]["hyperframes-audio"]
        self.assertIn("audio-preservation overlay", entry["overlay_notes"])
        self.assertIn("re-vendoring", entry["overlay_notes"])
        self.assertTrue(entry["upstream_hash"])


@unittest.skipUnless(importlib.util.find_spec("PIL"), "Pillow inline dependency is required")
class AvatarAudioTests(unittest.TestCase):
    def test_delivery_keeps_native_audio_and_independent_tail(self):
        renderer = load_script("avatar_audio_preservation", "seedance-avatar-news/scripts/render_short.py")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "words.json").write_text('{"words":[]}')
            config = {
                "take": "take.mp4", "stt": "words.json", "out": "out.mp4",
                "end": 1, "segments": [], "chunks": [],
            }
            (root / "edit.json").write_text(json.dumps(config))
            with (
                patch("sys.argv", ["render_short.py", str(root / "edit.json")]),
                patch.object(renderer, "validate", return_value=[]),
                patch.object(renderer, "build_cues", return_value=[]),
                patch.object(renderer, "build_graphics", return_value=([], "header.png")),
                patch.object(renderer, "build_segments", return_value="picture.mp4"),
                patch.object(renderer, "run") as run,
            ):
                renderer.main()
        command = run.call_args.args[0]
        self.assertEqual(command[command.index("-c:a") + 1], "copy")
        self.assertIn("1:a:0?", command)
        for option in ("-af", "-ar", "-b:a", "-shortest", "-t"):
            self.assertNotIn(option, command)


class ShowreelAudioTests(unittest.TestCase):
    def test_default_showreel_has_no_audio_filters(self):
        showreel = load_script("showreel_audio_preservation", "lark-showcase-aigc/scripts/assemble_showreel.py")
        with patch.object(showreel, "assemble", return_value={}) as assemble:
            showreel.main(["a.mp4", "b.mp4", "--out", "reel.mp4"])
        self.assertEqual(assemble.call_args.args[2:4], (0, 0))

    def test_legacy_gain_and_limiter_options_are_removed(self):
        portfolio = load_script("portfolio_audio_preservation", "showcase-html/scripts/portfolio.py")
        for flag in ("--target-lufs", "--limit"):
            with self.subTest(flag=flag), tempfile.TemporaryDirectory() as directory:
                with self.assertRaises(SystemExit) as caught:
                    portfolio.main([str(Path(directory) / "out"), "project", flag, "1"])
                self.assertEqual(caught.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
