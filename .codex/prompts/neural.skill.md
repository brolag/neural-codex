---
description: Create or install Codex skills
argument-hint: ACTION=<create|install|list> [name]
---

You are managing Codex skills for the neural-codex workflow.

## Actions

### Create a new skill
```
/prompts:neural.skill create <skill-name>
```
This invokes `$skill-creator` to bootstrap a new skill with SKILL.md template.

### Install an external skill
```
/prompts:neural.skill install <source>
```
This invokes `$skill-installer` to add a skill from a URL or registry.

### List available skills
```
/prompts:neural.skill list
```
Shows skills in `.codex/skills/` with their descriptions.

## Quick Reference

### Skill Structure
```
skill-name/
├── SKILL.md          # Required
├── scripts/          # Optional helpers
├── references/       # Optional docs
└── assets/           # Optional templates
```

### SKILL.md Frontmatter
```yaml
---
name: skill-name
description: One line for Codex matching
metadata:
  short-description: Brief label
  category: productivity|utilities|meta
  source: origin-identifier
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---
```

### Skill Locations (priority order)
1. `.codex/skills/` (project-local)
2. `~/.codex/skills/` (user global)
3. Built-in skills

## Examples

Create a commit helper:
```
/prompts:neural.skill create commit-helper
```

Install from GitHub:
```
/prompts:neural.skill install github.com/user/repo/skill
```

Outputs: Skill created/installed, or list of available skills with descriptions.
