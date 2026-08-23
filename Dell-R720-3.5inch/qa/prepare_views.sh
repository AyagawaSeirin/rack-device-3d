#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
stage="$root/qa/imagegen-staging"
views="$root/views"
mkdir -p "$views"

# Selected source-locked generations are never stretched.  Small crop/edge
# extensions reconcile the generated alpha bounds to the verified physical
# ratios while preserving all identity-bearing pixels.
convert "$stage/front-alpha.png" -trim +repage -gravity center \
  -crop 1824x330+0+0 +repage -resize 3072x "$views/front.png"

convert "$stage/rear-v2-alpha.png" -trim +repage -gravity center \
  -crop 1846x363+0+0 +repage -resize 3072x "$views/rear.png"

convert "$stage/left-alpha.png" -trim +repage -bordercolor '#c5c7c5' \
  -border 0x5 -resize 3072x "$views/left.png"

# The v2 right-side correction retained an unsupported cable-like fragment.
# Keep the earlier independent source-locked generation, whose plain shell is
# factual, and crop only its small projection distortion to the body ratio.
convert "$stage/right-alpha.png" -trim +repage -gravity center \
  -crop 1707x212+0+0 +repage -resize 3072x "$views/right.png"

convert "$stage/top-alpha.png" -trim +repage -bordercolor '#d0d1cf' \
  -border 22x0 -resize x3072 "$views/top.png"

convert "$stage/bottom-v2-alpha.png" -trim +repage -bordercolor '#aeb0ae' \
  -border 15x0 -resize x3072 "$views/bottom.png"
