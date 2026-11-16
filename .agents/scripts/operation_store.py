from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ruamel.yaml.error import YAMLError
from validate_request import (
    contained_path,
    parse_frontmatter,
    prepared_evidence_findings,
    project_mode_findings,
    request_review_findings,
    schema_findings,
    studio_project,
    validate_request,
)

TRANSITIONS = {
    "prepared": {"submitting"},
    "submitting": {"submission_unknown", "acknowledged", "terminal"},
    "submission_unknown": {"acknowledged", "terminal"},
    "acknowledged": {"acknowledged", "terminal"},
    "terminal": set(),
}

TERMINAL_PROVIDER_STATUSES = {
    "succeeded", "failed", "cancelled", "canceled", "expired", "moderation_rejected",
}


def require_provider_result(
    provider_task_id: str | None, provider_status: str | None, terminal: bool
) -> None:
    if not isinstance(provider_task_id, str) or not provider_task_id.strip():
        raise ValueError("Adopting or reconciling a job needs its provider task ID")
    if terminal and (
        not isinstance(provider_status, str)
        or provider_status not in TERMINAL_PROVIDER_STATUSES
    ):
        raise ValueError(
            "A terminal job requires an explicit definitive provider status: "
            + ", ".join(sorted(TERMINAL_PROVIDER_STATUSES))
            + "; completed or unknown is not a provider result"
        )
    if not isinstance(provider_status, str) or not provider_status.strip():
        raise ValueError("Adopting a submitted job needs its provider status")


@contextmanager
def selection_lock(root: Path) -> Iterator[None]:
    path = root.resolve() / ".selection.lock"
    if path.is_symlink():
        raise ValueError("Selection lock must not be a symlink")
    descriptor = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(descriptor, "a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        yield


@contextmanager
def registry_lock(root: Path) -> Iterator[Path]:
    root = root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    lock = root / ".task_ids.lock"
    if lock.is_symlink():
        raise ValueError("Registry lock must not be a symlink")
    descriptor = os.open(lock, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(descriptor, "a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        registry = root / "task_ids.json"
        if registry.is_symlink():
            raise ValueError("Registry must not be a symlink")
        yield registry


def read_registry(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema_version": 1, "tasks": []}
    document = json.loads(path.read_text())
    findings = schema_findings(document, "task-registry.schema.json")
    if findings:
        raise ValueError(
            "Legacy or invalid registry requires an explicit migration preview; existing data was preserved"
        )
    identifiers = [record["operation_id"] for record in document["tasks"]]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("Duplicate operation identities in registry")
    return document


def replace_registry(path: Path, document: dict[str, Any]) -> None:
    descriptor, name = tempfile.mkstemp(
        prefix=".task_ids-", suffix=".tmp", dir=path.parent
    )
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "w") as handle:
            json.dump(document, handle, indent=2, allow_nan=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        temporary.unlink(missing_ok=True)


def require_current_approval_contract(root: Path, record: dict[str, Any]) -> None:
    version = record.get("schema_version")
    project_path = root / "project.md"
    if version == 1 and project_path.exists():
        try:
            content = project_path.read_text(encoding="utf-8")
            metadata = parse_frontmatter(content) if content.startswith("---") else {}
        except (OSError, UnicodeError, ValueError, TypeError, YAMLError) as error:
            raise ValueError(f"Cannot verify legacy project mode: {error}") from error
        if any(field in metadata for field in ("approval_mode", "review_mode")):
            raise ValueError(
                "Explicit approval or review mode requires a version-2 generation request"
            )
    path = root / "showcase.json"
    if path.is_symlink():
        raise ValueError("Production canvas must not be a symlink")
    if not path.exists():
        if version == 2 and not studio_project(root):
            raise ValueError(
                "Version-2 generation requires a Studio project (a real studio/ "
                "directory and no showcase.json) or a pre-Studio canvas "
                "(showcase.json and current index.html)"
            )
        return
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"Invalid production canvas showcase.json: {error}") from error
    if not isinstance(document, dict):
        raise TypeError("Production canvas must be a JSON object")
    canvas = document.get("canvas")
    if (
        version == 1
        and isinstance(canvas, dict)
        and "approvalContractVersion" in canvas
    ):
        raise ValueError(
            "Versioned production canvas requires a version-2 generation request"
        )
    if version != 2:
        return
    if not isinstance(canvas, dict) or canvas.get("approvalContractVersion") != 1:
        raise ValueError("Version-2 generation requires a versioned production canvas")
    stage = canvas.get("currentStage")
    if not isinstance(stage, str) or not stage:
        raise ValueError("Production canvas requires a current stage")
    index_path = root / "index.html"
    if index_path.is_symlink():
        raise ValueError("Generated production canvas must not be a symlink")
    generator = (
        Path(__file__).resolve().parents[1]
        / "skills/showcase-html/scripts/generate_showcase.py"
    )
    result = subprocess.run(
        [sys.executable, str(generator), str(root), "--check", "--stage", stage],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stdout + result.stderr).strip()
        raise ValueError(f"Production canvas checkpoint failed: {detail}")


def prepare_operation(
    root: Path,
    request: dict[str, Any],
    capabilities: dict[str, Any],
    review: dict[str, Any] | None,
    required_rule_ids: list[str],
    allow_board_references: bool = False,
    *,
    existing_submission: bool = False,
) -> None:
    findings = validate_request(
        root,
        request,
        capabilities,
        allow_board_references,
        existing_submission=existing_submission,
    )
    findings.extend(
        request_review_findings(
            root, review, request.get("request_sha256", ""), required_rule_ids
        )
    )
    if findings:
        raise ValueError("; ".join(finding.message for finding in findings))
    with selection_lock(root), registry_lock(root) as path:
        mode_findings = project_mode_findings(root, request)
        mode_findings.extend(
            request_review_findings(
                root, review, request.get("request_sha256", ""), required_rule_ids
            )
        )
        if mode_findings:
            raise ValueError("; ".join(finding.message for finding in mode_findings))
        require_current_approval_contract(root, request)
        registry = read_registry(path)
        if any(
            record["operation_id"] == request["operation_id"]
            or record["asset_id"] == request["asset_id"]
            for record in registry["tasks"]
        ):
            raise ValueError(
                "Operation or asset identity already exists; reconcile or use an explicitly authorized new take"
            )
        registry["tasks"].append(deepcopy(request))
        replace_registry(path, registry)


def adopt_submitted_operation(
    root: Path,
    request: dict[str, Any],
    capabilities: dict[str, Any],
    review: dict[str, Any] | None,
    required_rule_ids: list[str],
    provider_task_id: str,
    provider_status: str,
    terminal: bool,
) -> None:
    require_provider_result(provider_task_id, provider_status, terminal)
    prepare_operation(
        root,
        request,
        capabilities,
        review,
        required_rule_ids,
        allow_board_references=True,
        existing_submission=True,
    )
    operation_id = request["operation_id"]
    try:
        transition_operation(
            root,
            operation_id,
            "prepared",
            "submitting",
            allow_board_references=True,
            existing_submission=True,
        )
        transition_operation(
            root,
            operation_id,
            "submitting",
            "acknowledged",
            provider_task_id=provider_task_id,
            provider_status=provider_status,
        )
        if terminal:
            transition_operation(
                root,
                operation_id,
                "acknowledged",
                "terminal",
                provider_status=provider_status,
            )
    except ValueError as error:
        raise ValueError(
            f"{operation_id} is registered but adoption stopped part-way ({error}); "
            "inspect task_ids.json and finish the transitions for the known "
            f"provider task {provider_task_id}, never resubmit; a request that "
            "references a storyboard file needs allow_board_references=True"
        ) from error


def reconcile_terminal_operation(
    root: Path,
    operation_id: str,
    expected_request_sha256: str,
    provider_result: str,
) -> None:
    if (
        not provider_result
        or Path(provider_result).is_absolute()
        or ".." in Path(provider_result).parts
    ):
        raise ValueError("Provider result must be a project-relative evidence file")
    with selection_lock(root), registry_lock(root) as path:
        registry = read_registry(path)
        record = next(
            (item for item in registry["tasks"] if item["operation_id"] == operation_id),
            None,
        )
        if (
            record is None
            or record["submission_status"] != "terminal"
            or record["provider_status"] != "completed"
            or record["request_sha256"] != expected_request_sha256
        ):
            raise ValueError(
                "Operation missing or stale: correction requires terminal/completed "
                "and the exact frozen request hash; never resubmit"
            )
        extensions = record.setdefault("extensions", {})
        if "terminal_reconciliation" in extensions:
            raise ValueError("An existing terminal reconciliation cannot be replaced")
        evidence_bytes = contained_path(root, provider_result).read_bytes()
        evidence = json.loads(evidence_bytes)
        if not isinstance(evidence, dict):
            raise TypeError("Provider result must be a task object with task_id and status")
        task_id, status = evidence.get("task_id"), evidence.get("status")
        require_provider_result(task_id, status, True)
        if task_id != record["provider_task_id"]:
            raise ValueError("Provider result task identity does not match the operation")
        extensions["terminal_reconciliation"] = {
            "previous_provider_status": record["provider_status"],
            "provider_status": status,
            "provider_task_id": task_id,
            "request_sha256": record["request_sha256"],
            "evidence_path": provider_result,
            "evidence_sha256": hashlib.sha256(evidence_bytes).hexdigest(),
            "reconciled_at": datetime.now(UTC).isoformat(),
        }
        record["provider_status"] = status
        replace_registry(path, registry)


def transition_operation(
    root: Path,
    operation_id: str,
    expected_status: str,
    new_status: str,
    provider_task_id: str | None = None,
    provider_status: str | None = None,
    allow_board_references: bool = False,
    *,
    existing_submission: bool = False,
) -> None:
    if new_status not in TRANSITIONS.get(expected_status, set()):
        raise ValueError(
            "Invalid operation transition; unknown acceptance cannot become a new submission"
        )
    with selection_lock(root), registry_lock(root) as path:
        registry = read_registry(path)
        record = next(
            (
                item
                for item in registry["tasks"]
                if item["operation_id"] == operation_id
            ),
            None,
        )
        if record is None or record["submission_status"] != expected_status:
            raise ValueError("Operation missing or stale expected state")
        if new_status == "submitting":
            evidence_findings = prepared_evidence_findings(
                root,
                record,
                allow_board_references,
                existing_submission=existing_submission,
            )
            if evidence_findings:
                raise ValueError(
                    "; ".join(finding.message for finding in evidence_findings)
                )
            require_current_approval_contract(root, record)
        if provider_task_id and record["provider_task_id"] not in (
            None,
            provider_task_id,
        ):
            raise ValueError("A provider task identity cannot be replaced")
        record["submission_status"] = new_status
        if provider_task_id is not None:
            record["provider_task_id"] = provider_task_id
        if provider_status is not None:
            record["provider_status"] = provider_status
        if schema_findings(record, "generation-request.schema.json"):
            raise ValueError("Transition requires a valid provider acknowledgment")
        replace_registry(path, registry)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Reconcile saved provider evidence; never calls a provider"
    )
    commands = parser.add_subparsers(dest="command", required=True)
    reconcile = commands.add_parser("reconcile-terminal")
    reconcile.add_argument("--project", type=Path, required=True)
    reconcile.add_argument("--operation-id", required=True)
    reconcile.add_argument("--expected-request-sha256", required=True)
    reconcile.add_argument("--provider-result", required=True)
    args = parser.parse_args(argv)
    try:
        reconcile_terminal_operation(
            args.project.resolve(), args.operation_id,
            args.expected_request_sha256, args.provider_result,
        )
    except (OSError, ValueError, TypeError) as error:
        print(json.dumps({"ok": False, "error": str(error)}))
        return 1
    print(json.dumps({"ok": True, "operation_id": args.operation_id}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
