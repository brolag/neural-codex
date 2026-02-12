from __future__ import annotations

from pathlib import Path

AGENT_FILES = [
    "agents/multi-ai/AGENTS.md",
    "agents/dispatcher/AGENTS.md",
    "agents/meta-agent/AGENTS.md",
]

TOOL_MARKERS = ["shell_command", "apply_patch", "rg"]
FORBIDDEN_MARKERS = ["statusline", "tts", "marketplace"]


def _agent_path(relpath: str) -> Path:
    repo_root = Path(__file__).resolve().parents[1]
    return repo_root / relpath


def _read_agent(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_agents_exist() -> None:
    for relpath in AGENT_FILES:
        path = _agent_path(relpath)
        assert path.exists(), f"Missing agent: {path}"


def test_agents_reference_codex_tools() -> None:
    for relpath in AGENT_FILES:
        text = _read_agent(_agent_path(relpath))
        assert any(marker in text for marker in TOOL_MARKERS), (
            f"Missing Codex tool reference in {relpath}"
        )


def test_agents_avoid_legacy_hooks() -> None:
    for relpath in AGENT_FILES:
        text = _read_agent(_agent_path(relpath)).lower()
        for marker in FORBIDDEN_MARKERS:
            assert marker not in text, f"Found {marker} reference in {relpath}"
