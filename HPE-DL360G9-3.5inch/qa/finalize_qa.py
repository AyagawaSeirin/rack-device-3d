#!/usr/bin/env python3
"""Build final contact sheets, comparison inputs, and viewer-load audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "qa"
NEUTRAL = (223, 227, 230)
VIEWS = [
    "front", "rear", "left", "right", "top", "bottom",
    "front-left", "front-right", "rear-left", "rear-right",
]
ORTHO = VIEWS[:6]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def device_bbox(render: Image.Image) -> tuple[int, int, int, int]:
    rgb = np.asarray(render.convert("RGB"), dtype=np.int16)
    bg = rgb[0, 0]
    mask = np.max(np.abs(rgb - bg), axis=2) > 12
    labels, count = ndimage.label(mask)
    if count == 0:
        raise ValueError("render contains no non-background object")
    sizes = np.bincount(labels.ravel())
    sizes[0] = 0
    keep = labels == int(np.argmax(sizes))
    ys, xs = np.where(keep)
    return int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)


def rgba_subject(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGBA")
    alpha = np.asarray(image.getchannel("A"))
    if np.any(alpha < 255):
        bbox = image.getchannel("A").getbbox()
        if bbox is None:
            raise ValueError(f"empty alpha subject: {path}")
        return image.crop(bbox)

    rgb = np.asarray(image.convert("RGB"), dtype=np.int16)
    corners = np.stack((rgb[0, 0], rgb[0, -1], rgb[-1, 0], rgb[-1, -1]))
    bg = np.median(corners, axis=0)
    candidate = np.max(np.abs(rgb - bg), axis=2) <= 22
    labels, _ = ndimage.label(candidate)
    border_labels = np.unique(np.concatenate((labels[0], labels[-1], labels[:, 0], labels[:, -1])))
    background = np.isin(labels, border_labels[border_labels != 0])
    subject = ~background
    subject = ndimage.binary_closing(subject, iterations=1)
    subject = ndimage.binary_fill_holes(subject)
    ys, xs = np.where(subject)
    if not len(xs):
        raise ValueError(f"could not isolate subject: {path}")
    x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)
    array = np.asarray(image).copy()
    array[:, :, 3] = np.where(subject, 255, 0).astype(np.uint8)
    return Image.fromarray(array).crop((x0, y0, x1, y1))


def reference_canvas(source_path: Path, render_path: Path, output_path: Path) -> None:
    render = Image.open(render_path).convert("RGB")
    source = rgba_subject(source_path)
    x0, y0, x1, y1 = device_bbox(render)
    target_w, target_h = x1 - x0, y1 - y0
    scale = min(target_w / source.width, target_h / source.height)
    resized = source.resize(
        (max(1, round(source.width * scale)), max(1, round(source.height * scale))),
        Image.Resampling.LANCZOS,
    )
    canvas = Image.new("RGBA", render.size, (*NEUTRAL, 255))
    px = x0 + (target_w - resized.width) // 2
    py = y0 + (target_h - resized.height) // 2
    canvas.alpha_composite(resized, (px, py))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output_path)


def contact_sheet(engine: str, profile: str) -> None:
    folder = QA / f"viewer-{engine}"
    cell_w, cell_h, label_h = 480, 360, 44
    margin = 8
    canvas = Image.new("RGB", (5 * (cell_w + margin) + margin, 2 * (cell_h + label_h + margin) + margin), NEUTRAL)
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default(size=20)
    for index, view in enumerate(VIEWS):
        row, col = divmod(index, 5)
        image = Image.open(folder / f"{profile}-{view}.png").convert("RGB")
        image.thumbnail((cell_w, cell_h), Image.Resampling.LANCZOS)
        x = margin + col * (cell_w + margin) + (cell_w - image.width) // 2
        y = margin + row * (cell_h + label_h + margin) + (cell_h - image.height) // 2
        canvas.paste(image, (x, y))
        label = f"{profile}-{view}"
        label_box = draw.textbbox((0, 0), label, font=font)
        draw.text((margin + col * (cell_w + margin) + (cell_w - (label_box[2] - label_box[0])) // 2,
                   margin + row * (cell_h + label_h + margin) + cell_h + 8), label, fill=(30, 34, 38), font=font)
    out = QA / "contact-sheets" / f"viewer-{engine}-{profile}-10views.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out)


def alpha_review() -> dict:
    result = {"faces": {}, "status": "PASS"}
    for face in ORTHO:
        alpha = np.asarray(Image.open(ROOT / "views" / f"{face}.png").convert("RGBA").getchannel("A"))
        ys, xs = np.where(alpha > 0)
        x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)
        crop = alpha[y0:y1, x0:x1]
        zero = crop == 0
        labels, count = ndimage.label(zero)
        internal = []
        for label in range(1, count + 1):
            yy, xx = np.where(labels == label)
            touches = bool(np.any(xx == 0) or np.any(xx == crop.shape[1] - 1) or np.any(yy == 0) or np.any(yy == crop.shape[0] - 1))
            if not touches:
                internal.append({"pixels": int(len(xx)), "bbox": [int(xx.min()), int(yy.min()), int(xx.max() + 1), int(yy.max() + 1)]})
        core = crop[max(1, crop.shape[0] // 10):-max(1, crop.shape[0] // 10),
                    max(1, crop.shape[1] // 10):-max(1, crop.shape[1] // 10)]
        row = {
            "content_bbox_px": [x0, y0, x1, y1],
            "core_alpha_below_250_percent": float(np.mean(core < 250) * 100.0) if core.size else 0.0,
            "internal_fully_transparent_components": internal,
            "review": "external silhouette/antialias only" if not internal and not np.any(core < 250) else "REVIEW",
        }
        if row["review"] != "external silhouette/antialias only":
            result["status"] = "FAIL"
        result["faces"][face] = row
    return result


def main() -> None:
    model_paths = {
        "standard": ROOT / "model/HPE-DL360G9-3.5inch.glb",
        "web": ROOT / "model/HPE-DL360G9-3.5inch-web.glb",
    }
    audit = {"required_view_count": 40, "dark_background_count": 4, "source_camera_count": 6, "models": {}, "captures": [], "supplemental_captures": [], "errors": []}
    for profile, model_path in model_paths.items():
        audit["models"][profile] = {
            "path": str(model_path.relative_to(ROOT)), "bytes": model_path.stat().st_size,
            "sha256": sha256(model_path), "mtime_ns": model_path.stat().st_mtime_ns,
        }

    for engine in ("threejs", "babylonjs"):
        for profile in ("standard", "web"):
            contact_sheet(engine, profile)
            for view in VIEWS:
                path = QA / f"viewer-{engine}" / f"{profile}-{view}.png"
                row = {"engine": engine, "profile": profile, "view": view, "path": str(path.relative_to(ROOT))}
                if not path.exists():
                    audit["errors"].append(f"missing {row['path']}")
                else:
                    row.update({"bytes": path.stat().st_size, "sha256": sha256(path), "mtime_ns": path.stat().st_mtime_ns,
                                "newer_than_model": path.stat().st_mtime_ns >= model_paths[profile].stat().st_mtime_ns})
                    if not row["newer_than_model"]:
                        audit["errors"].append(f"stale {row['path']}")
                audit["captures"].append(row)

            dark = QA / f"viewer-{engine}" / f"{profile}-front-dark.png"
            dark_row = {"engine": engine, "profile": profile, "view": "front-dark", "path": str(dark.relative_to(ROOT))}
            if not dark.exists():
                audit["errors"].append(f"missing {dark_row['path']}")
            else:
                dark_row.update({"bytes": dark.stat().st_size, "sha256": sha256(dark), "mtime_ns": dark.stat().st_mtime_ns,
                                 "newer_than_model": dark.stat().st_mtime_ns >= model_paths[profile].stat().st_mtime_ns})
                if not dark_row["newer_than_model"]:
                    audit["errors"].append(f"stale {dark_row['path']}")
            audit["supplemental_captures"].append(dark_row)

        for face in ORTHO:
            reference_canvas(ROOT / "views" / f"{face}.png", QA / f"viewer-{engine}" / f"standard-{face}.png",
                             QA / "comparisons/reference-canvas" / f"{engine}-{face}.png")

    source_cameras = {
        "pios-front-high": (ROOT / "source/third-party/pios-15304-1.jpg", "source-front-high"),
        "pios-rear-high": (ROOT / "source/third-party/pios-15304-2.jpg", "source-rear-high"),
        "servak-rear-high": (ROOT / "source/third-party/servak-dl360g9-lff4.jpg", "source-rear-high"),
        "newserverlife-front-low": (ROOT / "source/third-party/newserverlife-dl360-g9-4lff.png", "source-front-low"),
    }
    for engine in ("threejs", "babylonjs"):
        for label, (source_path, view) in source_cameras.items():
            render = QA / f"viewer-{engine}" / f"standard-{view}.png"
            output = QA / "comparisons/source-camera-reference" / f"{engine}-{label}.png"
            reference_canvas(source_path, render, output)
        for view in ("source-front-high", "source-rear-high", "source-front-low"):
            path = QA / f"viewer-{engine}" / f"standard-{view}.png"
            row = {"engine": engine, "profile": "standard", "view": view, "path": str(path.relative_to(ROOT))}
            if not path.exists():
                audit["errors"].append(f"missing {row['path']}")
            else:
                row.update({"bytes": path.stat().st_size, "sha256": sha256(path), "mtime_ns": path.stat().st_mtime_ns,
                            "newer_than_model": path.stat().st_mtime_ns >= model_paths["standard"].stat().st_mtime_ns})
                if not row["newer_than_model"]:
                    audit["errors"].append(f"stale {row['path']}")
            audit["supplemental_captures"].append(row)

    audit["actual_required_view_count"] = len(audit["captures"])
    audit["actual_dark_background_count"] = sum(row["view"] == "front-dark" for row in audit["supplemental_captures"])
    audit["actual_source_camera_count"] = sum(row["view"].startswith("source-") for row in audit["supplemental_captures"])
    audit["status"] = "PASS" if (not audit["errors"] and len(audit["captures"]) == 40
                                   and audit["actual_dark_background_count"] == 4
                                   and audit["actual_source_camera_count"] == 6) else "FAIL"
    (QA / "viewer-load-audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    alpha = alpha_review()
    (QA / "alpha-review.json").write_text(json.dumps(alpha, indent=2), encoding="utf-8")
    print(json.dumps({"status": audit["status"], "captures": len(audit["captures"]), "errors": audit["errors"]}, indent=2))


if __name__ == "__main__":
    main()
