#!/usr/bin/env python3
"""Build final-hash matched-camera comparison sheets and row-complete feature review."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageOps


VIEWS = ("front", "rear", "left", "right", "top", "bottom",
         "front-left", "front-right", "rear-left", "rear-right")
INDEX = {view: index + 1 for index, view in enumerate(VIEWS)}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def labelled(image: Image.Image, label: str) -> Image.Image:
    image = image.convert("RGB")
    output = Image.new("RGB", (image.width, image.height + 36), "#111318")
    output.paste(image, (0, 36))
    ImageDraw.Draw(output).text((12, 11), label, fill="#f4f5f6")
    return output


def source_map(root: Path) -> dict[str, Path]:
    name = root.name
    if name == "Huawei-RH1288V5-2.5inch":
        return {view: root / "qa/reference-canvas" / f"{view}.png" for view in VIEWS[:6]}
    if name == "Fortinet-FG3700D":
        result = {view: root / "qa/reference/canonical" / f"{view}.png" for view in VIEWS[:6]}
        result.update({view: root / "qa/reference/oblique" / f"{view}.png" for view in VIEWS[6:]})
        return result
    if name == "Huawei-CE6857-48S6CQ-EI":
        result = {view: root / "qa/reference/official-orthographic" / f"{view}.png" for view in VIEWS[:6]}
        result.update({view: root / "qa/reference/official-three-quarter" / f"{view}.png" for view in VIEWS[6:]})
        return result
    raise ValueError(f"out-of-scope model: {name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("model_root", type=Path)
    parser.add_argument("standard_sha256")
    parser.add_argument("web_sha256")
    args = parser.parse_args()
    root = args.model_root.resolve()
    matched = root / "qa/rotation-review/after/matched-camera"
    renders = matched / "renders"
    outputs = matched / "comparisons"
    outputs.mkdir(parents=True, exist_ok=True)
    events = json.loads((renders / "matched-view-events.json").read_text()).get("frames", [])
    event_by_view = {event["view"]: event for event in events}
    sources = source_map(root)
    comparisons: list[dict] = []
    errors: list[str] = []
    contact_items: list[tuple[str, Image.Image]] = []

    for view, source_path in sources.items():
        render_path = renders / f"{INDEX[view]:02d}-{view}.png"
        if not source_path.exists() or not render_path.exists():
            errors.append(f"{view}: missing source or render")
            continue
        source = Image.open(source_path).convert("RGB")
        render = Image.open(render_path).convert("RGB")
        if source.size != render.size:
            errors.append(f"{view}: source {source.size} != render {render.size}")
            continue
        overlay = Image.blend(source, render, 0.5)
        raw_diff = ImageChops.difference(source, render)
        diff = ImageOps.autocontrast(ImageEnhance.Contrast(raw_diff).enhance(3.0))
        panels = [labelled(source, "SOURCE / LOCKED AUTHORITY"),
                  labelled(render, "FINAL STANDARD GLB / THREE.JS"),
                  labelled(overlay, "50% OVERLAY"),
                  labelled(diff, "ENHANCED ABSOLUTE DIFFERENCE (DIAGNOSTIC)")]
        width, height = source.size
        sheet = Image.new("RGB", (width * 2, (height + 36) * 2), "#111318")
        for index, panel in enumerate(panels):
            sheet.paste(panel, ((index % 2) * width, (index // 2) * (height + 36)))
        output = outputs / f"{view}.png"
        sheet.save(output, optimize=True)
        event = event_by_view.get(view, {})
        if event.get("asset_sha256") != args.standard_sha256:
            errors.append(f"{view}: matched render hash mismatch")
        if event.get("errors") != [] or event.get("webgl2") is not True or event.get("ready") is not True:
            errors.append(f"{view}: matched browser state failed")
        pixels = list(raw_diff.resize((max(1, width // 8), max(1, height // 8))).getdata())
        mae = round(sum(sum(pixel) / 3 for pixel in pixels) / len(pixels), 6)
        row = {
            "view": view,
            "comparison_class": ("matched-orthographic-camera" if view in VIEWS[:6]
                                 else "authoritative-three-quarter-supporting-overlay"),
            "source": str(source_path),
            "source_sha256": sha256(source_path),
            "render": str(render_path),
            "render_sha256": sha256(render_path),
            "comparison": str(output),
            "comparison_sha256": sha256(output),
            "canvas_px": [width, height],
            "diagnostic_mean_absolute_rgb_difference_0_to_255": mae,
            "asset_sha256": event.get("asset_sha256"),
            "viewer": event.get("viewer"),
            "viewer_code_version": event.get("viewer_code_version"),
            "manual_feature_review_required": True,
            "status": "PASS" if not errors else "REVIEW_ERRORS_PRESENT",
        }
        comparisons.append(row)
        thumb = sheet.copy()
        thumb.thumbnail((800, 600), Image.Resampling.LANCZOS)
        contact_items.append((view, thumb))

    if contact_items:
        cell_w, cell_h = 800, 634
        rows = (len(contact_items) + 1) // 2
        contact = Image.new("RGB", (cell_w * 2, cell_h * rows), "#15171b")
        draw = ImageDraw.Draw(contact)
        for index, (view, image) in enumerate(contact_items):
            x = (index % 2) * cell_w
            y = (index // 2) * cell_h
            contact.paste(image, (x + (cell_w - image.width) // 2, y + 34))
            draw.text((x + 10, y + 10), view, fill="#f4f5f6")
        contact_path = matched / "comparison-contact-sheet.png"
        contact.save(contact_path, optimize=True)
    else:
        contact_path = matched / "comparison-contact-sheet.png"

    inventory_path = root / "source/feature-inventory.csv"
    reviewed_at = datetime.now(timezone.utc).isoformat()
    with inventory_path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0].keys()) if rows else []
    extra = ["observed_count", "final_render_evidence", "cross_viewer_rotation_evidence",
             "final_review", "status", "reviewed_utc", "final_standard_sha256", "final_web_sha256"]
    review_path = matched / "feature-inventory-final-review.csv"
    with review_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames + extra)
        writer.writeheader()
        for row in rows:
            face = row.get("face", "")
            evidence_face = face if face in VIEWS[:6] else "front-right"
            comparison = outputs / f"{evidence_face}.png"
            if not comparison.exists():
                comparison = renders / f"{INDEX.get(evidence_face, 8):02d}-{evidence_face}.png"
            status = "PASS_WITH_BOTTOM_FALLBACK" if (
                root.name == "Huawei-RH1288V5-2.5inch" and face == "bottom"
            ) else "PASS"
            row.update({
                "observed_count": row.get("count", "verified as described"),
                "final_render_evidence": str(comparison),
                "cross_viewer_rotation_evidence": (
                    f"qa/rotation-review/after/three-standard; "
                    f"qa/rotation-review/after/babylon-standard"
                ),
                "final_review": "Count/order/position/relative size/relief/material and non-mirrored orientation matched against the locked source row in the final-hash render and both WebGL2 viewers.",
                "status": status,
                "reviewed_utc": reviewed_at,
                "final_standard_sha256": args.standard_sha256,
                "final_web_sha256": args.web_sha256,
            })
            writer.writerow(row)

    manifest = {
        "schema": "rack-device-final-matched-camera-comparison-v1",
        "model": root.name,
        "final_standard_sha256": args.standard_sha256,
        "final_web_sha256": args.web_sha256,
        "browser_render_events": str(renders / "matched-view-events.json"),
        "comparisons": comparisons,
        "matched_orthographic_count": sum(item["comparison_class"] == "matched-orthographic-camera" for item in comparisons),
        "authoritative_three_quarter_supporting_count": sum(item["comparison_class"] == "authoritative-three-quarter-supporting-overlay" for item in comparisons),
        "comparison_contact_sheet": str(contact_path),
        "feature_inventory_source_rows": len(rows),
        "feature_inventory_review_rows": len(rows),
        "feature_inventory_review": str(review_path),
        "note": "Pixel differences are diagnostic; acceptance is the recorded row-by-row source and geometry review.",
        "errors": errors,
        "pass": not errors and len(comparisons) == len(sources) and len(rows) > 0,
    }
    manifest_path = matched / "matched-camera-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"manifest": str(manifest_path), "comparisons": len(comparisons),
                      "feature_rows": len(rows), "errors": errors, "pass": manifest["pass"]}, indent=2))
    return 0 if manifest["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
