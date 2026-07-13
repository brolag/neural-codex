# neural-codex - Project Instructions

## Overview
- Codex-native port of the neural workflow features: Ralph loop, lifecycle hooks, namespaced prompts, templates, MCP, and agents.
- All state is file-based: `plans/prd.json` (tasks), `plans/progress.jsonl` (log), `.codex/prompts/` (prompts), `.codex/templates/` (templates), `scripts/` (automation).
- Hooks use Codex's native `.codex/hooks.json` contract; no Claude hook paths, statusline, or TTS.
- Setup and usage reference: `README-neural-codex.md`.

## Workflow
- Use Ralph loop: `scripts/ralph-loop.sh <iters>` with `TEST_CMD` set as needed.
- Keep tasks small; follow PRD `depends_on` and attempts limits.
- Use namespaced prompts (`neural.*`) for loop control, recall, plan, evolve, research, todo, output styles.
- Memory is explicit: append to `plans/progress.jsonl` or expertise files; no auto indexing.

## Knowledge map
- This file is the entry map for agent instructions; keep it short.
- Harness guidance: `docs/AGENT-HARNESS.md`.
- Docs index: `docs/README.md`.
- Architecture overview: `ARCHITECTURE.md`.
- Lifecycle hook contract and trust flow: `docs/HOOKS.md`.
- Verification contract and evidence lanes: `docs/VERIFICATION.md`.
- Gated development workflow: `docs/WORKFLOW.md`.
- Setup + usage reference: `README-neural-codex.md`.
- Task state: `plans/prd.json` and `plans/progress.jsonl`.
- ExecPlans for multi-hour work: `docs/PLANS.md` and `docs/exec-plans/active/`.
- Skills procedures: `.agents/skills/` (each has `SKILL.md`). Legacy copies may exist in `.codex/skills/`.
- Persona-specific guidance: `agents/*/AGENTS.md`.

## Overrides
- Use `AGENTS.override.md` for short-lived, local overrides. Keep it minimal and remove when done.

## Safety & Style
- Prefer small, incremental commits; avoid touching unrelated files.
- Use `rg` for search; respect existing code style and tests.
- If unsure, summarize findings and ask before large changes.
- Avoid recursive `codex` invocations; use scripts/prompts directly.

## Agents/Personas
- If multiple personas are needed, reset context between them (fresh turn, restate objective).
- Route tasks via `neural.route` prompt; keep a single active persona per task.
- Local agents available under `agents/`: `multi-ai`, `dispatcher`, `meta-agent` (use their AGENTS.md for scope).
