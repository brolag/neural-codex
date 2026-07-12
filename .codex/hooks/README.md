# Codex-native security and continuity hooks

These hooks adapt the protections in `neural-claude-code/hooks` to Codex's
current lifecycle contract. They intentionally use Python's standard library so
the installed hooks do not depend on `jq`.

## Included hooks

- `dangerous_actions_blocker.py`: blocks high-confidence destructive Bash commands and warns on recursive deletion.
- `prompt_injection_detector.py`: blocks obvious instruction-injection strings in executable commands and non-document patches.
- `sensitive_file_guard.py`: blocks `apply_patch` writes to common credential and environment files.
- `output_scanner.py`: warns when `tool_response` contains common secret formats.
- `pre_compact.py`: writes a small recovery snapshot to `.codex/compact-context.md` before compaction.

Codex loads the matching definitions from `.codex/hooks.json`. Open `/hooks` in
the CLI to review and trust new or changed hooks. Trust is tied to the hook hash,
so edits require review again.

## Boundaries

Codex hooks are guardrails, not a complete security boundary. Current
`PreToolUse` coverage includes simple `Bash`, `apply_patch`, and MCP calls, but
not every shell path, built-in read/search tool, or web search. The sensitive
file guard therefore prevents writes through `apply_patch`; filesystem and
sandbox policy must still protect other access paths.

Hook timeouts in `hooks.json` are seconds. Repo-local commands resolve their
scripts from `git rev-parse --show-toplevel` so they still work when Codex starts
from a subdirectory.
