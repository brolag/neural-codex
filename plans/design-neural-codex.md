# Technical Design: neural-codex (Codex-native port of neural-claude-code-plugin)

## Goals
- Port key neural-claude capabilities to Codex-native primitives (skills/prompts/AGENTS/config) without Claude-specific hooks/statusline/TTS.
- Provide a reusable toolkit: loop automation (Ralph), namespaced prompts, MCP integrations, templates, agents, and notification hook.
- Keep everything file-based and portable (bash + jq + Git + Codex CLI).

## Non-Goals
- Re-implement Claude plugin hooks, statusline streaming, or TTS.
- Build a marketplace/installer; distribution is repo-based.

## Constraints
- Codex supports SKILL.md, custom prompts in ~/.codex/prompts, AGENTS.md, config.toml (with mcpServers, notify). No session hooks.
- Shell tools available: bash, jq, git, timeout.
- Keep tasks small; loop is test-gated; avoid recursive Codex invocations.

## Architecture
- **Ralph Loop**: `scripts/ralph-loop.sh` drives iterations, claims tasks in `plans/prd.json`, logs to `plans/progress.jsonl`, runs Codex, runs tests, commits on green, rolls back on red, respects attempts/depends_on, lock-protected.
- **Prompts (namespaced `neural.*`)**:
  - Loop control: loop-start/status/plan/cancel, plan-execute.
  - Memory: recall, route, memory update/read.
  - Knowledge ingest: gh-learn, yt-learn.
  - Patterning: evolve (patterns/anti-patterns/tests).
  - Planning: plan (short actionable plan).
  - Research: research (MCP-backed).
  - Todos: todo-new, todo-check.
  - Output styles: presets.
  - Meta: meta-agent/skill scaffolding (optional).
- **Templates**: expertise.template.yaml, todo-workflow.md under `.codex/templates/`.
- **Agents**: convert key profiles to AGENTS.md (either per-agent in agents/ or consolidated). Include reset/routing guidance to avoid persona bleed.
- **MCP**: Configure in `.codex/config.toml` (chrome-devtools, github, playwright/browser, search/Exa). No `.claude` JSONs.
- **Notify**: Optional `notify` hook calling `telegram_notify.sh` or similar; event source is Codex `notify`.
- **Memory Store**: Files (expertise notes, progress log). Manual update via prompts/scripts (no auto hooks).

## Data Flows
- Tasks: `plans/prd.json` (passes/attempts/status/depends_on/in_progress).
- Progress: `plans/progress.jsonl` (JSONL entries per iteration).
- Templates: `.codex/templates/`.
- Prompts: `.codex/prompts/`.
- Agents: `agents/*/AGENTS.md` or root `AGENTS.md`.
- Config: `.codex/config.toml` (MCP, notify).

## Key Risks & Mitigations
- No hooks/statusline: make loop explicit; optional cron/polling; use `notify` for alerts.
- JSON corruption: atomic writes (tmp + mv); jq-based mutations.
- Stale memory: provide explicit memory update/read prompts; optionally run them every N iterations.
- Agent bleed: add reset language in router/AGENTS; namespace prompts.
- Env deps (yt/gh learn): document Python deps; guard scripts with checks.
- MCP/headless: ensure configs use headless-safe commands; document requirements.

## Deliverables
- Updated `plans/prd.json` (tasks defined).
- Prompts under `.codex/prompts/neural.*.md`.
- Templates under `.codex/templates/`.
- Agents converted to AGENTS.md.
- `.codex/config.toml` with MCP stubs; optional notify stub.
- Scripts: `scripts/ralph-loop.sh`, `scripts/telegram_notify.sh` (optional), any support scripts for yt/gh ingest.
- README/notes summarizing unsupported features and usage.
