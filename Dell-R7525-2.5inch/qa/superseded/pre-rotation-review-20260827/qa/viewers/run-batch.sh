#!/usr/bin/env bash
set -euo pipefail

start="${1:?start index required}"
count="${2:-2}"
root="/root/Project/rack-device-3d/Dell-R7525-2.5inch"
pw="/root/.codex/skills/playwright/scripts/playwright_cli.sh"

cd "$root"
python3 -m http.server 8787 --bind 127.0.0.1 >qa/viewers/http-server.log 2>&1 &
server_pid=$!
trap 'kill "$server_pid" 2>/dev/null || true' EXIT

for _ in 1 2 3 4 5; do
  if curl -fsS -o /dev/null http://127.0.0.1:8787/qa/viewers/control.html; then break; fi
  sleep 0.2
done

"$pw" --session r7525bottom run-code "async (page)=>{await page.goto('http://127.0.0.1:8787/qa/viewers/control.html?start=${start}&count=${count}')}"
"$pw" --session r7525bottom run-code --filename qa/viewers/capture-matrix.js
