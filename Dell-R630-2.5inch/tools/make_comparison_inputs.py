#!/usr/bin/env python3
"""Create same-camera reference/render canvases for the six orthographic QA sheets."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SIZE = (1400, 900)
ASPECT = SIZE[0] / SIZE[1]
MARGIN = 1.13
FACE_METRES = {
    "front": (0.4824, 0.0428),
    "rear": (0.4824, 0.0428),
    "left": (0.7521, 0.0428),
    "right": (0.7521, 0.0428),
    "top": (0.4824, 0.7521),
    "bottom": (0.4824, 0.7521),
}


def checker_from_render(render: Image.Image) -> Image.Image:
    # The CSS checker has a 32 px period and anti-aliased diagonal boundaries.
    # Sample one unobstructed, phase-aligned period from the real viewer capture
    # so reference and render backgrounds are pixel-identical.
    tile = render.crop((384, 0, 416, 32))
    image = Image.new("RGB", SIZE)
    for y in range(0, SIZE[1], 32):
        for x in range(0, SIZE[0], 32):
            image.paste(tile, (x, y))
    return image


def projected_size(face: str) -> tuple[int, int]:
    width, height = FACE_METRES[face]
    frustum_height = max(height, width / ASPECT) * MARGIN
    return (
        round(width / (frustum_height * ASPECT) * SIZE[0]),
        round(height / frustum_height * SIZE[1]),
    )


def paste_approved_face(canvas: Image.Image, face: str) -> None:
    with Image.open(ROOT / "views" / f"{face}.png") as source:
        rgba = source.convert("RGBA")
        alpha_box = rgba.getchannel("A").getbbox()
        if alpha_box:
            rgba = rgba.crop(alpha_box)
        target = projected_size(face)
        rgba.thumbnail(target, Image.Resampling.LANCZOS)
        x = (SIZE[0] - rgba.width) // 2
        y = (SIZE[1] - rgba.height) // 2
        canvas.paste(rgba, (x, y), rgba)


def restore_badge_background(render: Image.Image, background: Image.Image) -> None:
    # The QA badge is viewer UI rather than model output. Remove it identically
    # before the diagnostic pixel comparison.
    render.paste(background.crop((0, 0, 360, 100)), (0, 0))


def main() -> None:
    reference_dir = ROOT / "qa" / "reference" / "orthographic"
    render_dir = ROOT / "qa" / "renders" / "comparison-ready"
    reference_dir.mkdir(parents=True, exist_ok=True)
    render_dir.mkdir(parents=True, exist_ok=True)

    for face in FACE_METRES:
        render_path = ROOT / "qa" / "renders" / f"viewer-b-standard-{face}.png"
        with Image.open(render_path) as source:
            render = source.convert("RGB")
        background = checker_from_render(render)
        restore_badge_background(render, background)

        reference = background.copy()
        paste_approved_face(reference, face)

        if face == "bottom":
            for image in (reference, render):
                ImageDraw.Draw(image).text(
                    (1040, 24),
                    "GENERIC_BOTTOM_FALLBACK",
                    fill="#8b1a1a",
                    stroke_width=2,
                    stroke_fill="#ffffff",
                )

        reference.save(reference_dir / f"{face}.png")
        render.save(render_dir / f"viewer-b-standard-{face}.png")


if __name__ == "__main__":
    main()
