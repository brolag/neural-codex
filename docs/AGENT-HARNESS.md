# Agent harness contract

Neural Codex separates authoring from evaluation. The five skills form a gated
artifact flow rather than a collection of unrelated commands.

```text
request
  -> $discover -> unknowns-map.md
  -> $spec     -> plan.md + approval
  -> $craft    -> implementation + baseline/delta
  -> $vet      -> SHIP | HOLD
  -> $exercise -> PASS | FAIL
```

## Authority by gate

| Gate | May inspect | May write | Must not do |
|---|---|---|---|
| `$discover` | repository and relevant sources | `unknowns-map.md` | implement |
| `$spec` | map, repository, tests, docs | `plan.md` | implement |
| `$craft` | approved plan and implementation | code and evidence | self-approve or publish |
| `$vet` | neutral diff bundle and acceptance | review report | rewrite scope or excuse missing evidence |
| `$exercise` | runnable product and public docs | behavioral evidence | infer behavior from source alone |

Small edits may enter later in the flow, but authority remains separated. A
builder cannot turn its own confidence into a `SHIP` verdict.

## Why the harness is artifact-based

The workflow treats code, plans, tests, and reports as an operational substrate:

| Property | Neural Codex expression |
|---|---|
| Executable | Acceptance criteria name commands, tests, and observable outcomes. |
| Inspectable | Plans, diffs, baselines, review reports, and exercise evidence remain readable. |
| Stateful | The plan and its append-only amendments preserve progress across long tasks. |
| Governed | Approval, sandbox, hook trust, and ship boundaries are explicit state rather than prompt advice. |

This is why a polished answer is not evidence by itself. The harness should be
able to observe what happened, verify it, preserve the result, and enforce the
authority boundary.

## Durable context

Artifacts live under `plans/<date>-<slug>/`. They preserve decisions across
context compaction and allow a fresh reviewer to evaluate the change without
the author's narrative. Paths must remain inside the repository's `plans/`
boundary; the skills explicitly reject traversal and escaping symlinks.

Load context selectively: repository rules and the active artifact first, then
only the implementation and references needed for the current gate. One focused
change per plan is easier to verify than several unrelated changes sharing a
context window.

## Model use

GPT-5.6 benefits from concise goals, explicit constraints, verifiable outcomes,
and permission boundaries. Neural Codex encodes those properties in artifacts
instead of relying on repeated prose. Model and reasoning settings remain user
configuration; see [CONFIGURATION.md](CONFIGURATION.md).
