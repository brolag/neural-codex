# Vet Report

Target: complete working tree against `origin/main`, including untracked files

Reviewer: fresh independent Codex context

Final verdict: **SHIP**

## Material findings

None remain.

## Acceptance evidence

- Full suite: 81 passed; only the pre-existing `pytest_asyncio` deprecation warning.
- Codex skill validation: `discover`, `spec`, `craft`, `vet`, and `exercise` all passed `quick_validate.py`.
- Documentation: `scripts/doc-lint.sh` and `git diff --check` passed.
- Upgrade: the installed updater refresh and normal upgrade passed for exact and customized legacy craft states, including canonical downstream propagation.
- Backup boundary: an existing `craft.legacy-backup` caused a safe exit with original and backup state preserved.
- Artifact containment: `spec`, `craft`, and `exercise` contracts reject traversal, absolute external paths, and escaping symlinks.
- Review completeness: every untracked file was reconciled by path, size, and SHA-256 evidence.
- Compatibility: `/prompts:neural.craft` and `craft.yaml` remain intact.
- Hygiene: secret, generated-slop, and forbidden Claude-contract scans passed.

## Review iterations

Earlier independent passes returned `HOLD` and exposed four classes of defects that were fixed before the final verdict:

1. legacy `$craft` surviving a normal upgrade;
2. untracked files omitted from review bundles and incomplete artifact path containment;
3. customized staging copies reinfecting downstream skill roots;
4. a stale installed project updater, missing `$exercise` containment, and generated browser artifacts.

## Residual risk

- Live agent execution quality remains dependent on the host Codex version and task context.
- Browser verification covered the local static site; GitHub Pages CDN delivery remains a post-merge smoke check.
