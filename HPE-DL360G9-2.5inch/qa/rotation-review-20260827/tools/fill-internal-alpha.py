#!/usr/bin/env python3
"""Make internal chassis pixels opaque while preserving border-connected exterior alpha."""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--threshold", type=int, default=250)
    parser.add_argument("--opaque-core", action="store_true", help="also force the audit-defined 8% inset chassis core opaque")
    args = parser.parse_args()
    image = Image.open(args.source).convert("RGBA")
    rgba = np.asarray(image).copy()
    low = rgba[:, :, 3] < args.threshold
    height, width = low.shape
    exterior = np.zeros_like(low, dtype=bool)
    queue = deque()
    for x in range(width):
        if low[0, x]: queue.append((0, x))
        if low[height - 1, x]: queue.append((height - 1, x))
    for y in range(height):
        if low[y, 0]: queue.append((y, 0))
        if low[y, width - 1]: queue.append((y, width - 1))
    while queue:
        y, x = queue.popleft()
        if exterior[y, x] or not low[y, x]:
            continue
        exterior[y, x] = True
        if y: queue.append((y - 1, x))
        if y + 1 < height: queue.append((y + 1, x))
        if x: queue.append((y, x - 1))
        if x + 1 < width: queue.append((y, x + 1))
    internal = low & ~exterior
    rgba[internal, 3] = 255
    core_pixels = 0
    if args.opaque_core:
        content = rgba[:, :, 3] >= 8
        ys, xs = np.where(content)
        if len(xs):
            left, right = int(xs.min()), int(xs.max()) + 1
            top, bottom = int(ys.min()), int(ys.max()) + 1
            inset_x = max(1, round((right - left) * 0.08))
            inset_y = max(1, round((bottom - top) * 0.08))
            core = rgba[top + inset_y:bottom - inset_y, left + inset_x:right - inset_x, 3]
            core_pixels = int(np.sum(core < 255))
            core[:] = 255
    args.output.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba, "RGBA").save(args.output, optimize=True)
    print(f"{args.source}: internal_alpha_pixels_filled={int(np.sum(internal))} opaque_core_pixels_filled={core_pixels} exterior_alpha_pixels_preserved={int(np.sum(exterior))}")


if __name__ == "__main__":
    main()
