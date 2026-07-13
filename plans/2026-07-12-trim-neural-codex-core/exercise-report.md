# Exercise Report

Target: Neural Codex plugin, repository marketplace, hooks, documentation, and GitHub Page  
Backends: CLI and isolated Playwright browser  
Tests: 45 passed, 0 failed; one environment-level `pytest-asyncio` deprecation warning  
Scenarios: 5 run, 5 passed

## PASS: Install from the repository marketplace

- Steps: created an isolated temporary `HOME` and `CODEX_HOME`; added the checkout as a local marketplace; listed available plugins; installed `neural-codex@neural-codex`; listed plugins again.
- Expected: Codex recognizes the marketplace and reports Neural Codex 1.0.0 as installed and enabled without changing the real user configuration.
- Observed: `codex plugin marketplace add` reported `Added marketplace neural-codex`; `codex plugin add` reported the plugin added; the final list reported `installed, enabled` and version `1.0.0`.
- Evidence: terminal output from the isolated CLI run; the temporary config contained only the local marketplace source and `plugins."neural-codex@neural-codex".enabled = true`.

## PASS: Installed inventory and hook behavior

- Steps: inspected the installed plugin cache, counted skill directories, checked the conventional hook manifest, ran the dangerous-action hook with a safe command and a destructive root deletion command.
- Expected: exactly `craft`, `discover`, `exercise`, `spec`, and `vet`; portable `${PLUGIN_ROOT}` hook commands; safe input exits 0; destructive input exits 2 without executing it.
- Observed: exactly the five expected skill directories were present; six hook commands referenced `${PLUGIN_ROOT}/hooks/`; `git status --short` was allowed; `rm -rf /` was rejected with `BLOCKED: Recursive deletion of a root or home directory` and exit 2.
- Evidence: CLI inventory and hook probe output. Installation did not create a hook-trust override, matching the documented manual `/hooks` review boundary.

## PASS: Five-gate workflow runs in fresh Codex tasks

- Steps: linked authentication into an isolated `CODEX_HOME` without reading or copying its contents; installed the plugin; created a disposable documentation repository; invoked `$discover`, `$spec`, approved and invoked `$craft`, then invoked `$vet` and `$exercise` in separate ephemeral Codex tasks. After reviewing the bundled hooks, the last four invocations used Codex's automation-only `--dangerously-bypass-hook-trust` flag inside the disposable environment.
- Expected: the plugin is selected by name; discovery and planning stop at their artifact boundaries; craft makes the approved change without committing; a fresh vet returns `SHIP`; a fresh exercise returns `PASS`; enabled hooks visibly run.
- Observed: `$discover` wrote `unknowns-map.md`; `$spec` wrote a draft `plan.md` without changing the README; `$craft` added the approved `## Installation` section and passed its `rg` check without committing; the fresh `$vet` task returned `SHIP`; the fresh `$exercise` task returned `PASS`. Trusted automation logs showed `hook: PreToolUse Completed` and `hook: PostToolUse Completed` throughout.
- Evidence: isolated Codex session outputs and final fixture checks `5:## Installation`, `9:## Usage`, with the required command exiting 0.

## PASS: Model availability is separated from prompting guidance

- Steps: attempted the requested GPT-5.6 model ID in the isolated Codex task, recorded the exact client error, then repeated without a model override.
- Expected: documentation must not claim API or ChatGPT model availability guarantees Codex client availability.
- Observed: Codex CLI 0.142.5 with ChatGPT authentication rejected `gpt-5.6` as unsupported. Without an override, Codex selected `gpt-5.5` and completed the live five-gate exercise.
- Evidence: exact error `The 'gpt-5.6' model is not supported when using Codex with a ChatGPT account.` and the successful default-model session headers.

## PASS: GitHub Page at desktop and mobile widths

- Steps: served `docs/` locally; opened the page at 1440x1000 and 390x844; captured semantic snapshots and full-page screenshots; inspected browser console output and both rendered images.
- Expected: readable five-gate workflow, marketplace commands, hook trust boundary, plugin structure, and GPT-5.6 guidance with no broken local assets, console errors, clipping, or page overflow.
- Observed: all required sections and links were present; console reported 0 errors and 0 warnings at both widths. The first pass revealed that direct Markdown links downloaded from the static server; links were changed to GitHub-rendered documents and rechecked. The mobile install commands were then wrapped to keep their full text visible.
- Evidence: [desktop screenshot](evidence/github-page-desktop.png) and [mobile screenshot](evidence/github-page-mobile.png).

## Documentation clarity cross-check

Read-only comparison against the relevant synthesized research in `~/Sites/sb` confirmed four harness properties that the docs now state explicitly:

- executable acceptance;
- inspectable plans, diffs, and evidence;
- state preserved across long work;
- governance through approval, sandbox, trust, and ship boundaries.

The docs also now recommend selective context and one focused change per plan. They do not reintroduce the removed agent, memory, prompt, or loop inventory.

## Verdict: PASS

All five scenarios passed with direct CLI, live Codex-task, or browser evidence.

## Residual risk

- The public GitHub Pages deployment still reflects `main` until the branch is merged and Pages finishes publishing; browser evidence covers the exact local artifact that will be published.
- Hook trust remains an explicit user decision in `/hooks`; the live workflow used the CLI's explicit automation bypass only after source review and only inside the disposable environment. No trust state was written to the user's real configuration.
