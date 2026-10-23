# Workflow

Neural Codex exposes exactly five skills:

```text
$discover -> $spec -> approval -> $craft -> $vet + $exercise -> ship
```

## 1. Discover

Use `$discover` when the request hides architectural choices, unfamiliar code,
security boundaries, or expensive assumptions.

```text
$discover inspect this repository before we replace authentication
```

It writes `unknowns-map.md`, resolves architecture-changing questions, and
stops. Skip it for obvious low-risk work.

## 2. Spec

Use `$spec` to turn evidence into a build contract.

```text
$spec plan the approved authentication migration
```

`plan.md` locks interfaces, quality gates, dependency-aware subtasks,
and executable acceptance. Its initial status is `draft`; implementation waits
for explicit approval.

## Quality criteria carried through the workflow

| Gate ID | Plan locks | Vet judges | Exercise observes |
|---|---|---|---|
| `security` | Trust boundaries, mitigations, CWE and applicable ASVS 5.0.0 IDs | Boundary correctness and counterexamples | Applicable authorized/unauthorized flows |
| `simplicity` | Reuse, justified abstractions/dependencies, maintainability | Duplication and speculative layers | Not a behavioral gate |
| `usability` | User, task, feedback, error recovery, accessibility | Workflow risks and required evidence | Task completion, recovery, and platform accessibility |

Each gate has applicability, a concrete criterion, verification, and expected
evidence. An unrelated gate is `N/A` with a reason. In a draft, an applicable
gate is `PLANNED`; after verification it is `PASS`, `FAIL`, or `NOT RUN`.
Missing required evidence blocks success. Carry the same criteria through
`$craft`, `$vet`, and `$exercise`; do not lower them after a failed check.

The detailed contract lives in [$spec](../plugins/neural-codex/skills/spec/SKILL.md).
It uses ASVS 5.0.0/CWE for applicable security requirements,
ISO/IEC 25010:2023 as a maintainability reference, ISO 9241-11:2018 for usability,
and WCAG 2.2 A/AA criteria for affected web accessibility. Accessibility is part
of usability; a clean automated scan does not prove full conformance, and
automated task success does not establish real users' satisfaction.

For an older plan without these gate criteria, return to `$spec` to add their
applicability and verification before `$craft`. Preserve the already agreed
scope and decisions; obtain renewed approval only for a material contract change.

## 3. Craft

Use `$craft` after reviewing and approving the plan.

```text
$craft implement the plan we just approved
```

Craft captures a baseline, implements against locked signatures, verifies each
subtask, records deviations, and measures the final delta. It does not silently
commit, publish, deploy, or merge.

## 4. Vet

Use `$vet` as the independent pre-ship review.

```text
$vet --spec plans/2026-07-12-example/plan.md --scope working-tree
```

The reviewer receives a neutral bundle, actively searches for counterexamples,
checks every required criterion, and returns exactly `SHIP` or `HOLD`.

## 5. Exercise

Use `$exercise` to verify the public workflow after automated checks.

```text
$exercise --spec plans/2026-07-12-example/plan.md
```

Exercise drives the appropriate browser, desktop, CLI, installer, or docs
surface and captures direct evidence. It returns `PASS` or `FAIL`.

## Artifact lifecycle

```text
plans/<date>-<slug>/
├── unknowns-map.md   # when discovery is needed
├── plan.md           # source-of-truth contract
├── baseline.md       # before metrics
├── delta.md          # after metrics
├── vet-report.md     # independent review
└── exercise-report.md
```

Artifacts are append-friendly and reviewable. Do not store credentials,
personal data, machine-specific caches, or unredacted sensitive output in them.

## Choosing the smallest safe path

- Obvious edit: implement and test directly.
- Clear non-trivial change: `$spec -> $craft -> $vet -> $exercise`.
- Ambiguous or high-cost change: start with `$discover`.

The workflow adds gates based on uncertainty and consequence, not file count.
