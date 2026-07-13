# Verification

Neural Codex uses four complementary evidence lanes.

## 1. Structural validation

The plugin validator checks the manifest and component layout. Each skill also
passes Codex's `quick_validate.py`.

```bash
python3 /path/to/plugin-creator/scripts/validate_plugin.py plugins/neural-codex
python3 /path/to/skill-creator/scripts/quick_validate.py plugins/neural-codex/skills/spec
```

This proves schema compatibility, not workflow correctness.

## 2. Semantic tests

```bash
python3 -m pytest -q
./scripts/doc-lint.sh
```

Tests assert the exact five-skill allowlist, manifest and marketplace paths,
hook behavior, trust documentation, path containment, stale-reference denial,
and GitHub Page links.

## 3. Independent review

`$vet` verifies the approved plan against a neutral change bundle. Every
required criterion must be `PASS`; missing required evidence prevents `SHIP`.

## 4. Behavioral exercise

`$exercise` follows the documented installation and workflow as a user, then
inspects the GitHub Page at desktop and mobile widths. Source inspection alone
cannot produce `PASS`.

## Release gate

A change is ready only when:

- plugin and skill validators pass;
- pytest and documentation lint pass;
- no unsupported inventory or stale claim remains;
- `$vet` returns `SHIP`;
- `$exercise` returns `PASS`;
- required pull-request checks are green.
