#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root_dir"
mkdir -p qa/webgl-loads/{three,babylon}/{standard,web}

session="cisco-n9kc9336-final"
pwcli="/root/.codex/skills/playwright/scripts/playwright_cli.sh"
"$pwcli" -s="$session" open "http://127.0.0.1:8936/qa/viewers/three-viewer.html?model=standard&view=front&run=bootstrap"
"$pwcli" -s="$session" resize 1280 900
capture_code=""
IFS= read -r -d '' capture_code < qa/viewers/capture-function.js || true
"$pwcli" -s="$session" run-code "$capture_code"
"$pwcli" -s="$session" close
