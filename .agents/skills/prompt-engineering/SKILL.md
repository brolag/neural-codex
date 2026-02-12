---
name: prompt-engineering
description: Improve prompts and command templates. Use when creating or refining prompts under .codex/prompts.
metadata:
  short-description: Prompt review and improvement
  category: utilities
  source: neural-claude-code
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Prompt Engineering

Improve or create prompts that follow the neural-codex style.

## When to Use
- Adding new `/prompts:neural.*` commands
- Refining argument hints or usage steps
- Simplifying verbose prompt instructions

## Workflow
1) Read existing prompts in `.codex/prompts/` for style.
2) Keep prompts focused on a single task.
3) Include `description` and `argument-hint` frontmatter.
4) Prefer short, numbered steps.

## Usage Examples
Improve a prompt with a tighter argument hint:
```
/prompts:neural.meta.improve
```

## Related Prompts
- `/prompts:neural.plan`
- `/prompts:neural.output-style`
- `/prompts:neural.route`
