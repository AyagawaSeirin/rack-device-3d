#!/usr/bin/env python3
"""Prepare the six source-locked imagegen faces without anisotropic scaling."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
KEYED = ROOT / "qa" / "work" / "imagegen-keyed"
VIEWS = ROOT / "views"
REPORT = ROOT / "qa" / "views-processing.json"
LONG_EDGE = 3072
PADDING = 8
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def crop_face(name: str, image: Image.Image) -> tuple[Image.Image, str]:
    """Crop only verified product regions; splice only featureless metal bands."""

    if name == "front":
        # Remove chroma antialias residue while retaining the complete rack wings.
        return image.crop((53, 289, 1666, 580)), "crop x53:1666 y289:580"
    if name == "rear":
        # Discard the perspective-only upper projections inherited from Image 1.
        return image.crop((35, 256, 1744, 598)), "crop x35:1744 y256:598"
    if name == "left":
        return image.crop((62, 329, 1859, 550)), "crop x62:1859 y329:550"
    if name == "right":
        return image.crop((69, 287, 1915, 515)), "crop x69:1915 y287:515"
    if name == "top":
        # Keep the 434 mm body only. Remove the separate front-wing corners and
        # rear projection, then shorten a plain label-deck metal band so the
        # source pixels reach the verified 434:647.07 ratio without stretching.
        body = image.crop((114, 140, 896, 1377))
        upper = body.crop((0, 0, 782, 945))
        lower = body.crop((0, 1016, 782, 1237))
        out = Image.new("RGBA", (782, 1166), (0, 0, 0, 0))
        out.alpha_composite(upper, (0, 0))
        out.alpha_composite(lower, (0, 945))
        return out, "crop body x114:896 y140:1377; remove plain deck band y945:1016"
    if name == "bottom":
        # Preserve both folded perimeter edges and remove only 32 px of plain,
        # non-identifying central metal to reach the verified body ratio.
        body = image.crop((50, 63, 973, 1471))
        upper = body.crop((0, 0, 923, 687))
        lower = body.crop((0, 719, 923, 1408))
        out = Image.new("RGBA", (923, 1376), (0, 0, 0, 0))
        out.alpha_composite(upper, (0, 0))
        out.alpha_composite(lower, (0, 687))
        return out, "crop body x50:973 y63:1471; remove plain center band y687:719"
    raise ValueError(name)


def make_opaque(image: Image.Image) -> Image.Image:
    """Keep antialiased silhouette pixels, force visible product pixels opaque."""

    array = np.array(image.convert("RGBA"), dtype=np.uint8)
    alpha = array[:, :, 3]
    array[alpha >= 224, 3] = 255
    clear = alpha <= 8
    array[clear] = (0, 0, 0, 0)
    return Image.fromarray(array, mode="RGBA")


def force_rect_opaque(image: Image.Image) -> Image.Image:
    """Fill any chroma-cut pinholes in a proven rectangular equipment face."""

    array = np.array(image.convert("RGBA"), dtype=np.uint8)
    # The selected crops are the proven rectangular equipment surfaces. Any
    # transparent pixel inside them is a chroma-removal error; its retained RGB
    # is kept and only alpha is repaired. Dark retained RGB is correct for the
    # server's edge gaps, vents, and recesses.
    array[:, :, 3] = 255
    return Image.fromarray(array, mode="RGBA")


def repair_verified_markings(name: str, image: Image.Image) -> Image.Image:
    """Replace only AI pseudo-text with verified factory/model markings."""

    output = image.copy()
    draw = ImageDraw.Draw(output)
    if name == "front":
        brand_font = ImageFont.truetype(FONT_BOLD, 6)
        draw.text((1494, 266), "DELL", font=brand_font, fill=(228, 230, 231, 255))
    elif name == "rear":
        draw.rounded_rectangle(
            (538, 273, 610, 321),
            radius=3,
            fill=(21, 23, 23, 255),
            outline=(164, 167, 166, 255),
            width=1,
        )
        draw.text(
            (544, 281),
            "DELL EMC",
            font=ImageFont.truetype(FONT_BOLD, 7),
            fill=(235, 237, 236, 255),
        )
        draw.text(
            (544, 294),
            "PowerEdge",
            font=ImageFont.truetype(FONT_REGULAR, 6),
            fill=(218, 220, 219, 255),
        )
        draw.text(
            (544, 306),
            "R7515",
            font=ImageFont.truetype(FONT_BOLD, 7),
            fill=(235, 237, 236, 255),
        )
    elif name == "top":
        # Keep the real generated paper, borders, colors and lighting, while
        # making unsupported serial/QR/service pseudo-text intentionally unreadable.
        box = (45, 990, 760, 1145)
        softened = output.crop(box).filter(ImageFilter.GaussianBlur(radius=2.2))
        output.paste(softened, box)
    return output


def main() -> None:
    VIEWS.mkdir(parents=True, exist_ok=True)
    report: dict[str, object] = {
        "method": "built-in image_gen; magenta chroma removal; no anisotropic resize",
        "long_edge_px": LONG_EDGE,
        "padding_px": PADDING,
        "faces": {},
    }

    for name in ("front", "rear", "left", "right", "top", "bottom"):
        source = KEYED / f"{name}.png"
        image = Image.open(source).convert("RGBA")
        cropped, operation = crop_face(name, image)
        cropped = make_opaque(cropped)
        cropped = repair_verified_markings(name, cropped)
        if name in {"front", "rear", "top", "bottom"}:
            cropped = force_rect_opaque(cropped)

        scale = LONG_EDGE / max(cropped.size)
        resized_size = tuple(max(1, round(value * scale)) for value in cropped.size)
        resized = cropped.resize(resized_size, Image.Resampling.LANCZOS)
        resized = make_opaque(resized)

        canvas = Image.new(
            "RGBA",
            (resized.width + 2 * PADDING, resized.height + 2 * PADDING),
            (0, 0, 0, 0),
        )
        canvas.alpha_composite(resized, (PADDING, PADDING))
        output = VIEWS / f"{name}.png"
        canvas.save(output, optimize=True)

        alpha = canvas.getchannel("A")
        histogram = alpha.histogram()
        bbox = alpha.getbbox()
        content_ratio = (bbox[2] - bbox[0]) / (bbox[3] - bbox[1]) if bbox else None
        report["faces"][name] = {
            "source": str(source.relative_to(ROOT)),
            "source_sha256": sha256(source),
            "operation": operation,
            "cropped_size": list(cropped.size),
            "output_size": list(canvas.size),
            "alpha_bbox": list(bbox) if bbox else None,
            "content_ratio": content_ratio,
            "transparent_pixels": histogram[0],
            "partial_alpha_pixels": sum(histogram[1:255]),
            "opaque_pixels": histogram[255],
            "output": str(output.relative_to(ROOT)),
            "output_sha256": sha256(output),
        }

    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(REPORT)


if __name__ == "__main__":
    main()
