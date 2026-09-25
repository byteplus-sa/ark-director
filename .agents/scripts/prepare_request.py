from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from operation_store import prepare_operation, require_current_approval_contract
from ruamel.yaml.error import YAMLError
from validate_request import (
    Finding,
    compute_request_hash,
    contained_path,
    frontmatter,
    parse_frontmatter,
    prepared_evidence_findings,
    project_mode_snapshot,
    schema_findings,
    validate_request,
    validate_review,
)

VIDEO_SUFFIXES = {".mp4", ".mov", ".mkv", ".webm", ".m4v"}
AUDIO_SUFFIXES = {".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg"}
ASSET_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
VENDOR_PREFIXES = {"dreamina", "dola", "byteplus"}
DECISION_KEYS = (
    "decision_id",
    "decision_path",
    "decision_sha256",
    "review_path",
    "review_sha256",
    "selected_sha256",
)


def parse_value(text: str) -> Any:
    def reject(constant: str) -> Any:
        raise ValueError(constant)

    try:
        return json.loads(text, parse_constant=reject)
    except ValueError:
        return text


def parse_params(items: list[str]) -> dict[str, Any]:
    params: dict[str, Any] = {}
    for item in items:
        key, separator, value = item.partition("=")
        if not separator or not key:
            raise ValueError(f"Expected key=value parameter: {item}")
        if key in params:
            raise ValueError(f"Duplicate parameter: {key}")
        params[key] = parse_value(value)
    return params


def relative_path(value: str) -> str:
    path = Path(value)
    if not value or path.is_absolute() or ".." in path.parts:
        raise ValueError(f"Expected a project-relative path without traversal: {value}")
    return path.as_posix()


def media_kind(path: str) -> str:
    suffix = Path(path).suffix.lower()
    if suffix in VIDEO_SUFFIXES:
        return "Video"
    if suffix in AUDIO_SUFFIXES:
        return "Audio"
    return "Image"


def parse_legacy(items: list[str]) -> dict[str, str]:
    legacy: dict[str, str] = {}
    for item in items:
        path, separator, asset = item.partition("=")
        if not separator or not path or not asset:
            raise ValueError(f"Expected --ref-legacy <path>=<legacy-asset-id>: {item}")
        legacy[relative_path(path)] = asset
    return legacy


def decision_evidence(
    root: Path, reference: dict[str, Any], legacy_asset: str | None
) -> dict[str, Any]:
    evidence = reference["approval_evidence"]
    if legacy_asset is not None:
        audit = contained_path(root, "selection.log")
        return {
            **evidence,
            "selected_sha256": reference["sha256"],
            "evidence_type": "legacy",
            "legacy_asset_id": legacy_asset,
            "audit_path": "selection.log",
            "audit_sha256": hashlib.sha256(audit.read_bytes()).hexdigest(),
        }
    recorded = frontmatter(root, evidence["manifest"]).get("selection_evidence")
    if evidence["field"] == "selected_variants" and isinstance(recorded, dict):
        recorded = recorded.get(evidence.get("key"))
    if not isinstance(recorded, dict) or any(
        not isinstance(recorded.get(key), str) for key in DECISION_KEYS
    ):
        raise ValueError(
            f"Reference {reference['path']}: {evidence['manifest']} has no structured "
            f"selection_evidence ({', '.join(DECISION_KEYS)}). Record a hash-bound "
            "selection decision for it first, or, for a pre-contract selection "
            "confirmed in selection.log, pass "
            f"--ref-legacy {reference['path']}=<legacy-asset-id>"
        )
    return {**evidence, **{key: recorded[key] for key in DECISION_KEYS}}


def canvas_contract_version(root: Path) -> int:
    path = root / "showcase.json"
    if not path.exists():
        return 0
    if path.is_symlink():
        raise ValueError("Production canvas must not be a symlink")
    document = json.loads(path.read_text())
    canvas = document.get("canvas") if isinstance(document, dict) else None
    version = canvas.get("approvalContractVersion") if isinstance(canvas, dict) else 0
    return version if isinstance(version, int) and not isinstance(version, bool) else 0


def declares_approval_mode(root: Path) -> bool:
    text = contained_path(root, "project.md").read_text(encoding="utf-8")
    return text.startswith("---") and "approval_mode" in parse_frontmatter(text)


def canvas_finding(root: Path, request: dict[str, Any]) -> Finding | None:
    try:
        require_current_approval_contract(root, request)
    except (ValueError, TypeError) as error:
        stage = "<stage-id>"
        try:
            canvas = json.loads((root / "showcase.json").read_text()).get("canvas")
            stage = canvas.get("currentStage") or stage
        except (OSError, ValueError, AttributeError):
            pass
        generator = ".agents/skills/showcase-html/scripts/generate_showcase.py"
        return Finding(
            "approval.current_canvas",
            f"{error}. Initialize the canvas with `uv run python {generator} "
            f"{root} --init` if showcase.json is missing, set canvas.currentStage, "
            f"then regenerate index.html with `uv run python {generator} {root} "
            f"--stage {stage}` and retry.",
            "showcase.json",
        )
    return None


def build_references(root: Path, items: list[str]) -> list[dict[str, Any]]:
    counters = {"Image": 0, "Video": 0, "Audio": 0}
    references: list[dict[str, Any]] = []
    for item in items:
        parts = item.split(":")
        if len(parts) not in (3, 4, 5):
            raise ValueError(
                f"Expected path:role:manifest[:field[:key]] reference: {item}"
            )
        path, role, manifest = (relative_path(part) for part in parts[:3])
        field = parts[3] if len(parts) > 3 else "selected_variant"
        target = contained_path(root, path)
        contained_path(root, manifest)
        kind = media_kind(path)
        counters[kind] += 1
        evidence: dict[str, Any] = {"manifest": manifest, "field": field}
        if len(parts) == 5:
            evidence["key"] = parts[4]
        references.append(
            {
                "path": path,
                "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                "role": role,
                "binding": f"@{kind} {counters[kind]}",
                "approval_evidence": evidence,
            }
        )
    return references


def model_family(model: str) -> str:
    tokens = [token for token in re.split(r"[-._]", model.lower()) if token]
    if tokens and tokens[0] in VENDOR_PREFIXES:
        tokens = tokens[1:]
    if len(tokens) > 1 and re.fullmatch(r"\d{6}", tokens[-1]):
        tokens = tokens[:-1]
    if not tokens:
        raise ValueError("Model identifier has no family name")
    return tokens[0] + "".join(tokens[1:])


def build_request(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    if not ASSET_PATTERN.fullmatch(args.asset):
        raise ValueError("Asset ID must contain only letters, digits, _ and -")
    prompt_file = relative_path(args.prompt)
    prompt_bytes = contained_path(root, prompt_file).read_bytes()
    references = build_references(root, args.ref)
    params = parse_params(args.param)
    version = args.schema_version or (
        2 if declares_approval_mode(root) or canvas_contract_version(root) >= 1 else 1
    )
    legacy = parse_legacy(args.ref_legacy)
    unknown = set(legacy) - {reference["path"] for reference in references}
    if unknown:
        raise ValueError(f"--ref-legacy names no --ref path: {min(unknown)}")
    if legacy and version != 2:
        raise ValueError("--ref-legacy applies only to schema version 2 requests")
    mode: dict[str, Any] = {}
    if version == 2:
        for reference in references:
            reference["approval_evidence"] = decision_evidence(
                root, reference, legacy.get(reference["path"])
            )
        approval_mode, project_sha256 = project_mode_snapshot(root)
        mode = {"approval_mode": approval_mode, "project_sha256": project_sha256}
    operation_id = args.operation_id or "-".join(
        (
            model_family(args.model),
            args.asset.replace("_", "-"),
            datetime.now(UTC).strftime("%Y%m%d"),
        )
    )
    return {
        "schema_version": version,
        "operation_id": operation_id,
        "asset_id": args.asset,
        "transport": args.transport,
        "model": args.model,
        "operation": args.operation,
        "prompt_file": prompt_file,
        "prompt_sha256": hashlib.sha256(prompt_bytes).hexdigest(),
        "request_sha256": compute_request_hash(
            prompt_bytes, references, args.model, args.operation, params, **mode
        ),
        "references": references,
        "params": params,
        "submission_status": "prepared",
        "provider_task_id": None,
        "provider_status": None,
        "review_status": "not_started",
        "cost": {"estimated": None, "confirmed": None, "currency": "USD"},
        "extensions": {"expected_output": relative_path(args.expected_output)},
        **mode,
    }


def serialize(document: dict[str, Any]) -> str:
    return json.dumps(document, indent=2, ensure_ascii=False, allow_nan=False) + "\n"


def write_once(root: Path, relative: str, content: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError("Output path escapes the project")
    if path.exists():
        if path.read_text() != content:
            raise ValueError(f"Refusing to overwrite a different file: {relative}")
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as handle:
        handle.write(content)
    return path


def load_json(root: Path, relative: str) -> Any:
    return json.loads(contained_path(root, relative_path(relative)).read_text())


def run(args: argparse.Namespace) -> tuple[dict[str, Any], list[Finding]]:
    root = args.project.resolve()
    if not root.is_dir():
        raise ValueError("Project directory does not exist")
    request = build_request(root, args)
    findings = schema_findings(request, "generation-request.schema.json")
    if not findings:
        findings = prepared_evidence_findings(root, request)
    result: dict[str, Any] = {"request_sha256": request["request_sha256"]}
    review = capabilities = None
    if args.register and not findings:
        review = load_json(root, args.review)
        capabilities = load_json(root, args.capabilities)
        findings = validate_request(root, request, capabilities)
        findings.extend(
            validate_review(review, request["request_sha256"], args.required_rule)
        )
        canvas = canvas_finding(root, request)
        if canvas is not None:
            findings.append(canvas)
    if findings or not args.write:
        result["request"] = request
        return result, findings
    path = write_once(root, f"requests/request_{args.asset}.json", serialize(request))
    result["path"] = path.relative_to(root).as_posix()
    if args.register and review is not None and capabilities is not None:
        try:
            prepare_operation(root, request, capabilities, review, args.required_rule)
        except ValueError as error:
            return result, [Finding("registry.prepare", str(error), "task_ids.json")]
        result["registered"] = request["operation_id"]
    return result, findings


def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a generation request; never calls a provider"
    )
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--asset", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--operation", required=True)
    parser.add_argument("--param", action="append", default=[])
    parser.add_argument("--ref", action="append", default=[])
    parser.add_argument("--expected-output", required=True)
    parser.add_argument("--transport", choices=("ark-mcp", "arkcli"), default="ark-mcp")
    parser.add_argument("--operation-id")
    parser.add_argument("--schema-version", type=int, choices=(1, 2))
    parser.add_argument("--ref-legacy", action="append", default=[])
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--register", action="store_true")
    parser.add_argument("--review")
    parser.add_argument("--capabilities")
    parser.add_argument("--required-rule", action="append", default=[])
    return parser


def main(argv: list[str] | None = None) -> int:
    cli = parser()
    args = cli.parse_args(argv)
    if args.register and not (args.write and args.review and args.capabilities):
        cli.error("--register requires --write, --review and --capabilities")
    try:
        result, findings = run(args)
    except (OSError, ValueError, TypeError, UnicodeError, YAMLError) as error:
        result, findings = {}, [Finding("input.readable", str(error))]
    print(
        json.dumps(
            {"ok": not findings, **result, "findings": [asdict(f) for f in findings]},
            indent=2,
            ensure_ascii=False,
        )
    )
    return int(bool(findings))


if __name__ == "__main__":
    sys.exit(main())
