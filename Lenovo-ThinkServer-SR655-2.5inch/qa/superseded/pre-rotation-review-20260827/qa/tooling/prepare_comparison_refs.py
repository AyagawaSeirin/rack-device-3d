from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
BG = np.array([238, 240, 242], dtype=np.uint8)
VIEWS = ("front", "rear", "right", "left", "top", "bottom", "frontRight", "rearRight")


def render_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    a = np.asarray(image.convert("RGB"), dtype=np.int16)
    delta = np.max(np.abs(a - BG.astype(np.int16)), axis=2)
    ys, xs = np.where(delta > 8)
    return int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)


def source_asset(view: str) -> Image.Image:
    if view in {"front", "rear", "right", "left", "top", "bottom"}:
        return Image.open(ROOT / "views" / f"{view}.png").convert("RGBA")
    path = ROOT / "qa" / "reference" / f"official-viewer-{view.replace('Right', '-right')}-crop.png"
    image = Image.open(path).convert("RGBA")
    rgb = np.asarray(image.convert("RGB"))
    mask = np.any(rgb < 247, axis=2)
    ys, xs = np.where(mask)
    return image.crop((int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)))


def place_reference(source: Image.Image, canvas_size, bbox, preserve_aspect: bool) -> Image.Image:
    canvas = Image.new("RGB", canvas_size, tuple(BG.tolist()))
    target_w, target_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    if preserve_aspect:
        ratio = min(target_w / source.width, target_h / source.height)
        size = (max(1, round(source.width * ratio)), max(1, round(source.height * ratio)))
        placed = source.resize(size, Image.Resampling.LANCZOS)
        x = bbox[0] + (target_w - size[0]) // 2
        y = bbox[1] + (target_h - size[1]) // 2
    else:
        placed = source.resize((target_w, target_h), Image.Resampling.LANCZOS)
        x, y = bbox[0], bbox[1]
    if placed.mode == "RGBA":
        canvas.paste(placed.convert("RGB"), (x, y), placed.getchannel("A"))
    else:
        canvas.paste(placed, (x, y))
    return canvas


def main() -> None:
    for engine in ("three-standard", "babylon-web"):
        out_dir = ROOT / "qa" / "reference" / "compare" / engine
        out_dir.mkdir(parents=True, exist_ok=True)
        for view in VIEWS:
            render = Image.open(ROOT / "qa" / "renders" / engine / f"{view}.png").convert("RGB")
            bbox = render_bbox(render)
            source = source_asset(view)
            ref = place_reference(source, render.size, bbox, preserve_aspect=view in {"frontRight", "rearRight"})
            ref.save(out_dir / f"{view}.png", optimize=True)


if __name__ == "__main__":
    main()
