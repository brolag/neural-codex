---
description: Choose or create a current Codex profile for a workflow
argument-hint: PROFILE=<default|fast|autonomous|careful>
---

Select the requested profile from `$CODEX_HOME/<name>.config.toml` and show the
exact command that starts Codex with it. Do not edit configuration unless the
user asks to create or change a profile.

## Bundled profiles

| Profile | Model / effort | Approval | Use case |
|---------|----------------|----------|----------|
| default | gpt-5.6 / medium | on-request | Standard development |
| fast | gpt-5.6 / low | on-request | Latency-sensitive work |
| autonomous | gpt-5.6 / high | never | Test-gated unattended loops |
| careful | gpt-5.6 / xhigh | untrusted | Sensitive changes |

Launch a new session:

```bash
codex --profile fast
```

Run a non-interactive task:

```bash
codex --profile autonomous exec "<task>"
```

Codex 0.134+ does not read `[profiles.<name>]` tables. To create a custom
profile, write top-level keys to `$CODEX_HOME/<name>.config.toml`:

```toml
model = "gpt-5.6"
model_reasoning_effort = "medium"
model_verbosity = "medium"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
```

Keep the recommendation outcome-focused: identify the profile, explain the
quality/latency and approval trade-off, and provide the launch command.
