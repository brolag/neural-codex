---
description: Generate a CRAFT-structured spec
argument-hint: TASK="<summary>" [--mode interactive|quick|loop]
---

Generate a CRAFT spec using `.codex/templates/craft.yaml` as the base.

- interactive: ask the CRAFT questions
- quick: emit a minimal CRAFT
- loop: produce a compact version suited for `neural.loop-start`

Save filled specs under `plans/craft/<slug>.yaml`.
