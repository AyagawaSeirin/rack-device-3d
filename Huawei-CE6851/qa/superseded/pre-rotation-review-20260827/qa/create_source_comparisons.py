#!/usr/bin/env python3
"""Create matched-canvas source/render/overlay/difference sheets."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "qa"
VIEWS = ROOT / "views"
HELPER = ROOT.parent / ".agents" / "skills" / "rack-device-3d-model-assets" / "scripts" / "create_comparison_sheet.py"
FACES = ("front", "rear", "left", "right", "top", "bottom")
SETS = {
    "threejs-standard": QA / "renders" / "threejs" / "standard",
    "babylonjs-web": QA / "renders" / "babylonjs" / "web",
}


def tight_crop(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    alpha = np.asarray(rgba.getchannel("A"))
    ys, xs = np.nonzero(alpha > 8)
    if not len(xs):
        raise ValueError("empty alpha content")
    return rgba.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))


def clean_and_bbox(render: Image.Image) -> tuple[Image.Image, tuple[int, int, int, int], tuple[int, int, int]]:
    rgb = render.convert("RGB")
    array = np.asarray(rgb).copy()
    background = tuple(int(value) for value in array[-1, -1])
    array[:42, :250] = np.asarray(background, dtype=np.uint8)
    delta = np.max(np.abs(array.astype(np.int16) - np.asarray(background, dtype=np.int16)), axis=2)
    mask = delta > 12
    ys, xs = np.nonzero(mask)
    if not len(xs):
        raise ValueError("render has no visible model")
    bbox = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
    return Image.fromarray(array, mode="RGB"), bbox, background


def main() -> None:
    for set_name, render_dir in SETS.items():
        matched_dir = QA / "reference" / "matched" / set_name
        clean_dir = QA / "reference" / "clean-renders" / set_name
        matched_dir.mkdir(parents=True, exist_ok=True)
        clean_dir.mkdir(parents=True, exist_ok=True)

        for face in FACES:
            render = Image.open(render_dir / f"{face}.png")
            clean_render, bbox, background = clean_and_bbox(render)
            clean_path = clean_dir / f"{face}.png"
            clean_render.save(clean_path)

            source = tight_crop(Image.open(VIEWS / f"{face}.png"))
            target_width = bbox[2] - bbox[0]
            target_height = bbox[3] - bbox[1]
            scale = min(target_width / source.width, target_height / source.height)
            resized = source.resize(
                (max(1, round(source.width * scale)), max(1, round(source.height * scale))),
                Image.Resampling.LANCZOS,
            )
            canvas = Image.new("RGBA", render.size, (*background, 255))
            center_x = (bbox[0] + bbox[2]) / 2.0
            center_y = (bbox[1] + bbox[3]) / 2.0
            x = round(center_x - resized.width / 2.0)
            y = round(center_y - resized.height / 2.0)
            canvas.alpha_composite(resized, (x, y))
            reference_path = matched_dir / f"{face}.png"
            canvas.convert("RGB").save(reference_path)

            comparison_path = QA / "comparisons" / f"source-{set_name}-{face}.png"
            subprocess.run(
                [sys.executable, str(HELPER), str(reference_path), str(clean_path), str(comparison_path)],
                check=True,
            )


if __name__ == "__main__":
    main()
