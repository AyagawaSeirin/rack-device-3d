#!/usr/bin/env python3
"""Validate the prescribed 40 fresh viewer loads and build review sheets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


COMBINATIONS = ("three-standard", "three-web", "babylon-standard", "babylon-web")
VIEWS = ("front", "rear", "left", "right", "top", "bottom",
         "front-left", "front-right", "rear-left", "rear-right")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sheet(items: list[tuple[str, Path]], output: Path, columns: int = 5) -> None:
    thumb_w, thumb_h, label_h = 300, 225, 24
    rows = (len(items) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * thumb_w, rows * (thumb_h + label_h)), "#17191d")
    draw = ImageDraw.Draw(canvas)
    for index, (label, path) in enumerate(items):
        image = Image.open(path).convert("RGB")
        image.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x0 = (index % columns) * thumb_w
        y0 = (index // columns) * (thumb_h + label_h)
        x = x0 + (thumb_w - image.width) // 2
        y = y0 + (thumb_h - image.height) // 2
        canvas.paste(image, (x, y))
        draw.rectangle((x0, y0 + thumb_h, x0 + thumb_w, y0 + thumb_h + label_h), fill="#111318")
        draw.text((x0 + 7, y0 + thumb_h + 5), label, fill="#f1f2f4")
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, optimize=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("model_root", type=Path)
    parser.add_argument("standard_sha256")
    parser.add_argument("web_sha256")
    args = parser.parse_args()
    evidence = args.model_root.resolve() / "qa/rotation-review/after/static-loads"
    expected_hash = {"standard": args.standard_sha256, "web": args.web_sha256}
    expected_viewer_version = {
        "three": "rotation-review-20260827-v3",
        "babylon": "rotation-review-20260827-v4",
    }
    errors: list[str] = []
    all_events: list[dict] = []
    combo_summary: dict[str, dict] = {}
    all_sheet_items: list[tuple[str, Path]] = []

    for combo in COMBINATIONS:
        event_path = evidence / combo / "load-events.json"
        if not event_path.exists():
            errors.append(f"missing {event_path}")
            continue
        data = json.loads(event_path.read_text())
        events = data.get("events", [])
        if len(events) != 10:
            errors.append(f"{combo}: expected 10 events, got {len(events)}")
        if [event.get("view") for event in events] != list(VIEWS):
            errors.append(f"{combo}: prescribed view sequence mismatch")
        variant = combo.rsplit("-", 1)[1]
        viewer = combo.split("-", 1)[0]
        image_items: list[tuple[str, Path]] = []
        for event in events:
            screenshot = Path(event.get("screenshot", ""))
            checks = {
                "viewer": event.get("viewer") == viewer,
                "viewer_version": event.get("viewer_code_version") == expected_viewer_version[viewer],
                "hash": event.get("asset_sha256") == expected_hash[variant],
                "webgl2": event.get("webgl2") is True,
                "loaded": event.get("loaded") is True,
                "ready": event.get("ready") is True,
                "errors": event.get("errors") == [],
                "screenshot": screenshot.exists(),
            }
            failed = [key for key, passed in checks.items() if not passed]
            if failed:
                errors.append(f"{combo} load {event.get('load_index')}: failed {failed}")
            enriched = dict(event)
            enriched["combination"] = combo
            enriched["checks"] = checks
            if screenshot.exists():
                enriched["screenshot_sha256"] = file_sha256(screenshot)
                image_items.append((f"{combo} / {event['view']}", screenshot))
                all_sheet_items.append((f"{combo} / {event['view']}", screenshot))
            all_events.append(enriched)
        combo_sheet = evidence / combo / "ten-load-contact-sheet.png"
        if image_items:
            sheet(image_items, combo_sheet)
        combo_summary[combo] = {
            "load_count": len(events),
            "asset_sha256": expected_hash[variant],
            "viewer": viewer,
            "contact_sheet": str(combo_sheet),
            "pass": not any(error.startswith(combo) for error in errors),
        }

    all_sheet = evidence / "static-40-loads-contact-sheet.png"
    if all_sheet_items:
        sheet(all_sheet_items, all_sheet)
    report = {
        "schema": "rack-device-static-40-load-gate-v1",
        "model_root": str(args.model_root.resolve()),
        "required_combinations": list(COMBINATIONS),
        "required_views": list(VIEWS),
        "total_required_loads": 40,
        "total_observed_loads": len(all_events),
        "fresh_navigation_per_load": True,
        "viewer_code_versions_required": expected_viewer_version,
        "expected_hashes": expected_hash,
        "combinations": combo_summary,
        "all_contact_sheet": str(all_sheet),
        "events": all_events,
        "errors": errors,
        "pass": len(all_events) == 40 and not errors,
    }
    output = evidence / "static-40-loads.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"output": str(output), "loads": len(all_events), "errors": errors, "pass": report["pass"]}, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
