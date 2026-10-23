---
name: exercise
description: Verify a completed change through real user behavior after automated tests. Use as $craft's independent behavioral gate for web, desktop, CLI, installer, documentation, or static-site workflows. Drives concrete scenarios, captures evidence for every assertion, and returns PASS or FAIL.
---

# Exercise

Verify that the changed product works for a user. Tests answer whether code checks pass; exercise answers whether the promised workflow is usable end to end.

## 1. Select the backend

Detect the changed surface:

- web application or static site: isolated browser automation;
- desktop application: computer-use automation;
- CLI, TUI, installer, or scripts: terminal interaction;
- documentation-only workflow: follow the documented commands in an isolated fixture and inspect the rendered or generated result.

Ask for launch details only when they cannot be derived safely from repository scripts or documentation.

## 2. Run automated tests first

Detect and run the repository's normal test command. Record pass/fail counts and warnings. A failing suite makes the exercise verdict `FAIL`; do not hide it behind a successful manual scenario.

If no test suite exists, record `Tests: none found` as a caveat.

## 3. Derive concrete scenarios

When `--spec <plan>` is supplied, turn its `when/requires/ensures` acceptance into one to three user flows. Otherwise derive flows from the user request and changed documentation.

Before reading the plan or selecting an evidence directory, resolve the repository root, the repository's `plans/` directory, and the candidate spec. Require `os.path.commonpath([candidate, plans_root]) == plans_root` and reject escaping symlinks. Reject `../../outside/plan.md`, `plans/../outside/plan.md`, `/tmp/external-plan.md`, and equivalent traversal. Without `--spec`, resolve `exercise-evidence/` beneath the repository root and apply the same containment check before writing.

Each scenario needs:

- a named user goal;
- exact steps and inputs;
- one observable expected result;
- the evidence type captured at the assertion point.

Cover the plan's applicable behavior-facing gates:

- **Security:** observe the authorized/unauthorized or permission flow at the changed boundary using synthetic local data. Do not perform destructive or external probes.
- **Usability:** drive the intended task, success feedback, a likely error, and recovery. Observe whether the user can understand what happened and what to do next; an exit code or successful HTTP response alone is insufficient. This applies to CLI, installer, and operator workflows as well as UI.
- For a web usability gate, drive keyboard-only navigation and focus and run axe/Lighthouse or an equivalent available accessibility tool. Record applicable WCAG 2.2 A/AA checks, manual observations, scan violations, and untested criteria. A clean scan is partial evidence, not a claim of full conformance. Use appropriate accessibility checks for other platforms.

Simplicity is judged by `$vet`, not by exercising a product. Keep security and usability applicability explicit; use `N/A` with rationale where no related behavior changed. Do not require a browser for a CLI-only scenario. Unavailable required checks remain `NOT RUN`; do not silently substitute source inspection or claim user satisfaction from an automated probe.

## 4. Drive the workflow

Launch only local trusted software. Poll for readiness instead of using blind delays. Follow the same public commands and navigation a user would use.

Capture at least one artifact per scenario:

- screenshot and browser-console excerpt;
- terminal stdout/stderr and exit code;
- generated file inspection;
- installer destination inventory.

Never trigger payment, deletion, sending, deployment, or another destructive/external side effect without explicit confirmation. Keep evidence free of secrets and personal data; store safe artifacts under the validated plan's `evidence/` directory.

## 5. Judge from observations

A scenario passes only when the observed result matches the expected result and the supporting evidence exists. Unexpected console errors or non-zero exits, unexpected files, broken links, missing UI content, or unavailable required steps fail the scenario. An expected error response can pass a negative scenario only when its required explanation and recovery also work.

Do not infer behavior solely from source inspection. When a surface cannot be run, label it `NOT RUN` and make the overall verdict `FAIL` if it is required.

## 6. Report

```markdown
## Exercise Report

Target: <surface>
Backend: <browser|desktop|cli|docs>
Tests: <passed/failed/none>
Scenarios: <run/passed>

### PASS | FAIL: <scenario>
- Steps:
- Expected:
- Observed:
- Evidence:

### Verdict: PASS | FAIL
### Quality gates
| Gate | PASS / FAIL / NOT RUN / N/A | Observed evidence or applicability rationale |
### Residual risk
```

## Usage Examples

- `$exercise --spec plans/2026-07-12-hooks/plan.md`
- `$exercise verify the setup script in a temporary HOME`
- `$exercise walk the changed GitHub Page on desktop and mobile`

## Done when

The automated suite has run, every required scenario has direct evidence, and the final `PASS` or `FAIL` follows from observed behavior rather than assertion.
