"""Record stage reviews and locks, and move the production canvas between stages.

Subcommands:
  review   write a schema-valid candidate review for an artifact
  lock     record a picture, audio, or final_master stage lock
  reopen   return the canvas to an earlier stage for a revision
  advance  close the current stage and activate the next one

Every command validates before writing and refreshes index.html afterwards.
"""
from __future__ import annotations

import argparse
import copy
import datetime
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate_showcase import CANVAS_STAGE_IDS, canvas_validation_errors
from selection_service import (
    STAGE_LOCKS,
    SelectionError,
    commit_targets,
    contained_path,
    read_project_mode,
    record_stage_decision,
    recover_selection,
    sha256,
    validate_schema,
    writer_lock,
)

GENERATOR = Path(__file__).resolve().parent / "generate_showcase.py"
VIDEO_SUFFIXES = {".mp4", ".mov", ".mkv", ".webm"}
AUDIO_SUFFIXES = {".wav", ".mp3", ".m4a", ".aac", ".flac"}
CHECK_STATUSES = {"pass", "fail", "incomplete", "not_applicable"}


def now() -> str:
    return datetime.datetime.now(datetime.UTC).isoformat()


def load_showcase(root: Path) -> dict[str, Any]:
    return json.loads(contained_path(root, "showcase.json").read_text())


def dump(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n"


def refresh_html(root: Path, stage: str) -> None:
    subprocess.run(
        [sys.executable, str(GENERATOR), str(root), "--stage", stage],
        check=True,
        capture_output=True,
        text=True,
    )


def evidence_problem(artifact: str, method: str) -> str | None:
    suffix = Path(artifact).suffix.lower()
    lowered = method.lower()
    if suffix in VIDEO_SUFFIXES and not any(word in lowered for word in ("playback", "temporal")):
        return "video review needs temporal or playback evidence in --method"
    if suffix in AUDIO_SUFFIXES and "listen" not in lowered:
        return "audio review needs listening evidence in --method"
    return None


def parse_check(text: str) -> dict[str, str]:
    criterion, separator, rest = text.partition("=")
    status, separator_two, evidence = rest.partition(":")
    status = status.strip()
    if not separator or not separator_two or not criterion.strip() or not evidence.strip():
        raise SelectionError(f"--check must look like 'criterion=pass: evidence', got {text!r}")
    if status not in CHECK_STATUSES:
        raise SelectionError(f"--check status must be one of {sorted(CHECK_STATUSES)}")
    return {"criterion": criterion.strip(), "status": status, "evidence": evidence.strip()}


def build_review(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    problem = evidence_problem(args.artifact, args.method)
    if problem:
        raise SelectionError(problem)
    checks = [parse_check(item) for item in args.check]
    failing = [check["criterion"] for check in checks if check["status"] not in {"pass", "not_applicable"}]
    status = "pass" if checks and not failing else "fail"
    review = {
        "schema_version": 1,
        "artifact_path": args.artifact,
        "artifact_sha256": sha256(contained_path(root, args.artifact)),
        "status": status,
        "inspection_method": args.method,
        "coverage": args.coverage,
        "checks": checks,
        "observations": args.observation,
        "limitations": args.limitation,
        "recommendation": args.recommendation,
    }
    validate_schema(review, "candidate-review.schema.json")
    return review


def command_review(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    review = build_review(root, args)
    out = contained_path(root, args.out, must_exist=False)
    if out.exists() and not args.replace:
        raise SelectionError(f"{args.out} exists; pass --replace to overwrite an unused review")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(dump(review))
    return {"ok": review["status"] == "pass", "review": args.out, "status": review["status"], "sha256": sha256(out)}


def build_lock(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    mode = read_project_mode(root)
    if mode["project_sha256"] is None:
        raise SelectionError("project.md is required before recording a lock")
    stem = Path(args.artifact).stem
    decision: dict[str, Any] = {
        "schema_version": 1,
        "decision_id": args.decision_id or f"lock_{args.kind}_{stem}",
        "decision_type": "stage_lock",
        "stage_id": STAGE_LOCKS[args.kind],
        "lock_kind": args.kind,
        "subject_path": args.artifact,
        "subject_sha256": sha256(contained_path(root, args.artifact)),
        "actor": args.actor,
        "approval_mode": mode["mode"],
        "project_sha256": mode["project_sha256"],
        "result": "approved",
        "review_path": args.review,
        "review_sha256": sha256(contained_path(root, args.review)),
        "upstream_sha256": {path: sha256(contained_path(root, path)) for path in args.upstream},
        "reason": args.reason,
        "decided_at": now(),
    }
    if args.actor == "user":
        if not args.authorization:
            raise SelectionError("a user lock needs --authorization with the user's chat approval")
        decision["authorization"] = {"source": "chat", "evidence": args.authorization}
    validate_schema(decision, "production-decision.schema.json")
    return decision


def command_lock(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    decision = build_lock(root, args)
    result = record_stage_decision(root, decision)
    refresh_html(root, decision["stage_id"])
    return result


def next_stage(stages: list[dict[str, Any]], index: int) -> int | None:
    for candidate in range(index + 1, len(stages)):
        if stages[candidate].get("status") != "skipped":
            return candidate
    return None


def command_advance(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    with writer_lock(root):
        recover_selection(root)
        showcase = load_showcase(root)
        canvas = showcase["canvas"]
        current = CANVAS_STAGE_IDS.index(canvas["currentStage"])
        if args.stage and args.stage != canvas["currentStage"]:
            raise SelectionError(f"current stage is {canvas['currentStage']}, not {args.stage}")
        updated = copy.deepcopy(showcase)
        stage_list = updated["canvas"]["stages"]
        stage_list[current]["status"] = args.status
        following = next_stage(stage_list, current)
        if following is not None:
            activated = stage_list[following]
            activated["status"] = "active"
            updated["canvas"]["currentStage"] = activated["id"]
            sources = activated.setdefault("sources", [])
            known = {source.get("path") for source in sources if isinstance(source, dict)}
            for item in args.source:
                relative, _, kind = item.partition(":")
                contained_path(root, relative)
                if relative not in known:
                    sources.append({"path": relative, "kind": kind or "data"})
                    known.add(relative)
        errors = canvas_validation_errors(updated, root)
        empty = f"{updated['canvas']['currentStage']}: progressed stage requires a source or section"
        errors = [
            f"{updated['canvas']['currentStage']} has no sources yet; pass --source PATH[:kind] for its first input"
            if error == empty else error
            for error in errors
        ]
        if errors:
            raise SelectionError("cannot advance: " + "; ".join(errors))
        commit_targets(root, {"showcase.json": dump(updated)})
    refresh_html(root, updated["canvas"]["currentStage"])
    return {"ok": True, "completed": CANVAS_STAGE_IDS[current], "currentStage": updated["canvas"]["currentStage"]}


def command_reopen(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    with writer_lock(root):
        recover_selection(root)
        showcase = load_showcase(root)
        canvas = showcase["canvas"]
        stages = canvas["stages"]
        target = CANVAS_STAGE_IDS.index(args.stage)
        current = CANVAS_STAGE_IDS.index(canvas["currentStage"])
        if target > current:
            raise SelectionError(f"{args.stage} is after the current stage {canvas['currentStage']}; use advance")
        reopened_at = now()
        superseded = []
        for index in range(target, len(stages)):
            stage = stages[index]
            if index > target and stage.get("status") != "skipped":
                stage["status"] = "pending"
            locks = stage.pop("locks", None)
            if locks:
                history = stage.setdefault("supersededLocks", [])
                history.append({"reopened_at": reopened_at, "reason": args.reason, "locks": locks})
                superseded.append(stage["id"])
        stages[target]["status"] = "active"
        canvas["currentStage"] = args.stage
        log_path = contained_path(root, "selection.log", must_exist=False)
        log = log_path.read_text() if log_path.exists() else ""
        event = {
            "ts": reopened_at,
            "event": "reopen_stage",
            "stage": args.stage,
            "previous_stage": CANVAS_STAGE_IDS[current],
            "actor": args.actor,
            "reason": args.reason,
            "superseded_locks": superseded,
        }
        commit_targets(root, {"showcase.json": dump(showcase), "selection.log": log + json.dumps(event) + "\n"})
    refresh_html(root, args.stage)
    return {"ok": True, "currentStage": args.stage, "superseded_locks": superseded}


def parser() -> argparse.ArgumentParser:
    main = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = main.add_subparsers(dest="command", required=True)

    review = commands.add_parser("review", help="write a candidate review")
    review.add_argument("project")
    review.add_argument("--artifact", required=True)
    review.add_argument("--out", required=True)
    review.add_argument("--method", required=True, help="how it was inspected; video needs playback/temporal, audio needs listening")
    review.add_argument("--coverage", required=True)
    review.add_argument("--check", action="append", default=[], required=True, help="criterion=pass: evidence")
    review.add_argument("--observation", action="append", default=[], required=True)
    review.add_argument("--limitation", action="append", default=[])
    review.add_argument("--recommendation", required=True)
    review.add_argument("--replace", action="store_true")

    lock = commands.add_parser("lock", help="record a stage lock")
    lock.add_argument("project")
    lock.add_argument("--kind", required=True, choices=sorted(STAGE_LOCKS))
    lock.add_argument("--artifact", required=True)
    lock.add_argument("--review", required=True)
    lock.add_argument("--reason", required=True)
    lock.add_argument("--upstream", action="append", default=[])
    lock.add_argument("--decision-id")
    lock.add_argument("--actor", choices=["agent", "user"], default="agent")
    lock.add_argument("--authorization", help="the user's approval, quoted from chat (user locks only)")

    reopen = commands.add_parser("reopen", help="return to an earlier stage for a revision")
    reopen.add_argument("project")
    reopen.add_argument("--stage", required=True, choices=CANVAS_STAGE_IDS)
    reopen.add_argument("--reason", required=True)
    reopen.add_argument("--actor", choices=["agent", "user"], default="agent")

    advance = commands.add_parser("advance", help="close the current stage")
    advance.add_argument("project")
    advance.add_argument("--stage", choices=CANVAS_STAGE_IDS, help="assert the stage being closed")
    advance.add_argument("--status", choices=["complete", "approved"], default="complete")
    advance.add_argument("--source", action="append", default=[], help="PATH[:kind] to attach to the stage being activated")
    return main


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    root = Path(args.project).resolve()
    handlers = {"review": command_review, "lock": command_lock, "reopen": command_reopen, "advance": command_advance}
    try:
        result = handlers[args.command](root, args)
    except (SelectionError, OSError, subprocess.CalledProcessError) as error:
        print(json.dumps({"ok": False, "error": str(error)}), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0 if result.get("ok", True) else 1


if __name__ == "__main__":
    sys.exit(main())
