# Gated Development Workflow

Use `$discover -> $spec -> $craft -> $vet + $exercise` for non-trivial changes. The gates keep exploration, approval, implementation, code review, and observed user behavior from collapsing into one self-confirming pass.

## Quick start

```text
$discover map the unknowns in this change
$spec turn the unknowns map into an implementation plan
# Review plans/<date>-<task>/plan.md
$craft implement the plan we just approved
```

`$craft` runs `$vet` and `$exercise` before its ship handoff. It does not commit, push, merge, deploy, or send anything automatically.

Skills use `$name`. Namespaced prompts use `/prompts:neural.name`. In particular:

- `$craft` implements an approved `plan.md`.
- `/prompts:neural.craft` builds a legacy CRAFT YAML specification: Context, Requirements, Actions, Flow, Tests.

## Gate contract

| Gate | Use it when | Input | Durable output | Stop condition |
| --- | --- | --- | --- | --- |
| `$discover` | Important unknowns or architectural choices remain | Request, repository, references | `unknowns-map.md` | Map is ready for planning or explicitly blocked |
| `$spec` | The change needs a reviewable contract | Unknowns map plus repository evidence | Draft `plan.md` | Human approval is required |
| `$craft` | A specific plan is approved | Approved `plan.md` | `baseline.md`, implementation, updated plan, gate evidence | Human ship decision is required |
| `$vet` | Material changes need independent review | Neutral diff and acceptance bundle | `SHIP` or `HOLD` review | Findings are fixed or explicitly accepted |
| `$exercise` | Behavior can be driven as a user | Acceptance scenarios and runnable surface | Evidence-backed `PASS` or `FAIL` | Every required scenario has direct evidence |

## Artifact flow

```text
request
  -> unknowns-map.md (ready-for-spec | blocked)
  -> plan.md (draft -> approved -> in-progress -> done | blocked)
  -> baseline.md + changed files + verification evidence
  -> vet review (SHIP | HOLD)
  -> exercise report (PASS | FAIL)
  -> human ship decision
```

The files are the shared state. Conversation context may be compacted or replaced; the approved decisions, dependencies, evidence, and failure causes remain inspectable in the repository.

## 1. Discover unknowns

`$discover` reads the real repository before asking questions. It performs a grounded blindspot pass and maps:

- known knowns: explicit intent and constraints;
- known unknowns: visible questions;
- unknown knowns: tacit conventions and recognition criteria;
- unknown unknowns: newly exposed risks and dependencies.

It writes only `plans/<date>-<task>/unknowns-map.md` and stops. It does not change application code or generate HTML.

## 2. Specify the contract

`$spec` consumes the latest related unknowns map and writes `plan.md`. Every plan locks:

- changed or introduced interfaces;
- security invariants with relevant CWE boundaries;
- subtasks with `[needs:]` dependencies and `[tier:]` routing hints;
- `when / requires / ensures` acceptance;
- executable validation commands and text assertions;
- contradictions, non-goals, and open questions.

The initial status is `draft`. Review the file before invoking `$craft`; an explicit `$craft` invocation that clearly refers to that reviewed draft records approval.

## 3. Craft the approved change

`$craft` records `baseline.md` before implementation. It preserves pre-existing dirty work, follows dependency order, and updates subtask state as checks pass.

Tier tags describe the cheapest suitable execution class:

- `cheap`: mechanical work and narrow tests;
- `mid`: normal implementation judgment;
- `hard`: architecture, security, or ambiguity;
- `batch`: long multi-step operations.

Local Codex execution is the default. Parallel execution is optional and cannot override dependencies, scope, signatures, or side-effect boundaries.

If implementation evidence requires a signature or scope change, update the plan and record the reason in its Amend log. Never weaken acceptance to turn a failure green.

## 4. Vet independently

`$vet` receives a neutral bundle: objective, acceptance, refs, diff, tests, and relevant constraints. It should not receive the implementer's persuasive narrative or proposed verdict.

The reviewer checks acceptance, regressions, security boundaries, compatibility, cleanup quality, and active counterexamples. Required criteria are `PASS`, `FAIL`, or `NOT RUN`; a required failure or missing check prevents `SHIP`.

When fresh-context review is unavailable, disclose the limitation. Do not label self-review as independent review.

## 5. Exercise real behavior

`$exercise` first runs the automated suite, then follows one to three public user flows through the relevant backend:

- browser for a web app or static page;
- computer automation for a desktop app;
- terminal for a CLI, TUI, installer, or script;
- isolated fixtures plus rendered/generated output for documentation workflows.

Every scenario needs evidence such as a screenshot, console excerpt, exit code, generated-file inspection, or installer inventory. A green unit suite does not override a broken user flow.

## Failure and approval behavior

- A blocking unknown stops `$discover` before planning.
- An unresolved architecture question keeps `$spec` in `draft` or `blocked`.
- A failed prerequisite blocks dependent `$craft` subtasks.
- `HOLD` from `$vet` or `FAIL` from `$exercise` prevents completion.
- Required but unavailable evidence is reported as `NOT RUN`, never silently skipped.
- The human approval represented by `plan.md` governs what may be built; it is not an informal interruption that can be inferred later.

## Install and verify

Install globally, then seed a temporary or real project:

```bash
scripts/setup-global.sh
scripts/setup-project.sh --path /path/to/project
```

A normal upgrade recognizes and migrates the legacy CRAFT-builder `craft`
skill distributed by earlier releases. If that legacy directory contains local
changes, the installer moves it to `craft.legacy-backup` before activating the
new orchestrator. If that backup path already exists, setup stops instead of
overwriting it. Normal global setup also refreshes the installed
`setup-global.sh` and `setup-project.sh` entrypoints so a later project setup
cannot run stale migration logic; other existing scripts remain preserved.

Confirm the skills exist:

```bash
for skill in discover spec craft vet exercise; do
  test -f ".agents/skills/$skill/SKILL.md"
done
```

Validate this repository:

```bash
python3 -m pytest -q
bash scripts/doc-lint.sh
for skill in discover spec craft vet exercise; do
  python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" ".agents/skills/$skill"
done
```

Schema validation proves that a skill is discoverable. The semantic contract tests, `$vet`, and `$exercise` separately prove handoff integrity, review independence, and observed behavior.

## Lightweight alternatives

- `plan-execute` remains available for smaller work that does not need all approval and evidence gates.
- `code-reviewer` remains a general review helper; `$vet` is the formal independent pre-ship gate.
- The Ralph loop remains a task-loop runtime. It is not a replacement for the discovery and approval artifacts when architectural unknowns are material.
