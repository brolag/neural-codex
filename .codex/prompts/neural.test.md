---
description: Run tests with smart detection and Ralph loop integration
argument-hint: [filter] [--watch] [--coverage]
---

You are running tests for the neural-codex workflow.

## Quick Commands

Run all tests:
```
/prompts:neural.test
```

Run specific tests:
```
/prompts:neural.test auth
```

Watch mode:
```
/prompts:neural.test --watch
```

## Test Detection

The test runner auto-detects your framework:
1. `TEST_CMD` environment variable (explicit)
2. `package.json` test script
3. Framework config files (pytest.ini, Cargo.toml, go.mod)
4. Fallback: npm test, pnpm test, pytest

## Ralph Loop Integration

Set TEST_CMD for the loop:
```bash
TEST_CMD="npm test -- --passWithNoTests" scripts/ralph-loop.sh 5
```

For targeted tests:
```bash
TEST_CMD="npm test -- auth.test.ts" scripts/ralph-loop.sh 3
```

## Diagnose Mode

When tests fail unexpectedly:
```
/prompts:neural.test diagnose
```

Checks:
- Missing dependencies
- Environment issues
- Stale caches
- Configuration problems

## Output Format

```
Test Results: 42 passed, 1 failed, 2 skipped

FAILED: src/auth/login.test.ts
  - "should validate email format"
  Suggested fix: Check email regex pattern
```

Outputs: Test results summary, failures with suggestions, next steps.
