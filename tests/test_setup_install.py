from __future__ import annotations

import re
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _read_script(name: str) -> str:
    path = _repo_root() / "scripts" / name
    return path.read_text(encoding="utf-8")


def _assert_regex(pattern: str, text: str, message: str) -> None:
    assert re.search(pattern, text), message


def test_setup_global_installs_skills() -> None:
    text = _read_script("setup-global.sh")
    _assert_regex(
        r'copy_dir\s+"\${SRC_SKILLS}"\s+"\${GLOBAL_SKILLS}"',
        text,
        "setup-global.sh should copy repo skills into the global install",
    )
    _assert_regex(
        r'copy_dir\s+"\${GLOBAL_SKILLS}"\s+"\${HOME}/\.agents/skills"',
        text,
        "setup-global.sh should copy skills into ~/.agents/skills",
    )
    _assert_regex(
        r'copy_dir\s+"\${GLOBAL_SKILLS}"\s+"\${HOME}/\.codex/skills"',
        text,
        "setup-global.sh should copy skills into ~/.codex/skills (legacy)",
    )


def test_setup_project_seeds_skills() -> None:
    text = _read_script("setup-project.sh")
    _assert_regex(
        r'copy_dir\s+"\${GLOBAL_ROOT}/skills"\s+"\${PROJECT_ROOT}/\.agents/skills"',
        text,
        "setup-project.sh should seed project skills from the global install",
    )
    _assert_regex(
        r'copy_dir\s+"\${GLOBAL_ROOT}/skills"\s+"\${PROJECT_ROOT}/\.codex/skills"',
        text,
        "setup-project.sh should seed legacy project skills from the global install",
    )
