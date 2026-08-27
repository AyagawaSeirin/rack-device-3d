#!/usr/bin/env python3
"""Create same-camera 1280x720 elevation canvases for GLB comparison sheets.

The production elevation is fitted uniformly (never anisotropically) into the
analytical orthographic bounds used by both QA viewers.  The checkerboard is
sampled from an actual render so the comparison helper measures the device,
not a synthetic background mismatch.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "views"
RENDERS = ROOT / "qa" / "renders"
OUT = ROOT / "qa" / "comparison-references"
CANVAS = (1280, 720)
ASPECT = CANVAS[0] / CANVAS[1]

# Exact final GLB bounds, in metres.
PROJECTIONS = {
    "front": (0.482, 0.0868),
    "rear": (0.482, 0.0868),
    "left": (0.703755, 0.0868),
    "right": (0.703755, 0.0868),
    "top": (0.482, 0.703755),
    "bottom": (0.482, 0.703755),
}


def tight_alpha(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    bbox = rgba.getchannel("A").point(lambda value: 255 if value > 8 else 0).getbbox()
    if bbox is None:
        raise ValueError("empty production elevation")
    return rgba.crop(bbox)


def checker_from_actual(render: Image.Image) -> Image.Image:
    """Rebuild the 48 px CSS checker from a known clear bottom-right tile."""
    rgba = render.convert("RGBA")
    tile = rgba.crop((1200, 624, 1248, 672))
    canvas = Image.new("RGBA", CANVAS)
    for y in range(0, CANVAS[1], 48):
        for x in range(0, CANVAS[0], 48):
            canvas.paste(tile, (x, y))
    # Preserve the viewer/status identity overlay exactly.
    canvas.paste(rgba.crop((0, 0, 620, 90)), (0, 0))
    return canvas


def projected_box(face: str) -> tuple[int, int, int, int]:
    world_width, world_height = PROJECTIONS[face]
    half_height = max(world_height * 0.62, world_width / ASPECT * 0.62)
    viewport_height = 2 * half_height
    viewport_width = viewport_height * ASPECT
    pixel_width = world_width / viewport_width * CANVAS[0]
    pixel_height = world_height / viewport_height * CANVAS[1]
    x0 = math.floor((CANVAS[0] - pixel_width) / 2)
    y0 = math.floor((CANVAS[1] - pixel_height) / 2)
    x1 = math.ceil((CANVAS[0] + pixel_width) / 2)
    y1 = math.ceil((CANVAS[1] + pixel_height) / 2)
    return x0, y0, x1, y1


def main() -> None:
    for viewer in ("three", "babylon"):
        for model in ("standard", "web"):
            output_dir = OUT / viewer / model
            output_dir.mkdir(parents=True, exist_ok=True)
            for face in PROJECTIONS:
                render_path = RENDERS / viewer / model / f"{face}.png"
                canvas = checker_from_actual(Image.open(render_path))
                x0, y0, x1, y1 = projected_box(face)
                source = tight_alpha(Image.open(VIEWS / f"{face}.png"))
                scale = min((x1 - x0) / source.width, (y1 - y0) / source.height)
                target_size = (
                    max(1, round(source.width * scale)),
                    max(1, round(source.height * scale)),
                )
                source = source.resize(target_size, Image.Resampling.LANCZOS)
                target_x = round((CANVAS[0] - source.width) / 2)
                target_y = round((CANVAS[1] - source.height) / 2)
                canvas.alpha_composite(source, (target_x, target_y))
                canvas.convert("RGB").save(output_dir / f"{face}.png")


if __name__ == "__main__":
    main()
