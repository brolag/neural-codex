# Exercise Report

Target: neural-codex workflow skills, installers, documentation, and GitHub Page

Backends: CLI fixture and Playwright browser

Tests: 81 passed, 0 failed; one pre-existing `pytest_asyncio` deprecation warning

Scenarios: 4 run, 4 passed

## PASS: Install the complete workflow in an isolated environment

- Steps: created a temporary `HOME`, `CODEX_HOME`, and project; ran `scripts/setup-global.sh --force`; ran `scripts/setup-project.sh --force --path <fixture-project>`.
- Expected: `discover`, `spec`, `craft`, `vet`, and `exercise` are installed in global and project skill roots without touching the live user installation.
- Observed: all five `SKILL.md` files existed under global `~/.agents/skills`, global `$CODEX_HOME/skills`, project `.agents/skills`, and project `.codex/skills`.
- Evidence: terminal output reported `PASS` for all four destinations; fixture was `/tmp/neural-codex-exercise.bWYRlK`.

## PASS: Preserve the legacy CRAFT workflow

- Steps: inspected the isolated project's seeded prompt and template after setup.
- Expected: replacing `$craft` does not remove `/prompts:neural.craft` or `.codex/templates/craft.yaml`.
- Observed: both files were present in the fixture and the semantic contract test passed.
- Evidence: terminal output reported `PASS legacy CRAFT prompt and template preserved`; `tests/test_pipeline_skills.py::test_legacy_craft_prompt_and_template_are_preserved` passed.

## PASS: Upgrade the exact legacy `$craft` without `--force`

- Steps: seeded the legacy CRAFT-builder `SKILL.md` into three global and two project skill roots, seeded a stale installed `setup-project.sh`, then ran global setup and invoked the refreshed updater from `$CODEX_HOME` without `--force`.
- Expected: the installed updater is refreshed, the known bundled legacy skill is replaced by the build orchestrator in all five roots, the other pipeline skills are installed, and customized copies remain archived safely.
- Observed: the installers reported three global and two project migrations; every root contained the new `# Craft` orchestrator plus `discover`, `spec`, `vet`, and `exercise`. A mixed-state probe with a customized staging directory archived its companion file and still activated the new orchestrator in all downstream roots. The formerly stale updater matched the repository script before it seeded the project.
- Evidence: terminal output reported `PASS upgraded workflow`, `PASS active orchestrator`, and `PASS installed setup-project refreshed`; fixtures were `/tmp/neural-codex-upgrade-exercise.rtNviZ`, `/tmp/neural-codex-mixed-upgrade.MfWWx9`, and `/tmp/neural-codex-installed-upgrade.2MTofR`; upgrade regression tests passed.

## PASS: Use the workflow section on desktop and mobile

- Steps: served `docs/` locally, opened it with Playwright, followed the `workflow` navigation link, inspected the five gate cards, checked console warnings, and repeated at 1440x1000 and 390x844.
- Expected: all five gates and the legacy CRAFT distinction are visible, navigation works, the page has no horizontal viewport overflow, and the console is clean.
- Observed: five workflow cards rendered; desktop and mobile document widths matched their viewports; the initial mobile exercise exposed a 39 px command overflow, clipped heading, and overlapping fixed badge, all fixed before rerunning; final console had 0 errors and 0 warnings.
- Evidence: ignored screenshots at `exercise-evidence/playwright/workflow-desktop-final.png` and `exercise-evidence/playwright/workflow-mobile-final-v2.png`; final mobile viewport was exactly 390x844 and the badge used static mobile positioning.

## Verdict: PASS

The installed and upgraded workflow is self-contained, the legacy prompt remains available, the documented route is usable, and every required scenario has direct CLI or browser evidence.

## Residual risk

- The browser run exercised the local static page, not GitHub Pages' CDN after merge.
- Skill behavior is validated through schema, semantic contract tests, and installation flow; live agent quality still depends on the host Codex version and the repository context supplied at invocation time.
