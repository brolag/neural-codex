# Exec Plans (PLANS)

Use ExecPlans for multi-hour tasks. Keep the plan concrete and update after each checkpoint.

## Template
```
# ExecPlan: <title>

## Objective
- <single sentence outcome>

## Scope
- In scope:
- Out of scope:

## Acceptance Contract
- Scenario:
  - Given:
  - When:
  - Then:
- Validation command:
- Behavioral backend: CLI | browser | desktop
- Rollback:

## Approach
1. <step>
2. <step>

## Risks
- <risk + mitigation>

## Checkpoints
- [ ] <checkpoint + verification>

## Test/Verify
- <command or explicit manual check>

## Evidence
- <test output, console log, screenshot, or artifact path>
- Residual risks:

## Notes
- <ongoing log>
```

## Where to store
- Active: `docs/exec-plans/active/`
- Completed: `docs/exec-plans/completed/`
