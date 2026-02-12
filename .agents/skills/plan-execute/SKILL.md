---
name: plan-execute
description: Orchestrate a plan-first workflow, optionally routing simple steps to other models or profiles.
metadata:
  short-description: Plan, execute, review
  category: productivity
  source: neural-claude-code
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Plan-Execute

Plan complex tasks, then execute in smaller, verifiable steps.

## When to Use
- Large changes with multiple moving parts
- Tasks that benefit from explicit success criteria
- Situations where you want to split reasoning vs. execution

## Workflow
1) Create a short plan with steps and success criteria.
2) Execute steps in order; keep changes small.
3) Verify with tests or checks.
4) Summarize results and next actions.
5) If a plan exists in `plans/prd.json`, align with dependencies and attempts.

## Optional Multi-Model Routing
If other CLIs are installed, route simple steps:
- `codex --profile fast "..."`
- `gemini -y "..."`

## Related Prompt
Use `/prompts:neural.plan-execute` to follow the structured plan format.

## Usage Examples
Plan a multi-step refactor before editing:
```
/prompts:neural.plan-execute
```
