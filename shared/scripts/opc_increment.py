#!/usr/bin/env python3
"""Create and verify revision-bound acceptance receipts for standard increments.

The helper keeps expensive checks out of the ordinary debug loop. It records commands with
timestamps, exit codes, output paths, authenticity labels, production-assembly metadata, and a
content-tree fingerprint. A code/test/plan change makes earlier evidence stale automatically.

Typical flow:
  opc_increment.py init --plan docs/features/7-x/feature-plan.md \
    --receipt docs/features/7-x/acceptance.json
  opc_increment.py run --receipt ... --kind build --label seeded\ passed -- <build command>
  opc_increment.py run --receipt ... --kind browser --label local\ real\ service\ passed \
    --core --browser-action --production-assembly --data-hash sha256:... -- <journey command>
  opc_increment.py check --receipt ... --require real-service-core-journey

Exit codes: command exit code for `run`; 0 success, 1 failed guard/check, 2 usage error otherwise.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from functools import wraps
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

from validate_artifacts import check_feature_plan, field

try:
    import fcntl  # type: ignore[attr-defined]
except ImportError:  # pragma: no cover - Windows fallback
    fcntl = None
    import msvcrt  # type: ignore[import-not-found]

SCHEMA = "opc-acceptance-v1"
LABELS = (
    "mock passed", "seeded passed", "local real service passed",
    "external provider passed", "human accepted", "long-run passed",
    "not run", "pending", "blocked",
)
COMMAND_PASS_LABELS = (
    "mock passed", "seeded passed", "local real service passed",
    "external provider passed", "long-run passed",
)
KINDS = ("logic", "build", "service", "browser", "replay", "provider")
LEVELS = (
    "code-build", "automated-core-journey",
    "real-service-core-journey", "human-accepted",
)
REAL_LABELS = {
    "local real service passed", "external provider passed",
    "human accepted", "long-run passed",
}
GLOBAL_PROCESS_PATHS = (
    ":(glob)docs/features/*/acceptance.json",
    ":(glob)docs/features/*/reviews/**",
    ":(glob)docs/features/*/ledger.jsonl",
    ":(glob)docs/features/*/reports/**",
    ":(glob)docs/features/*/release-manifest.md",
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def git(repo: Path, *args: str, env: dict[str, str] | None = None,
        check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=repo, env=env, capture_output=True, text=True, check=check,
    )


def repo_root(value: str) -> Path:
    path = Path(value).resolve()
    result = git(path, "rev-parse", "--show-toplevel", check=False)
    if result.returncode != 0:
        raise ValueError(f"not a git repository: {path}")
    return Path(result.stdout.strip()).resolve()


def relative_inside(path: Path, repo: Path) -> str:
    try:
        return path.resolve().relative_to(repo).as_posix()
    except ValueError as exc:
        raise ValueError(f"path must be inside repository: {path}") from exc


def canonical_exclusions(receipt_rel: str) -> list[str]:
    artifact_dir = Path(receipt_rel).parent
    def artifact_path(name: str) -> str:
        return (artifact_dir / name).as_posix()
    return list(dict.fromkeys([
        receipt_rel,
        artifact_path("reviews"),
        artifact_path("ledger.jsonl"),
        artifact_path("reports"),
        artifact_path("release-manifest.md"),
    ]))


def receipt_exclusions(repo: Path, receipt_path: Path, receipt: dict) -> list[str]:
    expected_plan = relative_inside(receipt_path.parent / "feature-plan.md", repo)
    if receipt.get("plan") != expected_plan:
        raise ValueError("receipt plan path is non-canonical or tampered; reinitialize the receipt")
    expected = canonical_exclusions(relative_inside(receipt_path, repo))
    if receipt.get("excluded_paths") != expected:
        raise ValueError(
            "receipt excluded_paths is non-canonical or tampered; reinitialize the receipt"
        )
    return expected


def head(repo: Path) -> str:
    result = git(repo, "rev-parse", "HEAD", check=False)
    return result.stdout.strip() if result.returncode == 0 else "UNBORN"


@contextmanager
def receipt_lock(repo: Path, receipt_path: Path):
    result = git(repo, "rev-parse", "--git-path", "opc-locks", check=False)
    base = Path(result.stdout.strip()) if result.returncode == 0 else repo / ".git/opc-locks"
    if not base.is_absolute():
        base = repo / base
    base.mkdir(parents=True, exist_ok=True)
    namespace = hashlib.sha256(relative_inside(receipt_path, repo).encode("utf-8")).hexdigest()
    lock_path = base / f"{namespace}.lock"
    with lock_path.open("a+b") as handle:
        if fcntl is not None:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        else:  # pragma: no cover - Windows fallback
            handle.seek(0, os.SEEK_END)
            if handle.tell() == 0:
                handle.write(b"\0"); handle.flush()
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
        try:
            yield
        finally:
            if fcntl is not None:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            else:  # pragma: no cover - Windows fallback
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)


def locked_receipt_command(func):
    @wraps(func)
    def wrapper(args: argparse.Namespace) -> int:
        try:
            repo = repo_root(args.repo)
            receipt_path = Path(args.receipt).resolve()
            relative_inside(receipt_path, repo)
            with receipt_lock(repo, receipt_path):
                return func(args)
        except (ValueError, OSError) as exc:
            return fail(str(exc))
    return wrapper


def tree_fingerprint(repo: Path, excluded: list[str]) -> str:
    """Hash the current visible tree without mutating the real index.

    A temporary index makes the fingerprint independent of whether identical content is committed
    before or after verification. The receipt itself is removed to avoid a self-referential hash.
    """
    fd, name = tempfile.mkstemp(prefix="opc-index-")
    os.close(fd)
    Path(name).unlink()
    env = os.environ.copy()
    env["GIT_INDEX_FILE"] = name
    try:
        if head(repo) == "UNBORN":
            git(repo, "read-tree", "--empty", env=env)
        else:
            git(repo, "read-tree", "HEAD", env=env)
        added = git(repo, "add", "-A", "--", ".", env=env, check=False)
        if added.returncode != 0:
            raise ValueError(added.stderr.strip() or "git add failed in temporary index")
        for rel in excluded:
            git(
                repo, "rm", "-r", "--cached", "--ignore-unmatch", "--", rel,
                env=env, check=False,
            )
        for pathspec in GLOBAL_PROCESS_PATHS:
            git(
                repo, "rm", "-r", "--cached", "--ignore-unmatch", "--", pathspec,
                env=env, check=False,
            )
        result = git(repo, "write-tree", env=env, check=False)
        if result.returncode != 0:
            raise ValueError(result.stderr.strip() or "git write-tree failed")
        return result.stdout.strip()
    finally:
        Path(name).unlink(missing_ok=True)


def atomic_write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def initial_chain(receipt: dict) -> str:
    return canonical_hash({
        "schema_version": receipt.get("schema_version"),
        "receipt_id": receipt.get("receipt_id"),
        "plan": receipt.get("plan"),
        "created_at": receipt.get("created_at"),
    })


def command_hash(previous: str, command: dict) -> str:
    body = {key: value for key, value in command.items() if key not in {"previous_hash", "entry_hash"}}
    return canonical_hash({"previous_hash": previous, "command": body})


def acceptance_hash(chain_head: str, acceptance: dict) -> str:
    body = {key: value for key, value in acceptance.items() if key != "acceptance_hash"}
    return canonical_hash({"chain_head": chain_head, "acceptance": body})


def verify_receipt_chain(data: dict) -> None:
    current = initial_chain(data)
    for index, command in enumerate(data.get("commands", []), 1):
        if command.get("previous_hash") != current:
            raise ValueError(f"tampered receipt command chain at CMD-{index}: previous hash mismatch")
        expected = command_hash(current, command)
        if command.get("entry_hash") != expected:
            raise ValueError(f"tampered receipt command chain at CMD-{index}: entry hash mismatch")
        current = expected
    if data.get("chain_head") != current:
        raise ValueError("tampered receipt command chain: head mismatch")
    acceptance = data.get("human_acceptance")
    if acceptance is not None and acceptance.get("acceptance_hash") != acceptance_hash(current, acceptance):
        raise ValueError("tampered human acceptance record")


def read_receipt(path: Path) -> dict:
    if not path.exists():
        raise ValueError(f"receipt does not exist: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"receipt is not valid JSON: {exc}") from exc
    if data.get("schema_version") != SCHEMA:
        raise ValueError(f"receipt schema must be {SCHEMA}")
    if not isinstance(data.get("commands"), list):
        raise ValueError("receipt commands must be an array")
    verify_receipt_chain(data)
    return data


def resolve_plan(repo: Path, receipt: dict) -> Path:
    plan = repo / str(receipt.get("plan", ""))
    if not plan.exists():
        raise ValueError(f"plan does not exist: {plan}")
    findings: list[str] = []
    inventory = plan.parent / "demo" / "mock-inventory.md"
    prd = plan.parent / "prd.md"
    technical = plan.parent / "technical.md"
    check_feature_plan(
        plan.read_text(encoding="utf-8"), findings,
        inventory.read_text(encoding="utf-8") if inventory.exists() else None,
        prd.read_text(encoding="utf-8") if prd.exists() else None,
        technical.read_text(encoding="utf-8") if technical.exists() else None,
    )
    if findings:
        raise ValueError("invalid feature plan: " + "; ".join(findings))
    if field(plan.read_text(encoding="utf-8"), "Class") == "split":
        raise ValueError(
            "split plans are plan-only; choose one <=240-minute standard increment and initialize its receipt"
        )
    return plan


def evidence_files_current(command: dict, repo: Path) -> bool:
    output = Path(str(command.get("output", "")))
    if not output.is_absolute():
        output = repo / output
    if not output.is_file() or not command.get("output_sha256"):
        return False
    content = output.read_bytes()
    if hashlib.sha256(content).hexdigest() != command.get("output_sha256"):
        return False
    records = command.get("artifacts")
    if not isinstance(records, list):
        return False
    for record in records:
        if not isinstance(record, dict) or not record.get("path") or not record.get("sha256"):
            return False
        path = repo / record["path"]
        if not path.is_file():
            return False
        artifact = path.read_bytes()
        if hashlib.sha256(artifact).hexdigest() != record["sha256"]:
            return False
    return True


def valid_commands(receipt: dict, revision: str, repo: Path) -> list[dict]:
    """Return only the freshest passing attempt for each evidence layer.

    A later failed build/core/replay/provider attempt dominates an earlier pass on the same
    revision. Non-passing authenticity labels never create a completion level.
    """
    latest: dict[str, dict] = {}
    for command in receipt.get("commands", []):
        if command.get("revision") != revision:
            continue
        key = "core" if command.get("core") else str(command.get("kind"))
        latest[key] = command
    return [
        command for command in latest.values()
        if command.get("exit_code") == 0
        and command.get("label") in COMMAND_PASS_LABELS
        and not command.get("mutated_worktree", False)
        and evidence_files_current(command, repo)
    ]


def core_is_real(command: dict, plan_text: str) -> bool:
    if not command.get("core") or not command.get("production_assembly"):
        return False
    if command.get("label") not in REAL_LABELS:
        return False
    if not command.get("evidence_complete"):
        return False
    journey_type = field(plan_text, "Journey-Type")
    if journey_type == "ui" and (
        command.get("kind") != "browser" or not command.get("browser_action")
    ):
        return False
    if journey_type != "ui" and command.get("kind") not in {"service", "browser"}:
        return False
    data_kind = field(plan_text, "Data-Kind")
    if data_kind in {"snapshot", "real"}:
        return command.get("data_hash") == field(plan_text, "Data-Hash")
    return True


def evaluate(repo: Path, receipt_path: Path, receipt: dict) -> tuple[str, str, list[str], str]:
    plan = resolve_plan(repo, receipt)
    plan_text = plan.read_text(encoding="utf-8")
    revision = tree_fingerprint(repo, receipt_exclusions(repo, receipt_path, receipt))
    commands = valid_commands(receipt, revision, repo)
    levels: list[str] = []
    build_ok = any(command.get("kind") == "build" for command in commands)
    if build_ok:
        levels.append("code-build")
    core = [command for command in commands if command.get("core")] if build_ok else []
    if core:
        levels.append("automated-core-journey")
    real_core = [command for command in core if core_is_real(command, plan_text)]
    if real_core:
        levels.append("real-service-core-journey")
    acceptance = receipt.get("human_acceptance") or {}
    if (
        real_core
        and acceptance.get("revision") == revision
        and acceptance.get("verdict") == "accepted"
        and acceptance.get("command_count") == len(receipt.get("commands", []))
    ):
        levels.append("human-accepted")
    current = levels[-1] if levels else "none"
    return current, revision, levels, field(plan_text, "Journey-Type") or ""


@locked_receipt_command
def cmd_init(args: argparse.Namespace) -> int:
    try:
        repo = repo_root(args.repo)
        plan = Path(args.plan).resolve()
        receipt_path = Path(args.receipt).resolve()
        plan_rel = relative_inside(plan, repo)
        receipt_rel = relative_inside(receipt_path, repo)
        if plan.name != "feature-plan.md" or receipt_path.name != "acceptance.json" or plan.parent != receipt_path.parent:
            return fail("plan and receipt must be sibling feature-plan.md and acceptance.json files")
        if receipt_path.exists():
            return fail(
                "receipt already exists; reuse it so command history and provider stop-loss remain intact"
            )
        if not plan.exists():
            return fail(f"plan does not exist: {plan}")
        findings: list[str] = []
        inventory = plan.parent / "demo" / "mock-inventory.md"
        prd = plan.parent / "prd.md"
        technical = plan.parent / "technical.md"
        check_feature_plan(
            plan.read_text(encoding="utf-8"), findings,
            inventory.read_text(encoding="utf-8") if inventory.exists() else None,
            prd.read_text(encoding="utf-8") if prd.exists() else None,
            technical.read_text(encoding="utf-8") if technical.exists() else None,
        )
        if findings:
            return fail("invalid feature plan: " + "; ".join(findings))
        if field(plan.read_text(encoding="utf-8"), "Class") == "split":
            return fail(
                "split plans are plan-only; choose one <=240-minute standard increment first"
            )
        excluded = canonical_exclusions(receipt_rel)
        for item in excluded:
            if Path(item).is_absolute() or item == ".." or item.startswith("../"):
                return fail(f"excluded path must be repository-relative: {item}")
        receipt = {
            "schema_version": SCHEMA,
            "receipt_id": f"receipt-{uuid.uuid4().hex}",
            "plan": plan_rel,
            "created_at": now(),
            "updated_at": now(),
            "head": head(repo),
            "revision": tree_fingerprint(repo, excluded),
            "excluded_paths": excluded,
            "commands": [],
            "human_acceptance": None,
        }
        receipt["chain_head"] = initial_chain(receipt)
        atomic_write(receipt_path, receipt)
        print(f"initialized {receipt_path}")
        return 0
    except (ValueError, OSError) as exc:
        return fail(str(exc))


def evidence_dir(repo: Path, receipt_id: str, revision: str) -> Path:
    result = git(repo, "rev-parse", "--git-path", "opc-evidence", check=False)
    base = Path(result.stdout.strip()) if result.returncode == 0 else repo / ".git/opc-evidence"
    if not base.is_absolute():
        base = repo / base
    directory = base / receipt_id / revision
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def provider_precheck(receipt: dict, revision: str, plan_text: str, repo: Path,
                      allow_repeat: bool, reason: str | None) -> str | None:
    attempts = [
        command for command in receipt.get("commands", [])
        if command.get("kind") == "provider" and command.get("revision") == revision
    ]
    if attempts and not allow_repeat:
        return "provider repeat refused for this revision; return to offline layers or use an explicit reasoned override"
    if allow_repeat and not reason:
        return "provider repeat override requires --reason"
    commands = valid_commands(receipt, revision, repo)
    cheap = any(command.get("kind") in {"logic", "build"} for command in commands)
    local_core = any(core_is_real(command, plan_text) for command in commands)
    replay = any(command.get("kind") == "replay" for command in commands)
    missing = []
    if not cheap:
        missing.append("logic/build")
    if not local_core:
        missing.append("local core journey")
    if not replay:
        missing.append("offline replay")
    if missing:
        return "external provider is locked until offline layers pass: " + ", ".join(missing)
    return None


def structured_evidence_problem(args: argparse.Namespace) -> str | None:
    if not (args.core and args.label in REAL_LABELS) and args.kind != "provider":
        return None
    missing = []
    for value, label in (
        (args.origin, "--origin"), (args.session_type, "--session-type"),
        (args.trace_id, "--trace-id"),
    ):
        if not value:
            missing.append(label)
    if not args.object_id:
        missing.append("--object-id")
    if not args.artifact:
        missing.append("--artifact")
    if args.core and not args.scratch_db:
        missing.append("--scratch-db")
    if missing:
        return "real evidence requires " + ", ".join(missing)
    return None


def artifact_snapshot(repo: Path, paths: list[str]) -> dict[str, tuple[str, int, int]]:
    snapshot = {}
    for raw in paths:
        path = Path(raw)
        if not path.is_absolute():
            path = repo / path
        try:
            rel = relative_inside(path, repo)
        except ValueError:
            continue
        if path.is_file():
            content = path.read_bytes()
            snapshot[rel] = (
                hashlib.sha256(content).hexdigest(), path.stat().st_mtime_ns, len(content),
            )
    return snapshot


def artifact_metadata(repo: Path, paths: list[str]) -> tuple[list[dict], str | None]:
    records = []
    for raw in paths:
        path = Path(raw)
        if not path.is_absolute():
            path = repo / path
        try:
            rel = relative_inside(path, repo)
        except ValueError:
            return [], f"evidence artifact must be inside the repository: {raw}"
        if not path.is_file():
            return [], f"evidence artifact does not exist after command: {raw}"
        content = path.read_bytes()
        records.append({
            "path": rel, "sha256": hashlib.sha256(content).hexdigest(),
            "bytes": len(content), "mtime_ns": path.stat().st_mtime_ns,
        })
    return records, None


@locked_receipt_command
def cmd_run(args: argparse.Namespace) -> int:
    try:
        repo = repo_root(args.repo)
        receipt_path = Path(args.receipt).resolve()
        relative_inside(receipt_path, repo)
        receipt = read_receipt(receipt_path)
        excluded = receipt_exclusions(repo, receipt_path, receipt)
        plan = resolve_plan(repo, receipt)
        plan_text = plan.read_text(encoding="utf-8")
        revision = tree_fingerprint(repo, excluded)
        command = list(args.command)
        if command and command[0] == "--":
            command = command[1:]
        if not command:
            return fail("no command supplied after --")
        if args.core:
            if field(plan_text, "Journey-Type") == "ui" and args.kind != "browser":
                return fail("the UI core journey must use kind=browser")
            if not args.production_assembly:
                return fail("a core journey must run through production assembly")
            if field(plan_text, "Journey-Type") == "ui" and not args.browser_action:
                return fail("the UI core journey must drive the key action in a browser")
            expected_hash = field(plan_text, "Data-Hash")
            if field(plan_text, "Data-Kind") in {"snapshot", "real"} and args.data_hash != expected_hash:
                return fail(f"core journey must use the plan Data-Hash ({expected_hash})")
        if args.kind == "provider":
            if args.label != "external provider passed":
                return fail("a successful provider canary must use label 'external provider passed'")
            problem = provider_precheck(
                receipt, revision, plan_text, repo, args.allow_provider_repeat,
                args.reason,
            )
            if problem:
                return fail(problem)
        evidence_problem = structured_evidence_problem(args)
        if evidence_problem:
            return fail(evidence_problem)
        structured_required = (args.core and args.label in REAL_LABELS) or args.kind == "provider"
        before_artifacts = artifact_snapshot(repo, args.artifact)

        started = now()
        try:
            proc = subprocess.run(command, cwd=repo, capture_output=True, text=True, errors="replace")
            command_exit = proc.returncode
            output = proc.stdout + (("\n" if proc.stdout and proc.stderr else "") + proc.stderr)
        except OSError as exc:
            command_exit = 127
            output = f"command launch failed: {exc}\n"
        ended = now()
        receipt_namespace = hashlib.sha256(
            relative_inside(receipt_path, repo).encode("utf-8")
        ).hexdigest()
        log = evidence_dir(repo, receipt_namespace, revision) / f"{len(receipt['commands']) + 1:03d}-{args.kind}.log"
        log.write_text(output, encoding="utf-8")
        log_content = log.read_bytes()
        after = tree_fingerprint(repo, excluded)
        artifact_records, artifact_problem = artifact_metadata(repo, args.artifact)
        artifact_changed = any(
            before_artifacts.get(record["path"]) != (
                record["sha256"], record["mtime_ns"], record["bytes"],
            )
            for record in artifact_records
        )
        if structured_required and artifact_problem is None and not artifact_changed:
            artifact_problem = "structured evidence artifact was not created or updated by the command"
        effective_exit = command_exit if command_exit != 0 else (1 if artifact_problem else 0)
        entry = {
            "id": f"CMD-{len(receipt['commands']) + 1}",
            "kind": args.kind,
            "command": command,
            "cwd": str(repo),
            "started_at": started,
            "ended_at": ended,
            "exit_code": effective_exit,
            "command_exit_code": command_exit,
            "output": str(log),
            "output_sha256": hashlib.sha256(log_content).hexdigest(),
            "output_bytes": len(log_content),
            "output_excerpt": output[-2000:],
            "head": head(repo),
            "revision": revision,
            "revision_after": after,
            "mutated_worktree": revision != after,
            "label": args.label if effective_exit == 0 else "blocked",
            "core": args.core,
            "browser_action": args.browser_action,
            "production_assembly": args.production_assembly,
            "data_hash": args.data_hash,
            "build_id": args.build_id,
            "origin": args.origin,
            "session_type": args.session_type,
            "scratch_db": args.scratch_db,
            "object_ids": args.object_id,
            "trace_id": args.trace_id,
            "artifacts": artifact_records,
            "artifact_changed": artifact_changed,
            "evidence_complete": artifact_problem is None,
            "evidence_problem": artifact_problem,
            "external_provider": args.kind == "provider",
            "provider_repeat_override": args.reason if args.allow_provider_repeat else None,
        }
        entry["previous_hash"] = receipt["chain_head"]
        entry["entry_hash"] = command_hash(receipt["chain_head"], entry)
        receipt["chain_head"] = entry["entry_hash"]
        receipt["commands"].append(entry)
        receipt["updated_at"] = now()
        receipt["head"] = head(repo)
        receipt["revision"] = after
        receipt["human_acceptance"] = None
        atomic_write(receipt_path, receipt)
        if output:
            print(output, end="" if output.endswith("\n") else "\n")
        if artifact_problem:
            print(f"ERROR: {artifact_problem}", file=sys.stderr)
        print(f"recorded {entry['id']} ({args.kind}) exit={effective_exit} revision={revision[:12]}")
        return effective_exit
    except (ValueError, OSError) as exc:
        return fail(str(exc))


def cmd_check(args: argparse.Namespace) -> int:
    try:
        repo = repo_root(args.repo)
        receipt_path = Path(args.receipt).resolve()
        receipt = read_receipt(receipt_path)
        current, revision, levels, journey_type = evaluate(repo, receipt_path, receipt)
        required_index = LEVELS.index(args.require)
        current_index = LEVELS.index(current) if current in LEVELS else -1
        if current_index < required_index:
            old_revisions = {command.get("revision") for command in receipt.get("commands", [])}
            if old_revisions and revision not in old_revisions:
                return fail(
                    f"STALE acceptance evidence: current revision {revision[:12]} has no matching command results"
                )
            detail = ""
            if journey_type == "ui" and args.require in {"real-service-core-journey", "human-accepted"}:
                detail = "; UI completion requires a browser-driven key action through production assembly"
            return fail(f"completion level is {current}; required {args.require}{detail}")
        print(json.dumps({
            "ok": True, "completion_level": current, "levels": levels,
            "revision": revision, "receipt": str(receipt_path),
        }, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as exc:
        return fail(str(exc))


@locked_receipt_command
def cmd_accept(args: argparse.Namespace) -> int:
    try:
        repo = repo_root(args.repo)
        receipt_path = Path(args.receipt).resolve()
        receipt = read_receipt(receipt_path)
        current, revision, _, _ = evaluate(repo, receipt_path, receipt)
        if current not in {"real-service-core-journey", "human-accepted"}:
            return fail("human acceptance requires a fresh real-service core journey first")
        acceptance = {
            "verdict": "accepted", "actor": args.actor, "ts": now(),
            "revision": revision, "note": args.note,
            "command_count": len(receipt.get("commands", [])),
        }
        acceptance["acceptance_hash"] = acceptance_hash(receipt["chain_head"], acceptance)
        receipt["human_acceptance"] = acceptance
        receipt["updated_at"] = now()
        atomic_write(receipt_path, receipt)
        print(f"recorded human acceptance for revision {revision[:12]}")
        return 0
    except (ValueError, OSError) as exc:
        return fail(str(exc))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command_name", required=True)

    init = sub.add_parser("init")
    init.add_argument("--repo", default=".")
    init.add_argument("--plan", required=True)
    init.add_argument("--receipt", required=True)
    init.set_defaults(func=cmd_init)

    run = sub.add_parser("run")
    run.add_argument("--repo", default=".")
    run.add_argument("--receipt", required=True)
    run.add_argument("--kind", choices=KINDS, required=True)
    run.add_argument("--label", choices=COMMAND_PASS_LABELS, required=True)
    run.add_argument("--core", action="store_true")
    run.add_argument("--browser-action", action="store_true")
    run.add_argument("--production-assembly", action="store_true")
    run.add_argument("--data-hash")
    run.add_argument("--build-id")
    run.add_argument("--origin")
    run.add_argument("--session-type")
    run.add_argument("--scratch-db")
    run.add_argument("--object-id", action="append", default=[])
    run.add_argument("--trace-id")
    run.add_argument("--artifact", action="append", default=[])
    run.add_argument("--allow-provider-repeat", action="store_true")
    run.add_argument("--reason")
    run.add_argument("command", nargs=argparse.REMAINDER)
    run.set_defaults(func=cmd_run)

    check = sub.add_parser("check")
    check.add_argument("--repo", default=".")
    check.add_argument("--receipt", required=True)
    check.add_argument("--require", choices=LEVELS, default="real-service-core-journey")
    check.set_defaults(func=cmd_check)

    accept = sub.add_parser("accept")
    accept.add_argument("--repo", default=".")
    accept.add_argument("--receipt", required=True)
    accept.add_argument("--actor", required=True)
    accept.add_argument("--note")
    accept.set_defaults(func=cmd_accept)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
