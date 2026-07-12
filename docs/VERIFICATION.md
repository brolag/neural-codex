# Verification Contract

## Purpose

Tests, reviews, and screenshots answer different questions. Define what “done”
means before implementation, then collect evidence for each claim. A green test
suite does not replace a user flow, and a code review does not prove runtime
behavior.

## Before Implementation

For a non-trivial change, record this contract in the issue, PRD, or ExecPlan:

- **Objective:** one observable outcome.
- **Non-goals:** boundaries the change must not cross.
- **Acceptance scenarios:** concrete inputs and visible results.
- **Validation commands:** exact automated checks.
- **Behavioral backend:** CLI, browser, or desktop flow.
- **Rollback:** how to restore the previous behavior.

Keep repository-level instructions minimal. Put task-specific context in the
plan instead of expanding `AGENTS.md` with information already available in the
code or documentation.

## Verification Lanes

| Change | Required evidence |
|--------|-------------------|
| Documentation only | Doc lint, link/HTML validation, rendered inspection |
| Hook or configuration | Unit tests, malformed-input case, isolated install smoke test |
| User-facing behavior | Automated tests plus a real CLI/browser/desktop scenario |
| Security-sensitive or pre-merge | The relevant lane plus an independent clean-context review |

For blocking rules, always test both the dangerous input and a nearby safe
counterexample. For browser flows, inspect the console and network requests in
addition to the rendered screen.

## Proof Of Work

Report evidence as structured facts rather than a success narrative:

```yaml
tests:
  command: python3 -m pytest -q
  result: <N passed, 0 failed>
behavior:
  scenario: project hooks install under a custom CODEX_HOME
  result: pass
  evidence: exercise-evidence/report.md
review:
  result: ship
files_changed:
  - scripts/setup-global.sh
residual_risks:
  - dynamically assembled shell commands can evade static parsing
rollback: revert the change commit
```

Keep raw command output, console logs, and screenshots long enough to diagnose a
failure. Store local exercise evidence under `exercise-evidence/` or a scoped
`plans/<change>/evidence/` directory. Never commit evidence containing secrets,
tokens, or personal data.

## Improving The Harness

Treat each harness change as a small experiment:

1. Capture the failing trace or baseline.
2. State one falsifiable improvement hypothesis.
3. Change the smallest relevant component: instruction, tool, hook, memory, or loop.
4. Run the same representative scenarios, including held-out or regression cases.
5. Keep the change only when the evidence improves without breaking neighboring flows.

Prefer additive, reversible changes when the interaction between harness
components is uncertain. Prompt wording is only one component; tool behavior,
state, observability, and verification often matter more.

## Research Basis

See [`references/harness-research.md`](references/harness-research.md) for the
research findings and caveats behind these operating rules.
