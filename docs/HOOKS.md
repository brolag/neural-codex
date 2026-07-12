# Lifecycle Hooks

## Purpose

neural-codex installs deterministic Python handlers around supported Codex
lifecycle events. They provide defense in depth for destructive commands,
sensitive file writes, leaked credentials, prompt-injection patterns, and
context compaction.

Hooks are guardrails, not a complete security boundary. Keep Codex sandboxing,
approval policy, repository rules, and human review enabled where the risk
requires them.

## Layout

- `.codex/hooks.json` maps Codex events and matchers to handlers.
- `.codex/hooks/*.py` contains dependency-free Python handlers.
- `.codex/compact-context.md` is generated before compaction and ignored by Git.
- `.codex/profiles/*.config.toml` contains source templates for global profiles.

## Event Map

| Event | Matcher | Handler | Behavior |
|-------|---------|---------|----------|
| `PreToolUse` | `Bash` | `dangerous_actions_blocker.py` | Blocks high-confidence destructive commands and warns on recursive deletion. |
| `PreToolUse` | `Bash` | `prompt_injection_detector.py` | Blocks obvious instruction-injection strings in executable command content. |
| `PreToolUse` | `Edit|Write` | `sensitive_file_guard.py` | Blocks `apply_patch` writes to common secret-bearing files. Codex treats `Edit` and `Write` as aliases for `apply_patch`. |
| `PreToolUse` | `Edit|Write` | `prompt_injection_detector.py` | Checks non-document patches for obvious instruction-injection strings. |
| `PostToolUse` | all supported tools | `output_scanner.py` | Warns when `tool_response` resembles a known secret format. |
| `PreCompact` | `manual|auto` | `pre_compact.py` | Records Git state and the latest plan before compaction. |

Matching handlers for the same event can run concurrently. Do not rely on one
hook preventing another matching hook from starting.

## Installation And Trust

1. Run `scripts/setup-global.sh` to stage hooks and install Codex profile overlays.
2. Run `scripts/setup-project.sh` inside the target Git repository.
3. Restart Codex after the global installation.
4. Open `/hooks`, inspect every definition, and trust the exact hashes you approve.

Codex marks changed hook definitions for review again. Project-local hooks load
only when the project `.codex/` layer is trusted.

## Destructive Command Detection

The command guard tokenizes shell input with Python `shlex`. It blocks recursive
deletion of `/`, the active home directory, or their globbed contents across
common forms, including:

- Short flags in different orders: `-rf`, `-fr`, `-R -f`.
- Long flags: `--recursive --force`.
- Literal and quoted home references: `~`, `$HOME`, `${HOME}`.
- Root and home content globs: `/*`, `$HOME/*`, `~/*`.
- Commands wrapped by tools such as `sudo rm` and `env rm`.
- Nested shell execution such as `bash -c "rm -rf /"` and `zsh -lc ...`.

Detection is command-position aware, so text such as `echo rm -rf /` and
subcommands such as `git rm` do not produce false blocks. It intentionally
allows recursive deletion of narrower paths such as temporary build
directories. Dynamically assembled commands can still evade static analysis;
the sandbox and approval policy remain the enforcement boundary.

## Profiles

Codex 0.134 and later loads named profiles from
`$CODEX_HOME/<name>.config.toml`, not inline `[profiles.*]` tables. The global
installer provides `default`, `fast`, `autonomous`, and `careful` overlays.
Installers honor `CODEX_HOME` and default it to `~/.codex` when unset.

The templates target GPT-5.6 with explicit reasoning effort. If the current
account or provider does not expose GPT-5.6, use GPT-5.5 temporarily instead of
relying on fallback model metadata.

## Validation

Run the behavior and installation gates before publishing hook changes:

```bash
python3 -m pytest -q
bash scripts/doc-lint.sh
bash -n scripts/setup-global.sh scripts/setup-project.sh
python3 -m json.tool .codex/hooks.json >/dev/null
```

Any new blocked behavior needs both a positive regression case and a nearby
safe counterexample that must remain allowed.
