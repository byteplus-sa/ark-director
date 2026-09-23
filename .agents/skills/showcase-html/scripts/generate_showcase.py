"""Generate a self-contained showcase index.html from template.html + showcase.json.

Usage:
  python3 scripts/generate_showcase.py <project_dir> --init
  python3 scripts/generate_showcase.py <project_dir> --stage <stage-id> [--out index.html]
  python3 scripts/generate_showcase.py <project_dir> --check --stage <stage-id>
  python3 scripts/generate_showcase.py <project_dir> --serve --stage <stage-id> [--port 8000]

Reads <project_dir>/showcase.json (relative asset paths are resolved against
<project_dir>) and writes the final HTML next to it. The HTML embeds the data
JSON and the renderer, so it is a single portable file.

Modes:
  --init     create an eight-stage production canvas without overwriting one.
  (default)  generate index.html in place (read-only review page).
  --check    validate paths; with --stage, verify the generated canvas is current.
  --serve    generate, then run a local HTTP server so in-browser variant
             selection can persist to the project (writes selection.json, the
             element/shot manifests, and a timestamped selection.log). Opens the
             URL in the default browser.

Selection contract (see references/schema.md):
  A card is selectable when it carries ``id`` and ``manifest``. Selecting it in
  the page (server mode only) sets that asset's ``selected_variant`` (scalar)
  or, when the card also carries ``field: "selected_variants"`` and ``key``, a
  single key inside a ``selected_variants`` map in the manifest frontmatter.
"""
import argparse
import copy
import datetime
import hashlib
import html
import json
import os
import re
import secrets
import subprocess
import sys
import threading
import webbrowser
from collections.abc import Mapping
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, ClassVar

from selection_service import (
    SelectionConflict,
    SelectionError,
    SelectionService,
    atomic_write,
    collect_selectable,
    contained_path,
    parse_frontmatter,
    read_project_mode,
    read_selection,
    record_stage_decision,
    set_project_mode,
    stage_revision,
    validate_schema,
    validate_stage_media,
    validated_review,
)

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "template.html")
RENDERER = os.path.join(HERE, "..", "renderer.js")
CANVAS_TEMPLATE = os.path.join(HERE, "..", "assets", "production-canvas.json")

CANVAS_STAGE_IDS = (
    "brief-development",
    "scene-breakdown",
    "canon-elements",
    "storyboard-visual-plan",
    "audio-preparation",
    "shot-generation",
    "assembly-review",
    "delivery",
)
CANVAS_STATUSES = {
    "pending",
    "active",
    "review",
    "approved",
    "complete",
    "blocked",
    "skipped",
}
CANVAS_TERMINAL_STATUSES = {"approved", "complete", "skipped"}
CANVAS_TEXT_KINDS = {"brief", "data", "document", "manifest", "prompt", "review"}
CANVAS_TEXT_EXTENSIONS = {".json", ".md", ".txt", ".yaml", ".yml"}
CANVAS_EMBED_LIMIT = 512 * 1024


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_json_argument(value, label):
    raw = value.strip()
    try:
        return json.loads(raw) if raw.startswith("{") else load_json(raw)
    except (json.JSONDecodeError, OSError) as error:
        raise SelectionError(f"invalid JSON for {label}: {error}") from error


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inferred_source_kind(path):
    suffix = path.suffix.lower()
    if suffix in _VIDEO_EXTS:
        return "video"
    if suffix in _IMAGE_EXTS:
        return "image"
    if suffix in _AUDIO_EXTS:
        return "audio"
    if suffix == ".md" and path.name.startswith("prompt_"):
        return "prompt"
    if suffix == ".json":
        return "data"
    if suffix in {".md", ".txt", ".yaml", ".yml"}:
        return "document"
    return "other"


def inspect_paths(value):
    paths = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"src", "contactSheet", "promptFile", "reviewPath", "manifest", "path"} and isinstance(item, str):
                paths.append(item)
            elif isinstance(item, (dict, list)):
                paths.extend(inspect_paths(item))
    elif isinstance(value, list):
        for item in value:
            paths.extend(inspect_paths(item))
    return paths


def section_contract_errors(value, section_id):
    errors = []
    if isinstance(value, dict):
        if isinstance(value.get("prompt"), str) and value["prompt"] and not value.get("promptFile"):
            errors.append(
                f"Section {section_id}: inline production prompts require promptFile"
            )
        refs = value.get("refs")
        if isinstance(refs, list):
            for reference in refs:
                if not isinstance(reference, dict) or not isinstance(reference.get("path"), str):
                    errors.append(
                        f"Section {section_id}: every element reference requires a project-relative path"
                    )
        for item in value.values():
            if isinstance(item, (dict, list)):
                errors.extend(section_contract_errors(item, section_id))
    elif isinstance(value, list):
        for item in value:
            errors.extend(section_contract_errors(item, section_id))
    return errors


def hydrate_prompt_files(value, proj):
    if isinstance(value, dict):
        prompt_file = value.get("promptFile")
        if isinstance(prompt_file, str):
            path = contained_path(proj, prompt_file)
            if path.stat().st_size > CANVAS_EMBED_LIMIT:
                raise SelectionError(f"Prompt file is too large to embed: {prompt_file}")
            prompt = path.read_text(encoding="utf-8")
            authored = value.get("prompt")
            if isinstance(authored, str) and authored and authored != prompt:
                raise SelectionError(f"Inline prompt differs from promptFile: {prompt_file}")
            value["prompt"] = prompt
        for item in value.values():
            if isinstance(item, (dict, list)):
                hydrate_prompt_files(item, proj)
    elif isinstance(value, list):
        for item in value:
            hydrate_prompt_files(item, proj)


def canvas_selection_errors(data, proj, stages):
    errors = []
    try:
        registry = collect_selectable(data)
        selections = read_selection(registry, proj)
    except (SelectionError, TypeError, AttributeError) as error:
        return [str(error)]
    by_stage = {stage["id"]: stage for stage in stages}
    for asset_id, meta in registry.items():
        stage = by_stage.get(meta.get("stage"))
        if stage is None:
            errors.append(f"{asset_id}: selectable asset requires a canvas stage")
            continue
        if stage.get("status") not in {"approved", "complete"}:
            continue
        filename = selections.get(asset_id)
        source = meta["variants"].get(filename)
        if source is None:
            errors.append(f"{asset_id}: completed stage requires a registered selected variant")
            continue
        try:
            media_hash = file_sha256(contained_path(proj, source))
            manifest = contained_path(proj, meta["manifest"])
            _, document, _ = parse_frontmatter(manifest.read_text(encoding="utf-8"))
        except (SelectionError, OSError, UnicodeError) as error:
            errors.append(f"{asset_id}: {error}")
            continue
        evidence = document.get("selection_evidence")
        if meta["field"] == "selected_variants" and isinstance(evidence, Mapping):
            evidence = evidence.get(meta["key"])
        if not isinstance(evidence, Mapping) or evidence.get("result") != "approved":
            errors.append(f"{asset_id}: completed stage requires approved selection evidence")
            continue
        if evidence.get("selected_sha256") != media_hash:
            errors.append(f"{asset_id}: selected media hash is stale")
        decision_id = evidence.get("decision_id")
        decision_path = evidence.get("decision_path")
        review_path = evidence.get("review_path")
        if not isinstance(decision_id, str) or decision_path != f"decisions/{decision_id}.json":
            errors.append(f"{asset_id}: selection decision path is invalid")
            continue
        sources = stage.get("sources", [])
        source_paths = {item.get("path") for item in sources if isinstance(item, dict)} if isinstance(sources, list) else set()
        for relative in (source, decision_path, review_path):
            if relative not in source_paths:
                errors.append(f"{asset_id}: {relative} must be a stage source")
        try:
            decision_file = contained_path(proj, decision_path)
            decision = load_json(decision_file)
            if evidence.get("decision_sha256") != file_sha256(decision_file):
                errors.append(f"{asset_id}: selection decision hash is stale")
            validated_review(proj, review_path, evidence.get("review_sha256"), source, media_hash)
            validate_schema(decision, "production-decision.schema.json")
        except (SelectionError, OSError, json.JSONDecodeError) as error:
            errors.append(f"{asset_id}: approval evidence is unavailable: {error}")
            continue
        expected = {
            "decision_id": decision_id,
            "decision_type": "variant_selection",
            "asset_id": asset_id,
            "subject_path": source,
            "selected_variant": filename,
            "selected_sha256": media_hash,
            "result": "approved",
            "review_path": review_path,
            "review_sha256": evidence.get("review_sha256"),
            "actor": evidence.get("actor"),
            "approval_mode": evidence.get("approval_mode"),
            "reason": evidence.get("reason"),
        }
        if not isinstance(decision, dict) or any(decision.get(key) != value for key, value in expected.items()):
            errors.append(f"{asset_id}: selection decision does not match the manifest")
            continue
        if decision["actor"] == "user" and decision["authorization"]["source"] != "local_ui":
            errors.append(f"{asset_id}: user decision requires local UI authorization")
        upstream = decision.get("upstream_sha256", {})
        if not isinstance(upstream, dict):
            errors.append(f"{asset_id}: selection decision upstream hashes are invalid")
            continue
        for relative, expected_hash in upstream.items():
            try:
                if file_sha256(contained_path(proj, relative)) != expected_hash:
                    errors.append(f"{asset_id}: upstream source hash is stale: {relative}")
            except SelectionError as error:
                errors.append(f"{asset_id}: {error}")
    return errors


def canvas_validation_errors(data, proj, expected_stage=None):
    canvas = data.get("canvas") if isinstance(data, dict) else None
    if not isinstance(canvas, dict):
        return ["Lifecycle review requires a top-level canvas object"]
    if canvas.get("approvalContractVersion") not in (None, 1):
        return ["Unsupported canvas approvalContractVersion"]
    current_stage = canvas.get("currentStage")
    if current_stage not in CANVAS_STAGE_IDS:
        return [f"canvas.currentStage must be one of: {', '.join(CANVAS_STAGE_IDS)}"]
    errors = []
    if expected_stage and current_stage != expected_stage:
        errors.append(
            f"Canvas stage mismatch: expected {expected_stage}, found {current_stage}"
        )
    stages = canvas.get("stages")
    if not isinstance(stages, list):
        return errors + ["canvas.stages must be an array"]
    stage_ids = [stage.get("id") for stage in stages if isinstance(stage, dict)]
    if stage_ids != list(CANVAS_STAGE_IDS):
        errors.append("canvas.stages must contain all eight production stages in order")
        return errors
    current_index = CANVAS_STAGE_IDS.index(current_stage)
    sections = data.get("sections")
    if not isinstance(sections, list):
        errors.append("showcase.json requires a sections array")
        sections = []
    sections_by_stage = {stage_id: [] for stage_id in CANVAS_STAGE_IDS}
    section_ids = set()
    for section in sections:
        if not isinstance(section, dict):
            errors.append("Every canvas section must be an object")
            continue
        section_id = section.get("id")
        if not isinstance(section_id, str) or not section_id:
            errors.append("Every canvas section requires a nonempty id")
        elif section_id in section_ids:
            errors.append(f"Duplicate canvas section id: {section_id}")
        else:
            section_ids.add(section_id)
        stage_id = section.get("stage")
        if stage_id not in CANVAS_STAGE_IDS:
            errors.append(f"Section {section_id or '<unknown>'} requires a valid stage")
        else:
            sections_by_stage[stage_id].append(section)
            errors.extend(section_contract_errors(section, section_id or "<unknown>"))
    for index, stage in enumerate(stages):
        status = stage.get("status")
        if status not in CANVAS_STATUSES:
            errors.append(f"{stage['id']}: invalid canvas stage status: {status}")
            continue
        if index < current_index and status not in CANVAS_TERMINAL_STATUSES:
            errors.append(f"{stage['id']}: earlier stages must be approved, complete, or skipped")
        if index == current_index and status == "pending":
            errors.append(f"{stage['id']}: current stage cannot be pending")
        if index > current_index and status not in {"pending", "skipped"}:
            errors.append(f"{stage['id']}: future stages must be pending or skipped")
        if canvas.get("approvalContractVersion") == 1 and status in {"approved", "complete"}:
            required_locks = []
            if stage["id"] == "assembly-review":
                required_locks.append("picture")
                if stages[CANVAS_STAGE_IDS.index("audio-preparation")].get("status") != "skipped":
                    required_locks.append("audio")
            if stage["id"] == "delivery":
                required_locks.append("final_master")
            locks = stage.get("locks", {})
            if not isinstance(locks, dict):
                errors.append(f"{stage['id']}: locks must be an object")
                locks = {}
            for lock_kind in required_locks:
                if lock_kind not in locks:
                    errors.append(f"{stage['id']}: {lock_kind} lock is required before stage exit")
        sources = stage.get("sources", [])
        if not isinstance(sources, list):
            errors.append(f"{stage['id']}: sources must be an array")
            continue
        if status not in {"pending", "skipped"} and not sources and not sections_by_stage[stage["id"]]:
            errors.append(f"{stage['id']}: progressed stage requires a source or section")
        if canvas.get("approvalContractVersion") == 1:
            candidates = stage.get("lockCandidates", [])
            if not isinstance(candidates, list):
                errors.append(f"{stage['id']}: lockCandidates must be an array")
            else:
                candidate_keys = set()
                for candidate in candidates:
                    if not isinstance(candidate, dict):
                        errors.append(f"{stage['id']}: every lock candidate must be an object")
                        continue
                    lock_kind = candidate.get("lock_kind")
                    artifact_path = candidate.get("artifact_path")
                    review_path = candidate.get("review_path")
                    lock_stages = {"picture": "assembly-review", "audio": "assembly-review", "final_master": "delivery"}
                    if not isinstance(lock_kind, str) or lock_stages.get(lock_kind) != stage["id"]:
                        errors.append(f"{stage['id']}: lock candidate has an invalid lock_kind")
                    if not isinstance(candidate.get("reason"), str) or not candidate["reason"].strip():
                        errors.append(f"{stage['id']}: lock candidate requires a reason")
                    upstream = candidate.get("upstream_sha256")
                    if not isinstance(upstream, dict) or any(not isinstance(path, str) or not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None for path, digest in upstream.items()):
                        errors.append(f"{stage['id']}: lock candidate requires upstream_sha256")
                    else:
                        for relative, digest in upstream.items():
                            try:
                                if file_sha256(contained_path(proj, relative)) != digest:
                                    errors.append(f"{stage['id']}: lock candidate upstream source hash is stale: {relative}")
                            except SelectionError as error:
                                errors.append(f"{stage['id']}: invalid lock candidate: {error}")
                    try:
                        artifact = contained_path(proj, artifact_path)
                        review_file = contained_path(proj, review_path)
                        review = validated_review(proj, review_path, file_sha256(review_file), artifact_path, file_sha256(artifact))
                        if isinstance(lock_kind, str) and lock_stages.get(lock_kind) == stage["id"]:
                            audio_required = lock_kind == "final_master" and stages[CANVAS_STAGE_IDS.index("audio-preparation")].get("status") != "skipped"
                            validate_stage_media(proj, lock_kind, artifact_path, review, audio_required=audio_required)
                    except (SelectionError, TypeError) as error:
                        errors.append(f"{stage['id']}: invalid lock candidate: {error}")
                    if isinstance(lock_kind, str) and isinstance(artifact_path, str):
                        key = (lock_kind, artifact_path)
                        if key in candidate_keys:
                            errors.append(f"{stage['id']}: duplicate lock candidate")
                        candidate_keys.add(key)
        for source in sources:
            if not isinstance(source, dict):
                errors.append(f"{stage['id']}: every source must be an object")
                continue
            relative = source.get("path")
            try:
                path = contained_path(proj, relative)
            except SelectionError as error:
                errors.append(str(error))
                continue
            kind = source.get("kind", inferred_source_kind(path))
            if not isinstance(kind, str) or not kind:
                errors.append(f"{stage['id']}: source kind must be a nonempty string")
            if kind in CANVAS_TEXT_KINDS and path.stat().st_size > CANVAS_EMBED_LIMIT:
                errors.append(f"Canvas text source is too large to embed: {relative}")
        if canvas.get("approvalContractVersion") == 1:
            locks = stage.get("locks") or {}
            if not isinstance(locks, dict):
                errors.append(f"{stage['id']}: locks must be an object")
                continue
            for lock_kind, lock in locks.items():
                if not isinstance(lock, dict):
                    errors.append(f"{stage['id']}: {lock_kind} lock must be an object")
                    continue
                if lock.get("result") != "approved":
                    errors.append(f"{stage['id']}: {lock_kind} lock is not approved")
                for path_key, hash_key in (("artifact_path", "artifact_sha256"), ("review_path", "review_sha256")):
                    relative = lock.get(path_key)
                    try:
                        path = contained_path(proj, relative)
                    except SelectionError as error:
                        errors.append(f"{stage['id']}: {lock_kind} {error}")
                        continue
                    if lock.get(hash_key) != file_sha256(path):
                        errors.append(f"{stage['id']}: {lock_kind} {path_key} hash is stale")
                    if relative not in [source.get("path") for source in sources if isinstance(source, dict)]:
                        errors.append(f"{stage['id']}: {lock_kind} {path_key} must be a stage source")
                decision_id = lock.get("decision_id")
                if not isinstance(decision_id, str) or not decision_id:
                    errors.append(f"{stage['id']}: {lock_kind} requires a decision_id")
                    continue
                decision_relative = f"decisions/{decision_id}.json"
                if decision_relative not in [source.get("path") for source in sources if isinstance(source, dict)]:
                    errors.append(f"{stage['id']}: {lock_kind} decision must be a stage source")
                try:
                    decision_path = contained_path(proj, decision_relative)
                    decision = load_json(decision_path)
                    validate_schema(decision, "production-decision.schema.json")
                except (SelectionError, OSError, json.JSONDecodeError) as error:
                    errors.append(f"{stage['id']}: {lock_kind} decision is unavailable: {error}")
                    continue
                if lock.get("decision_sha256") != file_sha256(decision_path):
                    errors.append(f"{stage['id']}: {lock_kind} decision hash is stale")
                expected_fields = {
                    "decision_id": decision_id,
                    "decision_type": "stage_lock",
                    "stage_id": stage["id"],
                    "lock_kind": lock_kind,
                    "result": lock.get("result"),
                    "actor": lock.get("actor"),
                    "subject_path": lock.get("artifact_path"),
                    "subject_sha256": lock.get("artifact_sha256"),
                    "review_path": lock.get("review_path"),
                    "review_sha256": lock.get("review_sha256"),
                    "reason": lock.get("reason"),
                }
                if not isinstance(decision, dict) or any(decision.get(key) != value for key, value in expected_fields.items()):
                    errors.append(f"{stage['id']}: {lock_kind} decision does not match the lock")
                    continue
                if decision["actor"] == "user" and decision["authorization"]["source"] != "local_ui":
                    errors.append(f"{stage['id']}: {lock_kind} user decision requires local UI authorization")
                try:
                    review = validated_review(proj, lock.get("review_path"), lock.get("review_sha256"), lock.get("artifact_path"), lock.get("artifact_sha256"))
                    audio_required = lock_kind == "final_master" and stages[CANVAS_STAGE_IDS.index("audio-preparation")].get("status") != "skipped"
                    validate_stage_media(proj, lock_kind, lock["artifact_path"], review, audio_required=audio_required)
                except SelectionError as error:
                    errors.append(f"{stage['id']}: {lock_kind} review is invalid: {error}")
                upstream = decision.get("upstream_sha256", {})
                if not isinstance(upstream, dict):
                    errors.append(f"{stage['id']}: {lock_kind} upstream hashes are invalid")
                    continue
                for relative, expected_hash in upstream.items():
                    try:
                        if file_sha256(contained_path(proj, relative)) != expected_hash:
                            errors.append(f"{stage['id']}: {lock_kind} upstream source hash is stale: {relative}")
                    except SelectionError as error:
                        errors.append(f"{stage['id']}: {lock_kind} {error}")
    if canvas.get("approvalContractVersion") == 1:
        errors.extend(canvas_selection_errors(data, proj, stages))
    return errors


def prepare_canvas_data(data, proj, manifest_bytes=None, expected_stage=None):
    errors = canvas_validation_errors(data, proj, expected_stage)
    if errors:
        raise SelectionError("; ".join(errors))
    prepared = copy.deepcopy(data)
    prepared["approvalMode"] = read_project_mode(proj)
    hydrate_prompt_files(prepared.get("sections", []), proj)
    manifest_content = manifest_bytes
    if manifest_content is None:
        manifest_path = proj / "showcase.json"
        manifest_content = (
            manifest_path.read_bytes()
            if manifest_path.exists()
            else json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
        )
    source_records = {}
    for stage in prepared["canvas"]["stages"]:
        stage_sections = [
            section for section in prepared["sections"] if section.get("stage") == stage["id"]
        ]
        stage["sectionIds"] = [section["id"] for section in stage_sections]
        stage_paths = []
        for source in stage.get("sources", []):
            path = contained_path(proj, source["path"])
            kind = source.get("kind", inferred_source_kind(path))
            source["kind"] = kind
            source["sha256"] = file_sha256(path)
            source["bytes"] = path.stat().st_size
            if kind in CANVAS_TEXT_KINDS or path.suffix.lower() in CANVAS_TEXT_EXTENSIONS:
                source["content"] = path.read_text(encoding="utf-8")
            stage_paths.append(source["path"])
        for candidate in stage.get("lockCandidates", []):
            stage_paths.extend((candidate["artifact_path"], candidate["review_path"]))
            stage_paths.extend(candidate["upstream_sha256"])
        for section in stage_sections:
            stage_paths.extend(inspect_paths(section))
        unique_paths = list(dict.fromkeys(stage_paths))
        media_count = 0
        prompt_count = 0
        for relative in unique_paths:
            path = contained_path(proj, relative)
            kind = inferred_source_kind(path)
            if kind in {"image", "video", "audio"}:
                media_count += 1
            if kind == "prompt":
                prompt_count += 1
            source_records[relative] = {
                "path": relative,
                "kind": kind,
                "sha256": file_sha256(path),
                "bytes": path.stat().st_size,
            }
        stage["counts"] = {
            "sections": len(stage_sections),
            "sources": len(unique_paths),
            "media": media_count,
            "prompts": prompt_count,
        }
    build = {
        "currentStage": prepared["canvas"]["currentStage"],
        "manifestSha256": hashlib.sha256(manifest_content).hexdigest(),
        "projectSha256": prepared["approvalMode"]["project_sha256"],
        "templateSha256": file_sha256(Path(TEMPLATE)),
        "rendererSha256": file_sha256(Path(RENDERER)),
        "sources": [source_records[path] for path in sorted(source_records)],
    }
    snapshot_payload = json.dumps(build, sort_keys=True, separators=(",", ":")).encode("utf-8")
    build["snapshotSha256"] = hashlib.sha256(snapshot_payload).hexdigest()
    build["generatedAt"] = datetime.datetime.now(datetime.UTC).isoformat()
    prepared["canvasBuild"] = build
    return prepared


def embedded_showcase_data(path):
    text = path.read_text(encoding="utf-8")
    match = re.search(
        r'<script id="showcase-data" type="application/json">(.*?)</script>',
        text,
        re.DOTALL,
    )
    if not match:
        raise SelectionError(f"Generated HTML has no embedded showcase data: {path.name}")
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError as error:
        raise SelectionError(f"Generated HTML contains invalid showcase data: {path.name}") from error


def canvas_sync_errors(data, proj, out_path, expected_stage):
    errors = canvas_validation_errors(data, proj, expected_stage)
    if errors:
        return errors
    try:
        expected = prepare_canvas_data(data, proj, expected_stage=expected_stage)["canvasBuild"]
    except (OSError, UnicodeError, SelectionError) as error:
        return [str(error)]
    if not out_path.is_file():
        return [f"Missing generated production canvas: {out_path.name}"]
    try:
        actual = embedded_showcase_data(out_path).get("canvasBuild", {})
    except (OSError, UnicodeError, SelectionError) as error:
        return [str(error)]
    if actual.get("snapshotSha256") != expected["snapshotSha256"]:
        return [
            "Production canvas is stale; regenerate index.html after updating this stage"
        ]
    return []


# --------------------------------------------------------------------------- #
# audit logging (append-only, timestamped, JSON Lines)
# --------------------------------------------------------------------------- #

def log_file(proj):
    return contained_path(proj, "selection.log", must_exist=False)


def read_log(proj, limit=200):
    """Return the most recent `limit` log entries, newest last."""
    path = log_file(proj)
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines[-limit:]:
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


# --------------------------------------------------------------------------- #
# selection write-back
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# validation
# --------------------------------------------------------------------------- #

def validate(data, proj):
    errors = []
    def inspect(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key in ('src', 'contactSheet', 'promptFile', 'reviewPath', 'manifest'):
                    try:
                        contained_path(proj, item)
                    except SelectionError as error:
                        errors.append(str(error))
                elif isinstance(item, (dict, list)):
                    inspect(item)
        elif isinstance(value, list):
            for item in value:
                inspect(item)
    inspect(data)
    try:
        registry = collect_selectable(data)
        read_selection(registry, proj)
    except (SelectionError, TypeError, AttributeError) as error:
        errors.append(str(error))
    return errors


# --------------------------------------------------------------------------- #
# ffprobe + contact sheet helpers
# --------------------------------------------------------------------------- #

def _run_ffprobe(path):
    """Return dict with duration, width, height, fps, codec, size_mb or {} on failure."""
    try:
        r = subprocess.run(
            [
                "ffprobe", "-v", "quiet",
                "-show_entries", "format=duration,size:stream=codec_name,codec_type,width,height,r_frame_rate",
                "-of", "json", str(path),
            ],
            check=False, capture_output=True, text=True, timeout=15,
        )
        if r.returncode != 0:
            return {}
        d = json.loads(r.stdout)
        fmt = d.get("format", {})
        streams = d.get("streams", [])
        vstream: dict[str, Any] = next((s for s in streams if s.get("codec_type") == "video"), {})
        duration = float(fmt.get("duration", 0))
        size_bytes = int(fmt.get("size", 0))
        width = vstream.get("width", 0)
        height = vstream.get("height", 0)
        fps_raw = vstream.get("r_frame_rate", "0/1")
        fps_num, fps_den = fps_raw.split("/")
        fps = round(int(fps_num) / int(fps_den), 1) if int(fps_den) else 0
        codec = vstream.get("codec_name", "")
        has_audio = any(s.get("codec_type") == "audio" for s in streams)
        return {
            "duration": duration,
            "size_bytes": size_bytes,
            "width": width,
            "height": height,
            "fps": fps,
            "codec": codec,
            "has_audio": has_audio,
            "audio_codecs": list(dict.fromkeys(s.get("codec_name", "unknown") for s in streams if s.get("codec_type") == "audio")),
        }
    except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError, ValueError, KeyError):
        return {}


def _fmt_duration(seconds):
    if seconds < 10:
        return f"{seconds:.2f}s"
    return f"{seconds:.1f}s"


def _fmt_size(bytes_val):
    mb = bytes_val / (1024 * 1024)
    if mb < 10:
        return f"{mb:.1f} MB"
    return f"{mb:.0f} MB"


def _ffprobe_chips(path):
    """Return a chips list for a take card from ffprobe."""
    info = _run_ffprobe(path)
    if not info:
        return []
    chips = []
    if info["size_bytes"]:
        chips.append(_fmt_size(info["size_bytes"]))
    if info["duration"]:
        chips.append(_fmt_duration(info["duration"]))
    if info["fps"]:
        chips.append(f"{info['fps']}fps")
    if info["width"] and info["height"]:
        chips.append(f"{info['width']}x{info['height']}")
    if info["codec"]:
        audio_str = " + " + ", ".join(info["audio_codecs"]) if info["has_audio"] else ""
        chips.append(f"{info['codec']}{audio_str}")
    return chips


def generate_contact_sheet(video_path, output_path, frames=4):
    """Generate a 4-frame contact sheet (opening, 1/3, 2/3, ending) as a JPEG."""
    info = _run_ffprobe(video_path)
    if not info or not info["duration"]:
        return False
    duration = info["duration"]
    w = info["width"] or 1280
    h = info["height"] or 720
    timestamps = [
        min(0.1, duration / 2),
        duration / 3,
        2 * duration / 3,
        max(duration - 0.1, 3 * duration / 4),
    ]
    clip_dur = 0.2
    thumb_w = w // 2
    thumb_h = h // 2
    filter_parts = []
    for i, ts in enumerate(timestamps):
        end_ts = ts + clip_dur
        filter_parts.append(
            f"[0:v]trim={ts:.3f}:{end_ts:.3f},setpts=PTS-STARTPTS,"
            f"scale={thumb_w}:{thumb_h}[t{i}]"
        )
    inputs = "".join(f"[t{i}]" for i in range(len(timestamps)))
    filter_complex = ";".join(filter_parts) + f";{inputs}hstack=inputs={len(timestamps)}[out]"
    try:
        r = subprocess.run(
            [
                "ffmpeg", "-y", "-i", str(video_path),
                "-filter_complex", filter_complex,
                "-map", "[out]", "-frames:v", "1",
                "-q:v", "3", str(output_path),
            ],
            check=False, capture_output=True, timeout=30,
        )
        return r.returncode == 0 and output_path.exists()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def enrich_takes(data, proj, generate_sheets=False):
    """Auto-populate chips and contact sheets for takes sections."""
    for section in data.get("sections", []):
        if section.get("kind") != "takes":
            continue
        for grp in section.get("groups", []):
            # also enrich group meta from first take if empty
            first_info = None
            for tk in grp.get("takes", []):
                src = tk.get("media", {}).get("src", "")
                if not src:
                    continue
                video_path = proj / src
                if not video_path.exists():
                    continue
                info = _run_ffprobe(video_path)
                if not first_info and info:
                    first_info = info
                # auto-populate chips if missing or if we're regenerating
                if (not tk.get("chips") or generate_sheets) and info:
                    tk["chips"] = _ffprobe_chips(video_path)
                # generate contact sheet if requested
                if generate_sheets and not tk.get("contactSheet"):
                    cs_path = video_path.with_name(
                        video_path.stem + "_contacts.jpg"
                    )
                    if generate_contact_sheet(video_path, cs_path):
                        tk["contactSheet"] = str(cs_path.relative_to(proj))
            # auto-populate group meta if empty or regenerating
            if (not grp.get("meta") or generate_sheets) and first_info:
                meta = []
                if first_info["width"] and first_info["height"]:
                    ratio = "16:9" if first_info["width"] > first_info["height"] else "9:16"
                    meta.append(f"{first_info['height']}p")
                    meta.append(ratio)
                if first_info["duration"]:
                    meta.append(f"{_fmt_duration(first_info['duration'])}")
                if meta:
                    grp["meta"] = meta


# --------------------------------------------------------------------------- #
# generation
# --------------------------------------------------------------------------- #

def generate(proj, data, out_name, expected_stage=None):
    with open(TEMPLATE, "r", encoding="utf-8") as f:
        template = f.read()
    with open(RENDERER, "r", encoding="utf-8") as f:
        renderer = f.read()

    proj_path = Path(proj) if proj else None
    if proj_path and data.get("canvas"):
        data = prepare_canvas_data(data, proj_path, expected_stage=expected_stage)

    # bake in current manifest selections if available
    selectable = collect_selectable(data)
    if proj_path and selectable:
        current_sel = read_selection(selectable, proj_path)
        data = dict(data)
        data["currentSelections"] = current_sel
        evidence = {}
        for asset_id, meta in selectable.items():
            path = contained_path(proj_path, meta["manifest"])
            _, document, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
            selection_evidence = document.get("selection_evidence")
            if meta["field"] == "selected_variants" and isinstance(selection_evidence, Mapping):
                selection_evidence = selection_evidence.get(meta["key"])
            if isinstance(selection_evidence, Mapping):
                evidence[asset_id] = {
                    key: selection_evidence.get(key)
                    for key in ("decision_id", "decision_path", "actor", "approval_mode", "result", "review_path", "selected_sha256", "reason")
                    if isinstance(selection_evidence.get(key), str)
                }
                if isinstance(document.get("status"), str):
                    evidence[asset_id]["status"] = document["status"]
        data["selectionEvidence"] = evidence

    data = dict(data)
    data["selectableRegistry"] = selectable
    title = html.escape(str(data.get("title", "Showcase")))
    data_json = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    rendered_html = (
        template
        .replace("__TITLE__", title)
        .replace("__DATA__", data_json)
        .replace(
            "<script>\n/* renderer injected by generator; see scripts/generate_showcase.py */\n</script>",
            "<script>\n" + renderer + "\n</script>",
        )
    )
    out = proj / out_name
    atomic_write(out, rendered_html.encode("utf-8"))
    return out


# --------------------------------------------------------------------------- #
# HTTP server (--serve)
# --------------------------------------------------------------------------- #

class ShowcaseHandler(BaseHTTPRequestHandler):
    service: SelectionService
    proj: Path
    data: ClassVar[dict] = {}
    expected_stage: ClassVar[str | None] = None
    server: HTTPServer
    session_token: str
    index_name = 'index.html'
    maximum_body = 65536

    def _same_host(self):
        return self.headers.get('Host') == f'127.0.0.1:{self.server.server_port}'

    def _send_json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if not self._same_host():
            self._send_json({'ok': False, 'error': 'Invalid localhost host'}, 403)
            return
        if self.path in ('/api/session', '/api/selection', '/api/log'):
            try:
                if self.path == '/api/session':
                    self._send_json({'token': self.session_token, 'stageRevision': stage_revision(self.proj), **self.service.snapshot()})
                elif self.path == '/api/selection':
                    self._send_json(self.service.snapshot())
                else:
                    self._send_json(read_log(self.proj))
            except (SelectionError, OSError) as error:
                self._send_json({'ok': False, 'error': str(error)}, 409)
            return
        from urllib.parse import unquote
        relative = unquote(self.path.split('?', 1)[0]).lstrip('/') or self.index_name
        if any(part.startswith('.') for part in Path(relative).parts):
            self.send_error(404)
            return
        try:
            path = contained_path(self.proj, relative)
        except SelectionError:
            self.send_error(404)
            return
        size = path.stat().st_size
        start, end, status = 0, size - 1, 200
        range_header = self.headers.get('Range')
        if range_header:
            match = re.fullmatch(r'bytes=(\d*)-(\d*)', range_header)
            try:
                if not match or not any(match.groups()) or not size:
                    raise ValueError()
                if match[1]:
                    start = int(match[1])
                    end = min(int(match[2]), size - 1) if match[2] else size - 1
                else:
                    suffix = int(match[2])
                    if suffix <= 0:
                        raise ValueError()
                    start = max(0, size - suffix)
                if start > end or start >= size:
                    raise ValueError()
                status = 206
            except ValueError:
                self.send_response(416)
                self.send_header('Content-Range', f'bytes */{size}')
                self.send_header('Content-Length', '0')
                self.end_headers()
                return
        import mimetypes
        content_type = mimetypes.guess_type(str(path))[0] or 'application/octet-stream'
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(max(0, end - start + 1)))
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('X-Content-Type-Options', 'nosniff')
        if status == 206:
            self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.end_headers()
        with path.open('rb') as stream:
            stream.seek(start)
            remaining = end - start + 1
            while remaining > 0:
                chunk = stream.read(min(65536, remaining))
                if not chunk:
                    break
                self.wfile.write(chunk)
                remaining -= len(chunk)

    def do_POST(self):
        origin = f'http://127.0.0.1:{self.server.server_port}'
        if not self._same_host() or self.headers.get('Origin') != origin or not secrets.compare_digest(self.headers.get('X-Showcase-Token', ''), self.session_token or ''):
            self._send_json({'ok': False, 'error': 'Same-origin session token required'}, 403)
            return
        if self.path not in ('/api/select', '/api/stage-lock'):
            self._send_json({'ok': False, 'error': 'not found'}, 404)
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if length <= 0 or length > self.maximum_body or self.headers.get('Transfer-Encoding'):
                self._send_json({'ok': False, 'error': 'Invalid or oversized request body'}, 413)
                return
            if self.headers.get_content_type() != 'application/json':
                raise SelectionError('Content-Type must be application/json')
            self.connection.settimeout(10)
            payload = self.rfile.read(length)
            if len(payload) != length:
                raise SelectionError('Incomplete request body')
            body = json.loads(payload)
            if not isinstance(body, dict) or not isinstance(body.get('expected_revision'), str) or not body['expected_revision']:
                raise SelectionError('Expected a nonempty expected_revision')
            if self.path == '/api/stage-lock':
                result = self._stage_lock(body)
            else:
                canvas = self.data.get('canvas') or {}
                user_event = secrets.token_urlsafe(24) if canvas.get('approvalContractVersion') == 1 else None
                result = self.service.apply(body.get('selections'), body['expected_revision'], user_event=user_event)
        except SelectionConflict as error:
            self._send_json({'ok': False, 'error': str(error)}, 409)
        except (SelectionError, ValueError, OSError) as error:
            self._send_json({'ok': False, 'error': str(error)}, 400)
        else:
            if self.data.get("canvas"):
                try:
                    type(self).data = load_json(self.proj / "showcase.json")
                    generate(
                        self.proj,
                        self.data,
                        self.index_name,
                        expected_stage=self.expected_stage,
                    )
                except (OSError, UnicodeError, SelectionError) as error:
                    result["canvasSynced"] = False
                    result["canvasError"] = str(error)
                else:
                    result["canvasSynced"] = True
            self._send_json(result)

    def _stage_lock(self, body):
        showcase_path = contained_path(self.proj, 'showcase.json')
        if body.get('canvas_manifest_sha256') != file_sha256(showcase_path):
            raise SelectionConflict('Production canvas changed; reload before approving')
        data = load_json(showcase_path)
        canvas = data.get('canvas')
        if not isinstance(canvas, dict) or canvas.get('approvalContractVersion') != 1:
            raise SelectionError('Stage approval requires a versioned production canvas')
        errors = canvas_validation_errors(data, self.proj, self.expected_stage)
        if errors:
            raise SelectionError('; '.join(errors))
        mode = read_project_mode(self.proj)
        if mode['mode'] != 'ask_for_approval':
            raise SelectionError('User stage approval requires ask_for_approval mode')
        if body['expected_revision'] != stage_revision(self.proj):
            raise SelectionConflict('Stale project revision before stage decision')
        stage_id = canvas.get('currentStage')
        stage = next((item for item in canvas.get('stages', []) if isinstance(item, dict) and item.get('id') == stage_id), None)
        if stage is None or stage.get('status') not in {'active', 'review'}:
            raise SelectionError('Current stage is not awaiting approval')
        choice = body.get('candidate')
        if not isinstance(choice, dict) or set(choice) != {'lock_kind', 'artifact_path'}:
            raise SelectionError('Expected a registered stage lock candidate')
        candidates = stage.get('lockCandidates', [])
        matches = [item for item in candidates if isinstance(item, dict) and item.get('lock_kind') == choice['lock_kind'] and item.get('artifact_path') == choice['artifact_path']]
        if len(matches) != 1:
            raise SelectionError('Stage lock candidate is unavailable or ambiguous')
        candidate = matches[0]
        if candidate['lock_kind'] in stage.get('locks', {}):
            raise SelectionError('Stage lock already exists; reload before changing it')
        artifact = contained_path(self.proj, candidate['artifact_path'])
        review = contained_path(self.proj, candidate['review_path'])
        decision = {
            'schema_version': 1,
            'decision_id': f"ui-{secrets.token_hex(12)}",
            'decision_type': 'stage_lock',
            'stage_id': stage_id,
            'lock_kind': candidate['lock_kind'],
            'subject_path': candidate['artifact_path'],
            'subject_sha256': file_sha256(artifact),
            'actor': 'user',
            'approval_mode': mode['mode'],
            'project_sha256': mode['project_sha256'],
            'result': 'approved',
            'review_path': candidate['review_path'],
            'review_sha256': file_sha256(review),
            'upstream_sha256': candidate['upstream_sha256'],
            'reason': candidate['reason'],
            'decided_at': datetime.datetime.now(datetime.UTC).isoformat(),
            'authorization': {'source': 'local_ui', 'evidence': secrets.token_urlsafe(24)},
        }
        return record_stage_decision(self.proj, decision, body['expected_revision'], user_event=decision['authorization']['evidence'])

    def log_message(self, *args):
        pass


def serve(proj, data, port, index_name='index.html', expected_stage=None):
    handler = type('ProjectShowcaseHandler', (ShowcaseHandler,), {
        'service': SelectionService(proj, data), 'proj': proj,
        'data': data, 'expected_stage': expected_stage,
        'session_token': secrets.token_urlsafe(32), 'index_name': index_name,
    })
    httpd = HTTPServer(('127.0.0.1', port), handler)
    url = f'http://127.0.0.1:{httpd.server_port}/{index_name}'
    print(f'serving {proj} at {url}  (Ctrl+C to stop)')
    threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nstopped')
    finally:
        httpd.server_close()


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

_VIDEO_EXTS = {".mp4", ".mov", ".webm", ".mkv", ".avi"}
_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
_AUDIO_EXTS = {".wav", ".mp3", ".ogg", ".flac", ".aac"}


def _detect_media_type(path):
    ext = path.suffix.lower()
    if ext in _VIDEO_EXTS:
        return "video"
    if ext in _IMAGE_EXTS:
        return "image"
    if ext in _AUDIO_EXTS:
        return "audio"
    return None


def quick_review(paths, out_path=None, do_contact_sheets=False, open_browser=False):
    """Build a minimal showcase page from a list of media file paths — no showcase.json needed.

    Videos from the same directory are grouped into takes groups.
    Images are placed in a grid section.
    Audio files are placed in an audio section.
    """
    # resolve to absolute paths and validate
    resolved = []
    for p in paths:
        fp = Path(p).resolve()
        if not fp.exists():
            print(f"warning: file not found: {p}")
            continue
        resolved.append(fp)
    if not resolved:
        sys.exit("no valid media files found")

    # group by type
    videos_by_dir: dict[str, list[Path]] = {}
    images = []
    audios = []
    for fp in resolved:
        mtype = _detect_media_type(fp)
        if mtype == "video":
            d = str(fp.parent)
            videos_by_dir.setdefault(d, []).append(fp)
        elif mtype == "image":
            images.append(fp)
        elif mtype == "audio":
            audios.append(fp)
        else:
            print(f"warning: unrecognized file type: {fp}")

    sections: list[dict[str, Any]] = []

    # build takes groups for videos
    if videos_by_dir:
        groups = []
        for d, vids in sorted(videos_by_dir.items()):
            dpath = Path(d)
            group_title = dpath.name or "Videos"
            takes = []
            first_info = None
            for v in sorted(vids):
                info = _run_ffprobe(v)
                if not first_info and info:
                    first_info = info
                chips = _ffprobe_chips(v) if info else []
                take = {
                    "label": v.stem,
                    "media": {"type": "video", "src": str(v)},
                    "chips": chips,
                }
                # contact sheet
                if do_contact_sheets:
                    cs_path = v.with_name(v.stem + "_contacts.jpg")
                    if generate_contact_sheet(v, cs_path):
                        take["contactSheet"] = str(cs_path)
                takes.append(take)
            meta = []
            if first_info:
                if first_info.get("height"):
                    ratio = "16:9" if first_info.get("width", 0) > first_info.get("height", 0) else "9:16"
                    meta.append(f"{first_info['height']}p")
                    meta.append(ratio)
                if first_info.get("duration"):
                    meta.append(_fmt_duration(first_info["duration"]))
            groups.append({
                "title": group_title,
                "uc": "",
                "meta": meta,
                "takes": takes,
            })
        sections.append({
            "id": "video-review",
            "title": "Video Review",
            "icon": "🎥",
            "iconBg": "var(--accent-soft)",
            "count": f"{sum(len(g['takes']) for g in groups)} videos · {len(groups)} group(s)",
            "desc": "Quick review — auto-generated from file paths. Videos from the same folder are grouped.",
            "kind": "takes",
            "groups": groups,
        })

    # build grid for images
    if images:
        cards = []
        for img in sorted(images):
            cards.append({
                "type": "elem",
                "kindPill": "Image",
                "media": {"type": "image", "src": str(img), "alt": img.name},
                "tag": "",
                "title": img.stem,
                "sub": img.name,
                "chips": [],
                "prompt": "",
            })
        sections.append({
            "id": "images",
            "title": "Images",
            "icon": "🖼️",
            "iconBg": "var(--accent-2-soft)",
            "count": f"{len(images)} image(s)",
            "desc": "Quick review — auto-generated from file paths.",
            "kind": "grid",
            "mediaOnly": True,
            "cards": cards,
        })

    # build grid for audio
    if audios:
        cards = []
        for aud in sorted(audios):
            cards.append({
                "type": "audio",
                "kindPill": "Audio",
                "media": {"type": "audio", "src": str(aud)},
                "tag": "AUDIO",
                "title": aud.stem,
                "sub": aud.name,
                "chips": [],
                "prompt": "",
            })
        sections.append({
            "id": "audio",
            "title": "Audio",
            "icon": "🔊",
            "iconBg": "var(--accent-3-soft)",
            "count": f"{len(audios)} track(s)",
            "desc": "Quick review — auto-generated from file paths.",
            "kind": "grid",
            "mediaOnly": False,
            "cards": cards,
        })

    data: dict[str, Any] = {
        "title": "Quick Review",
        "kicker": "Ad-hoc Media Review",
        "lede": f"Auto-generated from {len(resolved)} file(s). No showcase.json required.",
        "badges": [],
        "sections": sections,
        "footer": "Generated with showcase-html --quick.",
    }

    # use absolute paths for media src (since there's no project dir)
    # convert to file:// URIs for browser access
    for section in data["sections"]:
        if section.get("kind") == "takes":
            for grp in section.get("groups", []):
                for tk in grp.get("takes", []):
                    src = tk.get("media", {}).get("src", "")
                    if src and not src.startswith("http"):
                        tk["media"]["src"] = "file://" + src
                    cs = tk.get("contactSheet", "")
                    if cs and not cs.startswith("http"):
                        tk["contactSheet"] = "file://" + cs
        else:
            for card in section.get("cards", []):
                src = card.get("media", {}).get("src", "")
                if src and not src.startswith("http") and not src.startswith("file://"):
                    card["media"]["src"] = "file://" + src

    # determine output path
    if out_path:
        out = Path(out_path)
    else:
        out = Path.cwd() / "_quick_review.html"
    # write to a temp dir, use common_root for relative paths if possible
    # but since we're using file:// URIs, the output location doesn't matter
    # generate using the template directly
    with open(TEMPLATE, "r", encoding="utf-8") as f:
        template = f.read()
    with open(RENDERER, "r", encoding="utf-8") as f:
        renderer = f.read()

    data_json = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    rendered_html = (
        template
        .replace("__TITLE__", data["title"])
        .replace("__DATA__", data_json)
        .replace(
            "<script>\n/* renderer injected by generator; see scripts/generate_showcase.py */\n</script>",
            "<script>\n" + renderer + "\n</script>",
        )
    )
    out.write_text(rendered_html, encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    if open_browser:
        webbrowser.open(f"file://{out.resolve()}")
    return out


def main():
    parser = argparse.ArgumentParser(
        description="Generate a self-contained showcase index.html from showcase.json, or a quick review page from file paths."
    )
    parser.add_argument("project_dir", nargs="?", default=None,
                        help="Project directory containing showcase.json. Required unless --quick is used.")
    parser.add_argument("--quick", nargs="+", metavar="PATH",
                        help="Quick mode: build a review page from file paths (no showcase.json needed).")
    parser.add_argument("--out", default=None,
                        help="Output HTML filename (default: index.html, or _quick_review.html in --quick mode).")
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--init",
        action="store_true",
        help="Initialize the persistent eight-stage canvas without overwriting an existing showcase.json.",
    )
    parser.add_argument(
        "--stage",
        choices=CANVAS_STAGE_IDS,
        help="Require this production-canvas stage and verify HTML freshness with --check.",
    )
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--contact-sheets", action="store_true",
                        help="Generate contact sheet images for video takes via FFmpeg.")
    parser.add_argument("--apply", metavar="JSON_OR_FILE",
                        help="Apply selections from a JSON string or file path, updating manifests and selection.json.")
    parser.add_argument("--stage-decision", metavar="JSON_OR_FILE",
                        help="Record a reviewed picture, audio, or final-master stage lock.")
    parser.add_argument("--set-approval-mode", choices=("approve_for_me", "ask_for_approval"),
                        help="Set the project approval mode and refresh the production canvas.")
    parser.add_argument("--open", action="store_true",
                        help="Open the generated HTML in the default browser.")
    parser.add_argument("--expected-revision", help="Reject --apply when current manifest hashes differ")
    args = parser.parse_args()
    writes = sum(bool(item) for item in (args.apply, args.stage_decision, args.set_approval_mode))
    if writes > 1:
        parser.error("--apply, --stage-decision, and --set-approval-mode cannot be combined")
    if writes and (args.serve or args.contact_sheets):
        parser.error("project writes cannot be combined with --serve or --contact-sheets")
    if args.check and (writes or args.serve or args.quick or args.init):
        parser.error("--check cannot be combined with a write, --serve, --quick, or --init")
    if args.init and (writes or args.serve or args.quick or args.contact_sheets or args.stage):
        parser.error("--init cannot be combined with a write, --serve, --quick, --contact-sheets, or --stage")
    if args.quick and (writes or args.serve or args.stage):
        parser.error("--quick cannot be combined with project writes, --serve, or --stage")

    # ---- quick mode ----
    if args.quick:
        out_path = args.out or "_quick_review.html"
        quick_review(
            args.quick,
            out_path=out_path,
            do_contact_sheets=args.contact_sheets,
            open_browser=True,  # always open in quick mode
        )
        return

    # ---- normal mode (requires project_dir + showcase.json) ----
    if not args.project_dir:
        parser.error("project_dir is required (or use --quick with file paths)")
    if not os.path.isdir(args.project_dir):
        sys.exit(f"not a directory: {args.project_dir}")

    proj = os.path.abspath(args.project_dir)
    proj_path = Path(proj)
    out_name = args.out or "index.html"
    manifest = os.path.join(proj, "showcase.json")
    if args.init:
        if os.path.exists(manifest):
            sys.exit(f"refusing to overwrite existing manifest: {manifest}")
        data = load_json(CANVAS_TEMPLATE)
        data["title"] = f"{proj_path.name.replace('-', ' ').title()} Production Canvas"
        errors = canvas_validation_errors(data, proj_path, "brief-development")
        if errors:
            for item in errors:
                print(f"invalid showcase: {item}")
            sys.exit(1)
        manifest_content = (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
        try:
            prepare_canvas_data(
                data,
                proj_path,
                manifest_bytes=manifest_content,
                expected_stage="brief-development",
            )
        except (OSError, UnicodeError, SelectionError) as error:
            sys.exit(f"canvas initialization failed: {error}")
        atomic_write(
            Path(manifest),
            manifest_content,
        )
        out = generate(
            proj_path,
            data,
            out_name,
            expected_stage="brief-development",
        )
        print(f"initialized {manifest}")
        print(f"wrote {out} ({out.stat().st_size} bytes)")
        if args.open:
            webbrowser.open(f"file://{out.resolve()}")
        return
    if not os.path.exists(manifest):
        sys.exit(f"missing manifest: {manifest}")

    data = load_json(manifest)
    if data.get("canvas") and not args.stage:
        sys.exit("production canvas commands require --stage <stage-id>")

    missing = validate(data, proj_path)
    if args.stage or data.get("canvas"):
        missing.extend(canvas_validation_errors(data, proj_path, args.stage))
    if missing:
        for item in missing:
            print(f"invalid showcase: {item}")
        if args.check or args.strict or args.apply or args.serve or args.stage or data.get("canvas"):
            sys.exit(1)
    if args.check:
        if args.stage:
            stale = canvas_sync_errors(data, proj_path, proj_path / out_name, args.stage)
            if stale:
                for item in stale:
                    print(f"invalid showcase: {item}")
                sys.exit(1)
            print(f"OK: production canvas is current for {args.stage}")
            return
        print("OK: all media, prompts, and manifests resolve")
        return

    if args.apply:
        try:
            payload = load_json_argument(args.apply, "--apply")
        except SelectionError as error:
            sys.exit(str(error))
        decisions = payload.get("decisions") if isinstance(payload, dict) else None
        selections = payload.get("selections") if isinstance(payload, dict) and "selections" in payload else payload
        if not isinstance(selections, dict):
            sys.exit("expected a dict of {asset_id: filename} for --apply")

        try:
            result = SelectionService(proj_path, data).apply(
                selections, args.expected_revision, decisions=decisions
            )
        except (SelectionError, OSError) as error:
            sys.exit(f"selection failed: {error}")
        if data.get("canvas"):
            try:
                data = load_json(manifest)
                generate(proj_path, data, out_name, expected_stage=args.stage)
            except (OSError, UnicodeError, SelectionError) as error:
                result["canvasSynced"] = False
                result["canvasError"] = str(error)
                print(json.dumps(result))
                sys.exit(2)
            result["canvasSynced"] = True
        print(json.dumps(result))
        return

    if args.stage_decision or args.set_approval_mode:
        try:
            if args.stage_decision:
                decision = load_json_argument(args.stage_decision, "--stage-decision")
                result = record_stage_decision(
                    proj_path, decision, expected_revision=args.expected_revision
                )
            else:
                result = set_project_mode(proj_path, args.set_approval_mode, expected_revision=args.expected_revision)
        except (SelectionError, OSError, UnicodeError) as error:
            sys.exit(f"decision failed: {error}")
        try:
            data = load_json(manifest)
            generate(proj_path, data, out_name, expected_stage=args.stage)
        except (SelectionError, OSError, UnicodeError) as error:
            result["canvasSynced"] = False
            result["canvasError"] = str(error)
            print(json.dumps(result))
            sys.exit(2)
        result["canvasSynced"] = True
        print(json.dumps(result))
        return

    enrich_takes(data, proj_path, generate_sheets=args.contact_sheets)
    if args.contact_sheets:
        atomic_write(proj_path / 'showcase.json', (json.dumps(data, indent=2, ensure_ascii=False) + '\n').encode('utf-8'))

    if args.serve:
        try:
            generate(proj_path, data, out_name, expected_stage=args.stage)
        except (OSError, UnicodeError, SelectionError) as error:
            sys.exit(f"canvas generation failed: {error}")
        serve(proj_path, data, args.port, out_name, expected_stage=args.stage)
        return

    try:
        out = generate(proj_path, data, out_name, expected_stage=args.stage)
    except (OSError, UnicodeError, SelectionError) as error:
        sys.exit(f"canvas generation failed: {error}")
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    if args.open:
        webbrowser.open(f"file://{out.resolve()}")


if __name__ == "__main__":
    main()
