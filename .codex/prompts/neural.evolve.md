---
description: Analyze patterns and anti-patterns from PRD, progress, and git
argument-hint: none
---

Analyze the working set:
1) Read `plans/prd.json` (statuses, attempts, deps, needs_human).
2) Read recent `plans/progress.jsonl` entries.
3) Read recent git log/commits (e.g., last 10) and diffs for churn.
4) Report:
   - Patterns (what’s working)
   - Anti-patterns (what’s failing/flaky)
   - Suggested tests/automation/cleanup
   - Task(s) to tackle next and why
Keep it concise and actionable.
