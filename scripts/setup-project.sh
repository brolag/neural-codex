#!/usr/bin/env bash
set -euo pipefail

# Set up neural-codex assets inside a project from global install.
# Usage: scripts/setup-project.sh [--force] [--path /path/to/project]

FORCE=0
PROJECT_ROOT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force) FORCE=1; shift ;;
    --path) PROJECT_ROOT="$2"; shift 2 ;;
    *) shift ;;
  esac
done

if [[ -z "${PROJECT_ROOT}" ]]; then
  PROJECT_ROOT="$(pwd)"
fi

CODEX_ROOT="${CODEX_HOME:-${HOME}/.codex}"
GLOBAL_ROOT="${CODEX_ROOT}/neural-codex"
if [[ ! -d "${GLOBAL_ROOT}" ]]; then
  echo "Global neural-codex not found. Run scripts/setup-global.sh first."
  exit 1
fi

copy_dir() {
  local src="$1"
  local dst="$2"
  mkdir -p "$dst"
  for f in "$src"/*; do
    [[ -e "$f" ]] || continue
    local base
    base="$(basename "$f")"
    [[ "$base" == "__pycache__" || "$base" == ".DS_Store" ]] && continue
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

echo "Setting up project at ${PROJECT_ROOT}"

mkdir -p "${PROJECT_ROOT}/.codex/prompts" "${PROJECT_ROOT}/.codex/templates"
mkdir -p "${PROJECT_ROOT}/.codex/hooks"
mkdir -p "${PROJECT_ROOT}/.agents/skills" "${PROJECT_ROOT}/.codex/skills"
mkdir -p "${PROJECT_ROOT}/scripts/neural-codex" "${PROJECT_ROOT}/plans"

copy_dir "${GLOBAL_ROOT}/prompts" "${PROJECT_ROOT}/.codex/prompts"
copy_dir "${GLOBAL_ROOT}/templates" "${PROJECT_ROOT}/.codex/templates"
copy_dir "${GLOBAL_ROOT}/skills" "${PROJECT_ROOT}/.agents/skills"

# Legacy fallback (optional)
copy_dir "${GLOBAL_ROOT}/skills" "${PROJECT_ROOT}/.codex/skills"
copy_dir "${GLOBAL_ROOT}/scripts" "${PROJECT_ROOT}/scripts/neural-codex"
copy_dir "${GLOBAL_ROOT}/hooks" "${PROJECT_ROOT}/.codex/hooks"

if [[ -f "${GLOBAL_ROOT}/hooks.json" ]]; then
  if [[ "${FORCE}" == "1" || ! -f "${PROJECT_ROOT}/.codex/hooks.json" ]]; then
    cp "${GLOBAL_ROOT}/hooks.json" "${PROJECT_ROOT}/.codex/hooks.json"
  fi
fi

# Seed config.toml if missing
if [[ -f "${GLOBAL_ROOT}/config.toml" ]]; then
  if [[ "$FORCE" == "1" || ! -f "${PROJECT_ROOT}/.codex/config.toml" ]]; then
    cp "${GLOBAL_ROOT}/config.toml" "${PROJECT_ROOT}/.codex/config.toml"
  fi
fi

# Seed PRD/progress if missing
if [[ ! -f "${PROJECT_ROOT}/plans/prd.json" && -f "${GLOBAL_ROOT}/templates/prd.template.json" ]]; then
  cp "${GLOBAL_ROOT}/templates/prd.template.json" "${PROJECT_ROOT}/plans/prd.json"
fi

if [[ ! -f "${PROJECT_ROOT}/plans/progress.jsonl" && -f "${GLOBAL_ROOT}/templates/progress.template.jsonl" ]]; then
  cp "${GLOBAL_ROOT}/templates/progress.template.jsonl" "${PROJECT_ROOT}/plans/progress.jsonl"
fi

echo "Done. Project prompts/templates/scripts/hooks installed. Review hooks with /hooks."
