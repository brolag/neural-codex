# neural-codex setup

This repository contains Codex-native prompts, templates, scripts, and config
to port the neural-claude workflow into Codex.

## Quick setup
1) Run the global install from this repo:
```bash
scripts/setup-global.sh
```
2) Restart Codex so `/prompts:neural.*` are picked up.
3) In any project, run the project install:
```bash
scripts/setup-project.sh
```
4) Verify prompts:
```
/prompts:neural.loop-start
```

## Global install (one time)
```bash
scripts/setup-global.sh
```

This installs:
- `~/.codex/neural-codex/` (prompts, templates, skills, scripts, config stub)
- `~/.codex/prompts/` (so `/prompts:neural.*` appear)
- `~/.codex/skills/` (optional autodiscovery)

Use `--force` to overwrite existing files:
```bash
scripts/setup-global.sh --force
```

## Project install (per repo)
```bash
scripts/setup-project.sh
```

This seeds a project with:
- `.codex/prompts/`
- `.codex/templates/`
- `.codex/skills/`
- `.codex/config.toml` (MCP stubs)
- `scripts/neural-codex/` (loop + helpers)
- `plans/prd.json`, `plans/progress.jsonl` (from templates)

Install into another path:
```bash
scripts/setup-project.sh --path /path/to/project
```

## Loop usage
```bash
TEST_CMD="npm test" scripts/neural-codex/ralph-loop.sh 5
```

## Prompts
After global setup, restart Codex and run:
```
/prompts:neural.loop-start
```

Key prompts:
- loop: `neural.loop-start`, `neural.loop-plan`, `neural.loop-status`, `neural.loop-cancel`
- planning: `neural.plan`, `neural.plan-execute`
- memory: `neural.memory`, `neural.recall`
- routing: `neural.route`, `neural.question`, `neural.pv`
- research/learning: `neural.research`, `neural.gh-learn`, `neural.yt-learn`
- meta: `neural.meta.agent`, `neural.meta.skill`, `neural.meta.prompt`, `neural.meta.improve`, `neural.meta.eval`, `neural.meta.brain`
- output styles: `neural.output-style` (default/concise/table/yaml/html/genui)

## Skills
Project-scoped skills live in `.codex/skills/`:
- autonomous-loop
- worktree-manager
- code-reviewer
- memory-system
- pattern-detector
- prompt-engineering
- plan-execute
- youtube-learner

## Helper Scripts
- `scripts/memory_write.py` and `scripts/memory_read.py` for progress-log memory
- `scripts/youtube-transcript.py` for transcript extraction
- In seeded projects, these live under `scripts/neural-codex/`
