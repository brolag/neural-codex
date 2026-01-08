from __future__ import annotations

from pathlib import Path

SCRIPT_NAMES = [
    "memory_read.py",
    "memory_write.py",
    "youtube-transcript.py",
]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _script_path(name: str) -> Path:
    return _repo_root() / "scripts" / name


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_scripts_support_files_exist() -> None:
    for name in SCRIPT_NAMES:
        path = _script_path(name)
        assert path.exists(), f"Missing script: {path}"


def test_memory_skill_references_helper_scripts() -> None:
    path = _repo_root() / ".codex" / "skills" / "memory-system" / "SKILL.md"
    text = _read_text(path)
    assert "scripts/memory_write.py" in text
    assert "scripts/memory_read.py" in text


def test_youtube_references_helper_script() -> None:
    skill_path = _repo_root() / ".codex" / "skills" / "youtube-learner" / "SKILL.md"
    prompt_path = _repo_root() / ".codex" / "prompts" / "neural.yt-learn.md"
    skill_text = _read_text(skill_path)
    prompt_text = _read_text(prompt_path)
    assert "scripts/youtube-transcript.py" in skill_text
    assert "scripts/youtube-transcript.py" in prompt_text
