# Quality-gate evaluation — 2026-10-22

Baseline: `79218b6`. Client: Codex CLI 0.153.3. Six synthetic cases used the same
fixture inputs before and after, with only the selected skill revision changed.
The JSON report records each skill hash and the current fixture/runner hashes.

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
For runnable cases the grader checked actual completed command observations.
The CLI helper emitted observed error code 2 with `E42`, followed by a successful
CSV retry; the missing recovery explanation correctly failed usability.

Validation: 79 Python tests, documentation lint, plugin validator, and all five
skill validators passed. Existing hooks and exactly five skills were preserved.

Evaluations were isolated from other installed skills. Prompts read the selected
instructions from a fixture file, avoiding explicit skill auto-loading from
embedded dollar mentions. Early contaminated attempts were discarded. Individual
cases were rerun when fixing evaluator isolation and command receipt capture;
this is a development check, not a statistical benchmark. Read-only Python
launcher cache warnings occurred, but the observed scripts completed.

Expected answers were withheld from evaluator prompts. The grader separates
verdict correctness from gate IDs, accepts capitalization differences, and does
not accept source text or an agent's claim as runtime evidence. Unit tests also
check false-green reports and unavailable execution.

Limits: no browser audit, full artifact workflow, human satisfaction study,
standards certification, or implementation-review pipeline was run. Model
behavior can vary. Raw local runs remain under the ignored plan directory;
the portable decisions are in [decisions.json](decisions.json). Reproduce with
the runner documented in [VERIFICATION](../../docs/VERIFICATION.md).
