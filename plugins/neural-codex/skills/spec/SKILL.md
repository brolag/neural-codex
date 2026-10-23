---
name: spec
description: Plan a non-trivial change before implementation. Lock interfaces, security, simplicity, usability, dependencies, and executable acceptance. Consumes unknowns-map.md when available, writes an approvable plan.md, and stops without coding.
---

# Spec

Turn intent and repository evidence into an approvable implementation contract. Never write implementation code.

## 1. Right-size and research

Skip ceremony for an obvious change under roughly 25 lines with no new interface, ambiguity, or risk.

Otherwise:

1. Find the newest related `plans/**/unknowns-map.md` and read it first.
2. Read repository guidance, the relevant code, tests, documentation, and useful history.
3. Reuse established patterns before proposing new ones.
4. If discovery was skipped, record that fact and clarify only architecture-changing ambiguity.

Treat resolved discovery decisions as inputs. Preserve unresolved blockers instead of guessing around them.

## 2. Lock the contract

Declare every introduced or changed interface before implementation:

```text
name(parameters) -> result [new|adapt|reuse] -> path
```

Interfaces include functions, types, commands, files, routes, events, schemas, and durable artifact shapes. A new interface that duplicates an existing one is a planning defect.

### Quality gates

For every material change, record the gate IDs `security`, `simplicity`, and `usability`. Each gate needs applicability, an observable criterion, a `verify` command or procedure, and the evidence required to pass. Use `N/A` with a concrete scope rationale when a gate does not apply. Do not omit a gate or invent a requirement to fill the table. During planning, applicable gates are `PLANNED`, not `PASS`.

### Security invariants

**Security.** For every relevant trust or data boundary, write an `@invariant` with its CWE, concrete mitigation, and verification at that boundary. Cover path handling, secret exposure, command execution, authorization, destructive side effects, and validation integrity where applicable. For web applications and services, map applicable requirements to [OWASP ASVS 5.0.0](https://github.com/OWASP/ASVS/tree/v5.0.0) using versioned IDs such as `v5.0.0-1.2.5`. Verify the actual requirement before citing it; do not invent ASVS mappings for an unrelated platform.

**Simplicity.** Use [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html) maintainability as a quality reference. Name the existing symbols to reuse and justify new abstractions or dependencies against the actual requirement. Reject duplicate implementations, unused extension points, and speculative layers. A new abstraction can be appropriate when the locked contract needs it; line count alone is not the criterion. Record a concrete source comparison or check rather than claiming ISO conformance.

**Usability.** Use [ISO 9241-11:2018](https://www.iso.org/standard/63500.html) to define the intended user, task, and context. For a changed product or operator workflow, specify observable task completion, understandable feedback, and recovery from likely errors; include a justified time/step/error threshold only when it helps decide success. A CLI or installer has a user workflow too. A private library change with no user-visible behavior may be `N/A`.

Accessibility is part of usability. For a changed web surface, identify applicable [WCAG 2.2](https://www.w3.org/TR/WCAG22/) A/AA criteria and verification, including keyboard access, visible/unobscured focus, names/roles/values, contrast, and other affected criteria. Use suitable platform checks for desktop or TUI surfaces. Automated accessibility scans provide partial coverage; name manual checks and remaining limits. Scripted task success cannot establish real users' satisfaction or full standards conformance.

## 3. Decompose and route

Give every subtask a stable ID and a `[tier:]` model-routing tag:

- `cheap`: mechanical edits, boilerplate, and narrow tests;
- `mid`: normal implementation requiring local judgment;
- `hard`: architecture, security, ambiguity, or tricky debugging;
- `batch`: long-running multi-step or operational work.

Add `[needs: S1, S2]` only for real dependencies. No dependency tag means the work may execute independently. Validate that every referenced ID exists and that the graph is acyclic.

## 4. Make acceptance executable

Every subtask must include:

- `when`: the triggering state or behavior;
- `requires`: preconditions and boundaries;
- `ensures`: observable postconditions;
- `verify`: a safe command, test path, or deterministic assertion;
- `must_include` or `must_not_include` when text contracts matter.

State what each verification oracle proves and what it does not prove. A green unit test cannot substitute for behavioral or independent review when those gates are required.

## 5. Scan contradictions

Resolve incompatible requirements, unreachable states, naming collisions, and approval ambiguity. Validate the dependency graph. Record deliberate tradeoffs and residual questions rather than hiding them in implementation notes.

## 6. Write `plan.md` and stop

Normalize the task slug to lowercase letters, digits, and hyphens. Resolve the repository root and its `plans/` directory before creating anything. Resolve the candidate artifact path and require `os.path.commonpath([candidate, plans_root]) == plans_root`; reject symlinks or normalized paths that escape that boundary. Inputs such as `../../outside/plan.md`, `plans/../outside/plan.md`, and `/tmp/external-plan.md` are invalid.

Write `plans/<YYYY-MM-DD-task-slug>/plan.md` with this frontmatter:

```yaml
---
project: <repo>
created: YYYY-MM-DD
status: draft
modified: []
commits: []
agents: []
related:
  back: []
  forward: []
---
```

Include these sections:

1. Context and locked decisions
2. Signatures
3. Quality gates: security invariants, simplicity, and usability (including accessibility)
4. Subtasks with state legend, dependencies, tiers, and executable acceptance
5. Contradiction scan
6. Out of scope
7. Open questions
8. Notes
9. Amend log

`plan.md` is the source of truth. Do not generate HTML; accept `--no-html` as a compatibility no-op. Present the plan and STOP for approval. A later explicit `$craft` invocation that clearly refers to this reviewed draft counts as approval; otherwise require an explicit approval before changing its status.

## Usage Examples

- `$spec implement the approved unknowns map for account export`
- `$spec plan the hook migration --no-html`
- `$spec turn this issue into a dependency-aware build contract`

## Done when

The draft plan has locked signatures, three quality gates with testable criteria or justified `N/A`, executable acceptance, a valid dependency graph, explicit non-goals, and has been presented without implementation edits.
