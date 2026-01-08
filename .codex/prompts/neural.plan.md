---
description: Produce a short actionable plan from PRD and git status
argument-hint: none
---

Plan steps:
1) Inspect `plans/prd.json` for ready tasks (passes=false, not needs_human, deps satisfied).
2) Check git status for dirty files; list any blockers.
3) Produce a 3–6 step plan focusing on the next 1–2 tasks, including test commands to run.
4) Keep output compact; no code changes.
