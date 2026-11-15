from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.parse import unquote

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError


@dataclass(frozen=True)
class Finding:
    rule_id: str
    path: str
    message: str
    line: int = 0
    severity: str = "error"


def validate_skill(path: Path) -> tuple[dict[str, Any], list[Finding]]:
    findings: list[Finding] = []
    text = path.read_text()
    match = re.match(r"\A---\s*\n(.*?)\n---(?:\n|$)", text, re.DOTALL)
    if not match:
        return {}, [Finding("metadata.yaml", str(path), "Missing frontmatter")]
    try:
        metadata = YAML(typ="safe").load(match.group(1))
    except YAMLError as error:
        return {}, [Finding("metadata.yaml", str(path), str(error), 2)]
    if not isinstance(metadata, dict):
        return {}, [
            Finding("metadata.yaml", str(path), "Frontmatter must be a mapping")
        ]
    name = metadata.get("name", "")
    if name in ("seedance-prompt-20", "seedance-prompt-25"):
        findings.append(
            Finding(
                "metadata.retired",
                str(path),
                "Retired versioned prompt skill; use seedance-prompt",
            )
        )
    if (
        not isinstance(name, str)
        or name != path.parent.name
        or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
        or len(name) > 64
    ):
        findings.append(
            Finding(
                "metadata.name",
                str(path),
                "Name must match its directory and the skill naming format",
            )
        )
    description = metadata.get("description")
    if (
        not isinstance(description, str)
        or not description.strip()
        or len(description) > 1024
    ):
        findings.append(
            Finding(
                "metadata.description",
                str(path),
                "Description must be 1-1024 characters",
            )
        )
    return metadata, findings


def prose_lines(path: Path) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    fence = False
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
        elif not fence:
            result.append((number, line))
    return result


def validate_links(
    root: Path, documents: list[Path], portable_files: set[str]
) -> list[Finding]:
    findings: list[Finding] = []
    for document in documents:
        for number, line in prose_lines(document):
            for raw in re.findall(r"\]\(([^)]+)\)", line):
                if "://" in raw or raw.startswith(("#", "mailto:")):
                    continue
                relative = unquote(raw.split("#")[0].strip("<>"))
                if not relative or any(token in relative for token in ("<", ">", "*")):
                    continue
                target = (document.parent / relative).resolve()
                if not target.is_relative_to(root.resolve()):
                    findings.append(
                        Finding(
                            "links.contained",
                            str(document),
                            f"External filesystem reference: {relative}",
                            number,
                        )
                    )
                elif not target.exists():
                    findings.append(
                        Finding(
                            "links.exists",
                            str(document),
                            f"Missing runtime reference: {relative}",
                            number,
                        )
                    )
                elif (
                    target.is_file()
                    and str(target.relative_to(root.resolve())) not in portable_files
                ):
                    findings.append(
                        Finding(
                            "links.portable",
                            str(document),
                            f"Runtime reference absent from tracked inventory: {relative}",
                            number,
                        )
                    )
    return findings


def load_evaluations(path: Path) -> list[dict[str, Any]]:
    document = json.loads(path.read_text())
    if not isinstance(document, dict) or not isinstance(document.get("evals"), list):
        raise TypeError("Expected an evals list")
    cases: list[dict[str, Any]] = []
    ids: set[Any] = set()
    for case in document["evals"]:
        if (
            not isinstance(case, dict)
            or not isinstance(case.get("prompt"), str)
            or not case["prompt"].strip()
        ):
            raise ValueError("Each evaluation needs a nonempty prompt")
        identifier = case.get("id")
        if not isinstance(identifier, (str, int)) or identifier in ids:
            raise ValueError("Evaluation IDs must be unique strings or integers")
        ids.add(identifier)
        assertions = case.get("assertions", case.get("expectations", []))
        if not isinstance(assertions, list):
            raise TypeError("Assertions must be a list")
        cases.append(dict(case, assertions=assertions))
    return cases


def installed_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in (root / ".agents/skills").rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.name != ".DS_Store"
        and path.suffix != ".pyc"
    )


def bundle_hashes(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in installed_files(root)
    }


def read_inventory(root: Path, inventory: Path | None) -> set[str]:
    if inventory:
        value = json.loads(inventory.read_text())
        if not isinstance(value, list) or not all(
            isinstance(item, str) for item in value
        ):
            raise ValueError(
                "Inventory must be a JSON list of repository-relative files"
            )
        return set(value)
    output = subprocess.check_output(["git", "ls-files", "-z"], cwd=root)
    return set(output.decode().strip("\x00").split("\x00"))


def validate_workspace(
    root: Path, portable_files: set[str]
) -> tuple[dict[str, int], list[Finding]]:
    findings: list[Finding] = []
    skills = sorted((root / ".agents/skills").glob("*/SKILL.md"))
    lock = json.loads((root / "skills-lock.json").read_text())["skills"]
    catalog = json.loads((root / ".agents/catalog/skills.json").read_text())["skills"]
    known = {path.parent.name for path in skills}
    if known != set(lock) or known != set(catalog):
        findings.append(
            Finding(
                "catalog.coverage",
                "skills-lock.json",
                "Installed, lock and catalog skill names differ",
            )
        )
    readme = (root / "README.md").read_text()
    eval_count = 0
    for path in skills:
        name = path.parent.name
        metadata, problems = validate_skill(path)
        findings.extend(problems)
        if lock.get(name, {}).get("sourceType") == "local" and hashlib.sha256(
            path.read_bytes()
        ).hexdigest() != lock[name].get("computedHash"):
            findings.append(
                Finding(
                    "lock.current_hash",
                    str(path),
                    "Local entry hash differs from reviewed lock",
                )
            )
        if str(path.relative_to(root)) not in portable_files:
            findings.append(
                Finding(
                    "catalog.portable",
                    str(path),
                    "Installed skill absent from tracked inventory",
                )
            )
        if (
            len(
                re.findall(
                    r"^\| \*\*" + re.escape(name) + r"\*\* \|", readme, re.MULTILINE
                )
            )
            != 1
        ):
            findings.append(
                Finding(
                    "readme.coverage",
                    "README.md",
                    f"{name} must appear in exactly one skill row",
                )
            )
        if (
            catalog.get(name, {}).get("description")
            != metadata.get("description", "").strip()
        ):
            findings.append(
                Finding(
                    "catalog.description",
                    str(path),
                    "Catalog metadata differs from skill",
                )
            )
        if catalog.get(name, {}).get("kind") not in (
            "leaf",
            "orchestrator",
            "tooling",
            "vendored",
        ):
            findings.append(
                Finding("catalog.kind", str(path), "Missing skill classification")
            )
        if (
            lock.get(name, {}).get("sourceType") == "local"
            and len(path.read_text().splitlines()) > 500
        ):
            findings.append(
                Finding(
                    "size.entrypoint",
                    str(path),
                    "Consider loading conditional material on demand",
                    severity="warning",
                )
            )
        eval_path = path.parent / "evals/evals.json"
        if eval_path.exists():
            try:
                eval_count += len(load_evaluations(eval_path))
            except (ValueError, TypeError) as error:
                findings.append(Finding("evals.shape", str(eval_path), str(error)))
    integrity_path = root / ".agents/catalog/integrity.json"
    recorded = json.loads(integrity_path.read_text())["files"]
    current = bundle_hashes(root)
    for relative_path in sorted(set(recorded) | set(current)):
        if recorded.get(relative_path) != current.get(relative_path):
            findings.append(
                Finding(
                    "bundle.integrity",
                    relative_path,
                    "Bundle file differs from reviewed integrity inventory",
                )
            )
    documents = [
        root / "AGENTS.md",
        root / "README.md",
        *(root / ".agents/contracts").rglob("*.md"),
        *(root / ".agents/skills").rglob("*.md"),
    ]
    findings.extend(validate_links(root, documents, portable_files))
    for schema_path in (root / ".agents/contracts/schemas").glob("*.json"):
        try:
            Draft202012Validator.check_schema(json.loads(schema_path.read_text()))
        except (SchemaError, TypeError, ValueError) as error:
            findings.append(Finding("schema.valid", str(schema_path), str(error)))
    rules = json.loads((root / ".agents/contracts/rules.json").read_text())["rules"]
    rule_ids = [rule["id"] for rule in rules]
    if len(set(rule_ids)) != len(rule_ids):
        findings.append(
            Finding(
                "rules.unique",
                ".agents/contracts/rules.json",
                "Duplicate rule identifiers",
            )
        )
    for rule in rules:
        if rule["owner_path"] not in portable_files:
            findings.append(
                Finding(
                    "rules.owner",
                    rule["owner_path"],
                    "Rule owner absent from tracked inventory",
                )
            )
    return {
        "skills": len(skills),
        "evaluation_cases": eval_count,
        "bundle_files": len(current),
    }, findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Offline, read-only workspace validation"
    )
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[2]
    )
    parser.add_argument("--offline", action="store_true")
    parser.add_argument(
        "--inventory",
        type=Path,
        help="Prospective tracked-file JSON list for uncommitted work",
    )
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        stats, findings = validate_workspace(root, read_inventory(root, args.inventory))
    except (
        ValueError,
        OSError,
        KeyError,
        TypeError,
        subprocess.CalledProcessError,
    ) as error:
        stats, findings = {}, [Finding("input.readable", str(args.root), str(error))]
    failed = any(finding.severity == "error" for finding in findings)
    print(
        json.dumps(
            {
                "ok": not failed,
                "stats": stats,
                "findings": [asdict(finding) for finding in findings],
            },
            indent=2,
        )
    )
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
