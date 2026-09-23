from __future__ import annotations

import fcntl
import json
import os
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from typing import Any

from validate_request import (
    prepared_evidence_findings,
    project_mode_findings,
    schema_findings,
    validate_request,
    validate_review,
)

TRANSITIONS = {
    "prepared": {"submitting"},
    "submitting": {"submission_unknown", "acknowledged", "terminal"},
    "submission_unknown": {"acknowledged", "terminal"},
    "acknowledged": {"acknowledged", "terminal"},
    "terminal": set(),
}


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
    path = root / "showcase.json"
    if not path.exists():
        return
    if path.is_symlink():
        raise ValueError("Production canvas must not be a symlink")
    document = json.loads(path.read_text())
    if not isinstance(document, dict):
        raise TypeError("Production canvas must be a JSON object")
    canvas = document.get("canvas")
    if isinstance(canvas, dict) and canvas.get("approvalContractVersion") == 1 and record.get("schema_version") != 2:
        raise ValueError("Versioned production canvas requires a version-2 generation request")


def prepare_operation(
    root: Path,
    request: dict[str, Any],
    capabilities: dict[str, Any],
    review: dict[str, Any],
    required_rule_ids: list[str],
) -> None:
    findings = validate_request(root, request, capabilities)
    findings.extend(
        validate_review(review, request.get("request_sha256", ""), required_rule_ids)
    )
    if findings:
        raise ValueError("; ".join(finding.message for finding in findings))
    with selection_lock(root), registry_lock(root) as path:
        require_current_approval_contract(root, request)
        mode_findings = project_mode_findings(root, request)
        if mode_findings:
            raise ValueError("; ".join(finding.message for finding in mode_findings))
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


def transition_operation(
    root: Path,
    operation_id: str,
    expected_status: str,
    new_status: str,
    provider_task_id: str | None = None,
    provider_status: str | None = None,
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
            require_current_approval_contract(root, record)
            evidence_findings = prepared_evidence_findings(root, record)
            if evidence_findings:
                raise ValueError(
                    "; ".join(finding.message for finding in evidence_findings)
                )
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
