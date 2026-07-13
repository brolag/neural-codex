---
project: neural-codex
created: 2026-07-12
status: done
modified:
  - 2026-07-12
commits:
  - a4c47d0
  - d713756
related:
  back:
    - plans/2026-07-12-discover-spec-craft-vet/plan.md
    - plans/research/2026-07-12-hooks-gpt-5-6.md
    - https://developers.openai.com/codex/plugins/build
    - https://developers.openai.com/codex/concepts/customization
    - https://developers.openai.com/codex/config-advanced
    - https://developers.openai.com/codex/custom-prompts
  forward: []
---

# Plan: neural-codex / Trim to the reviewed Codex plugin core

## Context

`neural-codex` currently contains 193 tracked files and mixes three generations of distribution: 45 deprecated custom prompts under `.codex/prompts/`, 28 repo-local skills under `.agents/skills/`, eight persona trees under `agents/`, custom setup scripts, Ralph-loop task state, and the newly reviewed `discover -> spec -> craft -> vet -> exercise` workflow. The README, architecture guide, project instructions, tests, and GitHub Page still advertise both generations as if they were one supported product.

The approved direction is a breaking cleanup to the current Codex plugin standard:

```text
.agents/plugins/marketplace.json
plugins/neural-codex/.codex-plugin/plugin.json
plugins/neural-codex/skills/{discover,spec,craft,vet,exercise}/...
plugins/neural-codex/hooks/{hooks.json,README.md,*.py}
docs/{index.html,README.md,AGENT-HARNESS.md,CONFIGURATION.md,HOOKS.md,VERIFICATION.md,WORKFLOW.md,favicon.svg,.nojekyll}
tests/{test_plugin_structure.py,test_pipeline_skills.py,test_hooks.py,test_docs.py}
```

The canonical workflow skills move from `.agents/skills/` to `plugins/neural-codex/skills/`; hooks move from `.codex/hooks*` to `plugins/neural-codex/hooks/` and resolve handlers through `${PLUGIN_ROOT}`. A repo marketplace entry points at `./plugins/neural-codex` and makes the catalog discoverable through `codex plugin marketplace add brolag/neural-codex`. Plugin installation will not mutate a user's `~/.codex/config.toml`; GPT-5.6 reasoning, verbosity, approval, and sandbox recommendations remain explicit documentation rather than bundled profiles or installer side effects.

The retained product is exactly five workflow skills plus the reviewed safety hooks. Remove deprecated prompts, old skills/personas, Ralph loops, task-state templates, duplicate setup paths, and documentation/tests that only exist to support them. Keep historical evidence from the immediately preceding reviewed migration and the new plan, but remove superseded generic scaffolding and old task-state files.

Contradiction scan:

- `.agents/skills/` is valid for repo-local authoring, while `skills/` is required for a distributable plugin. The approved distribution requirement wins; there will be one canonical skill copy under `skills/`.
- `.codex/hooks.json` is valid for project-local hooks, while `hooks/hooks.json` is the plugin convention. The approved plugin requirement wins; hook commands use `${PLUGIN_ROOT}` and no project-root lookup.
- Standalone `.codex/profiles/*.config.toml` preserve prior convenience but are not a plugin component and can silently overwrite user policy. They are removed; equivalent safe examples are documented without automated installation.
- The previous compatibility promise for `/prompts:neural.craft` conflicts with Codex's deprecation of shared custom prompts and the requested cleanup. Compatibility is intentionally dropped and documented as a breaking change.
- The repository currently has no detected license. The plugin manifest must not claim `MIT` or another license until a license file is explicitly added in a separate decision.

## Signatures

- `{ name: "neural-codex", version: string, description: string, author: object, homepage: string, repository: string, keywords: string[], skills: "./skills/", interface: object }` [new] -> `plugins/neural-codex/.codex-plugin/plugin.json`; omit `hooks` because the default `./hooks/hooks.json` is auto-discovered
- `{ name: "neural-codex", interface: { displayName: "Neural Codex" }, plugins: [{ name: "neural-codex", source: { source: "local", path: "./plugins/neural-codex" }, policy: { installation: "AVAILABLE", authentication: "ON_INSTALL" }, category: "Developer Tools" }] }` [new] -> `.agents/plugins/marketplace.json`
- `skills/<name>/SKILL.md`, where `<name>` is exactly one of `discover | spec | craft | vet | exercise` [adapt] -> `plugins/neural-codex/skills/`
- `{ hooks: { PreToolUse: HookGroup[], PostToolUse: HookGroup[], PreCompact: HookGroup[] } }` [adapt] -> `plugins/neural-codex/hooks/hooks.json`
- `command = 'python3 "${PLUGIN_ROOT}/hooks/<handler>.py"'` [adapt] -> every command hook in `plugins/neural-codex/hooks/hooks.json`
- `main(): int` and existing JSON stdin/stdout contracts for hook handlers [reuse] -> `plugins/neural-codex/hooks/*.py`
- `README -> install -> discover -> spec -> craft -> vet -> exercise` [adapt] -> `README.md`, `docs/README.md`, `docs/WORKFLOW.md`, `docs/index.html`
- `recommended_config(profile: safe | fast | autonomous | careful): TOML example` [adapt] -> `docs/CONFIGURATION.md` as documentation only, never an installer or plugin mutation

## Security invariants

- @invariant: every plugin manifest path starts with `./`, resolves inside the plugin root, and cannot traverse upward (CWE-22).
- @invariant: hook commands quote `${PLUGIN_ROOT}` and append only repository-controlled handler names; hook input must never become shell syntax (CWE-78).
- @invariant: the sensitive-file guard and output scanner continue to fail closed for protected paths and detected secret material without echoing secret values (CWE-200).
- @invariant: installation instructions use the Codex marketplace flow and an exact GitHub source; they never recommend `curl | sh`, arbitrary remote execution, or implicit installer scripts (CWE-494).
- @invariant: no committed config, fixture, documentation example, or test contains credentials; MCP examples use placeholders and no `.env` file is read or modified (CWE-798).
- @invariant: plugin hooks remain untrusted until the user reviews and trusts them through Codex; documentation must not imply installation automatically grants hook execution (CWE-829).

## Subtasks

<!-- state legend: [ ] todo | [~] in-progress | [x] done | [!] blocked (reason inline) -->

- [x] S1: Capture the pre-cleanup baseline and finalize a tracked-file keep/remove matrix before destructive edits; invoke `$plugin-creator` and follow its scaffold contract for the plugin manifest and marketplace metadata. -- verify: `git status --short && git ls-files | wc -l && test -f plans/2026-07-12-discover-spec-craft-vet/vet-report.md && test -f plans/research/2026-07-12-hooks-gpt-5-6.md`
- [x] S2: Create the official repo marketplace and nested plugin surfaces, move the five reviewed skills to canonical `plugins/neural-codex/skills/`, and remove duplicate skill roots. Preserve each skill's scripts/references/assets only when reachable from its `SKILL.md`. -- verify: `python3 -m json.tool plugins/neural-codex/.codex-plugin/plugin.json >/dev/null && python3 -m json.tool .agents/plugins/marketplace.json >/dev/null && test "$(find plugins/neural-codex/skills -mindepth 1 -maxdepth 1 -type d | sed 's#plugins/neural-codex/skills/##' | sort | tr '\n' ' ')" = "craft discover exercise spec vet " && test ! -e .agents/skills && test ! -e .codex/skills` | test: `tests/test_plugin_structure.py`
- [x] S3: Migrate the reviewed hooks to plugin-root `plugins/neural-codex/hooks/`, replace project-root path discovery with quoted `${PLUGIN_ROOT}` paths, retain the trust boundary, and verify all hook event contracts and adversarial fixtures. -- verify: `python3 -m pytest -q tests/test_hooks.py && ! rg -n 'git rev-parse|\.codex/hooks' plugins/neural-codex/hooks` | must_include: `${PLUGIN_ROOT}` | test: `tests/test_hooks.py`
- [x] S4: Delete the unsupported generations: `.codex/prompts/`, `.codex/templates/`, `.codex/profiles/`, `.codex/config.toml`, `agents/`, the 23 non-core skills, Ralph/memory/sync/Telegram/YouTube/setup scripts, their fixtures/tests, and old `plans/{prd.json,progress.jsonl,task-list.md,design-neural-codex.md}`. Retain `scripts/doc-lint.sh` only if CI still calls it after cleanup. -- verify: `test ! -e .codex/prompts && test ! -e .codex/templates && test ! -e .codex/profiles && test ! -e agents && test ! -e scripts/setup-global.sh && test ! -e scripts/setup-project.sh && test ! -e scripts/ralph-loop.sh && test ! -e plans/prd.json && test ! -e plans/progress.jsonl`
- [x] S5: Rewrite `README.md`, `AGENTS.md`, and `ARCHITECTURE.md` as a concise, truthful description of the plugin; remove duplicate `README-neural-codex.md`; reduce `docs/` to the workflow, hook, verification, harness, configuration, and GitHub Page surfaces; and clearly label the removal of legacy commands as a breaking change. -- verify: `./scripts/doc-lint.sh && ! rg -n 'Ralph loop|/prompts:|\.codex/prompts|agents/\*/AGENTS|setup-global|setup-project|plan-execute|code-reviewer|slop-scan|memory-system' README.md AGENTS.md ARCHITECTURE.md docs` | test: `tests/test_docs.py`
- [x] S6: Replace inventory tests with semantic plugin tests: manifest/path schema, exact five-skill allowlist, skill frontmatter and cross-links, hook portability/trust, stale-reference denial, marketplace source, README commands, GitHub Page links, and validation of every retained skill with Codex's `quick_validate.py`. Update CI to run only the supported suite. -- verify: `for skill in plugins/neural-codex/skills/*; do python3 /Users/brolag/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$skill" || exit 1; done && python3 -m pytest -q && ./scripts/doc-lint.sh` | test: `tests/`
- [x] S7: Exercise the result as a user: add the local marketplace, confirm Codex resolves the plugin and exactly five skills, review/trust hooks in a disposable context, run a representative `discover -> spec -> craft -> vet -> exercise` dry workflow, and inspect the GitHub Page at desktop and mobile widths with no broken links or stale capability claims. Record exact commands, screenshots, and results without committing machine-specific paths or caches. -- verify: `test -f plans/2026-07-12-trim-neural-codex-core/exercise-report.md && rg -n 'PASS|FAIL|BLOCKED' plans/2026-07-12-trim-neural-codex-core/exercise-report.md`
- [x] S8: Run a clean-context `$vet` review over the complete branch diff, resolve every actionable finding, rerun the full validation, push a feature branch, open a ready PR, wait for required checks, and squash-merge only on a SHIP verdict and green required checks. -- verify: `test -f plans/2026-07-12-trim-neural-codex-core/vet-report.md && rg -n 'SHIP' plans/2026-07-12-trim-neural-codex-core/vet-report.md && git status --short && gh pr checks --watch` | must_include: `SHIP`

## Out of scope

- Publishing Neural Codex to OpenAI's public Plugins Directory or requesting workspace-wide administrative rollout.
- Adding MCP servers, connectors, `.app.json`, authentication, telemetry, or network services.
- Preserving backward compatibility for `.codex/prompts`, `neural.*` prompt names, Ralph Loop, personas, legacy skills, or the setup scripts.
- Automatically changing a user's model, reasoning effort, approval policy, sandbox, global configuration, or trusted-hook state.
- Claiming a software license before the repository contains an explicit license file.
- Modifying `neural-claude-code`; it remains research/reference input only.

## Open questions

- None. The user approved the breaking migration to the official plugin format and requested only this Markdown plan before implementation.

## Notes

Official Codex documentation confirms that distributable plugins use `.codex-plugin/plugin.json`, root `skills/`, and root `hooks/hooks.json`; plugin hook commands receive `${PLUGIN_ROOT}` and `${PLUGIN_DATA}`. For a repo marketplace, `$plugin-creator` requires the plugin at `plugins/neural-codex/` and the marketplace source `./plugins/neural-codex`; its validator also requires omitting the redundant `hooks` manifest field because default discovery already loads `hooks/hooks.json`. Codex also marks custom prompts as deprecated in favor of skills. The implementation must validate semantics as well as directory shape: a schema-valid plugin that still advertises removed workflows is not complete.

No optional HTML rendering was requested, so `plan.md` is the only plan artifact.

## Amend log

<!-- append-only; post-approval changes: YYYY-MM-DD - what changed - why -->
- 2026-07-12 - Moved the installable plugin under `plugins/neural-codex/`, changed the repo marketplace to the canonical local source path, and removed the redundant manifest `hooks` field - required by `$plugin-creator` repo-marketplace and validation contracts discovered at implementation start.
- 2026-07-12 - Replaced the hardcoded GPT-5.6 Codex example with product-aware model guidance - live Codex CLI 0.142.5 rejected that ID for ChatGPT authentication, while the default available model completed the full plugin workflow.
- 2026-07-12 - Reactivated the inactive GitHub Actions workflow and expanded it from documentation lint to the supported pytest plus documentation suite - required to obtain a real green PR check before merge.
