#!/usr/bin/env python3
"""Fit approved face assets to the exact QA orthographic camera canvases."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
VIEWS = ROOT / "views"
OUT = ROOT / "qa" / "reference" / "orthographic-canvases"

CANVAS = (1600, 900)
MARGIN = 1.12
BODY_W = 436.0
OVERALL_W = 482.6
BODY_H = 43.0
VISIBLE_H = 43.53
BODY_D = 708.0
VISIBLE_D = 715.7


def crop_alpha(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    bounds = rgba.getchannel("A").getbbox()
    if bounds is None:
        raise RuntimeError("empty alpha matte")
    return rgba.crop(bounds)


def scale_for(face: str) -> float:
    width, height = CANVAS
    if face in {"front", "rear"}:
        projected_w, projected_h = OVERALL_W, VISIBLE_H
    elif face in {"left", "right"}:
        projected_w, projected_h = VISIBLE_D, VISIBLE_H
    else:
        projected_w, projected_h = OVERALL_W, VISIBLE_D
    return min(width / (projected_w * MARGIN), height / (projected_h * MARGIN))


def face_size_mm(face: str) -> tuple[float, float]:
    if face == "front":
        return OVERALL_W, BODY_H
    if face == "rear":
        return BODY_W, BODY_H
    if face in {"left", "right"}:
        return BODY_D, BODY_H
    return BODY_W, BODY_D


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for face in ("front", "rear", "left", "right", "top", "bottom"):
        source = crop_alpha(Image.open(VIEWS / f"{face}.png"))
        width_mm, height_mm = face_size_mm(face)
        pixels_per_mm = scale_for(face)
        fitted = source.resize(
            (round(width_mm * pixels_per_mm), round(height_mm * pixels_per_mm)),
            Image.Resampling.LANCZOS,
        )
        canvas = Image.new("RGBA", CANVAS, (255, 255, 255, 255))
        x = round((CANVAS[0] - fitted.width) / 2)
        y = round((CANVAS[1] - fitted.height) / 2)
        canvas.alpha_composite(fitted, (x, y))
        canvas.convert("RGB").save(OUT / f"{face}.png", optimize=True)


if __name__ == "__main__":
    main()
