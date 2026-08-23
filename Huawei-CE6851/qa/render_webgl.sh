#!/usr/bin/env bash
set -euo pipefail

MODEL_ROOT="/root/Project/rack-device-3d/Huawei-CE6851"
PWCLI_PATH="/root/.codex/skills/playwright/scripts/playwright_cli.sh"
BASE_URL="http://127.0.0.1:8765"

core_views=(front rear left right top bottom front_left front_right rear_left rear_right)
detail_views=(front_ear_left front_ear_right front_logo rear_management)
if [[ -n "${RENDER_VIEWS:-}" ]]; then
  read -r -a core_views <<< "$RENDER_VIEWS"
fi

capture_set() {
  local engine="$1"
  local profile="$2"
  local viewer="$3"
  local model="$4"
  local session="ce6851-${engine}-${profile}"
  local work_dir="${MODEL_ROOT}/output/playwright/${engine}/${profile}"
  local qa_dir="${MODEL_ROOT}/qa/renders/${engine}/${profile}"
  local view

  mkdir -p "$work_dir" "$qa_dir"
  cd "$work_dir"

  "$PWCLI_PATH" --session "$session" open "${BASE_URL}/qa/viewers/${viewer}.html?model=../../model/${model}&view=${core_views[0]}&bg=light"
  "$PWCLI_PATH" --session "$session" resize 1280 720

  for view in "${core_views[@]}"; do
    "$PWCLI_PATH" --session "$session" run-code "async (page) => { await page.goto('${BASE_URL}/qa/viewers/${viewer}.html?model=../../model/${model}&view=${view}&bg=light'); await page.waitForFunction(() => window.__viewerReady === true); await page.waitForTimeout(250); await page.screenshot({path: '${view}.png', scale: 'css', type: 'png'}); }"
    cp "$work_dir/${view}.png" "$qa_dir/${view}.png"
  done

  if [[ "$profile" == "standard" && -z "${RENDER_VIEWS:-}" ]]; then
    for view in "${detail_views[@]}"; do
      "$PWCLI_PATH" --session "$session" run-code "async (page) => { await page.goto('${BASE_URL}/qa/viewers/${viewer}.html?model=../../model/${model}&view=${view}&bg=light'); await page.waitForFunction(() => window.__viewerReady === true); await page.waitForTimeout(250); await page.screenshot({path: '${view}.png', scale: 'css', type: 'png'}); }"
      cp "$work_dir/${view}.png" "$qa_dir/${view}.png"
    done

    "$PWCLI_PATH" --session "$session" run-code "async (page) => { await page.goto('${BASE_URL}/qa/viewers/${viewer}.html?model=../../model/${model}&view=front&bg=checker-light'); await page.waitForFunction(() => window.__viewerReady === true); await page.waitForTimeout(250); await page.screenshot({path: 'front-checker-light.png', scale: 'css', type: 'png'}); }"
    cp "$work_dir/front-checker-light.png" "$qa_dir/front-checker-light.png"

    "$PWCLI_PATH" --session "$session" run-code "async (page) => { await page.goto('${BASE_URL}/qa/viewers/${viewer}.html?model=../../model/${model}&view=rear&bg=checker-dark'); await page.waitForFunction(() => window.__viewerReady === true); await page.waitForTimeout(250); await page.screenshot({path: 'rear-checker-dark.png', scale: 'css', type: 'png'}); }"
    cp "$work_dir/rear-checker-dark.png" "$qa_dir/rear-checker-dark.png"
  fi

  "$PWCLI_PATH" --session "$session" close
}

case "${1:-all}" in
  all)
    capture_set threejs standard threejs Huawei-CE6851.glb
    capture_set threejs web threejs Huawei-CE6851-web.glb
    capture_set babylonjs standard babylonjs Huawei-CE6851.glb
    capture_set babylonjs web babylonjs Huawei-CE6851-web.glb
    ;;
  threejs)
    capture_set threejs standard threejs Huawei-CE6851.glb
    capture_set threejs web threejs Huawei-CE6851-web.glb
    ;;
  babylonjs)
    capture_set babylonjs standard babylonjs Huawei-CE6851.glb
    capture_set babylonjs web babylonjs Huawei-CE6851-web.glb
    ;;
  *)
    echo "usage: $0 [all|threejs|babylonjs]" >&2
    exit 2
    ;;
esac
