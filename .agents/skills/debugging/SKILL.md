---
name: debugging
description: Structured debugging workflow for root-cause analysis and fixes.
metadata:
  short-description: Debugging workflow
  category: utilities
  source: neural-claude-code-plugin
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Debugging

Root-cause analysis with a repeatable workflow.

## Steps
1. Reproduce (minimal case)
2. Observe (logs, stack traces)
3. Hypothesize (3+ causes)
4. Test hypotheses
5. Fix and verify

## Usage
```
$debugging "<symptom>"
```

## Output
- Repro steps
- Root cause
- Fix summary
- Verification results
