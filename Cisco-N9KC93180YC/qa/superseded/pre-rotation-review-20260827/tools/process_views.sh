#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root_dir"

mkdir -p qa/intermediate views
for face in front rear left right top bottom; do
  if [[ ! -f "qa/intermediate/${face}-dekey-raw.png" ]]; then
    cp "views/${face}.png" "qa/intermediate/${face}-dekey-raw.png"
  fi
done

# Crop to the complete-appliance silhouette and enforce verified physical ratios.
# Front includes the 19-inch ears; rear has no ears.
convert qa/intermediate/front-dekey-raw.png -trim +repage -resize '2400x219!' \
  -region '1900x28+95+0' -blur '0x4' +region views/front.png
convert qa/intermediate/rear-dekey-raw.png  -trim +repage -resize '2200x221!' views/rear.png
convert qa/intermediate/left-dekey-raw.png  -trim +repage -resize '2600x200!' views/left.png
convert qa/intermediate/right-dekey-raw.png -trim +repage -resize '2600x200!' views/right.png

# Blur generated serial-like microtext while retaining the verified factory-label
# color block; recolor top-edge PE-blue pixels to verified PI burgundy.
convert qa/intermediate/top-dekey-raw.png -trim +repage \
  -fuzz 18% -fill '#8f3157' -opaque '#2450a0' \
  -resize '1760x2082!' \
  -region '250x180+130+730' -blur '0x4' +region \
  -region '300x470+130+890' -blur '0x2' +region views/top.png

convert qa/intermediate/bottom-dekey-raw.png -trim +repage -resize '1760x2082!' views/bottom.png

# The exact rear has no through-holes in the audit core. Preserve all RGB and
# silhouette-edge anti-aliasing while restoring accidental core alpha to 255.
python3 tools/repair_rear_core_alpha.py
