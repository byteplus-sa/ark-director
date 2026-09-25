from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import re
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
validation = importlib.import_module("validate_request")

ASSET_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")


def json_objects(text: str) -> list[dict[str, Any]]:
    decoder = json.JSONDecoder()
    objects: list[dict[str, Any]] = []
    index = text.find("{")
    while index != -1:
        try:
            value, end = decoder.raw_decode(text, index)
        except ValueError:
            index = text.find("{", index + 1)
            continue
        if isinstance(value, dict):
            objects.append(value)
        index = text.find("{", end)
    return objects


def extract_review(text: str, request_hash: str) -> dict[str, Any]:
    candidates = [
        value
        for value in json_objects(text)
        if "request_sha256" in value and "checks" in value
    ]
    if not candidates:
        raise ValueError("No review JSON object with request_sha256 and checks found")
    matching = [
        value for value in candidates if value["request_sha256"] == request_hash
    ]
    if not matching:
        raise ValueError("No review JSON object matches the request hash")
    if any(value != matching[0] for value in matching[1:]):
        raise ValueError("Multiple different review objects match the request hash")
    return matching[0]


def request_identity(root: Path, relative: str) -> tuple[str, str]:
    request = json.loads(validation.contained_path(root, relative).read_text())
    malformed = validation.schema_findings(request, "generation-request.schema.json")
    if malformed:
        raise ValueError(f"Invalid request: {malformed[0].message}")
    prompt_bytes = validation.contained_path(root, request["prompt_file"]).read_bytes()
    digest = validation.compute_request_hash(
        prompt_bytes,
        request["references"],
        request["model"],
        request["operation"],
        request["params"],
        approval_mode=request.get("approval_mode"),
        project_sha256=request.get("project_sha256"),
    )
    if digest != request["request_sha256"]:
        raise ValueError("Request file is stale; its request_sha256 no longer matches")
    return request["asset_id"], request["request_sha256"]


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


def run(args: argparse.Namespace) -> tuple[dict[str, Any], list[Any]]:
    root = args.project.resolve()
    if not root.is_dir():
        raise ValueError("Project directory does not exist")
    if args.request:
        asset, request_hash = request_identity(root, args.request)
    else:
        asset, request_hash = args.asset, args.request_sha256
    if not ASSET_PATTERN.fullmatch(asset):
        raise ValueError("Asset ID must contain only letters, digits, _ and -")
    if not HASH_PATTERN.fullmatch(request_hash):
        raise ValueError("Request hash must be 64 lowercase hexadecimal characters")
    text = sys.stdin.read() if args.input == "-" else Path(args.input).read_text()
    review = extract_review(text, request_hash)
    findings = validation.validate_review(review, request_hash, args.required_rule)
    result: dict[str, Any] = {"request_sha256": request_hash, "asset_id": asset}
    if findings or not args.write:
        result["review"] = review
        return result, findings
    content = json.dumps(review, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    path = write_once(root, f"reviews/review_{asset}.json", content)
    result["path"] = path.relative_to(root).as_posix()
    result["review_sha256"] = hashlib.sha256(content.encode()).hexdigest()
    return result, findings


def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract, validate and record a prompt-review result"
    )
    parser.add_argument("--project", type=Path, required=True)
    identity = parser.add_mutually_exclusive_group(required=True)
    identity.add_argument("--request")
    identity.add_argument("--request-sha256")
    parser.add_argument("--asset")
    parser.add_argument("--input", required=True)
    parser.add_argument("--required-rule", action="append", default=[])
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    cli = parser()
    args = cli.parse_args(argv)
    if args.request_sha256 and not args.asset:
        cli.error("--request-sha256 requires --asset")
    if args.request and args.asset:
        cli.error("--asset is read from --request")
    try:
        result, findings = run(args)
    except (OSError, ValueError, TypeError, UnicodeError) as error:
        result, findings = {}, [validation.Finding("input.readable", str(error))]
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
