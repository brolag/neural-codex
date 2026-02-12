---
name: test-runner
description: Run tests with smart detection, filtering, and Ralph loop integration. Use for automated testing in development and CI.
metadata:
  short-description: Smart test execution
  category: productivity
  source: neural-codex
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Test Runner

Run tests with auto-detection, filtering, and integration with the Ralph loop.

## When to Use
- Running tests after code changes
- Validating a specific feature or fix
- Integrating tests into the Ralph loop
- Debugging test failures

## Usage
```
$test-runner [--filter <pattern>] [--watch] [--coverage]
$test-runner targeted <file-or-pattern>
$test-runner diagnose
```

## Usage Examples
Run all tests:
```
$test-runner
```

Run tests for a specific file:
```
$test-runner targeted src/auth/**/*.test.ts
```

Watch mode:
```
$test-runner --watch
```

Debug failing tests:
```
$test-runner diagnose
```

## Auto-Detection
The skill detects the test framework from:
- `package.json` scripts (npm/pnpm/yarn)
- `pyproject.toml` or `pytest.ini` (pytest)
- `Cargo.toml` (cargo test)
- `go.mod` (go test)

### Detection Priority
1. `TEST_CMD` environment variable (explicit override)
2. `package.json` test script
3. Framework-specific config files
4. Fallback commands: `npm test`, `pnpm test`, `pytest`

## Ralph Loop Integration
Set `TEST_CMD` for the loop:
```bash
TEST_CMD="npm test -- --passWithNoTests" scripts/ralph-loop.sh 5
```

For targeted tests in the loop:
```bash
TEST_CMD="npm test -- auth.test.ts" scripts/ralph-loop.sh 3
```

## Output Parsing
The skill parses test output to:
- Count passed/failed/skipped tests
- Extract failure details and stack traces
- Suggest fixes for common errors

## Diagnose Mode
When tests fail unexpectedly:
```
$test-runner diagnose
```

This checks:
- Missing dependencies
- Environment issues
- Stale caches
- Configuration problems

## Output Format
```
Test Results: 42 passed, 1 failed, 2 skipped

FAILED: src/auth/login.test.ts
  - "should validate email format"
  Expected: true
  Received: false

Suggested fix: Check email regex pattern in validateEmail()
```

## Safety
- Never modify test files without explicit request
- Timeout tests after 5 minutes by default
- Warn before running tests that modify data
- Use `--dry-run` to preview test commands
