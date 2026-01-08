---
description: Evaluate agents/skills against test cases
argument-hint: TARGET="<agent-or-skill>" [--all] [--report]
---

Evaluate agents or skills against local test cases.

Steps:
1) Look for tests in `.codex/tests/*.yaml` or `tests/*.yaml`.
2) If TARGET is provided, filter to that test suite.
3) Execute each test manually by simulating the prompt and verifying expected behavior.
4) Summarize pass/fail results.
5) If --report, write a short markdown report under `reports/`.

If no tests exist, propose a minimal test case template.
