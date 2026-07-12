from __future__ import annotations

import re
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
]

REQUIRED_SNIPPETS = [
    "no legacy hooks",
    "scripts/setup-global.sh",
    "scripts/setup-project.sh",
    "docs/hooks.md",
    "docs/verification.md",
    "/hooks",
    "gpt-5.6",
    '${codex_home:-$home/.codex}/neural-codex/scripts/setup-project.sh',
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


def test_readme_capability_inventories_match_the_repository() -> None:
    root = _repo_root()
    expected_prompts = {path.stem for path in (root / ".codex" / "prompts").glob("neural.*.md")}
    expected_skills = {path.name for path in (root / ".agents" / "skills").iterdir() if path.is_dir()}
    expected_agents = {path.parent.name for path in (root / "agents").glob("*/AGENTS.md")}

    for readme in README_FILES:
        text = _readme_text(readme)
        for prompt in expected_prompts:
            assert prompt in text, f"Prompt inventory drift in {readme}: {prompt}"
        for skill in expected_skills:
            assert skill in text, f"Skill inventory drift in {readme}: {skill}"
        for agent in expected_agents:
            assert f"agents/{agent}/agents.md" in text, f"Agent inventory drift in {readme}: {agent}"


def test_readmes_call_out_mcp_servers() -> None:
    for readme in README_FILES:
        text = _readme_text(readme)
        assert "mcp" in text, f"Missing MCP reference in {readme}"
        for server in REQUIRED_MCP:
            assert server in text, f"Missing MCP server '{server}' in {readme}"
        assert "codex --search" in text


def test_readmes_do_not_claim_unconfigured_advanced_features() -> None:
    unsupported_claims = ["**notifications**", "**history**", "**telemetry**", "**tui**"]
    for readme in README_FILES:
        text = _readme_text(readme)
        for claim in unsupported_claims:
            assert claim not in text, f"Unsupported config claim '{claim}' in {readme}"


def test_github_page_covers_current_hook_and_profile_flow() -> None:
    text = _read_text(_repo_root() / "docs" / "index.html")
    for snippet in [
        'id="hooks"',
        'id="profiles"',
        "LIFECYCLE_HOOKS",
        "GPT_5.6_PROFILES",
        "COMMAND_GUARD",
        "COMPACTION_RECOVERY",
        "/hooks",
        "scripts/setup-project.sh --path /path/to/project",
        'rel="icon" href="favicon.svg"',
    ]:
        assert snippet in text, f"GitHub Page missing current content: {snippet}"
    assert (_repo_root() / "docs" / "favicon.svg").is_file()


def test_core_documentation_links_resolve() -> None:
    root = _repo_root()
    documents = [
        root / "README.md",
        root / "AGENTS.md",
        root / "docs" / "README.md",
        root / "docs" / "AGENT-HARNESS.md",
        root / "docs" / "VERIFICATION.md",
    ]
    for document in documents:
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", _read_text(document)):
            if target.startswith(("http://", "https://", "#")):
                continue
            resolved = (document.parent / target.split("#", 1)[0]).resolve()
            assert resolved.exists(), f"Broken local link in {document}: {target}"
