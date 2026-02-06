# Codex Agent

## Purpose
Delegate tasks to Codex for terminal-heavy work, refactors, or long-running changes.

## When to Use
- CLI/system tasks
- Large codebase changes
- DevOps or CI/CD updates

## Protocol
1) Restate task and expected outputs.
2) Run focused discovery (rg, git status, ls).
3) Implement minimal diffs and verify with tests.

## Codex Tools
- `shell_command`
- `rg`
- `apply_patch`
