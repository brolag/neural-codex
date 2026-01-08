---
description: Review PRD tasks and surface ready vs blocked items
argument-hint: none
---

Check todos:
1) Read `plans/prd.json`.
2) List ready tasks (passes=false, status not needs_human, attempts<max, deps satisfied).
3) List blocked tasks (deps unmet or needs_human) with reasons.
4) Suggest the single best next task and a test command to validate it.
5) Keep it concise.
