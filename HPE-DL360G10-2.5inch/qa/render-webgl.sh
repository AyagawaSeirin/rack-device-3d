#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VIEWER="${1:?viewer-a or viewer-b}"
TIER="${2:?standard or web}"
shift 2

if [[ "$TIER" == "web" ]]; then
  MODEL_NAME="HPE-DL360G10-2.5inch-web.glb"
else
  MODEL_NAME="HPE-DL360G10-2.5inch.glb"
fi

OUT_DIR="$ROOT_DIR/qa/renders/$VIEWER/$TIER"
mkdir -p "$OUT_DIR"

for VIEW in "$@"; do
  URL="file://$ROOT_DIR/qa/$VIEWER/index.html?model=../../model/$MODEL_NAME&view=$VIEW&bg=light"
  PROFILE_DIR="$(mktemp -d)"
  SHOT="$OUT_DIR/$VIEW.png"
  SHOT_TMP="$OUT_DIR/.${VIEW}.$$.png"
  set +e
  timeout 20s google-chrome \
    --headless=new --no-sandbox --disable-dev-shm-usage \
    --disable-background-networking --disable-sync --no-first-run \
    --disable-default-apps --metrics-recording-only \
    --user-data-dir="$PROFILE_DIR" \
    --allow-file-access-from-files --disable-web-security \
    --use-gl=angle --use-angle=swiftshader --enable-webgl --enable-unsafe-swiftshader --ignore-gpu-blocklist \
    --window-size=1200,800 --virtual-time-budget=9000 \
    --run-all-compositor-stages-before-draw \
    --screenshot="$SHOT_TMP" "$URL" \
    >"$ROOT_DIR/qa/$VIEWER/chrome-$TIER-$VIEW.log" 2>&1
  CHROME_STATUS=$?
  set -e
  rm -rf "$PROFILE_DIR"
  if [[ ! -s "$SHOT_TMP" ]]; then
    echo "render failed: viewer=$VIEWER tier=$TIER view=$VIEW chrome_status=$CHROME_STATUS" >&2
    exit 1
  fi
  mv -f "$SHOT_TMP" "$SHOT"
done
