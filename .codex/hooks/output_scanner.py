#!/usr/bin/env python3
"""PostToolUse hook that warns when tool output appears to contain secrets."""

from __future__ import annotations

import json
import re
from typing import Any

from hook_utils import emit, read_event


SECRET_PATTERNS = (
    ("Anthropic API key", re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}")),
    ("OpenAI API key", re.compile(r"sk-(?!ant-)[A-Za-z0-9_-]{20,}")),
    ("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("GitHub token", re.compile(r"(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}")),
    ("Stripe key", re.compile(r"(?:sk|pk)_(?:live|test)_[0-9A-Za-z]{24,}")),
    ("Slack token", re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,}")),
    ("GitLab token", re.compile(r"glpat-[A-Za-z0-9_-]{20,}")),
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----")),
    ("database URL with password", re.compile(r"(?:postgres|mysql|mongodb)://[^:\s]+:[^@\s]+@")),
)


def stringify(value: Any) -> str:
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, ensure_ascii=True)
    except (TypeError, ValueError):
        return repr(value)


def main() -> int:
    event = read_event()
    output = stringify(event.get("tool_response", ""))
    warnings = [name for name, pattern in SECRET_PATTERNS if pattern.search(output)]
    if warnings:
        emit({"systemMessage": "SECRET LEAK WARNING: Detected in tool output: " + ", ".join(warnings) + ". Do not commit or share it."})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
