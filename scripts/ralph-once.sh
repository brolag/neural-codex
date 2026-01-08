#!/usr/bin/env bash
set -euo pipefail

PRD_PATH="${PRD_PATH:-plans/prd.json}"
echo "Running one interactive Ralph iteration (no loop)."
echo "Inspect ${PRD_PATH}, pick a single ready task, implement, run tests, and commit."

codex -p "$(cat <<'EOF'
You are running a single Ralph iteration manually.
Rules:
- Pick ONE eligible task from plans/prd.json (passes=false, not needs_human, deps satisfied).
- Do NOT edit plans/prd.json directly.
- Implement only that task; keep changes small.
- Add/adjust tests; run the project test command.
- If tests pass, summarize changes and suggest commit message.
- If tests fail, summarize failure and suggest fix.
EOF
)"
