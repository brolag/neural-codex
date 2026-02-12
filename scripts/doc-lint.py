#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

REQUIRED_FILES = [
    "AGENTS.md",
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


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    failures: list[str] = []

    for rel in REQUIRED_FILES:
        path = root / rel
        if not path.exists():
            failures.append(f"Missing required file: {rel}")
            continue
        if not read_text(path):
            failures.append(f"Empty required file: {rel}")

    agents_text = read_text(root / "AGENTS.md") if (root / "AGENTS.md").exists() else ""
    for ref in REQUIRED_AGENTS_REFERENCES:
        if ref not in agents_text:
            failures.append(f"AGENTS.md missing reference: {ref}")

    docs_index_text = read_text(root / "docs/README.md") if (root / "docs/README.md").exists() else ""
    for term in REQUIRED_DOCS_INDEX_TERMS:
        if term not in docs_index_text:
            failures.append(f"docs/README.md missing section for: {term}")

    if failures:
        for item in failures:
            print(f"[FAIL] {item}")
        return 1

    print("[OK] Doc structure validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
