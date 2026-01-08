---
name: worktree-manager
description: Create, manage, and merge git worktrees for parallel development. Use when running parallel features or multi-agent work.
metadata:
  short-description: Git worktree management
  category: productivity
  source: codex-templates
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Worktree Manager

Manage git worktrees for parallel Codex development sessions.

## Why Worktrees
- Isolation: separate working directories
- Parallelism: multiple Codex sessions without stashing
- Clean integration: feature branches merge back to main

## Usage
```
$worktree-manager new <feature-name>
$worktree-manager list
$worktree-manager status <name>
$worktree-manager merge <name>
$worktree-manager clean <name>
$worktree-manager clean --stale
```

## Recommended Process
1) Create a worktree:
```
$worktree-manager new auth-system
```
2) Initialize the project setup in the new worktree:
```
scripts/setup-project.sh --path ../worktrees/auth-system
```
3) Run Codex from the worktree:
```
cd ../worktrees/auth-system && codex
```

## Safety
- Never create worktrees inside other worktrees
- Ensure no uncommitted changes before merging
- Use kebab-case for feature names
