#!/usr/bin/env bash
set -euo pipefail

# Install neural-codex assets into CODEX_HOME (defaults to ~/.codex).
# Usage: scripts/setup-global.sh [--force]

FORCE=0
if [[ "${1:-}" == "--force" ]]; then
  FORCE=1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

CODEX_ROOT="${CODEX_HOME:-${HOME}/.codex}"
GLOBAL_ROOT="${CODEX_ROOT}/neural-codex"
GLOBAL_PROMPTS="${GLOBAL_ROOT}/prompts"
GLOBAL_TEMPLATES="${GLOBAL_ROOT}/templates"
GLOBAL_SKILLS="${GLOBAL_ROOT}/skills"
GLOBAL_SCRIPTS="${GLOBAL_ROOT}/scripts"
GLOBAL_HOOKS="${GLOBAL_ROOT}/hooks"

SRC_PROMPTS="${REPO_ROOT}/.codex/prompts"
SRC_TEMPLATES="${REPO_ROOT}/.codex/templates"
SRC_SKILLS="${REPO_ROOT}/.agents/skills"
SRC_SCRIPTS="${REPO_ROOT}/scripts"
SRC_CONFIG="${REPO_ROOT}/.codex/config.toml"
SRC_HOOKS="${REPO_ROOT}/.codex/hooks"
SRC_HOOKS_CONFIG="${REPO_ROOT}/.codex/hooks.json"
SRC_PROFILES="${REPO_ROOT}/.codex/profiles"

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

echo "Installing neural-codex assets to ${GLOBAL_ROOT}"
mkdir -p "${GLOBAL_ROOT}"

copy_dir "${SRC_PROMPTS}" "${GLOBAL_PROMPTS}"
copy_dir "${SRC_TEMPLATES}" "${GLOBAL_TEMPLATES}"
migrate_known_legacy_craft "${SRC_SKILLS}" "${GLOBAL_SKILLS}"
copy_dir "${SRC_SKILLS}" "${GLOBAL_SKILLS}"
copy_dir "${SRC_SCRIPTS}" "${GLOBAL_SCRIPTS}"
copy_dir "${SRC_HOOKS}" "${GLOBAL_HOOKS}"

# Keep the installed upgrade entrypoints current even when other existing
# scripts are preserved. A stale setup-project.sh cannot apply new migrations.
for installer in setup-global.sh setup-project.sh; do
  if [[ -f "${SRC_SCRIPTS}/${installer}" ]]; then
    cp "${SRC_SCRIPTS}/${installer}" "${GLOBAL_SCRIPTS}/${installer}"
    chmod +x "${GLOBAL_SCRIPTS}/${installer}"
  fi
done

if [[ -f "${SRC_HOOKS_CONFIG}" ]]; then
  if [[ "${FORCE}" == "1" || ! -f "${GLOBAL_ROOT}/hooks.json" ]]; then
    cp "${SRC_HOOKS_CONFIG}" "${GLOBAL_ROOT}/hooks.json"
  fi
fi

# Install prompts into Codex global prompts dir (required for slash commands)
mkdir -p "${CODEX_ROOT}/prompts"
copy_dir "${GLOBAL_PROMPTS}" "${CODEX_ROOT}/prompts"

# Install skills into Codex global skills dir (optional, for autodiscovery)
mkdir -p "${HOME}/.agents/skills"
migrate_known_legacy_craft "${SRC_SKILLS}" "${HOME}/.agents/skills"
copy_dir "${GLOBAL_SKILLS}" "${HOME}/.agents/skills"

# Legacy fallback (optional)
mkdir -p "${CODEX_ROOT}/skills"
migrate_known_legacy_craft "${SRC_SKILLS}" "${CODEX_ROOT}/skills"
copy_dir "${GLOBAL_SKILLS}" "${CODEX_ROOT}/skills"

# Store a config stub for project setup
if [[ -f "${SRC_CONFIG}" ]]; then
  if [[ "$FORCE" == "1" || ! -f "${GLOBAL_ROOT}/config.toml" ]]; then
    cp "${SRC_CONFIG}" "${GLOBAL_ROOT}/config.toml"
  fi
fi

# Codex 0.134+ loads named profiles from $CODEX_HOME/<name>.config.toml.
for profile in "${SRC_PROFILES}"/*.config.toml; do
  [[ -e "${profile}" ]] || continue
  target="${CODEX_ROOT}/$(basename "${profile}")"
  if [[ "${FORCE}" == "1" || ! -f "${target}" ]]; then
    cp "${profile}" "${target}"
  fi
done

echo "Done. Restart Codex to pick up prompts and profiles."
