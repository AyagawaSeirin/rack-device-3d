#!/usr/bin/env python3
"""Finalize six imagegen chroma-key outputs as ratio-locked transparent PNGs."""

from __future__ import annotations

from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
KEYED = ROOT / "qa" / "imagegen-keyed"
VIEWS = ROOT / "views"

PHYSICAL = {
    "front": (482.6, 43.0, 3600),
    "rear": (436.0, 43.0, 3600),
    "left": (708.0, 43.0, 3600),
    "right": (708.0, 43.0, 3600),
    "top": (436.0, 708.0, 3000),
    "bottom": (436.0, 708.0, 3000),
}


def fill_enclosed_holes(mask: np.ndarray) -> np.ndarray:
    """Fill transparent islands without filling notches connected to the canvas edge."""
    h, w = mask.shape
    outside = np.zeros((h, w), dtype=bool)
    queue: deque[tuple[int, int]] = deque()
    for x in range(w):
        if not mask[0, x]:
            queue.append((0, x))
        if not mask[h - 1, x]:
            queue.append((h - 1, x))
    for y in range(h):
        if not mask[y, 0]:
            queue.append((y, 0))
        if not mask[y, w - 1]:
            queue.append((y, w - 1))
    while queue:
        y, x = queue.popleft()
        if outside[y, x] or mask[y, x]:
            continue
        outside[y, x] = True
        if y:
            queue.append((y - 1, x))
        if y + 1 < h:
            queue.append((y + 1, x))
        if x:
            queue.append((y, x - 1))
        if x + 1 < w:
            queue.append((y, x + 1))
    return mask | (~mask & ~outside)


def finalize(face: str) -> None:
    image = Image.open(KEYED / f"{face}.png").convert("RGBA")
    array = np.asarray(image).copy()
    alpha = array[..., 3]
    binary = alpha >= 128

    # Front-ear holes are the only verified transparent islands. Every other
    # face is opaque, so close any chroma reflection accidentally removed.
    if face != "front":
        binary = fill_enclosed_holes(binary)
    if face in {"left", "right"}:
        # The published 436 x 43 x 708 mm body has a rectangular side
        # silhouette.  Chroma spill around stamped relief must not punch
        # transparent channels through that opaque sheet-metal panel.
        ys, xs = np.nonzero(binary)
        binary[ys.min() : ys.max() + 1, xs.min() : xs.max() + 1] = True
    array[..., 3] = np.where(binary, 255, 0).astype(np.uint8)
    array[~binary, :3] = 0
    image = Image.fromarray(array, "RGBA")

    bbox = image.getchannel("A").getbbox()
    if not bbox:
        raise RuntimeError(f"{face}: empty alpha mask")
    crop = image.crop(bbox)

    physical_w, physical_h, long_edge = PHYSICAL[face]
    ratio = physical_w / physical_h
    if ratio >= 1:
        content_w = long_edge
        content_h = round(long_edge / ratio)
    else:
        content_h = long_edge
        content_w = round(long_edge * ratio)
    crop = crop.resize((content_w, content_h), Image.Resampling.LANCZOS)

    margin = 24
    canvas = Image.new("RGBA", (content_w + 2 * margin, content_h + 2 * margin), (0, 0, 0, 0))
    canvas.alpha_composite(crop, (margin, margin))
    VIEWS.mkdir(parents=True, exist_ok=True)
    canvas.save(VIEWS / f"{face}.png", optimize=True)
    print(f"{face}: source_bbox={bbox} content={content_w}x{content_h} canvas={canvas.size}")


def main() -> None:
    for face in ("front", "rear", "left", "right", "top", "bottom"):
        finalize(face)


if __name__ == "__main__":
    main()
