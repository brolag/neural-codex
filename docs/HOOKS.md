# Hooks

Neural Codex packages lifecycle hooks at
`plugins/neural-codex/hooks/hooks.json`. Codex auto-discovers this conventional
plugin path and provides `${PLUGIN_ROOT}` to every command.

## Included handlers

| Handler | Event | Behavior |
|---|---|---|
| `dangerous_actions_blocker.py` | `PreToolUse` | Blocks high-confidence destructive shell and protected-branch force-push patterns. |
| `sensitive_file_guard.py` | `PreToolUse` | Blocks patch writes to common secret-bearing files. |
| `prompt_injection_detector.py` | `PreToolUse` | Blocks obvious instruction-injection text in executable inputs while allowing documentation discussion. |
| `output_scanner.py` | `PostToolUse` | Warns when tool output resembles credentials without repeating the detected value. |
| `pre_compact.py` | `PreCompact` | Writes a small project recovery note before context compaction. |

Handlers use only the Python standard library and exchange JSON through stdin
and stdout. Hook timeouts in `hooks.json` are seconds.

## Trust

Installing or enabling the plugin does not trust its hooks. Open `/hooks`,
inspect the exact definitions, and grant trust only when they match your local
policy. A changed hook hash requires review again.

## Boundaries

Hooks reduce mistakes but do not replace:

- Codex approval policy;
- filesystem and network sandboxing;
- repository branch protection;
- secret scanning in CI;
- human review for destructive or external side effects.

The sensitive-file guard covers patch inputs; it is not a universal filesystem
access control. The prompt-injection detector intentionally targets obvious
signals and cannot establish that arbitrary external content is trustworthy.

## Validate

```bash
python3 -m json.tool plugins/neural-codex/hooks/hooks.json >/dev/null
python3 -m pytest -q tests/test_hooks.py
```
