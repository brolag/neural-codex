---
description: Route task to the right agent/persona for neural-codex
argument-hint: TASK="<brief task>"
---

Routing guidance:
1) Inspect available agents (agents/*/AGENTS.md or root AGENTS.md). If none, suggest which persona to load.
2) For the TASK, choose a single primary agent/persona; include a one-liner why.
3) Remind to reset context before switching (fresh turn, restate objective).
4) Suggest the most relevant prompt(s) to run next (e.g., loop-start, plan, research).
Keep output brief.
