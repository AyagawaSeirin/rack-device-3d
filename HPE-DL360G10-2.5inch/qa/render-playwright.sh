#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PW="/root/.codex/skills/playwright/scripts/playwright_cli.sh"
SESSION="hpe_final_render"
BASE_URL="http://127.0.0.1:18999"
VIEWS=(front rear left right top bottom front-left front-right rear-left rear-right)

cd "$ROOT_DIR"
mkdir -p qa/final/webgl-renders

SERVER_PID=""
if ! curl -sS -o /dev/null "$BASE_URL/qa/viewer-a/index.html"; then
  python3 -m http.server 18999 --bind 127.0.0.1 > qa/final/http-server.log 2>&1 &
  SERVER_PID=$!
fi
cleanup() {
  if [[ -n "$SERVER_PID" ]]; then
    kill "$SERVER_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT

"$PW" -s="$SESSION" open "$BASE_URL/qa/viewer-a/index.html" >/dev/null
"$PW" -s="$SESSION" resize 1200 800 >/dev/null

for viewer in viewer-a viewer-b; do
  for tier in standard web; do
    if [[ "$tier" == "web" ]]; then
      model="HPE-DL360G10-2.5inch-web.glb"
    else
      model="HPE-DL360G10-2.5inch.glb"
    fi
    out_dir="qa/final/webgl-renders/$viewer/$tier"
    mkdir -p "$out_dir"
    for view in "${VIEWS[@]}"; do
      if [[ -s "$out_dir/$view.png" && "$out_dir/$view.png" -nt "model/$model" ]]; then
        echo "SKIP current $viewer $tier $view"
        continue
      fi
      url="$BASE_URL/qa/$viewer/index.html?model=../../model/$model&view=$view&bg=light"
      "$PW" -s="$SESSION" goto "$url" >/dev/null
      ready=0
      for _attempt in 1 2 3 4 5 6 7 8 9 10; do
        snapshot="$($PW -s="$SESSION" snapshot)"
        if [[ "$snapshot" == *"PASS · $view ·"* && "$snapshot" == *"$tier GLB"* ]]; then
          ready=1
          break
        fi
        sleep 0.5
      done
      if [[ "$ready" != 1 ]]; then
        echo "Playwright render did not reach PASS: $viewer $tier $view" >&2
        exit 1
      fi
      shot_output="$($PW -s="$SESSION" screenshot)"
      shot_rel="$(printf '%s\n' "$shot_output" | sed -n 's/.*(\(\.playwright-cli\/[^)]*\.png\)).*/\1/p' | head -n 1)"
      if [[ -z "$shot_rel" || ! -s "$shot_rel" ]]; then
        echo "Playwright screenshot missing: $viewer $tier $view" >&2
        exit 1
      fi
      cp "$shot_rel" "$out_dir/$view.png"
      echo "PASS $viewer $tier $view"
    done
  done
done

"$PW" -s="$SESSION" close >/dev/null
