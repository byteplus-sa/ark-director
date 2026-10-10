import contextlib
import datetime
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".agents/scripts"))
import studio_project as studio
from validate_request import schema_findings

PROBE = {
    "format": {"duration": "10.0"},
    "streams": [
        {
            "codec_type": "video",
            "codec_name": "h264",
            "width": 1280,
            "height": 720,
            "pix_fmt": "yuv420p",
            "r_frame_rate": "24/1",
        },
        {
            "codec_type": "audio",
            "codec_name": "aac",
            "sample_rate": "48000",
            "channels": 2,
        },
    ],
}


PROBE_SUMMARY = {"duration_s": 10.0, "streams": [{"codec_type": "video"}]}
CHECK_OK = json.dumps({"ok": True, "browserSkipped": False})


def fake_runner(returncode=0, stdout=None, stderr=""):
    calls = []

    def runner(argv, **kwargs):
        calls.append((argv, kwargs))
        return subprocess.CompletedProcess(
            argv,
            returncode,
            stdout if stdout is not None else json.dumps(PROBE),
            stderr,
        )

    runner.calls = calls
    return runner


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class StudioProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name).resolve() / "demo"
        self.project.mkdir()
        self.write_project("approve_for_me")

    def write_project(self, mode):
        (self.project / "project.md").write_text(
            f"---\napproval_mode: {mode}\n---\n\n# Demo\n"
        )

    def add_shot(
        self,
        shot_id="s01_sh010",
        scene="scene-01",
        takes=None,
        selected=None,
        active=None,
        duration=4,
        extra="",
    ):
        directory = self.project / "scenes" / scene / shot_id
        directory.mkdir(parents=True, exist_ok=True)
        takes = (
            takes
            if takes is not None
            else {f"{shot_id}_t01_v01.mp4": b"take-one-" + shot_id.encode()}
        )
        listing = ""
        for name, data in takes.items():
            (directory / name).write_bytes(data)
            listing += (
                f"- filename: {name}\n  sha256: {sha(data)}\n  duration_s: {duration}\n"
            )
        front = f'shot_id: {shot_id}\nstatus: review\nduration_s: {duration}\naspect: "16:9"\nresolution: 720p\n'
        if listing:
            front += "takes:\n" + listing
        if selected:
            front += f"selected_variant: {selected}\n"
        if active:
            front += f"active_take: {active}\n"
        (directory / "shot.md").write_text(
            f"---\n{front}{extra}---\n\n# Opening street\n"
        )
        return directory

    @property
    def root(self):
        return self.project / "studio"

    def test_sync_creates_frames_storyboard_assets_and_provenance(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        self.add_shot(
            "s01_sh020",
            takes={"s01_sh020_t01_v01.mp4": b"two"},
            selected="s01_sh020_t01_v01.mp4",
            duration=6,
        )
        report = studio.sync(self.project)
        self.assertEqual(report.added, ["s01_sh010", "s01_sh020"])
        index = (self.root / "index.html").read_text()
        self.assertIn('data-composition-src="compositions/s01_sh010.html"', index)
        self.assertIn('data-start="4"', index)
        self.assertIn(
            'data-composition-id="main" data-start="0" data-duration="10"', index
        )
        asset = f"s01_sh010_t01_v01__{sha(b'take-one-s01_sh010')[:12]}.mp4"
        self.assertEqual(
            (self.root / "assets" / asset).read_bytes(), b"take-one-s01_sh010"
        )
        self.assertIn(
            f'src="assets/{asset}"',
            (self.root / "compositions/s01_sh010.html").read_text(),
        )
        storyboard = (self.root / "STORYBOARD.md").read_text()
        self.assertIn("## Frame 1 — s01_sh010", storyboard)
        self.assertIn("## Frame 2 — s01_sh020", storyboard)
        self.assertIn("- duration: 6s", storyboard)
        record = json.loads((self.root / "provenance.json").read_text())
        self.assertEqual(
            [frame["shot_id"] for frame in record["frames"]], ["s01_sh010", "s01_sh020"]
        )
        self.assertEqual(schema_findings(record, "studio-provenance.schema.json"), [])

    def test_generated_files_are_readable_by_other_tools(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        for name in ("index.html", "STORYBOARD.md", "provenance.json"):
            self.assertEqual((self.root / name).stat().st_mode & 0o777, 0o644, name)

    def test_sync_is_idempotent(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        before = {
            name: (self.root / name).read_bytes()
            for name in ("index.html", "STORYBOARD.md", "provenance.json")
        }
        report = studio.sync(self.project)
        self.assertEqual(report.added, [])
        self.assertEqual(report.preserved, ["s01_sh010"])
        for name, content in before.items():
            self.assertEqual((self.root / name).read_bytes(), content, name)

    def test_swap_made_in_studio_is_preserved_and_reported(self):
        directory = self.add_shot(
            takes={"s01_sh010_t01_v01.mp4": b"one", "s01_sh010_t02_v01.mp4": b"two"},
            selected="s01_sh010_t01_v01.mp4",
        )
        studio.sync(self.project)
        swapped = f"s01_sh010_t02_v01__{sha(b'two')[:12]}.mp4"
        shutil.copy2(
            directory / "s01_sh010_t02_v01.mp4", self.root / "assets" / swapped
        )
        composition = self.root / "compositions/s01_sh010.html"
        text = composition.read_text()
        old = f"s01_sh010_t01_v01__{sha(b'one')[:12]}.mp4"
        composition.write_text(text.replace(old, swapped))
        report = studio.sync(self.project)
        self.assertEqual(report.preserved, ["s01_sh010"])
        self.assertIn(swapped, composition.read_text())
        result = studio.status(self.project)
        self.assertFalse(result["ok"])
        self.assertIn(
            "placed_differs_from_selection",
            [issue["code"] for issue in result["issues"]],
        )

    def test_new_shot_appends_without_touching_existing_edits(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        index_path = self.root / "index.html"
        edited = index_path.read_text().replace(
            '<div id="s01_sh010"', '<div data-hf-id="hf-keep" id="s01_sh010"'
        )
        index_path.write_text(edited)
        self.add_shot(
            "s01_sh020",
            takes={"s01_sh020_t01_v01.mp4": b"two"},
            selected="s01_sh020_t01_v01.mp4",
            duration=2.5,
        )
        report = studio.sync(self.project)
        self.assertEqual(report.added, ["s01_sh020"])
        index = index_path.read_text()
        self.assertIn('data-hf-id="hf-keep"', index)
        self.assertIn(
            'id="s01_sh020" data-composition-id="s01_sh020" data-composition-src="compositions/s01_sh020.html" data-start="4"',
            index,
        )
        self.assertIn(
            'data-composition-id="main" data-start="0" data-duration="6.5"', index
        )
        self.assertIn(
            "## Frame 2 — s01_sh020", (self.root / "STORYBOARD.md").read_text()
        )

    def test_changed_take_is_reported_stale(self):
        directory = self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        (directory / "s01_sh010_t01_v01.mp4").write_bytes(b"re-rendered")
        result = studio.status(self.project)
        self.assertIn("take_changed", [issue["code"] for issue in result["issues"]])
        self.assertFalse(result["ok"])

    def test_missing_and_modified_assets_are_reported(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        asset = next((self.root / "assets").iterdir())
        asset.write_bytes(b"tampered")
        self.assertIn(
            "asset_modified", [i["code"] for i in studio.status(self.project)["issues"]]
        )
        asset.unlink()
        self.assertIn(
            "asset_missing", [i["code"] for i in studio.status(self.project)["issues"]]
        )

    def test_shot_without_selection_is_skipped_unless_requested(self):
        self.add_shot()
        report = studio.sync(self.project)
        self.assertEqual(report.added, [])
        self.assertEqual(report.skipped[0]["shot_id"], "s01_sh010")
        report = studio.sync(self.project, {"s01_sh010": "s01_sh010_t01_v01.mp4"})
        self.assertEqual(report.added, ["s01_sh010"])
        issues = studio.status(self.project)["issues"]
        self.assertEqual([i["code"] for i in issues], ["selection_pending"])
        self.assertTrue(studio.status(self.project)["ok"])

    def test_shot_without_a_take_becomes_an_outline_frame_with_its_narrative(self):
        directory = self.add_shot()
        manifest = directory / "shot.md"
        manifest.write_text(
            manifest.read_text()
            + "\n## Action\n\nA bus arrives at dusk.\nPeople step off.\n\nSecond paragraph.\n"
        )
        report = studio.sync(self.project)
        self.assertEqual(report.outlined, ["s01_sh010"])
        storyboard = (self.root / "STORYBOARD.md").read_text()
        self.assertIn("## Frame 1 — s01_sh010\n- status: outline", storyboard)
        self.assertNotIn("- src:", storyboard)
        self.assertIn("A bus arrives at dusk. People step off.", storyboard)
        self.assertNotIn("Second paragraph", storyboard)
        self.assertFalse((self.root / "compositions/s01_sh010.html").exists())
        self.assertNotIn("s01_sh010", (self.root / "index.html").read_text())

    def test_resync_does_not_duplicate_an_outline_frame(self):
        self.add_shot()
        studio.sync(self.project)
        report = studio.sync(self.project)
        self.assertEqual(report.outlined, [])
        self.assertEqual((self.root / "STORYBOARD.md").read_text().count("## Frame"), 1)

    def test_outline_frame_is_upgraded_in_place_when_a_take_arrives(self):
        directory = self.add_shot()
        manifest = directory / "shot.md"
        manifest.write_text(
            manifest.read_text() + "\n## Action\n\nA bus arrives at dusk.\n"
        )
        self.add_shot(
            "s01_sh020",
            takes={"s01_sh020_t01_v01.mp4": b"two"},
            selected="s01_sh020_t01_v01.mp4",
        )
        studio.sync(self.project)
        before = (self.root / "STORYBOARD.md").read_text()
        self.assertIn("## Frame 1 — s01_sh010\n- status: outline", before)
        self.assertIn("## Frame 2 — s01_sh020\n- status: built", before)
        report = studio.sync(self.project, {"s01_sh010": "s01_sh010_t01_v01.mp4"})
        self.assertEqual(report.added, ["s01_sh010"])
        after = (self.root / "STORYBOARD.md").read_text()
        self.assertIn(
            "## Frame 1 — s01_sh010\n- status: built\n- src: compositions/s01_sh010.html",
            after,
        )
        self.assertIn("A bus arrives at dusk.", after)
        self.assertEqual(after.count("## Frame"), 2)
        self.assertIn("- take: s01_sh010_t01_v01.mp4", after)

    def test_active_take_is_used_when_nothing_is_selected(self):
        self.add_shot(
            takes={"s01_sh010_t01_v01.mp4": b"a", "s01_sh010_t02_v01.mp4": b"b"},
            active="t02_v01",
        )
        report = studio.sync(self.project)
        self.assertEqual(report.added, ["s01_sh010"])
        self.assertTrue(
            any("t02_v01" in p.name for p in (self.root / "assets").iterdir())
        )

    def test_duplicate_shot_ids_are_rejected(self):
        self.add_shot("s01_sh010")
        self.add_shot("s01_sh020", extra="shot: ignored\n")
        manifest = self.project / "scenes/scene-01/s01_sh020/shot.md"
        manifest.write_text(
            manifest.read_text().replace("shot_id: s01_sh020", "shot_id: s01_sh010")
        )
        with self.assertRaisesRegex(studio.StudioError, "Duplicate shot id"):
            studio.discover_shots(self.project)

    def test_unsafe_take_filenames_are_rejected(self):
        self.add_shot(selected="../../escape.mp4")
        with self.assertRaises(studio.StudioError):
            studio.sync(self.project)
        self.assertFalse(
            (self.root / "assets").exists() and any((self.root / "assets").iterdir())
        )

    def test_symlinked_studio_directory_is_rejected(self):
        outside = Path(self.temp.name).resolve() / "outside"
        outside.mkdir()
        (self.project / "studio").symlink_to(outside)
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        with self.assertRaisesRegex(studio.StudioError, "real directory"):
            studio.sync(self.project)

    def test_missing_frames_marker_fails_clearly(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.init_studio(self.project)
        index = self.root / "index.html"
        index.write_text(index.read_text().replace(studio.FRAMES_MARKER, ""))
        with self.assertRaisesRegex(studio.StudioError, "marker"):
            studio.sync(self.project)

    def test_orphan_composition_is_reported(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        (self.root / "compositions/ghost.html").write_text("<html></html>")
        codes = [i["code"] for i in studio.status(self.project)["issues"]]
        self.assertIn("orphan_frame", codes)

    def test_dimensions(self):
        self.assertEqual(studio.dimensions("16:9", "720p"), (1280, 720))
        self.assertEqual(studio.dimensions("9:16", "1080p"), (1080, 1920))
        self.assertEqual(studio.dimensions("1:1", "720p"), (720, 720))
        with self.assertRaises(studio.StudioError):
            studio.dimensions("wide", "720p")

    def test_missing_duration_is_an_error(self):
        directory = self.add_shot(selected="s01_sh010_t01_v01.mp4")
        manifest = directory / "shot.md"
        text = "".join(
            line
            for line in manifest.read_text().splitlines(keepends=True)
            if "duration_s" not in line
        )
        manifest.write_text(text)
        with self.assertRaisesRegex(studio.StudioError, "no duration"):
            studio.sync(self.project)

    def test_measured_duration_overrides_the_manifest_and_warns(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4", duration=10)
        report = studio.sync(self.project, probe=lambda path: 6.0)
        self.assertIn(
            'data-duration="6"', (self.root / "compositions/s01_sh010.html").read_text()
        )
        self.assertIn(
            'data-composition-id="main" data-start="0" data-duration="6"',
            (self.root / "index.html").read_text(),
        )
        self.assertEqual(len(report.warnings), 1)
        self.assertIn("measured length", report.warnings[0])

    def test_matching_measured_duration_does_not_warn(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4", duration=4)
        report = studio.sync(self.project, probe=lambda path: 4.04)
        self.assertEqual(report.warnings, [])

    def test_probe_failure_falls_back_to_the_manifest(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4", duration=4)
        studio.sync(self.project, probe=lambda path: None)
        self.assertIn(
            'data-duration="4"', (self.root / "compositions/s01_sh010.html").read_text()
        )

    def test_probe_duration_parses_ffprobe_output_and_tolerates_failure(self):
        good = fake_runner(stdout=json.dumps({"format": {"duration": "6.0"}}))
        self.assertEqual(studio.probe_duration(Path("x.mp4"), good), 6.0)
        self.assertIsNone(
            studio.probe_duration(Path("x.mp4"), fake_runner(returncode=1, stdout=""))
        )
        self.assertIsNone(
            studio.probe_duration(Path("x.mp4"), fake_runner(stdout="not json"))
        )

    def make_render(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        render = self.root / "renders" / "delivery.mp4"
        render.write_bytes(b"rendered-bytes")
        return render

    def test_record_render_writes_valid_sidecar(self):
        render = self.make_render()
        sidecar = studio.record_render(
            self.project, render, ["--quality", "delivery"], fake_runner()
        )
        record = json.loads(sidecar.read_text())
        self.assertEqual(sidecar.name, "delivery.mp4.render.json")
        self.assertEqual(record["output"]["sha256"], sha(b"rendered-bytes"))
        self.assertEqual(record["hyperframes"]["arguments"], ["--quality", "delivery"])
        self.assertEqual(record["frames"][0]["shot_id"], "s01_sh010")
        self.assertEqual(
            schema_findings(record, "studio-render-record.schema.json"), []
        )

    def test_record_render_rejects_files_outside_renders(self):
        self.make_render()
        outside = self.project / "other.mp4"
        outside.write_bytes(b"x")
        with self.assertRaisesRegex(studio.StudioError, "inside studio/renders"):
            studio.record_render(self.project, outside, [], fake_runner())

    def test_record_render_fails_when_probe_fails(self):
        render = self.make_render()
        with self.assertRaisesRegex(studio.StudioError, "ffprobe failed"):
            studio.record_render(
                self.project, render, [], fake_runner(returncode=1, stderr="bad file")
            )
        self.assertFalse(render.with_name("delivery.mp4.render.json").exists())

    def render_runner(self, returncode=0):
        calls = []

        def runner(argv, **kwargs):
            calls.append(argv)
            if argv[0] == "ffprobe":
                return subprocess.CompletedProcess(argv, 0, json.dumps(PROBE), "")
            if returncode == 0:
                Path(argv[argv.index("--output") + 1]).write_bytes(b"rendered")
            return subprocess.CompletedProcess(argv, returncode, "", "browser crashed")

        runner.calls = calls
        return runner

    def test_render_runs_pinned_cli_and_records_the_output(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        runner = self.render_runner()
        sidecar = studio.render(self.project, "final", "delivery", runner)
        argv = next(call for call in runner.calls if call[0] == "npx")
        self.assertEqual(
            argv[:4],
            ["npx", "--yes", f"hyperframes@{studio.HYPERFRAMES_VERSION}", "render"],
        )
        self.assertIn("delivery", argv)
        self.assertEqual(sidecar.name, "final.mp4.render.json")
        self.assertEqual(
            json.loads(sidecar.read_text())["hyperframes"]["arguments"],
            ["render", "--quality", "delivery"],
        )

    def test_render_refuses_to_overwrite_an_earlier_render(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        studio.render(self.project, "final", "draft", self.render_runner())
        with self.assertRaisesRegex(studio.StudioError, "already exists"):
            studio.render(self.project, "final", "draft", self.render_runner())

    def test_delivery_render_is_blocked_by_stale_takes_but_draft_is_not(self):
        directory = self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        (directory / "s01_sh010_t01_v01.mp4").write_bytes(b"re-rendered")
        with self.assertRaisesRegex(studio.StudioError, "clean status"):
            studio.render(self.project, "final", "delivery", self.render_runner())
        self.assertFalse((self.root / "renders/final.mp4").exists())
        studio.render(self.project, "preview", "draft", self.render_runner())
        self.assertTrue((self.root / "renders/preview.mp4").is_file())

    def test_render_failure_is_reported_and_not_recorded(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        with self.assertRaisesRegex(studio.StudioError, "browser crashed"):
            studio.render(
                self.project, "final", "draft", self.render_runner(returncode=1)
            )
        self.assertEqual(list((self.root / "renders").glob("*.json")), [])

    def test_render_rejects_bad_names_and_qualities(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        with self.assertRaises(studio.StudioError):
            studio.render(self.project, "../escape", "draft", self.render_runner())
        with self.assertRaises(studio.StudioError):
            studio.render(self.project, "final", "ultra", self.render_runner())

    def test_hyperframes_command_is_pinned_and_privacy_safe(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        runner = fake_runner(stdout=CHECK_OK)
        studio.run_hyperframes(self.project, ["check", "--json"], runner)
        argv, kwargs = runner.calls[0]
        self.assertEqual(
            argv[:3], ["npx", "--yes", f"hyperframes@{studio.HYPERFRAMES_VERSION}"]
        )
        self.assertEqual(argv[3:5], ["check", str(self.root)])
        for key in (
            "HYPERFRAMES_SKIP_SKILLS",
            "HYPERFRAMES_NO_TELEMETRY",
            "HYPERFRAMES_NO_UPDATE_CHECK",
            "DO_NOT_TRACK",
        ):
            self.assertEqual(kwargs["env"][key], "1")

    def test_run_hyperframes_requires_a_studio_project(self):
        with self.assertRaisesRegex(studio.StudioError, "No Studio project"):
            studio.run_hyperframes(self.project, ["check"], fake_runner())

    def review_and_decision(
        self,
        filename="s01_sh010_t01_v01.mp4",
        actor="agent",
        method="temporal playback of the full clip",
        mode="approve_for_me",
        authorization=None,
    ):
        relative = f"scenes/scene-01/s01_sh010/{filename}"
        digest = sha((self.project / relative).read_bytes())
        review = {
            "schema_version": 1,
            "artifact_path": relative,
            "artifact_sha256": digest,
            "status": "pass",
            "inspection_method": method,
            "coverage": "Whole clip watched.",
            "checks": [
                {
                    "criterion": "Matches the brief",
                    "status": "pass",
                    "evidence": "Fixture evidence",
                }
            ],
            "observations": ["Content visible."],
            "limitations": [],
            "recommendation": "Approve.",
        }
        review_bytes = json.dumps(review).encode()
        (self.project / "review.json").write_bytes(review_bytes)
        project_bytes = (self.project / "project.md").read_bytes()
        decision = {
            "schema_version": 1,
            "decision_id": "studio-decision-1",
            "decision_type": "variant_selection",
            "asset_id": "s01_sh010",
            "subject_path": relative,
            "selected_variant": filename,
            "selected_sha256": digest,
            "actor": actor,
            "approval_mode": mode,
            "project_sha256": sha(project_bytes),
            "result": "approved",
            "review_path": "review.json",
            "review_sha256": sha(review_bytes),
            "upstream_sha256": {},
            "reason": "The placed take passes the recorded checks.",
            "decided_at": datetime.datetime.now(datetime.UTC).isoformat(),
        }
        if authorization is not None:
            decision["authorization"] = authorization
        return decision

    def test_agent_selection_updates_manifest_and_writes_decision(self):
        self.add_shot(takes={"s01_sh010_t01_v01.mp4": b"one"})
        studio.sync(self.project, {"s01_sh010": "s01_sh010_t01_v01.mp4"})
        result = studio.record_selection(
            self.project, "s01_sh010", self.review_and_decision()
        )
        self.assertTrue(result["ok"])
        manifest = (self.project / "scenes/scene-01/s01_sh010/shot.md").read_text()
        self.assertIn("selected_variant: s01_sh010_t01_v01.mp4", manifest)
        self.assertTrue((self.project / "decisions/studio-decision-1.json").is_file())
        self.assertTrue(studio.status(self.project)["ok"])

    def test_selection_must_match_what_is_placed(self):
        directory = self.add_shot(
            takes={"s01_sh010_t01_v01.mp4": b"one", "s01_sh010_t02_v01.mp4": b"two"}
        )
        studio.sync(self.project, {"s01_sh010": "s01_sh010_t01_v01.mp4"})
        decision = self.review_and_decision("s01_sh010_t02_v01.mp4")
        with self.assertRaisesRegex(studio.StudioError, "placed"):
            studio.record_selection(self.project, "s01_sh010", decision)
        self.assertNotIn("selected_variant", (directory / "shot.md").read_text())

    def chat_authorization(self, words="go with take one for the opening"):
        return {"source": "chat", "evidence": words}

    def synced_single_take(self, mode="approve_for_me"):
        self.write_project(mode)
        self.add_shot(takes={"s01_sh010_t01_v01.mp4": b"one"})
        studio.sync(self.project, {"s01_sh010": "s01_sh010_t01_v01.mp4"})

    def test_user_choice_quoted_from_chat_is_recorded_under_ask_for_approval(self):
        self.synced_single_take("ask_for_approval")
        decision = self.review_and_decision(
            actor="user",
            mode="ask_for_approval",
            authorization=self.chat_authorization(),
        )
        result = studio.record_selection(self.project, "s01_sh010", decision)
        self.assertTrue(result["ok"])
        manifest = (self.project / "scenes/scene-01/s01_sh010/shot.md").read_text()
        self.assertIn("selected_variant: s01_sh010_t01_v01.mp4", manifest)
        self.assertIn("actor: user", manifest)
        saved = json.loads(
            (self.project / "decisions/studio-decision-1.json").read_text()
        )
        self.assertEqual(saved["authorization"], self.chat_authorization())
        self.assertIn("- approval: approved", (self.root / "STORYBOARD.md").read_text())

    def test_user_choice_is_also_accepted_under_approve_for_me(self):
        self.synced_single_take()
        decision = self.review_and_decision(
            actor="user", authorization=self.chat_authorization()
        )
        self.assertTrue(
            studio.record_selection(self.project, "s01_sh010", decision)["ok"]
        )

    def test_user_decision_without_the_users_words_is_refused(self):
        self.synced_single_take("ask_for_approval")
        bad_authorizations = [
            None,
            {"source": "local_ui", "evidence": "a1b2c3"},
            {"source": "chat", "evidence": "   "},
            {"source": "chat", "evidence": "ok"},
            {"source": "chat"},
            "chat",
        ]
        for authorization in bad_authorizations:
            decision = self.review_and_decision(
                actor="user", mode="ask_for_approval", authorization=authorization
            )
            with self.assertRaisesRegex(studio.StudioError, "authorization"):
                studio.record_selection(self.project, "s01_sh010", decision)
        self.assertFalse((self.project / "decisions").exists())
        self.assertNotIn(
            "selected_variant",
            (self.project / "scenes/scene-01/s01_sh010/shot.md").read_text(),
        )

    def test_unknown_actor_is_refused(self):
        self.synced_single_take()
        decision = self.review_and_decision(actor="agent")
        decision["actor"] = "system"
        with self.assertRaisesRegex(studio.StudioError, "actor"):
            studio.record_selection(self.project, "s01_sh010", decision)

    def test_an_agent_cannot_replace_a_choice_the_user_made(self):
        directory = self.add_shot(
            takes={"s01_sh010_t01_v01.mp4": b"one", "s01_sh010_t02_v01.mp4": b"two"}
        )
        studio.sync(
            self.project, {"s01_sh010": "s01_sh010_t01_v01.mp4"}, probe=lambda path: 4.0
        )
        user = self.review_and_decision(
            actor="user", authorization=self.chat_authorization()
        )
        studio.record_selection(self.project, "s01_sh010", user)
        studio.place_take(
            self.project, "s01_sh010", "s01_sh010_t02_v01.mp4", lambda path: 4.0
        )
        agent = self.review_and_decision("s01_sh010_t02_v01.mp4")
        agent["decision_id"] = "studio-decision-2"
        with self.assertRaisesRegex(ValueError, "agent cannot replace"):
            studio.record_selection(self.project, "s01_sh010", agent)
        self.assertIn(
            "selected_variant: s01_sh010_t01_v01.mp4",
            (directory / "shot.md").read_text(),
        )

    def test_chat_authorization_is_not_accepted_outside_studio_projects(self):
        self.synced_single_take("ask_for_approval")
        decision = self.review_and_decision(
            actor="user",
            mode="ask_for_approval",
            authorization=self.chat_authorization(),
        )
        service = studio.selection_service()
        shot = studio.find_shot(self.project, "s01_sh010")
        registry = studio.selection_registry(self.project, shot)
        with self.assertRaisesRegex(ValueError, "only accepted for Studio"):
            service.apply_selection_batch(
                self.project,
                {
                    "registry": registry,
                    "selections": {"s01_sh010": "s01_sh010_t01_v01.mp4"},
                },
                service.revision(self.project, registry),
                decisions={"s01_sh010": decision},
            )

    def test_agent_decision_is_refused_in_ask_for_approval(self):
        self.write_project("ask_for_approval")
        self.add_shot(takes={"s01_sh010_t01_v01.mp4": b"one"})
        studio.sync(self.project, {"s01_sh010": "s01_sh010_t01_v01.mp4"})
        decision = self.review_and_decision()
        with self.assertRaisesRegex(studio.StudioError, "approve_for_me"):
            studio.record_selection(self.project, "s01_sh010", decision)

    def test_selection_for_unknown_or_unplaced_shot_fails(self):
        self.add_shot(takes={"s01_sh010_t01_v01.mp4": b"one"})
        decision = self.review_and_decision()
        with self.assertRaisesRegex(studio.StudioError, "Unknown shot"):
            studio.record_selection(self.project, "s09_sh999", decision)
        with self.assertRaisesRegex(studio.StudioError, "no placed take"):
            studio.record_selection(self.project, "s01_sh010", decision)

    @unittest.skipUnless(
        os.environ.get("STUDIO_SMOKE") == "1",
        "set STUDIO_SMOKE=1 to run the HyperFrames CLI smoke test",
    )
    def test_generated_project_passes_hyperframes_lint(self):
        self.add_shot(
            takes={"s01_sh010_t01_v01.mp4": b"x"}, selected="s01_sh010_t01_v01.mp4"
        )
        studio.sync(self.project)
        completed = studio.run_hyperframes(self.project, ["lint", "--json"])
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def project_mode(self):
        text = (self.project / "project.md").read_text()
        return "ask_for_approval" if "ask_for_approval" in text else "approve_for_me"

    def lock_decision(
        self,
        kind,
        subject,
        decision_id=None,
        actor=None,
        authorization=None,
        stage_id=None,
    ):
        mode = self.project_mode()
        actor = actor or ("user" if mode == "ask_for_approval" else "agent")
        if actor == "user" and authorization is None:
            authorization = self.chat_authorization("lock it, that looks right")
        method = (
            "listening to the full audio"
            if kind == "audio"
            else "temporal playback and listening of the full clip"
        )
        digest = sha((self.project / subject).read_bytes())
        review = {
            "schema_version": 1,
            "artifact_path": subject,
            "artifact_sha256": digest,
            "status": "pass",
            "inspection_method": method,
            "coverage": "Whole artifact.",
            "checks": [
                {
                    "criterion": "Matches the brief",
                    "status": "pass",
                    "evidence": "Fixture evidence",
                }
            ],
            "observations": ["Content visible."],
            "limitations": [],
            "recommendation": "Approve.",
        }
        review_name = f"review-{decision_id or kind}.json"
        review_bytes = json.dumps(review).encode()
        (self.project / review_name).write_bytes(review_bytes)
        decision = {
            "schema_version": 1,
            "decision_id": decision_id or f"lock-{kind}",
            "decision_type": "stage_lock",
            "stage_id": stage_id or studio.STAGE_LOCKS[kind],
            "lock_kind": kind,
            "subject_path": subject,
            "subject_sha256": digest,
            "actor": actor,
            "approval_mode": mode,
            "project_sha256": sha((self.project / "project.md").read_bytes()),
            "result": "approved",
            "review_path": review_name,
            "review_sha256": sha(review_bytes),
            "upstream_sha256": {},
            "reason": "The artifact passes the recorded checks.",
            "decided_at": datetime.datetime.now(datetime.UTC).isoformat(),
        }
        if authorization is not None:
            decision["authorization"] = authorization
        return decision

    def record_lock(self, kind, subject, **options):
        decision = self.lock_decision(kind, subject, **options)
        service = studio.selection_service()
        with mock.patch.object(
            service, "probe_media_streams", return_value={"video", "audio"}
        ):
            return studio.record_lock(self.project, decision)

    def lock_final(self, name="final", **options):
        return self.record_lock("final_master", f"studio/renders/{name}.mp4", **options)

    def lock_assembly(self):
        studio.render(self.project, "cut", "draft", self.render_runner())
        self.record_lock("picture", "studio/renders/cut.mp4")

    def complete_through(self, stage_id, runner=None, skip_audio=True):
        runner = runner or fake_runner(stdout=CHECK_OK)
        for stage in studio.STAGES:
            if stage == "audio-preparation" and skip_audio:
                studio.skip_stage(self.project, stage, "native audio only")
            else:
                studio.start_stage(self.project, stage)
                if stage == "assembly-review":
                    self.lock_assembly()
                studio.complete_stage(self.project, stage, runner)
            if stage == stage_id:
                return

    def test_stages_start_pending_and_must_complete_in_order(self):
        value = studio.read_stages(self.project)
        self.assertEqual([item["status"] for item in value["stages"]], ["pending"] * 8)
        with self.assertRaisesRegex(
            studio.StudioError, "Complete brief-development before"
        ):
            studio.start_stage(self.project, "scene-breakdown")
        with self.assertRaisesRegex(studio.StudioError, "Unknown stage"):
            studio.start_stage(self.project, "polish")

    def test_brief_stage_needs_a_valid_project_record(self):
        (self.project / "project.md").unlink()
        studio.start_stage(self.project, "brief-development")
        with self.assertRaisesRegex(studio.StudioError, "cannot exit"):
            studio.complete_stage(self.project, "brief-development")
        self.write_project("approve_for_me")
        value = studio.complete_stage(self.project, "brief-development")
        self.assertEqual(value["current_stage"], "scene-breakdown")
        self.assertEqual(schema_findings(value, "studio-stages.schema.json"), [])

    def test_planning_stages_need_the_studio_project_but_not_takes(self):
        self.add_shot()
        self.complete_through("brief-development")
        studio.start_stage(self.project, "scene-breakdown")
        with self.assertRaisesRegex(studio.StudioError, "No Studio project"):
            studio.complete_stage(self.project, "scene-breakdown")
        studio.sync(self.project)
        studio.complete_stage(self.project, "scene-breakdown")

    def test_shot_generation_needs_a_placed_take_per_shot_and_a_clean_check(self):
        self.add_shot()
        studio.sync(self.project)
        self.complete_through("audio-preparation")
        studio.start_stage(self.project, "shot-generation")
        with self.assertRaisesRegex(studio.StudioError, "s01_sh010: no placed take"):
            studio.complete_stage(
                self.project, "shot-generation", fake_runner(stdout=CHECK_OK)
            )
        studio.sync(self.project, {"s01_sh010": "s01_sh010_t01_v01.mp4"})
        with self.assertRaisesRegex(studio.StudioError, "hyperframes check failed"):
            studio.complete_stage(
                self.project,
                "shot-generation",
                fake_runner(returncode=1, stdout=CHECK_OK),
            )
        value = studio.complete_stage(
            self.project, "shot-generation", fake_runner(stdout=CHECK_OK)
        )
        entry = next(
            item for item in value["stages"] if item["id"] == "shot-generation"
        )
        self.assertTrue(
            entry["evidence"]["check_ran"] and entry["evidence"]["check_ok"]
        )
        self.assertRegex(entry["evidence"]["provenance_sha256"], "^[0-9a-f]{64}$")

    def test_stage_cannot_exit_with_a_stale_take(self):
        directory = self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        self.complete_through("storyboard-visual-plan")
        (directory / "s01_sh010_t01_v01.mp4").write_bytes(b"re-rendered")
        studio.start_stage(self.project, "audio-preparation")
        with self.assertRaisesRegex(studio.StudioError, "take_changed"):
            studio.complete_stage(self.project, "audio-preparation")

    def test_delivery_needs_a_render_that_matches_the_placed_takes(self):
        directory = self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        self.complete_through("assembly-review")
        studio.start_stage(self.project, "delivery")
        with self.assertRaisesRegex(
            studio.StudioError, "no render made by studio_project.py render"
        ):
            studio.complete_stage(
                self.project, "delivery", fake_runner(stdout=CHECK_OK)
            )
        studio.render(self.project, "final", "delivery", self.render_runner())
        self.lock_final()
        value = studio.complete_stage(
            self.project, "delivery", fake_runner(stdout=CHECK_OK)
        )
        entry = next(item for item in value["stages"] if item["id"] == "delivery")
        self.assertEqual(
            entry["evidence"]["render_record"], "studio/renders/final.mp4.render.json"
        )
        self.assertEqual(value["current_stage"], "delivery")
        self.assertTrue((directory / "s01_sh010_t01_v01.mp4").exists())

    def test_delivery_rejects_a_render_made_before_a_swap(self):
        directory = self.add_shot(
            takes={"s01_sh010_t01_v01.mp4": b"one", "s01_sh010_t02_v01.mp4": b"two"},
            selected="s01_sh010_t01_v01.mp4",
        )
        studio.sync(self.project)
        self.complete_through("assembly-review")
        studio.render(self.project, "final", "delivery", self.render_runner())
        new_asset = f"s01_sh010_t02_v01__{sha(b'two')[:12]}.mp4"
        shutil.copy2(
            directory / "s01_sh010_t02_v01.mp4", self.root / "assets" / new_asset
        )
        composition = self.root / "compositions/s01_sh010.html"
        composition.write_text(
            composition.read_text().replace(
                f"s01_sh010_t01_v01__{sha(b'one')[:12]}.mp4", new_asset
            )
        )
        manifest = directory / "shot.md"
        manifest.write_text(
            manifest.read_text().replace(
                "selected_variant: s01_sh010_t01_v01.mp4",
                "selected_variant: s01_sh010_t02_v01.mp4",
            )
        )
        studio.start_stage(self.project, "delivery")
        with self.assertRaisesRegex(
            studio.StudioError, "does not match the placed takes"
        ):
            studio.complete_stage(
                self.project, "delivery", fake_runner(stdout=CHECK_OK)
            )

    def test_reopening_a_stage_returns_it_and_later_stages_to_review(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        self.complete_through("shot-generation")
        value = studio.reopen_stage(self.project, "canon-elements")
        statuses = {item["id"]: item["status"] for item in value["stages"]}
        self.assertEqual(statuses["brief-development"], "complete")
        self.assertEqual(statuses["scene-breakdown"], "complete")
        self.assertEqual(statuses["canon-elements"], "review")
        self.assertEqual(statuses["shot-generation"], "review")
        self.assertEqual(value["current_stage"], "canon-elements")
        reopened = next(
            item for item in value["stages"] if item["id"] == "shot-generation"
        )
        self.assertNotIn("evidence", reopened)
        with self.assertRaisesRegex(
            studio.StudioError, "Complete canon-elements before"
        ):
            studio.start_stage(self.project, "shot-generation")

    def test_hand_edited_stages_file_is_rejected(self):
        studio.start_stage(self.project, "brief-development")
        path = self.root / "stages.json"
        value = json.loads(path.read_text())
        value["stages"][0]["status"] = "done"
        path.write_text(json.dumps(value))
        with self.assertRaisesRegex(studio.StudioError, "stages.json is invalid"):
            studio.read_stages(self.project)

    def test_stage_commands_through_the_cli(self):
        code, payload = self.run_cli("stage", str(self.project), "show")
        self.assertEqual((code, payload["current_stage"]), (0, "brief-development"))
        code, payload = self.run_cli(
            "stage", str(self.project), "start", "brief-development"
        )
        self.assertEqual(code, 0)
        code, payload = self.run_cli(
            "stage", str(self.project), "complete", "brief-development"
        )
        self.assertEqual((code, payload["current_stage"]), (0, "scene-breakdown"))
        code, payload = self.run_cli("stage", str(self.project), "complete")
        self.assertEqual(code, 1)
        self.assertIn("stage id", payload["error"])

    def host_count(self, shot_id):
        return (self.root / "index.html").read_text().count(f'<div id="{shot_id}"')

    def test_canvas_projects_are_refused(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        (self.project / "showcase.json").write_text("{}")
        with self.assertRaisesRegex(studio.StudioError, "showcase.json"):
            studio.sync(self.project)
        with self.assertRaisesRegex(studio.StudioError, "showcase.json"):
            studio.status(self.project)

    def test_reserved_and_digit_leading_shot_ids_are_rejected(self):
        self.add_shot("main", takes={})
        with self.assertRaisesRegex(studio.StudioError, "reserved"):
            studio.discover_shots(self.project)
        shutil.rmtree(self.project / "scenes")
        self.add_shot("s01_sh010", takes={})
        manifest = self.project / "scenes/scene-01/s01_sh010/shot.md"
        manifest.write_text(
            manifest.read_text().replace("shot_id: s01_sh010", "shot_id: 01_shot")
        )
        with self.assertRaisesRegex(studio.StudioError, "invalid"):
            studio.discover_shots(self.project)

    def test_sync_writes_nothing_when_a_later_shot_fails(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        self.add_shot(
            "s01_sh020",
            takes={"s01_sh020_t01_v01.mp4": b"x"},
            selected="s01_sh020_t99_v01.mp4",
        )
        with self.assertRaises(ValueError):
            studio.sync(self.project)
        self.assertFalse((self.root / "compositions/s01_sh010.html").exists())
        self.assertNotIn("s01_sh010", (self.root / "index.html").read_text())

    def test_composition_missing_from_the_timeline_is_reported_and_not_duplicated(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        index = self.root / "index.html"
        text = index.read_text()
        start = text.index('<div id="s01_sh010"')
        end = text.index("</div>", start) + len("</div>")
        index.write_text(text[:start] + text[end:])
        codes = [i["code"] for i in studio.status(self.project)["issues"]]
        self.assertIn("not_on_timeline", codes)
        self.assertFalse(studio.status(self.project)["ok"])
        report = studio.sync(self.project)
        self.assertEqual(report.added, [])
        self.assertTrue(
            any("not_on_timeline" in warning for warning in report.warnings)
        )
        self.assertEqual(self.host_count("s01_sh010"), 0)

    def test_host_without_composition_is_reported_and_not_duplicated(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        (self.root / "compositions/s01_sh010.html").unlink()
        self.assertIn(
            "frame_missing", [i["code"] for i in studio.status(self.project)["issues"]]
        )
        report = studio.sync(self.project)
        self.assertEqual(report.added, [])
        self.assertEqual(self.host_count("s01_sh010"), 1)

    def test_root_duration_never_shrinks_when_a_shot_is_added(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        index = self.root / "index.html"
        index.write_text(
            index.read_text().replace(
                'data-duration="4" data-fps', 'data-duration="30" data-fps', 1
            )
        )
        self.add_shot(
            "s01_sh020",
            takes={"s01_sh020_t01_v01.mp4": b"two"},
            selected="s01_sh020_t01_v01.mp4",
        )
        studio.sync(self.project)
        self.assertIn(
            'data-composition-id="main" data-start="0" data-duration="30"',
            index.read_text(),
        )

    def test_single_quoted_hosts_are_read_and_relative_timing_is_a_clear_error(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        index = self.root / "index.html"
        quoted = index.read_text().replace(
            'data-start="0" data-duration="4"', "data-start='0' data-duration='4'"
        )
        self.assertEqual(studio.timeline_end(quoted), 4.0)
        index.write_text(
            index.read_text().replace(
                'data-start="0" data-duration="4"',
                'data-start="intro + 1" data-duration="4"',
            )
        )
        self.add_shot(
            "s01_sh020",
            takes={"s01_sh020_t01_v01.mp4": b"two"},
            selected="s01_sh020_t01_v01.mp4",
        )
        with self.assertRaisesRegex(studio.StudioError, "relative or invalid timing"):
            studio.sync(self.project)

    def test_unmanaged_asset_is_reported_and_sync_still_completes(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        composition = self.root / "compositions/s01_sh010.html"
        asset = next((self.root / "assets").iterdir()).name
        (self.root / "assets/custom.mp4").write_bytes(b"x")
        composition.write_text(composition.read_text().replace(asset, "custom.mp4"))
        self.assertIn(
            "unmanaged_asset",
            [i["code"] for i in studio.status(self.project)["issues"]],
        )
        studio.sync(self.project)
        self.assertEqual(
            json.loads((self.root / "provenance.json").read_text())["frames"], []
        )

    def test_take_option_for_unknown_or_existing_shot(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        with self.assertRaisesRegex(studio.StudioError, "unknown shots"):
            studio.sync(self.project, {"s09_sh999": "x.mp4"})
        studio.sync(self.project)
        report = studio.sync(self.project, {"s01_sh010": "s01_sh010_t01_v01.mp4"})
        self.assertTrue(any("--take ignored" in warning for warning in report.warnings))

    def test_mixed_aspect_ratios_warn(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        directory = self.add_shot(
            "s01_sh020",
            takes={"s01_sh020_t01_v01.mp4": b"two"},
            selected="s01_sh020_t01_v01.mp4",
        )
        manifest = directory / "shot.md"
        manifest.write_text(
            manifest.read_text().replace('aspect: "16:9"', 'aspect: "9:16"')
        )
        report = studio.sync(self.project)
        self.assertTrue(
            any(
                "differs from the project canvas" in warning
                for warning in report.warnings
            )
        )

    def test_sync_refreshes_the_approval_line_from_the_manifest(self):
        directory = self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        manifest = directory / "shot.md"
        manifest.write_text(
            manifest.read_text().replace("status: review", "status: approved", 1)
        )
        studio.sync(self.project)
        self.assertIn("- approval: approved", (self.root / "STORYBOARD.md").read_text())

    def test_pending_selection_blocks_assembly_review_and_delivery_level_renders(self):
        self.add_shot()
        studio.sync(self.project, {"s01_sh010": "s01_sh010_t01_v01.mp4"})
        self.complete_through("shot-generation")
        studio.start_stage(self.project, "assembly-review")
        with self.assertRaisesRegex(studio.StudioError, "selection_pending"):
            studio.complete_stage(
                self.project, "assembly-review", fake_runner(stdout=CHECK_OK)
            )
        with self.assertRaisesRegex(studio.StudioError, "clean status"):
            studio.render(self.project, "final", "delivery", self.render_runner())
        studio.render(self.project, "look", "draft", self.render_runner())

    def delivery_ready(self):
        directory = self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        self.complete_through("assembly-review")
        studio.start_stage(self.project, "delivery")
        return directory

    def test_draft_render_cannot_satisfy_delivery(self):
        self.delivery_ready()
        studio.render(self.project, "look", "draft", self.render_runner())
        with self.assertRaisesRegex(studio.StudioError, "standard or higher"):
            studio.complete_stage(
                self.project, "delivery", fake_runner(stdout=CHECK_OK)
            )

    def test_manually_recorded_render_cannot_satisfy_delivery(self):
        self.delivery_ready()
        render = self.root / "renders" / "external.mp4"
        render.write_bytes(b"made elsewhere")
        studio.record_render(
            self.project, render, ["render", "--quality", "delivery"], fake_runner()
        )
        with self.assertRaisesRegex(
            studio.StudioError, "no render made by studio_project.py render"
        ):
            studio.complete_stage(
                self.project, "delivery", fake_runner(stdout=CHECK_OK)
            )

    def test_render_file_replaced_after_recording_fails_delivery(self):
        self.delivery_ready()
        studio.render(self.project, "final", "delivery", self.render_runner())
        (self.root / "renders/final.mp4").write_bytes(b"swapped file")
        with self.assertRaisesRegex(
            studio.StudioError, "no longer matches its recorded file"
        ):
            studio.complete_stage(
                self.project, "delivery", fake_runner(stdout=CHECK_OK)
            )

    def test_timeline_edit_after_render_fails_delivery(self):
        self.delivery_ready()
        studio.render(self.project, "final", "delivery", self.render_runner())
        index = self.root / "index.html"
        index.write_text(
            index.read_text().replace(
                'data-start="0" data-duration="4"',
                'data-start="1" data-duration="4"',
                1,
            )
        )
        with self.assertRaisesRegex(studio.StudioError, "changed after"):
            studio.complete_stage(
                self.project, "delivery", fake_runner(stdout=CHECK_OK)
            )

    def test_optional_stages_can_be_skipped_with_a_reason_and_others_cannot(self):
        studio.start_stage(self.project, "brief-development")
        studio.complete_stage(self.project, "brief-development")
        with self.assertRaisesRegex(studio.StudioError, "can be skipped"):
            studio.skip_stage(self.project, "scene-breakdown", "not needed")
        self.add_shot()
        studio.sync(self.project)
        studio.complete_stage(self.project, "scene-breakdown")
        studio.complete_stage(self.project, "canon-elements")
        with self.assertRaisesRegex(studio.StudioError, "needs a reason"):
            studio.skip_stage(self.project, "storyboard-visual-plan", "  ")
        value = studio.skip_stage(
            self.project, "storyboard-visual-plan", "no storyboard requested"
        )
        entry = next(
            item for item in value["stages"] if item["id"] == "storyboard-visual-plan"
        )
        self.assertEqual(
            (entry["status"], entry["reason"]), ("skipped", "no storyboard requested")
        )
        self.assertEqual(value["current_stage"], "audio-preparation")
        studio.complete_stage(self.project, "audio-preparation")
        self.assertEqual(
            schema_findings(
                studio.read_stages(self.project), "studio-stages.schema.json"
            ),
            [],
        )

    def test_recompleting_an_earlier_stage_does_not_move_the_current_stage_back(self):
        self.add_shot()
        studio.sync(self.project)
        self.complete_through("canon-elements")
        studio.complete_stage(self.project, "scene-breakdown")
        self.assertEqual(
            studio.read_stages(self.project)["current_stage"], "storyboard-visual-plan"
        )

    def test_completed_stage_without_evidence_is_rejected(self):
        studio.start_stage(self.project, "brief-development")
        path = self.root / "stages.json"
        value = json.loads(path.read_text())
        value["stages"][0]["status"] = "complete"
        path.write_text(json.dumps(value))
        with self.assertRaisesRegex(studio.StudioError, "stages.json is invalid"):
            studio.read_stages(self.project)

    def test_check_must_report_ok_and_actually_run_the_browser(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        self.complete_through("audio-preparation")
        studio.start_stage(self.project, "shot-generation")
        for output in (
            json.dumps({"ok": True, "browserSkipped": True}),
            "not json",
            "{}",
        ):
            with self.assertRaisesRegex(studio.StudioError, "hyperframes check failed"):
                studio.complete_stage(
                    self.project, "shot-generation", fake_runner(stdout=output)
                )

    def test_a_hung_hyperframes_process_becomes_an_error(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)

        def hung(argv, **kwargs):
            raise subprocess.TimeoutExpired(argv, kwargs["timeout"])

        with self.assertRaisesRegex(studio.StudioError, "timed out"):
            studio.run_hyperframes(self.project, ["check"], hung)

    def test_environment_passed_to_hyperframes_is_an_allow_list(self):
        with mock.patch.dict(
            os.environ,
            {
                "BYTEPLUS_MODELARK_API_KEY": "secret",
                "PATH": "/bin",
                "npm_config_cache": "/tmp/c",
            },
        ):
            env = studio.hyperframes_environment()
        self.assertNotIn("BYTEPLUS_MODELARK_API_KEY", env)
        self.assertEqual((env["PATH"], env["npm_config_cache"]), ("/bin", "/tmp/c"))
        self.assertEqual(env["HYPERFRAMES_SKIP_SKILLS"], "1")

    def test_failed_render_removes_the_partial_file_so_the_name_can_be_reused(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)

        def crashing(argv, **kwargs):
            Path(argv[argv.index("--output") + 1]).write_bytes(b"partial")
            return subprocess.CompletedProcess(argv, 1, "", "crashed")

        with self.assertRaisesRegex(studio.StudioError, "crashed"):
            studio.render(self.project, "final", "draft", crashing)
        self.assertFalse((self.root / "renders/final.mp4").exists())
        studio.render(self.project, "final", "draft", self.render_runner())

    def test_symlinked_studio_subdirectory_is_rejected(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        outside = Path(self.temp.name).resolve() / "elsewhere"
        outside.mkdir()
        shutil.rmtree(self.root / "renders")
        (self.root / "renders").symlink_to(outside)
        with self.assertRaisesRegex(studio.StudioError, "inside the studio directory"):
            studio.render(self.project, "final", "draft", self.render_runner())

    def test_selection_is_refused_when_the_studio_asset_copy_was_tampered_with(self):
        self.add_shot(takes={"s01_sh010_t01_v01.mp4": b"one"})
        studio.sync(self.project, {"s01_sh010": "s01_sh010_t01_v01.mp4"})
        decision = self.review_and_decision()
        next((self.root / "assets").iterdir()).write_bytes(b"tampered")
        with self.assertRaisesRegex(studio.StudioError, "no longer matches"):
            studio.record_selection(self.project, "s01_sh010", decision)

    def test_recorded_selection_refreshes_the_storyboard_and_provenance(self):
        self.add_shot(takes={"s01_sh010_t01_v01.mp4": b"one"})
        studio.sync(self.project, {"s01_sh010": "s01_sh010_t01_v01.mp4"})
        studio.record_selection(self.project, "s01_sh010", self.review_and_decision())
        self.assertIn("- approval: approved", (self.root / "STORYBOARD.md").read_text())
        record = json.loads((self.root / "provenance.json").read_text())
        self.assertEqual(schema_findings(record, "studio-provenance.schema.json"), [])

    def test_candidates_copies_every_take_and_place_swaps_the_placed_one(self):
        self.add_shot(
            takes={"s01_sh010_t01_v01.mp4": b"one", "s01_sh010_t02_v01.mp4": b"two"},
            selected="s01_sh010_t01_v01.mp4",
        )
        studio.sync(self.project, probe=lambda path: 4.0)
        result = studio.candidates(self.project, "s01_sh010")
        assets = result["assets"]
        self.assertEqual((len(assets), result["skipped"]), (2, []))
        self.assertEqual(len(list((self.root / "assets").iterdir())), 2)
        result = studio.place_take(
            self.project, "s01_sh010", "s01_sh010_t02_v01.mp4", lambda path: 4.1
        )
        self.assertEqual(result["placed"], "s01_sh010_t02_v01.mp4")
        self.assertIn(
            result["asset"], (self.root / "compositions/s01_sh010.html").read_text()
        )
        self.assertIn(
            "- take: s01_sh010_t02_v01.mp4", (self.root / "STORYBOARD.md").read_text()
        )
        self.assertIn(
            "placed_differs_from_selection",
            [i["code"] for i in studio.status(self.project)["issues"]],
        )
        provenance = json.loads((self.root / "provenance.json").read_text())
        self.assertEqual(provenance["frames"][0]["take"], "s01_sh010_t02_v01.mp4")

    def test_place_refuses_a_take_of_a_different_length(self):
        self.add_shot(
            takes={"s01_sh010_t01_v01.mp4": b"one", "s01_sh010_t02_v01.mp4": b"two"},
            selected="s01_sh010_t01_v01.mp4",
        )
        studio.sync(self.project, probe=lambda path: 4.0)
        with self.assertRaisesRegex(studio.StudioError, "retime it in Studio"):
            studio.place_take(
                self.project, "s01_sh010", "s01_sh010_t02_v01.mp4", lambda path: 9.0
            )
        self.assertIn(
            f"s01_sh010_t01_v01__{sha(b'one')[:12]}.mp4",
            (self.root / "compositions/s01_sh010.html").read_text(),
        )

    def test_place_needs_an_existing_frame_and_a_safe_filename(self):
        self.add_shot(takes={"s01_sh010_t01_v01.mp4": b"one"})
        with self.assertRaisesRegex(studio.StudioError, "no frame yet"):
            studio.place_take(self.project, "s01_sh010", "s01_sh010_t01_v01.mp4")
        studio.sync(self.project, {"s01_sh010": "s01_sh010_t01_v01.mp4"})
        with self.assertRaises(studio.StudioError):
            studio.place_take(self.project, "s01_sh010", "../escape.mp4")

    def test_extra_compositions_do_not_block_status_or_delivery(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        (self.root / "compositions/title-card.html").write_text("<html></html>")
        result = studio.status(self.project)
        self.assertTrue(result["ok"])
        self.assertIn("orphan_frame", [i["code"] for i in result["issues"]])
        self.complete_through("shot-generation")

    def test_init_derives_the_canvas_from_the_shots_and_sync_follows_the_root(self):
        directory = self.add_shot(selected="s01_sh010_t01_v01.mp4")
        manifest = directory / "shot.md"
        manifest.write_text(
            manifest.read_text().replace('aspect: "16:9"', 'aspect: "9:16"')
        )
        code, _ = self.run_cli("init", str(self.project))
        self.assertEqual(code, 0)
        self.assertIn(
            'data-width="720" data-height="1280"',
            (self.root / "index.html").read_text(),
        )
        report = studio.sync(self.project)
        self.assertEqual(report.warnings, [])
        self.assertIn(
            'data-width="720" data-height="1280"',
            (self.root / "compositions/s01_sh010.html").read_text(),
        )

    def test_init_accepts_an_explicit_canvas(self):
        code, _ = self.run_cli(
            "init", str(self.project), "--aspect", "1:1", "--resolution", "1080p"
        )
        self.assertEqual(code, 0)
        self.assertEqual(studio.canvas_dimensions(self.project), (1080, 1080))

    def test_root_without_a_duration_gets_one(self):
        html = '<div id="root" data-composition-id="main" data-start="0">'
        self.assertIn(
            'data-duration="5"', studio.with_root_duration(html + "</div>", 5)
        )

    def test_non_finite_timing_is_rejected(self):
        for value in ("nan", "inf", "-inf"):
            with self.assertRaisesRegex(studio.StudioError, "invalid timing"):
                studio.timing(value, "host")

    def test_shot_ids_that_differ_only_by_case_are_duplicates(self):
        self.add_shot("s01_sh010", takes={})
        self.add_shot("S01_SH010", scene="scene-02", takes={})
        with self.assertRaisesRegex(studio.StudioError, "Duplicate shot id"):
            studio.discover_shots(self.project)

    def test_empty_or_malformed_takes_list_is_tolerated(self):
        directory = self.add_shot(takes={})
        manifest = directory / "shot.md"
        manifest.write_text(
            manifest.read_text().replace(
                "shot_id: s01_sh010\n", "shot_id: s01_sh010\ntakes:\n"
            )
        )
        self.assertEqual(studio.discover_shots(self.project)[0].takes, {})
        manifest.write_text(manifest.read_text().replace("takes:\n", "takes: none\n"))
        self.assertEqual(studio.discover_shots(self.project)[0].takes, {})

    def test_newer_draft_or_manual_records_do_not_hide_a_good_delivery_render(self):
        self.delivery_ready()
        studio.render(self.project, "final", "delivery", self.render_runner())
        self.lock_final()
        studio.render(self.project, "look", "draft", self.render_runner())
        manual = self.root / "renders" / "export.mp4"
        manual.write_bytes(b"external")
        studio.record_render(self.project, manual, ["render"], fake_runner())
        value = studio.complete_stage(
            self.project, "delivery", fake_runner(stdout=CHECK_OK)
        )
        entry = next(item for item in value["stages"] if item["id"] == "delivery")
        self.assertEqual(
            entry["evidence"]["render_record"], "studio/renders/final.mp4.render.json"
        )

    def test_edit_to_a_composition_or_asset_after_render_fails_delivery(self):
        self.delivery_ready()
        studio.render(self.project, "final", "delivery", self.render_runner())
        self.lock_final()
        composition = self.root / "compositions/s01_sh010.html"
        original = composition.read_text()
        composition.write_text(original + "<!-- edited -->")
        with self.assertRaisesRegex(studio.StudioError, "changed after"):
            studio.complete_stage(
                self.project, "delivery", fake_runner(stdout=CHECK_OK)
            )
        composition.write_text(original)
        studio.complete_stage(self.project, "delivery", fake_runner(stdout=CHECK_OK))
        studio.reopen_stage(self.project, "delivery")
        (self.root / "assets" / "music.mp3").write_bytes(b"added after the render")
        with self.assertRaisesRegex(studio.StudioError, "changed after"):
            studio.complete_stage(
                self.project, "delivery", fake_runner(stdout=CHECK_OK)
            )

    def test_project_changed_while_rendering_discards_the_render(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)

        def editing_during_render(argv, **kwargs):
            if argv[0] == "ffprobe":
                return subprocess.CompletedProcess(argv, 0, json.dumps(PROBE), "")
            Path(argv[argv.index("--output") + 1]).write_bytes(b"rendered")
            index = self.root / "index.html"
            index.write_text(index.read_text() + "<!-- edited in Studio -->")
            return subprocess.CompletedProcess(argv, 0, "", "")

        with self.assertRaisesRegex(studio.StudioError, "changed during the render"):
            studio.render(self.project, "final", "draft", editing_during_render)
        self.assertEqual(list((self.root / "renders").iterdir()), [])

    def test_probe_failure_after_render_removes_the_output(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)

        def no_probe(argv, **kwargs):
            if argv[0] == "ffprobe":
                return subprocess.CompletedProcess(argv, 1, "", "no ffprobe")
            Path(argv[argv.index("--output") + 1]).write_bytes(b"rendered")
            return subprocess.CompletedProcess(argv, 0, "", "")

        with self.assertRaisesRegex(studio.StudioError, "ffprobe failed"):
            studio.render(self.project, "final", "draft", no_probe)
        self.assertFalse((self.root / "renders/final.mp4").exists())

    def test_timeout_during_render_removes_the_partial_file(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)

        def hung(argv, **kwargs):
            Path(argv[argv.index("--output") + 1]).write_bytes(b"partial")
            raise subprocess.TimeoutExpired(argv, kwargs["timeout"])

        with self.assertRaisesRegex(studio.StudioError, "timed out"):
            studio.render(self.project, "final", "draft", hung)
        self.assertFalse((self.root / "renders/final.mp4").exists())

    def test_malformed_render_sidecars_are_ignored_not_fatal(self):
        self.delivery_ready()
        (self.root / "renders/broken.mp4.render.json").write_text("not json")
        (self.root / "renders/list.mp4.render.json").write_text("[]")
        (self.root / "renders/partial.mp4.render.json").write_text(
            json.dumps({"produced_by": "render"})
        )
        studio.render(self.project, "final", "delivery", self.render_runner())
        self.lock_final()
        studio.complete_stage(self.project, "delivery", fake_runner(stdout=CHECK_OK))

    def test_record_selection_needs_a_json_object(self):
        self.add_shot(takes={"s01_sh010_t01_v01.mp4": b"one"})
        studio.sync(self.project, {"s01_sh010": "s01_sh010_t01_v01.mp4"})
        with self.assertRaisesRegex(studio.StudioError, "one JSON object"):
            studio.record_selection(self.project, "s01_sh010", [])
        path = self.project / "decision.json"
        path.write_text("[]")
        code, payload = self.run_cli(
            "record-selection", str(self.project), "s01_sh010", "--decision", str(path)
        )
        self.assertEqual(code, 1)
        self.assertIn("JSON object", payload["error"])

    def test_candidates_skips_a_take_it_cannot_copy_and_says_so(self):
        directory = self.add_shot(takes={"s01_sh010_t01_v01.mp4": b"one"})
        outside = Path(self.temp.name).resolve() / "outside.mp4"
        outside.write_bytes(b"x")
        (directory / "s01_sh010_t02_v01.mp4").symlink_to(outside)
        result = studio.candidates(self.project, "s01_sh010")
        self.assertEqual(len(result["assets"]), 1)
        self.assertEqual(result["skipped"][0]["filename"], "s01_sh010_t02_v01.mp4")

    def test_place_falls_back_to_the_manifest_length_when_probing_fails(self):
        self.add_shot(
            takes={"s01_sh010_t01_v01.mp4": b"one", "s01_sh010_t02_v01.mp4": b"two"},
            selected="s01_sh010_t01_v01.mp4",
            duration=4,
        )
        studio.sync(self.project, probe=lambda path: 4.0)
        studio.place_take(
            self.project, "s01_sh010", "s01_sh010_t02_v01.mp4", lambda path: None
        )
        directory = self.project / "scenes/scene-01/s01_sh010"
        manifest = directory / "shot.md"
        manifest.write_text(
            "".join(
                line
                for line in manifest.read_text().splitlines(keepends=True)
                if "duration_s" not in line
            )
        )
        with self.assertRaisesRegex(studio.StudioError, "no duration recorded"):
            studio.place_take(
                self.project, "s01_sh010", "s01_sh010_t01_v01.mp4", lambda path: None
            )

    def test_hf_runs_only_allowed_commands_pinned_inside_the_studio_directory(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        runner = fake_runner(stdout="{}")
        studio.hf_command(self.project, ["preview", "--no-open", "--json"], runner)
        argv, kwargs = runner.calls[0]
        self.assertEqual(
            argv,
            [
                "npx",
                "--yes",
                f"hyperframes@{studio.HYPERFRAMES_VERSION}",
                "preview",
                "--no-open",
                "--json",
            ],
        )
        self.assertEqual(Path(kwargs["cwd"]), self.root)
        self.assertEqual(kwargs["env"]["HYPERFRAMES_SKIP_SKILLS"], "1")
        for command in (
            "publish",
            "cloud",
            "auth",
            "feedback",
            "upgrade",
            "skills",
            "init",
            "usage",
            "open",
            "lambda",
            "cloudrun",
        ):
            with self.assertRaisesRegex(studio.StudioError, "hf runs only"):
                studio.hf_command(self.project, [command], runner)
        with self.assertRaises(studio.StudioError):
            studio.hf_command(self.project, [], runner)

    def test_hyperframes_environment_keeps_the_producer_variables(self):
        with mock.patch.dict(os.environ, {"PRODUCER_HEADLESS_SHELL_PATH": "/x"}):
            self.assertEqual(
                studio.hyperframes_environment()["PRODUCER_HEADLESS_SHELL_PATH"], "/x"
            )

    def test_a_hand_edited_current_stage_is_rejected(self):
        studio.start_stage(self.project, "brief-development")
        path = self.root / "stages.json"
        value = json.loads(path.read_text())
        value["current_stage"] = "polish"
        path.write_text(json.dumps(value))
        with self.assertRaisesRegex(studio.StudioError, "stages.json is invalid"):
            studio.read_stages(self.project)

    def test_record_render_arguments_may_start_with_dashes(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        render = self.root / "renders" / "x.mp4"
        render.write_bytes(b"r")
        with mock.patch.object(studio, "probe_media", return_value=PROBE_SUMMARY):
            code, _ = self.run_cli(
                "record-render", str(self.project), str(render), "--quality", "delivery"
            )
        self.assertEqual(code, 0)
        record = json.loads((self.root / "renders/x.mp4.render.json").read_text())
        self.assertEqual(record["hyperframes"]["arguments"], ["--quality", "delivery"])

    def ready_for_assembly(self, mode="approve_for_me", skip_audio=True):
        self.write_project(mode)
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        studio.sync(self.project)
        self.complete_through("shot-generation", skip_audio=skip_audio)
        studio.start_stage(self.project, "assembly-review")

    def test_assembly_review_needs_a_picture_lock(self):
        self.ready_for_assembly()
        with self.assertRaisesRegex(studio.StudioError, "picture lock is required"):
            studio.complete_stage(
                self.project, "assembly-review", fake_runner(stdout=CHECK_OK)
            )
        self.lock_assembly()
        value = studio.complete_stage(
            self.project, "assembly-review", fake_runner(stdout=CHECK_OK)
        )
        entry = next(
            item for item in value["stages"] if item["id"] == "assembly-review"
        )
        self.assertEqual(entry["locks"]["picture"]["actor"], "agent")
        self.assertEqual(schema_findings(value, "studio-stages.schema.json"), [])

    def test_audio_lock_is_required_unless_audio_preparation_was_skipped(self):
        self.ready_for_assembly(skip_audio=False)
        self.lock_assembly()
        with self.assertRaisesRegex(studio.StudioError, "audio lock is required"):
            studio.complete_stage(
                self.project, "assembly-review", fake_runner(stdout=CHECK_OK)
            )
        (self.project / "library").mkdir()
        (self.project / "library/mix.wav").write_bytes(b"audio bytes")
        self.record_lock("audio", "library/mix.wav")
        studio.complete_stage(
            self.project, "assembly-review", fake_runner(stdout=CHECK_OK)
        )

    def test_user_can_lock_through_chat_under_ask_for_approval(self):
        self.ready_for_assembly("ask_for_approval")
        studio.render(self.project, "cut", "draft", self.render_runner())
        result = self.record_lock("picture", "studio/renders/cut.mp4")
        self.assertEqual(result["lock"], "picture")
        saved = json.loads((self.project / "decisions/lock-picture.json").read_text())
        self.assertEqual(
            (saved["actor"], saved["authorization"]["source"]), ("user", "chat")
        )
        studio.complete_stage(
            self.project, "assembly-review", fake_runner(stdout=CHECK_OK)
        )

    def test_agent_cannot_lock_under_ask_for_approval(self):
        self.ready_for_assembly("ask_for_approval")
        studio.render(self.project, "cut", "draft", self.render_runner())
        with self.assertRaisesRegex(
            studio.StudioError, "only valid when project.md sets approval_mode"
        ):
            self.record_lock("picture", "studio/renders/cut.mp4", actor="agent")
        self.assertFalse((self.project / "decisions").exists())

    def test_user_lock_needs_the_users_words(self):
        self.ready_for_assembly("ask_for_approval")
        studio.render(self.project, "cut", "draft", self.render_runner())
        decision = self.lock_decision(
            "picture",
            "studio/renders/cut.mp4",
            actor="user",
            authorization={"source": "chat", "evidence": " "},
        )
        with self.assertRaisesRegex(studio.StudioError, "authorization"):
            studio.record_lock(self.project, decision)

    def test_final_master_lock_completes_delivery_and_must_be_for_the_delivery_render(
        self,
    ):
        self.delivery_ready()
        studio.render(self.project, "first", "delivery", self.render_runner())
        self.lock_final("first")
        studio.render(self.project, "second", "delivery", self.render_runner())
        with self.assertRaisesRegex(studio.StudioError, "not for the delivery render"):
            studio.complete_stage(
                self.project, "delivery", fake_runner(stdout=CHECK_OK)
            )
        self.lock_final("second", decision_id="lock-final-2")
        value = studio.complete_stage(
            self.project, "delivery", fake_runner(stdout=CHECK_OK)
        )
        entry = next(item for item in value["stages"] if item["id"] == "delivery")
        self.assertEqual(
            entry["locks"]["final_master"]["artifact_path"], "studio/renders/second.mp4"
        )

    def test_delivery_without_a_final_master_lock_is_refused(self):
        self.delivery_ready()
        studio.render(self.project, "final", "delivery", self.render_runner())
        with self.assertRaisesRegex(
            studio.StudioError, "final_master lock is required"
        ):
            studio.complete_stage(
                self.project, "delivery", fake_runner(stdout=CHECK_OK)
            )

    def test_lock_subjects_must_be_recorded_renders_of_the_right_quality(self):
        self.delivery_ready()
        manual = self.root / "renders" / "export.mp4"
        manual.write_bytes(b"external")
        studio.record_render(self.project, manual, ["render"], fake_runner())
        with self.assertRaisesRegex(
            studio.StudioError, "not made by studio_project.py render"
        ):
            self.lock_final("export")
        studio.render(self.project, "look", "draft", self.render_runner())
        with self.assertRaisesRegex(studio.StudioError, "standard-or-higher"):
            self.lock_final("look")
        (self.root / "renders" / "stray.mp4").write_bytes(b"x")
        with self.assertRaisesRegex(studio.StudioError, "not a recorded render"):
            self.lock_final("stray")

    def test_a_lock_needs_the_stage_to_be_started_and_the_right_stage(self):
        self.ready_for_assembly()
        studio.render(self.project, "cut", "draft", self.render_runner())
        wrong = self.lock_decision(
            "picture", "studio/renders/cut.mp4", stage_id="delivery"
        )
        with self.assertRaisesRegex(studio.StudioError, "belongs to assembly-review"):
            studio.record_lock(self.project, wrong)
        studio.reopen_stage(self.project, "shot-generation")
        with self.assertRaisesRegex(studio.StudioError, "Start assembly-review"):
            self.record_lock("picture", "studio/renders/cut.mp4")

    def test_an_agent_cannot_replace_a_users_lock(self):
        self.ready_for_assembly()
        studio.render(self.project, "cut", "draft", self.render_runner())
        self.record_lock(
            "picture",
            "studio/renders/cut.mp4",
            actor="user",
            authorization=self.chat_authorization("lock the picture"),
        )
        with self.assertRaisesRegex(
            studio.StudioError, "cannot replace a user stage lock"
        ):
            self.record_lock(
                "picture", "studio/renders/cut.mp4", decision_id="agent-retry"
            )

    def test_a_locked_file_changed_afterwards_blocks_stage_exit(self):
        self.ready_for_assembly()
        self.lock_assembly()
        (self.root / "renders/cut.mp4").write_bytes(b"swapped after the lock")
        with self.assertRaisesRegex(studio.StudioError, "lock is stale"):
            studio.complete_stage(
                self.project, "assembly-review", fake_runner(stdout=CHECK_OK)
            )

    def test_reopening_a_stage_clears_its_locks(self):
        self.ready_for_assembly()
        self.lock_assembly()
        value = studio.reopen_stage(self.project, "assembly-review")
        entry = next(
            item for item in value["stages"] if item["id"] == "assembly-review"
        )
        self.assertNotIn("locks", entry)

    def test_lock_decisions_must_be_objects_of_the_right_type(self):
        self.ready_for_assembly()
        for bad in ([], {"decision_type": "variant_selection"}):
            with self.assertRaisesRegex(studio.StudioError, "stage_lock decision"):
                studio.record_lock(self.project, bad)

    def test_record_lock_through_the_cli(self):
        self.ready_for_assembly()
        studio.render(self.project, "cut", "draft", self.render_runner())
        decision = self.lock_decision("picture", "studio/renders/cut.mp4")
        path = self.project / "lock.json"
        path.write_text(json.dumps(decision))
        service = studio.selection_service()
        with mock.patch.object(
            service, "probe_media_streams", return_value={"video", "audio"}
        ):
            code, payload = self.run_cli(
                "record-lock", str(self.project), "--decision", str(path)
            )
        self.assertEqual((code, payload["lock"]), (0, "picture"))

    def add_scene_shot(
        self,
        scene="s01-dawn-movement",
        shot_id="s01_sh010",
        takes=("a", "b"),
        front="",
        bullets="- ratio: 16:9\n- resolution: 1080p\n",
    ):
        directory = self.project / "scenes" / scene
        directory.mkdir(parents=True, exist_ok=True)
        for index, label in enumerate(takes, start=1):
            (directory / f"{shot_id}_t0{index}_v01.mp4").write_bytes(
                f"take-{label}".encode()
            )
        (directory / "shot.md").write_text(
            f'---\nid: {shot_id}\ntitle: "Dawn Movement"\nselected_variant: null\nstatus: review\n{front}---\n\n# Shot — {shot_id}\n\n{bullets}'
        )
        return directory

    def test_scene_level_manifests_with_body_bullets_are_discovered(self):
        self.add_scene_shot()
        shots = studio.discover_shots(self.project)
        self.assertEqual([shot.shot_id for shot in shots], ["s01_sh010"])
        self.assertEqual(
            (shots[0].aspect, shots[0].resolution, shots[0].size_declared),
            ("16:9", "1080p", True),
        )
        self.assertEqual(shots[0].title, "Dawn Movement")
        report = studio.sync(
            self.project, {"s01_sh010": "s01_sh010_t01_v01.mp4"}, probe=lambda path: 5.0
        )
        self.assertEqual(report.added, ["s01_sh010"])
        self.assertEqual(studio.canvas_dimensions(self.project), (1920, 1080))

    def test_both_manifest_layouts_can_live_in_one_project(self):
        self.add_shot(
            "s02_sh010",
            takes={"s02_sh010_t01_v01.mp4": b"x"},
            selected="s02_sh010_t01_v01.mp4",
        )
        self.add_scene_shot()
        self.assertEqual(
            {shot.shot_id for shot in studio.discover_shots(self.project)},
            {"s01_sh010", "s02_sh010"},
        )

    def test_duplicate_ids_across_layouts_are_rejected(self):
        self.add_shot("s01_sh010", takes={})
        self.add_scene_shot()
        with self.assertRaisesRegex(studio.StudioError, "Duplicate shot id"):
            studio.discover_shots(self.project)

    def test_selected_take_alias_and_a_missing_recommendation(self):
        self.add_scene_shot(front="selected_take: s01_sh010_t02_v01.mp4\n")
        manifest = self.project / "scenes/s01-dawn-movement/shot.md"
        manifest.write_text(
            manifest.read_text().replace("selected_variant: null\n", "")
        )
        self.assertEqual(
            studio.discover_shots(self.project)[0].selected_variant,
            "s01_sh010_t02_v01.mp4",
        )

    def test_recommended_take_is_placed_only_when_the_file_exists(self):
        directory = self.add_scene_shot(
            front="recommended_take: s01_sh010_t02_v01.mp4\n"
        )
        report = studio.sync(self.project, probe=lambda path: 5.0)
        self.assertEqual(report.added, ["s01_sh010"])
        self.assertIn("t02_v01", studio.placed_asset(self.project, "s01_sh010"))
        shutil.rmtree(self.root)
        manifest = directory / "shot.md"
        manifest.write_text(manifest.read_text().replace("t02_v01.mp4", "t99_v01.mp4"))
        report = studio.sync(self.project, probe=lambda path: 5.0)
        self.assertEqual((report.added, report.outlined), ([], ["s01_sh010"]))

    def test_undeclared_size_is_measured_from_the_real_take(self):
        self.add_scene_shot(bullets="")
        self.assertFalse(studio.discover_shots(self.project)[0].size_declared)
        studio.sync(
            self.project,
            {"s01_sh010": "s01_sh010_t01_v01.mp4"},
            probe=lambda path: 5.0,
            size_probe=lambda path: (720, 1280),
        )
        self.assertEqual(studio.canvas_dimensions(self.project), (720, 1280))

    def test_undeclared_size_falls_back_when_measuring_fails(self):
        self.add_scene_shot(bullets="")
        studio.sync(
            self.project,
            {"s01_sh010": "s01_sh010_t01_v01.mp4"},
            probe=lambda path: 5.0,
            size_probe=lambda path: None,
        )
        self.assertEqual(studio.canvas_dimensions(self.project), (1280, 720))

    def test_probe_size_reads_ffprobe_output_and_rounds_to_even(self):
        good = fake_runner(
            stdout=json.dumps({"streams": [{"width": 719, "height": 1279}]})
        )
        self.assertEqual(studio.probe_size(Path("x.mp4"), good), (720, 1280))
        self.assertIsNone(
            studio.probe_size(Path("x.mp4"), fake_runner(returncode=1, stdout=""))
        )
        self.assertIsNone(
            studio.probe_size(
                Path("x.mp4"), fake_runner(stdout=json.dumps({"streams": []}))
            )
        )

    def test_a_manifest_bullet_list_is_not_used_as_the_narrative(self):
        self.add_scene_shot(bullets="- scene: s01\n- takes: 2\n- ratio: 16:9\n")
        self.assertEqual(studio.discover_shots(self.project)[0].narrative, "")
        body = "# Shot\n\n- scene: s01\n- takes: 2\n\nA runner crosses the street at dawn.\n"
        self.assertEqual(
            studio.shot_narrative(body), "A runner crosses the street at dawn."
        )

    def test_assets_are_named_take_first_so_they_group_by_shot(self):
        name = studio.asset_name("a" * 64, "s01_sh010_t02_v01.mp4")
        self.assertEqual(name, "s01_sh010_t02_v01__aaaaaaaaaaaa.mp4")
        self.assertEqual(
            studio.split_asset(name), ("aaaaaaaaaaaa", "s01_sh010_t02_v01.mp4")
        )
        self.assertEqual(studio.split_asset("custom.mp4"), ("", "custom.mp4"))
        self.assertEqual(
            studio.split_asset("clip__nothex.mp4"), ("", "clip__nothex.mp4")
        )

    def run_cli(self, *arguments):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = studio.main([*arguments])
        return code, json.loads(buffer.getvalue())

    def test_cli_sync_and_status_exit_codes(self):
        self.add_shot(selected="s01_sh010_t01_v01.mp4")
        code, payload = self.run_cli("sync", str(self.project))
        self.assertEqual((code, payload["added"]), (0, ["s01_sh010"]))
        code, payload = self.run_cli("status", str(self.project))
        self.assertEqual((code, payload["ok"]), (0, True))
        (self.project / "scenes/scene-01/s01_sh010/s01_sh010_t01_v01.mp4").write_bytes(
            b"changed"
        )
        code, payload = self.run_cli("status", str(self.project))
        self.assertEqual((code, payload["ok"]), (3, False))

    def test_cli_reports_errors_as_json(self):
        code, payload = self.run_cli("sync", str(self.project))
        self.assertEqual(code, 1)
        self.assertFalse(payload["ok"])
        self.assertIn("No shot manifests", payload["error"])

    def test_cli_rejects_malformed_take_option(self):
        self.add_shot()
        code, payload = self.run_cli(
            "sync", str(self.project), "--take", "no-separator"
        )
        self.assertEqual(code, 1)
        self.assertIn("--take", payload["error"])


if __name__ == "__main__":
    unittest.main()


class StudioElementLockTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name).resolve() / "demo"
        self.project.mkdir()
        self.write_project("approve_for_me")
        studio.init_studio(self.project, "9:16", "1080p")

    def write_project(self, mode):
        (self.project / "project.md").write_text(
            f"---\napproval_mode: {mode}\n---\n\n# Demo\n"
        )

    def add_element(
        self, element_id="mira", versions=("v01", "v02", "v03"), status="review"
    ):
        directory = self.project / "elements" / element_id
        directory.mkdir(parents=True, exist_ok=True)
        names = []
        for version in versions:
            name = f"char_{element_id}_turnaround_{version}.png"
            (directory / name).write_bytes(f"{element_id}-{version}".encode())
            names.append(name)
            self.write_review(element_id, name, version != "v01")
        (directory / "element.md").write_text(
            f"---\nelement_id: {element_id}\ntype: character\nstatus: {status}\n"
            f"variants: [{', '.join(names)}]\n---\n\n# {element_id}\n"
        )
        return names

    def write_review(self, element_id, name, passing=True):
        relative = f"elements/{element_id}/{name}"
        review = {
            "schema_version": 1,
            "artifact_path": relative,
            "artifact_sha256": sha((self.project / relative).read_bytes()),
            "status": "pass" if passing else "fail",
            "inspection_method": "direct visual inspection of the full image",
            "coverage": "whole sheet",
            "checks": [
                {
                    "criterion": "sheet",
                    "status": "pass" if passing else "fail",
                    "evidence": "fixture evidence",
                }
            ],
            "observations": ["Reads well" if passing else "Glossy skin"],
            "limitations": [],
            "recommendation": "Select." if passing else "Reject.",
        }
        stem = name.rsplit(".", 1)[0]
        path = self.project / f"elements/{element_id}/review_candidate_{stem}.json"
        path.write_text(json.dumps(review))

    def decision(
        self, element_id, name, actor="agent", authorization=None, decision_id=None
    ):
        relative = f"elements/{element_id}/{name}"
        stem = name.rsplit(".", 1)[0]
        review = f"elements/{element_id}/review_candidate_{stem}.json"
        mode = (
            "approve_for_me"
            if "approve_for_me" in (self.project / "project.md").read_text()
            else "ask_for_approval"
        )
        decision = {
            "schema_version": 1,
            "decision_id": decision_id or f"select_{element_id}_{stem[-3:]}",
            "decision_type": "variant_selection",
            "asset_id": element_id,
            "subject_path": relative,
            "selected_variant": name,
            "selected_sha256": sha((self.project / relative).read_bytes()),
            "actor": actor,
            "approval_mode": mode,
            "project_sha256": sha((self.project / "project.md").read_bytes()),
            "result": "approved",
            "review_path": review,
            "review_sha256": sha((self.project / review).read_bytes()),
            "upstream_sha256": {},
            "reason": "Passes the recorded checks.",
            "decided_at": datetime.datetime.now(datetime.UTC).isoformat(),
        }
        if authorization is not None:
            decision["authorization"] = authorization
        return decision

    @property
    def assets(self):
        return self.project / "studio/assets"

    def locked_files(self):
        return sorted(path.name for path in self.assets.glob("LOCKED_*"))

    def test_lock_records_the_decision_and_puts_only_the_locked_file_in_studio(self):
        names = self.add_element()
        result = studio.record_element_lock(
            self.project, "mira", self.decision("mira", names[2])
        )
        self.assertTrue(result["ok"])
        manifest = (self.project / "elements/mira/element.md").read_text()
        self.assertIn(f"selected_variant: {names[2]}", manifest)
        self.assertIn("status: approved", manifest)
        self.assertTrue((self.project / "decisions/select_mira_v03.json").is_file())
        self.assertEqual(self.locked_files(), ["LOCKED_mira_v03.png"])
        self.assertEqual(
            sorted(path.name for path in self.assets.iterdir()), ["LOCKED_mira_v03.png"]
        )

    def test_relocking_replaces_the_previous_studio_copy(self):
        names = self.add_element()
        studio.record_element_lock(
            self.project, "mira", self.decision("mira", names[1])
        )
        self.assertEqual(self.locked_files(), ["LOCKED_mira_v02.png"])
        studio.record_element_lock(
            self.project,
            "mira",
            self.decision("mira", names[2], decision_id="select_mira_again"),
        )
        self.assertEqual(self.locked_files(), ["LOCKED_mira_v03.png"])

    def test_page_and_index_show_locked_and_other_samples_without_a_script(self):
        names = self.add_element()
        studio.record_element_lock(
            self.project, "mira", self.decision("mira", names[2])
        )
        page = (self.project / "review/elements.html").read_text()
        self.assertTrue((self.project / "review/elements.css").is_file())
        self.assertNotIn("<script", page)
        self.assertIn('href="elements.css"', page)
        self.assertIn("LOCKED", page)
        self.assertEqual(page.count("OTHER"), 2)
        self.assertIn("../elements/mira/char_mira_turnaround_v03.png", page)
        self.assertIn("Glossy skin", page)
        index = (self.project / "elements/INDEX.md").read_text()
        self.assertIn("LOCKED_mira_v03.png", index)
        self.assertNotIn("v01.png", index)

    def test_a_variant_outside_the_manifest_is_refused(self):
        names = self.add_element()
        rogue = self.project / "elements/mira/char_mira_turnaround_v09.png"
        rogue.write_bytes(b"rogue")
        decision = self.decision("mira", names[0])
        decision["selected_variant"] = rogue.name
        with self.assertRaises(studio.StudioError):
            studio.record_element_lock(self.project, "mira", decision)
        self.assertEqual(self.locked_files(), [])

    def test_unsafe_element_ids_are_refused(self):
        self.add_element()
        for bad in ("../mira", "Mira", "mira/../mira", ""):
            with self.assertRaises(studio.StudioError):
                studio.record_element_lock(self.project, bad, {})

    def test_agent_cannot_lock_under_ask_for_approval(self):
        self.write_project("ask_for_approval")
        names = self.add_element()
        with self.assertRaises(studio.StudioError):
            studio.record_element_lock(
                self.project, "mira", self.decision("mira", names[2])
            )
        self.assertEqual(self.locked_files(), [])

    def test_user_chat_lock_works_and_an_agent_cannot_replace_it(self):
        self.write_project("ask_for_approval")
        names = self.add_element()
        user = self.decision(
            "mira",
            names[1],
            actor="user",
            authorization={"source": "chat", "evidence": "lock Mira v02"},
        )
        studio.record_element_lock(self.project, "mira", user)
        self.assertEqual(self.locked_files(), ["LOCKED_mira_v02.png"])
        self.write_project("approve_for_me")
        agent = self.decision("mira", names[2], decision_id="agent_override")
        with self.assertRaises((studio.StudioError, ValueError)):
            studio.record_element_lock(self.project, "mira", agent)
        self.assertEqual(self.locked_files(), ["LOCKED_mira_v02.png"])

    def test_sync_removes_stale_locked_copies_and_keeps_other_assets(self):
        names = self.add_element()
        studio.record_element_lock(
            self.project, "mira", self.decision("mira", names[2])
        )
        (self.assets / "LOCKED_ghost_v01.png").write_bytes(b"stale")
        (self.assets / "s01_sh010_t01_v01__abc.mp4").write_bytes(b"take")
        report = studio.sync_elements(self.project)
        self.assertEqual(report["removed"], ["LOCKED_ghost_v01.png"])
        self.assertEqual(self.locked_files(), ["LOCKED_mira_v03.png"])
        self.assertTrue((self.assets / "s01_sh010_t01_v01__abc.mp4").is_file())

    def test_sync_ignores_elements_that_are_not_approved(self):
        self.add_element("nena", versions=("v01",), status="review")
        report = studio.sync_elements(self.project)
        self.assertEqual(report["locked"], [])
        self.assertEqual(self.locked_files(), [])

    def test_sync_needs_an_initialised_studio_project(self):
        shutil.rmtree(self.project / "studio")
        with self.assertRaises(studio.StudioError):
            studio.sync_elements(self.project)

    def test_canvas_projects_are_refused(self):
        self.add_element()
        (self.project / "showcase.json").write_text("{}")
        with self.assertRaises(studio.StudioError):
            studio.sync_elements(self.project)

    def test_cli_lock_element_and_sync_elements(self):
        names = self.add_element()
        decision_file = self.project / "decision.json"
        decision_file.write_text(json.dumps(self.decision("mira", names[2])))
        with contextlib.redirect_stdout(io.StringIO()):
            code = studio.main(
                [
                    "lock-element",
                    str(self.project),
                    "mira",
                    "--decision",
                    str(decision_file),
                ]
            )
            self.assertEqual(code, 0)
            self.assertEqual(self.locked_files(), ["LOCKED_mira_v03.png"])
            (self.assets / "LOCKED_mira_v03.png").unlink()
            self.assertEqual(studio.main(["sync-elements", str(self.project)]), 0)
        self.assertEqual(self.locked_files(), ["LOCKED_mira_v03.png"])
