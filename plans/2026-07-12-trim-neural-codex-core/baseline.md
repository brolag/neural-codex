# Baseline: pre-cleanup neural-codex

Captured on 2026-07-12 from `main` commit `db90633` before plugin migration edits.

## Automated checks

| Check | Before |
|---|---:|
| Pytest | 81 passed in 6.65s |
| Documentation lint | PASS (`[OK] Doc structure validated`) |
| Coverage | n/a — the repository has no coverage configuration |
| Performance | n/a — documentation, plugin packaging, and hook dispatch are not a hot-path benchmark |
| Golden eval | n/a — no golden-task eval suite is present |

Pytest emitted one environment-level `pytest-asyncio` deprecation warning because `asyncio_default_fixture_loop_scope` is unset; no test failed.

## Inventory

| Surface | Before |
|---|---:|
| Tracked files | 193 |
| `.agents/skills/` directories | 28 |
| `.codex/prompts/` files | 45 |
| `agents/` persona directories | 8 |
| `tests/test_*.py` files | 10 |

## Keep/remove matrix

Keep and migrate:

- `discover`, `spec`, `craft`, `vet`, and `exercise`
- the five reviewed Python safety/continuity hooks plus shared hook utilities and hook documentation
- the immediately preceding migration plan, research, exercise evidence report, and vet report
- concise root instructions/architecture, focused docs, GitHub Page, semantic tests, CI, and documentation lint if still referenced

Remove or replace:

- all custom prompts, legacy skill copies, personas, templates, profiles, example project config, custom setup scripts, Ralph loops, memory/sync/Telegram/YouTube helpers, and old task-state files
- tests and docs whose only purpose is to enforce or advertise removed surfaces
- duplicate README and generic documentation scaffolding unrelated to the five-step workflow

## Reproduction

```bash
python3 -m pytest -q
./scripts/doc-lint.sh
git ls-files | wc -l
find .agents/skills -mindepth 1 -maxdepth 1 -type d | wc -l
find .codex/prompts -type f | wc -l
find agents -mindepth 1 -maxdepth 1 -type d | wc -l
find tests -maxdepth 1 -name 'test_*.py' | wc -l
```
