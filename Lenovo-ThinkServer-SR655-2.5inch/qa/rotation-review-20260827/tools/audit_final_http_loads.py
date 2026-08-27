#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import parse_qs


ROTATION_ROOT = Path(__file__).resolve().parents[1]
AFTER = ROTATION_ROOT / "after"


def main() -> None:
    summary = json.loads((AFTER / "browser-gate-summary.json").read_text(encoding="utf-8"))
    expected: dict[str, dict] = {}
    for engine in ("three", "babylon"):
        for variant in ("standard", "web"):
            load_id = f"after-rotation-{engine}-{variant}"
            expected[load_id] = {"engine": engine, "variant": variant, "kind": "rotation"}
    for record in summary["static_loads"]:
        expected[record["load_id"]] = {
            "engine": record["state"]["engine"],
            "variant": record["state"]["variant"],
            "kind": "static",
            "view": record["name"],
        }
    records = []
    for line in (AFTER / "http-loads.jsonl").read_text(encoding="utf-8").splitlines():
        item = json.loads(line)
        if not item["path"].endswith(".glb"):
            continue
        query = parse_qs(item["query"])
        load_id = query.get("load", [""])[0]
        if load_id not in expected:
            continue
        variant = expected[load_id]["variant"]
        expected_model = summary["models"][variant]
        item_hash = query.get("sha256", [""])[0]
        records.append({
            "load_id": load_id,
            **expected[load_id],
            "request_path": item["path"],
            "request_sha256": item_hash,
            "expected_sha256": expected_model["sha256"],
            "resolved_bytes": item["resolved_bytes"],
            "expected_bytes": expected_model["bytes"],
            "status_200": '" 200 ' in item["status_line"],
            "status": "PASS" if item_hash == expected_model["sha256"] and item["resolved_bytes"] == expected_model["bytes"] and '" 200 ' in item["status_line"] else "FAIL",
        })
    by_load: dict[str, list[dict]] = {}
    for record in records:
        by_load.setdefault(record["load_id"], []).append(record)
    unique = [items[-1] for load_id, items in sorted(by_load.items())]
    missing = sorted(set(expected) - set(by_load))
    failures = [record for record in unique if record["status"] != "PASS"]
    report = {
        "status": "PASS" if len(unique) == 44 and not missing and not failures else "FAIL",
        "expected_unique_glb_loads": 44,
        "observed_unique_final_hash_glb_loads": len(unique),
        "static_loads": sum(record["kind"] == "static" for record in unique),
        "rotation_loads": sum(record["kind"] == "rotation" for record in unique),
        "missing_load_ids": missing,
        "failures": failures,
        "records": unique,
    }
    (AFTER / "http-final-hash-audit.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("status", "observed_unique_final_hash_glb_loads", "static_loads", "rotation_loads")}))
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
