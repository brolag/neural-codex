---
name: tdd
description: Enforce RED-GREEN-REFACTOR for feature work and bug fixes.
metadata:
  short-description: TDD workflow
  category: productivity
  source: neural-claude-code-plugin
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# TDD

Follow the RED-GREEN-REFACTOR loop.

## Rules
- No production code without a failing test.
- Make the smallest change to go green.
- Refactor only with tests passing.

## Usage
```
$tdd "<task>"
```

## Output
- Test plan
- Failing test output
- Minimal implementation
- Refactor notes
