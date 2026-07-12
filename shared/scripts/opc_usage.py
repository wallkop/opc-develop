#!/usr/bin/env python3
"""Normalize usage snapshots from Codex session JSONL or supplied JSON."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

FIELDS = ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens", "total_tokens")


def normalize_usage(raw: dict) -> dict:
    aliases = {
        "input_tokens": ("input_tokens", "prompt_tokens"),
        "cached_input_tokens": ("cached_input_tokens", "cached_tokens", "cache_read_input_tokens"),
        "output_tokens": ("output_tokens", "completion_tokens"),
        "reasoning_output_tokens": ("reasoning_output_tokens", "reasoning_tokens"),
        "total_tokens": ("total_tokens",),
    }
    out = {}
    for target, keys in aliases.items():
        value = next((raw.get(key) for key in keys if raw.get(key) is not None), 0)
        out[target] = max(0, int(value or 0))
    if not out["total_tokens"]:
        out["total_tokens"] = out["input_tokens"] + out["output_tokens"]
    return out


def codex_session_path(thread_id: str, sessions_root: Path | None = None) -> Path | None:
    root = sessions_root or Path.home() / ".codex" / "sessions"
    matches = sorted(root.rglob(f"*{thread_id}*.jsonl")) if root.exists() else []
    if matches:
        return matches[-1]
    return None


def read_codex_usage(path: Path) -> dict | None:
    latest = None
    session_id = None
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") == "session_meta":
            session_id = obj.get("payload", {}).get("session_id") or obj.get("payload", {}).get("id")
        if obj.get("type") == "event_msg" and obj.get("payload", {}).get("type") == "token_count":
            latest = obj.get("payload", {}).get("info", {}).get("total_token_usage")
    if not isinstance(latest, dict):
        return None
    return {"source": "codex-session-jsonl", "session_id": session_id, "usage": normalize_usage(latest)}


def capture_usage(source: str = "auto", input_path: str | None = None, env: dict | None = None) -> dict | None:
    env = env or os.environ
    if source in {"auto", "codex"}:
        thread_id = env.get("CODEX_THREAD_ID")
        path = codex_session_path(thread_id) if thread_id else None
        if path:
            result = read_codex_usage(path)
            if result:
                result["thread_id"] = thread_id
                return result
        if source == "codex":
            return None
    if source in {"normalized", "claude-otel", "claude-insights", "transcript"} and input_path:
        raw = json.loads(Path(input_path).read_text(encoding="utf-8"))
        usage = raw.get("usage", raw)
        return {"source": source, "session_id": raw.get("session_id"), "usage": normalize_usage(usage)}
    return None


def usage_delta(start: dict | None, end: dict | None) -> dict | None:
    if not start or not end:
        return None
    if start.get("session_id") and end.get("session_id") and start["session_id"] != end["session_id"]:
        return None
    return {field: max(0, int(end["usage"].get(field, 0)) - int(start["usage"].get(field, 0))) for field in FIELDS}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot", nargs="?")
    parser.add_argument("--source", default="auto")
    parser.add_argument("--input")
    args = parser.parse_args()
    result = capture_usage(args.source, args.input)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result else 2


if __name__ == "__main__":
    raise SystemExit(main())
