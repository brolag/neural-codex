# Delta: neural-codex plugin cleanup

Measured on 2026-07-12 against the baseline captured from `main` commit `db90633`.

| Measure | Before | After | Delta |
|---|---:|---:|---:|
| Repository files represented by the change | 193 | 51 | -142 |
| Supported skills | 28 | 5 | exact reviewed allowlist |
| Custom prompt files | 45 | 0 | removed deprecated surface |
| Persona directories | 8 | 0 | removed unsupported surface |
| Test modules | 10 | 4 | stale inventory tests replaced |
| Automated tests | 81 passed | 45 passed | smaller suite targets only supported behavior |
| Hook behavior tests | included in legacy suite | 25 passed | portable plugin contract covered |
| Documentation files in `docs/` | broad scaffold | 9 | focused user-facing set |
| Documentation lint | PASS | PASS | contract rewritten for plugin surface |
| Plugin validator | n/a | PASS | new distribution contract proven |
| Skill validators | mixed inventory | 5/5 PASS | exact allowlist proven |
| Isolated marketplace installation | n/a | PASS | plugin 1.0.0 installed and enabled |
| Live five-gate Codex exercise | n/a | PASS | fresh `$vet`: SHIP; fresh `$exercise`: PASS |
| Independent branch vet | n/a | SHIP | no material findings |

## Quality improvements

- One canonical plugin location replaces overlapping repo-local, global-copy, and prompt installations.
- Hooks resolve through `${PLUGIN_ROOT}` and keep trust explicit.
- README, focused docs, tests, and GitHub Page describe the same five capabilities.
- Model guidance no longer claims GPT-5.6 is selectable in Codex merely because it appears in API or ChatGPT guidance.
- Documentation now explains executable, inspectable, stateful, and governed harness properties found in the `~/Sites/sb` research synthesis.

## Known warning

The local Python environment still emits the pre-existing `pytest-asyncio` deprecation warning about `asyncio_default_fixture_loop_scope`. Neural Codex has no async tests or pytest configuration, so this is an environment/plugin warning rather than a repository regression.
