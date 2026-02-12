---
name: craft
description: Generate CRAFT-structured specs for autonomous work.
metadata:
  short-description: CRAFT prompt builder
  category: productivity
  source: neural-claude-code-plugin
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# CRAFT Framework

CRAFT = Context, Requirements, Actions, Flow, Tests.

## When to Use
- Preparing an autonomous task or Ralph loop
- Complex changes that need explicit success criteria

## Usage
```
$craft "<task>" [--mode interactive|quick|loop]
```

## Template
Start from `.codex/templates/craft.yaml` and fill it out.

Suggested output location:
`plans/craft/<slug>.yaml`

## Notes
- Include the 3-tier boundaries (always / ask / never).
- Include a completion promise (e.g., `<promise>CRAFT_COMPLETE</promise>`).
- Keep tests explicit and runnable.
