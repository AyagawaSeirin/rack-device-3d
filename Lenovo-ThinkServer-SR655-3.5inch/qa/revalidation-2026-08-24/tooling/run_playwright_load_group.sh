#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 3 ]]; then
  echo "usage: $0 <three|babylon> <standard|web> <sha256>" >&2
  exit 2
fi

loader="$1"
model="$2"
sha256="$3"

case "$loader" in
  three|babylon) ;;
  *) echo "unsupported loader: $loader" >&2; exit 2 ;;
esac

case "$model" in
  standard|web) ;;
  *) echo "unsupported model: $model" >&2; exit 2 ;;
esac

if [[ ! "$sha256" =~ ^[0-9a-f]{64}$ ]]; then
  echo "invalid SHA-256: $sha256" >&2
  exit 2
fi

pwcli="/root/.codex/skills/playwright/scripts/playwright_cli.sh"
session="sr655-rv-${loader}-${model}"
viewer="${loader}-viewer.html"
base_url="http://127.0.0.1:8890/qa/revalidation-2026-08-24/viewers/${viewer}"
output_dir="renders/${loader}-${model}"
views=(front rear right left top bottom frontRight frontLeft rearRight rearLeft)

mkdir -p "$output_dir"

for index in "${!views[@]}"; do
  view="${views[$index]}"
  ordinal=$(printf '%02d' "$((index + 1))")
  run_id="RV-${loader}-${model}-${ordinal}"
  url="${base_url}?model=${model}&view=${view}&run=${run_id}&sha=${sha256}"
  if [[ "$index" -eq 0 ]]; then
    "$pwcli" --session "$session" open "$url"
    "$pwcli" --session "$session" resize 1200 800
  else
    "$pwcli" --session "$session" goto "$url"
  fi
  "$pwcli" --session "$session" run-code "async page => { await page.waitForFunction(() => document.body.dataset.ready === '1' || document.body.dataset.error, null, { timeout: 120000 }); }"
  "$pwcli" --session "$session" eval "() => { if (document.body.dataset.error) throw new Error(document.body.dataset.error); if (document.body.dataset.ready !== '1') throw new Error('viewer did not reach ready state'); return {title:document.title,dataset:{...document.body.dataset}}; }"
  "$pwcli" --session "$session" screenshot --filename "$output_dir/${ordinal}-${view}.png"
done

"$pwcli" --session "$session" close
