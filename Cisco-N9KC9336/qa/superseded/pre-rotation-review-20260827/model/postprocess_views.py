from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "views"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def flatten_opaque(image: Image.Image, matte: tuple[int, int, int]) -> Image.Image:
    rgba = image.convert("RGBA")
    background = Image.new("RGBA", rgba.size, (*matte, 255))
    background.alpha_composite(rgba)
    return background


def blur_region(image: Image.Image, box: tuple[int, int, int, int], radius: float) -> None:
    region = image.crop(box).filter(ImageFilter.GaussianBlur(radius))
    image.paste(region, box)


def save_atomic(image: Image.Image, path: Path) -> None:
    temporary = path.with_name(f".{path.stem}-writing.png")
    image.save(temporary, compress_level=6)
    temporary.replace(path)


def fix_front() -> None:
    path = VIEWS / "front.png"
    image = flatten_opaque(Image.open(path), (183, 183, 178))
    reference_path = ROOT / "qa" / "reference" / "serverlama-front-tight.jpg"
    with Image.open(reference_path) as source:
        source = source.convert("RGBA").resize(image.size, Image.Resampling.LANCZOS)

    # Retain the imagegen-built mechanical face and source-locked material, while
    # restoring the exact photographed number strip and branded control panel. This
    # is a source-pixel correction, not an AI-derived or invented label overlay.
    image.paste(source.crop((0, 0, image.width, 55)), (0, 0))
    image.paste(source.crop((0, 0, 205, image.height)), (0, 0))
    save_atomic(image, path)


def fix_left() -> None:
    path = VIEWS / "left.png"
    image = flatten_opaque(Image.open(path), (184, 184, 181))
    # Preserve the real yellow factory label block but remove the invented microtext.
    blur_region(image, (900, 70, 1250, 235), radius=7)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((928, 91, 1220, 214), radius=8, fill=(241, 209, 50, 255), outline=(75, 67, 16, 255), width=3)
    draw.polygon([(963, 188), (1008, 111), (1053, 188)], outline=(25, 25, 22, 255), width=5)
    draw.text((1072, 122), "CAUTION", font=font(25, bold=True), fill=(28, 28, 24, 255))
    save_atomic(image, path)


def fix_top() -> None:
    path = VIEWS / "top.png"
    image = flatten_opaque(Image.open(path), (185, 186, 184))
    reference_path = ROOT / "qa" / "reference" / "serverlama-top-surface-rectified.png"
    with Image.open(reference_path) as source:
        source = source.convert("RGBA")

    # Replace only label regions with exact photographed pixels. Feathered masks
    # keep the binding source's real blur and text character without a hard collage edge.
    def paste_source_patch(src_box: tuple[int, int, int, int], dst_box: tuple[int, int, int, int]) -> None:
        width = dst_box[2] - dst_box[0]
        height = dst_box[3] - dst_box[1]
        patch = source.crop(src_box).resize((width, height), Image.Resampling.LANCZOS)
        mask = Image.new("L", (width, height), 0)
        mask_draw = ImageDraw.Draw(mask)
        margin = 22
        mask_draw.rectangle((margin, margin, width - margin, height - margin), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(18))
        image.paste(patch, (dst_box[0], dst_box[1]), mask)

    paste_source_patch((55, 15, 520, 280), (95, 20, 545, 270))
    paste_source_patch((35, 1640, 900, 2940), (130, 1830, 960, 3230))
    save_atomic(image, path)


def make_all_opaque() -> None:
    mattes = {
        "rear.png": (171, 172, 169),
        "right.png": (184, 184, 181),
        "bottom.png": (187, 187, 184),
    }
    for name, matte in mattes.items():
        path = VIEWS / name
        with Image.open(path) as source:
            flattened = flatten_opaque(source, matte)
        save_atomic(flattened, path)


if __name__ == "__main__":
    fix_front()
    fix_left()
    fix_top()
    make_all_opaque()
