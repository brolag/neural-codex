#!/usr/bin/env python3
"""PreToolUse hook that detects obvious instruction injection in executable content."""

from __future__ import annotations

from hook_utils import block, command_from, patch_paths, read_event


ROLE_OVERRIDE_PATTERNS = (
    "ignore previous instructions",
    "ignore all previous",
    "disregard previous",
    "forget your instructions",
    "you are now",
    "pretend you are",
    "new instructions:",
    "override:",
    "system prompt:",
)

JAILBREAK_PATTERNS = (
    "do anything now",
    "developer mode",
    "jailbreak",
    "ignore safety",
    "bypass restrictions",
    "act as an unrestricted",
)

TEXT_EXTENSIONS = {".md", ".txt", ".yaml", ".yml"}


def main() -> int:
    event = read_event()
    tool_name = event.get("tool_name")
    if tool_name not in {"Bash", "apply_patch"}:
        return 0

    content = command_from(event)
    if not content:
        return 0

    if tool_name == "Bash" and content.lstrip().startswith(("git commit", "git log", "git tag")):
        return 0

    if tool_name == "apply_patch":
        paths = patch_paths(content)
        if paths and all(path.suffix.lower() in TEXT_EXTENSIONS for path in paths):
            return 0

    lowered = content.lower()
    for pattern in (*ROLE_OVERRIDE_PATTERNS, *JAILBREAK_PATTERNS):
        if pattern in lowered:
            return block(f"BLOCKED: Prompt injection pattern detected: {pattern!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
