---
description: Analyze a changelog or recent commits to discover feature synergies
argument-hint: SOURCE="CHANGELOG.md|git"
---

Analyze SOURCE for new capabilities and workflow synergies.

Steps:
1) If SOURCE is a file and exists, read it. Otherwise use `git log -n 20 --oneline` and recent diffs.
2) Identify new features or changes.
3) Map synergies between features (what combinations unlock new workflows).
4) Recommend concrete, actionable next steps (scripts, prompts, tests, docs).

Output:
- New capabilities summary
- Synergy map (short list)
- Recommended actions
