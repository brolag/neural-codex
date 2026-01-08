#!/usr/bin/env bash
set -euo pipefail

# Ralph loop for Codex: picks one task, runs Codex, runs tests, updates PRD atomically.
# Requirements: bash, jq, flock, git, timeout, Codex CLI available as `codex`.

LOCK_FILE="/tmp/ralph-loop.lock"
PRD_PATH="${PRD_PATH:-plans/prd.json}"
PROGRESS_PATH="${PROGRESS_PATH:-plans/progress.jsonl}"
MAX_ITERS="${1:-}"
FULL_EVERY="${FULL_EVERY:-5}"          # Run full test suite every N iterations
CODEx_TIMEOUT="${CODEX_TIMEOUT:-900}"  # Seconds
TEST_TIMEOUT="${TEST_TIMEOUT:-300}"    # Seconds
TEST_CMD="${TEST_CMD:-}"               # e.g., "npm test" or "pnpm test"
FALLBACK_TESTS=("npm test" "npm run test" "pnpm test" "pytest")

if [[ -z "${MAX_ITERS}" ]]; then
  echo "Usage: $0 <max-iterations>"
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required."
  exit 1
fi

exec 9>"${LOCK_FILE}"
if ! flock -n 9; then
  echo "Another Ralph loop is running (lock: ${LOCK_FILE})."
  exit 1
fi

timestamp() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

log_progress() {
  local iteration="$1" task="$2" status="$3" message="$4"
  printf '{"ts":"%s","iteration":%s,"task":"%s","status":"%s","message":"%s"}\n' \
    "$(timestamp)" "$iteration" "$task" "$status" "$message" >> "${PROGRESS_PATH}"
}

read_max_attempts() {
  jq -r '.max_attempts // 3' "${PRD_PATH}"
}

# Selects first eligible task: not passed, not needs_human, attempts < max_attempts, dependencies passed.
select_task() {
  local max_attempts="$1"
  jq -r --argjson max_attempts "${max_attempts}" '
    .items as $all
    | $all
    | map(select(.passes == false and (.status != "needs_human") and (.attempts // 0) < $max_attempts))
    | map(select((.depends_on // []) | all(. as $d | ($all | any(.id == $d and .passes == true)))))
    | .[0].id // empty
  ' "${PRD_PATH}"
}

mark_in_progress() {
  local task_id="$1"
  local tmp="${PRD_PATH}.tmp"
  jq --arg id "$task_id" '
    .items |= map(if .id == $id then .in_progress = true | .status = "in_progress" | .attempts = ((.attempts // 0)+1) else . end)
  ' "${PRD_PATH}" > "${tmp}"
  mv "${tmp}" "${PRD_PATH}"
}

mark_result() {
  local task_id="$1" result="$2" max_attempts="$3" note="$4"
  local tmp="${PRD_PATH}.tmp"
  if [[ "${result}" == "pass" ]]; then
    jq --arg id "$task_id" --arg note "$note" '
      .items |= map(if .id == $id then .passes = true | .status = "done" | .in_progress = false | .notes = $note else . end)
    ' "${PRD_PATH}" > "${tmp}"
  else
    jq --arg id "$task_id" --arg note "$note" --argjson max_attempts "$max_attempts" '
      .items |= map(if .id == $id then
        (if (.attempts // 0) >= $max_attempts then .status = "needs_human" else .status = "todo" end)
        | .in_progress = false
        | .notes = $note
      else . end)
    ' "${PRD_PATH}" > "${tmp}"
  fi
  mv "${tmp}" "${PRD_PATH}"
}

all_passed() {
  jq -e '.items | all(.passes == true)' "${PRD_PATH}" >/dev/null 2>&1
}

run_codex() {
  local task_id="$1"
  local codex_prompt
  codex_prompt=$(cat <<'EOF'
You are an expert engineer running a Ralph loop iteration.
Rules:
- Pick ONLY the claimed task (already locked by script).
- Do NOT edit plans/prd.json.
- Implement the feature/fix for that task only.
- Keep changes minimal and safe; avoid touching unrelated files.
- Add/adjust tests for this task.
- When done, print a brief summary and suggested targeted test command (if any), e.g., TEST: npm test -- file.spec.ts
EOF
)
  timeout "${CODEx_TIMEOUT}" codex -p "${codex_prompt}" || return 1
}

run_tests() {
  local iter="$1"
  local task_id="$2"
  local suggested_cmd
  suggested_cmd="$(git diff --unified=0 | grep -oE 'TEST:.*' || true)"

  set +e
  local ok=1

  run_with_timeout() {
    local cmd="$1"
    timeout "${TEST_TIMEOUT}" bash -lc "${cmd}"
  }

  if [[ -n "${TEST_CMD}" ]]; then
    run_with_timeout "${TEST_CMD}"
    ok=$?
  else
    for cmd in "${FALLBACK_TESTS[@]}"; do
      if run_with_timeout "${cmd}"; then
        ok=0
        break
      fi
    done
  fi

  # Optional targeted run from Codex suggestion
  if [[ -n "${suggested_cmd}" ]]; then
    run_with_timeout "${suggested_cmd/TEST: /}" || true
  fi

  # Periodic full run
  if (( iter % FULL_EVERY == 0 )); then
    if [[ -n "${TEST_CMD}" ]]; then
      run_with_timeout "${TEST_CMD}" || ok=$?
    else
      for cmd in "${FALLBACK_TESTS[@]}"; do
        if run_with_timeout "${cmd}"; then
          ok=0
          break
        fi
      done
    fi
  fi

  set -e
  return "${ok}"
}

git_clean_reset() {
  git reset --hard HEAD >/dev/null 2>&1 || true
  git clean -fd >/dev/null 2>&1 || true
}

git_commit() {
  local task_id="$1"
  if git diff --quiet && git diff --cached --quiet; then
    return
  fi
  git add -A
  git commit -m "Ralph: ${task_id}" >/dev/null 2>&1 || true
}

main() {
  local max_attempts
  max_attempts="$(read_max_attempts)"

  for iter in $(seq 1 "${MAX_ITERS}"); do
    if all_passed; then
      echo "All tasks complete."
      log_progress "${iter}" "all" "done" "All passes=true"
      exit 0
    fi

    local task_id
    task_id="$(select_task "${max_attempts}")"
    if [[ -z "${task_id}" ]]; then
      echo "No eligible tasks (all done or blocked)."
      log_progress "${iter}" "none" "blocked" "No eligible tasks"
      exit 0
    fi

    echo "== Iteration ${iter}/${MAX_ITERS} :: ${task_id} =="

    mark_in_progress "${task_id}"
    log_progress "${iter}" "${task_id}" "start" "Claimed task"

    if ! run_codex "${task_id}"; then
      log_progress "${iter}" "${task_id}" "error" "Codex failed/timed out"
      git_clean_reset
      mark_result "${task_id}" "fail" "${max_attempts}" "Codex failed"
      continue
    fi

    if run_tests "${iter}" "${task_id}"; then
      log_progress "${iter}" "${task_id}" "green" "Tests passed"
      git_commit "${task_id}"
      mark_result "${task_id}" "pass" "${max_attempts}" "Tests passed"
    else
      log_progress "${iter}" "${task_id}" "red" "Tests failed"
      git_clean_reset
      mark_result "${task_id}" "fail" "${max_attempts}" "Tests failed"
    fi
  done

  echo "Reached max iterations (${MAX_ITERS}) without completing."
  log_progress "${MAX_ITERS}" "all" "stopped" "Max iterations"
  exit 2
}

main "$@"
