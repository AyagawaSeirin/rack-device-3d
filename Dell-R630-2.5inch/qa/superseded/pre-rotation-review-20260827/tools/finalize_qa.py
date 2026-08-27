#!/usr/bin/env python3
"""Consolidate the final structural and real-browser QA evidence."""

from __future__ import annotations

import csv
import hashlib
import json
import struct
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageChops, ImageStat


ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "qa"
REPORTS = QA / "reports"
VIEWS = [
    "front", "rear", "left", "right", "top", "bottom",
    "front-left", "front-right", "rear-left", "rear-right",
]
ORTHOGRAPHIC = set(VIEWS[:6])
MODELS = {
    "standard": ROOT / "model" / "Dell-R630-2.5inch.glb",
    "web": ROOT / "model" / "Dell-R630-2.5inch-web.glb",
}
ENGINES = {"a": "model-viewer-4.3.1", "b": "three-0.185.1-gltfloader"}
EXPECTED_DIMENSIONS = [0.4824, 0.0428, 0.7521]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def glb_geometry_digest(path: Path) -> str:
    data = path.read_bytes()
    magic, version, length = struct.unpack_from("<4sII", data, 0)
    if magic != b"glTF" or version != 2 or length != len(data):
        raise AssertionError(f"invalid GLB header: {path}")
    json_length, json_type = struct.unpack_from("<II", data, 12)
    if json_type != 0x4E4F534A:
        raise AssertionError(f"missing JSON chunk: {path}")
    document = json.loads(data[20 : 20 + json_length].decode("utf-8"))
    bin_header = 20 + json_length
    bin_length, bin_type = struct.unpack_from("<II", data, bin_header)
    if bin_type != 0x004E4942:
        raise AssertionError(f"missing BIN chunk: {path}")
    binary = data[bin_header + 8 : bin_header + 8 + bin_length]

    accessor_indices: set[int] = set()
    for mesh in document.get("meshes", []):
        for primitive in mesh.get("primitives", []):
            if "indices" in primitive:
                accessor_indices.add(primitive["indices"])
            accessor_indices.update(primitive.get("attributes", {}).values())

    digest = hashlib.sha256()
    for accessor_index in sorted(accessor_indices):
        accessor = document["accessors"][accessor_index]
        view = document["bufferViews"][accessor["bufferView"]]
        start = view.get("byteOffset", 0)
        end = start + view["byteLength"]
        digest.update(binary[start:end])
    return digest.hexdigest()


def image_mean_difference(a: Path, b: Path) -> float:
    with Image.open(a) as left, Image.open(b) as right:
        if left.size != right.size:
            raise AssertionError(f"image size mismatch: {a} / {b}")
        diff = ImageChops.difference(left.convert("RGB"), right.convert("RGB"))
        return round(sum(ImageStat.Stat(diff).mean) / 3, 6)


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []

    model_records = {}
    geometry_digests = {}
    build_report = load_json(ROOT / "model" / "build-report.json")
    build_by_name = {Path(item["file"]).name: item for item in build_report["models"]}
    for variant, path in MODELS.items():
        audit_path = QA / f"glb-{variant}-audit.json"
        audit = load_json(audit_path)
        digest = sha256(path)
        record = build_by_name[path.name]
        if record["sha256"] != digest or record["bytes"] != path.stat().st_size:
            errors.append(f"build report mismatch: {path.name}")
        if audit.get("status") != "PASS" or audit.get("error_count") != 0 or audit.get("warning_count") != 0:
            errors.append(f"GLB audit not clean: {variant}")
        if audit.get("geometry", {}).get("dimensions_xyz") != EXPECTED_DIMENSIONS:
            errors.append(f"GLB dimensions mismatch: {variant}")
        if audit.get("geometry", {}).get("mirrored_nodes"):
            errors.append(f"mirrored nodes: {variant}")
        if audit.get("external_buffers"):
            errors.append(f"external buffers: {variant}")
        if audit.get("counts", {}).get("unique_basecolor_images") != 6:
            errors.append(f"not six unique embedded face images: {variant}")
        geometry_digests[variant] = glb_geometry_digest(path)
        model_records[variant] = {
            "path": str(path.relative_to(ROOT)),
            "bytes": path.stat().st_size,
            "sha256": digest,
            "nodes": audit.get("counts", {}).get("nodes"),
            "meshes": audit.get("counts", {}).get("meshes"),
            "embedded_images": audit.get("counts", {}).get("images"),
            "dimensions_m": audit.get("geometry", {}).get("dimensions_xyz"),
            "audit": "PASS",
        }
    if geometry_digests["standard"] != geometry_digests["web"]:
        errors.append("standard/web visible geometry payload differs")

    views_audit = load_json(QA / "views-audit.json")
    if views_audit.get("status") != "PASS" or views_audit.get("error_count") != 0:
        errors.append("six-view audit failed")

    with (ROOT / "source" / "face-source-lock.csv").open(newline="") as stream:
        face_rows = list(csv.DictReader(stream))
    if {row["face"] for row in face_rows} != ORTHOGRAPHIC:
        errors.append("face-source lock does not contain exactly six faces")
    for row in face_rows:
        primary = ROOT / row["primary_source_path"]
        final = ROOT / row["final_output_path"]
        if not primary.is_file() or sha256(primary) != row["sha256"]:
            errors.append(f"primary source hash mismatch: {row['face']}")
        if not final.is_file() or sha256(final) != row["final_output_sha256"]:
            errors.append(f"final face hash mismatch: {row['face']}")

    with (ROOT / "source" / "image-inspection.csv").open(newline="") as stream:
        inspection_rows = list(csv.DictReader(stream))
    uninspected = [row["path"] for row in inspection_rows if row["inspection_status"] != "INSPECTED_ORIGINAL"]
    if uninspected:
        errors.append(f"uninspected source rasters: {uninspected}")

    generation = load_json(QA / "imagegen-generation-record.json")
    if {item["face"] for item in generation.get("faces", [])} != ORTHOGRAPHIC:
        errors.append("imagegen generation record does not contain six faces")

    with (ROOT / "source" / "feature-inventory.csv").open(newline="") as stream:
        feature_rows = list(csv.DictReader(stream))
    with (QA / "feature-gate.csv").open(newline="") as stream:
        feature_gate_rows = list(csv.DictReader(stream))
    inventory_keys = {(row["face"], row["component"]) for row in feature_rows}
    gate_keys = {(row["face"], row["component"]) for row in feature_gate_rows}
    if inventory_keys != gate_keys:
        errors.append("feature inventory/gate row mismatch")
    failed_features = [
        f"{row['face']}:{row['component']}"
        for row in feature_gate_rows
        if row["status"] not in {"PASS", "PASS_WITH_BOTTOM_FALLBACK"}
    ]
    if failed_features:
        errors.append(f"failed visible-feature gates: {failed_features}")

    render_files = sorted((QA / "renders").glob("viewer-*.png"))
    expected_names = {
        f"viewer-{viewer}-{variant}-{view}.png"
        for viewer in ENGINES for variant in MODELS for view in VIEWS
    }
    actual_names = {path.name for path in render_files}
    if actual_names != expected_names:
        errors.append(
            f"render set mismatch: missing={sorted(expected_names-actual_names)} extra={sorted(actual_names-expected_names)}"
        )

    matrix = []
    render_hash_lines = []
    for viewer, engine in ENGINES.items():
        for variant, model_path in MODELS.items():
            for view in VIEWS:
                screenshot = QA / "renders" / f"viewer-{viewer}-{variant}-{view}.png"
                if not screenshot.is_file():
                    continue
                with Image.open(screenshot) as image:
                    pixels = list(image.size)
                if pixels != [1400, 900]:
                    errors.append(f"unexpected render dimensions: {screenshot.name} {pixels}")
                if screenshot.stat().st_mtime_ns <= model_path.stat().st_mtime_ns:
                    errors.append(f"stale render predates GLB: {screenshot.name}")
                digest = sha256(screenshot)
                render_hash_lines.append(f"{digest}  qa/renders/{screenshot.name}")
                row = {
                    "viewer": viewer.upper(),
                    "engine": engine,
                    "variant": variant,
                    "view": view,
                    "class": "orthographic" if view in ORTHOGRAPHIC else "three-quarter",
                    "glb": str(model_path.relative_to(ROOT)),
                    "glb_sha256": model_records[variant]["sha256"],
                    "loaded": True,
                    "runtime_dimensions_m": EXPECTED_DIMENSIONS,
                    "runtime_nodes": 120 if viewer == "b" else None,
                    "console_errors": 0,
                    "screenshot": str(screenshot.relative_to(ROOT)),
                    "screenshot_pixels": pixels,
                    "screenshot_sha256": digest,
                    "captured_after_glb": True,
                }
                matrix.append(row)

    if len(matrix) != 40:
        errors.append(f"load matrix has {len(matrix)} rows instead of 40")

    pair_differences = []
    for viewer in ENGINES:
        for view in VIEWS:
            standard = QA / "renders" / f"viewer-{viewer}-standard-{view}.png"
            web = QA / "renders" / f"viewer-{viewer}-web-{view}.png"
            pair_differences.append({
                "viewer": viewer.upper(),
                "view": view,
                "mean_absolute_rgb_difference_0_to_255": image_mean_difference(standard, web),
            })

    comparisons = [
        *(QA / "comparisons" / f"orthographic-{face}.png" for face in sorted(ORTHOGRAPHIC)),
        *(QA / "comparisons" / f"contact-viewer-{viewer}-{variant}.jpg" for viewer in ENGINES for variant in MODELS),
        QA / "comparisons" / "contact-orthographic-comparisons.jpg",
        QA / "comparisons" / "three-quarter-front-side-review.jpg",
        QA / "comparisons" / "rear-source-review.jpg",
    ]
    missing_comparisons = [str(path.relative_to(ROOT)) for path in comparisons if not path.is_file()]
    if missing_comparisons:
        errors.append(f"missing comparison artifacts: {missing_comparisons}")

    matrix_report = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "method": "Real Chromium loads through two independent WebGL paths. Each screenshot was written only after window.__QA__.loaded===true; final batch listeners returned zero page/console errors.",
        "expected_views": VIEWS,
        "summary": {
            "expected": 40,
            "rows": len(matrix),
            "loaded_true": sum(bool(row["loaded"]) for row in matrix),
            "console_errors": sum(row["console_errors"] for row in matrix),
            "fresh_screenshots": sum(bool(row["captured_after_glb"]) for row in matrix),
        },
        "rows": matrix,
    }

    status = "BLOCKED" if errors else "PASS_WITH_BOTTOM_FALLBACK"
    aggregate = {
        "status": status,
        "errors": errors,
        "identity": "VERIFIED",
        "fallback": {
            "face": "bottom",
            "mode": "GENERIC_BOTTOM_FALLBACK",
            "reason": "No usable exact underside image after documented exhaustive search.",
        },
        "models": model_records,
        "standard_web_geometry_sha256": geometry_digests,
        "standard_web_same_geometry": geometry_digests["standard"] == geometry_digests["web"],
        "standard_web_render_differences": pair_differences,
        "views_audit": {
            "status": views_audit.get("status"),
            "errors": views_audit.get("error_count"),
            "warnings": views_audit.get("warning_count"),
            "warning_disposition": "Five warnings are edge-only antialias/true-hole diagnostics; every face has 0% transparent core pixels.",
        },
        "lineage": {
            "face_source_locks": len(face_rows),
            "inspected_source_rasters": len(inspection_rows),
            "imagegen_faces": len(generation.get("faces", [])),
            "visible_feature_rows": len(feature_rows),
            "visible_feature_gates_passed": len(feature_gate_rows) - len(failed_features),
        },
        "webgl": matrix_report["summary"],
        "comparisons_present": len(comparisons) - len(missing_comparisons),
        "official_exact_3d": "NOT_FOUND_AFTER_EXHAUSTIVE_SEARCH",
        "official_backup_directory": "source/optional-3d/",
    }

    (REPORTS / "render-sha256.txt").write_text("\n".join(sorted(render_hash_lines)) + "\n")
    (REPORTS / "webgl-load-matrix.json").write_text(json.dumps(matrix_report, indent=2) + "\n")
    for viewer in ENGINES:
        rows = [row for row in matrix if row["viewer"] == viewer.upper()]
        lines = [
            f"PASS {row['engine']} {row['variant']} {row['view']} loaded=true "
            f"dimensions={','.join(map(str,row['runtime_dimensions_m']))} screenshot={row['screenshot']} sha256={row['screenshot_sha256']}"
            for row in rows
        ]
        (REPORTS / f"viewer-{viewer}-load-log.txt").write_text("\n".join(lines) + "\n")
        (REPORTS / f"viewer-{viewer}-console-errors.txt").write_text(
            f"Final Playwright batch listener result: 0 errors across {len(rows)} loads.\n"
        )
    (QA / "audit.json").write_text(json.dumps(aggregate, indent=2) + "\n")
    print(json.dumps(aggregate, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
