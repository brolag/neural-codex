#!/usr/bin/env bash
# Template: send Codex notify events to Telegram.
# Requirements: curl; env TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

set -euo pipefail

if [[ -z "${TELEGRAM_BOT_TOKEN:-}" || -z "${TELEGRAM_CHAT_ID:-}" ]]; then
  echo "Telegram env vars not set; skipping." >&2
  exit 0
fi

payload="$(cat)"
event="$(echo "$payload" | jq -r '.event // "unknown"')"
msg="Codex event: ${event}"

curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d chat_id="${TELEGRAM_CHAT_ID}" \
  -d text="${msg}" >/dev/null 2>&1 || true
