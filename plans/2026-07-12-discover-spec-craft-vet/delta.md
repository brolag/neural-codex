# Before / After Delta

| Measure | Before | After | Delta |
| --- | --- | --- | --- |
| Automated suite | 67 passed | 81 passed | +14 regression/contract tests, no failures |
| Documentation lint | PASS | PASS | Preserved while adding the workflow guide and Page section |
| Pipeline skills distributed | Legacy `$craft` only | `$discover`, `$spec`, `$craft`, `$vet`, `$exercise` | Complete gated workflow plus behavioral companion |
| `$craft` semantics | CRAFT YAML prompt builder | Approved-plan build orchestrator | Legacy builder preserved at `/prompts:neural.craft` |
| Normal upgrade | Preserved legacy `$craft` | Migrates exact legacy and archives customized legacy | Existing installations receive the active orchestrator safely |
| Installed project updater | Could remain stale | Refreshed during normal global setup | Later project installs apply current migrations |
| Review bundle | Could omit all untracked content | NUL-safe manifest plus safe content/hash accounting | Complete working-tree review boundary |
| Artifact path boundary | Partial | `spec`, `craft`, and `exercise` constrained under repository paths | Traversal, external absolute paths, and escaping symlinks rejected |
| GitHub Page | No gated workflow section | Five workflow cards plus legacy-command distinction | Desktop/mobile verified with zero console errors |
| Mobile layout | Long install commands and title could overflow; badge overlaid content | Viewport width equals document width; title fits; badge is static | Behavioral defects found and fixed during `$exercise` |
| `$exercise` | Not distributed | PASS, 4/4 scenarios | Clean install, upgrade, compatibility, and responsive page evidence |
| `$vet` | Not distributed | SHIP | Independent clean-context gate passed after fixes |

The single pre-existing `pytest_asyncio` deprecation warning is unchanged. Coverage and performance remain `n/a` because the repository does not configure coverage and this change adds instructional/documentation infrastructure rather than a runtime hot path.
