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

LEGACY_CRAFT_SHA256="ec6c84c5e8add0ea8cd9c1eb2fe9244fd60a4dd8a12e71181970c884cbabb2bc"

file_sha256() {
  local path="$1"
  if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$path" | awk '{print $1}'
  else
    sha256sum "$path" | awk '{print $1}'
  fi
}

migrate_known_legacy_craft() {
  local src_root="$1"
  local dst_root="$2"
  local dst_craft="${dst_root}/craft"
  local dst_skill="${dst_craft}/SKILL.md"

  [[ "$FORCE" == "0" && -f "$dst_skill" ]] || return 0

  local hash
  hash="$(file_sha256 "$dst_skill")"
  if [[ "$hash" != "$LEGACY_CRAFT_SHA256" ]]; then
    grep -qF "# CRAFT Framework" "$dst_skill" || return 0
    grep -qF "CRAFT = Context, Requirements, Actions, Flow, Tests." "$dst_skill" || return 0
  fi

  local extra
  extra="$(find "$dst_craft" -mindepth 1 -maxdepth 1 ! -name SKILL.md -print -quit)"
  if [[ "$hash" != "$LEGACY_CRAFT_SHA256" || -n "$extra" ]]; then
    local backup="${dst_root}/craft.legacy-backup"
    if [[ -e "$backup" ]]; then
      echo "Cannot migrate customized legacy craft skill: backup already exists at ${backup}." >&2
      return 1
    fi
    mv "$dst_craft" "$backup"
    cp -R "${src_root}/craft" "$dst_craft"
    echo "Migrated customized legacy craft skill at ${dst_craft}; preserved the original at ${backup}."
    return 0
  fi

  rm -rf "$dst_craft"
  cp -R "${src_root}/craft" "$dst_craft"
  echo "Migrated legacy craft skill at ${dst_craft}."
}

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
migrate_known_legacy_craft "${GLOBAL_ROOT}/skills" "${PROJECT_ROOT}/.agents/skills"
copy_dir "${GLOBAL_ROOT}/skills" "${PROJECT_ROOT}/.agents/skills"

# Legacy fallback (optional)
migrate_known_legacy_craft "${GLOBAL_ROOT}/skills" "${PROJECT_ROOT}/.codex/skills"
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
