#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 4 ]]; then
  echo "usage: $0 <three|babylon> <standard|web> <sha256> <first-run-number>" >&2
  exit 2
fi

audit_engine="$1"
audit_variant="$2"
audit_expected="$3"
audit_first_run="$4"
audit_root="/root/Project/rack-device-3d/Huawei-RH1288V5-3.5inch/qa/revalidation-2026-08-24"
audit_pw="/root/.codex/skills/playwright/scripts/playwright_cli.sh"
audit_session="rh1288v5-revalidation"
audit_views=(front rear left right top bottom frontLeft frontRight rearLeft rearRight)

mkdir -p "$audit_root/loads/$audit_engine/$audit_variant" "$audit_root/loads/events" "$audit_root/logs/load-cli"

for audit_index in "${!audit_views[@]}"; do
  audit_view="${audit_views[$audit_index]}"
  audit_run=$((audit_first_run + audit_index))
  audit_page="http://127.0.0.1:8129/qa/revalidation-2026-08-24/viewers/${audit_engine}.html?model=${audit_variant}&view=${audit_view}&expected=${audit_expected}&run=${audit_run}"
  "$audit_pw" -s="$audit_session" goto "$audit_page" > "$audit_root/logs/load-cli/$(printf '%02d' "$audit_run")-goto.txt"

  audit_ready=""
  for audit_attempt in $(seq 1 45); do
    audit_ready=$("$audit_pw" --raw -s="$audit_session" eval "() => document.body.dataset.ready || (document.body.dataset.error ? 'ERROR:' + document.body.dataset.error : '')" 2>/dev/null | tr -d '"\r\n')
    if [[ "$audit_ready" == "1" ]]; then
      break
    fi
    if [[ "$audit_ready" == ERROR:* ]]; then
      echo "load $audit_run failed: $audit_ready" >&2
      exit 1
    fi
    sleep 1
  done
  if [[ "$audit_ready" != "1" ]]; then
    echo "load $audit_run timed out" >&2
    exit 1
  fi

  "$audit_pw" --raw -s="$audit_session" eval "() => window.__loadEvidence" > "$audit_root/loads/events/$(printf '%02d' "$audit_run").json"
  "$audit_pw" -s="$audit_session" screenshot --filename="$audit_root/loads/$audit_engine/$audit_variant/$(printf '%02d' "$audit_run")-${audit_view}.png" > "$audit_root/logs/load-cli/$(printf '%02d' "$audit_run")-screenshot.txt"
  printf 'PASS run=%02d engine=%s model=%s view=%s sha256=%s\n' "$audit_run" "$audit_engine" "$audit_variant" "$audit_view" "$audit_expected"
done
