---
description: Append learnings/notes to neural-codex memory store
argument-hint: NOTE="<summary>"
---

Add a note:
1) Append a JSONL entry to `plans/progress.jsonl` with ts/task=note/status=note/message=NOTE.
2) If expertise files exist (e.g., `expertise/*.yaml`), propose an appended section; ensure valid YAML.
3) Use apply_patch safely; keep edits minimal and atomic.
4) Confirm what was written.
