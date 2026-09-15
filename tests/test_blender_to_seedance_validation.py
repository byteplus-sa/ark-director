import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents/skills/blender-to-seedance"
VALIDATOR_PATH = SKILL / "scripts/validate_blockout_manifest.py"
PROBE_PATH = SKILL / "scripts/probe_blender_runtime.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validation = load_module("blockout_validation", VALIDATOR_PATH)
runtime_probe = load_module("blender_runtime_probe", PROBE_PATH)


class BlenderToSeedanceValidationTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {
            "schema_version": "1.0",
            "shot_id": "s01_sh010",
            "source": {
                "blend_path": "scenes/scene-01/s01_sh010/blockout.blend",
                "blend_sha256": "1" * 64,
            },
            "timeline": {
                "fps": 24,
                "fps_base": 1.0,
                "frame_start": 1,
                "frame_end": 240,
                "duration_seconds": 10.0,
            },
            "render": {
                "previz_path": "scenes/scene-01/s01_sh010/previz_s01_sh010_v01.mp4",
                "previz_sha256": "2" * 64,
                "width": 1920,
                "height": 1080,
                "resolution_percentage": 100,
                "container": "MPEG4",
                "codec": "H264",
            },
            "cameras": [
                {"id": "camera-main", "object_name": "Camera_Main"},
                {"id": "camera-detail", "object_name": "Camera_Detail"},
            ],
            "cuts": [
                {"frame": 1, "camera": "camera-main"},
                {"frame": 121, "camera": "camera-detail"},
            ],
            "subjects": [
                {
                    "id": "car-red",
                    "object_name": "CAR_RED",
                    "proxy_role": "vehicle",
                    "final_subject": "red rally car",
                    "proxy_color": "#d61f2c",
                    "appearance_reference": "@Image 1",
                },
                {
                    "id": "countertop",
                    "object_name": "COUNTERTOP",
                    "proxy_role": "support",
                    "final_subject": "kitchen countertop",
                    "proxy_color": "#808080",
                },
            ],
            "motion_checks": [
                {
                    "id": "car-advances",
                    "type": "world_displacement",
                    "subject": "car-red",
                    "start_frame": 1,
                    "end_frame": 120,
                    "rule": "The car advances at least two meters along positive Y.",
                    "expectation": {
                        "axis": "Y",
                        "direction": "positive",
                        "minimum_delta": 2.0,
                    },
                },
                {
                    "id": "car-contact",
                    "type": "ground_contact",
                    "subject": "car-red",
                    "target": "countertop",
                    "start_frame": 1,
                    "end_frame": 240,
                    "rule": "The tires remain on the countertop.",
                    "expectation": {"maximum_gap": 0.02},
                },
            ],
            "conditioning": {"control_only": True},
        }

    def rule_ids(self, findings):
        return {finding.rule_id for finding in findings}

    def test_valid_manifest_passes_without_mutation(self):
        before = copy.deepcopy(self.manifest)
        self.assertEqual(validation.validate_manifest(self.manifest), [])
        self.assertEqual(self.manifest, before)

    def test_timeline_and_render_drift_are_rejected(self):
        self.manifest["timeline"]["fps_base"] = 1.001
        self.manifest["timeline"]["duration_seconds"] = 9.0
        self.manifest["render"]["width"] = 1280
        self.manifest["render"]["codec"] = "HEVC"
        rules = self.rule_ids(validation.validate_manifest(self.manifest))
        self.assertIn("previz.timeline", rules)
        self.assertIn("previz.render", rules)

    def test_subject_cut_and_motion_references_are_checked(self):
        self.manifest["subjects"].append(copy.deepcopy(self.manifest["subjects"][0]))
        self.manifest["cuts"][0]["frame"] = 2
        self.manifest["cuts"][1]["camera"] = "camera-missing"
        self.manifest["motion_checks"][0]["subject"] = "car-missing"
        self.manifest["motion_checks"][1]["end_frame"] = 999
        rules = self.rule_ids(validation.validate_manifest(self.manifest))
        self.assertIn("blockout.subjects", rules)
        self.assertIn("blockout.cuts", rules)
        self.assertIn("blockout.motion", rules)

    def test_selected_conditioning_requires_current_hash_and_evidence(self):
        self.manifest["conditioning"] = {
            "control_only": False,
            "selection_manifest": "selections/shot-selection.json",
            "selection_field": "selected_variant",
            "selection_key": "previz-v02",
            "selected_previz_sha256": "3" * 64,
        }
        rules = self.rule_ids(validation.validate_manifest(self.manifest))
        self.assertIn("conditioning.source_current", rules)

    def test_type_specific_motion_expectations_are_required(self):
        self.manifest["motion_checks"][0]["expectation"] = {"trend": "decreasing"}
        self.manifest["motion_checks"][1].pop("target")
        rules = self.rule_ids(validation.validate_manifest(self.manifest))
        self.assertIn("blockout.motion", rules)

    def test_malformed_values_and_unsafe_paths_return_findings(self):
        for value in (None, [], {}, {"timeline": "bad"}):
            with self.subTest(value=value):
                self.assertTrue(validation.validate_manifest(value))
        self.manifest["source"]["blend_path"] = "/tmp/scene.blend"
        self.manifest["render"]["previz_path"] = "../outside.mp4"
        self.assertIn(
            "blockout.paths",
            self.rule_ids(validation.validate_manifest(self.manifest)),
        )

    def test_schema_is_valid_and_cli_has_meaningful_status(self):
        schema_path = SKILL / "references/blockout-manifest.schema.json"
        Draft202012Validator.check_schema(json.loads(schema_path.read_text()))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(json.dumps(self.manifest))
            valid = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), str(path)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(valid.returncode, 0)
            self.assertTrue(json.loads(valid.stdout)["ok"])
            self.manifest["timeline"]["duration_seconds"] = 1.0
            path.write_text(json.dumps(self.manifest))
            invalid = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), str(path)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(invalid.returncode, 1)
            self.assertFalse(json.loads(invalid.stdout)["ok"])

    def test_runtime_probe_selects_supported_eevee_identifier(self):
        render = types.SimpleNamespace(
            engine="BLENDER_EEVEE",
            resolution_x=1920,
            resolution_y=1080,
            resolution_percentage=100,
            fps=24,
            fps_base=1.0,
        )
        scene = types.SimpleNamespace(
            name="Scene",
            render=render,
            frame_start=1,
            frame_end=240,
        )
        engine_property = types.SimpleNamespace(
            enum_items_static=[
                types.SimpleNamespace(identifier="CYCLES"),
                types.SimpleNamespace(identifier="BLENDER_EEVEE"),
            ]
        )
        render_settings = types.SimpleNamespace(
            bl_rna=types.SimpleNamespace(properties={"engine": engine_property})
        )
        bpy_module = types.SimpleNamespace(
            app=types.SimpleNamespace(version=(5, 2, 0), version_string="5.2.0 LTS"),
            context=types.SimpleNamespace(scene=scene),
            types=types.SimpleNamespace(RenderSettings=render_settings),
        )
        result = runtime_probe.collect_runtime(bpy_module, python_version="3.13.13")
        self.assertEqual(result["recommended_eevee_engine"], "BLENDER_EEVEE")
        self.assertEqual(result["effective_fps"], 24.0)
        self.assertEqual(
            runtime_probe.choose_eevee_engine(["BLENDER_EEVEE_NEXT"]),
            "BLENDER_EEVEE_NEXT",
        )
        self.assertIsNone(runtime_probe.choose_eevee_engine(["CYCLES"]))


if __name__ == "__main__":
    unittest.main()
