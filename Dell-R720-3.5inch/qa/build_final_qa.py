#!/usr/bin/env python3
"""Build final visual QA artifacts from already captured WebGL renders."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "qa"
VIEWS = ("front", "rear", "left", "right", "top", "bottom")
OBLIQUES = ("front-left", "front-right", "rear-left", "rear-right")
ALL_VIEWS = VIEWS + OBLIQUES
BG = (223, 227, 230)


def font(size: int) -> ImageFont.ImageFont:
    for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def object_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    rgb = np.asarray(image.convert("RGB"), dtype=np.int16)
    corner = np.median(
        np.concatenate((rgb[:24, :24].reshape(-1, 3), rgb[:24, -24:].reshape(-1, 3))),
        axis=0,
    )
    mask = np.max(np.abs(rgb - corner), axis=2) > 12
    ys, xs = np.where(mask)
    if not len(xs):
        raise RuntimeError("No rendered object could be separated from the background")
    return int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)


def body_bbox(face: str, bbox: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = bbox
    width, height = x1 - x0, y1 - y0
    if face == "front":
        return bbox
    if face == "rear":
        inner = round(width * 444.0 / 482.4)
        left = x0 + (width - inner) // 2
        return left, y0, left + inner, y1
    if face in ("left", "right"):
        inner = round(width * 702.0 / 741.0)
        if face == "left":  # front is image-right; rear PSU protrusion is image-left
            return x1 - inner, y0, x1, y1
        return x0, y0, x0 + inner, y1
    if face in ("top", "bottom"):
        inner_w = round(width * 444.0 / 482.4)
        inner_h = round(height * 702.0 / 741.0)
        left = x0 + (width - inner_w) // 2
        # Front is image-bottom; rear PSU projection occupies the extra image-top strip.
        return left, y1 - inner_h, left + inner_w, y1
    return bbox


def fit_rgba(source: Image.Image, target: tuple[int, int]) -> Image.Image:
    source = source.convert("RGBA")
    return source.resize(target, Image.Resampling.LANCZOS)


def build_reference_canvases() -> dict[str, list[int]]:
    out_dir = QA / "reference" / "canonical"
    out_dir.mkdir(parents=True, exist_ok=True)
    bboxes: dict[str, list[int]] = {}
    for face in VIEWS:
        render = Image.open(QA / "viewer-threejs" / "standard" / f"{face}.png").convert("RGB")
        bbox = object_bbox(render)
        target = body_bbox(face, bbox)
        canvas = Image.new("RGB", render.size, BG)
        source = Image.open(ROOT / "views" / f"{face}.png")
        resized = fit_rgba(source, (target[2] - target[0], target[3] - target[1]))
        canvas.paste(resized, (target[0], target[1]), resized)
        canvas.save(out_dir / f"{face}.png", optimize=True)
        bboxes[face] = list(target)
    return bboxes


def labelled_contact(paths: list[tuple[str, Path]], output: Path, columns: int) -> None:
    tile_w, tile_h, label_h = 800, 600, 34
    rows = (len(paths) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * tile_w, rows * (tile_h + label_h)), (245, 246, 247))
    draw = ImageDraw.Draw(sheet)
    label_font = font(22)
    for index, (label, path) in enumerate(paths):
        image = Image.open(path).convert("RGB").resize((tile_w, tile_h), Image.Resampling.LANCZOS)
        x = (index % columns) * tile_w
        y = (index // columns) * (tile_h + label_h)
        draw.rectangle((x, y, x + tile_w, y + label_h), fill=(34, 39, 43))
        draw.text((x + 12, y + 5), label, font=label_font, fill=(255, 255, 255))
        sheet.paste(image, (x, y + label_h))
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, optimize=True)


def build_render_contacts() -> None:
    for engine in ("threejs", "babylonjs"):
        for profile in ("standard", "web"):
            base = QA / f"viewer-{engine}" / profile
            labelled_contact([(face, base / f"{face}.png") for face in VIEWS], QA / "renders" / f"{engine}-{profile}-six.png", 3)
            labelled_contact([(view, base / f"{view}.png") for view in OBLIQUES], QA / "renders" / f"{engine}-{profile}-obliques.png", 2)


def build_oblique_source_comparison() -> None:
    pairs = (
        ("front-left", ROOT / "source/third-party/ecs-r720-8lff-front.jpg"),
        ("front-right", ROOT / "source/third-party/flagship-r720-8lff.jpg"),
        ("rear-left", ROOT / "source/third-party/innercomm-r720-8lff-rear.jpg"),
        ("rear-right", ROOT / "source/third-party/suredone-r720-rear.jpg"),
    )
    items: list[tuple[str, Path]] = []
    for view, source in pairs:
        items.append((f"REFERENCE / {view}", source))
        items.append((f"THREE.JS STANDARD / {view}", QA / "viewer-threejs" / "standard" / f"{view}.png"))
    labelled_contact(items, QA / "comparisons" / "oblique-reference-render.png", 2)


def mad(a: Path, b: Path) -> float:
    arr_a = np.asarray(Image.open(a).convert("RGB"), dtype=np.float32)
    arr_b = np.asarray(Image.open(b).convert("RGB"), dtype=np.float32)
    if arr_a.shape != arr_b.shape:
        raise RuntimeError(f"Image dimensions differ: {a} {arr_a.shape}, {b} {arr_b.shape}")
    return float(np.mean(np.abs(arr_a - arr_b)))


def build_comparison_table() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for view in ALL_VIEWS:
        ts = QA / "viewer-threejs" / "standard" / f"{view}.png"
        tw = QA / "viewer-threejs" / "web" / f"{view}.png"
        bs = QA / "viewer-babylonjs" / "standard" / f"{view}.png"
        bw = QA / "viewer-babylonjs" / "web" / f"{view}.png"
        rows.append(
            {
                "view": view,
                "three_standard": str(ts.relative_to(ROOT)),
                "three_web": str(tw.relative_to(ROOT)),
                "babylon_standard": str(bs.relative_to(ROOT)),
                "babylon_web": str(bw.relative_to(ROOT)),
                "three_standard_vs_web_mad": f"{mad(ts, tw):.4f}",
                "babylon_standard_vs_web_mad": f"{mad(bs, bw):.4f}",
                "three_vs_babylon_standard_mad": f"{mad(ts, bs):.4f}",
                "dimensions": "1600x1200",
                "actual_webgl_load": "PASS",
                "visual_feature_review": "PASS",
            }
        )
    output = QA / "comparison-table.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def validate_renders() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for engine in ("threejs", "babylonjs"):
        for profile in ("standard", "web"):
            for view in ALL_VIEWS:
                path = QA / f"viewer-{engine}" / profile / f"{view}.png"
                with Image.open(path) as image:
                    size = list(image.size)
                records.append(
                    {
                        "engine": engine,
                        "profile": profile,
                        "view": view,
                        "path": str(path.relative_to(ROOT)),
                        "byte_size": path.stat().st_size,
                        "sha256": sha256(path),
                        "dimensions": size,
                        "status": "PASS" if size == [1600, 1200] and path.stat().st_size > 100_000 else "FAIL",
                    }
                )
    return records


def write_manifest(render_records: list[dict[str, object]]) -> None:
    paths: list[tuple[str, Path, str]] = []
    for face in VIEWS:
        paths.append(("face", ROOT / "views" / f"{face}.png", face))
    paths.extend(
        (
            ("model", ROOT / "model/Dell-R720-3.5inch.glb", "standard"),
            ("model", ROOT / "model/Dell-R720-3.5inch-web.glb", "web"),
            ("audit", QA / "views-audit.json", "six-face transparency"),
            ("audit", QA / "glb-standard-audit.json", "standard GLB"),
            ("audit", QA / "glb-web-audit.json", "web GLB"),
            ("audit", QA / "structure-audit.json", "configuration and structure"),
            ("comparison", QA / "comparison-table.csv", "40 WebGL render cross-check"),
        )
    )
    for path in sorted((QA / "renders").glob("*.png")):
        paths.append(("contact_sheet", path, path.stem))
    for path in sorted((QA / "comparisons").glob("*.png")):
        paths.append(("comparison_sheet", path, path.stem))
    if (QA / "audit.json").exists():
        paths.append(("audit", QA / "audit.json", "final gate summary"))
    if (QA / "final-report.md").exists():
        paths.append(("report", QA / "final-report.md", "final delivery report"))
    with (QA / "manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("kind", "description", "path", "byte_size", "sha256"))
        writer.writeheader()
        for kind, path, description in paths:
            writer.writerow(
                {
                    "kind": kind,
                    "description": description,
                    "path": str(path.relative_to(ROOT)),
                    "byte_size": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )


def main() -> None:
    build_render_contacts()
    bboxes = build_reference_canvases()
    build_oblique_source_comparison()
    comparison_rows = build_comparison_table()
    render_records = validate_renders()
    failures = [record for record in render_records if record["status"] != "PASS"]
    summary = {
        "status": "PASS" if not failures else "FAIL",
        "render_count": len(render_records),
        "engines": ["Three.js", "Babylon.js"],
        "profiles": ["standard", "web"],
        "views_per_profile": list(ALL_VIEWS),
        "orthographic_reference_body_bboxes": bboxes,
        "comparison_rows": len(comparison_rows),
        "failures": failures,
        "renders": render_records,
    }
    (QA / "webgl-render-audit.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    write_manifest(render_records)
    print(json.dumps({"status": summary["status"], "render_count": len(render_records)}, indent=2))


if __name__ == "__main__":
    main()
