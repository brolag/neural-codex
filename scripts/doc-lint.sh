#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

REQUIRED_FILES=(
  "README.md"
  "AGENTS.md"
  "ARCHITECTURE.md"
  ".agents/plugins/marketplace.json"
  "plugins/neural-codex/.codex-plugin/plugin.json"
  "plugins/neural-codex/hooks/hooks.json"
  "docs/README.md"
  "docs/AGENT-HARNESS.md"
  "docs/CONFIGURATION.md"
  "docs/HOOKS.md"
  "docs/VERIFICATION.md"
  "docs/WORKFLOW.md"
  "docs/index.html"
)

CORE_SKILLS=(discover spec craft vet exercise)
DOCS_WITH_COMPLETE_FLOW=(
  "README.md"
  "docs/README.md"
  "docs/WORKFLOW.md"
  "docs/index.html"
)

STALE_PATTERNS=(
  "/prompts:"
  ".codex/prompts"
  "scripts/setup-global.sh"
  "scripts/setup-project.sh"
  "scripts/ralph-loop.sh"
  ".agents/skills/"
)

failures=()

contains_text() {
  local file="$1"
  local needle="$2"
  if command -v rg >/dev/null 2>&1; then
    rg -q --fixed-strings "$needle" "$file"
  else
    grep -qF "$needle" "$file"
  fi
}

for rel in "${REQUIRED_FILES[@]}"; do
  if [[ ! -s "${ROOT_DIR}/${rel}" ]]; then
    failures+=("Missing or empty required file: ${rel}")
  fi
done

for skill in "${CORE_SKILLS[@]}"; do
  skill_file="plugins/neural-codex/skills/${skill}/SKILL.md"
  if [[ ! -s "${ROOT_DIR}/${skill_file}" ]]; then
    failures+=("Missing skill: ${skill_file}")
  fi
  for rel in "${DOCS_WITH_COMPLETE_FLOW[@]}"; do
    if [[ -f "${ROOT_DIR}/${rel}" ]] && ! contains_text "${ROOT_DIR}/${rel}" "\$${skill}"; then
      failures+=("${rel} does not name \$${skill}")
    fi
  done
done

for pattern in "${STALE_PATTERNS[@]}"; do
  while IFS= read -r rel; do
    [[ -z "$rel" ]] && continue
    if contains_text "${ROOT_DIR}/${rel}" "$pattern"; then
      failures+=("Stale reference ${pattern} in ${rel}")
    fi
  done < <(printf '%s\n' README.md AGENTS.md ARCHITECTURE.md docs/*.md docs/index.html)
done

if [[ "${#failures[@]}" -gt 0 ]]; then
  printf '[FAIL] %s\n' "${failures[@]}"
  exit 1
fi

echo "[OK] Plugin documentation validated"
