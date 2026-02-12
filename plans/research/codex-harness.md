# Research: Codex Harness — Best-in-Class Alignment

## Summary
OpenAI’s harness engineering guidance emphasizes a structured knowledge base, short `AGENTS.md` as a table of contents, mechanical doc hygiene, and durable ExecPlans for long-running work. Codex’s official docs specify `AGENTS.override.md` precedence, configurable fallback filenames, and `.agents/skills` as the canonical skills location. The implementation below aligns the repo with those standards.

## Key Facts (from OpenAI sources)
- Harness engineering recommends `AGENTS.md` as a short index and a structured `docs/` tree with design docs, exec plans, product specs, references, and generated artifacts, enforced with mechanical checks and doc-gardening. (OpenAI harness engineering)
- Codex loads instructions in order and supports `AGENTS.override.md` to supersede `AGENTS.md`, plus configurable fallback filenames and size caps. (OpenAI Codex: Unrolling the agent loop + config)
- Codex skills are discovered from `.agents/skills` (repo, user, admin, system scopes). (OpenAI Codex skills docs)
- OpenAI recommends combining **skills + shell + compaction** for long-running, reliable work and using strict allowlists for safety. (OpenAI skills/shell tips)
- OpenAI’s cookbook recommends using `PLANS.md` (ExecPlan) for multi-hour tasks with explicit checkpoints and updates. (OpenAI cookbook)

## Current Alignment (implemented)
- Added a structured docs tree with indexes and core guides in `docs/`.
- Added `docs/PLANS.md` (ExecPlan template) and `docs/exec-plans/` folders.
- Added `ARCHITECTURE.md` and expanded `AGENTS.md` with a concise knowledge map.
- Moved skills to `.agents/skills` as canonical and added a legacy sync path.
- Added a doc lint script (`scripts/doc-lint.py`) and tests to enforce doc structure.
- Added `.codex/config.toml` settings for `project_doc_fallback_filenames` and `project_doc_max_bytes`.

## Trade-offs
| Approach | Pros | Cons |
|---|---|---|
| Lean harness | Low overhead, fast onboarding | Knowledge drift, weaker long-run reliability |
| Full harness (current) | Durable knowledge base, better autonomy, clearer ops | More docs to maintain and validate |

## Recommendations (next)
1. Add CI to run `scripts/doc-lint.py` and tests on every PR.
2. Create a lightweight doc-gardening automation (weekly) to validate staleness and link health.
3. Expand `docs/references/` with primary sources for Codex usage and internal standards.

## Sources
- https://openai.com/index/harness-engineering/
- https://openai.com/index/unrolling-the-codex-agent-loop/
- https://developers.openai.com/codex/skills/
- https://developers.openai.com/blog/skills-shell-tips
- https://developers.openai.com/codex/config-advanced/
- https://cookbook.openai.com/examples/agents/plan_write_execute
