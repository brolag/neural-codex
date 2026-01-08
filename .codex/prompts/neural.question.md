---
description: Answer a project, codebase, or general knowledge question
argument-hint: QUESTION="<your question>"
---

Answer QUESTION with the best available method.

1) Check for project expertise files:
   - `expertise/*.yaml`
   - `.codex/templates/expertise.template.yaml` (for schema)
2) Classify the question:
   - Project/codebase: search files with `rg`, read key files.
   - Current events: use web search if needed.
   - General knowledge: answer directly; verify if uncertain.
3) Respond with a direct answer, then short details.
4) Cite sources used (file paths or URLs).

Keep it concise and specific.
