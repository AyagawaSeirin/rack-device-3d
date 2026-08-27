#!/usr/bin/env python3
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw, ImageStat


ROOT = Path(__file__).resolve().parents[3]
QA = ROOT / "qa" / "revalidation-2026-08-24"
LOG = QA / "http-glb-loads.jsonl"
OUTPUT = QA / "load-evidence-audit.json"
CSV_OUTPUT = QA / "load-evidence.csv"
CONTACT_DIR = QA / "contact-sheets"
VIEWS = ["front", "rear", "right", "left", "top", "bottom", "frontRight", "frontLeft", "rearRight", "rearLeft"]
MODELS = {
    "standard": ROOT / "model" / "Lenovo-ThinkServer-SR655-3.5inch.glb",
    "web": ROOT / "model" / "Lenovo-ThinkServer-SR655-3.5inch-web.glb",
}
LOADERS = ["three", "babylon"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


current_models = {
    model: {"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size, "sha256": sha256(path)}
    for model, path in MODELS.items()
}
events = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
errors = []
records = []

if len(events) != 40:
    errors.append(f"expected exactly 40 formal GLB load events, found {len(events)}")

run_ids = [event.get("query", {}).get("run") for event in events]
if None in run_ids or len(set(run_ids)) != len(run_ids):
    errors.append("run IDs are missing or not unique")

observed = Counter()
for event in events:
    query = event.get("query", {})
    loader = query.get("loader")
    model = query.get("model")
    view = query.get("view")
    run = query.get("run")
    observed[(loader, model, view)] += 1
    if loader not in LOADERS or model not in MODELS or view not in VIEWS:
        errors.append(f"invalid matrix values in event {run}: {loader}/{model}/{view}")
        continue
    ordinal = VIEWS.index(view) + 1
    screenshot = QA / "renders" / f"{loader}-{model}" / f"{ordinal:02d}-{view}.png"
    screenshot_exists = screenshot.is_file()
    screenshot_sha = sha256(screenshot) if screenshot_exists else None
    screenshot_info = None
    if not screenshot_exists:
        errors.append(f"missing screenshot for {run}: {screenshot}")
    else:
        with Image.open(screenshot) as image:
            rgb = image.convert("RGB")
            stats = ImageStat.Stat(rgb)
            screenshot_info = {
                "width": rgb.width,
                "height": rgb.height,
                "mean_rgb": stats.mean,
                "stddev_rgb": stats.stddev,
            }
            if rgb.size != (1200, 800):
                errors.append(f"wrong screenshot dimensions for {run}: {rgb.size}")
            if sum(stats.stddev) / 3.0 < 1.0:
                errors.append(f"blank/near-blank screenshot for {run}")
    expected_model = current_models[model]
    checks = {
        "http_200": event.get("status") == 200,
        "bytes_match_current": event.get("bytes") == expected_model["bytes"],
        "actual_sha_matches_current": event.get("sha256") == expected_model["sha256"],
        "requested_sha_matches_current": event.get("expected_sha256") == expected_model["sha256"],
        "server_sha_match_flag": event.get("sha256_match") is True,
        "unique_chromium_user_agent": "Chrome" in (event.get("user_agent") or ""),
        "screenshot_exists": screenshot_exists,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        errors.append(f"{run}: failed checks {failed}")
    records.append({
        "timestamp_utc": event.get("timestamp_utc"),
        "loader": loader,
        "model": model,
        "view": view,
        "run_id": run,
        "http_status": event.get("status"),
        "bytes": event.get("bytes"),
        "actual_sha256": event.get("sha256"),
        "requested_sha256": event.get("expected_sha256"),
        "request_path": event.get("request_path"),
        "user_agent": event.get("user_agent"),
        "screenshot_path": str(screenshot.relative_to(ROOT)) if screenshot_exists else None,
        "screenshot_sha256": screenshot_sha,
        "screenshot": screenshot_info,
        "checks": checks,
    })

expected_matrix = {(loader, model, view) for loader in LOADERS for model in MODELS for view in VIEWS}
missing_matrix = sorted(expected_matrix - set(observed))
duplicate_matrix = sorted((combo, count) for combo, count in observed.items() if count != 1)
if missing_matrix:
    errors.append(f"missing matrix cells: {missing_matrix}")
if duplicate_matrix:
    errors.append(f"non-singleton matrix cells: {duplicate_matrix}")

with CSV_OUTPUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle)
    writer.writerow(["timestamp_utc", "loader", "model", "view", "run_id", "http_status", "bytes", "actual_sha256", "requested_sha256", "screenshot_path", "screenshot_sha256"])
    for record in records:
        writer.writerow([
            record["timestamp_utc"], record["loader"], record["model"], record["view"], record["run_id"],
            record["http_status"], record["bytes"], record["actual_sha256"], record["requested_sha256"],
            record["screenshot_path"], record["screenshot_sha256"],
        ])

CONTACT_DIR.mkdir(parents=True, exist_ok=True)
for loader in LOADERS:
    for model in MODELS:
        canvas = Image.new("RGB", (800, 1040), (245, 246, 248))
        draw = ImageDraw.Draw(canvas)
        draw.text((16, 10), f"{loader} / {model} — 10 current-hash WebGL loads", fill=(20, 24, 30))
        for index, view in enumerate(VIEWS):
            screenshot = QA / "renders" / f"{loader}-{model}" / f"{index + 1:02d}-{view}.png"
            with Image.open(screenshot) as image:
                thumb = image.convert("RGB")
                thumb.thumbnail((376, 180), Image.Resampling.LANCZOS)
            column = index % 2
            row = index // 2
            x = 16 + column * 392
            y = 42 + row * 198
            canvas.paste(thumb, (x, y + 16))
            draw.text((x, y), f"{index + 1:02d} {view}", fill=(20, 24, 30))
        canvas.save(CONTACT_DIR / f"{loader}-{model}.png", optimize=True)

summary = {
    f"{loader}-{model}": {
        "loads": sum(1 for record in records if record["loader"] == loader and record["model"] == model),
        "views": [record["view"] for record in records if record["loader"] == loader and record["model"] == model],
        "bytes_served": sum(record["bytes"] for record in records if record["loader"] == loader and record["model"] == model),
        "contact_sheet": str((CONTACT_DIR / f"{loader}-{model}.png").relative_to(ROOT)),
    }
    for loader in LOADERS for model in MODELS
}

report = {
    "status": "PASS" if not errors else "FAIL",
    "formal_load_count": len(events),
    "unique_run_id_count": len(set(run_ids)),
    "required_matrix": "2 loaders x 2 current-hash GLBs x 10 views",
    "view_order": VIEWS,
    "current_models_after_all_loads": current_models,
    "summary": summary,
    "total_bytes_served": sum(record["bytes"] for record in records),
    "raw_http_log": str(LOG.relative_to(ROOT)),
    "csv_manifest": str(CSV_OUTPUT.relative_to(ROOT)),
    "records": records,
    "missing_matrix_cells": missing_matrix,
    "non_singleton_matrix_cells": duplicate_matrix,
    "errors": errors,
}
OUTPUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: report[key] for key in ["status", "formal_load_count", "unique_run_id_count", "current_models_after_all_loads", "summary", "total_bytes_served", "errors"]}, indent=2))
raise SystemExit(1 if errors else 0)
