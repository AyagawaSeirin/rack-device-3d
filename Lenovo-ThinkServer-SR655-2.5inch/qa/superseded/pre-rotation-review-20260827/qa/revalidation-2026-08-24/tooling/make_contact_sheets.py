#!/usr/bin/env python3
"""Build review sheets and a simple non-blank audit for the 40 GLB renders."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageStat


ROOT = Path(__file__).resolve().parents[3]
VALIDATION_LABEL = os.environ.get("SR655_REVALIDATION_LABEL", "revalidation-2026-08-24")
OUT = ROOT / "qa" / VALIDATION_LABEL
VIEWS = (
    "front",
    "rear",
    "right",
    "left",
    "top",
    "bottom",
    "frontLeft",
    "frontRight",
    "rearLeft",
    "rearRight",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    sheets = OUT / "contact-sheets"
    sheets.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    records = []
    for loader in ("three", "babylon"):
        for variant in ("standard", "web"):
            canvas = Image.new("RGB", (2560, 656), (34, 37, 41))
            draw = ImageDraw.Draw(canvas)
            for index, view in enumerate(VIEWS):
                path = OUT / "renders" / loader / variant / f"{view}.png"
                image = Image.open(path).convert("RGB")
                if image.size != (1280, 720):
                    raise RuntimeError(f"unexpected render size {image.size}: {path}")
                background = Image.new("RGB", image.size, (238, 240, 242))
                diff = ImageChops.difference(image, background)
                bbox = diff.getbbox()
                stats = ImageStat.Stat(image)
                gray_stats = ImageStat.Stat(image.convert("L"))
                if bbox is None or gray_stats.stddev[0] < 3:
                    raise RuntimeError(f"blank or near-blank render: {path}")
                tile = image.resize((512, 288), Image.Resampling.LANCZOS)
                x = (index % 5) * 512
                y = (index // 5) * 328
                canvas.paste(tile, (x, y + 40))
                draw.rectangle((x, y, x + 511, y + 39), fill=(34, 37, 41))
                draw.text((x + 12, y + 7), view, font=font, fill=(245, 247, 250))
                records.append(
                    {
                        "loader": loader,
                        "variant": variant,
                        "view": view,
                        "path": str(path),
                        "bytes": path.stat().st_size,
                        "sha256": digest(path),
                        "size_px": list(image.size),
                        "rgb_mean": [round(value, 6) for value in stats.mean],
                        "grayscale_stddev": round(gray_stats.stddev[0], 6),
                        "non_background_bbox": list(bbox),
                        "status": "PASS",
                    }
                )
            sheet_path = sheets / f"{loader}-{variant}-10views.png"
            canvas.save(sheet_path, optimize=True)
            print(sheet_path)
    report = {
        "status": "PASS",
        "render_count": len(records),
        "expected_size_px": [1280, 720],
        "blank_or_near_blank_count": 0,
        "records": records,
    }
    (OUT / "render-image-audit.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
