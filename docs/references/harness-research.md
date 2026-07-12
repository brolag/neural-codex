# Harness Research Notes

These references explain the design choices in the neural-codex documentation.
They are guidance, not universal laws; most studies use bounded benchmarks and
specific agent/model versions.

## Actionable Findings

### Keep repository instructions minimal and curated

Two 2026 studies point in different directions but support the same practical
rule. Lulla et al. observed lower median runtime and output tokens with curated
`AGENTS.md` files on small real pull requests, but did not measure final
correctness. Gloaguen et al. found that unnecessary or generated context files
can reduce success and increase cost. Therefore, `AGENTS.md` should contain only
operational requirements that are not obvious from the repository, with deeper
material linked from `docs/`.

- [Lulla et al., On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents](https://arxiv.org/abs/2601.20404)
- [Gloaguen et al., Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?](https://arxiv.org/abs/2602.11988)

### Improve the whole harness, not only prompts

Lin et al. model harness improvement as an observability-driven loop over
instructions, tools, middleware, skills, subagents, and memory. Their results
support changing one component with a falsifiable prediction and validating the
next run instead of making broad prompt/control-flow rewrites together.

- [Lin et al., Agentic Harness Engineering](https://arxiv.org/abs/2604.25850)

### Evaluate changes on regression and held-out scenarios

Self-Harness separates weakness discovery, proposal, and validation, and reports
held-out pass rates rather than accepting improvements on the adaptation set
alone. neural-codex applies the same principle through positive/negative hook
tests, user-flow exercise, and independent review.

- [Zhang et al., Self-Harness: Harnesses That Improve Themselves](https://arxiv.org/abs/2606.09498)

### Audit the runtime as a system

Guo et al. decompose an agent runtime into observation, context, control loop,
actions, persistent state, and verification. This is a useful checklist when a
model upgrade does not translate into reliable task completion.

- [Guo et al., From Question Answering to Task Completion: A Survey on Agent System and Harness Design](https://arxiv.org/abs/2606.20683)

## Repository Implications

- `AGENTS.md` remains a short entry map, not a second README.
- Plans carry task-specific objective, non-goals, acceptance, and rollback.
- Hooks and tests inject deterministic feedback at the moment it is useful.
- Exercise evidence and clean-context review are separate gates.
- Harness changes should preserve raw failure evidence and be easy to reverse.
