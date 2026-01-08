---
description: Propose adding a new task to PRD
argument-hint: TITLE="<title>" PRIORITY="P0|P1|P2|P3" DEPENDS_ON="id1,id2" ACCEPTANCE="<comma-separated>"
---

When adding a task:
1) Draft a JSON snippet suitable for `plans/prd.json` (id, title, priority, depends_on[], acceptance[], passes=false, attempts=0, status="todo", in_progress=false, notes="").
2) Keep IDs short and kebab-case.
3) Do not apply changes automatically unless instructed; present the snippet and a patch preview.
4) Check for conflicts with existing IDs.
