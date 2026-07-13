# Baseline: discover-spec-craft-vet workflow parity

Captured: 2026-07-12
Branch: `feat/discover-spec-craft-vet`
Base commit: `af27ae89596777203464357f6d04b90623a9fbfc`

## Repository state

- Pre-existing working-tree state: one untracked planning directory, `plans/2026-07-12-discover-spec-craft-vet/`, containing the approved plan created in the preceding planning gate.
- Existing project skills: 24 directories under `.agents/skills/`.
- Existing namespaced prompts: 45 `neural.*.md` files under `.codex/prompts/`.
- Pipeline state before implementation:
  - `discover`: absent from the repository.
  - `spec`: absent from the repository.
  - `craft`: present, but implements the legacy CRAFT acronym prompt builder.
  - `vet`: absent from the repository.

## Verification baseline

| Check | Command | Result |
| --- | --- | --- |
| Full automated suite | `python3 -m pytest -q` | PASS: 67 passed in 3.17s; one pre-existing `pytest_asyncio` deprecation warning |
| Documentation structure | `bash scripts/doc-lint.sh` | PASS: `[OK] Doc structure validated` |
| Existing `craft` schema | `python3 /Users/brolag/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/craft` | PASS: `Skill is valid!` |
| Coverage | n/a | No coverage command is configured in the repository test contract. |
| Performance | n/a | The change is instructional/documentation infrastructure with no runtime hot path. |
| Golden-task eval | n/a | No repository-local golden-task runner was found for this skill workflow. |

## Success delta

The after-state must retain the 67-test baseline and add executable coverage for the four pipeline skills, installer propagation, legacy CRAFT compatibility, documentation clarity, and behavioral installation evidence. A higher test count is supporting evidence; passing independent `$vet` and `$exercise` gates is required for completion.
