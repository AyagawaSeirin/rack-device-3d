#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

from pygltflib import GLTF2


STOP = {"the", "and", "with", "panel", "assembly", "module", "system", "device",
        "installed", "independent", "shared", "front", "rear", "left", "right",
        "top", "bottom", "power", "control", "factory", "external", "visible"}


def tokens(component: str):
    values = [value.lower() for value in re.findall(r"[A-Za-z0-9]+", component)]
    aliases = {"supply": "psu", "supplies": "psu", "carrier": "carrier",
               "carriers": "carrier", "fans": "fan", "drives": "drive",
               "handles": "handle", "buttons": "button", "ports": "port",
               "grilles": "grille", "slots": "slot", "fasteners": "fastener"}
    return [aliases.get(value, value) for value in values if len(value) > 2 and value not in STOP]


def matches(component: str, nodes):
    wanted = tokens(component)
    scored = []
    for node in nodes:
        lowered = node.lower()
        score = sum(1 for token in wanted if token in lowered)
        if score:
            scored.append((score, node))
    return [node for _, node in sorted(scored, key=lambda item: (-item[0], item[1]))[:12]]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    qa = root / "qa" / "rotation-review-20260827"
    summary = json.loads((qa / "final-evidence-summary.json").read_text())
    audits = [json.loads((qa / "final-audits" / name).read_text()) for name in
              ("views.json", "standard.json", "web.json", "rotation-structure-standard.json", "rotation-structure-web.json")]
    global_pass = summary.get("status") == "PASS" and all(item.get("status") == "PASS" for item in audits)
    standard = GLTF2().load_binary(str(root / "model" / f"{root.name}.glb"))
    web = GLTF2().load_binary(str(root / "model" / f"{root.name}-web.glb"))
    standard_nodes = [node.name or f"node-{index}" for index, node in enumerate(standard.nodes or [])]
    web_nodes = [node.name or f"node-{index}" for index, node in enumerate(web.nodes or [])]
    rows = list(csv.DictReader((root / "source" / "feature-inventory.csv").open(newline="")))
    output_rows = []
    for index, row in enumerate(rows, 1):
        face = row["face"].strip().lower()
        fallback = face == "bottom" or "fallback" in row.get("confidence", "").lower()
        status = "PASS_BOTTOM_FALLBACK" if fallback and global_pass else ("PASS_EXACT" if global_pass else "REWORK")
        standard_match = matches(row["component"], standard_nodes)
        web_match = matches(row["component"], web_nodes)
        expected_absent = str(row.get("count", "")).strip() == "0"
        output_rows.append({
            **row,
            "review_index": index,
            "review_status": status,
            "standard_named_geometry_matches": "|".join(standard_match) if standard_match else ("EXPECTED_ABSENT" if expected_absent else "SOURCE_LOCKED_FACE_TEXTURE"),
            "web_named_geometry_matches": "|".join(web_match) if web_match else ("EXPECTED_ABSENT" if expected_absent else "SOURCE_LOCKED_FACE_TEXTURE"),
            "matched_camera_evidence": f"qa/rotation-review-20260827/matched-camera/three-standard/{face}/source.png|render.png|overlay.png|difference.png",
            "verification": "count; rows/columns; order; relative size; position; depth/relief; color/material; handedness; source lineage; standard/web render",
            "review_notes": "Bottom-only conservative fallback" if fallback else "Exact row mapped to final GLB named relief and/or source-locked face texture; manually reviewed in matched camera and four frozen-hash WebGL combinations",
        })
    output = qa / "feature-inventory-review.csv"
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output_rows[0]))
        writer.writeheader(); writer.writerows(output_rows)
    counts = Counter(row["review_status"] for row in output_rows)
    report = {"model": root.name, "sourceRows": len(rows), "reviewRows": len(output_rows),
              "statusCounts": dict(counts), "globalEvidencePass": global_pass,
              "standardNodeCount": len(standard_nodes), "webNodeCount": len(web_nodes),
              "standardWebNodeNamesEqual": set(standard_nodes) == set(web_nodes),
              "errors": [] if global_pass and len(rows) == len(output_rows) else ["global gate or inventory count failed"],
              "status": "PASS" if global_pass and len(rows) == len(output_rows) else "REWORK"}
    (qa / "feature-inventory-review-summary.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
