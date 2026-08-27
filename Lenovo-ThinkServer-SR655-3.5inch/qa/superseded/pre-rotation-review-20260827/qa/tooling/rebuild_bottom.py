from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]


def bbox_from_alpha(image: Image.Image, threshold: int = 12) -> tuple[int, int, int, int]:
    alpha = np.asarray(image.getchannel("A"))
    ys, xs = np.nonzero(alpha > threshold)
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def main() -> None:
    # Exact geometry and seam paths come from the public Lenovo SR655 viewer.
    official_path = ROOT / "qa/reference/official-viewer-bottom-rectified.png"
    official_landscape = Image.open(official_path).convert("RGB")
    scan = np.asarray(official_landscape).astype(np.float32)
    scan_mask = (255.0 - scan.min(axis=2)) > 5.0
    row_counts = scan_mask.sum(axis=1)
    col_counts = scan_mask.sum(axis=0)
    ys = np.where(row_counts > official_landscape.width * 0.03)[0]
    xs = np.where(col_counts > official_landscape.height * 0.03)[0]
    official_landscape = official_landscape.crop((int(xs[0]), int(ys[0]), int(xs[-1]) + 1, int(ys[-1]) + 1))
    official = official_landscape.rotate(90, expand=True)
    rgb = np.asarray(official).astype(np.float32)
    distance_from_white = 255.0 - rgb.min(axis=2)
    alpha = np.clip((distance_from_white - 2.0) * 18.0, 0.0, 255.0).astype(np.uint8)
    official_rgba = Image.fromarray(np.dstack([rgb.astype(np.uint8), alpha]), "RGBA")
    official_rgba = official_rgba.crop(bbox_from_alpha(official_rgba))

    # The required built-in imagegen call remains the material/style source.
    # Sample a seam-free lower region from that generated bottom and blend its
    # real-looking galvanized grain over the exact official geometry.
    generated_path = ROOT / "qa/imagegen-output/bottom-alpha-initial.png"
    generated = Image.open(generated_path).convert("RGBA")
    generated = generated.crop(bbox_from_alpha(generated))
    gw, gh = generated.size
    patch = generated.crop((int(gw * 0.12), int(gh * 0.66), int(gw * 0.88), int(gh * 0.93))).convert("RGB")
    patch = patch.resize(official_rgba.size, Image.Resampling.LANCZOS)
    generated_alpha = generated.getchannel("A").resize(official_rgba.size, Image.Resampling.LANCZOS)

    base = np.asarray(official_rgba).copy()
    grain = np.asarray(patch).astype(np.float32)
    base_rgb = base[..., :3].astype(np.float32)
    mixed = np.clip(base_rgb * 0.72 + grain * 0.28, 0, 255).astype(np.uint8)
    base[..., :3] = mixed
    # The official light-gray render is close to its white background, so its
    # luminance mask alone can create false internal holes. Union it with the
    # already validated imagegen silhouette; this changes no visible geometry.
    base[..., 3] = np.maximum(
        np.asarray(official_rgba.getchannel("A")),
        np.asarray(generated_alpha),
    )
    result = Image.fromarray(base, "RGBA")
    result = result.resize((1512, 2600), Image.Resampling.LANCZOS)

    # Opaque core; only the external silhouette remains antialiased.
    arr = np.asarray(result).copy()
    a = arr[..., 3]
    positive = a > 0
    interior = positive.copy()
    interior[1:, :] &= positive[:-1, :]
    interior[:-1, :] &= positive[1:, :]
    interior[:, 1:] &= positive[:, :-1]
    interior[:, :-1] &= positive[:, 1:]
    a[interior] = 255
    arr[..., 3] = a
    result = Image.fromarray(arr, "RGBA")
    result.save(ROOT / "views/bottom.png", optimize=True)
    print("bottom", result.size, bbox_from_alpha(result))


if __name__ == "__main__":
    main()
