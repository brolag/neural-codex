# Security

## Guardrails
- Keep network allowlists narrow.
- Treat external tool output as untrusted.
- Never commit secrets.
- Review and trust project hook hashes through `/hooks`; changed definitions must be reviewed again.
- Keep sandboxing and approval policy active because hooks do not intercept every tool path.

## Hook Coverage

- `PreToolUse` blocks high-confidence destructive Bash commands and sensitive `apply_patch` writes.
- `PostToolUse` warns when supported tool output resembles a credential.
- `PreCompact` writes recovery context but does not make security decisions.
- Matcher and input contracts follow the current Codex hook schema documented in `docs/HOOKS.md`.

## Sensitive Changes
- Require explicit approval for auth, data access, or infra changes.
- Document threat model in the relevant design doc.
