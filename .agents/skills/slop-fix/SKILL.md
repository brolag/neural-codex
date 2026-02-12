---
name: slop-fix
description: Fix low-risk slop findings and propose refactor plans for larger issues.
metadata:
  short-description: Slop fix
  category: utilities
  source: neural-claude-code-plugin
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Slop Fix

Apply safe fixes for low-risk issues and draft plans for larger refactors.

## Usage
```
$slop-fix [path] [--scope quick|safe|plan]
```

## Guardrails
- Never change public APIs without approval.
- Prefer minimal diffs.
- Run tests after changes when available.

## Output
- Summary of fixes applied
- Remaining issues with proposed plan
