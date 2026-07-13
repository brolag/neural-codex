# Neural Codex

Neural Codex is a small, evidence-gated workflow for Codex:

```text
discover -> spec -> craft -> vet -> exercise
```

It is distributed as a native Codex plugin. The repository intentionally ships
only those five skills and the reviewed lifecycle hooks that support them.

## Install

Add this repository as a Codex marketplace and install the plugin:

```bash
codex plugin marketplace add brolag/neural-codex
codex plugin add neural-codex@neural-codex
```

Start a new Codex task after installation so the plugin inventory is refreshed.
Then open `/hooks`, inspect the bundled definitions, and trust them if they match
your policy. Installing or enabling the plugin does not trust hooks automatically.

Confirm the installation with:

```bash
codex plugin list
```

## Workflow

| Skill | Purpose | Artifact or verdict |
|---|---|---|
| `$discover` | Surface architectural unknowns before planning | `unknowns-map.md` |
| `$spec` | Lock interfaces, invariants, dependencies, and acceptance | `plan.md` |
| `$craft` | Build an approved plan and capture before/after evidence | implemented change |
| `$vet` | Review the change independently and adversarially | `SHIP` or `HOLD` |
| `$exercise` | Drive the result as a user after automated tests | `PASS` or `FAIL` |

Small, obvious edits can skip `$discover` and sometimes `$spec`. Material work
should preserve the gates: planning does not implement, implementation does not
self-approve, and green tests do not replace behavioral verification.

See [the workflow guide](docs/WORKFLOW.md) for artifact contracts and examples.

## Hooks

The plugin includes dependency-free Python hooks for:

- blocking high-confidence destructive shell commands;
- guarding common secret-bearing files from patch writes;
- detecting obvious instruction injection in executable content;
- warning when tool output resembles credentials;
- preserving a compact recovery note before context compaction.

Hooks are guardrails, not a sandbox. Review their limits and trust model in
[docs/HOOKS.md](docs/HOOKS.md).

## Model and prompting guidance

Neural Codex does not change `~/.codex/config.toml`, model selection, approval
policy, sandbox mode, or network access. Model availability differs between the
API, ChatGPT, and Codex clients, so do not hardcode a model ID only because it
appears in an API prompting guide. Safe copyable settings and GPT-5.6 prompting
principles are separated in [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

## Repository structure

```text
.agents/plugins/marketplace.json       # repository marketplace
plugins/neural-codex/
  .codex-plugin/plugin.json            # plugin manifest
  skills/                               # exactly five workflow skills
  hooks/hooks.json                      # auto-discovered lifecycle hooks
docs/                                   # focused guides and GitHub Page
tests/                                  # plugin, workflow, hook, and docs contracts
plans/                                  # reviewed migration evidence
```

The 1.0 plugin is a deliberate breaking cleanup. Previous command bundles,
personas, autonomous loops, profiles, templates, and custom installers are not
part of the supported product.

## Develop and validate

Requirements: Python 3.11+, `pytest`, and a current Codex installation.

```bash
python3 -m pytest -q
./scripts/doc-lint.sh
python3 /path/to/plugin-creator/scripts/validate_plugin.py plugins/neural-codex
```

Every skill also passes Codex's `quick_validate.py`. The full verification and
behavioral expectations are in [docs/VERIFICATION.md](docs/VERIFICATION.md).

## Documentation

- [Architecture](ARCHITECTURE.md)
- [Agent harness](docs/AGENT-HARNESS.md)
- [Workflow](docs/WORKFLOW.md)
- [Hooks](docs/HOOKS.md)
- [Configuration](docs/CONFIGURATION.md)
- [Verification](docs/VERIFICATION.md)
- [GitHub Page](https://brolag.github.io/neural-codex/)
