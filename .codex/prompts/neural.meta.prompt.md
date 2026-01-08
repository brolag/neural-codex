---
description: Generate a new neural prompt under .codex/prompts
argument-hint: NAME="<kebab-case>" PURPOSE="<one-line purpose>"
---

Create a new prompt under `.codex/prompts/`.

Steps:
1) Parse NAME and PURPOSE. If missing, ask for both.
2) Choose a filename: `neural.<name>.md`.
3) Include frontmatter:
   - description
   - argument-hint (if needed)
4) Write a short, numbered process.
5) Report the new prompt path and an example usage.
