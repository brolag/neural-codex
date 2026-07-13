from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE_SKILLS = ("discover", "spec", "craft", "vet", "exercise")
FLOW_DOCS = (
    ROOT / "README.md",
    ROOT / "docs" / "README.md",
    ROOT / "docs" / "WORKFLOW.md",
    ROOT / "docs" / "index.html",
)
PUBLIC_DOCS = (
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / "ARCHITECTURE.md",
    *(ROOT / "docs").glob("*.md"),
    ROOT / "docs" / "index.html",
)


def test_focused_documentation_inventory_exists() -> None:
    expected = {
        ".nojekyll",
        "AGENT-HARNESS.md",
        "CONFIGURATION.md",
        "HOOKS.md",
        "README.md",
        "VERIFICATION.md",
        "WORKFLOW.md",
        "favicon.svg",
        "index.html",
    }
    actual = {path.name for path in (ROOT / "docs").iterdir() if path.is_file()}
    assert actual == expected


def test_complete_flow_is_named_where_users_enter() -> None:
    for document in FLOW_DOCS:
        text = document.read_text(encoding="utf-8")
        for name in CORE_SKILLS:
            assert f"${name}" in text, f"Missing ${name} in {document.relative_to(ROOT)}"


def test_public_docs_do_not_advertise_removed_inventory() -> None:
    banned = (
        "/prompts:",
        ".codex/prompts",
        ".agents/skills/",
        "scripts/setup-global.sh",
        "scripts/setup-project.sh",
        "scripts/ralph-loop.sh",
    )
    for document in PUBLIC_DOCS:
        text = document.read_text(encoding="utf-8")
        for term in banned:
            assert term not in text, f"Stale {term!r} in {document.relative_to(ROOT)}"


def test_readme_documents_official_marketplace_install_and_hook_trust() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "codex plugin marketplace add brolag/neural-codex" in text
    assert "codex plugin add neural-codex@neural-codex" in text
    assert "codex plugin list" in text
    assert "does not trust hooks automatically" in text
    assert "does not change `~/.codex/config.toml`" in text


def test_github_page_has_required_sections_and_local_links() -> None:
    page = ROOT / "docs" / "index.html"
    text = page.read_text(encoding="utf-8")
    for section in ("workflow", "hooks", "install", "structure", "configuration"):
        assert f'id="{section}"' in text

    for target in re.findall(r'href="([^"#][^"]*)"', text):
        if target.startswith(("https://", "http://", "mailto:")):
            continue
        path = (page.parent / target).resolve()
        assert path.exists(), f"Broken local link {target}"

    assert "https://github.com/brolag/neural-codex/blob/main/docs/WORKFLOW.md" in text
    assert "https://github.com/brolag/neural-codex/blob/main/docs/CONFIGURATION.md" in text
    assert "https://github.com/brolag/neural-codex/blob/main/docs/VERIFICATION.md" in text


def test_github_page_keeps_visible_gray_matrix_with_reduced_motion_fallback() -> None:
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert 'id="matrix-bg"' in text
    assert "--matrix: #f7f7f7" in text
    assert "drawStaticMatrix" in text
    assert "prefers-reduced-motion: reduce" in text
    assert "#matrix-bg { display: none; }" not in text


def test_configuration_is_advisory_and_current() -> None:
    text = (ROOT / "docs" / "CONFIGURATION.md").read_text(encoding="utf-8")
    assert not re.search(r'^model = "gpt-5\.6"$', text, re.MULTILINE)
    assert "GPT-5.6 prompting principles" in text
    assert "The 'gpt-5.6' model is not supported when using Codex with a ChatGPT account." in text
    assert 'approval_policy = "on-request"' in text
    assert 'sandbox_mode = "workspace-write"' in text
    assert "does not install or edit Codex configuration" in text
