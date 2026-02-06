---
description: Agentic coding course launcher
argument-hint: ACTION="menu|start|lesson|ref|progress|reset" [value]
---

Launch the agentic course using `.codex/skills/agentic-course/`.

Actions:
- menu: show course menu and progress
- start: open lesson 1
- lesson <n>: open a specific lesson
- ref <topic>: open a reference card
- progress: show progress summary
- reset: reset `plans/course/progress.json`

If progress file is missing, create it with defaults.
