#!/usr/bin/env python3
"""Validate and aggregate the 40 final live WebGL load records."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
EVENT_DIR = ROOT / "qa" / "load-evidence" / "final-events"
VIEWS = ("front", "rear", "left", "right", "top", "bottom", "front-left", "front-right", "rear-left", "rear-right")
VIEWERS = ("three", "babylon")
MODELS = ("standard", "web")
EXPECTED_DIMS = [0.48240000009536743, 0.04285000078380108, 0.7525149881839752]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    errors: list[str] = []
    entries: list[dict[str, object]] = []
    expected = {(viewer, model, view) for viewer in VIEWERS for model in MODELS for view in VIEWS}
    found: set[tuple[str, str, str]] = set()
    for event_path in sorted(EVENT_DIR.glob("*.json")):
        event = json.loads(event_path.read_text(encoding="utf-8"))
        key = (event.get("viewer"), event.get("model"), event.get("view"))
        found.add(key)
        if key not in expected:
            errors.append(f"unexpected event key: {key}")
        if event.get("loaded") is not True or event.get("error") is not None:
            errors.append(f"failed page state: {event_path.name}")
        dimensions = event.get("bounds", {}).get("dimensions", [])
        if len(dimensions) != 3 or any(abs(a - b) > 1e-7 for a, b in zip(dimensions, EXPECTED_DIMS)):
            errors.append(f"bounds mismatch: {event_path.name}: {dimensions}")
        screenshot = ROOT / str(event.get("screenshot", ""))
        if not screenshot.is_file():
            errors.append(f"missing screenshot: {event_path.name}")
            continue
        with Image.open(screenshot) as image:
            size = list(image.size)
            extrema = image.convert("RGB").getextrema()
        if size != [1280, 720]:
            errors.append(f"wrong screenshot size: {screenshot}: {size}")
        if all(low == high for low, high in extrema):
            errors.append(f"blank screenshot: {screenshot}")
        comparison = ROOT / "qa" / "comparisons" / "final" / screenshot.name
        if not comparison.is_file():
            errors.append(f"missing comparison: {comparison.name}")
        entries.append({
            **event,
            "event": str(event_path.relative_to(ROOT)),
            "screenshot_bytes": screenshot.stat().st_size,
            "screenshot_sha256": sha256(screenshot),
            "screenshot_size": size,
            "comparison": str(comparison.relative_to(ROOT)),
        })
    missing = sorted(expected - found)
    duplicate_count = len(entries) - len(found)
    if missing:
        errors.append(f"missing event keys: {missing}")
    if duplicate_count:
        errors.append(f"duplicate event count: {duplicate_count}")
    if len(entries) != 40:
        errors.append(f"expected 40 events, got {len(entries)}")
    viewers = Counter(entry["viewer"] for entry in entries)
    models = Counter(entry["model"] for entry in entries)
    views = Counter(entry["view"] for entry in entries)
    summary = {
        "schema": "rack-device-webgl-load-evidence-v1",
        "status": "PASS" if not errors else "FAIL",
        "aggregated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "render_count": len(entries),
        "actual_load_render_count": len(entries),
        "unique_combinations": len(found),
        "direct_page_state_and_screenshot": len(entries),
        "recovered_or_inferred": 0,
        "browser": sorted({f'{entry["browser"]} {entry["browserVersion"]}' for entry in entries}),
        "breakdown": {"viewers": dict(viewers), "models": dict(models), "views": dict(views)},
        "errors": errors,
        "events": entries,
    }
    out_dir = ROOT / "qa" / "load-evidence"
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (ROOT / "qa" / "webgl-render-audit.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    with (out_dir / "final-load-events.ndjson").open("w", encoding="utf-8") as handle:
        for entry in entries:
            handle.write(json.dumps(entry, separators=(",", ":")) + "\n")
    print(json.dumps({"status": summary["status"], "loads": len(entries), "unique": len(found), "errors": len(errors)}, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
