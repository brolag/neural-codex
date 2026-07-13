from __future__ import annotations

import os
import re
import shutil
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


def _seed_legacy_craft(skill_root: Path, *, customized: bool = False) -> Path:
    target = skill_root / "craft" / "SKILL.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    fixture = _repo_root() / "tests" / "fixtures" / "legacy-craft-SKILL.md"
    shutil.copyfile(fixture, target)
    if customized:
        target.write_text(target.read_text(encoding="utf-8") + "\n# local customization\n", encoding="utf-8")
    return target


def test_normal_upgrade_migrates_only_the_known_legacy_craft(tmp_path: Path) -> None:
    root = _repo_root()
    home = tmp_path / "home"
    codex_home = tmp_path / "codex-home"
    project = tmp_path / "project"
    home.mkdir()
    project.mkdir()
    env = os.environ.copy()
    env.update({"HOME": str(home), "CODEX_HOME": str(codex_home)})

    global_targets = [
        codex_home / "neural-codex" / "skills",
        home / ".agents" / "skills",
        codex_home / "skills",
    ]
    project_targets = [project / ".agents" / "skills", project / ".codex" / "skills"]
    for target in global_targets + project_targets:
        _seed_legacy_craft(target)

    installed_project_setup = codex_home / "neural-codex" / "scripts" / "setup-project.sh"
    installed_project_setup.parent.mkdir(parents=True, exist_ok=True)
    installed_project_setup.write_text("#!/usr/bin/env bash\nexit 97\n", encoding="utf-8")
    installed_project_setup.chmod(0o755)

    global_run = subprocess.run(
        ["bash", "scripts/setup-global.sh"],
        cwd=root,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    project_run = subprocess.run(
        ["bash", str(installed_project_setup), "--path", str(project)],
        cwd=root,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )

    assert global_run.stdout.count("Migrated legacy craft skill") == 3
    assert project_run.stdout.count("Migrated legacy craft skill") == 2
    assert installed_project_setup.read_text(encoding="utf-8") == (root / "scripts" / "setup-project.sh").read_text(encoding="utf-8")
    assert os.access(installed_project_setup, os.X_OK)
    for target in global_targets + project_targets:
        text = (target / "craft" / "SKILL.md").read_text(encoding="utf-8")
        assert "# Craft" in text
        assert "# CRAFT Framework" not in text


def test_normal_upgrade_preserves_a_customized_legacy_craft(tmp_path: Path) -> None:
    root = _repo_root()
    home = tmp_path / "home"
    codex_home = tmp_path / "codex-home"
    home.mkdir()
    env = os.environ.copy()
    env.update({"HOME": str(home), "CODEX_HOME": str(codex_home)})

    customized_root = home / ".agents" / "skills"
    customized = _seed_legacy_craft(customized_root, customized=True)
    run = subprocess.run(
        ["bash", "scripts/setup-global.sh"],
        cwd=root,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Migrated customized legacy craft skill" in run.stdout
    assert "# Craft" in customized.read_text(encoding="utf-8")
    backup = customized_root / "craft.legacy-backup" / "SKILL.md"
    assert "# local customization" in backup.read_text(encoding="utf-8")


def test_customized_staging_craft_cannot_reinfect_migrated_destinations(tmp_path: Path) -> None:
    root = _repo_root()
    home = tmp_path / "home"
    codex_home = tmp_path / "codex-home"
    home.mkdir()
    env = os.environ.copy()
    env.update({"HOME": str(home), "CODEX_HOME": str(codex_home)})

    staging = codex_home / "neural-codex" / "skills"
    _seed_legacy_craft(staging)
    (staging / "craft" / "local-notes.md").write_text("keep me\n", encoding="utf-8")
    downstream = [home / ".agents" / "skills", codex_home / "skills"]
    for target in downstream:
        _seed_legacy_craft(target)

    run = subprocess.run(
        ["bash", "scripts/setup-global.sh"],
        cwd=root,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Migrated customized legacy craft skill" in run.stdout
    assert (staging / "craft.legacy-backup" / "local-notes.md").read_text(encoding="utf-8") == "keep me\n"
    for target in [staging] + downstream:
        text = (target / "craft" / "SKILL.md").read_text(encoding="utf-8")
        assert "# Craft" in text
        assert "# CRAFT Framework" not in text
