#!/usr/bin/env bash
set -euo pipefail

PWCLI=${PWCLI:-/root/.codex/skills/playwright/scripts/playwright_cli.sh}
SESSION=${PW_SESSION:-r7525-qa}
BASE_URL=http://127.0.0.1:8792/qa/viewers
EVIDENCE_DIR=${EVIDENCE_DIR:-/root/Project/rack-device-3d/Dell-R7525-3.5inch/qa/webgl-evidence}
LOADS="$EVIDENCE_DIR/load-evidence.ndjson"
RUN_ID=$(date +%s%N)

mkdir -p "$EVIDENCE_DIR"

views=(front rear left right top bottom front-left front-right rear-left rear-right)
combinations=(
  "three standard three-standard"
  "three web three-web"
  "babylon standard babylon-standard"
  "babylon web babylon-web"
)

touch "$LOADS"
load_index=$(wc -l < "$LOADS")

for combination in "${combinations[@]}"; do
  read -r viewer variant output_dir <<< "$combination"
  mkdir -p "$EVIDENCE_DIR/$output_dir"

  for view in "${views[@]}"; do
    if jq -e --arg viewer "$viewer" --arg variant "$variant" --arg view "$view" \
      'select(.viewer == $viewer and .variant == $variant and .view == $view and .status == "PASS")' \
      "$LOADS" >/dev/null 2>&1 && [[ -s "$EVIDENCE_DIR/$output_dir/$view.png" ]]; then
      continue
    fi
    load_index=$((load_index + 1))
    url="$BASE_URL/$viewer.html?view=$view&variant=$variant&labels=1&load=$load_index&run=$RUN_ID"
    nav_log="$EVIDENCE_DIR/$output_dir/$view-navigation.txt"
    load_log="$EVIDENCE_DIR/$output_dir/$view-load.txt"
    screenshot="$EVIDENCE_DIR/$output_dir/$view.png"

    "$PWCLI" --session "$SESSION" goto "$url" > "$nav_log"
    "$PWCLI" --session "$SESSION" run-code \
      'async page => { await page.waitForFunction(() => window.__VIEWER_READY__ === true, null, {timeout: 30000}); return await page.evaluate(() => window.__VIEWER_INFO__); }' \
      > "$load_log"
    "$PWCLI" --session "$SESSION" screenshot --filename "$screenshot" > "$EVIDENCE_DIR/$output_dir/$view-screenshot.txt"

    if rg -q 'Console: [1-9][0-9]* errors' "$nav_log"; then
      echo "Browser console error during $viewer/$variant/$view" >&2
      exit 1
    fi

    info_json=$(sed -n '/^### Result$/{n;p;q;}' "$load_log")
    jq -e . >/dev/null <<< "$info_json"
    expected_file=Dell-R7525-3.5inch.glb
    if [[ "$variant" == web ]]; then expected_file=Dell-R7525-3.5inch-web.glb; fi
    jq -e --arg viewer "$viewer" --arg view "$view" --arg expected "$expected_file" \
      'def close($x;$y): (($x - $y) < 0.000001 and ($y - $x) < 0.000001);
       (.view == $view) and (.variant == $expected) and
       ((.engine | ascii_downcase) | contains($viewer)) and
       close(.bounds.min[0];-0.241) and close(.bounds.min[1];-0.0434) and close(.bounds.min[2];-0.38594) and
       close(.bounds.max[0];0.241) and close(.bounds.max[1];0.0434) and close(.bounds.max[2];0.38619)' \
      <<< "$info_json" >/dev/null

    screenshot_sha=$(sha256sum "$screenshot" | awk '{print $1}')
    jq -nc \
      --argjson load_index "$load_index" \
      --arg viewer "$viewer" \
      --arg variant "$variant" \
      --arg view "$view" \
      --arg url "$url" \
      --arg screenshot "qa/webgl-evidence/$output_dir/$view.png" \
      --arg screenshot_sha256 "$screenshot_sha" \
      --argjson viewer_info "$info_json" \
      '{load_index:$load_index,viewer:$viewer,variant:$variant,view:$view,url:$url,screenshot:$screenshot,screenshot_sha256:$screenshot_sha256,viewer_info:$viewer_info,status:"PASS"}' \
      >> "$LOADS"
  done
done

jq -s '{status:"PASS",required_loads:40,actual_loads:length,viewer_model_pairs:(group_by(.viewer + "-" + .variant) | map({pair:(.[0].viewer + "-" + .[0].variant),loads:length,views:map(.view)})),bounds_unique:(map(.viewer_info.bounds)|unique),records:.}' \
  "$LOADS" > "$EVIDENCE_DIR/load-evidence.json"
jq -e '.actual_loads >= .required_loads and (.viewer_model_pairs | all(.loads == 10)) and (.bounds_unique | length <= 2)' \
  "$EVIDENCE_DIR/load-evidence.json" >/dev/null

echo "PASS: 40 WebGL loads completed across two viewers, two GLBs, and ten views."
