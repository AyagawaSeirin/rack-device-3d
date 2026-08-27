#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
keyed_dir="$root_dir/qa/work/keyed"
work_dir="$root_dir/qa/work/prepared"
views_dir="$root_dir/views"
mkdir -p "$work_dir" "$views_dir"

# Extend only feature-free metal/ear edge regions to restore the physical ratios.
# No identity-bearing component is stretched; the adjusted source extents already
# match the final resize ratios to within rounding error.
convert "$keyed_dir/front.png" -trim +repage \
  -background '#171a1c' -gravity center -extent 1493x133 \
  -resize 4000x356! -background none -gravity center -extent 4096x512 \
  "$views_dir/front.png"

convert "$keyed_dir/rear.png" -trim +repage \
  -background '#c4c6c5' -gravity center -extent 2079x205 \
  -resize 4000x394! -background none -gravity center -extent 4096x512 \
  "$views_dir/rear.png"

convert "$keyed_dir/left.png" -trim +repage \
  -crop 1415x87+0+0 +repage -trim +repage \
  -background '#c4c6c5' -gravity center -extent 1433x87 \
  -resize 4000x243! -background none -gravity center -extent 4096x512 \
  "$views_dir/left.png"

convert "$keyed_dir/right.png" -trim +repage \
  -crop 1425x111+58+0 +repage -trim +repage \
  -background '#c4c6c5' -gravity center -extent 1729x105 \
  -resize 4000x243! -background none -gravity center -extent 4096x512 \
  "$views_dir/right.png"

convert "$keyed_dir/top.png" -trim +repage \
  -crop 835x1427+40+0 +repage -trim +repage \
  -background '#c7cac9' -gravity center -extent 879x1427 \
  -resize 2463x4000! -background none -gravity center -extent 2560x4096 \
  "$views_dir/top.png"

convert "$keyed_dir/bottom.png" -trim +repage \
  -background '#c7cac9' -gravity center -extent 903x1466 \
  -resize 2463x4000! -background none -gravity center -extent 2560x4096 \
  "$views_dir/bottom.png"

for face in front rear left right top bottom; do
  convert "$views_dir/$face.png" -trim -format \
    "$face content=%wx%h ratio=%[fx:w/h] canvas=" info:
  identify -format '%wx%h channels=%[channels]\n' "$views_dir/$face.png"
done
