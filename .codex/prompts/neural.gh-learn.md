---
description: Learn from a GitHub repository snapshot
argument-hint: PATH="<repo path or URL>"
---

Goal: summarize repo structure, key patterns, and risks.

Steps:
1) If PATH is local, inspect README, package files, src/, tests/. If URL, instruct to clone shallowly and inspect.
2) Extract: main stack, entry points, key services/modules, tests coverage, build/test commands.
3) Note risks: missing tests, outdated deps, security-sensitive areas.
4) Emit a concise summary plus suggested next actions (tests to run, files to read next).
Dependencies: assumes git available; for remote URLs, ensure network is allowed before cloning.
