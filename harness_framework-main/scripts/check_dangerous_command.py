#!/usr/bin/env python3
"""Reject obviously destructive shell commands when used as a Codex/Claude hook."""

from __future__ import annotations

import json
import os
import re
import sys
from typing import Any


PATTERNS = [
    r"\brm\b(?=.*(?:^|\s)-[^\s]*r)(?=.*(?:^|\s)-[^\s]*f)",
    r"\b(?:Remove-Item|rm|ri)\b(?=.*(?:^|\s)-(?:Recurse|r)(?:\s|$))(?=.*(?:^|\s)-(?:Force|fo)(?:\s|$))",
    r"\bgit\s+reset\s+--hard\b",
    r"\bgit\s+push\b(?=.*(?:^|\s)--force(?:-with-lease)?(?:\s|$))",
    r"\bgit\s+clean\b(?=.*(?:^|\s)-[^\s]*f)(?=.*(?:^|\s)-[^\s]*d)",
    r"\b(?:rmdir|rd)\s+/s\b",
    r"\b(?:del|erase)\b(?=.*(?:^|\s)/[^\s]*s)(?=.*(?:^|\s)/[^\s]*q)",
    r"\bDROP\s+TABLE\b",
]


def find_dangerous_pattern(text: str) -> str | None:
    for pattern in PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            return pattern
    return None


def read_hook_payload() -> dict[str, Any]:
    """Read Codex stdin JSON, falling back to legacy env payloads."""
    stdin = ""
    if not sys.stdin.isatty():
        stdin = sys.stdin.read().strip()

    raw = stdin or os.environ.get("CODEX_TOOL_INPUT") or os.environ.get("CLAUDE_TOOL_INPUT") or "{}"
    try:
        loaded = json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}
    if isinstance(loaded, dict):
        return loaded
    return {"raw": loaded}


def extract_command(payload: dict[str, Any]) -> str:
    tool_input = payload.get("tool_input")
    if isinstance(tool_input, dict) and isinstance(tool_input.get("command"), str):
        return tool_input["command"]
    if isinstance(payload.get("command"), str):
        return payload["command"]
    return json.dumps(payload, ensure_ascii=False)


def main() -> int:
    payload = read_hook_payload()
    text = extract_command(payload)
    pattern = find_dangerous_pattern(text)
    if pattern:
        print(f"BLOCKED: dangerous command matched {pattern}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
