#!/usr/bin/env python3
"""PreCompact hook that records small, durable recovery context."""

from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path

from hook_utils import emit, read_event


def git_output(cwd: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    return completed.stdout.strip()


def latest_plan(plans: Path) -> str | None:
    if not plans.is_dir():
        return None
    entries = [path for path in plans.iterdir() if not path.name.startswith(".")]
    if not entries:
        return None
    return max(entries, key=lambda path: path.stat().st_mtime).relative_to(plans.parent).as_posix()


def main() -> int:
    event = read_event()
    cwd = Path(str(event.get("cwd") or Path.cwd())).resolve()
    target = cwd / ".codex" / "compact-context.md"
    lines = [
        f"# Pre-Compaction Context ({datetime.now(timezone.utc).isoformat()})",
        "",
    ]

    if (cwd / ".git").exists() or git_output(cwd, "rev-parse", "--git-dir"):
        lines.extend(
            [
                "## Git State",
                f"Branch: {git_output(cwd, 'branch', '--show-current') or 'unknown'}",
                "Recent commits:",
                git_output(cwd, "log", "--oneline", "-5") or "(none)",
                "",
                "Modified files:",
                git_output(cwd, "status", "--short") or "(clean)",
                "",
            ]
        )

    plan = latest_plan(cwd / "plans")
    if plan:
        lines.extend(["## Active Plan", f"Latest: {plan}", ""])

    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(lines), encoding="utf-8")
    except OSError as exc:
        emit({"systemMessage": f"Could not preserve compact context: {exc}"})
        return 0

    emit({"systemMessage": f"Context preserved to {target}. Read it after compaction to recover state."})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
