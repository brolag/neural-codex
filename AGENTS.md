# Neural Codex project instructions

## Product boundary

Neural Codex is one repository marketplace containing one plugin. Its supported
surface is exactly five skills: `discover`, `spec`, `craft`, `vet`, and
`exercise`, plus the reviewed hooks under `plugins/neural-codex/hooks/`.

Do not add a second skill root, a second hook manifest, or an installer that
copies files into a user's home directory. The plugin and marketplace are the
distribution contract.

## Canonical paths

- Marketplace: `.agents/plugins/marketplace.json`
- Plugin manifest: `plugins/neural-codex/.codex-plugin/plugin.json`
- Skills: `plugins/neural-codex/skills/<name>/SKILL.md`
- Hooks: `plugins/neural-codex/hooks/hooks.json`
- Public docs: `docs/`
- Plans and evidence: `plans/`

## Change workflow

Use `$discover` for material ambiguity, `$spec` before non-trivial
implementation, `$craft` for an approved plan, and independent `$vet` plus
`$exercise` gates before shipping. Keep generated evidence beside its plan.

Never auto-trust hooks or mutate a user's global Codex configuration. Never
commit credentials or read/write `.env` contents as part of validation.

## Required validation

```bash
python3 -m pytest -q
./scripts/doc-lint.sh
python3 /path/to/plugin-creator/scripts/validate_plugin.py plugins/neural-codex
```

Validate each retained skill with Codex's `quick_validate.py` when that tool is
available. A valid directory shape is necessary but not sufficient: tests must
also reject stale claims and unsupported inventory.

## Documentation map

- Architecture: `ARCHITECTURE.md`
- Harness contract: `docs/AGENT-HARNESS.md`
- Workflow: `docs/WORKFLOW.md`
- Hooks and trust: `docs/HOOKS.md`
- Model availability and prompting: `docs/CONFIGURATION.md`
- Verification: `docs/VERIFICATION.md`
