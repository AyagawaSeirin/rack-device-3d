#!/usr/bin/env python3
"""Create the six final transparent, physically proportioned elevation assets."""

from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "qa" / "work" / "imagegen-raw"
VIEWS = ROOT / "views"


def remove_magenta(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            red, green, blue, source_alpha = pixels[x, y]
            dominance = min(red, blue) - green
            strength = min(red, blue)
            if strength >= 125 and dominance >= 58:
                alpha = 0
            elif strength >= 95 and dominance > 26:
                alpha = max(0, min(255, round(255 * (58 - dominance) / 32)))
            else:
                alpha = 255
            pixels[x, y] = (red, green, blue, round(alpha * source_alpha / 255))
    return image


def crop_alpha(image: Image.Image) -> Image.Image:
    bounds = image.getchannel("A").getbbox()
    if bounds is None:
        raise RuntimeError("No visible pixels after chroma removal")
    return image.crop(bounds)


def fit_exact(image: Image.Image, size: tuple[int, int], pad: int = 32) -> Image.Image:
    image = crop_alpha(image).resize(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size[0] + pad * 2, size[1] + pad * 2), (0, 0, 0, 0))
    canvas.alpha_composite(image, (pad, pad))
    return canvas


def exact_front() -> Image.Image:
    """Projectively rectify the source-locked exact 24-SFF front photograph."""
    source = Image.open(ROOT / "source" / "third-party" / "kitairu-rh2288-v3-24sff.png").convert("RGBA")
    # Source quadrilateral order: upper-left, lower-left, lower-right, upper-right.
    quad = (67, 225, 67, 309, 583, 307, 583, 224)
    face = source.transform((4096, 731), Image.Transform.QUAD, quad, Image.Resampling.BICUBIC)
    face.putalpha(Image.new("L", face.size, 255))
    canvas = Image.new("RGBA", (4160, 795), (0, 0, 0, 0))
    canvas.alpha_composite(face, (32, 32))
    return canvas


def main() -> None:
    VIEWS.mkdir(parents=True, exist_ok=True)
    selections = {
        # Front is evidence-rectified after repeated ImageGen candidates failed the immutable 24-bay count.
        "rear": (RAW / "rear.png", (4096, 789)),       # 447 / 86.1
        "left": (RAW / "left-v4.png", (4096, 498)),   # 708 / 86.1
        "right": (RAW / "right-v2.png", (4096, 498)),
        "top": (RAW / "top-v3.png", (2586, 4096)),    # 447 / 708
        "bottom": (RAW / "bottom.png", (2586, 4096)),
    }
    exact_front().save(VIEWS / "front.png")
    for face, (path, size) in selections.items():
        fit_exact(remove_magenta(Image.open(path)), size).save(VIEWS / f"{face}.png")


if __name__ == "__main__":
    main()
