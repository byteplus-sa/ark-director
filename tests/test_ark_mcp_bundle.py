import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / ".agents/skills/ark-mcp"
SOURCE_REVISION = "ca2850965171b8e4f4069d55805993752e883a52"
EXPECTED_FILES = {
    "SKILL.md",
    "agents/openai.yaml",
    "references/background-job-output.md",
    "references/environment.md",
    "references/models-and-limits.md",
    "references/polling-and-artifacts.md",
    "references/tool-reference.md",
    "references/understanding-media-assets.md",
    "references/workflows.md",
}


class ArkMcpBundleTests(unittest.TestCase):
    def test_complete_upstream_bundle_has_no_obsolete_overlay_files(self):
        files = {
            str(path.relative_to(BUNDLE))
            for path in BUNDLE.rglob("*")
            if path.is_file()
        }
        self.assertEqual(files, EXPECTED_FILES)

    def test_source_provenance_and_license_are_preserved(self):
        lock = json.loads((ROOT / "skills-lock.json").read_text())["skills"]["ark-mcp"]
        catalog = json.loads(
            (ROOT / ".agents/catalog/skills.json").read_text()
        )["skills"]["ark-mcp"]
        self.assertIn("byteplus-sa/ark-mcp", lock["sourceNotes"])
        self.assertIn(SOURCE_REVISION, lock["sourceNotes"])
        self.assertEqual(catalog["source_revision"], SOURCE_REVISION)
        digest = hashlib.sha256((BUNDLE / "SKILL.md").read_bytes()).hexdigest()
        self.assertEqual(lock["computedHash"], digest)
        self.assertEqual(catalog["upstream_hash"], digest)
        license_text = (ROOT / ".agents/catalog/ark-mcp-LICENSE").read_text()
        self.assertIn("MIT License", license_text)
        self.assertIn("Copyright (c) 2026 Ark Seed MCP Server contributors", license_text)

    def test_every_upstream_file_matches_reviewed_integrity_inventory(self):
        inventory = json.loads(
            (ROOT / ".agents/catalog/integrity.json").read_text()
        )["files"]
        for relative in EXPECTED_FILES:
            with self.subTest(path=relative):
                path = BUNDLE / relative
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                self.assertEqual(inventory[str(path.relative_to(ROOT))], digest)

    def test_local_markdown_links_resolve_inside_the_bundle(self):
        for document in BUNDLE.rglob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", document.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                with self.subTest(document=document.name, target=target):
                    destination = (document.parent / target.split("#")[0]).resolve()
                    self.assertTrue(destination.is_relative_to(BUNDLE.resolve()))
                    self.assertTrue(destination.is_file())

    def test_current_create_poll_and_persistence_routes_are_documented(self):
        text = (BUNDLE / "SKILL.md").read_text()
        for tool in (
            "ark_list_models",
            "ark_job_submit",
            "ark_job_get",
            "seedance_create_task",
            "gen_task_get",
            "vod_get_task",
            "omnihuman_get_task",
            "seed_media_persist_url",
        ):
            with self.subTest(tool=tool):
                self.assertIn(tool, text)
        for tool in (
            "seedance_2_5_create_task",
            "seedance_get_task",
            "seedream_generate_image_variations",
            "media_upload_batch",
        ):
            with self.subTest(retired_tool=tool):
                self.assertNotIn(tool, text)

    def test_failure_boundary_and_partial_result_guidance_is_present(self):
        text = (BUNDLE / "references/workflows.md").read_text().lower()
        for concept in (
            "never blindly resubmit",
            "process-local",
            "partial failures",
            "queued",
            "generating",
            "persisting",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, text)
        limits = (BUNDLE / "references/models-and-limits.md").read_text()
        self.assertIn("every violation", limits)
        reference = (BUNDLE / "references/tool-reference.md").read_text()
        self.assertIn("both are rejected", reference)

    def test_claude_discovers_the_canonical_bundle_without_a_copy(self):
        alias = ROOT / ".claude/skills/ark-mcp"
        self.assertTrue(alias.is_symlink())
        self.assertEqual(alias.resolve(), BUNDLE.resolve())


if __name__ == "__main__":
    unittest.main()
