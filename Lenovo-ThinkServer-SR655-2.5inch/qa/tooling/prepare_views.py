from pathlib import Path
import sys
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "qa" / "imagegen-output"
OUT = ROOT / "views"

TARGETS = {
    "front": (2600, 467),
    "rear": (2600, 467),
    "right": (3000, 339),
    "left": (3000, 339),
    "top": (1512, 2600),
    "bottom": (1512, 2600),
}


def blur_rgb_region(im: Image.Image, frac_box, radius: float) -> None:
    w, h = im.size
    box = (
        round(frac_box[0] * w),
        round(frac_box[1] * h),
        round(frac_box[2] * w),
        round(frac_box[3] * h),
    )
    crop = im.crop(box)
    rgb = crop.convert("RGB").filter(ImageFilter.GaussianBlur(radius))
    rgba = Image.merge("RGBA", (*rgb.split(), crop.getchannel("A")))
    im.alpha_composite(rgba, (box[0], box[1]))


def clean_alpha(im: Image.Image) -> Image.Image:
    r, g, b, a = im.split()
    a = a.point(lambda p: 0 if p < 6 else (255 if p > 248 else p))
    return Image.merge("RGBA", (r, g, b, a))


def seal_opaque_equipment_surface(im: Image.Image) -> Image.Image:
    """Make every product scanline opaque between its exterior silhouette edges."""
    px = im.load()
    for y in range(im.height):
        visible = [x for x in range(im.width) if px[x, y][3] > 24]
        if not visible:
            continue
        left, right = visible[0], visible[-1]
        for x in range(left, right + 1):
            r, g, b, _ = px[x, y]
            px[x, y] = (r, g, b, 255)
    return im


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    selected = sys.argv[1:] or list(TARGETS)
    unknown = [face for face in selected if face not in TARGETS]
    if unknown:
        raise SystemExit(f"unknown faces: {unknown}")
    for face in selected:
        target = TARGETS[face]
        im = Image.open(RAW / f"{face}-alpha.png").convert("RGBA")
        mask = im.getchannel("A").point(lambda p: 255 if p > 16 else 0)
        bbox = mask.getbbox()
        if not bbox:
            raise RuntimeError(f"{face}: empty alpha")
        im = im.crop(bbox)

        if face == "front":
            # The direct user photo cannot prove protocol/serial microtext.
            blur_rgb_region(im, (0.075, 0.70, 0.925, 0.93), 1.25)
            blur_rgb_region(im, (0.948, 0.78, 0.995, 0.985), 3.0)
        elif face == "top":
            # Keep the factory service-label layout while deidentifying generated
            # serial/QR/barcode-like microcontent.
            blur_rgb_region(im, (0.055, 0.045, 0.925, 0.145), 1.1)
            blur_rgb_region(im, (0.070, 0.285, 0.855, 0.655), 0.9)
            blur_rgb_region(im, (0.060, 0.565, 0.200, 0.635), 3.0)
            blur_rgb_region(im, (0.410, 0.560, 0.515, 0.645), 3.5)

        im = clean_alpha(im)
        im = im.resize(target, Image.Resampling.LANCZOS)
        im = clean_alpha(im)
        im = seal_opaque_equipment_surface(im)

        # Canonical transparent pixels carry black RGB to avoid colored mip halos.
        px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                r, g, b, a = px[x, y]
                if a == 0:
                    px[x, y] = (0, 0, 0, 0)

        im.save(OUT / f"{face}.png", optimize=True)


if __name__ == "__main__":
    main()
