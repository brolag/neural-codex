---
description: Start a Ralph loop iteration run for neural-codex
argument-hint: ITERATIONS=<count>
---

You are starting a Ralph loop run for neural-codex.

1) Inspect `plans/prd.json` to understand current tasks and dependencies.
2) Run `scripts/ralph-loop.sh <ITERATIONS>` (or `scripts/neural-codex/ralph-loop.sh` if installed via setup-project). Set `TEST_CMD` if needed, e.g., `TEST_CMD="npm test"`. The loop:
   - claims one task
   - runs Codex
   - runs tests
   - commits on green
   - rolls back on red
3) Monitor `plans/progress.jsonl` for status.
4) If no eligible tasks, report why (needs_human/blocked/deps).
5) Do not edit `plans/prd.json` manually; the loop handles state.
6) If iteration fails, surface logs and suggest fixes (deps, tests, env, flaky tests).

Outputs: brief status, tasks touched, next steps, and whether to rerun with a different iteration count.
