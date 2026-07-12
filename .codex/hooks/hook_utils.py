#!/usr/bin/env python3
"""Shared helpers for neural-codex lifecycle hooks."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


SENSITIVE_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".env.staging",
    ".npmrc",
    ".pypirc",
    "credentials.json",
    "id_dsa",
    "id_ed25519",
    "id_rsa",
    "serviceAccountKey.json",
}


def read_event() -> dict[str, Any]:
    try:
        value = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return {}
    return value if isinstance(value, dict) else {}


def command_from(event: dict[str, Any]) -> str:
    tool_input = event.get("tool_input", {})
    if not isinstance(tool_input, dict):
        return ""
    command = tool_input.get("command", "")
    return command if isinstance(command, str) else ""


def emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=True))


def block(reason: str) -> int:
    print(reason, file=sys.stderr)
    return 2


def patch_paths(patch: str) -> list[Path]:
    prefixes = ("*** Add File: ", "*** Update File: ", "*** Delete File: ")
    paths: list[Path] = []
    for line in patch.splitlines():
        for prefix in prefixes:
            if line.startswith(prefix):
                paths.append(Path(line.removeprefix(prefix).strip()))
                break
    return paths


def is_sensitive(path: Path) -> bool:
    name = path.name
    return name in SENSITIVE_NAMES or name.startswith(".env.")
