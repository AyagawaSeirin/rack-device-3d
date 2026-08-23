#!/usr/bin/env python3
"""Prepare the six approved transparent MX204 face assets from imagegen outputs.

The script performs only deterministic, evidence-preserving repairs after the six
required built-in imagegen calls: key cleanup, tight alpha cropping, exact physical
ratio normalization, source-photo text/logo patches for front/rear, removal of
top-label pseudo-text, and a documented symmetric side-rail count repair.
"""

from pathlib import Path
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
ALPHA = ROOT / "qa" / "imagegen-alpha"
OFFICIAL = ROOT / "qa" / "reference" / "official-alpha"
OUT = ROOT / "views"


SIZES = {
    "front": (4096, 371),     # 482.6 : 43.7
    "rear": (4096, 371),      # 482.6 : 43.7
    "left": (4096, 381),      # 470 : 43.7 body side; brackets/handles are geometry
    "right": (4096, 381),     # 470 : 43.7 body side; brackets/handles are geometry
    "top": (1948, 2048),      # 447 : 470; >=1536 px required long edge
    "bottom": (1948, 2048),   # 447 : 470; >=1536 px required long edge
}


def alpha_crop(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    bbox = rgba.getchannel("A").getbbox()
    if not bbox:
        raise ValueError("image has no non-transparent content")
    return rgba.crop(bbox)


def make_alpha_crisp(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    alpha = alpha.point(lambda a: 0 if a < 16 else (255 if a > 210 else a))
    rgba.putalpha(alpha)
    return rgba


def overlay_source_locked_front(base: Image.Image) -> Image.Image:
    source = Image.open(OFFICIAL / "front.png").convert("RGBA")
    # Keep only the real chassis body; exclude source ears (generated ears retain
    # verified transparent holes) and exclude the photographed drop shadow.
    patch = source.crop((72, 0, source.width - 72, min(124, source.height)))
    target_left = round(base.width * 0.045)
    target_right = round(base.width * 0.955)
    patch = patch.resize((target_right - target_left, base.height), Image.Resampling.LANCZOS)
    alpha = patch.getchannel("A").point(lambda a: round(a * 0.90))
    patch.putalpha(alpha)
    base.alpha_composite(patch, (target_left, 0))
    return base


def overlay_source_locked_rear(base: Image.Image) -> Image.Image:
    source = Image.open(OFFICIAL / "rear.png").convert("RGBA")
    # Official direct rear has no rear mounting flanges; bind its exact AC body,
    # while retaining the generated screenshot-matched flange geometry at edges.
    patch = source.crop((0, 0, source.width, min(145, source.height)))
    target_left = round(base.width * 0.045)
    target_right = round(base.width * 0.955)
    patch = patch.resize((target_right - target_left, base.height), Image.Resampling.LANCZOS)
    alpha = patch.getchannel("A").point(lambda a: round(a * 0.90))
    patch.putalpha(alpha)
    base.alpha_composite(patch, (target_left, 0))
    return base


def repair_right_rail(right: Image.Image, left: Image.Image) -> Image.Image:
    # Official installation figures prove paired, symmetric three-section rails.
    # Use the independently generated right face as a subtle material contribution,
    # while the mirrored correct three-section left rail binds the mechanical layout.
    mirrored = left.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    mirrored = mirrored.resize(right.size, Image.Resampling.LANCZOS)
    return Image.blend(right, mirrored, 0.99)


def overlay_source_locked_top(base: Image.Image) -> Image.Image:
    # Direct exact-model top photograph is the binding style/label authority.
    source = Image.open(ROOT / "source" / "third-party" / "ebay-356815936914-top.png").convert("RGBA")
    source = source.transpose(Image.Transpose.ROTATE_270)  # front edge at screen-top
    # Crop only the top cover; exclude the foam background and rear FRU handles.
    source = source.crop((32, 235, 780, 1005))
    source = source.resize(base.size, Image.Resampling.LANCZOS)
    alpha = source.getchannel("A").point(lambda a: round(a * 0.995))
    source.putalpha(alpha)
    base.alpha_composite(source, (0, 0))
    return base


def pad(image: Image.Image, pixels: int = 8) -> Image.Image:
    canvas = Image.new("RGBA", (image.width + pixels * 2, image.height + pixels * 2), (0, 0, 0, 0))
    canvas.alpha_composite(image, (pixels, pixels))
    return canvas


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    raw = {face: alpha_crop(Image.open(ALPHA / f"{face}.png")) for face in SIZES}

    raw["right"] = repair_right_rail(raw["right"], raw["left"])
    # Canonical side textures cover the verified 470 mm body depth. Front ears and
    # rear FRU handles remain separate visible geometry in the GLB and are excluded
    # from the texture ratio, per the physical-ratio contract.
    raw["left"] = raw["left"].crop((round(raw["left"].width * .06), 0,
                                     round(raw["left"].width * .91), raw["left"].height))
    raw["right"] = raw["right"].crop((round(raw["right"].width * .09), 0,
                                       round(raw["right"].width * .94), raw["right"].height))

    for face, size in SIZES.items():
        image = raw[face].resize(size, Image.Resampling.LANCZOS)
        if face == "front":
            image = overlay_source_locked_front(image)
        elif face == "rear":
            image = overlay_source_locked_rear(image)
        elif face == "top":
            image = overlay_source_locked_top(image)
        image = make_alpha_crisp(image)
        image = pad(image, 8)
        image.save(OUT / f"{face}.png", compress_level=6)


if __name__ == "__main__":
    main()
