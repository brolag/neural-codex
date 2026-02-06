---
name: overseer
description: Review diffs or PRs for quality, security, and slop before merge.
metadata:
  short-description: Pre-merge review
  category: utilities
  source: neural-claude-code-plugin
allowed-tools: Read, Glob, Grep, Bash
---

# Overseer

Pre-merge review for correctness, security, and quality.

## Usage
```
$overseer [--pr <branch>] [path] [--quick]
```

## Checks
- Slop/duplication
- Missing tests
- Security issues
- Consistency with repo conventions

## Output
Provide severity-ranked findings and a clear approve/fix recommendation.
