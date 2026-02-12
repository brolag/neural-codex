---
name: squad
description: Multi-agent orchestration with architect/dev/critic roles and file-based task flow.
metadata:
  short-description: Neural Squad
  category: productivity
  source: neural-claude-code-plugin
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Neural Squad

Three-role workflow: Architect (specs), Dev (TDD), Critic (review).

## Suggested State Paths
- Tasks: `plans/squad/tasks/{inbox,assigned,in-progress,review,done}`
- Messages: `plans/squad/messages/`
- Activity: `plans/squad/activity/`

## Usage
```
$squad init
$squad status
$squad task create "<title>"
$squad task move <id> <status>
$squad standup
```

## Notes
- Use worktrees for isolation when possible.
- Critic never approves their own changes.
