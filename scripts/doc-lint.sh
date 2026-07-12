#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

REQUIRED_FILES=(
  "AGENTS.md"
  "ARCHITECTURE.md"
  "docs/README.md"
  "docs/AGENT-HARNESS.md"
  "docs/DESIGN.md"
  "docs/PLANS.md"
  "docs/PRODUCT_SENSE.md"
  "docs/QUALITY_SCORE.md"
  "docs/RELIABILITY.md"
  "docs/SECURITY.md"
  "docs/HOOKS.md"
  "docs/FRONTEND.md"
  "docs/design-docs/README.md"
  "docs/exec-plans/README.md"
  "docs/product-specs/README.md"
  "docs/references/README.md"
  "docs/generated/README.md"
)

REQUIRED_AGENTS_REFS=(
  "docs/README.md"
  "docs/PLANS.md"
  "ARCHITECTURE.md"
  "docs/HOOKS.md"
)

REQUIRED_DOCS_INDEX_TERMS=(
  "design-docs"
  "exec-plans"
  "product-specs"
  "references"
  "generated"
  "HOOKS.md"
)

failures=()

have_rg=0
if command -v rg >/dev/null 2>&1; then
  have_rg=1
fi

contains_text() {
  local file="$1"
  local needle="$2"
  if [[ "$have_rg" == "1" ]]; then
    rg -q --fixed-strings "$needle" "$file"
  else
    grep -qF "$needle" "$file"
  fi
}

for rel in "${REQUIRED_FILES[@]}"; do
  path="${ROOT_DIR}/${rel}"
  if [[ ! -f "$path" ]]; then
    failures+=("Missing required file: ${rel}")
    continue
  fi
  if [[ ! -s "$path" ]]; then
    failures+=("Empty required file: ${rel}")
  fi
done

agents_path="${ROOT_DIR}/AGENTS.md"
if [[ -f "$agents_path" ]]; then
  for ref in "${REQUIRED_AGENTS_REFS[@]}"; do
    if ! contains_text "$agents_path" "$ref"; then
      failures+=("AGENTS.md missing reference: ${ref}")
    fi
  done
else
  failures+=("Missing required file: AGENTS.md")
fi

docs_index_path="${ROOT_DIR}/docs/README.md"
if [[ -f "$docs_index_path" ]]; then
  for term in "${REQUIRED_DOCS_INDEX_TERMS[@]}"; do
    if ! contains_text "$docs_index_path" "$term"; then
      failures+=("docs/README.md missing section for: ${term}")
    fi
  done
else
  failures+=("Missing required file: docs/README.md")
fi

if [[ "${#failures[@]}" -gt 0 ]]; then
  for item in "${failures[@]}"; do
    echo "[FAIL] ${item}"
  done
  exit 1
fi

echo "[OK] Doc structure validated"
