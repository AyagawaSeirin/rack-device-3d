#!/usr/bin/env python3
"""Prepare matched-size real-source canvases for the WebGL QA comparisons."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "qa"
SIZE = (1600, 1200)
BACKGROUND = (223, 227, 230, 255)


def fitted_canvas(path: Path, max_size: tuple[int, int], transparent: bool) -> Image.Image:
    source = Image.open(path).convert("RGBA")
    if transparent:
        bbox = source.getchannel("A").point(lambda value: 255 if value > 8 else 0).getbbox()
        if bbox:
            source = source.crop(bbox)
    scale = min(max_size[0] / source.width, max_size[1] / source.height)
    source = source.resize(
        (max(1, round(source.width * scale)), max(1, round(source.height * scale))),
        Image.Resampling.LANCZOS,
    )
    canvas = Image.new("RGBA", SIZE, BACKGROUND)
    x = (SIZE[0] - source.width) // 2
    y = (SIZE[1] - source.height) // 2
    canvas.alpha_composite(source, (x, y))
    return canvas.convert("RGB")


def main() -> None:
    canonical = QA / "reference" / "canonical"
    oblique = QA / "reference" / "oblique"
    canonical.mkdir(parents=True, exist_ok=True)
    oblique.mkdir(parents=True, exist_ok=True)

    limits = {
        "front": (1360, 580),
        "rear": (1360, 580),
        "left": (1380, 500),
        "right": (1380, 500),
        "top": (900, 1080),
        "bottom": (900, 1080),
    }
    for face, limit in limits.items():
        fitted_canvas(ROOT / "views" / f"{face}.png", limit, True).save(
            canonical / f"{face}.png", optimize=True
        )

    oblique_sources = {
        "front-left": ROOT / "source" / "third-party" / "ebay-236708345684-01.webp",
        "front-right": ROOT / "source" / "third-party" / "ebay-236755802715-01.webp",
        "rear-left": ROOT / "source" / "third-party" / "ebay-236708345684-06.webp",
        "rear-right": ROOT / "source" / "third-party" / "ebay-236755802715-06.webp",
    }
    for view, path in oblique_sources.items():
        fitted_canvas(path, SIZE, False).save(oblique / f"{view}.png", optimize=True)


if __name__ == "__main__":
    main()
