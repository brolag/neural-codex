---
name: pattern-detector
description: Analyze PRD and progress logs to detect repeated patterns and automation candidates. Use with /prompts:neural.evolve.
metadata:
  short-description: Pattern detection for neural-codex
  category: productivity
  source: neural-claude-code
allowed-tools: Read, Glob, Grep, Bash
---

# Pattern Detector

Analyze `plans/prd.json` and `plans/progress.jsonl` for repeatable workflows.

## Data Sources
- `plans/progress.jsonl` (events, outcomes)
- `plans/prd.json` (tasks, attempts, dependencies)
- `git log -n 10` (recent changes)

## Output
- Patterns (what worked)
- Anti-patterns (flaky or failing sequences)
- Suggested automation (scripts, skills, prompts)
- Next tasks to prioritize

## Usage
Run via:
```
/prompts:neural.evolve
```

## Usage Examples
After several failed attempts, generate an automation idea list:
```
/prompts:neural.evolve
```

## Safety
- Read-only analysis
- Do not edit PRD directly
