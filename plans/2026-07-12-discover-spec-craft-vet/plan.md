---
project: neural-codex
created: 2026-07-12
status: done
modified:
  - 2026-07-12
commits:
  - 28e0f98c0becfcc19908d086df11766b6e2f3d93
agents:
  - codex-main
  - codex-vet-independent
related:
  back:
    - plans/research/2026-07-12-hooks-gpt-5-6.md
    - docs/AGENT-HARNESS.md
    - docs/VERIFICATION.md
  forward: []
---

# Plan: neural-codex / discover-spec-craft-vet workflow parity

## Context

The merged hooks and GPT-5.6 update modernized the runtime, profiles, README, documentation, and GitHub Page, but it did not port the development workflow used locally with Claude Code: `discover -> spec -> craft -> vet` (with `exercise` as the independent behavioral gate during craft). The omission is real rather than a documentation-only problem.

### Current-state findings

| Surface | `discover` | `spec` | `craft` | `vet` |
| --- | --- | --- | --- | --- |
| Local Claude installation (`~/.claude/skills`) | Current unknowns gate | Current planning gate | Current build orchestrator | Current clean-context review gate |
| Published `brolag/neural-claude-code` | Missing | Present, older/simpler | Present, older/simpler | Present, older/simpler |
| Local Codex installation (`~/.codex/skills`) | Missing | Present | Present | Present |
| `brolag/neural-codex` after PR #1 | Missing | Missing | Name occupied by the legacy CRAFT prompt builder | Missing |

The existing `.agents/skills/craft/SKILL.md` means **Context, Requirements, Actions, Flow, Tests** and emits `plans/craft/<slug>.yaml`. That conflicts with the desired `$craft` build-orchestrator name. The namespaced prompt `.codex/prompts/neural.craft.md` already provides an unambiguous home for the legacy CRAFT-spec builder, so the skill name can be reassigned without deleting that workflow.

`plan-execute` and `code-reviewer` overlap with parts of the new pipeline but do not implement its approval, artifact, clean-context, or independent behavior gates. They remain useful as lightweight/general-purpose procedures and must not silently masquerade as the gated workflow.

### Research-derived requirements

- The local Claude workflow is the semantic source, but every skill must be adapted to Codex primitives and paths rather than copied with Claude-only tools or `.claude/` dependencies.
- `discover` must inspect the real repository, perform a blindspot pass, map all four unknown quadrants, resolve architecture-changing questions first, pin references, and hand off a durable Markdown artifact to `spec`.
- `spec` must consume recent discovery output, lock interfaces and security invariants, declare real dependencies and model tiers, define executable acceptance, scan contradictions, emit `plan.md`, and stop for approval.
- `craft` must require an approved plan, capture a reproducible baseline before edits, respect dependency order, record deviations/evidence, run both `$vet` and `$exercise` as independent gates, update the living plan, and stop before publishing unless the user separately authorizes it.
- `vet` must evaluate a neutral change bundle in a fresh context, probe beyond the happy path, and return an explicit `SHIP` or `HOLD` verdict. Passing tests alone is not sufficient evidence.
- Research under `~/Sites/sb` strengthens the workflow contract: harness state should be executable, inspectable, stateful, and governed; planning is a change contract; approvals are durable state; and verification must state what each oracle proves and does not prove.
- The current main-branch baseline is `67 passed` from `python3 -m pytest -q`.

### Locked decisions

1. Codex invocation is `$discover -> $spec -> $craft`; `$craft` runs `$vet` and `$exercise` as separate gates before its final handoff.
2. Markdown artifacts are the source of truth. This change does not add generated HTML plans or unknowns maps.
3. `$craft` becomes the build orchestrator. The legacy CRAFT acronym workflow remains available as `/prompts:neural.craft` and through `.codex/templates/craft.yaml`.
4. `plan-execute` remains documented as a lightweight alternative; it is not an alias for the gated pipeline.
5. `code-reviewer` remains a reusable review checklist/persona; `$vet` becomes the formal pre-ship gate and may reuse non-conflicting review guidance.
6. The implementation targets `neural-codex` only. The missing published Claude `discover` skill is recorded as upstream drift for a separate `neural-claude-code` change.
7. Existing installer behavior is reused: skills added under `.agents/skills/` must flow through `setup-global.sh` and `setup-project.sh` without a second installer path.

## Signatures

- `$discover [task]` -> `plans/<YYYY-MM-DD-task>/unknowns-map.md` [new] -> `.agents/skills/discover/SKILL.md`
- `UnknownsMap = { context, knownKnowns, knownUnknowns, unknownKnowns, unknownUnknowns, resolvedDecisions, references, remainingUnknowns, recommendedNextStep }` [adapt] -> `.agents/skills/discover/references/unknowns-framework.md`
- `$spec [task] [--no-html accepted as compatibility no-op]` -> `plans/<YYYY-MM-DD-task>/plan.md` and STOP [new] -> `.agents/skills/spec/SKILL.md`
- `PlanArtifact = { frontmatter, context, signatures, securityInvariants, subtasks, outOfScope, openQuestions, notes, amendLog }` [adapt] -> `.agents/skills/spec/SKILL.md`
- `Subtask = { id, state, description, needs, tier, acceptance, verify }` [adapt] -> `.agents/skills/spec/SKILL.md`
- `$craft [approved-plan-path]` -> updated plan, baseline, implementation evidence, gate results, ship handoff [replace] -> `.agents/skills/craft/SKILL.md`
- `BuildEvidence = { baseline, changedFiles, verificationCommands, verificationResults, deviations, vetVerdict, exerciseVerdict }` [new] -> `.agents/skills/craft/SKILL.md`
- `/prompts:neural.craft TASK=<summary> [--mode interactive|quick|loop]` -> `plans/craft/<slug>.yaml` [reuse] -> `.codex/prompts/neural.craft.md`
- `$vet [change-scope]` -> `VetVerdict` [new] -> `.agents/skills/vet/SKILL.md`
- `ReviewBundle = { objective, acceptance, baseRef, headRef, diff, tests, constraints }` [new] -> `.agents/skills/vet/SKILL.md`
- `VetVerdict = { verdict: SHIP|HOLD, findings, probes, evidence, residualRisk }` [new] -> `.agents/skills/vet/SKILL.md`
- `$exercise [--spec <plan>]` -> evidence-backed behavioral `PASS|FAIL` verdict [new supporting gate] -> `.agents/skills/exercise/SKILL.md`
- `PIPELINE_SKILLS = [discover, spec, craft, vet]` [new] -> `tests/test_pipeline_skills.py`
- `docs/WORKFLOW.md` as the canonical user-facing pipeline guide [new] -> `docs/WORKFLOW.md`

## Security invariants

- @invariant: generated artifacts stay under a repository-relative `plans/<date>-<slug>/` path; user-controlled slugs cannot escape the repository through traversal (CWE-22).
- @invariant: discovery maps, plans, baselines, diffs, and review bundles must never copy secrets, `.env` contents, tokens, or sensitive command output into durable evidence (CWE-200).
- @invariant: any fresh-context reviewer transport must pass refs, paths, and user text as data rather than interpolating untrusted values into executable shell fragments (CWE-78).
- @invariant: `$craft` and `$vet` may prepare changes and verdicts but may not commit, push, open or merge a PR, deploy, or send external messages without explicit authorization for that side effect (CWE-862).
- @invariant: a green unit-test command cannot weaken or replace the independent behavioral and semantic gates; failed, skipped, unavailable, or inconclusive gates are reported as such and cannot be presented as success (CWE-693).
- @invariant: approval state is explicit in `plan.md`; `$craft` must not infer approval from the existence of a draft file (CWE-284).

## Subtasks

<!-- state legend: [ ] todo | [~] in-progress | [x] done | [!] blocked/failed (reason inline) -->
<!-- deps: append [needs: S1, S2] to gate a subtask; no needs = runs in parallel -->
<!-- tier: append [tier: cheap|mid|hard|batch] to route the subtask -->

- [x] S1: Add the Codex-native `$discover` skill and its portable unknowns framework [tier: hard]
  - when: a user invokes `$discover` for non-trivial work
  - requires: repository context is readable; no implementation edits are authorized by discovery
  - ensures: the skill performs the grounded blindspot pass, four-quadrant map, architecture-first interview, reference capture, and writes only `unknowns-map.md` before recommending `$spec` or a prototype
  - ensures: the artifact distinguishes resolved decisions from remaining/blocking unknowns and records source paths or URLs
  - verify: `python3 /Users/brolag/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/discover`
  - test: `python3 -m pytest -q tests/test_pipeline_skills.py -k discover`
  - must_not_include: `.claude/skills/`, `AskUserQuestion`, `Agent(`, `Skill(`, or a mandatory HTML dependency

- [x] S2: Add the Codex-native `$spec` planning gate that consumes discovery state [tier: hard]
  - when: a user invokes `$spec` with a recent related `unknowns-map.md`
  - requires: discovery decisions are treated as input rather than re-asked; unresolved architecture blockers remain visible
  - ensures: `plan.md` contains draft frontmatter, locked signatures, CWE invariants, dependency/tier-tagged subtasks, executable `when/requires/ensures` acceptance, contradiction/dependency scans, explicit non-goals, and STOP-for-approval behavior
  - ensures: without a discovery artifact, `$spec` performs only the minimum clarification needed and records that discovery was skipped
  - verify: `python3 /Users/brolag/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/spec`
  - test: `python3 -m pytest -q tests/test_pipeline_skills.py -k spec`
  - must_include: `unknowns-map.md`, `status: draft`, `[needs:`, `[tier:`, `Security invariants`, `STOP`

- [x] S3: Replace the conflicting `$craft` skill with the approved-plan build orchestrator while preserving the namespaced legacy CRAFT prompt [needs: S2] [tier: hard]
  - when: a user invokes `$craft` with a plan whose frontmatter is `status: approved`
  - requires: a reproducible baseline and pre-existing dirty state are captured before implementation; the `[needs:]` graph is valid
  - ensures: subtasks execute in dependency order, independent work may run in parallel when supported, failures block dependents, plan state/evidence/deviations are append-only, and `$vet` plus `$exercise` both run before the ship handoff
  - ensures: a draft/blocked/missing plan causes a clear stop; no automatic commit/push/merge occurs
  - ensures: `.codex/prompts/neural.craft.md` and `.codex/templates/craft.yaml` continue to produce the legacy CRAFT YAML workflow
  - verify: `python3 /Users/brolag/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/craft`
  - test: `python3 -m pytest -q tests/test_pipeline_skills.py -k craft`
  - must_include: `status: approved`, `baseline`, `$vet`, `$exercise`, `[needs:]`

- [x] S4: Add the Codex-native `$vet` independent review gate and its `$exercise` behavioral companion [tier: hard]
  - when: a completed change is submitted for review
  - requires: the reviewer receives a neutral `ReviewBundle`, not the implementer's persuasive narrative; fresh-context transport uses a Codex-supported isolation mechanism
  - ensures: review covers acceptance, regression risk, security boundaries, slop/dead-code cleanup, active probes, and returns exactly `SHIP` or `HOLD` with evidence
  - ensures: unavailable clean-context isolation, unrun required probes, or material uncertainty are explicit limitations rather than silently converted to `SHIP`
  - ensures: `$exercise` is distributed with the repository and independently drives the installed workflow or application as a user, with evidence for every scenario
  - verify: `python3 /Users/brolag/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/vet`
  - test: `python3 -m pytest -q tests/test_pipeline_skills.py -k vet`
  - must_not_include: `.claude/`, `AskUserQuestion`, `Task(`, or unsupported Claude hook/tool contracts

- [x] S5: Add contract tests for the four-stage workflow and its legacy-name compatibility [needs: S1, S2, S3, S4] [tier: mid]
  - when: any pipeline skill, README inventory, or installer behavior changes
  - requires: tests inspect both structural validity and semantic handoffs; schema validity alone is not accepted as proof of a correct port
  - ensures: all four skills exist and validate; `discover -> spec -> craft -> vet/exercise` artifact/state transitions are asserted; Claude-only vocabulary is rejected; the legacy `/prompts:neural.craft` contract remains intact
  - ensures: dependency references are valid and acyclic in the documented example; draft plans cannot satisfy craft's approval precondition
  - verify: `python3 -m pytest -q tests/test_pipeline_skills.py tests/test_skills_core.py tests/test_prompts_core.py tests/test_setup_install.py`
  - test: `tests/test_pipeline_skills.py`

- [x] S6: Document the pipeline clearly in both READMEs, the docs set, and the GitHub Page [needs: S1, S2, S3, S4] [tier: mid]
  - when: a new user lands on the README or GitHub Page and wants the recommended development workflow
  - requires: `$skill` invocations are distinguished from namespaced `/prompts:neural.*`; the legacy CRAFT builder is not mislabeled as the build orchestrator
  - ensures: `README.md`, `README-neural-codex.md`, `docs/README.md`, `docs/AGENT-HARNESS.md`, new `docs/WORKFLOW.md`, and `docs/index.html` explain entry/exit artifacts, approval pauses, failure behavior, and the independent roles of `$vet` and `$exercise`
  - ensures: `plan-execute` and `code-reviewer` are positioned without ambiguity; installation and verification commands are copy-pasteable; the page remains responsive and accessible
  - verify: `python3 -m pytest -q tests/test_docs_readme.py`
  - verify: `bash scripts/doc-lint.sh`
  - test: `tests/test_docs_readme.py`

- [x] S7: Exercise installation and the artifact/state flow in an isolated temporary project [needs: S5, S6] [tier: batch]
  - when: the repository skills are installed globally and seeded into a clean project using a temporary `HOME` and `CODEX_HOME`
  - requires: no writes reach the user's live Codex installation; the fixture contains a draft discovery map and plan lifecycle scenario
  - ensures: `discover`, `spec`, `craft`, `vet`, and supporting gate `exercise` are installed in both supported skill roots; the project receives all five; legacy CRAFT prompt/template files remain available; evidence records what was executed versus only statically inspected
  - verify: `python3 -m pytest -q tests/test_setup_install.py tests/test_pipeline_skills.py`
  - verify: `python3 -m pytest -q`

- [x] S8: Run final `$vet` and `$exercise` gates and record the before/after delta [needs: S7] [tier: hard]
  - when: implementation and documentation are complete
  - requires: baseline is the recorded `67 passed`; review runs in clean context; behavioral verification covers README-to-install-to-skill-discovery flow and GitHub Page presentation
  - ensures: final evidence contains full-suite result, skill validation result for all four skills, docs/link checks, installer smoke result, behavioral observations, `SHIP|HOLD`, and residual risks
  - ensures: any failed or unavailable required gate leaves the plan blocked instead of done
  - verify: `python3 -m pytest -q`
  - verify: `for skill in discover spec craft vet exercise; do python3 /Users/brolag/.codex/skills/.system/skill-creator/scripts/quick_validate.py ".agents/skills/$skill"; done`

## Contradiction scan

- **`craft` name collision:** resolved by assigning `$craft` to the build orchestrator while retaining the legacy CRAFT acronym as `/prompts:neural.craft` plus its YAML template.
- **`spec` writes no code but does write an artifact:** resolved by allowing only the scoped `plan.md` planning artifact before approval.
- **Fresh review vs recursive Codex caution:** the implementation must define a supported isolation/transport ladder and must not assume recursive CLI execution is always available. Lack of genuine isolation is a disclosed limitation, not a silent self-review.
- **Parallelism vs dependencies:** only subtasks without `[needs:]` may fan out; a failed prerequisite blocks descendants. The graph above is acyclic and all referenced IDs exist.
- **Tests vs real behavior:** static skill-contract tests establish portability, while `$exercise` separately verifies the installed user flow. Neither substitutes for the other.
- **Claude parity vs Codex nativeness:** semantic behavior is ported; Claude tool names, paths, HTML dependencies, and hook contracts are not.

## Out of scope

- Adding `discover` to the separate `brolag/neural-claude-code` repository in this change.
- Adding or porting `discover-standards`, `playground`, PlanViewer, or any HTML artifact generator.
- Deleting `plan-execute`, `code-reviewer`, `.codex/prompts/neural.craft.md`, or `.codex/templates/craft.yaml`.
- Installing the draft skills into the user's live `~/.codex`, `~/.agents`, or a production project.
- Changing the existing hooks, GPT-5.6 profiles, MCP configuration, Ralph loop, or model-routing runtime except where documentation must explain their relationship to the pipeline.
- Automatic commits, pushes, PR creation/merge, deployment, or cross-repository publication.

## Open questions

- None blocking. The implementation decisions above are locked for review; a follow-up plan can port the missing `discover` skill to `neural-claude-code` after this Codex workflow ships.

## Notes

- The published Claude repository is behind the local Claude skill set, so remote parity alone would reproduce the omission. The local current workflow plus Codex constraints is the correct source combination.
- The `~/Sites/sb` review adds three quality requirements beyond a mechanical port: explicit durable state, declared verification coverage/limitations, and governed human approval before side effects.
- Documentation clarity should be judged from the user's path (choose a gate -> inspect the artifact -> approve -> build -> understand evidence/verdict), not only by listing four new skill names.
- The current branch is `feat/discover-spec-craft-vet` from merged `origin/main`; only this plan artifact is created during the planning gate.

## Amend log

<!-- append-only; post-approval changes: YYYY-MM-DD - what changed - why -->
- 2026-07-12 - Plan approved through explicit `$craft` invocation; no scope or signature changes.
- 2026-07-12 - Added the missing `$exercise` supporting-skill signature after implementation inspection showed the repository could not execute craft's required behavioral gate after a clean install; this preserves the approved pipeline contract.
- 2026-07-12 - First independent `$vet` returned HOLD; added targeted legacy-craft migration, complete untracked review-bundle accounting, and explicit `plans/` path-containment contracts plus regression tests.
- 2026-07-12 - Second independent `$vet` exposed a mixed customized-staging upgrade; migration now archives customized legacy directories as `craft.legacy-backup` and always activates the canonical orchestrator downstream.
- 2026-07-12 - Third independent `$vet` found a stale installed project installer and missing exercise path containment; setup entrypoints now refresh during normal upgrades, exercise validates all artifact paths, and generated browser snapshots are ignored.
