#!/usr/bin/env python3
"""Remove ImageGen's non-uniform magenta key without touching green device accents."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    image = Image.open(args.input).convert("RGBA")
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            red, green, blue, source_alpha = pixels[x, y]
            dominance = min(red, blue) - green
            chroma_strength = min(red, blue)
            if chroma_strength >= 125 and dominance >= 58:
                alpha = 0
            elif chroma_strength >= 95 and dominance > 26:
                alpha = round(255 * (58 - dominance) / 32)
                alpha = max(0, min(255, alpha))
            else:
                alpha = 255
            pixels[x, y] = (red, green, blue, round(alpha * source_alpha / 255))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.output)


if __name__ == "__main__":
    main()
