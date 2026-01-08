---
description: Switch between Codex profiles for different workflows
argument-hint: PROFILE=<default|fast|autonomous|careful>
---

You are switching Codex profiles for the neural-codex workflow.

## Available Profiles

| Profile | Model | Approval | Use Case |
|---------|-------|----------|----------|
| default | gpt-5.2-codex | on-failure | Standard development |
| fast | gpt-4.1-mini | on-failure | Quick tasks, low cost |
| autonomous | gpt-5.2-codex | never | Ralph loop, unattended work |
| careful | gpt-5.2-codex | untrusted | Sensitive changes, review all |

## Usage

Switch profile for current session:
```bash
codex --profile fast
```

Use in Ralph loop:
```bash
codex --profile autonomous exec ...
```

## Profile Selection Guide

1. **default**: Day-to-day development with safety nets
2. **fast**: Quick research, simple edits, cost-sensitive tasks
3. **autonomous**: Ralph loop iterations, batch processing, CI tasks
4. **careful**: Production deployments, security-sensitive code, database migrations

## Creating Custom Profiles

Edit `.codex/config.toml`:
```toml
[profiles.my-profile]
model = "gpt-5.2-codex"
approval_policy = "on-request"
sandbox = "workspace-write"
```

Then use: `codex --profile my-profile`

Outputs: Confirm the profile switch and summarize active settings.
