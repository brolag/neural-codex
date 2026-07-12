#!/usr/bin/env python3
"""PreToolUse hook that blocks high-confidence destructive Bash commands."""

from __future__ import annotations

import re

from hook_utils import block, command_from, emit, read_event


BLOCKED_SUBSTRINGS = (
    "dd if=",
    "mkfs",
    ":(){:|:&};:",
    "> /dev/sda",
    "chmod -R 777 /",
    "--no-preserve-root",
    "DROP DATABASE",
    "DROP TABLE",
)


def main() -> int:
    event = read_event()
    if event.get("tool_name") != "Bash":
        return 0

    command = command_from(event)
    if re.search(r"\brm\s+-[A-Za-z]*r[A-Za-z]*f[A-Za-z]*\s+(?:/|~|\$HOME)\s*(?:$|[;&|])", command):
        return block("BLOCKED: Recursive deletion of a root or home directory")

    for pattern in BLOCKED_SUBSTRINGS:
        if pattern in command:
            return block(f"BLOCKED: Destructive command detected: {pattern!r}")

    if re.search(r"git\s+push\b", command) and re.search(r"(?:\s-f\b|--force(?:-with-lease)?\b)", command) and re.search(r"\b(?:main|master)\b", command):
        return block("BLOCKED: Force push to main/master")

    if re.search(r"(?:^|[;&|]\s*)(?:npm|pnpm|yarn)\s+publish\b", command):
        return block("BLOCKED: Package publication requires manual confirmation")

    if re.search(r"(?:^|\s)(?:rm\s+-r\b|rmdir\b)", command):
        emit({"systemMessage": "Warning: File deletion detected. Verify that it is intentional."})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
