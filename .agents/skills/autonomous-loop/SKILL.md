---
name: autonomous-loop
description: Long autonomous task execution with iteration control. Use for multi-iteration work that benefits from PRD-driven loops and test gating.
metadata:
  short-description: PRD-driven autonomous loop
  category: productivity
  source: codex-templates
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Autonomous Loop (Ralph)

Run longer tasks safely using the Ralph loop harness and PRD gating.

## When to Use
- Multi-step refactors or migrations
- TDD flows with repeated test/repair cycles
- Batch operations that need progress tracking

## How It Works
- Uses `plans/prd.json` for task selection and dependency checks
- Logs to `plans/progress.jsonl`
- Runs tests via `TEST_CMD` (or fallback commands)

## Usage
```
$autonomous-loop "<task description>" --max <n>
```

Recommended workflow:
1) Create or update tasks in `plans/prd.json` (small, atomic items).
2) Run the loop:
```
TEST_CMD="npm test" scripts/ralph-loop.sh 5
# or, if installed via setup-project:
TEST_CMD="npm test" scripts/neural-codex/ralph-loop.sh 5
```
3) Monitor `plans/progress.jsonl` for outcomes.

## Notes
- The loop will skip tasks with unmet dependencies or maxed attempts.
- If the loop fails, inspect logs and update dependencies or tests.
- Use `/prompts:neural.loop-start` for guided usage.

## Safety
- Keep iterations small (5-10) for early runs.
- Use targeted `TEST_CMD` for faster feedback.
- Avoid large, unfocused tasks in the PRD.
