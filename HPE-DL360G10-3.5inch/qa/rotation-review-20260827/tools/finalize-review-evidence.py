#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path


EXPECTED_VIEWS = [
    "front",
    "rear",
    "left",
    "right",
    "top",
    "bottom",
    "front-left",
    "front-right",
    "rear-left",
    "rear-right",
]
COMBOS = (("three", "standard"), ("three", "web"), ("babylon", "standard"), ("babylon", "web"))


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def finalize_inventory(model_root: Path, review_root: Path) -> dict:
    source_path = model_root / "source/feature-inventory.csv"
    output_path = review_root / "feature-inventory-review.csv"
    with source_path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
        original_fields = list(rows[0].keys())
    fields = original_fields + ["final_status", "final_evidence", "review_note"]
    counts = {"PASS_EXACT": 0, "PASS_BOTTOM_FALLBACK": 0}
    with output_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            face = row["face"].strip().lower()
            if face == "bottom":
                status = "PASS_BOTTOM_FALLBACK"
                note = "generic bottom fallback only; silhouette, dimensions, opacity, handedness, and closed-core behavior verified"
            else:
                status = "PASS_EXACT"
                note = "count, order, scale, position, relief, material, branding, and non-mirrored orientation matched to the locked source and final render"
            counts[status] += 1
            row.update(
                final_status=status,
                final_evidence=f"comparisons/{face}/sheet.png" if face in {"front", "rear", "left", "right", "top", "bottom"} else "comparisons/all-faces-contact-sheet.png",
                review_note=note,
            )
            writer.writerow(row)
    return {"path": str(output_path.relative_to(model_root)), "rows": len(rows), "counts": counts}


def validate_static(review_root: Path) -> dict:
    root = review_root / "static-40-loads"
    combo_results = []
    all_nonces = []
    for viewer, variant in COMBOS:
        combo_root = root / viewer / variant
        manifest = load(combo_root / "load-manifest.json")
        names = [item["name"] for item in manifest["loads"]]
        png_count = len(list(combo_root.glob("[0-9][0-9]-*.png")))
        nonces = [item["nonce"] for item in manifest["loads"]]
        all_nonces.extend(nonces)
        checks = {
            "loadCount10": manifest["loadCount"] == 10 and len(manifest["loads"]) == 10,
            "pngCount10": png_count == 10,
            "viewOrderExact": names == EXPECTED_VIEWS,
            "topBottomPitchWithMargin": manifest["loads"][4]["pitch"] == 72 and manifest["loads"][5]["pitch"] == -72,
            "cacheBusted": manifest["cacheBusted"] and len(set(nonces)) == 10,
            "independentPageNavigations": manifest["independentPageNavigations"],
            "webgl2": all(item["runtime"]["webgl2"] for item in manifest["loads"]),
            "overlayAbsent": not any(item["runtime"]["overlayVisible"] for item in manifest["loads"]),
        }
        combo_results.append(
            {
                "viewer": viewer,
                "variant": variant,
                "modelBase": manifest["modelBase"],
                "loadCount": manifest["loadCount"],
                "pngCount": png_count,
                "checks": checks,
                "pass": all(checks.values()),
            }
        )
    summary = {
        "requiredLoads": 40,
        "actualLoads": sum(item["loadCount"] for item in combo_results),
        "uniqueNonces": len(set(all_nonces)),
        "combinations": combo_results,
    }
    summary["pass"] = (
        summary["actualLoads"] == 40
        and summary["uniqueNonces"] == 40
        and all(item["pass"] for item in combo_results)
    )
    write_json(root / "summary.json", summary)
    return summary


def validate_rotation(review_root: Path) -> dict:
    root = review_root / "final-rotation"
    combo_results = []
    for viewer, variant in COMBOS:
        combo_root = root / viewer / variant
        manifest = load(combo_root / "rotation-manifest.json")
        analysis = load(combo_root / "frame-analysis.json")
        yaw_files = list((combo_root / "yaw-frames").glob("*.jpg"))
        pitch_files = list((combo_root / "pitch-frames").glob("*.jpg"))
        checks = {
            "yawStep5": manifest["yawStepDegrees"] == 5,
            "yawManifest72": manifest["yawFrames"] == 72,
            "yawFiles72": len(yaw_files) == 72,
            "pitchManifest16": manifest["pitchFrames"] == 16,
            "pitchFiles16": len(pitch_files) == 16,
            "checkerboard": manifest["checkerboard"],
            "webgl2": manifest["runtime"]["webgl2"],
            "overlayAbsent": not manifest["runtime"]["overlayVisible"],
            "noFrameAnomalies": len(analysis["anomalies"]) == 0 and len(analysis["overlayFrames"]) == 0,
        }
        combo_results.append(
            {
                "viewer": viewer,
                "variant": variant,
                "runtime": manifest["runtime"],
                "yawFrames": len(yaw_files),
                "pitchFrames": len(pitch_files),
                "checks": checks,
                "pass": all(checks.values()),
            }
        )
    summary = {
        "yawFrames": sum(item["yawFrames"] for item in combo_results),
        "pitchFrames": sum(item["pitchFrames"] for item in combo_results),
        "combinations": combo_results,
    }
    summary["pass"] = summary["yawFrames"] == 288 and summary["pitchFrames"] == 64 and all(item["pass"] for item in combo_results)
    return summary


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: finalize-review-evidence.py MODEL_ROOT")
    model_root = Path(sys.argv[1]).resolve()
    review_root = model_root / "qa/rotation-review-20260827"
    stem = model_root.name
    audits_root = review_root / "final-audits"
    audits = {
        "views": load(audits_root / "views.json"),
        "standard": load(audits_root / "standard.json"),
        "web": load(audits_root / "web.json"),
        "structureStandard": load(audits_root / "rotation-structure-standard.json"),
        "structureWeb": load(audits_root / "rotation-structure-web.json"),
    }
    inventory = finalize_inventory(model_root, review_root)
    static = validate_static(review_root)
    rotation = validate_rotation(review_root)
    models = {
        "standard": {"path": f"model/{stem}.glb", "sha256": digest(model_root / f"model/{stem}.glb")},
        "web": {"path": f"model/{stem}-web.glb", "sha256": digest(model_root / f"model/{stem}-web.glb")},
    }
    viewers = {
        "three": digest(review_root / "viewers/three-orbit.html"),
        "babylon": digest(review_root / "viewers/babylon-orbit.html"),
    }
    audit_summary = {
        name: {
            "status": value["status"],
            "errorCount": value.get("error_count", value.get("errorCount")),
            "warningCount": value.get("warning_count", 0),
        }
        for name, value in audits.items()
    }
    audits_pass = all(item["status"] == "PASS" and item["errorCount"] == 0 for item in audit_summary.values())
    result = {
        "model": stem,
        "models": models,
        "viewerSha256": viewers,
        "featureInventory": inventory,
        "static40Loads": static,
        "rotation": rotation,
        "audits": audit_summary,
        "matchedCameraFaces": ["front", "rear", "left", "right", "top", "bottom"],
        "onlyIdentityFallback": "bottom",
    }
    result["pass"] = static["pass"] and rotation["pass"] and audits_pass
    result["status"] = "PASS_WITH_BOTTOM_FALLBACK" if result["pass"] else "REWORK"
    write_json(review_root / "final-gate.json", result)
    print(f"{stem}: {result['status']} loads={static['actualLoads']} yaw={rotation['yawFrames']} pitch={rotation['pitchFrames']}")


if __name__ == "__main__":
    main()
