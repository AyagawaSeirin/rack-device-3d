#!/usr/bin/env python3
"""Convert the six magenta imagegen elevations into clean, ratio-locked RGBA PNGs."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


EXPECTED = {
    "front": (482.6, 43.0),
    "rear": (436.0, 43.0),
    "left": (748.0, 43.0),
    "right": (748.0, 43.0),
    "top": (436.0, 748.0),
    "bottom": (436.0, 748.0),
}


def chroma_alpha(image: Image.Image) -> Image.Image:
    rgb = np.asarray(image.convert("RGB"), dtype=np.int16)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]

    # Imagegen's nominal #ff00ff field varies slightly across the canvas.
    # This predicate removes only strongly magenta pixels and leaves black
    # vents, blue VGA, yellow latches, red warning marks, and silver metal.
    chroma = (
        (r > 125)
        & (b > 125)
        & ((np.minimum(r, b) - g) > 72)
        & (np.abs(r - b) < 105)
    )
    alpha = np.where(chroma, 0, 255).astype(np.uint8)

    # A tiny feather removes jagged chroma edges without creating a large
    # semi-transparent halo or opening holes inside the chassis core.
    matte = Image.fromarray(alpha, mode="L").filter(ImageFilter.GaussianBlur(0.45))
    matte_arr = np.asarray(matte, dtype=np.uint8)
    matte_arr = np.where(matte_arr < 20, 0, np.where(matte_arr > 235, 255, matte_arr)).astype(np.uint8)
    return Image.fromarray(matte_arr, mode="L")


def finalize(src: Path, dst: Path, face: str, long_edge: int) -> None:
    image = Image.open(src).convert("RGBA")
    alpha = chroma_alpha(image)
    image.putalpha(alpha)

    bbox = alpha.getbbox()
    if not bbox:
        raise RuntimeError(f"{src}: chroma removal produced an empty image")
    crop = image.crop(bbox)

    physical_w, physical_h = EXPECTED[face]
    ratio = physical_w / physical_h
    if ratio >= 1:
        content_w = long_edge
        content_h = max(1, round(content_w / ratio))
    else:
        content_h = long_edge
        content_w = max(1, round(content_h * ratio))

    crop = crop.resize((content_w, content_h), Image.Resampling.LANCZOS)
    margin = 24
    canvas = Image.new("RGBA", (content_w + margin * 2, content_h + margin * 2), (0, 0, 0, 0))
    canvas.alpha_composite(crop, (margin, margin))
    dst.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dst, optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_dir", type=Path)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--long-edge", type=int, default=2400)
    args = parser.parse_args()

    for face in ("front", "rear", "left", "right", "top", "bottom"):
        finalize(args.raw_dir / f"{face}.png", args.out_dir / f"{face}.png", face, args.long_edge)
        print(args.out_dir / f"{face}.png")


if __name__ == "__main__":
    main()
