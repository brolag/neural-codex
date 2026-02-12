from __future__ import annotations

from pathlib import Path

CORE_SKILLS = [
    "memory-system",
    "pattern-detector",
    "prompt-engineering",
    "plan-execute",
    "worktree-manager",
    "youtube-learner",
]


def _skill_path(name: str) -> Path:
    repo_root = Path(__file__).resolve().parents[1]
    return repo_root / ".agents" / "skills" / name / "SKILL.md"


def _read_skill(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_core_skills_exist() -> None:
    for name in CORE_SKILLS:
        path = _skill_path(name)
        assert path.exists(), f"Missing skill: {path}"


def test_core_skills_have_usage_examples() -> None:
    for name in CORE_SKILLS:
        text = _read_skill(_skill_path(name))
        assert "Usage Examples" in text, f"Missing Usage Examples in {name}"


def test_core_skills_use_codex_paths() -> None:
    for name in CORE_SKILLS:
        text = _read_skill(_skill_path(name))
        assert (
            "plans/" in text or ".codex/" in text
        ), f"Missing Codex path reference in {name}"
