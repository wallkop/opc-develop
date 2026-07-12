#!/usr/bin/env python3
"""Project-agnostic compressed incident fixtures for the OPC runner self-test."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


def stderr_case(bad: bool) -> int:
    child = [sys.executable, "-c", "import sys; sys.stderr.write('x'*4000000); sys.stderr.flush()"]
    proc = subprocess.Popen(child, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        if bad:
            proc.wait(timeout=0.2)  # deliberately do not consume the pipe
        else:
            proc.communicate(timeout=5)
            return 0 if proc.returncode == 0 else 1
    except subprocess.TimeoutExpired:
        return 1 if bad else 2
    finally:
        if proc.poll() is None:
            proc.kill(); proc.communicate()
    return 2


def approval_case(bad: bool) -> int:
    events = ["approval_required", "decline"]
    terminal = None if bad else "turn_cancelled"
    return 0 if events[-1] == "decline" and terminal == "turn_cancelled" else 1


def delete_case(bad: bool) -> int:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "external-repo"; repo.mkdir(); sentinel = repo / "sentinel.txt"; sentinel.write_text("keep")
        if bad:
            sentinel.unlink(); repo.rmdir()
        project_row_deleted = True
        safe = project_row_deleted and repo.exists() and sentinel.exists()
        return 0 if safe else 1


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("case", choices=["stderr", "approval", "delete"]); parser.add_argument("--bad", action="store_true"); args = parser.parse_args()
    return {"stderr": stderr_case, "approval": approval_case, "delete": delete_case}[args.case](args.bad)


if __name__ == "__main__": raise SystemExit(main())
