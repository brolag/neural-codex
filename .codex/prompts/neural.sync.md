---
description: Sync neural-codex prompts, templates, skills, and scripts
argument-hint: MODE="status|global|project|all" [--force] [--path <dir>]
---

Sync neural-codex assets using the setup scripts.

Modes:
- status: report whether global and project installs exist
- global: run `scripts/setup-global.sh`
- project: run `scripts/setup-project.sh` (optionally `--path`)
- all: run global then project

Steps:
1) If MODE is status, check for:
   - `~/.codex/neural-codex/`
   - `~/.codex/prompts/`
   - `.codex/` in the current project
2) If MODE is global, run:
   - `scripts/setup-global.sh [--force]`
3) If MODE is project, run:
   - `scripts/setup-project.sh [--force] [--path <dir>]`
4) If MODE is all, run global then project.
5) Remind the user to restart Codex after global install to load prompts.
