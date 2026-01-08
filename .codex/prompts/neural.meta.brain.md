---
description: Show system status for agents, skills, and memory
argument-hint: [--detailed]
---

Display the current neural-codex system status.

Steps:
1) List agents under `agents/*/AGENTS.md`.
2) List skills under `.codex/skills/*/SKILL.md`.
3) Count entries in `plans/progress.jsonl`.
4) Show stale or missing expertise files in `expertise/*.yaml`.
5) Summarize in a concise dashboard.

If --detailed, include file lists and last-modified timestamps.
