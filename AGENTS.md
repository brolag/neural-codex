# neural-codex - Project Instructions

## Overview
- Codex-native port of neural-claude features: Ralph loop, namespaced prompts, templates, MCP, and agents.
- All state is file-based: `plans/prd.json` (tasks), `plans/progress.jsonl` (log), `.codex/prompts/` (prompts), `.codex/templates/` (templates), `scripts/` (automation).
- No Claude-specific hooks/statusline/TTS/marketplace.
- Setup and usage reference: `README-neural-codex.md`.

## Workflow
- Use Ralph loop: `scripts/ralph-loop.sh <iters>` with `TEST_CMD` set as needed.
- Keep tasks small; follow PRD `depends_on` and attempts limits.
- Use namespaced prompts (`neural.*`) for loop control, recall, plan, evolve, research, todo, output styles.
- Memory is explicit: append to `plans/progress.jsonl` or expertise files; no auto indexing.

## Safety & Style
- Prefer small, incremental commits; avoid touching unrelated files.
- Use `rg` for search; respect existing code style and tests.
- If unsure, summarize findings and ask before large changes.
- Avoid recursive `codex` invocations; use scripts/prompts directly.

## Agents/Personas
- If multiple personas are needed, reset context between them (fresh turn, restate objective).
- Route tasks via `neural.route` prompt; keep a single active persona per task.
- Local agents available under `agents/`: `multi-ai`, `dispatcher`, `meta-agent` (use their AGENTS.md for scope).
