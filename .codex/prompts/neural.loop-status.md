---
description: Report current Ralph loop status for neural-codex
argument-hint: none
---

Check Ralph loop status:
1) Read `plans/prd.json` to list tasks with `status`, `passes`, `attempts`, `in_progress`, `depends_on`, `notes`.
2) Read tail of `plans/progress.jsonl` for the latest iterations.
3) Check git status/log for recent "Ralph:" commits and any dirty files.
4) Summarize:
   - Eligible tasks remaining (blocked vs ready)
   - Needs-human items (attempts >= max)
   - Last iteration results (pass/fail/reason)
   - Suggested next action (rerun loop? fix tests? adjust deps?)
Keep it concise.
