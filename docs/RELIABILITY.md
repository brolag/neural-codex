# Reliability

## Testing
- Use `TEST_CMD` for loop runs and CI.
- Prefer targeted tests for small changes.
- For blocking hooks, test dangerous variants and a safe neighboring command.
- Smoke-test global and project installation in isolated temporary directories.
- For user-facing changes, exercise the real CLI/browser/desktop flow and inspect errors.
- Preserve raw failing output before compressing it into a summary.

## Rollback
- Keep changes small and reversible.
- Document rollback steps in ExecPlans when risk is non-trivial.

## Circuit Breakers
- Stop automation on repeated failures.
- Log failure context in `plans/progress.jsonl`.
- Preserve recovery context through the `PreCompact` hook when available.

## Proof Of Work

- Record the exact command and pass/fail count.
- Link behavioral evidence such as console output or screenshots.
- Separate observed facts from residual risks and inference.
- Use `docs/VERIFICATION.md` for the full evidence contract.
