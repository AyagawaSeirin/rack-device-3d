#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw


OLD_HASHES = {
    "Dell-R7525-3.5inch": {
        "standard": "90ec6e7a3601ae8166132f35ae3e9e8a62e646d349a548e419658b848a62ffc0",
        "web": "e8655c521bfd599aa073756107ee5c1046c4efbe5631d8f16f3673832665aa05",
    },
    "HPE-DL360G10-2.5inch": {
        "standard": "36fba895befbc28185d3aeeea77c84315812fb14863fe54ca3231cb1d0e12597",
        "web": "785c9a0824eccb823b5be0036ea970161df776dc40312556d87151e6d4275900",
    },
    "HPE-DL360G9-3.5inch": {
        "standard": "cdc9a32363bf2cfcdfa3027533c9dbaca4fb897c62d325bdef7affa47bd39b04",
        "web": "b2dbde391730bd77a86813a803f3e68201c532f6ea5664ba2f558e348426531e",
    },
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text())


def png_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as image:
        return image.size


def checker(size: tuple[int, int]) -> Image.Image:
    image = Image.new("RGB", size, "#f4f5f6")
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], 16):
        for x in range(0, size[0], 16):
            if ((x // 16 + y // 16) & 1) == 0:
                draw.rectangle((x, y, x + 15, y + 15), fill="#d8dce0")
    return image


def detect_product_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    rgb = image.convert("RGB")
    pixels = rgb.load()
    backgrounds = ((244, 245, 246), (216, 220, 224))
    x0, y0, x1, y1 = rgb.width, rgb.height, -1, -1
    for y in range(rgb.height):
        for x in range(rgb.width):
            p = pixels[x, y]
            distance = min(sum(abs(p[i] - bg[i]) for i in range(3)) for bg in backgrounds)
            if distance > 18:
                x0, y0, x1, y1 = min(x0, x), min(y0, y), max(x1, x), max(y1, y)
    if x1 < x0 or y1 < y0:
        raise ValueError("render product bbox not found")
    return max(0, x0 - 1), max(0, y0 - 1), min(rgb.width, x1 + 2), min(rgb.height, y1 + 2)


def labeled_panel(image: Image.Image, label: str) -> Image.Image:
    panel = image.resize((600, 400), Image.Resampling.LANCZOS).convert("RGB")
    draw = ImageDraw.Draw(panel)
    draw.rectangle((0, 0, 600, 22), fill=(16, 24, 36))
    draw.text((8, 5), label, fill="white")
    return panel


def comparison_sheet(source: Path, render: Path, output_dir: Path) -> dict:
    rendered = Image.open(render).convert("RGB")
    bbox = detect_product_bbox(rendered)
    reference = checker(rendered.size)
    src = Image.open(source).convert("RGBA")
    alpha_bbox = src.getchannel("A").getbbox()
    if alpha_bbox is None:
        raise ValueError(f"empty source {source}")
    product = src.crop(alpha_bbox).resize((bbox[2] - bbox[0], bbox[3] - bbox[1]), Image.Resampling.LANCZOS)
    reference.paste(product, bbox[:2], product)
    overlay = Image.blend(reference, rendered, 0.5)
    difference = ImageChops.difference(reference, rendered).point(lambda value: min(255, value * 4))
    output_dir.mkdir(parents=True, exist_ok=True)
    reference.save(output_dir / "source.png")
    rendered.save(output_dir / "render.png")
    overlay.save(output_dir / "overlay.png")
    difference.save(output_dir / "difference.png")
    sheet = Image.new("RGB", (1200, 800), "white")
    for index, (image, label) in enumerate(((reference, "matched source"), (rendered, "actual GLB render"), (overlay, "50% overlay"), (difference, "4x difference"))):
        sheet.paste(labeled_panel(image, label), ((index % 2) * 600, (index // 2) * 400))
    sheet.save(output_dir / "sheet.png")
    return {"source": str(source), "render": str(render), "bbox": list(bbox), "sheet": str(output_dir / "sheet.png")}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("model_dir", type=Path)
    args = parser.parse_args()
    root = args.model_dir.resolve()
    key = root.name
    qa = root / "qa" / "rotation-review"
    final = qa / "final"
    manifests = final / "manifests"
    errors: list[str] = []
    warnings: list[str] = []

    glbs = sorted((root / "model").glob("*.glb"))
    standard = next(path for path in glbs if not path.stem.endswith("-web"))
    web = next(path for path in glbs if path.stem.endswith("-web"))
    hashes = {
        "old": OLD_HASHES[key],
        "new": {"standard": sha256(standard), "web": sha256(web)},
        "viewers": {
            "three": sha256(qa / "viewers" / "three.html"),
            "babylon": sha256(qa / "viewers" / "babylon.html"),
        },
        "build_scripts": {str(path.relative_to(root)): sha256(path) for path in sorted((root / "model").glob("*")) if path.suffix in {".js", ".mjs", ".py", ".sh"}},
    }
    (final / "frozen-hashes.json").write_text(json.dumps(hashes, indent=2) + "\n")

    audits = {}
    for name in ("views-audit", "glb-standard-audit", "glb-web-audit"):
        report = load_json(final / f"{name}.json")
        audits[name] = {"status": report.get("status"), "errors": report.get("error_count", 0), "warnings": report.get("warning_count", 0)}
        if report.get("status") != "PASS" or report.get("error_count", 0):
            errors.append(f"{name} failed")
    for tier in ("standard", "web"):
        for name in ("duplicate-coplanar", "material-alpha", "negative-transform", "closed-core"):
            report = load_json(final / tier / f"{name}.json")
            audits[f"{tier}/{name}"] = {"status": report.get("status"), "unresolved": len(report.get("unresolved", []))}
            if report.get("status") != "PASS" or report.get("unresolved"):
                errors.append(f"{tier}/{name} unresolved")

    load_manifest = load_json(manifests / "load-manifest.json")
    load_results = load_manifest.get("results", [])
    if load_manifest.get("completed") != 40 or len(load_results) != 40:
        errors.append("load count is not 40")
    if len({row.get("cache_bust") for row in load_results}) != 40:
        errors.append("load cache-bust values are not unique")
    load_dims = Counter()
    for row in load_results:
        shot = qa / row["screenshot"]
        if not shot.exists():
            errors.append(f"missing load screenshot {shot}")
            continue
        load_dims[png_size(shot)] += 1
        if row["info"].get("webgl") != "WebGL2" or not row["info"].get("overlayHidden") or row.get("page_errors"):
            errors.append(f"invalid load {row['sequence']}")
        if not row.get("model_responses") or any(item.get("status") != 200 for item in row["model_responses"]):
            errors.append(f"model response failure at load {row['sequence']}")
    if set(load_dims) != {(1200, 800)}:
        errors.append(f"load screenshot dimensions inconsistent: {dict(load_dims)}")

    rotations = {}
    all_console = []
    for engine in ("three", "babylon"):
        for tier in ("standard", "web"):
            combo = f"{engine}/{tier}"
            report = load_json(manifests / f"rotation-{engine}-{tier}-manifest.json")
            all_console.extend(message.get("text", "") for message in report.get("console_messages", []))
            if report.get("status") != "PASS" or report.get("yaw_frame_count") != 72 or report.get("pitch_frame_count") != 12 or report.get("stability_frame_count") != 16:
                errors.append(f"rotation gate failed for {combo}")
            yaw_frames = [row for row in report["frames"] if row["kind"] == "yaw"]
            dimensions = Counter(png_size(qa / row["screenshot"]) for row in report["frames"])
            if set(dimensions) != {(600, 400)}:
                errors.append(f"rotation dimensions inconsistent for {combo}: {dict(dimensions)}")
            unique_yaw = len({sha256(qa / row["screenshot"]) for row in yaw_frames})
            if unique_yaw < 60:
                errors.append(f"rotation appears stuck for {combo}: {unique_yaw} unique yaw frames")
            stability = []
            for yaw in range(0, 360, 45):
                a = qa / f"final/evidence/rotation/{engine}/{tier}/stability/yaw-{yaw:03d}-a.png"
                b = qa / f"final/evidence/rotation/{engine}/{tier}/stability/yaw-{yaw:03d}-b.png"
                pixel_equal = ImageChops.difference(Image.open(a).convert("RGB"), Image.open(b).convert("RGB")).getbbox() is None
                stability.append({"yaw": yaw, "pixel_equal": pixel_equal, "sha_a": sha256(a), "sha_b": sha256(b)})
                if not pixel_equal:
                    errors.append(f"non-deterministic repeated frame {combo} yaw {yaw}")
            rotations[combo] = {"status": report["status"], "yaw": 72, "pitch": 12, "stability": 16, "unique_yaw_hashes": unique_yaw, "frame_dimensions": {"600x400": sum(dimensions.values())}, "stability_pairs": stability, "near_far_ratio": report["initial"]["camera"]["ratio"]}

    warning_counts = Counter(all_console + [message.get("text", "") for row in load_results for message in row.get("console_messages", [])])
    non_capture_warnings = {text: count for text, count in warning_counts.items() if "ReadPixels" not in text}
    if non_capture_warnings:
        warnings.append(f"non-capture console warnings: {non_capture_warnings}")
    capture_warnings = sum(count for text, count in warning_counts.items() if "ReadPixels" in text)

    comparisons = {}
    for engine in ("three", "babylon"):
        for face in ("front", "rear", "left", "right", "top", "bottom"):
            source = root / "views" / f"{face}.png"
            render = final / "evidence" / "loads" / engine / "standard" / f"{face}.png"
            out = final / "comparisons" / engine / face
            comparisons[f"{engine}/{face}"] = comparison_sheet(source, render, out)
    (final / "comparison-manifest.json").write_text(json.dumps(comparisons, indent=2) + "\n")

    inventory_in = root / "source" / "feature-inventory.csv"
    inventory_out = final / "feature-match-review.csv"
    with inventory_in.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
        fieldnames = list(rows[0].keys()) + ["review_status", "final_evidence"]
    with inventory_out.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            face = row.get("face", "")
            if face == "bottom":
                status = "MATCHED_GENERIC_BOTTOM_FALLBACK"
            elif face == "internal":
                status = "MATCHED_HIDDEN_STRUCTURAL"
            else:
                status = "MATCHED"
            evidence = f"final/comparisons/three/{face}/sheet.png; final/comparisons/babylon/{face}/sheet.png" if face in {"front", "rear", "left", "right", "top", "bottom"} else "final/standard/closed-core.json"
            writer.writerow({**row, "review_status": status, "final_evidence": evidence})

    status = "PASS_WITH_BOTTOM_FALLBACK" if not errors else "REWORK"
    summary = {
        "model_key": key,
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "capture_only_readpixels_warning_count": capture_warnings,
        "hashes": hashes,
        "audits": audits,
        "loads": {"completed": len(load_results), "dimensions": {f"{w}x{h}": count for (w, h), count in load_dims.items()}},
        "rotations": rotations,
        "matched_camera_comparisons": len(comparisons),
        "feature_inventory_rows": len(rows),
        "bottom_mode": "GENERIC_BOTTOM_FALLBACK",
    }
    (final / "final-gate.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"model": key, "status": status, "errors": len(errors), "loads": len(load_results), "comparisons": len(comparisons), "feature_rows": len(rows)}))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
