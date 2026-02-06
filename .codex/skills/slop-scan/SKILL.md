---
name: slop-scan
description: Scan a codebase for technical debt, duplication, and low-quality patterns.
metadata:
  short-description: Slop scan
  category: utilities
  source: neural-claude-code-plugin
allowed-tools: Read, Glob, Grep, Bash
---

# Slop Scan

Identify technical debt and code smells with a fast, repeatable scan.

## Usage
```
$slop-scan [path] [--quick]
```

## What to Check
- Large files/functions
- Nested conditionals
- Duplicated blocks
- TODO/FIXME accumulation
- Unused imports
- Missing tests for new logic

## Output
Provide a ranked list of issues with:
- severity (critical/high/medium/low)
- location
- suggested fix
- quick wins vs deep refactors
