#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PW="/root/.codex/skills/playwright/scripts/playwright_cli.sh"
PORT=$((20000 + $$ % 1000))
OUT_DIR="$ROOT_DIR/qa/final/alpha-inspection"
mkdir -p "$OUT_DIR"
cd "$ROOT_DIR"

python3 -m http.server "$PORT" --bind 127.0.0.1 > "$OUT_DIR/http-server.log" 2>&1 &
SERVER_PID=$!
cleanup(){ kill "$SERVER_PID" 2>/dev/null || true; }
trap cleanup EXIT

for viewer in viewer-a viewer-b; do
  for background in checker-light checker-dark; do
    session="hpe_alpha_${viewer}_${background}_$$"
    url="http://127.0.0.1:$PORT/qa/$viewer/index.html?model=../../model/HPE-DL360G10-2.5inch.glb&view=front&bg=$background"
    "$PW" -s="$session" open "$url" >/dev/null
    "$PW" -s="$session" resize 1200 800 >/dev/null
    ready=0
    for _attempt in 1 2 3 4 5 6 7 8 9 10; do
      snapshot="$("$PW" -s="$session" snapshot)"
      if [[ "$snapshot" == *"PASS · front ·"* && "$snapshot" == *"standard GLB"* ]]; then ready=1; break; fi
      sleep 0.4
    done
    if [[ "$ready" != 1 ]]; then echo "Alpha inspection render did not reach PASS: $viewer $background" >&2; exit 1; fi
    shot_output="$("$PW" -s="$session" screenshot)"
    shot_rel="$(printf '%s\n' "$shot_output" | sed -n 's/.*(\(\.playwright-cli\/[^)]*\.png\)).*/\1/p' | head -n 1)"
    test -n "$shot_rel" && test -s "$shot_rel"
    cp "$shot_rel" "$OUT_DIR/$viewer-front-$background.png"
    "$PW" -s="$session" close >/dev/null
    echo "PASS $viewer front $background"
  done
done
