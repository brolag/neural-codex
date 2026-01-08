---
description: Propose next iteration plan for Ralph loop
argument-hint: none
---

Plan the next Ralph iteration:
1) Read `plans/prd.json` and identify the highest-priority eligible task (passes=false, status!=needs_human, attempts<max, deps passed).
2) Check recent failures in `plans/progress.jsonl`.
3) Propose a short plan (3-5 bullets) for the next loop run:
   - Target task ID and why
   - Key files/tests to touch
   - Risks (deps, flakiness)
   - Recommended `TEST_CMD` or targeted test
4) Keep output concise; no code changes.
