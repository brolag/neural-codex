---
description: Recall facts/notes from neural-codex memory
argument-hint: QUERY="<search terms>"
---

Recall workflow:
1) Read `plans/progress.jsonl` for recent notes.
2) Read expertise files if present (e.g., `.codex/templates/expertise.template.yaml` derivatives) or any `expertise/*.yaml`/`notes/*.md` if available.
3) Search for QUERY-related facts and return concise bullets.
4) If nothing found, say so and propose where to add a note (append to progress or an expertise file).
5) Do not edit files; just report findings.
