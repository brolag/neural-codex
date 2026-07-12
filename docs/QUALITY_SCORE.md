# Quality Score

## Rubric
- **Correctness**: Behavior matches docs and tests.
- **Observability**: Progress is logged to repo files.
- **Safety**: No hidden state or unreviewed automation.
- **Maintainability**: Changes are documented and linked.
- **Behavior**: A real user flow matches the acceptance scenario.
- **Evidence**: Claims link to raw command output, logs, screenshots, or artifacts.

## Gates
- Tests pass or explicit justification for skip.
- User-facing changes pass the relevant CLI/browser/desktop exercise.
- Security-sensitive or pre-merge changes receive an independent review.
- AGENTS.md updated when new docs are added.
- No orphaned docs or dead links.
