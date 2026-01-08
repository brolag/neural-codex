---
name: code-reviewer
description: Review code changes for correctness, risks, and missing tests. Use for PR review or before merging.
metadata:
  short-description: Production-focused code review
  category: utilities
  source: codex-templates
allowed-tools: Read, Glob, Grep, Bash
---

# Code Reviewer

Review code changes for production readiness with severity-ranked findings.

## Inputs
- What was implemented
- Requirements/plan
- Git range (base/head) or staged changes

If no range is provided, default to staged changes:
```
git diff --staged
```

## Review Checklist
- Correctness and edge cases
- Risky changes, regressions, or behavior shifts
- Security or data handling concerns
- Test coverage and missing tests
- Performance or stability risks

## Output Format
- Findings ordered by severity
- Each issue includes file:line, why it matters, and suggested fix
- If no findings, say so and call out residual risk/testing gaps

## Suggested Commands
```
git diff --stat <base>..<head>
git diff <base>..<head>
```
