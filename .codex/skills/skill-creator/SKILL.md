---
name: skill-creator
description: Bootstrap new skills with proper structure and metadata. Use when creating custom skills for a project or global use.
metadata:
  short-description: Create new Codex skills
  category: meta
  source: neural-codex
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Skill Creator

Bootstrap new skills with proper SKILL.md structure following the agent skills specification.

## When to Use
- Creating a new project-specific skill
- Adding a global skill to `~/.codex/skills/`
- Converting a repeated workflow into a reusable skill

## Usage
```
$skill-creator "<skill-name>" [--global] [--description "<desc>"]
```

## Usage Examples
Create a local project skill:
```
$skill-creator "api-tester" --description "Test REST APIs with curl"
```

Create a global skill:
```
$skill-creator "commit-helper" --global --description "Smart commit messages"
```

## Skill Structure
A skill folder contains:
```
skill-name/
├── SKILL.md          # Required: instructions and metadata
├── scripts/          # Optional: executable helpers
├── references/       # Optional: documentation
└── assets/           # Optional: templates
```

## SKILL.md Template
```markdown
---
name: <skill-name>
description: <one-line description for Codex matching>
metadata:
  short-description: <brief label>
  category: <productivity|utilities|meta>
  source: <origin identifier>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# <Skill Name>

<What this skill does and when to use it.>

## Usage
```
$<skill-name> <args>
```

## Usage Examples
<Concrete examples with expected behavior.>

## Steps
1) <Step one>
2) <Step two>
3) <Step three>

## Safety
- <Constraint or warning>
```

## Skill Locations
Skills are discovered from (highest to lowest priority):
- `.codex/skills/` (project-local)
- `~/.codex/skills/` (user global)
- Built-in skills

## Steps
1) Parse skill name and options
2) Create the skill directory
3) Generate SKILL.md with provided description
4) Optionally scaffold scripts/ folder
5) Print usage instructions

## Safety
- Use kebab-case for skill names
- Keep descriptions concise for better Codex matching
- Test skills locally before sharing
