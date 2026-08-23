from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
RENDERS = ROOT / "qa/renders/three-standard"
OUT = ROOT / "qa/reference/compare"
BG = (238, 240, 242, 255)


def alpha_bbox(image: Image.Image, threshold: int = 12) -> tuple[int, int, int, int]:
    alpha = np.asarray(image.getchannel("A"))
    ys, xs = np.nonzero(alpha > threshold)
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def render_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    arr = np.asarray(image.convert("RGB")).astype(np.int16)
    bg = np.array(BG[:3], dtype=np.int16)
    mask = np.abs(arr - bg).max(axis=2) > 8
    ys, xs = np.nonzero(mask)
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def fit_rgba_to_box(source: Image.Image, canvas_size: tuple[int, int], box: tuple[int, int, int, int]) -> Image.Image:
    source = source.convert("RGBA").crop(alpha_bbox(source))
    target_w = box[2] - box[0]
    target_h = box[3] - box[1]
    scale = min(target_w / source.width, target_h / source.height)
    size = (max(1, round(source.width * scale)), max(1, round(source.height * scale)))
    source = source.resize(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", canvas_size, BG)
    x = box[0] + (target_w - size[0]) // 2
    y = box[1] + (target_h - size[1]) // 2
    canvas.alpha_composite(source, (x, y))
    return canvas.convert("RGB")


def white_render_to_rgba(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGB")
    arr = np.asarray(image)
    distance = 255 - arr.min(axis=2)
    alpha = np.clip((distance.astype(np.float32) - 2.0) * 15.0, 0, 255).astype(np.uint8)
    return Image.fromarray(np.dstack([arr, alpha]), "RGBA")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    faces = ["front", "rear", "right", "left", "top", "bottom"]
    for face in faces:
        render = Image.open(RENDERS / f"{face}.png").convert("RGB")
        box = render_bbox(render)
        source = Image.open(ROOT / "views" / f"{face}.png")
        ref = fit_rgba_to_box(source, render.size, box)
        ref.save(OUT / f"{face}.png", optimize=True)
        print(face, box)

    three_quarter = {
        "frontRight": ROOT / "qa/reference/official-viewer-front-right-crop.png",
        "rearRight": ROOT / "qa/reference/official-viewer-rear-right-crop.png",
    }
    for name, path in three_quarter.items():
        render = Image.open(RENDERS / f"{name}.png").convert("RGB")
        box = render_bbox(render)
        source = white_render_to_rgba(path)
        ref = fit_rgba_to_box(source, render.size, box)
        ref.save(OUT / f"{name}.png", optimize=True)
        print(name, box)


if __name__ == "__main__":
    main()

