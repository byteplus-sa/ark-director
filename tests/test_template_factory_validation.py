import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / ".agents/skills/template-factory/scripts/validate_breakdown.py"
SPEC = importlib.util.spec_from_file_location("template_validation", VALIDATOR_PATH)
validation = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validation
SPEC.loader.exec_module(validation)


class TemplateFactoryValidationTests(unittest.TestCase):
    def setUp(self):
        self.breakdown = {
            "schema_version": "1.0",
            "title": "Fixture",
            "genre": "commercial",
            "visual_style": {
                "grade": "warm",
                "lighting_direction": "side key",
                "lens": "wide",
                "film_look": "clean digital",
            },
            "camera": {
                "shot_sizes": ["wide"],
                "moves": ["dolly"],
                "framing": "centered",
                "transitions": ["hard cut"],
            },
            "audio": {
                "mode": "silent",
                "music": None,
                "sfx": [],
                "dialogue": None,
            },
            "elements": [
                {
                    "type": "prop",
                    "id": "hero-shoe",
                    "tag": "@hero-shoe",
                    "descriptor": "red running shoe with a white sole",
                    "keyframe_index": [1],
                    "in_shots": [1, 2],
                }
            ],
            "shots": [self.shot(1, 0.0, 1.0), self.shot(2, 1.0, 2.0)],
        }

    def shot(self, index, start, end):
        return {
            "index": index,
            "start_s": start,
            "end_s": end,
            "duration_s": end - start,
            "composition": "centered product",
            "camera": "locked",
            "action": "shoe rotates",
            "lighting": "soft side key",
            "audio": "silent",
            "end_state": "shoe faces camera",
        }

    def motion_review(self, analysis_bytes, order=(1, 2), mode="source"):
        by_index = {shot["index"]: shot for shot in self.breakdown["shots"]}
        result = {
            "schema_version": "1.0",
            "source_breakdown_sha256": hashlib.sha256(analysis_bytes).hexdigest(),
            "mode": mode,
            "shots": [],
            "top_directing_prompt_text": ["Rotate the shoe steadily."],
        }
        for index in order:
            shot = by_index[index]
            result["shots"].append(
                {
                    "shot_index": index,
                    "start_s": shot["start_s"],
                    "end_s": shot["end_s"],
                    "visible_content": {
                        "subjects": ["shoe"],
                        "background_elements": [],
                        "effects": [],
                    },
                    "motion": {
                        "camera_motion": "locked",
                        "moving_elements": [
                            {
                                "name": "shoe",
                                "motion": "rotation",
                                "direction": "clockwise",
                                "speed": "slow",
                                "amplitude": "quarter turn",
                                "easing": "linear",
                                "loop_period": None,
                            }
                        ],
                        "light_motion": "steady",
                        "strongest_cue": "shoe rotation",
                    },
                    "confidence": "high",
                    "uncertain_estimates": [],
                    "directing_prompt_text": "Rotate the shoe clockwise.",
                }
            )
        if mode == "comparison":
            result["global_diffs"] = {
                "pace_cut_timing": "matched",
                "energy_level": "lower",
                "aesthetic": "matched",
            }
            for shot in result["shots"]:
                shot["missing_or_wrong"] = ["rotation is slow"]
                shot["concrete_fix_prompt_text"] = "Increase rotation speed."
        return result

    def audio_analysis(self, analysis_bytes):
        return {
            "schema_version": "1.0",
            "source_pin_sha256": "a" * 64,
            "source_breakdown_sha256": hashlib.sha256(analysis_bytes).hexdigest(),
            "picture_duration_s": 2.0,
            "audio_stream": {
                "status": "present",
                "duration_s": 2.2,
                "channels": 2,
                "sample_rate_hz": 48000,
            },
            "auditory_review": {
                "status": "completed",
                "method": "ark_mcp_seed_audio_understand",
                "evidence_ref": "resp_fixture_audio_review",
            },
            "soundscape": {
                "music": "A soft instrumental pulse rises to a final accent.",
                "speech": None,
                "effects": ["A click on the cut."],
                "ambience": None,
                "dynamic_arc": "Quiet opening, stronger final accent, short tail.",
            },
            "events": [
                {
                    "start_s": 0.9,
                    "end_s": 1.1,
                    "kind": "sfx",
                    "description": "A short click bridges the cut.",
                    "evidence": "listening",
                    "confidence": "high",
                    "synced_shots": [1, 2],
                },
                {
                    "start_s": 2.0,
                    "end_s": 2.2,
                    "kind": "music",
                    "description": "The score fades after picture ends.",
                    "evidence": "listening",
                    "confidence": "high",
                    "synced_shots": [],
                },
            ],
            "reproduction": {
                "locked_audio_grammar": ["Keep a quiet opening and one final accent."],
                "replaceable_audio": ["Use a newly selected instrumental track."],
                "sync_rules": ["Place one short accent across the visual cut."],
            },
        }

    def rule_ids(self, findings):
        return {finding.rule_id for finding in findings}

    def test_valid_breakdown_and_reversed_motion_order_pass_without_mutation(self):
        before = copy.deepcopy(self.breakdown)
        analysis_bytes = json.dumps(self.breakdown).encode()
        motion = self.motion_review(analysis_bytes, order=(2, 1))
        self.assertEqual(
            validation.validate_breakdown(self.breakdown, source_duration_s=2.0), []
        )
        self.assertEqual(
            validation.validate_motion_review(
                motion,
                self.breakdown,
                breakdown_sha256=hashlib.sha256(analysis_bytes).hexdigest(),
            ),
            [],
        )
        self.assertEqual(self.breakdown, before)

    def test_invalid_timeline_and_element_references_are_rejected(self):
        self.breakdown["shots"][0]["duration_s"] = 9.0
        self.breakdown["shots"][1]["start_s"] = 0.5
        self.breakdown["elements"][0]["keyframe_index"] = [9]
        rules = self.rule_ids(validation.validate_breakdown(self.breakdown))
        self.assertIn("breakdown.timeline", rules)
        self.assertIn("breakdown.element_references", rules)

    def test_nonfinite_times_duplicate_ids_and_blank_fields_are_rejected(self):
        self.breakdown["shots"][0]["start_s"] = float("nan")
        self.breakdown["shots"][1]["index"] = 1
        self.breakdown["elements"].append(copy.deepcopy(self.breakdown["elements"][0]))
        self.breakdown["shots"][0]["action"] = ""
        rules = self.rule_ids(validation.validate_breakdown(self.breakdown))
        self.assertIn("breakdown.schema", rules)
        self.assertIn("breakdown.timeline", rules)
        self.assertIn("breakdown.element_references", rules)

    def test_malformed_nested_types_return_findings_without_exceptions(self):
        motion = self.motion_review(json.dumps(self.breakdown).encode())
        self.breakdown["shots"][0]["index"] = {"bad": "value"}
        self.breakdown["elements"][0]["keyframe_index"] = [{"bad": "value"}]
        findings = validation.validate_breakdown(
            self.breakdown, source_duration_s=float("inf")
        )
        self.assertTrue(findings)

        analysis_bytes = json.dumps(self.breakdown).encode()
        motion["shots"][0]["shot_index"] = {"bad": "value"}
        self.assertTrue(
            validation.validate_motion_review(
                motion,
                self.breakdown,
                breakdown_sha256=hashlib.sha256(analysis_bytes).hexdigest(),
            )
        )
        audio = self.audio_analysis(analysis_bytes)
        audio["audio_stream"]["status"] = {"bad": "value"}
        audio["events"][0]["synced_shots"] = [{"bad": "value"}]
        self.assertTrue(
            validation.validate_audio_analysis(
                audio,
                self.breakdown,
                breakdown_sha256=hashlib.sha256(analysis_bytes).hexdigest(),
                source_pin_sha256="a" * 64,
            )
        )

    def test_stale_or_misaligned_motion_review_is_rejected(self):
        analysis_bytes = json.dumps(self.breakdown).encode()
        motion = self.motion_review(analysis_bytes)
        motion["source_breakdown_sha256"] = "0" * 64
        motion["shots"][0]["start_s"] = 0.4
        motion["shots"].pop()
        rules = self.rule_ids(
            validation.validate_motion_review(
                motion,
                self.breakdown,
                breakdown_sha256=hashlib.sha256(analysis_bytes).hexdigest(),
            )
        )
        self.assertIn("motion.source_current", rules)
        self.assertIn("motion.shot_alignment", rules)

    def test_audio_analysis_accepts_picture_synced_cue_and_audio_tail(self):
        analysis_bytes = json.dumps(self.breakdown).encode()
        audio = self.audio_analysis(analysis_bytes)
        self.assertEqual(
            validation.validate_audio_analysis(
                audio,
                self.breakdown,
                breakdown_sha256=hashlib.sha256(analysis_bytes).hexdigest(),
                source_pin_sha256="a" * 64,
            ),
            [],
        )

    def test_audio_analysis_rejects_stale_source_and_invalid_cue_timing(self):
        analysis_bytes = json.dumps(self.breakdown).encode()
        audio = self.audio_analysis(analysis_bytes)
        audio["source_pin_sha256"] = "b" * 64
        audio["source_breakdown_sha256"] = "c" * 64
        audio["events"][0]["synced_shots"] = [2, 9]
        audio["events"][1]["end_s"] = 2.4
        rules = self.rule_ids(
            validation.validate_audio_analysis(
                audio,
                self.breakdown,
                breakdown_sha256=hashlib.sha256(analysis_bytes).hexdigest(),
                source_pin_sha256="a" * 64,
            )
        )
        self.assertIn("audio.source_current", rules)
        self.assertIn("audio.timeline", rules)
        self.assertIn("audio.beat_alignment", rules)

    def test_audio_analysis_rejects_events_without_audio_and_measurement_as_identification(
        self,
    ):
        analysis_bytes = json.dumps(self.breakdown).encode()
        audio = self.audio_analysis(analysis_bytes)
        audio["audio_stream"] = {
            "status": "absent",
            "duration_s": None,
            "channels": None,
            "sample_rate_hz": None,
        }
        audio["events"][0]["evidence"] = "measurement"
        rules = self.rule_ids(
            validation.validate_audio_analysis(
                audio,
                self.breakdown,
                breakdown_sha256=hashlib.sha256(analysis_bytes).hexdigest(),
                source_pin_sha256="a" * 64,
            )
        )
        self.assertIn("audio.availability", rules)
        self.assertIn("audio.evidence", rules)

    def test_audio_analysis_requires_auditory_provenance_for_sound_labels(self):
        analysis_bytes = json.dumps(self.breakdown).encode()
        audio = self.audio_analysis(analysis_bytes)
        audio["auditory_review"] = {
            "status": "unavailable",
            "method": None,
            "evidence_ref": None,
        }
        rules = self.rule_ids(
            validation.validate_audio_analysis(
                audio,
                self.breakdown,
                breakdown_sha256=hashlib.sha256(analysis_bytes).hexdigest(),
                source_pin_sha256="a" * 64,
            )
        )
        self.assertIn("audio.auditory_evidence", rules)
        audio["auditory_review"] = {
            "status": "completed",
            "method": "ark_mcp_seed_audio_understand",
            "evidence_ref": None,
        }
        rules = self.rule_ids(
            validation.validate_audio_analysis(
                audio,
                self.breakdown,
                breakdown_sha256=hashlib.sha256(analysis_bytes).hexdigest(),
                source_pin_sha256="a" * 64,
            )
        )
        self.assertIn("audio.auditory_evidence", rules)

    def test_audio_analysis_rejects_legacy_arkcli_review_method(self):
        analysis_bytes = json.dumps(self.breakdown).encode()
        audio = self.audio_analysis(analysis_bytes)
        audio["auditory_review"]["method"] = "arkcli_vau"
        rules = self.rule_ids(
            validation.validate_audio_analysis(
                audio,
                self.breakdown,
                breakdown_sha256=hashlib.sha256(analysis_bytes).hexdigest(),
                source_pin_sha256="a" * 64,
            )
        )
        self.assertIn("audio.schema", rules)

    def test_audio_analysis_accepts_measured_silence_without_auditory_model(self):
        analysis_bytes = json.dumps(self.breakdown).encode()
        audio = self.audio_analysis(analysis_bytes)
        audio["auditory_review"] = {
            "status": "unavailable",
            "method": None,
            "evidence_ref": None,
        }
        audio["soundscape"] = {
            "music": None,
            "speech": None,
            "effects": [],
            "ambience": None,
            "dynamic_arc": "Audio exists, but no auditory review was available.",
        }
        audio["events"] = [
            {
                "start_s": 0.8,
                "end_s": 1.2,
                "kind": "silence",
                "description": "Below the recorded -40 dB threshold.",
                "evidence": "measurement",
                "confidence": "high",
                "synced_shots": [1, 2],
            }
        ]
        audio["reproduction"] = {
            "locked_audio_grammar": [],
            "replaceable_audio": [],
            "sync_rules": [],
        }
        self.assertEqual(
            validation.validate_audio_analysis(
                audio,
                self.breakdown,
                breakdown_sha256=hashlib.sha256(analysis_bytes).hexdigest(),
                source_pin_sha256="a" * 64,
            ),
            [],
        )

    def test_audio_analysis_distinguishes_absent_stream_from_unknown_sound(self):
        analysis_bytes = json.dumps(self.breakdown).encode()
        audio = self.audio_analysis(analysis_bytes)
        audio["audio_stream"] = {
            "status": "absent",
            "duration_s": None,
            "channels": None,
            "sample_rate_hz": None,
        }
        audio["auditory_review"] = {
            "status": "not_needed",
            "method": None,
            "evidence_ref": None,
        }
        audio["soundscape"] = {
            "music": None,
            "speech": None,
            "effects": [],
            "ambience": None,
            "dynamic_arc": "No audio stream is present.",
        }
        audio["events"] = []
        self.assertEqual(
            validation.validate_audio_analysis(
                audio,
                self.breakdown,
                breakdown_sha256=hashlib.sha256(analysis_bytes).hexdigest(),
                source_pin_sha256="a" * 64,
            ),
            [],
        )

    def test_uncertain_and_comparison_evidence_is_required(self):
        analysis_bytes = json.dumps(self.breakdown).encode()
        motion = self.motion_review(analysis_bytes)
        motion["shots"][0]["confidence"] = "low"
        self.assertIn(
            "motion.schema",
            self.rule_ids(
                validation.validate_motion_review(
                    motion,
                    self.breakdown,
                    breakdown_sha256=hashlib.sha256(analysis_bytes).hexdigest(),
                )
            ),
        )
        comparison = self.motion_review(analysis_bytes, mode="comparison")
        comparison["shots"][0].pop("concrete_fix_prompt_text")
        self.assertIn(
            "motion.schema",
            self.rule_ids(
                validation.validate_motion_review(
                    comparison,
                    self.breakdown,
                    breakdown_sha256=hashlib.sha256(analysis_bytes).hexdigest(),
                )
            ),
        )

    def test_schemas_are_valid_and_example_template_conforms(self):
        references = VALIDATOR_PATH.parents[1] / "references"
        for name in (
            "breakdown-schema.json",
            "motion-review-schema.json",
            "audio-analysis-schema.json",
            "template-schema.json",
        ):
            Draft202012Validator.check_schema(
                json.loads((references / name).read_text())
            )
        schema = json.loads((references / "template-schema.json").read_text())
        template = json.loads(
            (references / "templates/psychedelic-neon-cosmic/template.json").read_text()
        )
        self.assertEqual(list(Draft202012Validator(schema).iter_errors(template)), [])

    def test_cli_returns_parseable_json_and_meaningful_exit_status(self):
        with tempfile.TemporaryDirectory() as directory:
            analysis = Path(directory) / "analysis.json"
            analysis.write_text(json.dumps(self.breakdown))
            audio = Path(directory) / "audio-analysis.json"
            audio.write_text(json.dumps(self.audio_analysis(analysis.read_bytes())))
            valid = subprocess.run(
                [
                    sys.executable,
                    str(VALIDATOR_PATH),
                    str(analysis),
                    "--source-duration-s",
                    "2",
                    "--audio-analysis",
                    str(audio),
                    "--source-pin-sha256",
                    "a" * 64,
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(valid.returncode, 0)
            self.assertTrue(json.loads(valid.stdout)["ok"])
            self.breakdown["shots"][0]["duration_s"] = 8.0
            analysis.write_text(json.dumps(self.breakdown))
            invalid = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), str(analysis)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(invalid.returncode, 1)
            self.assertFalse(json.loads(invalid.stdout)["ok"])


if __name__ == "__main__":
    unittest.main()
