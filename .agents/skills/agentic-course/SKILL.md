---
name: agentic-course
description: Interactive agentic coding course with lessons and references.
metadata:
  short-description: Agentic coding course
  category: productivity
  source: neural-claude-code-plugin
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Agentic Coding Course

Interactive, file-based lessons for mastering agentic coding in Codex.

## When to Use
- Users ask for `/course` or want structured learning
- Onboarding collaborators to neural-codex

## Assets
- Lessons: `.codex/skills/agentic-course/lessons/`
- References: `.codex/skills/agentic-course/references/`
- Progress: `plans/course/progress.json`

## Usage
```
$agentic-course <action> [args]
```

Actions:
- `menu` (default): show progress and lessons
- `start`: begin lesson 1
- `lesson <n>`: open a specific lesson
- `ref <topic>`: open a reference card
- `progress`: show progress summary
- `reset`: reset progress

## Notes
- Create `plans/course/progress.json` if missing.
- Keep output focused on the lesson content and next step.
