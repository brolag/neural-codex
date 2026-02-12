from __future__ import annotations

from pathlib import Path

REQUIRED_FILES = [
    "ARCHITECTURE.md",
    "docs/README.md",
    "docs/AGENT-HARNESS.md",
    "docs/DESIGN.md",
    "docs/PLANS.md",
    "docs/PRODUCT_SENSE.md",
    "docs/QUALITY_SCORE.md",
    "docs/RELIABILITY.md",
    "docs/SECURITY.md",
    "docs/FRONTEND.md",
    "docs/design-docs/README.md",
    "docs/exec-plans/README.md",
    "docs/product-specs/README.md",
    "docs/references/README.md",
    "docs/generated/README.md",
]

REQUIRED_AGENTS_REFERENCES = [
    "docs/README.md",
    "docs/PLANS.md",
    "ARCHITECTURE.md",
]

REQUIRED_DOCS_INDEX_TERMS = [
    "design-docs",
    "exec-plans",
    "product-specs",
    "references",
    "generated",
]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_required_docs_exist() -> None:
    root = _repo_root()
    for rel in REQUIRED_FILES:
        path = root / rel
        assert path.exists(), f"Missing required doc: {rel}"
        assert path.read_text(encoding="utf-8").strip(), f"Empty doc: {rel}"


def test_agents_mentions_core_docs() -> None:
    text = _read_text(_repo_root() / "AGENTS.md")
    for ref in REQUIRED_AGENTS_REFERENCES:
        assert ref in text, f"AGENTS.md missing reference: {ref}"


def test_docs_index_has_sections() -> None:
    text = _read_text(_repo_root() / "docs/README.md")
    for term in REQUIRED_DOCS_INDEX_TERMS:
        assert term in text, f"docs/README.md missing term: {term}"
