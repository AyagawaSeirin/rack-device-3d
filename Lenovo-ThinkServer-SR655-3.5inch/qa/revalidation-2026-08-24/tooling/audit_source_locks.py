#!/usr/bin/env python3
import csv
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageOps, ImageStat


ROOT = Path(__file__).resolve().parents[3]
LOCKS = ROOT / "source" / "face-source-lock.csv"
SUMMARY = ROOT / "qa" / "imagegen-summary.csv"
OUTPUT = ROOT / "qa" / "revalidation-2026-08-24" / "source-lock-audit.json"
EXPECTED_FACES = ["front", "rear", "left", "right", "top", "bottom"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


errors = []
warnings = []
rows = []

with LOCKS.open(newline="", encoding="utf-8") as handle:
    lock_rows = list(csv.DictReader(handle))

if [row["face"] for row in lock_rows] != EXPECTED_FACES:
    errors.append("face-source-lock rows are not exactly front,rear,left,right,top,bottom")

primary_paths = []
for row in lock_rows:
    face = row["face"]
    primary = ROOT / row["primary_source_path"]
    final = ROOT / row["final_output_path"]
    primary_paths.append(row["primary_source_path"])
    primary_exists = primary.is_file()
    final_exists = final.is_file()
    actual_primary_sha = sha256(primary) if primary_exists else None
    actual_final_sha = sha256(final) if final_exists else None
    support = [item for item in row["supporting_source_paths"].split(";") if item]
    missing_support = [item for item in support if not (ROOT / item).is_file()]
    if not primary_exists:
        errors.append(f"{face}: missing primary source {row['primary_source_path']}")
    if actual_primary_sha != row["sha256"]:
        errors.append(f"{face}: primary SHA-256 mismatch")
    if not final_exists:
        errors.append(f"{face}: missing final output {row['final_output_path']}")
    if missing_support:
        errors.append(f"{face}: missing supporting sources: {missing_support}")
    image_info = None
    if final_exists:
        with Image.open(final) as image:
            image_info = {
                "format": image.format,
                "mode": image.mode,
                "width": image.width,
                "height": image.height,
                "has_alpha": "A" in image.getbands(),
            }
            if image.format != "PNG" or "A" not in image.getbands():
                errors.append(f"{face}: final output is not an alpha-capable PNG")
    rows.append({
        "face": face,
        "production_mode": row["production_mode"],
        "primary_source_path": row["primary_source_path"],
        "primary_source_exists": primary_exists,
        "recorded_primary_sha256": row["sha256"],
        "actual_primary_sha256": actual_primary_sha,
        "primary_sha256_match": actual_primary_sha == row["sha256"],
        "visual_origin": row["visual_origin"],
        "supporting_source_count": len(support),
        "missing_supporting_sources": missing_support,
        "final_output_path": row["final_output_path"],
        "final_sha256": actual_final_sha,
        "final_image": image_info,
    })

if len(set(primary_paths)) != len(primary_paths):
    errors.append("primary source paths are not independent across all six face locks")

with SUMMARY.open(newline="", encoding="utf-8") as handle:
    summary_rows = {row["face"]: row for row in csv.DictReader(handle)}

imagegen = []
for row in rows:
    face = row["face"]
    summary = summary_rows.get(face)
    if summary is None:
        errors.append(f"{face}: missing imagegen summary row")
        continue
    if summary["call_count"] != "1":
        errors.append(f"{face}: imagegen call_count is not 1")
    if summary["production_mode"] != row["production_mode"]:
        errors.append(f"{face}: production mode differs between source lock and imagegen summary")
    if summary["final_sha256"] != row["final_sha256"]:
        errors.append(f"{face}: final SHA-256 differs between current view and imagegen summary")
    prompt = ROOT / "qa" / "imagegen-prompts" / f"{face}.md"
    if not prompt.is_file():
        errors.append(f"{face}: missing prompt/input-role record")
    imagegen.append({
        "face": face,
        "call_count": int(summary["call_count"]),
        "production_mode": summary["production_mode"],
        "summary_final_sha256": summary["final_sha256"],
        "current_final_sha256": row["final_sha256"],
        "prompt_record": str(prompt.relative_to(ROOT)),
        "prompt_record_exists": prompt.is_file(),
    })

left_path = ROOT / "views" / "left.png"
right_path = ROOT / "views" / "right.png"
with Image.open(left_path) as left_image, Image.open(right_path) as right_image:
    left = left_image.convert("RGBA")
    right = right_image.convert("RGBA")
    if left.size != right.size:
        errors.append("left/right final views have different dimensions")
        mirror_metrics = None
    else:
        direct = ImageStat.Stat(ImageChops.difference(left, right)).mean
        mirrored = ImageStat.Stat(ImageChops.difference(left, ImageOps.mirror(right))).mean
        mirror_metrics = {
            "dimensions": list(left.size),
            "byte_identical": sha256(left_path) == sha256(right_path),
            "direct_mean_abs_rgba_0_255": direct,
            "right_mirrored_mean_abs_rgba_0_255": mirrored,
            "right_only_locked_landmark": "yellow weight/caution label",
            "left_only_locked_landmark": "two small rectangular rear slots and distinct hole pattern",
        }
        if mirror_metrics["byte_identical"]:
            errors.append("left/right final views are byte-identical")
        if sum(mirrored) / len(mirrored) < 1.0:
            errors.append("left/right final views appear to be mirrored copies")

report = {
    "status": "PASS" if not errors else "FAIL",
    "root": str(ROOT),
    "face_count": len(rows),
    "independent_primary_source_paths": len(set(primary_paths)) == len(primary_paths),
    "rows": rows,
    "imagegen_records": imagegen,
    "left_right_independence": mirror_metrics,
    "errors": errors,
    "warnings": warnings,
}
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": report["status"], "errors": errors, "output": str(OUTPUT), "left_right": mirror_metrics}, indent=2))
raise SystemExit(1 if errors else 0)
