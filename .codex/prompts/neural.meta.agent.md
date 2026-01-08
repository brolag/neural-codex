---
description: Create a new agent profile (AGENTS.md)
argument-hint: NAME="<kebab-case>" PURPOSE="<what it does>"
---

Create a new agent profile for the project.

Steps:
1) Parse NAME and PURPOSE. If missing, ask for both.
2) Check for existing `agents/<name>/AGENTS.md` and confirm before overwrite.
3) Create `agents/<name>/AGENTS.md` with:
   - Purpose and scope
   - Tools needed
   - Operating protocol
   - Guidance to read `expertise/<name>.yaml` if it exists
4) If requested, seed `expertise/<name>.yaml` from `.codex/templates/expertise.template.yaml`.
5) Report the files created and how to invoke the agent.
