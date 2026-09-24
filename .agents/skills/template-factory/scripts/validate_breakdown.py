from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCE_ROOT = SKILL_ROOT / "references"


@dataclass(frozen=True)
class Finding:
    rule_id: str
    path: str
    message: str
    severity: str = "error"


def finite_number(value: Any) -> float | None:
    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not math.isfinite(value)
    ):
        return None
    return float(value)


def schema_findings(value: Any, schema_name: str, rule_id: str) -> list[Finding]:
    schema = json.loads((REFERENCE_ROOT / schema_name).read_text())
    Draft202012Validator.check_schema(schema)
    return [
        Finding(rule_id, ".".join(map(str, error.path)), error.message)
        for error in Draft202012Validator(schema).iter_errors(value)
    ]


def validate_breakdown(
    value: Any,
    *,
    source_duration_s: float | None = None,
    tolerance_s: float = 0.05,
) -> list[Finding]:
    findings = schema_findings(value, "breakdown-schema.json", "breakdown.schema")
    if not isinstance(value, dict) or not isinstance(value.get("shots"), list):
        return findings
    shots = value["shots"]
    indexes = [shot.get("index") for shot in shots if isinstance(shot, dict)]
    integer_indexes = [
        index
        for index in indexes
        if isinstance(index, int) and not isinstance(index, bool)
    ]
    if len(integer_indexes) != len(set(integer_indexes)):
        findings.append(
            Finding("breakdown.timeline", "shots", "Shot indices must be unique")
        )
    if indexes != list(range(1, len(shots) + 1)):
        findings.append(
            Finding(
                "breakdown.timeline",
                "shots",
                "Shots must be ordered and numbered consecutively from 1",
            )
        )
    previous_end: float | None = None
    valid_indexes = set(integer_indexes)
    if source_duration_s is not None and (
        not math.isfinite(source_duration_s) or source_duration_s <= 0
    ):
        findings.append(
            Finding(
                "breakdown.timeline",
                "source_duration_s",
                "Source duration must be finite and greater than zero",
            )
        )
        source_duration_s = None
    for position, shot in enumerate(shots):
        if not isinstance(shot, dict):
            continue
        path = f"shots.{position}"
        motion = shot.get("motion")
        if isinstance(motion, dict) and isinstance(
            motion.get("moving_elements"), list
        ):
            names = [
                element.get("name")
                for element in motion["moving_elements"]
                if isinstance(element, dict)
            ]
            string_names = [name for name in names if isinstance(name, str)]
            if len(string_names) != len(set(string_names)):
                findings.append(
                    Finding(
                        "breakdown.motion_elements",
                        f"{path}.motion.moving_elements",
                        "Moving element names must be unique within a beat",
                    )
                )
        start = finite_number(shot.get("start_s"))
        end = finite_number(shot.get("end_s"))
        duration = finite_number(shot.get("duration_s"))
        if start is None or end is None or duration is None:
            findings.append(
                Finding("breakdown.timeline", path, "Shot times must be finite numbers")
            )
            continue
        if position == 0 and abs(start) > tolerance_s:
            findings.append(
                Finding(
                    "breakdown.timeline",
                    f"{path}.start_s",
                    "The first shot must start at 0",
                )
            )
        if end <= start:
            findings.append(
                Finding("breakdown.timeline", path, "Shot end must be after its start")
            )
        if abs((end - start) - duration) > tolerance_s:
            findings.append(
                Finding(
                    "breakdown.timeline",
                    f"{path}.duration_s",
                    "Duration must equal end_s minus start_s",
                )
            )
        if previous_end is not None and abs(start - previous_end) > tolerance_s:
            relation = "overlaps" if start < previous_end else "leaves a gap after"
            findings.append(
                Finding(
                    "breakdown.timeline",
                    f"{path}.start_s",
                    f"Shot {relation} the previous shot",
                )
            )
        if source_duration_s is not None and end > source_duration_s + tolerance_s:
            findings.append(
                Finding(
                    "breakdown.timeline",
                    f"{path}.end_s",
                    "Shot exceeds the measured source duration",
                )
            )
        previous_end = end
    if (
        source_duration_s is not None
        and previous_end is not None
        and abs(previous_end - source_duration_s) > tolerance_s
    ):
        findings.append(
            Finding(
                "breakdown.timeline",
                "shots",
                "The final shot must end at the measured source duration",
            )
        )
    elements = value.get("elements")
    if not isinstance(elements, list):
        return findings
    element_ids: list[Any] = []
    element_tags: list[Any] = []
    for position, element in enumerate(elements):
        if not isinstance(element, dict):
            continue
        element_ids.append(element.get("id"))
        if "tag" in element:
            element_tags.append(element.get("tag"))
        in_shots = element.get("in_shots")
        keyframes = element.get("keyframe_index")
        if isinstance(in_shots, list) and any(
            not isinstance(index, int) or index not in valid_indexes
            for index in in_shots
        ):
            findings.append(
                Finding(
                    "breakdown.element_references",
                    f"elements.{position}.in_shots",
                    "Element references an unknown shot",
                )
            )
        if isinstance(keyframes, list):
            if any(
                not isinstance(index, int) or index not in valid_indexes
                for index in keyframes
            ):
                findings.append(
                    Finding(
                        "breakdown.element_references",
                        f"elements.{position}.keyframe_index",
                        "Keyframe references an unknown shot",
                    )
                )
            valid_keyframes = {index for index in keyframes if isinstance(index, int)}
            valid_in_shots = (
                {index for index in in_shots if isinstance(index, int)}
                if isinstance(in_shots, list)
                else set()
            )
            if isinstance(in_shots, list) and not valid_keyframes.issubset(
                valid_in_shots
            ):
                findings.append(
                    Finding(
                        "breakdown.element_references",
                        f"elements.{position}.keyframe_index",
                        "Keyframes must be a subset of in_shots",
                    )
                )
    string_ids = [value for value in element_ids if isinstance(value, str)]
    if len(string_ids) != len(set(string_ids)):
        findings.append(
            Finding(
                "breakdown.element_references", "elements", "Element IDs must be unique"
            )
        )
    string_tags = [value for value in element_tags if isinstance(value, str)]
    if len(string_tags) != len(set(string_tags)):
        findings.append(
            Finding(
                "breakdown.element_references",
                "elements",
                "Element tags must be unique",
            )
        )
    return findings


def validate_motion_review(
    value: Any,
    breakdown: Any,
    *,
    breakdown_sha256: str,
    tolerance_s: float = 0.05,
) -> list[Finding]:
    findings = schema_findings(value, "motion-review-schema.json", "motion.schema")
    if not isinstance(value, dict):
        return findings
    if value.get("source_breakdown_sha256") != breakdown_sha256:
        findings.append(
            Finding(
                "motion.source_current",
                "source_breakdown_sha256",
                "Motion review does not match the approved breakdown bytes",
            )
        )
    if (
        not isinstance(breakdown, dict)
        or not isinstance(breakdown.get("shots"), list)
        or not isinstance(value.get("shots"), list)
    ):
        return findings
    breakdown_by_index = {
        shot.get("index"): shot
        for shot in breakdown["shots"]
        if isinstance(shot, dict) and isinstance(shot.get("index"), int)
    }
    reviews = value["shots"]
    review_indexes = [
        review.get("shot_index") for review in reviews if isinstance(review, dict)
    ]
    integer_review_indexes = [
        index
        for index in review_indexes
        if isinstance(index, int) and not isinstance(index, bool)
    ]
    if len(integer_review_indexes) != len(set(integer_review_indexes)) or set(
        integer_review_indexes
    ) != set(breakdown_by_index):
        findings.append(
            Finding(
                "motion.shot_alignment",
                "shots",
                "Motion review must contain each breakdown shot exactly once",
            )
        )
    for position, review in enumerate(reviews):
        if not isinstance(review, dict):
            continue
        shot_index = review.get("shot_index")
        source = (
            breakdown_by_index.get(shot_index)
            if isinstance(shot_index, int) and not isinstance(shot_index, bool)
            else None
        )
        if not isinstance(source, dict):
            continue
        for field in ("start_s", "end_s"):
            observed = finite_number(review.get(field))
            expected = finite_number(source.get(field))
            if (
                observed is not None
                and expected is not None
                and abs(observed - expected) > tolerance_s
            ):
                findings.append(
                    Finding(
                        "motion.shot_alignment",
                        f"shots.{position}.{field}",
                        "Motion boundary differs from the approved breakdown",
                    )
                )
        motion = review.get("motion")
        if isinstance(motion, dict) and isinstance(motion.get("moving_elements"), list):
            names = [
                item.get("name")
                for item in motion["moving_elements"]
                if isinstance(item, dict)
            ]
            string_names = [name for name in names if isinstance(name, str)]
            if len(string_names) != len(set(string_names)):
                findings.append(
                    Finding(
                        "motion.evidence_complete",
                        f"shots.{position}.motion.moving_elements",
                        "Moving element names must be unique within a shot",
                    )
                )
    return findings


def validate_audio_analysis(
    value: Any,
    breakdown: Any,
    *,
    breakdown_sha256: str,
    source_pin_sha256: str,
    tolerance_s: float = 0.05,
) -> list[Finding]:
    findings = schema_findings(value, "audio-analysis-schema.json", "audio.schema")
    if not isinstance(value, dict):
        return findings
    if (
        value.get("source_pin_sha256") != source_pin_sha256
        or value.get("source_breakdown_sha256") != breakdown_sha256
    ):
        findings.append(
            Finding(
                "audio.source_current",
                "source_pin_sha256",
                "Audio analysis does not match the current pin and breakdown bytes",
            )
        )
    if not isinstance(breakdown, dict) or not isinstance(breakdown.get("shots"), list):
        return findings
    shots = {
        shot.get("index"): shot
        for shot in breakdown["shots"]
        if isinstance(shot, dict)
        and isinstance(shot.get("index"), int)
        and not isinstance(shot.get("index"), bool)
    }
    picture_duration = finite_number(value.get("picture_duration_s"))
    last_shot = breakdown["shots"][-1] if breakdown["shots"] else None
    expected_picture_duration = (
        finite_number(last_shot.get("end_s")) if isinstance(last_shot, dict) else None
    )
    if (
        picture_duration is not None
        and expected_picture_duration is not None
        and abs(picture_duration - expected_picture_duration) > tolerance_s
    ):
        findings.append(
            Finding(
                "audio.timeline",
                "picture_duration_s",
                "Picture duration differs from the breakdown",
            )
        )
    audio_stream = value.get("audio_stream")
    auditory_review = value.get("auditory_review")
    events = value.get("events")
    if not isinstance(audio_stream, dict) or not isinstance(events, list):
        return findings
    status = audio_stream.get("status")
    audio_duration = finite_number(audio_stream.get("duration_s"))
    review = auditory_review if isinstance(auditory_review, dict) else {}
    review_status = review.get("status")
    soundscape = value.get("soundscape")
    reproduction = value.get("reproduction")
    has_sound_labels = isinstance(soundscape, dict) and any(
        soundscape.get(field) for field in ("music", "speech", "effects", "ambience")
    )
    has_sound_events = any(
        isinstance(event, dict)
        and (event.get("kind") != "silence" or event.get("evidence") != "measurement")
        for event in events
    )
    has_audio_recipe = isinstance(reproduction, dict) and any(
        reproduction.get(field)
        for field in ("locked_audio_grammar", "replaceable_audio", "sync_rules")
    )
    if review_status == "completed":
        method = review.get("method")
        evidence_ref = review.get("evidence_ref")
        if (
            not isinstance(method, str)
            or method not in {"ark_mcp_seed_audio_understand", "human_review"}
            or not isinstance(evidence_ref, str)
            or not evidence_ref.strip()
        ):
            findings.append(
                Finding(
                    "audio.auditory_evidence",
                    "auditory_review",
                    "Completed auditory review needs a method and evidence reference",
                )
            )
    elif any(
        review.get(field) is not None for field in ("method", "evidence_ref")
    ):
        findings.append(
            Finding(
                "audio.auditory_evidence",
                "auditory_review",
                "Unavailable or unneeded review cannot claim a method or evidence reference",
            )
        )
    if (
        status == "present"
        and review_status != "completed"
        and (has_sound_labels or has_sound_events or has_audio_recipe)
    ):
        findings.append(
            Finding(
                "audio.auditory_evidence",
                "auditory_review",
                "Sound labels and reusable audio grammar need completed auditory review",
            )
        )
    if status == "present" and (
        not isinstance(review_status, str)
        or review_status not in {"completed", "unavailable"}
    ):
        findings.append(
            Finding(
                "audio.auditory_evidence",
                "auditory_review.status",
                "Present audio requires completed or unavailable auditory review",
            )
        )
    expected_review_status = {"absent": "not_needed", "unavailable": "unavailable"}
    if (
        isinstance(status, str)
        and status in expected_review_status
        and review_status != expected_review_status[status]
    ):
        findings.append(
            Finding(
                "audio.auditory_evidence",
                "auditory_review.status",
                "Auditory review status does not match audio availability",
            )
        )
    if status == "present" and (audio_duration is None or audio_duration <= 0):
        findings.append(
            Finding(
                "audio.availability",
                "audio_stream.duration_s",
                "A present audio stream needs a measured positive duration",
            )
        )
    if isinstance(status, str) and status in {"absent", "unavailable"}:
        if events:
            findings.append(
                Finding(
                    "audio.availability",
                    "events",
                    "Audio events require an available audio stream",
                )
            )
        if any(
            audio_stream.get(field) is not None
            for field in ("duration_s", "channels", "sample_rate_hz")
        ):
            findings.append(
                Finding(
                    "audio.availability",
                    "audio_stream",
                    "Unavailable or absent audio cannot have measured stream properties",
                )
            )
        if isinstance(soundscape, dict) and any(
            soundscape.get(field)
            for field in ("music", "speech", "effects", "ambience")
        ):
            findings.append(
                Finding(
                    "audio.availability",
                    "soundscape",
                    "Absent or unavailable audio cannot have identified sound content",
                )
            )
    for position, event in enumerate(events):
        if not isinstance(event, dict):
            continue
        path = f"events.{position}"
        start = finite_number(event.get("start_s"))
        end = finite_number(event.get("end_s"))
        if start is None or end is None or start < 0 or end <= start:
            findings.append(
                Finding(
                    "audio.timeline",
                    path,
                    "Event must have a finite, positive interval",
                )
            )
            continue
        if audio_duration is not None and end > audio_duration + tolerance_s:
            findings.append(
                Finding(
                    "audio.timeline", f"{path}.end_s", "Event exceeds audio duration"
                )
            )
        if event.get("evidence") == "measurement" and event.get("kind") != "silence":
            findings.append(
                Finding(
                    "audio.evidence",
                    f"{path}.evidence",
                    "Measurements alone cannot identify music, voice, effects, or ambience",
                )
            )
        if event.get("evidence") == "asr" and event.get("kind") != "speech":
            findings.append(
                Finding(
                    "audio.evidence",
                    f"{path}.evidence",
                    "ASR can only support a speech event",
                )
            )
        synced_shots = event.get("synced_shots")
        if not isinstance(synced_shots, list):
            continue
        for shot_index in synced_shots:
            shot = (
                shots.get(shot_index)
                if isinstance(shot_index, int) and not isinstance(shot_index, bool)
                else None
            )
            shot_start = (
                finite_number(shot.get("start_s")) if isinstance(shot, dict) else None
            )
            shot_end = (
                finite_number(shot.get("end_s")) if isinstance(shot, dict) else None
            )
            if (
                shot_start is None
                or shot_end is None
                or start > shot_end + tolerance_s
                or end < shot_start - tolerance_s
            ):
                findings.append(
                    Finding(
                        "audio.beat_alignment",
                        f"{path}.synced_shots",
                        "Referenced visual beat must exist and overlap the audio event",
                    )
                )
    return findings


def validate_files(
    analysis_path: Path,
    motion_path: Path | None = None,
    source_duration_s: float | None = None,
    audio_path: Path | None = None,
    source_pin_sha256: str | None = None,
) -> list[Finding]:
    try:
        analysis_bytes = analysis_path.read_bytes()
        breakdown = json.loads(analysis_bytes)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, SchemaError) as error:
        return [Finding("breakdown.schema", str(analysis_path), str(error))]
    findings = validate_breakdown(breakdown, source_duration_s=source_duration_s)
    if motion_path is not None:
        try:
            motion = json.loads(motion_path.read_text())
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            return findings + [Finding("motion.schema", str(motion_path), str(error))]
        findings.extend(
            validate_motion_review(
                motion,
                breakdown,
                breakdown_sha256=hashlib.sha256(analysis_bytes).hexdigest(),
            )
        )
    if audio_path is not None:
        try:
            audio_analysis = json.loads(audio_path.read_text())
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            return findings + [Finding("audio.schema", str(audio_path), str(error))]
        if source_pin_sha256 is None:
            findings.append(
                Finding(
                    "audio.source_current",
                    "source_pin_sha256",
                    "Provide the current pin SHA-256",
                )
            )
        else:
            findings.extend(
                validate_audio_analysis(
                    audio_analysis,
                    breakdown,
                    breakdown_sha256=hashlib.sha256(analysis_bytes).hexdigest(),
                    source_pin_sha256=source_pin_sha256,
                )
            )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a template-factory breakdown and optional generated-take "
            "motion comparison"
        )
    )
    parser.add_argument("analysis", type=Path)
    parser.add_argument(
        "--motion-review",
        type=Path,
        help="optional hash-bound motion comparison against a generated take",
    )
    parser.add_argument("--audio-analysis", type=Path)
    parser.add_argument("--source-pin-sha256")
    parser.add_argument(
        "--source-duration-s",
        type=float,
        help="Picture (video-stream) duration in seconds; container duration often includes audio padding",
    )
    args = parser.parse_args()
    findings = validate_files(
        args.analysis,
        args.motion_review,
        args.source_duration_s,
        args.audio_analysis,
        args.source_pin_sha256,
    )
    print(
        json.dumps(
            {"ok": not findings, "findings": [asdict(finding) for finding in findings]},
            indent=2,
        )
    )
    return int(bool(findings))


if __name__ == "__main__":
    raise SystemExit(main())
