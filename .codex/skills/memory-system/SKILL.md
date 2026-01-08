---
name: memory-system
description: Read and write to the neural-codex memory log. Use when the user says remember/recall/forget or when persisting learnings.
metadata:
  short-description: Project memory via plans/progress.jsonl
  category: productivity
  source: neural-claude-code
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Memory System

Manage persistent memory using the project log at `plans/progress.jsonl`.

## Memory Sources
- `plans/progress.jsonl` (primary log)
- `plans/prd.json` (task state)
- Optional expertise files in `expertise/*.yaml`

## Usage
```
$memory-system remember "<fact or preference>"
$memory-system recall "<query>"
$memory-system forget "<query or id>"
```

## Write Memory (remember)
- Append a JSONL entry to `plans/progress.jsonl` with:
  - ts (UTC ISO-8601)
  - task: "memory"
  - status: "note|preference|pattern|learning"
  - message: the content
- Use `scripts/memory_write.py` (or `scripts/neural-codex/memory_write.py`) when available.

## Read Memory (recall)
- Search `plans/progress.jsonl` for matches in `message`.
- Return the most relevant lines with timestamps.
- Use `scripts/memory_read.py` (or `scripts/neural-codex/memory_read.py`) when available.

## Forget
- Do not delete history.
- Add a new entry noting a retraction, e.g. status="forget".

## Safety
- Never store secrets or credentials.
- Keep entries concise and factual.
