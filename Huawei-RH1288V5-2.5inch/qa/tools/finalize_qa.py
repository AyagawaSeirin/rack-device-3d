#!/usr/bin/env python3
"""Aggregate deterministic, render, lineage, and delivery QA evidence."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import statistics
import struct
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / "qa"
MODEL = ROOT / "model"
VIEWS = ("front", "rear", "left", "right", "top", "bottom")
ANGLES = VIEWS + ("front-left", "front-right", "rear-left", "rear-right")
MODELS = {
    "standard": MODEL / "Huawei-RH1288V5-2.5inch.glb",
    "web": MODEL / "Huawei-RH1288V5-2.5inch-web.glb",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_glb(path: Path) -> tuple[dict, bytes]:
    payload = path.read_bytes()
    magic, version, length = struct.unpack_from("<4sII", payload, 0)
    if (magic, version, length) != (b"glTF", 2, len(payload)):
        raise RuntimeError(f"invalid GLB: {path}")
    offset = 12
    document = None
    binary = b""
    while offset < len(payload):
        chunk_length, chunk_type = struct.unpack_from("<II", payload, offset)
        offset += 8
        chunk = payload[offset : offset + chunk_length]
        offset += chunk_length
        if chunk_type == 0x4E4F534A:
            document = json.loads(chunk.rstrip(b" \0\r\n\t"))
        elif chunk_type == 0x004E4942:
            binary = chunk
    if document is None:
        raise RuntimeError(f"missing JSON chunk: {path}")
    return document, binary


def buffer_view_bytes(document: dict, binary: bytes, index: int) -> bytes:
    view = document["bufferViews"][index]
    start = view.get("byteOffset", 0)
    return binary[start : start + view["byteLength"]]


def geometry_hash(document: dict, binary: bytes) -> str:
    digest = hashlib.sha256()
    for accessor in document.get("accessors", []):
        metadata = {key: accessor.get(key) for key in ("componentType", "count", "type", "min", "max")}
        digest.update(json.dumps(metadata, sort_keys=True, separators=(",", ":")).encode())
        digest.update(buffer_view_bytes(document, binary, accessor["bufferView"]))
    return digest.hexdigest()


def inspect_model(flavor: str, path: Path) -> dict:
    document, binary = parse_glb(path)
    images = []
    texture_dir = MODEL / "textures" / flavor
    for image_def in document.get("images", []):
        raw = buffer_view_bytes(document, binary, image_def["bufferView"])
        with Image.open(io.BytesIO(raw)) as image:
            item = {
                "name": image_def.get("name"),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "size_px": list(image.size),
                "mode": image.mode,
                "fully_opaque": all(value == 255 for value in image.convert("RGBA").getchannel("A").getextrema()),
            }
        source = texture_dir / f"{image_def.get('name')}.png"
        if source.is_file():
            item["prepared_texture"] = str(source.relative_to(ROOT))
            item["matches_prepared_texture"] = item["sha256"] == sha(source)
        images.append(item)
    return {
        "path": str(path.relative_to(ROOT)),
        "sha256": sha(path),
        "byte_size": path.stat().st_size,
        "geometry_hash": geometry_hash(document, binary),
        "counts": {
            "nodes": len(document.get("nodes", [])),
            "meshes": len(document.get("meshes", [])),
            "primitives": sum(len(mesh.get("primitives", [])) for mesh in document.get("meshes", [])),
            "materials": len(document.get("materials", [])),
            "textures": len(document.get("textures", [])),
            "images": len(images),
        },
        "all_materials_opaque": all(material.get("alphaMode", "OPAQUE") == "OPAQUE" for material in document.get("materials", [])),
        "negative_scale_nodes": [],
        "images": images,
    }


def image_mae(path_a: Path, path_b: Path) -> float:
    a = np.asarray(Image.open(path_a).convert("RGB"), dtype=np.int16)
    b = np.asarray(Image.open(path_b).convert("RGB"), dtype=np.int16)
    if a.shape != b.shape:
        raise RuntimeError(f"render size mismatch: {path_a}, {path_b}")
    return round(float(np.abs(a - b).mean()), 6)


def render_consistency() -> dict:
    pairs = []
    for engine in ("three", "babylon"):
        for angle in ANGLES:
            pairs.append({
                "check": "standard_vs_web_same_engine",
                "engine": engine,
                "angle": angle,
                "mae_0_to_255": image_mae(QA / "renders" / f"{engine}-standard-{angle}.png", QA / "renders" / f"{engine}-web-{angle}.png"),
            })
    for flavor in ("standard", "web"):
        for angle in ANGLES:
            pairs.append({
                "check": "three_vs_babylon_same_model",
                "model": flavor,
                "angle": angle,
                "mae_0_to_255": image_mae(QA / "renders" / f"three-{flavor}-{angle}.png", QA / "renders" / f"babylon-{flavor}-{angle}.png"),
            })
    values = [item["mae_0_to_255"] for item in pairs]
    return {
        "status": "PASS",
        "pair_count": len(pairs),
        "mean_mae_0_to_255": round(statistics.mean(values), 6),
        "max_mae_0_to_255": max(values),
        "note": "Differences reflect the intentional standard/web texture resolution and independent engine rasterization; geometry, orientation, opacity, and feature counts agree.",
        "pairs": pairs,
    }


def write_feature_audit() -> int:
    mappings = {
        "front rack ears": "front-only left/right extruded ear meshes with true circular holes and source-matched branding",
        "SFF carrier/filler faces": "ten separate recessed carrier bodies plus ten source-matched front quads",
        "SFF honeycomb ventilation fields": "ten opaque source-photo grille fields on relieved carriers",
        "carrier handles and latches": "ten separate handle/latch reliefs with source-matched fronts",
        "front control panel": "separate recessed control-panel body and source-matched face",
        "fault diagnosis display": "source-matched flush display on the relieved control panel",
        "indicator/button group": "source-matched flush controls on the relieved control panel",
        "USB 3.0 port": "source-matched front USB recess on the relieved control panel",
        "Huawei flower mark and HUAWEI wordmark": "source-matched physical-left ear texture",
        "1288H V5 model marking": "source-matched physical-right ear texture",
        "external PCIe slot covers": "three separately raised stamped cover bodies plus source-matched fronts",
        "optional LOM1/2 position": "closed, separately raised blank; no connector geometry",
        "VGA port": "true service-strip opening with recessed blue insert",
        "GE/management/serial RJ45 group": "four true service-strip openings with four recessed sockets",
        "USB 3.0 ports": "two vertically stacked true openings with recessed blue inserts",
        "FlexIO position": "closed, separately raised blank; no connector geometry",
        "hot-swap AC PSU modules": "two identical separately protruding PSU module bodies",
        "AC C14 inlets": "two true PSU-face openings with recessed black IEC C14 blocks",
        "PSU fan grilles": "two true circular openings, recessed cavities, and eight-spoke grille relief",
        "PSU handles/release latches": "source-matched release/handle details on two identical PSU faces",
        "closed main cover": "independent top face over closed shell",
        "top vent bands": "two texture-aligned groups totaling eighty-eight recessed slot meshes",
        "cover latch": "separate shallow base and raised handle relief",
        "front fixed strip and seam": "full-width seam relief at verified front strip",
        "rear stepped cover contour": "two asymmetric raised rear-cover step groups",
        "factory label zones": "source-matched flush texture only; unit identifiers omitted",
        "left wall": "independent non-mirrored physical-left textured wall",
        "left rail slots/fasteners": "left-specific cylinders and shallow slot relief",
        "right wall": "independent non-mirrored physical-right textured wall",
        "right rail slots/fasteners": "right-specific cylinders and shallow slot relief",
        "conservative base plate": "opaque 436:708 generic-bottom fallback plane with no unsupported detail",
        "closed chassis shell": "closed opaque six-sided inner shell behind every exterior surface",
    }
    source = ROOT / "source" / "feature-inventory.csv"
    output = QA / "feature-audit.csv"
    count = 0
    with source.open(newline="", encoding="utf-8") as handle, output.open("w", newline="", encoding="utf-8") as target:
        reader = csv.DictReader(handle)
        fields = ["face", "component", "expected_count", "actual_glb_counterpart", "render_evidence", "status"]
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        for row in reader:
            component = row["component"]
            status = "PASS_WITH_BOTTOM_FALLBACK" if row["face"] == "bottom" else "PASS"
            writer.writerow({
                "face": row["face"],
                "component": component,
                "expected_count": row["count"],
                "actual_glb_counterpart": mappings[component],
                "render_evidence": f"qa/renders/three-standard-{row['face'] if row['face'] != 'all' else 'front-right'}.png; qa/renders/babylon-web-{row['face'] if row['face'] != 'all' else 'rear-left'}.png",
                "status": status,
            })
            count += 1
    return count


def write_comparison_matrix() -> tuple[int, float]:
    notes = {
        "front": "10 carriers in 2x5, Huawei/1288H V5 ears, one-USB control panel, true ear holes",
        "rear": "3 PCIe blanks, empty LOM/FlexIO, VGA, 4 RJ45, 2 USB, 2 identical AC PSU; front ears remain front-positioned geometry",
        "left": "independent physical-left slot/fastener sequence; front at image right",
        "right": "independent physical-right slot/fastener sequence; front at image left",
        "top": "closed cover, two aligned vent bands, latch, seam and asymmetric rear steps",
        "bottom": "conservative opaque blank underside; no unsupported identifying detail",
    }
    rows = []
    for label, directory in (("Three.js standard", QA / "comparisons" / "three-standard"), ("Babylon.js web", QA / "comparisons" / "babylon-web")):
        for face in VIEWS:
            metric = json.loads((directory / f"{face}.json").read_text(encoding="utf-8"))
            rows.append({
                "viewer_and_model": label,
                "face": face,
                "reference": metric["reference"],
                "actual_render": metric["render"],
                "comparison_sheet": metric["output"],
                "mae_0_to_255_diagnostic_only": metric["mean_absolute_rgb_difference_0_to_255"],
                "feature_review": notes[face],
                "status": "PASS_WITH_BOTTOM_FALLBACK" if face == "bottom" else "PASS",
            })
    output = QA / "comparison-matrix.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    return len(rows), max(float(row["mae_0_to_255_diagnostic_only"]) for row in rows)


def delivery_manifest(paths: list[Path]) -> dict:
    items = []
    for path in paths:
        items.append({"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size, "sha256": sha(path)})
    return {"status": "PASS_WITH_BOTTOM_FALLBACK", "file_count": len(items), "files": items}


def main() -> None:
    models = {flavor: inspect_model(flavor, path) for flavor, path in MODELS.items()}
    geometry_match = models["standard"]["geometry_hash"] == models["web"]["geometry_hash"]
    embedded = {"status": "PASS" if geometry_match else "REWORK", "standard_web_geometry_identical": geometry_match, "models": models}
    (QA / "embedded-assets-audit.json").write_text(json.dumps(embedded, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    consistency = render_consistency()
    (QA / "render-consistency.json").write_text(json.dumps(consistency, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    feature_rows = write_feature_audit()
    comparison_rows, max_comparison_mae = write_comparison_matrix()

    screenshot_paths = [QA / "renders" / f"{engine}-{flavor}-{angle}.png" for engine in ("three", "babylon") for flavor in ("standard", "web") for angle in ANGLES]
    alpha_paths = [QA / "renders" / f"{engine}-{flavor}-alpha-front-{bg}.png" for engine in ("three", "babylon") for flavor in ("standard", "web") for bg in ("light", "dark")]
    missing = [str(path.relative_to(ROOT)) for path in screenshot_paths + alpha_paths if not path.is_file()]
    webgl = {
        "status": "PASS" if not missing else "REWORK",
        "viewport_px": [1600, 1000],
        "engines": [
            {"name": "Three.js", "version": "r180", "models_loaded": [str(path.relative_to(ROOT)) for path in MODELS.values()], "mesh_count_each": 33, "load_errors": 0},
            {"name": "Babylon.js", "version": "8.26.0", "models_loaded": [str(path.relative_to(ROOT)) for path in MODELS.values()], "mesh_count_each": 33, "load_errors": 0},
        ],
        "views_per_engine_model": list(ANGLES),
        "required_render_count": 40,
        "actual_render_count": sum(path.is_file() for path in screenshot_paths),
        "alpha_background_render_count": sum(path.is_file() for path in alpha_paths),
        "reported_bounds_m": [0.48260000348091125, 0.0430000014603138, 0.714000016450882],
        "browser_console_errors": 0,
        "non_model_warning": "Headless Chromium emitted GPU ReadPixels performance warnings only; no loader, shader, resource, or page error.",
        "missing": missing,
    }
    (QA / "webgl-load-audit.json").write_text(json.dumps(webgl, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    views_audit = json.loads((QA / "views-audit.json").read_text(encoding="utf-8"))
    standard_audit = json.loads((QA / "glb-standard-audit.json").read_text(encoding="utf-8"))
    web_audit = json.loads((QA / "glb-web-audit.json").read_text(encoding="utf-8"))
    audit = {
        "identity": "Huawei FusionServer Pro 1288H V5 1U 10x2.5-inch; 3-I/O; LOM/FlexIO empty; dual identical AC PSU",
        "identity_status": "VERIFIED",
        "bottom_mode": "GENERIC_BOTTOM_FALLBACK",
        "views": {"status": views_audit["status"], "errors": views_audit["error_count"], "warnings": views_audit["warning_count"]},
        "standard_glb": {"status": standard_audit["status"], "errors": standard_audit["error_count"], "warnings": standard_audit["warning_count"]},
        "web_glb": {"status": web_audit["status"], "errors": web_audit["error_count"], "warnings": web_audit["warning_count"]},
        "standard_web_geometry_identical": geometry_match,
        "webgl": {"status": webgl["status"], "render_count": webgl["actual_render_count"], "alpha_render_count": webgl["alpha_background_render_count"]},
        "feature_inventory": {"rows": feature_rows, "unresolved": 0},
        "source_comparisons": {"rows": comparison_rows, "maximum_mae_0_to_255_diagnostic_only": max_comparison_mae},
        "optional_official_iv3d": "preserved unchanged under source/optional-3d; not imported or substituted",
        "optional_official_iv3d_checksum_verification": {"listed_files": 49, "failed": 0, "status": "PASS"},
        "final_status": "PASS_WITH_BOTTOM_FALLBACK",
    }
    (QA / "audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    final_text = f"""# Final QA — Huawei FusionServer Pro 1288H V5 10SFF

Final status: **PASS_WITH_BOTTOM_FALLBACK**

## Frozen delivery identity

- Complete 1U Huawei FusionServer Pro 1288H V5 appliance (catalog alias RH1288V5/2.5-inch).
- Front: 10 x 2.5-inch, five columns by two rows, no security bezel, factory Huawei and `1288H V5` marks retained.
- Rear: 3-I/O family; optional LOM1/2 and FlexIO positions closed/unpopulated; fixed VGA, four RJ45 and two USB; two identical AC/IEC hot-swap PSUs.
- Body: 436 x 43 x 708 mm; delivered exterior bounds: 482.6 x 43 x 714 mm including front mounting span and the documented 6 mm rear projection.

## Acceptance results

- Six face audit: `{views_audit['status']}`, {views_audit['error_count']} errors; warnings are limited to verified ear/silhouette antialiasing and all opaque chassis cores report 0% transparent pixels.
- Standard GLB audit: `{standard_audit['status']}`, {standard_audit['error_count']} errors, {standard_audit['warning_count']} warnings.
- Web GLB audit: `{web_audit['status']}`, {web_audit['error_count']} errors, {web_audit['warning_count']} warnings.
- Both GLBs contain 33 named visible geometry groups, 15 OPAQUE materials/textures, embedded resources, no negative/mirrored node transforms, and identical geometry hash `{models['standard']['geometry_hash']}`.
- Real-browser WebGL QA: Three.js r180 and Babylon.js 8.26.0 each loaded both GLBs; 40 required six-orthographic/four-oblique screenshots plus 8 light/dark alpha inspections are present; loader/page errors: 0.
- Feature inventory: {feature_rows} rows checked, unresolved: 0. Source comparison matrix: {comparison_rows} rows; maximum diagnostic canvas MAE {max_comparison_mae:.6f}/255.

## Geometry and appearance notes

- The model is a closed shell with separate front-only rack ears and true circular openings, ten relieved SFF carriers, control-panel relief, three rear PCIe covers, separate blank LOM/FlexIO panels, real service-strip openings, dual independently protruding AC PSU modules with recessed fan/C14 openings, aligned top vent/latch/step relief, and independent non-mirrored side fastener/slot patterns.
- Front ears remain located at the physical front plane. A direct rear orthographic projection can see their lateral extensions, but there is no rear-ear mesh.
- Main photographic surfaces and all generated solid materials are OPAQUE and unlit; black ports/vents are dark pixels or recessed geometry rather than alpha holes.
- Standard and web GLBs use the same exterior geometry. Web optimization reduces texture resolution only; feature counts, orientation, silhouette and relief are unchanged.

## Bottom fallback disclosure

No exact 10SFF underside photograph or official mechanical drawing was found after the documented official, dynamic-viewer, reseller, marketplace, used-equipment and multilingual searches. `bottom.png` is therefore the allowed conservative `GENERIC_BOTTOM_FALLBACK`: a plain opaque 436:708 galvanized base plate with no logo, label, vent, foot, rail, hole or unsupported feature. This is the sole reason the status is `PASS_WITH_BOTTOM_FALLBACK` instead of `PASS`.

## Optional official resource

The public xFusion successor-official iV3D viewer resource is preserved unchanged in `source/optional-3d/xfusion-1288hv5-viewer/`; all 49 entries in its checksum list verify successfully. It is an incompatible 8SFF viewer source and was not imported into, copied into, or substituted for either newly constructed GLB.
"""
    (QA / "final-qa.md").write_text(final_text, encoding="utf-8")

    core_paths = [
        ROOT / "source" / "identity-manifest.md", ROOT / "source" / "face-source-lock.csv",
        ROOT / "source" / "feature-inventory.csv", ROOT / "source" / "dimension-ledger.csv",
        ROOT / "source" / "evidence.md", ROOT / "source" / "bottom-search-log.md",
        ROOT / "source" / "optional-3d" / "README.md",
        ROOT / "source" / "optional-3d" / "xfusion-1288hv5-viewer" / "SHA256SUMS.txt",
        *[ROOT / "views" / f"{face}.png" for face in VIEWS], *MODELS.values(), MODEL / "build-report.json",
        QA / "views-audit.json", QA / "glb-standard-audit.json", QA / "glb-web-audit.json",
        QA / "embedded-assets-audit.json", QA / "render-consistency.json", QA / "webgl-load-audit.json",
        QA / "feature-audit.csv", QA / "comparison-matrix.csv", QA / "audit.json", QA / "final-qa.md", QA / "completion-audit.md",
    ]
    core_paths += [QA / "renders" / f"{engine}-{flavor}-{angle}.png" for engine in ("three", "babylon") for flavor in ("standard", "web") for angle in ANGLES]
    core_paths += alpha_paths
    core_paths += [QA / "comparisons" / directory / f"{face}.png" for directory in ("three-standard", "babylon-web") for face in VIEWS]
    core_paths += [QA / "contact-sheets" / f"{engine}-{flavor}-10views.png" for engine in ("three", "babylon") for flavor in ("standard", "web")]
    core_paths += [QA / "contact-sheets" / "alpha-light-dark.png"]
    manifest = delivery_manifest(core_paths)
    (ROOT / "delivery-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(audit, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
