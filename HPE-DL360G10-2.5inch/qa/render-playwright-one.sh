#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PW="/root/.codex/skills/playwright/scripts/playwright_cli.sh"
VIEWER="${1:?viewer-a or viewer-b}"
TIER="${2:?standard or web}"
VIEW="${3:?view name}"
SESSION="hpe_one_${VIEWER}_${TIER}_${VIEW}_$$"
PORT=$((19000 + $$ % 1000))

if [[ "$TIER" == "web" ]]; then
  MODEL="HPE-DL360G10-2.5inch-web.glb"
else
  MODEL="HPE-DL360G10-2.5inch.glb"
fi

OUT_DIR="$ROOT_DIR/qa/renders/$VIEWER/$TIER"
mkdir -p "$OUT_DIR"
cd "$ROOT_DIR"

python3 -m http.server "$PORT" --bind 127.0.0.1 > "qa/$VIEWER/http-$TIER-$VIEW.log" 2>&1 &
SERVER_PID=$!
cleanup() {
  kill "$SERVER_PID" 2>/dev/null || true
}
trap cleanup EXIT

URL="http://127.0.0.1:$PORT/qa/$VIEWER/index.html?model=../../model/$MODEL&view=$VIEW&bg=light"
"$PW" -s="$SESSION" open "$URL" >/dev/null
"$PW" -s="$SESSION" resize 1200 800 >/dev/null

READY=0
for _attempt in 1 2 3 4 5 6 7 8 9 10; do
  SNAPSHOT="$("$PW" -s="$SESSION" snapshot)"
  if [[ "$SNAPSHOT" == *"PASS · $VIEW ·"* && "$SNAPSHOT" == *"$TIER GLB"* ]]; then
    READY=1
    break
  fi
  sleep 0.4
done
if [[ "$READY" != 1 ]]; then
  echo "Playwright render did not reach PASS: $VIEWER $TIER $VIEW" >&2
  exit 1
fi

SHOT_OUTPUT="$("$PW" -s="$SESSION" screenshot)"
SHOT_REL="$(printf '%s\n' "$SHOT_OUTPUT" | sed -n 's/.*(\(\.playwright-cli\/[^)]*\.png\)).*/\1/p' | head -n 1)"
if [[ -z "$SHOT_REL" || ! -s "$SHOT_REL" ]]; then
  echo "Playwright screenshot missing: $VIEWER $TIER $VIEW" >&2
  exit 1
fi
cp "$SHOT_REL" "$OUT_DIR/$VIEW.png"
"$PW" -s="$SESSION" close >/dev/null
echo "PASS $VIEWER $TIER $VIEW"
