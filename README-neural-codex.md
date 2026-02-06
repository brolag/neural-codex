# neural-codex

Codex-native prompts, templates, scripts, and agents that bring the neural-claude workflow to the Codex CLI. Everything is file-based, repo-local, and designed for repeatable iteration with clear state.

- No Claude-specific hooks, status lines, or TTS
- All state lives in `plans/` and `.codex/`
- Prompts are namespaced as `neural.*`

## What you get

### Prompts
- Loop control: `neural.loop-start`, `neural.loop-plan`, `neural.loop-status`, `neural.loop-cancel`
- Planning: `neural.plan`, `neural.plan-execute`
- Memory: `neural.memory`, `neural.recall`
- Routing & analysis: `neural.route`, `neural.question`, `neural.pv`, `neural.evolve`
- Research: `neural.research`, `neural.gh-learn`, `neural.yt-learn`
- Sync & changelog: `neural.sync`, `neural.changelog-architect`
- Execution helpers: `neural.course`, `neural.craft`, `neural.feature`, `neural.status`, `neural.onboard`
- Metrics: `neural.kpi`, `neural.ca`, `neural.cost`
- Quality: `neural.slop-scan`, `neural.slop-fix`, `neural.overseer`, `neural.tdd`, `neural.debug`
- Multi-agent: `neural.squad`, `neural.pv-mesh`
- Task tracking: `neural.todo-new`, `neural.todo-check`
- Meta creation: `neural.meta.agent`, `neural.meta.skill`, `neural.meta.prompt`, `neural.meta.improve`, `neural.meta.eval`, `neural.meta.brain`
- Output styles: `neural.output-style` (default/concise/table/yaml/html/genui)
- Skills & config: `neural.skill`, `neural.profile`, `neural.test`

### Skills
Project-scoped skills in `.codex/skills/`:
- autonomous-loop: Ralph loop usage and guardrails
- agentic-course: guided lessons and references
- worktree-manager: parallel worktrees for multi-session work
- code-reviewer: production-minded reviews
- memory-system: progress-log memory
- pattern-detector: PRD/progress pattern analysis
- prompt-engineering: prompt creation/refinement
- plan-execute: structured planning and execution
- craft: CRAFT prompt builder
- feature: branch-first workflow
- debugging: root-cause workflow
- tdd: red-green-refactor
- kpi: agentic KPI tracking
- compute-advantage: agentic leverage metric
- cost-tracker: usage cost logging
- slop-scan: technical debt detection
- slop-fix: safe cleanup + refactor plans
- overseer: pre-merge review
- squad: multi-agent orchestration
- youtube-learner: transcript-based summaries
- skill-creator: bootstrap new skills with SKILL.md template
- skill-installer: install external skills from URLs/registries
- deep-research: multi-source comprehensive research
- test-runner: smart test execution with Ralph integration

### Templates
- `plans/prd.json` and `plans/progress.jsonl`
- `expertise.template.yaml`
- `todo-workflow.md`
- `craft.yaml`

### Scripts
- `scripts/ralph-loop.sh` and `scripts/ralph-once.sh`
- `scripts/memory_read.py` / `scripts/memory_write.py`
- `scripts/youtube-transcript.py`
- `scripts/setup-global.sh` / `scripts/setup-project.sh`

### Agents
- `agents/multi-ai/AGENTS.md`
- `agents/dispatcher/AGENTS.md`
- `agents/meta-agent/AGENTS.md`
- `agents/code-reviewer/AGENTS.md`
- `agents/codex/AGENTS.md`
- `agents/gemini/AGENTS.md`
- `agents/optimizer/AGENTS.md`
- `agents/cognitive-amplifier/AGENTS.md`

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

## Loop prerequisites
The Ralph loop requires `flock` and `timeout`.

macOS (Homebrew):
```bash
brew install util-linux coreutils
export PATH="/opt/homebrew/opt/util-linux/bin:/opt/homebrew/opt/coreutils/libexec/gnubin:$PATH"
```

Linux:
- Ensure `flock` (util-linux) and `timeout` (coreutils) are available in `PATH`.

## Installation details

### Global install (one time)
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

### Project install (per repo)
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

## Ralph loop usage
```bash
TEST_CMD="npm test" scripts/neural-codex/ralph-loop.sh 5
```

Notes:
- The loop claims one task per iteration from `plans/prd.json`.
- It writes progress to `plans/progress.jsonl`.
- It commits only when tests pass.

## Memory workflow
- Use `/prompts:neural.memory` to append notes to `plans/progress.jsonl`.
- Use `/prompts:neural.recall` to search the log.
- For direct CLI usage: `scripts/memory_write.py` and `scripts/memory_read.py`.

## Profiles

Named configuration sets for different workflows. Switch with `codex --profile <name>`:

| Profile | Model | Approval | Use Case |
|---------|-------|----------|----------|
| default | gpt-5.2-codex | on-failure | Standard development |
| fast | gpt-4.1-mini | on-failure | Quick tasks, low cost |
| autonomous | gpt-5.2-codex | never | Ralph loop, unattended work |
| careful | gpt-5.2-codex | untrusted | Sensitive changes |

Example:
```bash
codex --profile autonomous exec "Fix the auth bug"
```

## MCP config
Supported MCP servers are stubbed in `.codex/config.toml` and include:
- chrome-devtools
- github
- search (Exa)
- optional playwright

Set tokens in your shell as needed (e.g., `GITHUB_PERSONAL_ACCESS_TOKEN`).

## Advanced Config

The config file supports advanced options (see `.codex/config.toml`):
- **Profiles**: Named config sets with different models/approval policies
- **Notifications**: Webhooks, desktop alerts, CI integration
- **History**: Session transcripts with size caps
- **Telemetry**: OpenTelemetry for observability
- **TUI**: Clickable file citations (vscode, cursor, windsurf)

Reference: https://developers.openai.com/codex/config-advanced/

## Repo layout
```
.
├── .codex/
│   ├── prompts/
│   ├── skills/
│   ├── templates/
│   └── config.toml
├── agents/
├── plans/
├── scripts/
└── README.md
```

## Troubleshooting

Prompts not showing:
- Run `scripts/setup-global.sh` and restart Codex.

Ralph loop fails immediately:
- Ensure `flock` and `timeout` are in `PATH`.
- Ensure `codex` CLI is installed and logged in.

Tests not running:
- Set `TEST_CMD` explicitly for your project.

## GitHub Pages
Static site lives in `docs/`. Enable Pages with source `main` / `docs/`.
