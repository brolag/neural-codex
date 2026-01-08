---
description: Sync agent or skill expertise with project reality
argument-hint: TARGET="<agent-or-skill>" [--validate-only] [--prune]
---

Sync an agent/skill's expertise file with the current codebase.

Steps:
1) Locate `expertise/<target>.yaml` (or a skill-local expertise file if it exists).
2) Validate required fields: domain, version, last_updated, understanding.
3) Check referenced files still exist; update paths as needed.
4) Update last_updated and bump version if changes were made.
5) If --prune, remove stale patterns with low confidence.
6) Report changes and any open questions.
