#!/usr/bin/env python3
"""Prepare exact-ratio canonical face PNGs from the accepted imagegen outputs.

All edits are geometry-neutral: border-connected chroma has already been removed;
feature-bearing regions are only cropped isotropically or separated by inserted
plain sheet-metal/edge strips. No face is mirrored.
"""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "qa" / "reference" / "generated"
VIEWS = ROOT / "views"


def repeat_edge(im: Image.Image, left: int, right: int) -> Image.Image:
    """Extend an opaque product edge without scaling feature-bearing pixels."""
    out = Image.new("RGBA", (im.width + left + right, im.height), (0, 0, 0, 0))
    alpha = im.getchannel("A")
    threshold = int(im.height * 0.95)
    left_sample = next(
        x for x in range(im.width) if sum(alpha.getpixel((x, y)) >= 220 for y in range(im.height)) >= threshold
    )
    right_sample = next(
        x
        for x in range(im.width - 1, -1, -1)
        if sum(alpha.getpixel((x, y)) >= 220 for y in range(im.height)) >= threshold
    )
    if left:
        sw = min(24, im.width - left_sample)
        strip = im.crop((left_sample, 0, left_sample + sw, im.height)).resize((left, im.height))
        out.alpha_composite(strip, (0, 0))
    out.alpha_composite(im, (left, 0))
    if right:
        sw = min(24, right_sample + 1)
        strip = im.crop((right_sample - sw + 1, 0, right_sample + 1, im.height)).resize((right, im.height))
        out.alpha_composite(strip, (left + im.width, 0))
    return out


def insert_plain_band(im: Image.Image, x: int, width: int, sample_x: int) -> Image.Image:
    """Insert a neutral vertical band sampled from feature-free generated metal."""
    out = Image.new("RGBA", (im.width + width, im.height), (0, 0, 0, 0))
    out.alpha_composite(im.crop((0, 0, x, im.height)), (0, 0))
    sample = im.crop((sample_x, 0, sample_x + width, im.height))
    out.alpha_composite(sample, (x, 0))
    out.alpha_composite(im.crop((x, 0, im.width, im.height)), (x + width, 0))
    return out


def resize_exact(im: Image.Image, size: tuple[int, int]) -> Image.Image:
    return im.resize(size, Image.Resampling.LANCZOS)


def prepare_front() -> None:
    im = Image.open(GENERATED / "front-alpha.png").convert("RGBA")
    # Crop perspective-only top/bottom edge pixels; do not duplicate either wing.
    im = im.crop((19, 512, 1313, 627))
    im = resize_exact(im, (4096, 364))

    # Repair only the five factual bay-number strips from Dell's official Figure 2.
    # Identity/material/carriers remain the source-locked imagegen result.
    page = Image.open(ROOT / "source" / "pdf-pages" / "technical-guide-page-01.png").convert("RGBA")
    official = page.crop((232, 1155, 1638, 1275)).resize(im.size, Image.Resampling.LANCZOS)
    for x in (1064, 1765, 2468, 3170, 3872):
        im.alpha_composite(official.crop((x - 42, 0, x + 42, im.height)), (x - 42, 0))
    im.save(VIEWS / "front.png", compress_level=6)


def prepare_rear() -> None:
    im = Image.open(GENERATED / "rear-alpha.png").convert("RGBA")
    # Crop perspective-only handle drop below the 1U envelope; handles are geometry in GLB.
    im = im.crop((11, 540, 1253, 663))
    im = resize_exact(im, (4096, 404))
    # The tight crop is entirely chassis; ports/vents are dark opaque pixels, never holes.
    im.putalpha(Image.new("L", im.size, 255))
    im.save(VIEWS / "rear.png", compress_level=6)


def prepare_side(face: str, source_name: str, box: tuple[int, int, int, int]) -> None:
    im = Image.open(GENERATED / source_name).convert("RGBA")
    im = im.crop(box)
    im = resize_exact(im, (4096, 240))
    im.save(VIEWS / f"{face}.png", compress_level=6)


def prepare_top() -> None:
    im = Image.open(GENERATED / "top-alpha.png").convert("RGBA")
    # Exclude front wing protrusions; those are separate GLB geometry.
    im = im.crop((64, 50, 901, 1557))
    # Orthographic physical-ratio rectification; feature counts and orientation stay fixed.
    im = resize_exact(im, (2048, 3449))
    im.save(VIEWS / "top.png", compress_level=4)


def prepare_bottom() -> None:
    im = Image.open(GENERATED / "bottom-alpha.png").convert("RGBA")
    # Discard unsupported loops/feet and retain only the conservative opaque plate.
    im = im.crop((85, 65, 881, 1566))
    # Bottom is intentionally non-identifying; rectify only to verified width:depth.
    im = resize_exact(im, (2048, 3449))
    # Store quickly; the web-GLB export performs its own texture optimization.
    im.save(VIEWS / "bottom.png", compress_level=0)


def main() -> None:
    VIEWS.mkdir(parents=True, exist_ok=True)
    prepare_front()
    prepare_rear()
    # Physical left: front control wing on image right. Physical right: Intel wing on image left.
    prepare_side("left", "left-v2-alpha.png", (67, 378, 1814, 480))
    prepare_side("right", "right-v2-alpha.png", (52, 387, 1714, 484))
    prepare_top()
    prepare_bottom()


if __name__ == "__main__":
    main()
