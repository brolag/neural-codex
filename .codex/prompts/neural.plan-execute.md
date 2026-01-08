---
description: Plan a complex task, then execute in steps
argument-hint: TASK="<task description>"
---

You are orchestrating a plan-first execution.

Phase 1: Planning
1) Break TASK into atomic steps.
2) Note dependencies.
3) Define success criteria.
4) Emit the plan as JSON:
```
{
  "task": "...",
  "steps": [
    {
      "id": 1,
      "description": "...",
      "tool": "Bash|Edit|Write|Read|Grep",
      "depends_on": []
    }
  ],
  "success_criteria": ["..."]
}
```

Phase 2: Execution
- Execute steps in order, keeping changes small.
- If optional external CLIs are installed, you may route simple steps:
  - `codex --profile fast "..."`
  - `gemini -y "..."`

Phase 3: Review
- Verify success criteria.
- Summarize results and list files changed.

Output:
- Plan summary, execution log, and final result.
