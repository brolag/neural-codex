# Reliability

## Testing
- Use `TEST_CMD` for loop runs and CI.
- Prefer targeted tests for small changes.
- For blocking hooks, test dangerous variants and a safe neighboring command.
- Smoke-test global and project installation in isolated temporary directories.

## Rollback
- Keep changes small and reversible.
- Document rollback steps in ExecPlans when risk is non-trivial.

## Circuit Breakers
- Stop automation on repeated failures.
- Log failure context in `plans/progress.jsonl`.
- Preserve recovery context through the `PreCompact` hook when available.
