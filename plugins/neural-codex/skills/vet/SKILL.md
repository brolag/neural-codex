---
name: vet
description: Independently review a working tree, branch, pull request, or implemented plan before ship. Use for a material pre-merge gate that checks acceptance criteria, regressions, security boundaries, project consistency, cleanup quality, and active counterexamples in fresh context. Returns SHIP or HOLD with evidence.
---

# Vet

Review the change as an evaluator with no stake in shipping it. Report material findings only and return exactly `SHIP` or `HOLD`.

## 1. Resolve the target

Accept:

- `--base <ref>` for a branch diff;
- `--scope working-tree|branch|pr`;
- `--pr <number>` and optional repository;
- `--spec <path>` for acceptance criteria;
- trailing text as a review focus.

Inspect status, branch, remotes, and the narrow project guidance relevant to touched files. If no diff or changed artifact exists, report that there is nothing to vet and stop.

## 2. Build a neutral review bundle

Create a temporary directory outside the repository and collect:

- objective and acceptance criteria from the plan;
- base/head refs and target label;
- status, tracked diff, staged diff, and diff stat;
- an `untracked-manifest.txt` generated from `git ls-files --others --exclude-standard -z`;
- tests already reported by the implementer;
- relevant project constraints;
- no authoring narrative, praise, or proposed verdict.

For every untracked status entry, resolve it beneath the repository and account for it in the manifest. Copy safe text files into an `untracked/` subtree that preserves relative paths. For directories, inventory their files recursively without following symlinks. For large, binary, ignored, sensitive, or excluded files, record path, size, hash when safe, and the reason content was omitted. The reviewer must compare the manifest with status before issuing a verdict; an unexplained missing path prevents `SHIP`.

Treat refs, paths, and user text as data. Quote shell arguments, reject traversal outside the expected repository, and never include `.env` contents, credentials, or unrelated sensitive output.

## 3. Separate the evaluator

Prefer the host's native fresh-reviewer capability and pass only the neutral bundle. If unavailable and repository policy permits it, use a separate `codex exec` process with high reasoning effort and no conversation history.

If genuine context separation is unavailable, perform the strictest possible local review, disclose that limitation, and return `HOLD` whenever independence is required by the plan or material uncertainty remains. Never present self-review as independent review.

## 4. Verify acceptance

Extract every safe machine-checkable command, required file, behavior, migration, policy, `must_include`, and `must_not_include` assertion from the plan.

Mark each criterion:

- `PASS`: executed or inspected with concrete evidence;
- `FAIL`: contradicted by a command, diff, or counterexample;
- `NOT RUN`: unsafe, unavailable, or outside the current environment.

A required `FAIL` or `NOT RUN` prevents `SHIP`.

## 5. Review adversarially

Prioritize failures with real impact:

- authorization, trust boundaries, and secret exposure;
- data loss, corruption, duplication, rollback, and partial failure;
- races, stale state, ordering, retries, and idempotency;
- empty, null, timeout, degraded dependency, and version-skew behavior;
- compatibility, installer, migration, and documentation drift;
- dead code, generated slop, swallowed errors, unsupported claims, and missing tests.

Construct distinguishing inputs or safe probes for testable behavior. A green suite is evidence, not the whole specification.

## 6. Report the verdict

Use this shape:

```markdown
## Vet Review

Target: <target>
Reviewer: <fresh reviewer transport or disclosed limitation>

### Verdict: SHIP | HOLD

### Acceptance
| Criterion | Result | Evidence |

### Findings
#### CRITICAL | HIGH | MEDIUM: <title>
- File: path:line
- What can go wrong:
- Evidence:
- Impact:
- Fix:

### Probes
### Residual risk
### Summary
```

Return `SHIP` only when no material finding remains and every required criterion passes. Return `HOLD` for addressable findings, missing required evidence, failed criteria, or an invalid review boundary.

## Usage Examples

- `$vet --base origin/main --spec plans/2026-07-12-hooks/plan.md`
- `$vet --scope working-tree focus on installer compatibility`
- `$vet --pr 42`

## Done when

The change has been challenged in fresh context, acceptance is evidence-backed, material findings are actionable, and the verdict is unambiguous.
