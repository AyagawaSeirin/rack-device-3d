#!/usr/bin/env python3
"""Materialize the final browser-load JSON into an audit-friendly CSV."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "qa" / "webgl-loads" / "load-events.json"
target = ROOT / "qa" / "viewer-load-evidence.csv"
records = json.loads(source.read_text(encoding="utf-8"))["records"]
fields = [
    "sequence", "started_utc", "completed_utc", "viewer", "renderer", "webgl",
    "model", "model_sha256", "expected_file_bytes", "view", "run", "model_url",
    "load_duration_ms", "resource_duration_ms", "transfer_size_bytes",
    "decoded_body_size_bytes", "mesh_node_count", "bounds_xyz_mm", "screenshot", "status",
]
with target.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    for record in records:
        row = dict(record)
        row["bounds_xyz_mm"] = " x ".join(f"{value:.6f}" for value in row["bounds_xyz_mm"])
        writer.writerow({field: row[field] for field in fields})
