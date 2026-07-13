#!/usr/bin/env python3
"""Compile, approve, check, and execute OPC black-box testcase manifests.

The human-readable ``testcases.md`` is product truth. ``testcases.json`` is a deterministic
machine compilation of that truth. A build may start only after an approved demo, an approved
PRD, an independently reviewed testcase manifest, and explicit product-owner approval all remain
fresh. E2E runners emit ``opc-case-evidence-v1``; this helper validates that evidence instead of
trusting caller-supplied claims about driver, assembly, data, provider, or observation quality.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from validate_artifacts import (
    AC_REF_RE,
    TC_HEADER_RE,
    check_prd,
    check_testcases,
)

MANIFEST_SCHEMA = "opc-testcases-v1"
APPROVAL_SCHEMA = "opc-testcase-approval-v1"
EVIDENCE_SCHEMA = "opc-case-evidence-v1"
STATUS_RE = re.compile(r"^\*\*Status:\*\*\s+(Approved|Issues Found)\s*$", re.M)
REVIEWED_RE = re.compile(
    r"^Reviewed-SHA:\s+(?P<path>\S+)\s+(?P<sha>[0-9a-f]{7,64})\s*$", re.M
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256_bytes(payload.encode("utf-8"))


def atomic_write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    temp.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    temp.replace(path)


def git_root(value: str | Path) -> Path:
    path = Path(value).resolve()
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], cwd=path,
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise ValueError(f"not a git repository: {path}")
    return Path(result.stdout.strip()).resolve()


def relative_inside(path: Path, repo: Path) -> str:
    try:
        return path.resolve().relative_to(repo).as_posix()
    except ValueError as exc:
        raise ValueError(f"path must be inside repository: {path}") from exc


def feature_paths(feature_dir: Path) -> dict[str, Path]:
    return {
        "prototype": feature_dir / "demo" / "prototype.md",
        "inventory": feature_dir / "demo" / "mock-inventory.md",
        "prd": feature_dir / "prd.md",
        "testcases": feature_dir / "testcases.md",
        "manifest": feature_dir / "testcases.json",
        "approval": feature_dir / "testcase-approval.json",
        "demo_review": feature_dir / "reviews" / "demo-review.md",
        "prd_review": feature_dir / "reviews" / "prd-review.md",
        "testcase_review": feature_dir / "reviews" / "testcase-review.md",
    }


def require_files(paths: list[Path]) -> None:
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise ValueError("missing required artifact(s): " + ", ".join(missing))


def check_review(review: Path, repo: Path, required: list[Path]) -> None:
    require_files([review])
    text = review.read_text(encoding="utf-8")
    statuses = STATUS_RE.findall(text)
    if statuses != ["Approved"]:
        raise ValueError(f"{review.name} must contain exactly one Approved status")
    records = {match.group("path"): match.group("sha") for match in REVIEWED_RE.finditer(text)}
    for artifact in required:
        rel = relative_inside(artifact, repo)
        recorded = records.get(rel)
        if not recorded:
            raise ValueError(f"{review.name} did not review required artifact {rel}")
        current = subprocess.run(
            ["git", "hash-object", rel], cwd=repo, capture_output=True, text=True,
        )
        if current.returncode != 0 or not current.stdout.strip().startswith(recorded):
            raise ValueError(f"{review.name} is stale for {rel}")


def check_upstream(repo: Path, feature_dir: Path) -> dict[str, Path]:
    paths = feature_paths(feature_dir)
    required = [paths["prototype"], paths["inventory"], paths["prd"], paths["testcases"]]
    require_files(required)
    prd_findings: list[str] = []
    check_prd(paths["prd"].read_text(encoding="utf-8"), prd_findings)
    testcase_findings: list[str] = []
    check_testcases(
        paths["testcases"].read_text(encoding="utf-8"), testcase_findings,
        paths["prd"].read_text(encoding="utf-8"),
    )
    findings = prd_findings + testcase_findings
    if findings:
        raise ValueError("invalid PRD/testcases: " + "; ".join(findings))
    check_review(paths["demo_review"], repo, [paths["prototype"], paths["inventory"]])
    check_review(paths["prd_review"], repo, [paths["prd"]])
    return paths


def body_field(body: str, name: str) -> str:
    match = re.search(rf"^{re.escape(name)}:\s*(.+)$", body, re.M)
    if not match:
        raise ValueError(f"missing {name}")
    return match.group(1).strip()


def natural_step(body: str, english: str, chinese: str) -> str:
    match = re.search(rf"^(?:{english}|{chinese})\s*(.+)$", body, re.M)
    if not match:
        raise ValueError(f"missing {english}")
    return match.group(1).strip()


def parse_cases(text: str) -> list[dict]:
    headers = list(TC_HEADER_RE.finditer(text))
    cases: list[dict] = []
    for index, match in enumerate(headers):
        case_id = match.group(1)
        header = match.group("header")
        end = headers[index + 1].start() if index + 1 < len(headers) else len(text)
        body = text[match.end():end]
        level = re.search(r"\[level:\s*(api|ui-e2e)\]", header)
        seed = re.search(r"\[seed:\s*seed:([^\]\s]+)\]", header)
        if not level or not seed:
            raise ValueError(f"{case_id} has invalid level/seed metadata")
        driver_raw = body_field(body, "Driver-Action")
        driver_parts = [part.strip() for part in driver_raw.split("|", 1)]
        if len(driver_parts) != 2:
            raise ValueError(f"{case_id} Driver-Action must be '<driver> | <action>'")
        data_raw = body_field(body, "Data-Provenance")
        data_parts = [part.strip() for part in data_raw.split("|", 1)]
        fallback = body_field(body, "Fallback") if level.group(1) == "ui-e2e" else "none"
        observations = {}
        for kind, value in re.findall(r"^Observe:\s*(interface|logs|state)\s*\|\s*(.+)$", body, re.M):
            observations[kind] = value.strip()
        title = header.split("[", 1)[0].strip()
        cases.append({
            "id": case_id,
            "title": title,
            "level": level.group(1),
            "seed": f"seed:{seed.group(1)}",
            "ac_ids": sorted(set(AC_REF_RE.findall(header)), key=lambda item: int(item.split("-")[1])),
            "given": natural_step(body, "Given", "给定"),
            "when": natural_step(body, "When", "当"),
            "then": natural_step(body, "Then", "(?:则|那么)"),
            "driver": {"type": driver_parts[0], "action": driver_parts[1]},
            "success_signal": body_field(body, "Success-Signal"),
            "failure_signal": body_field(body, "Failure-Signal"),
            "data": {"kind": data_parts[0], "source": data_parts[1]},
            "provider_mode": body_field(body, "Provider-Mode"),
            "observations": observations,
            "fallback": fallback,
        })
    return cases


def build_manifest(repo: Path, feature_dir: Path, paths: dict[str, Path]) -> dict:
    sources = {
        relative_inside(paths[key], repo): sha256_file(paths[key])
        for key in ("prototype", "inventory", "prd", "testcases")
    }
    return {
        "schema_version": MANIFEST_SCHEMA,
        "feature_dir": relative_inside(feature_dir, repo),
        "source_hashes": sources,
        "execution_contract": {
            "entry": "project testcase runner",
            "playwright_primary": True,
            "computer_use_fallback": "atomic-only",
            "max_human_screenshots_per_case": 3,
            "required_observations": ["interface", "logs", "state"],
        },
        "cases": parse_cases(paths["testcases"].read_text(encoding="utf-8")),
    }


def validate_manifest(repo: Path, feature_dir: Path) -> tuple[dict, dict[str, Path]]:
    paths = check_upstream(repo, feature_dir)
    require_files([paths["manifest"]])
    try:
        actual = json.loads(paths["manifest"].read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"testcases.json is invalid JSON: {exc}") from exc
    expected = build_manifest(repo, feature_dir, paths)
    if actual != expected:
        raise ValueError("testcases.json is stale or hand-edited; rerun opc_testcase.py compile")
    return actual, paths


def approval_hash(approval: dict) -> str:
    return canonical_hash({key: value for key, value in approval.items() if key != "approval_hash"})


def check_feature_ready(
    repo: Path, feature_dir: Path, require_approved: bool = True,
) -> tuple[dict, dict[str, Path]]:
    manifest, paths = validate_manifest(repo, feature_dir)
    if not require_approved:
        return manifest, paths
    check_review(paths["testcase_review"], repo, [paths["testcases"], paths["manifest"]])
    require_files([paths["approval"]])
    try:
        approval = json.loads(paths["approval"].read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"testcase-approval.json is invalid JSON: {exc}") from exc
    if approval.get("schema_version") != APPROVAL_SCHEMA or approval.get("verdict") != "accepted":
        raise ValueError("testcase approval is missing an accepted verdict")
    expected_manifest_hash = f"sha256:{sha256_file(paths['manifest'])}"
    if approval.get("manifest_sha256") != expected_manifest_hash:
        raise ValueError("testcase approval is stale for testcases.json")
    if not approval.get("actor") or not approval.get("decision_note"):
        raise ValueError("testcase approval requires actor and decision_note")
    if approval.get("approval_hash") != approval_hash(approval):
        raise ValueError("testcase approval record was hand-edited or corrupted")
    return manifest, paths


def validate_case_evidence(
    repo: Path, feature_dir: Path, case_id: str, evidence_path: Path,
) -> dict:
    manifest, paths = check_feature_ready(repo, feature_dir, require_approved=True)
    cases = {case["id"]: case for case in manifest["cases"]}
    if case_id not in cases:
        raise ValueError(f"unknown testcase {case_id}")
    require_files([evidence_path])
    try:
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"case evidence is invalid JSON: {exc}") from exc
    if evidence.get("schema_version") != EVIDENCE_SCHEMA:
        raise ValueError(f"case evidence schema must be {EVIDENCE_SCHEMA}")
    manifest_hash = f"sha256:{sha256_file(paths['manifest'])}"
    if evidence.get("case_id") != case_id or evidence.get("manifest_sha256") != manifest_hash:
        raise ValueError("case evidence does not match the approved testcase manifest")

    driver = evidence.get("driver") if isinstance(evidence.get("driver"), dict) else {}
    assembly = evidence.get("assembly") if isinstance(evidence.get("assembly"), dict) else {}
    data = evidence.get("data") if isinstance(evidence.get("data"), dict) else {}
    provider = evidence.get("provider") if isinstance(evidence.get("provider"), dict) else {}
    observation = evidence.get("observation") if isinstance(evidence.get("observation"), dict) else {}
    outcome = evidence.get("outcome") if isinstance(evidence.get("outcome"), dict) else {}
    correlations = evidence.get("correlations") if isinstance(evidence.get("correlations"), dict) else {}
    steps = evidence.get("steps") if isinstance(evidence.get("steps"), list) else []

    case = cases[case_id]
    if driver.get("type") not in {"playwright", "computer-use", "api", "cli"}:
        raise ValueError("case evidence has an unsupported driver type")
    if case["level"] == "ui-e2e" and driver.get("type") not in {"playwright", "computer-use"}:
        raise ValueError("UI case evidence must use Playwright or an atomic Computer Use fallback")
    if case["level"] == "api" and driver.get("type") != "api":
        raise ValueError("API case evidence must use the API driver")
    if case["level"] == "ui-e2e" and not driver.get("action_performed"):
        raise ValueError("UI case evidence must prove the key action was performed")
    if driver.get("type") == "computer-use" and (
        driver.get("atomic_scope") is not True or not driver.get("fallback_reason")
    ):
        raise ValueError("Computer Use is allowed only as a reasoned atomic fallback")
    if assembly.get("kind") not in {"production", "test-double"} or not assembly.get("origin"):
        raise ValueError("case evidence must declare assembly.kind and origin")
    if data.get("kind") not in {"synthetic", "canonical-clone", "live-real"}:
        raise ValueError("case evidence has an invalid data.kind")
    if data.get("kind") != case["data"]["kind"] or data.get("source") != case["data"]["source"]:
        raise ValueError("case evidence data provenance does not match the approved testcase")
    if data.get("kind") in {"canonical-clone", "live-real"}:
        if not data.get("source_sha256") or data.get("isolation") not in {
            "isolated-copy", "scratch", "read-only",
        }:
            raise ValueError("real/canonical data requires a source hash and safe isolation")
    if provider.get("mode") not in {"none", "stub", "replay", "live"}:
        raise ValueError("case evidence has an invalid provider.mode")
    approved_provider = case["provider_mode"]
    if provider.get("mode") != approved_provider and not (
        provider.get("mode") == "live" and approved_provider in {"stub", "replay"}
    ):
        raise ValueError("case evidence provider mode does not match the approved testcase")
    if outcome.get("product") not in {"passed", "failed", "inconclusive"}:
        raise ValueError("case evidence has an invalid product outcome")
    if correlations.get("case_id") != case_id:
        raise ValueError("correlations.case_id must match the executed case")
    if not steps or any(
        not isinstance(step, dict) or step.get("status") not in {"passed", "failed"}
        for step in steps
    ):
        raise ValueError("case evidence must include step-by-step execution results")

    artifacts = evidence.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError("case evidence must contain hashed artifacts")
    artifact_paths: list[str] = []
    screenshot_count = 0
    for record in artifacts:
        if not isinstance(record, dict) or not record.get("path") or not record.get("sha256"):
            raise ValueError("case evidence contains malformed artifact metadata")
        artifact = repo / str(record["path"])
        relative_inside(artifact, repo)
        if not artifact.is_file() or f"sha256:{sha256_file(artifact)}" != record["sha256"]:
            raise ValueError(f"case evidence artifact is missing or stale: {record['path']}")
        artifact_paths.append(relative_inside(artifact, repo))
        if record.get("kind") == "screenshot":
            screenshot_count += 1
    if screenshot_count > 3:
        raise ValueError("human screenshot limit exceeded: maximum 3 per case")

    corners = []
    for name in ("interface", "logs", "state"):
        corner = observation.get(name) if isinstance(observation.get(name), dict) else {}
        if not corner.get("artifact") or corner["artifact"] not in artifact_paths:
            raise ValueError(f"observation.{name} must reference a hashed artifact")
        corners.append(corner.get("passed") is True)
    complete = observation.get("complete") is True and all(corners)
    product_passed = outcome.get("product") == "passed" and all(
        isinstance(step, dict) and step.get("status") == "passed" for step in steps
    )
    if product_passed and not complete:
        raise ValueError("a passed product outcome requires all three observation corners")
    if product_passed and not correlations.get("trace_id"):
        raise ValueError("a passed case requires a correlation trace_id")

    if not product_passed or not complete:
        label = "blocked"
    elif assembly.get("kind") != "production":
        label = "mock passed"
    elif provider.get("mode") == "live":
        label = "external provider passed"
    elif data.get("kind") == "synthetic":
        label = "seeded passed"
    else:
        label = "local real service passed"
    return {
        "evidence": evidence,
        "label": label,
        "manifest_sha256": manifest_hash,
        "artifact_paths": artifact_paths,
        "axes": {
            "assembly": assembly.get("kind"),
            "data": data.get("kind"),
            "provider": provider.get("mode"),
            "driver": driver.get("type"),
            "observation": "complete" if complete else "incomplete",
            "product_outcome": outcome.get("product"),
        },
        "browser_action": case["level"] == "ui-e2e" and driver.get("action_performed") is True,
        "production_assembly": assembly.get("kind") == "production",
        "data_hash": data.get("source_sha256"),
        "origin": assembly.get("origin"),
        "session_type": assembly.get("session_type"),
        "scratch_db": data.get("db_path"),
        "object_ids": correlations.get("object_ids", []),
        "trace_id": correlations.get("trace_id"),
    }


def cmd_compile(args: argparse.Namespace) -> int:
    repo = git_root(args.repo)
    feature_dir = Path(args.feature_dir).resolve()
    relative_inside(feature_dir, repo)
    paths = check_upstream(repo, feature_dir)
    manifest = build_manifest(repo, feature_dir, paths)
    atomic_write(paths["manifest"], manifest)
    paths["approval"].unlink(missing_ok=True)
    print(f"compiled {len(manifest['cases'])} cases to {paths['manifest']}")
    return 0


def cmd_approve(args: argparse.Namespace) -> int:
    repo = git_root(args.repo)
    feature_dir = Path(args.feature_dir).resolve()
    manifest, paths = validate_manifest(repo, feature_dir)
    check_review(paths["testcase_review"], repo, [paths["testcases"], paths["manifest"]])
    approval = {
        "schema_version": APPROVAL_SCHEMA,
        "verdict": "accepted",
        "actor": args.actor,
        "decision_note": args.decision_note,
        "approved_at": now(),
        "manifest_sha256": f"sha256:{sha256_file(paths['manifest'])}",
        "case_ids": [case["id"] for case in manifest["cases"]],
    }
    approval["approval_hash"] = approval_hash(approval)
    atomic_write(paths["approval"], approval)
    print(f"approved {len(manifest['cases'])} cases in {paths['approval']}")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    repo = git_root(args.repo)
    feature_dir = Path(args.feature_dir).resolve()
    manifest, _ = check_feature_ready(repo, feature_dir, args.require_approved)
    print(json.dumps({
        "ok": True,
        "case_count": len(manifest["cases"]),
        "approved": args.require_approved,
        "feature_dir": relative_inside(feature_dir, repo),
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    repo = git_root(args.repo)
    feature_dir = Path(args.feature_dir).resolve()
    manifest, paths = check_feature_ready(repo, feature_dir, require_approved=True)
    if args.case not in {case["id"] for case in manifest["cases"]}:
        raise ValueError(f"unknown testcase {args.case}")
    evidence_path = Path(args.evidence).resolve()
    relative_inside(evidence_path, repo)
    before = sha256_file(evidence_path) if evidence_path.is_file() else None
    command = list(args.command)
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        raise ValueError("no project testcase runner command supplied after --")
    env = os.environ.copy()
    env.update({
        "OPC_CASE_ID": args.case,
        "OPC_CASE_MANIFEST": str(paths["manifest"]),
        "OPC_CASE_MANIFEST_SHA256": f"sha256:{sha256_file(paths['manifest'])}",
        "OPC_CASE_EVIDENCE": str(evidence_path),
    })
    result = subprocess.run(command, cwd=repo, env=env, text=True)
    if result.returncode != 0:
        return result.returncode
    after = sha256_file(evidence_path) if evidence_path.is_file() else None
    if after is None or after == before:
        raise ValueError("project testcase runner did not create new evidence content")
    validated = validate_case_evidence(repo, feature_dir, args.case, evidence_path)
    if validated["label"] == "blocked":
        raise ValueError("case runner completed but product outcome is failed or inconclusive")
    print(json.dumps({
        "ok": True, "case_id": args.case, "label": validated["label"],
        "axes": validated["axes"], "evidence": relative_inside(evidence_path, repo),
    }, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command_name", required=True)
    for name in ("compile", "approve", "check", "run"):
        command = sub.add_parser(name)
        command.add_argument("--repo", default=".")
        command.add_argument("--feature-dir", required=True)
        if name == "compile":
            command.set_defaults(func=cmd_compile)
        elif name == "approve":
            command.add_argument("--actor", required=True)
            command.add_argument("--decision-note", required=True)
            command.set_defaults(func=cmd_approve)
        elif name == "check":
            command.add_argument("--require-approved", action="store_true")
            command.set_defaults(func=cmd_check)
        else:
            command.add_argument("--case", required=True)
            command.add_argument("--evidence", required=True)
            command.add_argument("command", nargs=argparse.REMAINDER)
            command.set_defaults(func=cmd_run)
    args = parser.parse_args()
    try:
        return args.func(args)
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
