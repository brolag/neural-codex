from __future__ import annotations

from pathlib import Path

README_FILES = ["README.md", "README-neural-codex.md"]

REQUIRED_PROMPTS = [
    "neural.loop-start",
    "neural.plan",
    "neural.sync",
    "neural.changelog-architect",
    "neural.todo-new",
    "neural.todo-check",
]

REQUIRED_MCP = [
    "chrome-devtools",
    "github",
    "search",
    "playwright",
]

REQUIRED_SNIPPETS = [
    "no legacy hooks",
    "scripts/setup-global.sh",
    "scripts/setup-project.sh",
]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _readme_text(name: str) -> str:
    return _read_text(_repo_root() / name).lower()


def test_readmes_cover_prompts_and_setup() -> None:
    for readme in README_FILES:
        text = _readme_text(readme)
        for prompt in REQUIRED_PROMPTS:
            assert prompt in text, f"Missing prompt '{prompt}' in {readme}"
        for snippet in REQUIRED_SNIPPETS:
            assert snippet in text, f"Missing '{snippet}' in {readme}"


def test_readmes_call_out_mcp_servers() -> None:
    for readme in README_FILES:
        text = _readme_text(readme)
        assert "mcp" in text, f"Missing MCP reference in {readme}"
        for server in REQUIRED_MCP:
            assert server in text, f"Missing MCP server '{server}' in {readme}"
