---
description: Create a new Codex skill (SKILL.md)
argument-hint: NAME="<kebab-case>" PURPOSE="<what it does>"
---

Create a new Codex skill under `.codex/skills/`.

Steps:
1) Parse NAME and PURPOSE. If missing, ask for both.
2) Check for existing `.codex/skills/<name>/SKILL.md` and confirm before overwrite.
3) Create `.codex/skills/<name>/SKILL.md` with frontmatter:
   - name, description, allowed-tools
   - optional metadata
4) Add a short usage section and any templates/scripts.
5) Report the file path and suggested invocation.
