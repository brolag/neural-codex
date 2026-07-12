from __future__ import annotations

import os
import re
import subprocess
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
        r'copy_dir\s+"\${GLOBAL_SKILLS}"\s+"\${CODEX_ROOT}/skills"',
        text,
        "setup-global.sh should copy skills into $CODEX_HOME/skills (legacy)",
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


def test_setup_global_installs_hooks_and_profiles() -> None:
    text = _read_script("setup-global.sh")
    _assert_regex(
        r'copy_dir\s+"\${SRC_HOOKS}"\s+"\${GLOBAL_HOOKS}"',
        text,
        "setup-global.sh should stage Codex-native hooks",
    )
    assert "${SRC_PROFILES}" in text
    assert 'CODEX_ROOT="${CODEX_HOME:-${HOME}/.codex}"' in text
    assert "${CODEX_ROOT}/$(basename \"${profile}\")" in text
    assert '__pycache__' in text


def test_setup_project_seeds_hooks() -> None:
    text = _read_script("setup-project.sh")
    _assert_regex(
        r'copy_dir\s+"\${GLOBAL_ROOT}/hooks"\s+"\${PROJECT_ROOT}/\.codex/hooks"',
        text,
        "setup-project.sh should seed hook scripts",
    )
    assert '${PROJECT_ROOT}/.codex/hooks.json' in text


def test_setup_scripts_honor_custom_codex_home(tmp_path: Path) -> None:
    root = _repo_root()
    home = tmp_path / "home"
    codex_home = tmp_path / "custom-codex-home"
    project = tmp_path / "project"
    home.mkdir()
    project.mkdir()
    env = os.environ.copy()
    env.update({"HOME": str(home), "CODEX_HOME": str(codex_home)})

    subprocess.run(["bash", "scripts/setup-global.sh", "--force"], cwd=root, env=env, check=True, capture_output=True, text=True)
    subprocess.run(
        ["bash", "scripts/setup-project.sh", "--force", "--path", str(project)],
        cwd=root,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )

    assert (codex_home / "neural-codex" / "hooks.json").is_file()
    assert (codex_home / "prompts" / "neural.profile.md").is_file()
    assert (codex_home / "default.config.toml").is_file()
    assert (project / ".codex" / "hooks.json").is_file()
    assert not (home / ".codex" / "default.config.toml").exists()
