#!/usr/bin/env python3
"""PreToolUse hook that prevents apply_patch from changing secret-bearing files."""

from __future__ import annotations

from hook_utils import block, command_from, is_sensitive, patch_paths, read_event


def main() -> int:
    event = read_event()
    if event.get("tool_name") != "apply_patch":
        return 0

    for path in patch_paths(command_from(event)):
        if is_sensitive(path):
            return block(f"BLOCKED: Writing to sensitive file {path.name!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
