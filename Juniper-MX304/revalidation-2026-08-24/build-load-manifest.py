#!/usr/bin/env python3
"""Validate the 40 WebGL loads and build stable JSON/CSV evidence manifests."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path("/root/Project/rack-device-3d/Juniper-MX304")
RUN = ROOT / "revalidation-2026-08-24"
LOG = RUN / "logs/server-loads.jsonl"
OUT_JSON = RUN / "loads/load-manifest.json"
OUT_CSV = RUN / "loads/load-manifest.csv"
VIEWS = ["front", "rear", "left", "right", "top", "bottom", "front_left", "front_right", "rear_left", "rear_right"]
EXPECTED = {
    "standard": {
        "sha256": "6bd23219b2467b756de4d6f8d990ef539a0719136a28b7d8e9ae2b2ec34c3332",
        "byte_size": 15969012,
    },
    "web": {
        "sha256": "7f240baeb6ce9e8751e49bae90b0a2b40478d75dd76c673f9e2691fe9e9fc9e5",
        "byte_size": 2373988,
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


records = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
glb_by_id = {}
ready_by_id = {}
for record in records:
    load_id = record.get("query", {}).get("load_id")
    if not load_id:
        continue
    if record.get("record_type") == "glb_response":
        glb_by_id[load_id] = record
    elif record.get("record_type") == "viewer_ready_proof":
        ready_by_id[load_id] = record

rows = []
errors = []
for loader in ("three", "babylon"):
    for variant in ("standard", "web"):
        for index, view in enumerate(VIEWS, 1):
            load_id = f"{loader}-{variant}-{index:02d}-{view}"
            glb = glb_by_id.get(load_id)
            ready = ready_by_id.get(load_id)
            screenshot = RUN / "loads" / loader / variant / f"{index:02d}-{view}.png"
            expected = EXPECTED[variant]
            checks = {
                "glb_response_present": glb is not None,
                "glb_http_200": glb is not None and glb.get("response_status") == 200,
                "glb_sha_current": glb is not None and glb.get("sha256") == expected["sha256"],
                "glb_size_current": glb is not None and glb.get("byte_size") == expected["byte_size"],
                "query_loader_matches": glb is not None and glb.get("query", {}).get("loader") == loader,
                "query_variant_matches": glb is not None and glb.get("query", {}).get("variant") == variant,
                "query_view_matches": glb is not None and glb.get("query", {}).get("view") == view,
                "ready_proof_present": ready is not None,
                "ready_http_200": ready is not None and ready.get("response_status") == 200,
                "qa_ready_true": ready is not None and ready.get("query", {}).get("qa_ready") == "true",
                "body_ready_true": ready is not None and ready.get("query", {}).get("body_ready") == "true",
                "body_error_null": ready is not None and ready.get("query", {}).get("body_error") == "null",
                "screenshot_present": screenshot.is_file(),
            }
            row = {
                "load_id": load_id,
                "loader": loader,
                "variant": variant,
                "view": view,
                "expected_sha256": expected["sha256"],
                "served_sha256": glb.get("sha256") if glb else None,
                "served_byte_size": glb.get("byte_size") if glb else None,
                "glb_response_status": glb.get("response_status") if glb else None,
                "glb_timestamp_utc": glb.get("timestamp_utc") if glb else None,
                "ready_timestamp_utc": ready.get("timestamp_utc") if ready else None,
                "screenshot_path": str(screenshot),
                "screenshot_sha256": sha256(screenshot) if screenshot.is_file() else None,
                "checks": checks,
                "status": "PASS" if all(checks.values()) else "FAIL",
            }
            if row["status"] != "PASS":
                errors.append({"load_id": load_id, "failed_checks": [name for name, value in checks.items() if not value]})
            rows.append(row)

summary = {
    "schema": "mx304-current-hash-webgl-load-proof-v1",
    "status": "PASS" if len(rows) == 40 and not errors else "REWORK",
    "expected_total_loads": 40,
    "actual_validated_loads": sum(row["status"] == "PASS" for row in rows),
    "loader_counts": Counter(row["loader"] for row in rows if row["status"] == "PASS"),
    "variant_counts": Counter(row["variant"] for row in rows if row["status"] == "PASS"),
    "view_counts": Counter(row["view"] for row in rows if row["status"] == "PASS"),
    "expected_models": EXPECTED,
    "errors": errors,
    "loads": rows,
}
OUT_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=[
        "load_id", "loader", "variant", "view", "expected_sha256", "served_sha256",
        "served_byte_size", "glb_response_status", "glb_timestamp_utc", "ready_timestamp_utc",
        "screenshot_path", "screenshot_sha256", "status",
    ])
    writer.writeheader()
    for row in rows:
        writer.writerow({key: row[key] for key in writer.fieldnames})

print(json.dumps({key: summary[key] for key in ["status", "expected_total_loads", "actual_validated_loads", "loader_counts", "variant_counts", "view_counts", "errors"]}, indent=2))
if summary["status"] != "PASS":
    raise SystemExit(1)
