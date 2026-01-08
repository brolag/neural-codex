# Task List: neural-codex port

## Setup
- [x] Ensure script executables (`chmod +x scripts/ralph-loop.sh`), jq/git/timeout present.
- [x] Create `.codex/` scaffolding (prompts/, templates/, config.toml).
- [x] Add global setup (`scripts/setup-global.sh`) and project setup (`scripts/setup-project.sh`) commands.
- [x] Add setup README (`README-neural-codex.md`).

## Prompts (namespaced `neural.*`)
- [ ] Add loop prompts: loop-start/status/plan/cancel, plan-execute.
- [ ] Add memory prompts: recall, route, memory-update/read.
- [ ] Add ingest prompts: gh-learn, yt-learn (document Python deps).
- [ ] Add pattern prompt: evolve (reads prd/progress/git).
- [ ] Add plan prompt: plan (short actionable plan).
- [ ] Add research prompt: research (MCP-backed search).
- [ ] Add todo prompts: todo-new, todo-check.
- [ ] Add output-style presets.
- [ ] (Optional) meta-agent/skill scaffolding prompt.

## Templates
- [ ] Copy expertise.template.yaml to `.codex/templates/` (Codex-friendly placeholders).
- [ ] Copy todo-workflow.md to `.codex/templates/`.

## Agents
- [ ] Convert key agent profiles to AGENTS.md (agents/*/ or consolidated).
- [ ] Add reset/routing guidance to avoid persona bleed.

## MCP & Config
- [ ] Create `.codex/config.toml` with MCP stubs (chrome-devtools, github, playwright/browser, search/Exa).
- [ ] Add optional `notify` stub (can point to telegram_notify.sh).

## Scripts
- [ ] Keep `scripts/ralph-loop.sh` (done) and (optional) `ralph-once.sh`.
- [ ] Add `scripts/telegram_notify.sh` template (optional) and document env vars.
- [ ] Add support scripts for yt/gh ingest if needed (with dependency notes).

## Memory & Data
- [ ] Keep `plans/prd.json` and `plans/progress.jsonl` as task/log stores.
- [ ] Add a memory update/read workflow (prompt or script) to replace hook-based indexing.

## Docs
- [ ] README/notes: what’s ported vs unsupported (hooks/statusline/TTS/marketplace), usage of prompts/loop, MCP setup, deps.

## Validation
- [ ] Smoke test prompts resolve and run.
- [ ] Run Ralph loop against sample tasks (small, test-gated).
- [ ] Validate MCP connectivity (chrome-devtools/github/search).
- [ ] Validate notify script (if enabled).
