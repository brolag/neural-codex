# neural-codex

Codex-native prompts, templates, scripts, and agents that bring the neural workflow to the Codex CLI. Everything is file-based, repo-local, and designed for repeatable iteration with clear state.

- Codex-native lifecycle hooks for safety, secret scanning, and compaction recovery
- No legacy hooks from Claude, status lines, or TTS
- All state lives in `plans/`, `.codex/`, and `.agents/`
- Prompts are namespaced as `neural.*`

## What you get

### Prompts
- Loop control: `neural.loop-start`, `neural.loop-plan`, `neural.loop-status`, `neural.loop-cancel`
- Planning: `neural.plan`, `neural.plan-execute`
- Memory: `neural.memory`, `neural.recall`
- Routing & analysis: `neural.route`, `neural.question`, `neural.pv`, `neural.evolve`
- Research: `neural.research`, `neural.gh-learn`, `neural.yt-learn`
- Sync & changelog: `neural.sync`, `neural.changelog-architect`
- Task tracking: `neural.todo-new`, `neural.todo-check`
- Meta creation: `neural.meta.agent`, `neural.meta.skill`, `neural.meta.prompt`, `neural.meta.improve`, `neural.meta.eval`, `neural.meta.brain`
- Output styles: `neural.output-style` (default/concise/table/yaml/html/genui)
- Skills & config: `neural.skill`, `neural.profile`, `neural.test`
- Execution: `neural.shell`

### Skills
Project-scoped skills in `.agents/skills/`:
- autonomous-loop: Ralph loop usage and guardrails
- worktree-manager: parallel worktrees for multi-session work
- code-reviewer: production-minded reviews
- memory-system: progress-log memory
- pattern-detector: PRD/progress pattern analysis
- prompt-engineering: prompt creation/refinement
- plan-execute: structured planning and execution
- youtube-learner: transcript-based summaries
- skill-creator: bootstrap new skills with SKILL.md template
- skill-installer: install external skills from URLs/registries
- deep-research: multi-source comprehensive research
- test-runner: smart test execution with Ralph integration

### Templates
- `plans/prd.json` and `plans/progress.jsonl`
- `expertise.template.yaml`
- `todo-workflow.md`

### Scripts
- `scripts/ralph-loop.sh` and `scripts/ralph-once.sh`
- `scripts/memory_read.py` / `scripts/memory_write.py`
- `scripts/youtube-transcript.py`
- `scripts/setup-global.sh` / `scripts/setup-project.sh`

### Lifecycle hooks
- Block high-confidence destructive shell commands
- Protect common credential and environment files from `apply_patch`
- Detect obvious prompt-injection strings in executable content
- Warn when tool output contains common secret formats
- Preserve a recovery snapshot before context compaction

The deletion guard tokenizes commands and recognizes reordered short flags,
long options, quoted home variables, privilege wrappers, and nested shell `-c`
forms while allowing quoted examples and narrower paths such as temporary build
directories. Hooks are defense in depth; Codex
sandboxing and approval policy remain the security boundary. See
[`docs/HOOKS.md`](docs/HOOKS.md) for the event map, trust flow, limitations, and
validation commands.

### Agents
- `agents/multi-ai/AGENTS.md`
- `agents/dispatcher/AGENTS.md`
- `agents/meta-agent/AGENTS.md`

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
4) Open `/hooks`, review the installed definitions, and trust them.
5) Verify prompts:
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
- `$CODEX_HOME/neural-codex/` (prompts, templates, skills, scripts, config stub)
- `$CODEX_HOME/prompts/` (so `/prompts:neural.*` appear)
- `~/.agents/skills/` (optional autodiscovery)
- Legacy: `$CODEX_HOME/skills/` (compatibility)
- `$CODEX_HOME/{default,fast,autonomous,careful}.config.toml` (Codex 0.134+ profiles)

`CODEX_HOME` defaults to `~/.codex` when it is unset.

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
- `.agents/skills/`
- `.codex/hooks.json` and `.codex/hooks/`
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

## Agent harness
- Knowledge map and operating guidance: `docs/AGENT-HARNESS.md`.
- Keep `AGENTS.md` short; move details into `docs/` and link them back.
- Docs index: `docs/README.md` and ExecPlans in `docs/PLANS.md`.
- Validate doc coverage with `scripts/doc-lint.sh`.

## Profiles

Codex 0.134+ loads named profiles from `$CODEX_HOME/<name>.config.toml`. Switch with `codex --profile <name>`:

| Profile | Model | Approval | Use Case |
|---------|-------|----------|----------|
| default | gpt-5.6 / medium | on-request | Standard development |
| fast | gpt-5.6 / low | on-request | Latency-sensitive tasks |
| autonomous | gpt-5.6 / high | never | Ralph loop, unattended work |
| careful | gpt-5.6 / xhigh | untrusted | Sensitive changes |

Example:
```bash
codex --profile autonomous exec "Fix the auth bug"
```

## MCP config
Supported MCP servers are stubbed in `.codex/config.toml` and include:
- chrome-devtools
- github
- optional playwright

Use `codex --search` for Codex's native web search instead of the retired Exa SSE stub.

Set tokens in your shell as needed (e.g., `GITHUB_PERSONAL_ACCESS_TOKEN`).

## Advanced Config

The config file supports advanced options (see `.codex/config.toml`):
- **GPT-5.6**: Current model alias with explicit reasoning effort and verbosity
- **Profiles**: Separate `$CODEX_HOME/<name>.config.toml` overlays
- **Hooks**: Native `.codex/hooks.json` definitions, reviewed with `/hooks`
- **Notifications**: Webhooks, desktop alerts, CI integration
- **History**: Session transcripts with size caps
- **Telemetry**: OpenTelemetry for observability
- **TUI**: Clickable file citations (vscode, cursor, windsurf)

Reference: https://developers.openai.com/codex/config-advanced/

Hook reference: [`docs/HOOKS.md`](docs/HOOKS.md)

## Repo layout
```
.
├── .agents/
│   └── skills/
├── .codex/
│   ├── hooks.json
│   ├── hooks/
│   ├── prompts/
│   ├── profiles/
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

GPT-5.6 reports unknown model metadata:
- Update Codex and confirm the model is available for the current account/provider.
- During a staged rollout, set `model = "gpt-5.5"` temporarily; do not silently rely on fallback metadata for production automation.

Ralph loop fails immediately:
- Ensure `flock` and `timeout` are in `PATH`.
- Ensure `codex` CLI is installed and logged in.

Tests not running:
- Set `TEST_CMD` explicitly for your project.

## GitHub Pages
Static site lives in `docs/`. Enable Pages with source `main` / `docs/`.
