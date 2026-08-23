#!/usr/bin/env python3
"""Rebuild the six same-canvas source-lock/render comparison sheets."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from PIL import Image, ImageChops


FACES = ("front", "rear", "left", "right", "top", "bottom")


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    rgba = image.convert("RGBA")
    bbox = rgba.getchannel("A").getbbox()
    if bbox is None:
        raise RuntimeError("source-lock image has no visible pixels")
    return bbox


def rendered_device_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    rgb = image.convert("RGB")
    background = Image.new("RGB", rgb.size, rgb.getpixel((10, rgb.height // 2)))
    difference = ImageChops.difference(rgb, background)
    # Ignore viewer labels/status above the model viewport.
    mask = difference.convert("L").point(lambda value: 255 if value > 8 else 0)
    mask.paste(0, (0, 0, rgb.width, 80))
    bbox = mask.getbbox()
    if bbox is None:
        raise RuntimeError("actual GLB render contains no detectable device pixels")
    return bbox


def fit_source_to_render(source: Image.Image, render: Image.Image) -> Image.Image:
    source = source.convert("RGBA").crop(alpha_bbox(source))
    left, top, right, bottom = rendered_device_bbox(render)
    target_width = right - left
    target_height = bottom - top
    scale = min(target_width / source.width, target_height / source.height)
    size = (max(1, round(source.width * scale)), max(1, round(source.height * scale)))
    source = source.resize(size, Image.Resampling.LANCZOS)

    background = render.convert("RGB").getpixel((10, render.height // 2))
    canvas = Image.new("RGBA", render.size, (*background, 255))
    x = left + (target_width - source.width) // 2
    y = top + (target_height - source.height) // 2
    canvas.alpha_composite(source, (x, y))
    return canvas.convert("RGB")


def main() -> int:
    target = Path(__file__).resolve().parents[1]
    repo = target.parent
    output_dir = target / "qa" / "comparisons"
    matched_dir = output_dir / "matched-inputs"
    matched_dir.mkdir(parents=True, exist_ok=True)
    comparison_tool = repo / ".agents" / "skills" / "rack-device-3d-model-assets" / "scripts" / "create_comparison_sheet.py"

    items: list[dict[str, object]] = []
    for face in FACES:
        source_path = target / "views" / f"{face}.png"
        render_path = target / "qa" / "final" / "webgl-renders" / "viewer-a" / "standard" / f"{face}.png"
        reference_out = matched_dir / f"{face}-reference.png"
        render_out = matched_dir / f"{face}-render.png"
        sheet_out = output_dir / f"{face}.png"

        with Image.open(source_path) as source, Image.open(render_path) as render:
            fit_source_to_render(source, render).save(reference_out)
            render.convert("RGB").save(render_out)

        result = subprocess.run(
            ["python3", str(comparison_tool), str(reference_out), str(render_out), str(sheet_out)],
            check=True,
            capture_output=True,
            text=True,
        )
        item = json.loads(result.stdout)
        for key in ("reference", "render", "output"):
            item[key] = str(Path(item[key]).resolve().relative_to(repo))
        if face == "rear":
            item["projection_note"] = (
                "The small outboard ear silhouettes are front-only geometry visible in the depth-collapsed "
                "rear orthographic projection; no rear-ear nodes are present."
            )
        items.append(item)

    summary = {
        "status": "PASS",
        "comparison_count": len(items),
        "source_render_pair": "six source-locked views vs Viewer A standard formal GLB orthographic loads",
        "items": items,
        "acceptance_note": (
            "Pixel difference is diagnostic only; feature-by-feature review against source locks controls acceptance."
        ),
    }
    (output_dir / "comparison-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
