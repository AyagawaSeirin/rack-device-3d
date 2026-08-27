#!/usr/bin/env bash
set -euo pipefail

task_root="/root/Project/rack-device-3d/Dell-R7515-3.5inch"
pwcli="/root/.codex/skills/playwright/scripts/playwright_cli.sh"
base="http://127.0.0.1:8791"
session_base="${PW_SESSION:-r7515-webgl-qa}"
views=(front rear left right top bottom front-left front-right rear-left rear-right front-logo rear-psu)

for viewer in three babylon; do
  for model in standard web; do
    output_dir="$task_root/qa/renders/$viewer/$model"
    mkdir -p "$output_dir"
    for view in "${views[@]}"; do
      if [[ -s "$output_dir/$view.png" ]]; then
        echo "SKIP $viewer $model $view"
        continue
      fi
      qa_id="${viewer}-${model}-${view}"
      session="${session_base}-${qa_id}"
      url="$base/qa/viewers/$viewer.html?model=$model&view=$view&qa=$qa_id"
      "$pwcli" --session "$session" open "$url" >/dev/null
      "$pwcli" --session "$session" run-code "async (page) => { await page.waitForFunction(() => window.__QA__?.status === 'PASS' && window.__QA__?.server?.ok === true, null, {timeout: 90000}); }" >/dev/null
      "$pwcli" --session "$session" screenshot --filename "$output_dir/$view.png" >/dev/null
      "$pwcli" --session "$session" close >/dev/null || true
      echo "PASS $viewer $model $view"
    done
  done
done
