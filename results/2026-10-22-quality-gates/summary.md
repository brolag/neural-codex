# Quality-gate evaluation — 2026-10-22

Baseline: `79218b6`. Client: Codex CLI 0.153.3. Complete six-case before/after
runs used identical fixture inputs and the same hardened runner. The JSON report
records the current fixture/runner hashes and each evaluated skill hash.

| Measure | Before | After |
|---|---:|---:|
| Correct verdict and grounded defect location | 6/6 | 6/6 |
| Explicit gate applicability, results, and evidence | 0/6 | 6/6 |

The original skills already made the correct decisions on these cases. The
measured improvement is explicit, consistent gate coverage; these results do
not establish a general accuracy improvement.

Cases: web planning, internal-library planning, duplicate abstraction,
missing owner check, acceptable internal fix, and CLI error recovery.
The positive internal fix returned `SHIP`; the defect cases were rejected.
Runnable cases retain actual command observations in [decisions.json](decisions.json).
The CLI helper emitted observed error code 2 with `E42`, followed by a successful
CSV retry; the missing recovery explanation correctly failed usability.

## Independent review and hardening

A fresh reviewer returned `HOLD` after reproducing runtime false positives:
a failed fixture command with fallback output, a same-named decoy, and a relative
command run from a different directory. The oracle now validates the entire
simple wrapper and requires the absolute path of the selected fixture script.
The evaluator prompt supplies that path. Real subprocess regression tests cover
all three failures and a genuine fixture run from a changed directory.

The reviewer rechecked the patch and returned `SHIP` with no material findings.
Both complete six-case live runs were then repeated with the hardened evaluator;
the report contains only those refreshed results. Validation: 89 Python tests,
documentation lint, plugin validator, and all five skill validators passed.
Existing hooks and exactly five skills were preserved.

## Scope and limits

Expected answers are withheld. Per-run settings disable automatic AGENTS.md
inclusion, plugin/app loading, and delegation. Skill instructions are supplied
through a fixture file to avoid explicit skill auto-loading from dollar mentions.
The grader separates verdict correctness from gate IDs, accepts capitalization
differences, and rejects source text or an agent's claim as runtime evidence.
Some read-only Python launcher cache warnings occurred; the observed scripts
completed successfully.

These are bounded synthetic probes, not a full artifact workflow, browser audit,
human satisfaction study, or standards certification. Model behavior can vary.
Raw local runs remain under the ignored plan directory. Reproduce with the
runner documented in [VERIFICATION](../../docs/VERIFICATION.md).
