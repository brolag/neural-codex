# Reliability

## Testing
- Use `TEST_CMD` for loop runs and CI.
- Prefer targeted tests for small changes.

## Rollback
- Keep changes small and reversible.
- Document rollback steps in ExecPlans when risk is non-trivial.

## Circuit Breakers
- Stop automation on repeated failures.
- Log failure context in `plans/progress.jsonl`.
