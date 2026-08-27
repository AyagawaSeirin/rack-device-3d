#!/usr/bin/env python3
"""Repair only factual canvas ratio and external chroma spill in R720 SFF views.

No source pixels inside the chassis are regenerated, scaled, mirrored, or
restyled.  The archived pre-review assets remain immutable under qa/superseded.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "views"


def clear_border_magenta(image: Image.Image) -> tuple[Image.Image, int]:
    image = image.convert("RGBA")
    width, height = image.size
    pixels = image.load()
    seen = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def candidate(x: int, y: int) -> bool:
        r, g, b, a = pixels[x, y]
        return a <= 12 or (r - g > 24 and b - g > 20 and r > 90 and b > 80)

    def seed(x: int, y: int) -> None:
        index = y * width + x
        if not seen[index] and candidate(x, y):
            seen[index] = 1
            queue.append((x, y))

    for x in range(width):
        seed(x, 0)
        seed(x, height - 1)
    for y in range(height):
        seed(0, y)
        seed(width - 1, y)

    cleared = 0
    while queue:
        x, y = queue.popleft()
        r, g, b, a = pixels[x, y]
        if a:
            pixels[x, y] = (r, g, b, 0)
            cleared += 1
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < width and 0 <= ny < height:
                index = ny * width + nx
                if not seen[index] and candidate(nx, ny):
                    seen[index] = 1
                    queue.append((nx, ny))
    # This physical side contains no legitimate magenta product detail.  The
    # imagegen prompt explicitly forbade #FF00FF inside the chassis, so remove
    # any remaining chroma-dominant fringe even when an anti-aliased silver row
    # separated it from the border flood.
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a and r - g > 15 and b - g > 12 and r > 30 and b > 30:
                pixels[x, y] = (r, g, b, 0)
                cleared += 1
    return image, cleared


def pad_edge_rows(image: Image.Image, target_height: int) -> Image.Image:
    if image.height >= target_height:
        return image
    top = (target_height - image.height) // 2
    bottom = target_height - image.height - top
    output = Image.new("RGBA", (image.width, target_height))
    output.paste(image.crop((0, 0, image.width, 1)).resize((image.width, top)), (0, 0))
    output.paste(image, (0, top))
    output.paste(
        image.crop((0, image.height - 1, image.width, image.height)).resize((image.width, bottom)),
        (0, top + image.height),
    )
    return output


def pad_edge_columns(image: Image.Image, target_width: int) -> Image.Image:
    if image.width >= target_width:
        return image
    left = (target_width - image.width) // 2
    right = target_width - image.width - left
    output = Image.new("RGBA", (target_width, image.height))
    output.paste(image.crop((0, 0, 1, image.height)).resize((left, image.height)), (0, 0))
    output.paste(image, (left, 0))
    output.paste(
        image.crop((image.width - 1, 0, image.width, image.height)).resize((right, image.height)),
        (left + image.width, 0),
    )
    return output


def extend_side_content_height(image: Image.Image, target_height: int) -> Image.Image:
    """Extend only the verified straight sheet-metal edge; never scale pixels."""
    image = image.convert("RGBA")
    alpha = image.getchannel("A")
    bbox = alpha.point(lambda value: 255 if value > 12 else 0).getbbox()
    if not bbox:
        raise RuntimeError("left view has no opaque content")
    left, top, right, bottom = bbox
    pixels = image.load()
    neutral = (174, 177, 176, 255)
    for y in range(0, top):
        for x in range(left, right):
            sample = pixels[x, top]
            pixels[x, y] = sample if sample[3] > 12 else neutral
    for y in range(bottom, target_height):
        for x in range(left, right):
            sample = pixels[x, bottom - 1]
            pixels[x, y] = sample if sample[3] > 12 else neutral
    return image


def main() -> None:
    left, cleared = clear_border_magenta(Image.open(VIEWS / "left.png"))
    left = extend_side_content_height(pad_edge_rows(left, 298), 298)
    repairs = {
        "left": left,
        "right": pad_edge_rows(Image.open(VIEWS / "right.png").convert("RGBA"), 298),
        "top": pad_edge_columns(Image.open(VIEWS / "top.png").convert("RGBA"), 1518),
        "bottom": pad_edge_columns(Image.open(VIEWS / "bottom.png").convert("RGBA"), 1518),
    }
    for face, image in repairs.items():
        image.save(VIEWS / f"{face}.png", format="PNG")
    print({"magenta_border_pixels_cleared": cleared,
           "sizes": {face: image.size for face, image in repairs.items()}})


if __name__ == "__main__":
    main()
