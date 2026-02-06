---
name: feature
description: Branch-first workflow for implementing features with tests and PR-ready output.
metadata:
  short-description: Feature workflow
  category: productivity
  source: neural-claude-code-plugin
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Feature Workflow

Implement features on a dedicated branch with tests and a PR-ready summary.

## Usage
```
$feature "<description>"
```

## Steps
1. Create a `feature/<slug>` branch.
2. Implement changes following repo patterns.
3. Run tests and lint.
4. Summarize changes and next steps.
