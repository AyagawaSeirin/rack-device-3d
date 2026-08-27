from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[2]
VIEWS = ROOT / "views"

TARGETS = {
    "front": (2600, 467),
    "rear": (2400, 467),
    "left": (3000, 339),
    "right": (3000, 339),
    "top": (1512, 2600),
    "bottom": (1512, 2600),
}


def alpha_bbox(image: Image.Image, threshold: int = 12) -> tuple[int, int, int, int]:
    alpha = np.asarray(image.getchannel("A"))
    ys, xs = np.nonzero(alpha > threshold)
    if not len(xs):
        raise RuntimeError("empty alpha content")
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def paste_filtered_region(image: Image.Image, box: tuple[int, int, int, int], radius: float) -> None:
    region = image.crop(box).filter(ImageFilter.GaussianBlur(radius))
    image.paste(region, box)


def repair_front(image: Image.Image) -> Image.Image:
    # The generated SR655 badge is kept. Blur only the unverified synthetic
    # serial/QR-like microprint below it, preferring an unreadable factory area.
    w, h = image.size
    box = (int(w * 0.946), int(h * 0.70), int(w * 0.997), int(h * 0.98))
    paste_filtered_region(image, box, 5.0)
    return image


def repair_top(image: Image.Image) -> Image.Image:
    # Preserve the exact factory service-label layout from the real source while
    # suppressing generated serial/QR-like microtext. Diagrams, large blocks,
    # Lenovo marks, latch, vent and cover stampings remain in place.
    w, h = image.size
    paste_filtered_region(image, (int(w * 0.55), int(h * 0.02), int(w * 0.97), int(h * 0.12)), 2.2)
    paste_filtered_region(image, (int(w * 0.06), int(h * 0.27), int(w * 0.88), int(h * 0.69)), 1.4)
    draw = ImageDraw.Draw(image)
    draw.rectangle((int(w * 0.07), int(h * 0.635), int(w * 0.17), int(h * 0.66)), fill=(23, 23, 23, 255))
    draw.rectangle((int(w * 0.46), int(h * 0.635), int(w * 0.515), int(h * 0.67)), fill=(24, 24, 24, 255))
    return image


def erase_bottom_cross_seams(image: Image.Image) -> Image.Image:
    # The one permitted imagegen call transposed the official longitudinal seam
    # paths into crosswise seams. Interpolate only those two narrow bands, then
    # redraw the official longitudinal paths after final rectification.
    arr = np.asarray(image).copy()
    h, w, _ = arr.shape
    for y0f, y1f in ((0.245, 0.315), (0.505, 0.585)):
        y0 = max(2, int(h * y0f))
        y1 = min(h - 3, int(h * y1f))
        top = arr[y0 - 2].astype(np.float32)
        bottom = arr[y1 + 2].astype(np.float32)
        span = max(1, y1 - y0)
        for y in range(y0, y1 + 1):
            t = (y - y0) / span
            arr[y] = np.clip((1.0 - t) * top + t * bottom, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def make_core_opaque(image: Image.Image) -> Image.Image:
    arr = np.asarray(image).copy()
    alpha = arr[..., 3]
    positive = alpha > 0
    interior = positive.copy()
    interior[1:, :] &= positive[:-1, :]
    interior[:-1, :] &= positive[1:, :]
    interior[:, 1:] &= positive[:, :-1]
    interior[:, :-1] &= positive[:, 1:]
    alpha[interior] = 255
    arr[..., 3] = alpha
    return Image.fromarray(arr, "RGBA")


def draw_bottom_longitudinal_seams(image: Image.Image) -> Image.Image:
    w, h = image.size
    draw = ImageDraw.Draw(image)
    paths = [
        [(int(w * 0.34), 0), (int(w * 0.35), int(h * 0.34)), (int(w * 0.39), int(h * 0.52)), (int(w * 0.40), h - 1)],
        [(int(w * 0.67), 0), (int(w * 0.69), int(h * 0.40)), (int(w * 0.67), int(h * 0.57)), (int(w * 0.70), h - 1)],
    ]
    for points in paths:
        draw.line(points, fill=(145, 146, 144, 255), width=4, joint="curve")
        highlight = [(x + 4, y) for x, y in points]
        draw.line(highlight, fill=(222, 223, 221, 255), width=3, joint="curve")
    return image


def main() -> None:
    for face, target in TARGETS.items():
        path = VIEWS / f"{face}.png"
        image = Image.open(path).convert("RGBA")
        image = image.crop(alpha_bbox(image))
        if face == "front":
            image = repair_front(image)
        elif face == "top":
            image = repair_top(image)
        elif face == "bottom":
            image = erase_bottom_cross_seams(image)

        # This is a measured orthographic rectification to the authoritative
        # physical ratio, not a creative resize. Lanczos keeps source detail.
        image = image.resize(target, Image.Resampling.LANCZOS)
        image = make_core_opaque(image)
        if face == "bottom":
            image = draw_bottom_longitudinal_seams(image)
        image.save(path, optimize=True)
        print(face, image.size, alpha_bbox(image))


if __name__ == "__main__":
    main()

