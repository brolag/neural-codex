#!/usr/bin/env bash
set -euo pipefail

# Install neural-codex assets into ~/.codex (global).
# Usage: scripts/setup-global.sh [--force]

FORCE=0
if [[ "${1:-}" == "--force" ]]; then
  FORCE=1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

GLOBAL_ROOT="${HOME}/.codex/neural-codex"
GLOBAL_PROMPTS="${GLOBAL_ROOT}/prompts"
GLOBAL_TEMPLATES="${GLOBAL_ROOT}/templates"
GLOBAL_SKILLS="${GLOBAL_ROOT}/skills"
GLOBAL_SCRIPTS="${GLOBAL_ROOT}/scripts"

SRC_PROMPTS="${REPO_ROOT}/.codex/prompts"
SRC_TEMPLATES="${REPO_ROOT}/.codex/templates"
SRC_SKILLS="${REPO_ROOT}/.agents/skills"
SRC_SCRIPTS="${REPO_ROOT}/scripts"
SRC_CONFIG="${REPO_ROOT}/.codex/config.toml"

copy_dir() {
  local src="$1"
  local dst="$2"
  mkdir -p "$dst"
  for f in "$src"/*; do
    [[ -e "$f" ]] || continue
    local base
    base="$(basename "$f")"
    if [[ "$FORCE" == "1" ]]; then
      rm -rf "$dst/$base"
      cp -R "$f" "$dst/$base"
      continue
    fi
    if [[ ! -e "$dst/$base" ]]; then
      cp -R "$f" "$dst/$base"
    fi
  done
}

echo "Installing neural-codex assets to ${GLOBAL_ROOT}"
mkdir -p "${GLOBAL_ROOT}"

copy_dir "${SRC_PROMPTS}" "${GLOBAL_PROMPTS}"
copy_dir "${SRC_TEMPLATES}" "${GLOBAL_TEMPLATES}"
copy_dir "${SRC_SKILLS}" "${GLOBAL_SKILLS}"
copy_dir "${SRC_SCRIPTS}" "${GLOBAL_SCRIPTS}"

# Install prompts into Codex global prompts dir (required for slash commands)
mkdir -p "${HOME}/.codex/prompts"
copy_dir "${GLOBAL_PROMPTS}" "${HOME}/.codex/prompts"

# Install skills into Codex global skills dir (optional, for autodiscovery)
mkdir -p "${HOME}/.agents/skills"
copy_dir "${GLOBAL_SKILLS}" "${HOME}/.agents/skills"

# Legacy fallback (optional)
mkdir -p "${HOME}/.codex/skills"
copy_dir "${GLOBAL_SKILLS}" "${HOME}/.codex/skills"

# Store a config stub for project setup
if [[ -f "${SRC_CONFIG}" ]]; then
  if [[ "$FORCE" == "1" || ! -f "${GLOBAL_ROOT}/config.toml" ]]; then
    cp "${SRC_CONFIG}" "${GLOBAL_ROOT}/config.toml"
  fi
fi

echo "Done. Restart Codex to pick up new prompts."
