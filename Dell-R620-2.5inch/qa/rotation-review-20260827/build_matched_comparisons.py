#!/usr/bin/env python3
"""Build source/render/overlay/difference four-panel sheets from matched captures."""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

from PIL import Image, ImageChops, ImageEnhance, ImageStat


def stable_mask(light: Image.Image, dark: Image.Image) -> Image.Image:
    light = light.convert("RGB")
    dark = dark.convert("RGB")
    diff = ImageChops.difference(light, dark)
    width, height = light.size
    source = diff.load()
    mask = Image.new("L", light.size)
    target = mask.load()
    for y in range(height):
        for x in range(width):
            if x < 300 and y < 110:
                continue
            if max(source[x, y]) < 18:
                target[x, y] = 255
    # Keep the largest four-connected stable component (the rendered device).
    seen = bytearray(width * height)
    best: list[tuple[int, int]] = []
    for y in range(height):
        for x in range(width):
            index = y * width + x
            if seen[index] or target[x, y] == 0:
                continue
            seen[index] = 1
            queue = deque([(x, y)])
            component: list[tuple[int, int]] = []
            while queue:
                px, py = queue.popleft()
                component.append((px, py))
                for nx, ny in ((px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)):
                    if 0 <= nx < width and 0 <= ny < height:
                        ni = ny * width + nx
                        if not seen[ni] and target[nx, ny]:
                            seen[ni] = 1
                            queue.append((nx, ny))
            if len(component) > len(best):
                best = component
    output = Image.new("L", light.size)
    out = output.load()
    for x, y in best:
        out[x, y] = 255
    return output


def checker(size: tuple[int, int]) -> Image.Image:
    image = Image.new("RGB", size)
    pixels = image.load()
    colors = ((245, 246, 247), (207, 213, 218))
    for y in range(size[1]):
        for x in range(size[0]):
            pixels[x, y] = colors[((x // 16) + (y // 16)) & 1]
    return image


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("model_root", type=Path)
    parser.add_argument("capture_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for face in ("front", "rear", "left", "right", "top", "bottom"):
        light = Image.open(args.capture_dir / f"{face}-light.png").convert("RGB")
        dark = Image.open(args.capture_dir / f"{face}-dark.png").convert("RGB")
        mask = stable_mask(light, dark)
        bbox = mask.getbbox()
        if not bbox:
            raise RuntimeError(f"no stable rendered object for {face}")
        render = light
        reference = checker(light.size)
        source = Image.open(args.model_root / "views" / f"{face}.png").convert("RGBA")
        target_w, target_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        source.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
        x = bbox[0] + (target_w - source.width) // 2
        y = bbox[1] + (target_h - source.height) // 2
        reference.paste(source, (x, y), source)
        overlay = Image.blend(reference, render, 0.5)
        difference = ImageChops.difference(reference, render)
        difference = ImageEnhance.Contrast(difference).enhance(2.0)
        sheet = Image.new("RGB", (light.width * 4, light.height), "white")
        for index, panel in enumerate((reference, render, overlay, difference)):
            sheet.paste(panel, (index * light.width, 0))
        sheet.save(args.output_dir / f"{face}.png", format="PNG")
        stats = ImageStat.Stat(ImageChops.difference(reference, render))
        print(face, "bbox", bbox, "mean_abs_rgb", [round(value, 4) for value in stats.mean])


if __name__ == "__main__":
    main()
