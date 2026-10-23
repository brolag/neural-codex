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

## Synthetic quality-gate decision evaluations

Run the six opt-in cases with an authenticated Codex CLI that supports
`skip_host_skill_discovery` (verified with 0.153.3) and Python 3.11+:

```bash
python3 scripts/eval-quality-gates.py --output plans/quality-gate-evals.json
```

The runner supplies synthetic files and the selected skill to fresh ephemeral,
read-only sessions. Per-run settings skip host skill discovery and disable
plugins, apps, and delegation; user configuration and installed skills are not
modified. Each case has a bounded timeout. This uses Codex quota and is not part
of the ordinary unit suite or automatic CI.

Cases cover web/library planning, a duplicated abstraction, missing owner
authorization, an acceptable internal fix, and a CLI error without recovery
guidance. The positive case detects a gate that rejects everything. Expected
answers stay outside evaluator prompts. Python tests verify the grader rejects
wrong verdicts, missing/contradictory gates, unanchored findings, and runner
failures. Runnable cases also require completed tool executions with the
expected command arguments, exit code, and observed output. Reading or quoting
a test's source does not satisfy that oracle.

The report separates **decision correctness** (verdict and defect location)
from **gate-contract coverage** (explicit applicability, results, and evidence).
Renaming a gate alone does not improve the decision score. Use `--skills-root`
with an external copy of an earlier revision to compare before and after;
`--case` selects individual cases. Do not place another `SKILL.md` tree inside
this repository.

These bounded probes evaluate decisions, not the complete artifact workflow,
real users' satisfaction, a browser accessibility audit, or standards
certification. Results depend on the model and can vary between runs. Full
product verification still needs the appropriate local tests and behavior.

See the [2026-10-22 measured comparison](../results/2026-10-22-quality-gates/summary.md)
for recorded verdicts, gate coverage, provenance, and limitations.
