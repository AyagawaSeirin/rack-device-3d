#!/usr/bin/env python3
"""Build compact contact sheets only from the current frozen C6320 evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


REVIEW = Path(__file__).resolve().parent.parent
FINAL = REVIEW / "final"
ROTATION = REVIEW / "after" / "evidence" / "rotation"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sheet(paths: list[Path], output: Path, title: str, columns: int) -> dict:
    thumb_size = (240, 180)
    label_height = 22
    title_height = 30
    rows = (len(paths) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * thumb_size[0], title_height + rows * (thumb_size[1] + label_height)), (25, 29, 34))
    draw = ImageDraw.Draw(canvas)
    draw.text((8, 8), title, fill=(245, 247, 249))
    for index, path in enumerate(paths):
        image = Image.open(path).convert("RGB")
        image.thumbnail(thumb_size, Image.Resampling.LANCZOS)
        x = (index % columns) * thumb_size[0] + (thumb_size[0] - image.width) // 2
        y = title_height + (index // columns) * (thumb_size[1] + label_height)
        canvas.paste(image, (x, y))
        draw.text(((index % columns) * thumb_size[0] + 6, y + thumb_size[1] + 4), path.stem, fill=(230, 233, 236))
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, optimize=True)
    return {"path": str(output.relative_to(REVIEW)), "sha256": sha(output), "sourceCount": len(paths)}


def main() -> None:
    frozen = json.loads((FINAL / "frozen-hashes.json").read_text())
    loads_root = FINAL / "static-40-loads"
    records = []
    for engine in ("three", "babylon"):
        for variant in ("standard", "web"):
            out = FINAL / "contact-sheets" / f"{engine}-{variant}"
            combo = ROTATION / engine / variant
            expected = frozen["standardGlb" if variant == "standard" else "webGlb"]["sha256"]
            manifest = json.loads((combo / "rotation-manifest.json").read_text())
            load_manifest = json.loads((loads_root / engine / variant / "load-manifest.json").read_text())
            if manifest["modelSha256"] != expected or any(item["modelSha256"] != expected for item in load_manifest["loads"]):
                raise RuntimeError(f"evidence hash mismatch: {engine}/{variant}")
            records.append(sheet(sorted((combo / "yaw").glob("*.png")), out / "yaw-72.png", f"{engine}/{variant}: 72 x 5-degree yaw; frozen {expected[:16]}", 12))
            records.append(sheet(sorted((combo / "pitch").glob("*.png")), out / "pitch-16.png", f"{engine}/{variant}: four yaws x four pitches", 4))
            records.append(sheet(sorted((loads_root / engine / variant).glob("[0-9][0-9]-*.png")), out / "loads-10.png", f"{engine}/{variant}: 10 cache-busted independent loads", 5))
    result = {"model": "Dell-C6320-2.5inch", "frozenAt": frozen["frozenAt"], "sheetCount": len(records), "records": records}
    (FINAL / "contact-sheets" / "manifest.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"model": result["model"], "sheetCount": result["sheetCount"]}, indent=2))


if __name__ == "__main__":
    main()
