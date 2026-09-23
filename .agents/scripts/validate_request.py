from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

SCHEMA_ROOT = Path(__file__).resolve().parents[1] / "contracts/schemas"


@dataclass(frozen=True)
class Finding:
    rule_id: str
    message: str
    path: str = ""
    severity: str = "error"
    line: int = 0


@dataclass(frozen=True)
class RecoveryDecision:
    action: str
    task_id: str | None = None
    reason: str = ""


def contained_path(root: Path, value: str) -> Path:
    if (
        not isinstance(value, str)
        or not value
        or Path(value).is_absolute()
        or ".." in Path(value).parts
    ):
        raise ValueError("Expected a project-relative path without traversal")
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError("Path must resolve to an existing file within the project")
    return path


def schema_findings(value: Any, name: str) -> list[Finding]:
    schema = json.loads((SCHEMA_ROOT / name).read_text())
    if name == "generation-request.schema.json" and isinstance(value, dict):
        version = value.get("schema_version")
        if version in (1, 2):
            schema = schema["$defs"][f"requestV{version}"]
    return [
        Finding("schema.valid", error.message, ".".join(map(str, error.path)))
        for error in Draft202012Validator(
            schema, format_checker=FormatChecker()
        ).iter_errors(value)
    ]


def compute_request_hash(
    prompt_bytes: bytes,
    references: list[dict[str, Any]],
    model: str,
    operation: str,
    params: dict[str, Any],
    *,
    approval_mode: str | None = None,
    project_sha256: str | None = None,
) -> str:
    body: dict[str, Any] = {
        "prompt_sha256": hashlib.sha256(prompt_bytes).hexdigest(),
        "model": model,
        "operation": operation,
        "params": params,
        "references": [
            {key: ref.get(key) for key in ("sha256", "role", "binding")}
            for ref in references
        ],
    }
    if approval_mode is not None or project_sha256 is not None:
        body["approval_mode"] = approval_mode
        body["project_sha256"] = project_sha256
        body["references"] = [
            {
                key: ref.get(key)
                for key in ("sha256", "role", "binding", "approval_evidence")
            }
            for ref in references
        ]
    return hashlib.sha256(
        json.dumps(
            body,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode()
    ).hexdigest()


def parse_frontmatter(text: str) -> dict[str, Any]:
    match = re.match(r"\A---\s*\n(.*?)\n---(?:\n|$)", text, re.DOTALL)
    if not match:
        raise ValueError("Expected YAML frontmatter")
    metadata = YAML(typ="safe").load(match.group(1))
    if not isinstance(metadata, dict):
        raise TypeError("Expected frontmatter mapping")
    return metadata


def frontmatter(root: Path, relative: str) -> dict[str, Any]:
    return parse_frontmatter(contained_path(root, relative).read_text())


def project_mode_snapshot(root: Path) -> tuple[str, str]:
    path = contained_path(root, "project.md")
    content = path.read_bytes()
    text = content.decode("utf-8")
    metadata = parse_frontmatter(text) if text.startswith("---") else {}
    mode = metadata.get("approval_mode", "approve_for_me")
    if mode not in ("approve_for_me", "ask_for_approval"):
        raise ValueError("Invalid project approval mode")
    return mode, hashlib.sha256(content).hexdigest()


def project_mode_findings(root: Path, request: dict[str, Any]) -> list[Finding]:
    if request["schema_version"] != 2:
        return []
    try:
        mode, digest = project_mode_snapshot(root)
    except (ValueError, TypeError, OSError, UnicodeError, YAMLError) as error:
        return [Finding("approval.current_mode", str(error), "project.md")]
    if request["approval_mode"] != mode or request["project_sha256"] != digest:
        return [
            Finding(
                "approval.current_mode",
                "Project approval mode or project.md changed after request preparation",
                "project.md",
            )
        ]
    return []


def selected_manifest_value(
    metadata: dict[str, Any], evidence: dict[str, Any]
) -> str | None:
    field = evidence.get("field")
    if field not in ("selected_variant", "selected_variants"):
        return None
    selected = metadata.get(field)
    if field == "selected_variants":
        selected = (
            selected.get(evidence.get("key")) if isinstance(selected, dict) else None
        )
    return selected if isinstance(selected, str) and selected != "auto" else None


def approval_matches(root: Path, ref: dict[str, Any], target: Path) -> bool:
    evidence = ref.get("approval_evidence", {})
    try:
        manifest = contained_path(root, evidence.get("manifest", ""))
        metadata = frontmatter(root, evidence.get("manifest", ""))
        selected = selected_manifest_value(metadata, evidence)
        if (
            not isinstance(selected, str)
            or selected == "auto"
            or Path(selected).is_absolute()
            or ".." in Path(selected).parts
        ):
            return False
        return any(
            candidate.resolve() == target
            for candidate in (root / selected, manifest.parent / selected)
        )
    except (OSError, ValueError, TypeError, AttributeError, YAMLError):
        return False


def candidate_review_findings(
    root: Path, review: Any, subject_path: str, subject_sha256: str
) -> list[Finding]:
    findings = schema_findings(review, "candidate-review.schema.json")
    if findings:
        return findings
    if (
        review["artifact_path"] != subject_path
        or review["artifact_sha256"] != subject_sha256
        or review["status"] != "pass"
    ):
        findings.append(
            Finding(
                "approval.passing_review", "Review is stale, incomplete, or failing"
            )
        )
    if not any(check["status"] == "pass" for check in review["checks"]):
        findings.append(
            Finding("approval.passing_review", "Review has no passing check")
        )
    if any(check["status"] in ("fail", "incomplete") for check in review["checks"]):
        findings.append(
            Finding(
                "approval.passing_review",
                "Review contains a failed or incomplete check",
            )
        )
    method = review["inspection_method"].lower()
    suffix = Path(subject_path).suffix.lower()
    if suffix in (".mp4", ".mov", ".mkv", ".webm") and not any(
        word in method for word in ("playback", "temporal")
    ):
        findings.append(
            Finding("approval.inspection_method", "Video requires temporal inspection")
        )
    if suffix in (".wav", ".mp3", ".m4a", ".aac", ".flac") and "listen" not in method:
        findings.append(
            Finding("approval.inspection_method", "Audio requires listening evidence")
        )
    try:
        subject = contained_path(root, subject_path)
        if hashlib.sha256(subject.read_bytes()).hexdigest() != subject_sha256:
            findings.append(
                Finding(
                    "approval.selected_hash", "Selected artifact changed", subject_path
                )
            )
    except (ValueError, OSError) as error:
        findings.append(Finding("approval.selected_hash", str(error), subject_path))
    return findings


def decision_findings(
    root: Path, decision: Any, *, require_current_project: bool = False
) -> list[Finding]:
    findings = schema_findings(decision, "production-decision.schema.json")
    if findings:
        return findings
    if decision["result"] != "approved":
        findings.append(Finding("approval.decision_result", "Decision is not approved"))
    subject_sha256 = decision.get("selected_sha256", decision.get("subject_sha256"))
    try:
        subject = contained_path(root, decision["subject_path"])
        if hashlib.sha256(subject.read_bytes()).hexdigest() != subject_sha256:
            findings.append(
                Finding(
                    "approval.selected_hash",
                    "Selected artifact changed",
                    decision["subject_path"],
                )
            )
    except (ValueError, OSError) as error:
        findings.append(
            Finding("approval.selected_hash", str(error), decision["subject_path"])
        )
    try:
        review_path = contained_path(root, decision["review_path"])
        review_bytes = review_path.read_bytes()
        if hashlib.sha256(review_bytes).hexdigest() != decision["review_sha256"]:
            findings.append(
                Finding(
                    "approval.review_hash",
                    "Review file changed",
                    decision["review_path"],
                )
            )
        else:
            review = json.loads(review_bytes)
            findings.extend(
                candidate_review_findings(
                    root, review, decision["subject_path"], subject_sha256
                )
            )
    except (ValueError, OSError, UnicodeError, json.JSONDecodeError) as error:
        findings.append(
            Finding("approval.passing_review", str(error), decision["review_path"])
        )
    for path, digest in decision["upstream_sha256"].items():
        try:
            upstream = contained_path(root, path)
            if hashlib.sha256(upstream.read_bytes()).hexdigest() != digest:
                findings.append(
                    Finding("approval.upstream_hash", "Upstream artifact changed", path)
                )
        except (ValueError, OSError) as error:
            findings.append(Finding("approval.upstream_hash", str(error), path))
    if require_current_project:
        findings.extend(
            project_mode_findings(
                root,
                {
                    "schema_version": 2,
                    "approval_mode": decision["approval_mode"],
                    "project_sha256": decision["project_sha256"],
                },
            )
        )
    return findings


def approval_decision_findings(
    root: Path, ref: dict[str, Any], target: Path
) -> list[Finding]:
    evidence = ref["approval_evidence"]
    path = ref["path"]
    findings: list[Finding] = []
    if not approval_matches(root, ref, target):
        findings.append(
            Finding(
                "approval.selected_variant",
                "Reference does not match the manifest selection",
                path,
            )
        )
        return findings
    if evidence.get("evidence_type") == "legacy":
        return legacy_approval_findings(root, ref)
    try:
        metadata = frontmatter(root, evidence["manifest"])
        if (
            evidence["field"] == "selected_variant"
            and metadata.get("status") != "approved"
        ):
            findings.append(
                Finding(
                    "approval.manifest_status",
                    "Manifest selection is not approved",
                    evidence["manifest"],
                )
            )
        manifest_evidence = metadata.get("selection_evidence")
        if evidence["field"] == "selected_variants":
            manifest_evidence = (
                manifest_evidence.get(evidence["key"])
                if isinstance(manifest_evidence, dict)
                else None
            )
        expected = {
            key: evidence[key]
            for key in (
                "decision_id",
                "decision_path",
                "decision_sha256",
                "review_path",
                "review_sha256",
                "selected_sha256",
            )
        }
        if not isinstance(manifest_evidence, dict) or any(
            manifest_evidence.get(key) != value for key, value in expected.items()
        ):
            findings.append(
                Finding(
                    "approval.manifest_evidence",
                    "Manifest decision evidence differs from request",
                    evidence["manifest"],
                )
            )
        if evidence["decision_path"] != f"decisions/{evidence['decision_id']}.json":
            findings.append(
                Finding(
                    "approval.decision_path",
                    "Decision path does not match decision ID",
                    evidence["decision_path"],
                )
            )
            return findings
        decision_file = contained_path(root, evidence["decision_path"])
        content = decision_file.read_bytes()
        if hashlib.sha256(content).hexdigest() != evidence["decision_sha256"]:
            findings.append(
                Finding(
                    "approval.decision_hash",
                    "Decision file changed",
                    evidence["decision_path"],
                )
            )
            return findings
        decision = json.loads(content)
        findings.extend(decision_findings(root, decision))
        if schema_findings(decision, "production-decision.schema.json"):
            return findings
        if (
            decision["decision_id"] != evidence["decision_id"]
            or decision["decision_type"] != "variant_selection"
            or decision["subject_path"] != path
            or decision["selected_sha256"] != ref["sha256"]
            or decision["selected_sha256"] != evidence["selected_sha256"]
            or decision["selected_variant"]
            != selected_manifest_value(metadata, evidence)
            or decision["review_path"] != evidence["review_path"]
            or decision["review_sha256"] != evidence["review_sha256"]
            or (
                isinstance(manifest_evidence, dict)
                and (
                    manifest_evidence.get("actor") != decision["actor"]
                    or manifest_evidence.get("approval_mode")
                    != decision["approval_mode"]
                )
            )
        ):
            findings.append(
                Finding(
                    "approval.decision_binding",
                    "Decision does not match the selected reference",
                    path,
                )
            )
    except (
        ValueError,
        TypeError,
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        YAMLError,
    ) as error:
        findings.append(Finding("approval.decision_binding", str(error), path))
    return findings


def legacy_approval_findings(root: Path, ref: dict[str, Any]) -> list[Finding]:
    evidence = ref["approval_evidence"]
    findings: list[Finding] = []
    if evidence["selected_sha256"] != ref["sha256"]:
        findings.append(
            Finding(
                "approval.selected_hash",
                "Legacy selection hash differs from reference",
                ref["path"],
            )
        )
    try:
        metadata = frontmatter(root, evidence["manifest"])
        if (
            evidence["field"] == "selected_variant"
            and metadata.get("status") != "approved"
        ):
            findings.append(
                Finding(
                    "approval.legacy_status",
                    "Legacy selection is not approved",
                    evidence["manifest"],
                )
            )
        selected = selected_manifest_value(metadata, evidence)
        audit_path = contained_path(root, evidence["audit_path"])
        audit_bytes = audit_path.read_bytes()
        if hashlib.sha256(audit_bytes).hexdigest() != evidence["audit_sha256"]:
            findings.append(
                Finding(
                    "approval.legacy_audit",
                    "Legacy audit log changed",
                    evidence["audit_path"],
                )
            )
        else:
            latest = None
            for line in audit_bytes.decode("utf-8").splitlines():
                event = json.loads(line)
                selections = event.get("selections", {})
                if (
                    isinstance(selections, dict)
                    and evidence["legacy_asset_id"] in selections
                ):
                    latest = selections[evidence["legacy_asset_id"]]
            if latest != selected:
                findings.append(
                    Finding(
                        "approval.legacy_audit",
                        "Legacy audit does not confirm the current selection",
                        evidence["audit_path"],
                    )
                )
    except (
        ValueError,
        TypeError,
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        YAMLError,
    ) as error:
        findings.append(
            Finding("approval.legacy_audit", str(error), evidence["audit_path"])
        )
    return findings


def reference_findings(
    root: Path, references: list[dict[str, Any]], prompt: str, schema_version: int = 1
) -> list[Finding]:
    findings: list[Finding] = []
    counters = {"Image": 0, "Video": 0, "Audio": 0}
    expected_bindings: list[str] = []
    for ref in references:
        path = ref["path"]
        if ref.get("control_only"):
            findings.append(
                Finding(
                    "references.control_only",
                    "Control-only assets are not eligible generation inputs",
                    path,
                )
            )
        try:
            target = contained_path(root, path)
        except ValueError as error:
            findings.append(Finding("path.containment", str(error), path))
            continue
        if hashlib.sha256(target.read_bytes()).hexdigest() != ref["sha256"]:
            findings.append(
                Finding("references.current_hashes", "Reference content changed", path)
            )
        if schema_version == 2:
            findings.extend(approval_decision_findings(root, ref, target))
        elif not approval_matches(root, ref, target):
            findings.append(
                Finding(
                    "approval.explicit_choice",
                    "Reference must match an explicit manifest selection",
                    path,
                )
            )
        media = (
            "Audio"
            if "audio" in ref["role"]
            else "Video"
            if "video" in ref["role"]
            else "Image"
        )
        counters[media] += 1
        expected = f"@{media} {counters[media]}"
        expected_bindings.append(ref["binding"])
        if ref["binding"] != expected or expected not in prompt:
            findings.append(
                Finding(
                    "references.ordered_bindings",
                    f"Expected bound input {expected}",
                    path,
                )
            )
    actual = set(re.findall(r"@(?:Image|Video|Audio) \d+\b", prompt))
    if actual != set(expected_bindings):
        findings.append(
            Finding(
                "references.ordered_bindings",
                "Prompt bindings and ordered inputs differ",
            )
        )
    return findings


def external_schema_references(value: Any) -> bool:
    if isinstance(value, dict):
        return any(
            (key in ("$ref", "$dynamicRef") and not str(child).startswith("#"))
            or external_schema_references(child)
            for key, child in value.items()
        )
    if isinstance(value, list):
        return any(external_schema_references(child) for child in value)
    return False


def capability_findings(request: dict[str, Any], evidence: Any) -> list[Finding]:
    malformed = schema_findings(evidence, "capability-evidence.schema.json")
    if malformed:
        return [
            Finding("model.supported_mode", finding.message) for finding in malformed
        ]
    if external_schema_references(evidence["parameters"]):
        return [
            Finding(
                "model.supported_mode",
                "Capability schemas must be self-contained; remote references are not loaded",
            )
        ]
    findings: list[Finding] = []
    if evidence.get("model") != request["model"] or request[
        "operation"
    ] not in evidence.get("operations", []):
        findings.append(
            Finding(
                "model.supported_mode",
                "Model or operation is absent from capability evidence",
            )
        )
    properties = evidence.get("parameters", {})
    if not isinstance(properties, dict):
        return [
            Finding(
                "model.supported_mode", "Parameter evidence must be a schema mapping"
            )
        ]
    schema = {
        "type": "object",
        "properties": properties,
        "additionalProperties": False,
        "required": evidence.get("required_parameters", []),
    }
    try:
        Draft202012Validator.check_schema(schema)
        for error in Draft202012Validator(schema).iter_errors(request["params"]):
            findings.append(Finding("model.supported_mode", error.message))
    except (SchemaError, TypeError, ValueError) as error:
        findings.append(
            Finding("model.supported_mode", f"Invalid capability schema: {error}")
        )
    roles = [ref["role"] for ref in request["references"]]
    if any(role not in evidence.get("reference_roles", []) for role in roles):
        findings.append(
            Finding("model.supported_mode", "Reference role is unsupported")
        )
    maximum = evidence.get("max_references", 0)
    if not isinstance(maximum, int) or len(roles) > maximum:
        findings.append(
            Finding(
                "model.supported_mode", "Reference count exceeds verified allowance"
            )
        )
    if (
        "reference_image" in roles
        and any(role in roles for role in ("first_frame", "last_frame"))
        and not evidence.get("supports_first_frame_with_reference_images", False)
    ):
        findings.append(
            Finding(
                "model.supported_mode",
                "Mixed frame and reference-image roles are not verified",
            )
        )
    return findings


def prepared_evidence_findings(project_root: Path, request: Any) -> list[Finding]:
    findings = schema_findings(request, "generation-request.schema.json")
    if findings:
        return findings
    root = Path(project_root).resolve()
    try:
        prompt_path = contained_path(root, request["prompt_file"])
        prompt_bytes = prompt_path.read_bytes()
        prompt_text = prompt_bytes.decode("utf-8")
    except (ValueError, OSError, UnicodeError) as error:
        return [Finding("path.containment", str(error), request["prompt_file"])]
    if hashlib.sha256(prompt_bytes).hexdigest() != request["prompt_sha256"]:
        findings.append(
            Finding(
                "prompt.current_hash",
                "Prompt snapshot content changed",
                request["prompt_file"],
            )
        )
    try:
        digest = compute_request_hash(
            prompt_bytes,
            request["references"],
            request["model"],
            request["operation"],
            request["params"],
            approval_mode=request.get("approval_mode"),
            project_sha256=request.get("project_sha256"),
        )
        if digest != request["request_sha256"]:
            findings.append(
                Finding(
                    "request.current_hash",
                    "Request content differs from the reviewed request",
                )
            )
    except (ValueError, TypeError) as error:
        findings.append(Finding("request.current_hash", str(error)))
    findings.extend(
        reference_findings(
            root, request["references"], prompt_text, request["schema_version"]
        )
    )
    findings.extend(project_mode_findings(root, request))
    if (
        request["submission_status"] != "prepared"
        or request["provider_task_id"] is not None
    ):
        findings.append(
            Finding(
                "submission.reconcile_unknown",
                "Existing or uncertain operations must reconcile rather than submit",
            )
        )
    return findings


def validate_request(
    project_root: Path, request: Any, capability_evidence: Any
) -> list[Finding]:
    findings = prepared_evidence_findings(project_root, request)
    if schema_findings(request, "generation-request.schema.json"):
        return findings
    findings.extend(capability_findings(request, capability_evidence))
    return findings


def validate_review(
    review: Any, request_hash: str, required_rule_ids: list[str]
) -> list[Finding]:
    findings = schema_findings(review, "review-result.schema.json")
    if findings:
        return findings
    if (
        review["request_sha256"] != request_hash
        or review["reviewer_status"] != "complete"
    ):
        findings.append(
            Finding(
                "review.complete_evidence",
                "Review is incomplete or belongs to another request",
            )
        )
    seen: set[str] = set()
    for check in review["checks"]:
        if check["rule_id"] in seen:
            findings.append(
                Finding("review.complete_evidence", "Duplicate rule result")
            )
        seen.add(check["rule_id"])
        if check["status"] == "fail" or not check["evidence"].strip():
            findings.append(
                Finding(check["rule_id"], "Failed check or missing evidence")
            )
        if (
            check["status"] == "not_applicable"
            and check["rule_id"] in required_rule_ids
        ):
            findings.append(
                Finding(
                    check["rule_id"], "Required applicable checks cannot be skipped"
                )
            )
    for missing in set(required_rule_ids) - seen:
        findings.append(
            Finding("review.complete_evidence", f"Missing required rule: {missing}")
        )
    return findings


def reconcile_operation(
    operation: dict[str, Any], provider_observation: dict[str, Any]
) -> RecoveryDecision:
    task_id = operation.get("provider_task_id") or provider_observation.get(
        "provider_task_id"
    )
    status = provider_observation.get("provider_status")
    if status == "succeeded":
        return RecoveryDecision(
            "download", task_id, "Recover the existing output; do not regenerate"
        )
    if status in ("failed", "cancelled", "expired", "moderation_rejected"):
        return RecoveryDecision(
            "review_failure",
            task_id,
            "Review failure evidence before authorizing a new operation",
        )
    if task_id:
        return RecoveryDecision("poll", task_id, "Resume the existing provider task")
    return RecoveryDecision(
        "hold",
        None,
        "Acceptance is unknown; reconcile or obtain an explicit retry decision",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only generation preflight; never calls a provider"
    )
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--capabilities", type=Path, required=True)
    parser.add_argument("--review", type=Path)
    parser.add_argument("--required-rule", action="append", default=[])
    args = parser.parse_args()
    try:
        request = json.loads(args.request.read_text())
        findings = validate_request(
            args.project, request, json.loads(args.capabilities.read_text())
        )
        if args.review:
            findings.extend(
                validate_review(
                    json.loads(args.review.read_text()),
                    request.get("request_sha256", ""),
                    args.required_rule,
                )
            )
        else:
            findings.append(
                Finding(
                    "review.complete_evidence",
                    "A completed review is required before submission",
                )
            )
    except (OSError, ValueError) as error:
        findings = [Finding("input.readable", str(error))]
    print(
        json.dumps(
            {"ok": not findings, "findings": [asdict(f) for f in findings]}, indent=2
        )
    )
    return int(bool(findings))


if __name__ == "__main__":
    raise SystemExit(main())
