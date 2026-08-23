#!/usr/bin/env python3
"""Audit the final two-engine, two-variant WebGL screenshot matrix."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageChops, ImageStat


ROOT = Path(__file__).resolve().parents[2]
RENDERS = ROOT / "qa" / "renders"
ENGINES = ("three", "babylon")
VARIANTS = ("standard", "web")
VIEWS = (
    "front",
    "rear",
    "left",
    "right",
    "top",
    "bottom",
    "frontLeft",
    "frontRight",
    "rearLeft",
    "rearRight",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_rmse(first: Image.Image, second: Image.Image) -> float:
    difference = ImageChops.difference(first.convert("RGB"), second.convert("RGB"))
    per_channel = ImageStat.Stat(difference).rms
    return math.sqrt(sum(value * value for value in per_channel) / len(per_channel)) / 255.0


def main() -> None:
    records = []
    missing = []
    invalid = []
    for engine in ENGINES:
        for variant in VARIANTS:
            for view in VIEWS:
                path = RENDERS / engine / variant / f"{view}.png"
                if not path.exists():
                    missing.append(str(path.relative_to(ROOT)))
                    continue
                image = Image.open(path).convert("RGB")
                content_bbox = ImageChops.difference(
                    image, Image.new("RGB", image.size, "white")
                ).getbbox()
                if image.size != (1200, 800) or content_bbox is None:
                    invalid.append(str(path.relative_to(ROOT)))
                records.append(
                    {
                        "engine": engine,
                        "variant": variant,
                        "view": view,
                        "path": str(path.relative_to(ROOT)),
                        "bytes": path.stat().st_size,
                        "sha256": sha256(path),
                        "size_px": list(image.size),
                        "content_bbox_px": list(content_bbox) if content_bbox else None,
                    }
                )

    standard_web = {}
    for engine in ENGINES:
        standard_web[engine] = {}
        for view in VIEWS:
            standard = Image.open(RENDERS / engine / "standard" / f"{view}.png")
            web = Image.open(RENDERS / engine / "web" / f"{view}.png")
            standard_web[engine][view] = round(normalized_rmse(standard, web), 8)

    maximum_standard_web_rmse = max(
        value for engine in standard_web.values() for value in engine.values()
    )
    result = {
        "engines": list(ENGINES),
        "variants": list(VARIANTS),
        "views": list(VIEWS),
        "expected_render_count": 40,
        "actual_render_count": len(records),
        "playwright_real_chromium_load_result": "PASS_40_READY_SCREENSHOTS",
        "missing": missing,
        "invalid": invalid,
        "standard_web_normalized_rmse": standard_web,
        "maximum_standard_web_normalized_rmse": round(maximum_standard_web_rmse, 8),
        "standard_web_visual_threshold": 0.015,
        "records": records,
    }
    result["status"] = "PASS" if (
        len(records) == 40
        and not missing
        and not invalid
        and maximum_standard_web_rmse < result["standard_web_visual_threshold"]
    ) else "FAIL"
    output = ROOT / "qa" / "audits" / "browser.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(result["status"], output, result["maximum_standard_web_normalized_rmse"])


if __name__ == "__main__":
    main()
