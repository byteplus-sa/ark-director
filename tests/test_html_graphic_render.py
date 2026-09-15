from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents/skills/html-graphic-render/scripts/render_html.py"
SPEC = importlib.util.spec_from_file_location("html_graphic_render", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class HtmlGraphicRenderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory(prefix="html-graphic-render-test-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def write_html(self, body: str, style: str = "") -> Path:
        source = self.root / "card_v01.html"
        source.write_text(
            "<!doctype html><html><head><style>"
            + style
            + "</style></head><body>"
            + body
            + "</body></html>",
            encoding="utf-8",
        )
        return source

    def namespace(
        self, source: Path, output: Path, **values: object
    ) -> argparse.Namespace:
        defaults: dict[str, object] = {
            "source": source,
            "output": output,
            "width": 1080,
            "height": 1920,
            "scale": 1,
            "asset_root": self.root,
            "record": None,
            "browser": None,
            "copy": [],
            "transparent": False,
            "require_local_font": None,
            "overwrite": False,
            "timeout": 30.0,
        }
        defaults.update(values)
        return argparse.Namespace(**defaults)

    def test_audit_preserves_exact_copy_and_hashes_local_assets(self) -> None:
        asset = self.root / "product.svg"
        asset.write_text("<svg xmlns='http://www.w3.org/2000/svg'/>", encoding="utf-8")
        source = self.write_html(
            "<h1 data-copy-key='headline'>PICK YOUR POWER</h1><img src='product.svg'>"
        )
        files, copy = MODULE.audit_sources(source, self.root)
        self.assertEqual(copy, {"headline": "PICK YOUR POWER"})
        self.assertEqual(
            files["product.svg"], hashlib.sha256(asset.read_bytes()).hexdigest()
        )

    def test_audit_rejects_remote_resources_scripts_and_animation(self) -> None:
        cases = [
            ("<img src='https://example.com/product.png'>", "", "Remote asset"),
            ("<script src='local.js'></script>", "", "Active or temporal"),
            ("<iframe srcdoc='<p>nested</p>'></iframe>", "", "Active or temporal"),
            ("<base href='assets/'>", "", "Active or temporal"),
            ("<img src='data:image/png;base64,AAAA'>", "", "Data URLs"),
            ("<p>Copy</p>", "p { animation: pulse 1s; }", "animation"),
            ("<p>Copy</p>", "p { transition-duration: 1s; }", "transition"),
            ("<p>Copy</p>", "p { anim\\61 tion: pulse 1s; }", "animation"),
        ]
        for body, style, expected in cases:
            with self.subTest(expected=expected):
                source = self.write_html(body, style)
                with self.assertRaisesRegex(ValueError, expected):
                    MODULE.audit_sources(source, self.root)

    def test_execute_rejects_copy_mismatch_before_browser_launch(self) -> None:
        source = self.write_html("<h1 data-copy-key='headline'>PICK YOUR POWER</h1>")
        arguments = self.namespace(
            source,
            self.root / "card_v01.png",
            copy=[("headline", "Pick Your Power")],
            browser=self.root / "missing-browser",
        )
        with self.assertRaisesRegex(ValueError, "Exact copy mismatch"):
            MODULE.execute(arguments)

    def test_execute_rejects_undeclared_exact_copy(self) -> None:
        source = self.write_html("<h1 data-copy-key='headline'>PICK YOUR POWER</h1>")
        with self.assertRaisesRegex(ValueError, "matching --copy"):
            MODULE.execute(self.namespace(source, self.root / "card_v01.png"))

    def test_execute_rejects_output_escape_and_oversized_raster(self) -> None:
        source = self.write_html("<p>Poster</p>")
        with self.assertRaisesRegex(ValueError, "escapes asset root"):
            MODULE.execute(self.namespace(source, self.root.parent / "escape.png"))
        with self.assertRaisesRegex(ValueError, "8192"):
            MODULE.execute(self.namespace(source, self.root / "large.png", width=9000))
        with self.assertRaisesRegex(ValueError, "Timeout"):
            MODULE.execute(self.namespace(source, self.root / "timeout.png", timeout=0))

    def test_execute_rejects_record_output_and_input_aliases(self) -> None:
        source = self.write_html("<p>Poster</p>")
        output = self.root / "card_v01.png"
        with self.assertRaisesRegex(ValueError, "different paths"):
            MODULE.execute(self.namespace(source, output, record=output))
        with self.assertRaisesRegex(ValueError, "different paths"):
            MODULE.execute(
                self.namespace(
                    source,
                    self.root / "Card.png",
                    record=self.root / "card.png",
                )
            )
        with self.assertRaisesRegex(ValueError, "different paths"):
            MODULE.execute(
                self.namespace(
                    source,
                    self.root / "Caf\u00e9.png",
                    record=self.root / "Cafe\u0301.png",
                )
            )
        with self.assertRaisesRegex(ValueError, "aliases source or input"):
            MODULE.execute(
                self.namespace(source, output, record=source, overwrite=True)
            )

    def test_execute_enforces_local_font_policy_before_browser_launch(self) -> None:
        source = self.write_html("<p>Poster</p>")
        with self.assertRaisesRegex(ValueError, "project-local font"):
            MODULE.execute(
                self.namespace(
                    source,
                    self.root / "card_v01.png",
                    require_local_font="Brand Sans",
                )
            )

    def test_execute_rejects_local_font_source_with_required_family(self) -> None:
        font = self.root / "brand.woff2"
        font.write_bytes(b"not-used")
        source = self.write_html(
            "<p data-copy-key='headline'>Poster</p>",
            "@font-face{font-family:'Brand';"
            "src:local('Arial'),url('brand.woff2') format('woff2');}"
            "p{font-family:'Brand';}",
        )
        with self.assertRaisesRegex(ValueError, r"local\(\) font sources"):
            MODULE.execute(
                self.namespace(
                    source,
                    self.root / "card_v01.png",
                    copy=[("headline", "Poster")],
                    require_local_font="Brand",
                    browser=self.root / "missing-browser",
                )
            )

    def test_audit_rejects_escaped_css_and_legacy_background_escape(self) -> None:
        outside = self.root.parent / f"{self.root.name}-outside.svg"
        outside.write_text(
            "<svg xmlns='http://www.w3.org/2000/svg'/>", encoding="utf-8"
        )
        self.addCleanup(outside.unlink, missing_ok=True)
        source = self.write_html(
            "<p>Poster</p>", f"p{{background:u\\72l({outside.as_uri()})}}"
        )
        with self.assertRaisesRegex(ValueError, "Unsupported asset scheme"):
            MODULE.audit_sources(source, self.root)
        source = self.write_html(f"<body background='{outside.as_uri()}'>Poster</body>")
        with self.assertRaisesRegex(ValueError, "Unsupported asset scheme"):
            MODULE.audit_sources(source, self.root)

    def test_audit_rejects_symlink_asset_escape(self) -> None:
        outside = self.root.parent / f"{self.root.name}-outside.svg"
        outside.write_text(
            "<svg xmlns='http://www.w3.org/2000/svg'/>", encoding="utf-8"
        )
        self.addCleanup(outside.unlink, missing_ok=True)
        link = self.root / "outside.svg"
        try:
            link.symlink_to(outside)
        except OSError as error:
            self.skipTest(str(error))
        source = self.write_html("<img src='outside.svg'>")
        with self.assertRaisesRegex(ValueError, "escapes asset root"):
            MODULE.audit_sources(source, self.root)

    def test_audit_tracks_extensionless_stylesheet_and_visual_roles(self) -> None:
        stylesheet = self.root / "theme"
        image = self.root / "hero.asset"
        stylesheet.write_text(
            "body{background-image:url('hero.asset');}", encoding="utf-8"
        )
        image.write_bytes(b"image-placeholder")
        source = self.root / "card_v01.html"
        source.write_text(
            "<!doctype html><html><head><link rel='stylesheet' href='theme'>"
            "</head><body>Poster</body></html>",
            encoding="utf-8",
        )
        files, _, _, roles = MODULE.audit_sources_with_snapshots(source, self.root)
        self.assertEqual(set(files), {"card_v01.html", "hero.asset", "theme"})
        self.assertEqual(roles["theme"], {"stylesheet"})
        self.assertEqual(roles["hero.asset"], {"visual"})

    def test_render_record_schema_rejects_incomplete_provenance(self) -> None:
        with self.assertRaisesRegex(ValueError, "schema validation"):
            MODULE.validate_render_record(
                {"schema_version": 1, "generation": "deterministic_html"}
            )

    def test_audit_rejects_active_external_svg(self) -> None:
        svg = self.root / "animated.svg"
        svg.write_text(
            "<svg xmlns='http://www.w3.org/2000/svg'>"
            "<circle r='10'><animate attributeName='r' dur='1s'/></circle></svg>",
            encoding="utf-8",
        )
        source = self.write_html("<img src='animated.svg'>")
        with self.assertRaisesRegex(ValueError, "temporal SVG"):
            MODULE.audit_sources(source, self.root)

    def test_loopback_server_rejects_unaudited_asset(self) -> None:
        with MODULE.AssetServer({"card.html": b"<html></html>"}) as server:
            with self.assertRaises(HTTPError):
                urlopen(server.url("outside.svg"), timeout=5)
            self.assertEqual(server.denied, {"outside.svg"})

    def test_loopback_server_serves_immutable_audited_snapshot(self) -> None:
        source = self.root / "card.html"
        source.write_bytes(b"changed-on-disk")
        with (
            MODULE.AssetServer({"card.html": b"audited-snapshot"}) as server,
            urlopen(server.url("card.html"), timeout=5) as response,
        ):
            self.assertEqual(response.read(), b"audited-snapshot")

    def test_verify_current_inputs_rejects_post_audit_change(self) -> None:
        source = self.write_html("<p>Poster</p>")
        files, _, _, _ = MODULE.audit_sources_with_snapshots(source, self.root)
        source.write_text("<html><head></head><body>Changed</body></html>")
        with self.assertRaisesRegex(ValueError, "Input changed after audit"):
            MODULE.verify_current_inputs(self.root, files)

    def test_render_pair_rolls_back_when_record_promotion_fails(self) -> None:
        output = self.root / "card_v01.png"
        record = self.root / "render_card_v01.json"
        output.write_bytes(b"old-output")
        record.write_bytes(b"old-record")
        staged_output = MODULE.stage_bytes(output, b"new-output", ".png")
        original_replace = MODULE.replace_file
        failed = False

        def fail_record_once(source: Path, destination: Path) -> None:
            nonlocal failed
            if destination.resolve() == record.resolve() and not failed:
                failed = True
                raise OSError("injected record promotion failure")
            original_replace(source, destination)

        MODULE.replace_file = fail_record_once
        try:
            with self.assertRaisesRegex(OSError, "injected record"):
                MODULE.promote_render_pair(
                    self.root,
                    output,
                    record,
                    staged_output,
                    {"render": "new"},
                    {
                        output.resolve(): hashlib.sha256(b"old-output").hexdigest(),
                        record.resolve(): hashlib.sha256(b"old-record").hexdigest(),
                    },
                )
        finally:
            MODULE.replace_file = original_replace
        self.assertEqual(output.read_bytes(), b"old-output")
        self.assertEqual(record.read_bytes(), b"old-record")
        self.assertFalse(MODULE.transaction_path(record).exists())

    def test_transaction_setup_failure_cleans_staged_files_and_backups(self) -> None:
        output = self.root / "card_v01.png"
        record = self.root / "render_card_v01.json"
        output.write_bytes(b"old-output")
        record.write_bytes(b"old-record")
        staged_output = MODULE.stage_bytes(output, b"new-output", ".png")
        expected_targets = {
            output.resolve(): hashlib.sha256(b"old-output").hexdigest(),
            record.resolve(): hashlib.sha256(b"old-record").hexdigest(),
        }
        original_stage_bytes = MODULE.stage_bytes
        backup_count = 0

        def fail_second_backup(path: Path, content: bytes, suffix: str) -> Path:
            nonlocal backup_count
            if suffix == ".backup":
                backup_count += 1
                if backup_count == 2:
                    raise OSError("injected backup failure")
            return original_stage_bytes(path, content, suffix)

        MODULE.stage_bytes = fail_second_backup
        try:
            with self.assertRaisesRegex(OSError, "injected backup"):
                MODULE.promote_render_pair(
                    self.root,
                    output,
                    record,
                    staged_output,
                    {"render": "new"},
                    expected_targets,
                )
        finally:
            MODULE.stage_bytes = original_stage_bytes
        self.assertEqual(output.read_bytes(), b"old-output")
        self.assertEqual(record.read_bytes(), b"old-record")
        self.assertEqual(list(self.root.glob(".*")), [])

    def test_staging_write_failure_removes_temporary_files(self) -> None:
        target = self.root / "card_v01.png"
        original_fsync = MODULE.os.fsync

        def fail_fsync(descriptor: int) -> None:
            raise OSError("injected fsync failure")

        MODULE.os.fsync = fail_fsync
        try:
            with self.assertRaisesRegex(OSError, "injected fsync"):
                MODULE.stage_bytes(target, b"new-output", ".png")
            with self.assertRaisesRegex(OSError, "injected fsync"):
                MODULE.atomic_json(self.root / "record.json", {"render": "new"})
        finally:
            MODULE.os.fsync = original_fsync
        self.assertEqual(list(self.root.glob(".*")), [])

    def test_prepared_render_transaction_recovers_after_interruption(self) -> None:
        output = self.root / "card_v01.png"
        record = self.root / "render_card_v01.json"
        output.write_bytes(b"old-output")
        record.write_bytes(b"old-record")
        staged_output = MODULE.stage_bytes(output, b"new-output", ".png")
        staged_record = MODULE.stage_bytes(record, b"new-record", ".json.tmp")
        artifacts = [
            MODULE.transaction_artifact(self.root, output, staged_output),
            MODULE.transaction_artifact(self.root, record, staged_record),
        ]
        MODULE.atomic_json(
            MODULE.transaction_path(record),
            {"schema_version": 1, "state": "prepared", "artifacts": artifacts},
        )
        for artifact in artifacts:
            final, staged, _ = MODULE.transaction_files(self.root, artifact)
            MODULE.replace_file(staged, final)
        MODULE.recover_transaction(self.root, output, record)
        self.assertEqual(output.read_bytes(), b"old-output")
        self.assertEqual(record.read_bytes(), b"old-record")
        self.assertFalse(MODULE.transaction_path(record).exists())

    def test_render_target_lock_serializes_a_shared_output(self) -> None:
        output = self.root / "card_v01.png"
        record = self.root / "render_card_v01.json"
        competing_record = self.root / "alternate_record.json"
        attempting = threading.Event()
        acquired = threading.Event()

        def acquire_same_lock() -> None:
            attempting.set()
            with MODULE.render_target_lock(self.root, output, competing_record):
                acquired.set()

        thread = threading.Thread(target=acquire_same_lock)
        with MODULE.render_target_lock(self.root, output, record):
            thread.start()
            self.assertTrue(attempting.wait(1))
            self.assertFalse(acquired.wait(0.1))
        self.assertTrue(acquired.wait(2))
        thread.join(timeout=2)
        self.assertFalse(thread.is_alive())

    def test_render_pair_rejects_interleaved_target_change(self) -> None:
        output = self.root / "card_v01.png"
        record = self.root / "render_card_v01.json"
        output.write_bytes(b"original-output")
        record.write_bytes(b"original-record")
        expected_targets = {
            output.resolve(): hashlib.sha256(b"original-output").hexdigest(),
            record.resolve(): hashlib.sha256(b"original-record").hexdigest(),
        }
        output.write_bytes(b"user-edit")
        staged_output = MODULE.stage_bytes(output, b"new-output", ".png")
        with self.assertRaisesRegex(ValueError, "changed during rendering"):
            MODULE.promote_render_pair(
                self.root,
                output,
                record,
                staged_output,
                {"render": "new"},
                expected_targets,
            )
        self.assertEqual(output.read_bytes(), b"user-edit")
        self.assertEqual(record.read_bytes(), b"original-record")
        self.assertFalse(MODULE.transaction_path(record).exists())

    def test_browser_smoke_renders_repeatable_transparent_png_and_record(self) -> None:
        try:
            browser = MODULE.resolve_browser(None)
        except ValueError as error:
            self.skipTest(str(error))
        source = self.write_html(
            "<main><h1 data-copy-key='headline'>PICK YOUR POWER</h1></main>",
            "html,body{margin:0;width:100%;height:100%;background:transparent;}"
            "main{width:100%;height:100%;display:grid;place-items:center;}"
            "h1{color:#123b70;font:700 22px Arial,sans-serif;}",
        )
        hashes = []
        for version in (1, 2):
            output = self.root / f"overlay_v0{version}.png"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(source),
                    str(output),
                    "--asset-root",
                    str(self.root),
                    "--width",
                    "108",
                    "--height",
                    "192",
                    "--transparent",
                    "--copy",
                    "headline=PICK YOUR POWER",
                    "--browser",
                    str(browser),
                ],
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            response = json.loads(result.stdout)
            self.assertEqual((response["width"], response["height"]), (108, 192))
            self.assertTrue(response["has_alpha_channel"])
            self.assertTrue(response["has_transparency"])
            record = json.loads(
                (self.root / f"render_overlay_v0{version}.json").read_text()
            )
            MODULE.validate_render_record(record)
            self.assertEqual(record["copy"][0]["text"], "PICK YOUR POWER")
            hashes.append(response["sha256"])
        self.assertEqual(hashes[0], hashes[1])

    def test_browser_smoke_rejects_invalid_required_font(self) -> None:
        try:
            browser = MODULE.resolve_browser(None)
        except ValueError as error:
            self.skipTest(str(error))
        font = self.root / "broken.woff2"
        font.write_bytes(b"not-a-font")
        source = self.write_html(
            "<h1 data-copy-key='headline'>PICK YOUR POWER</h1>",
            "@font-face{font-family:'Broken';src:url('broken.woff2') format('woff2');}"
            "h1{font-family:'Broken';}",
        )
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(source),
                str(self.root / "card_v01.png"),
                "--asset-root",
                str(self.root),
                "--width",
                "108",
                "--height",
                "192",
                "--copy",
                "headline=PICK YOUR POWER",
                "--require-local-font",
                "Broken",
                "--browser",
                str(browser),
            ],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("Required local font failed", result.stderr)
        self.assertFalse((self.root / "card_v01.png").exists())

    def test_browser_smoke_accepts_audited_required_font(self) -> None:
        try:
            browser = MODULE.resolve_browser(None)
        except ValueError as error:
            self.skipTest(str(error))
        font = self.root / "inter.woff2"
        bundled_font = (
            ROOT
            / ".agents/skills/hyperframes-creative/frame-presets/code-editorial/fonts/Inter-400.woff2"
        )
        font.write_bytes(bundled_font.read_bytes())
        source = self.write_html(
            "<h1 data-copy-key='headline'>PICK YOUR POWER</h1>",
            "@font-face{font-family:'Required';src:url('inter.woff2') format('woff2');}"
            "h1{font-family:'Required';}",
        )
        output = self.root / "card_v01.png"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(source),
                str(output),
                "--asset-root",
                str(self.root),
                "--width",
                "108",
                "--height",
                "192",
                "--copy",
                "headline=PICK YOUR POWER",
                "--require-local-font",
                "Required",
                "--browser",
                str(browser),
            ],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        record = json.loads((self.root / "render_card_v01.json").read_text())
        self.assertEqual(record["renderer"]["font_policy"], "project_local_required")
        self.assertEqual(record["inputs"][0]["path"], "inter.woff2")

    def test_browser_smoke_rejects_unused_required_font(self) -> None:
        try:
            browser = MODULE.resolve_browser(None)
        except ValueError as error:
            self.skipTest(str(error))
        font = self.root / "inter.woff2"
        bundled_font = (
            ROOT
            / ".agents/skills/hyperframes-creative/frame-presets/code-editorial/fonts/Inter-400.woff2"
        )
        font.write_bytes(bundled_font.read_bytes())
        source = self.write_html(
            "<h1 data-copy-key='headline'>PICK YOUR POWER</h1>",
            "@font-face{font-family:'Required';src:url('inter.woff2') format('woff2');}"
            "h1{font-family:Arial,sans-serif;}",
        )
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(source),
                str(self.root / "card_v01.png"),
                "--asset-root",
                str(self.root),
                "--width",
                "108",
                "--height",
                "192",
                "--copy",
                "headline=PICK YOUR POWER",
                "--require-local-font",
                "Required",
                "--browser",
                str(browser),
            ],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("Required local font failed", result.stderr)
        self.assertFalse((self.root / "card_v01.png").exists())

    def test_browser_smoke_rejects_corrupt_css_background_image(self) -> None:
        try:
            browser = MODULE.resolve_browser(None)
        except ValueError as error:
            self.skipTest(str(error))
        for asset_name in ("broken.png", "broken"):
            with self.subTest(asset_name=asset_name):
                (self.root / asset_name).write_bytes(b"not-an-image")
                source = self.write_html(
                    "<main>Poster</main>",
                    "html,body{width:100%;height:100%;margin:0;}"
                    f"body{{background-image:url('{asset_name}');}}",
                )
                result = subprocess.run(
                    [
                        sys.executable,
                        str(SCRIPT),
                        str(source),
                        str(self.root / "card_v01.png"),
                        "--asset-root",
                        str(self.root),
                        "--width",
                        "108",
                        "--height",
                        "192",
                        "--browser",
                        str(browser),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    check=False,
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn("failed to decode", result.stderr)
                self.assertFalse((self.root / "card_v01.png").exists())


if __name__ == "__main__":
    unittest.main()
