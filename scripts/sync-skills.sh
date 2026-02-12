#!/usr/bin/env bash
set -euo pipefail

# Sync repo skills into legacy or global locations.
# Usage: scripts/sync-skills.sh [--legacy] [--global] [--force]

LEGACY=0
GLOBAL=0
FORCE=0

for arg in "$@"; do
  case "$arg" in
    --legacy) LEGACY=1 ;;
    --global) GLOBAL=1 ;;
    --force) FORCE=1 ;;
  esac
done

if [[ "$LEGACY" == "0" && "$GLOBAL" == "0" ]]; then
  echo "No target selected. Use --legacy and/or --global."
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SRC_SKILLS="${REPO_ROOT}/.agents/skills"

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

if [[ "$LEGACY" == "1" ]]; then
  copy_dir "$SRC_SKILLS" "${REPO_ROOT}/.codex/skills"
  echo "Synced skills to ${REPO_ROOT}/.codex/skills"
fi

if [[ "$GLOBAL" == "1" ]]; then
  copy_dir "$SRC_SKILLS" "${HOME}/.agents/skills"
  echo "Synced skills to ${HOME}/.agents/skills"
fi
