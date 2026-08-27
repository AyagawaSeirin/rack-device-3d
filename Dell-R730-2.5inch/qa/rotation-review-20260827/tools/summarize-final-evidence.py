#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


VIEW_ORDER = ["front", "rear", "left", "right", "top", "bottom",
              "front-left", "front-right", "rear-left", "rear-right"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    qa = root / "qa" / "rotation-review-20260827"
    frozen = json.loads((qa / "frozen-hashes.json").read_text())
    frozen_checks = {}
    for key in ("standard", "web"):
        current = sha(root / frozen[key]["path"])
        frozen_checks[key] = {"expected": frozen[key]["sha256"], "actual": current,
                              "match": current == frozen[key]["sha256"]}
    for key in ("three", "babylon"):
        current = sha(root / frozen["viewers"][key]["path"])
        frozen_checks[f"viewer-{key}"] = {
            "expected": frozen["viewers"][key]["sha256"], "actual": current,
            "match": current == frozen["viewers"][key]["sha256"]}

    load_combos, all_nonces = [], []
    for viewer in ("three", "babylon"):
        for variant in ("standard", "web"):
            combo = qa / "static-40-loads" / viewer / variant
            manifest = json.loads((combo / "load-manifest.json").read_text())
            loads = manifest.get("loads", [])
            nonces = [item.get("nonce") for item in loads]
            all_nonces.extend(nonces)
            pngs = sorted(combo.glob("[0-9][0-9]-*.png"))
            checks = {
                "loadCount10": len(loads) == 10 and manifest.get("loadCount") == 10,
                "pngCount10": len(pngs) == 10,
                "viewOrderExact": [item.get("name") for item in loads] == VIEW_ORDER,
                "cacheBusted": bool(manifest.get("cacheBusted")) and len(set(nonces)) == 10,
                "independentPageNavigations": bool(manifest.get("independentPageNavigations")),
                "webgl2": all(item.get("runtime", {}).get("webgl2") is True for item in loads),
                "overlayAbsent": all(item.get("runtime", {}).get("overlayVisible") is False for item in loads),
                "frozenFrustum": all(item.get("runtime", {}).get("frozenFrustum") is True for item in loads),
                "nearFar": all(item.get("runtime", {}).get("near") == .01 and item.get("runtime", {}).get("far") == 10 for item in loads),
            }
            load_combos.append({"viewer": viewer, "variant": variant,
                                "modelBase": manifest.get("modelBase"), "checks": checks,
                                "pass": all(checks.values())})

    rotation_combos = []
    for viewer in ("three", "babylon"):
        for variant in ("standard", "web"):
            combo = qa / "final-rotation" / viewer / variant
            manifest = json.loads((combo / "rotation-manifest.json").read_text())
            analysis = json.loads((combo / "analysis.json").read_text())
            checks = {
                "analysisPass": analysis.get("status") == "PASS" and analysis.get("errorCount") == 0,
                "yaw72x5": manifest.get("yawFrames") == 72 and manifest.get("yawStepDegrees") == 5 and len(list((combo / "yaw-frames").glob("*.png"))) == 72,
                "pitchChecker32": manifest.get("pitchCheckerFrames") == 32 and len(list((combo / "pitch-checker").glob("*.png"))) == 32,
                "stable18": manifest.get("stableFrames") == 18 and len(list((combo / "stable-frames").glob("*.png"))) == 18,
                "webgl2": manifest.get("runtime", {}).get("webgl2") is True,
                "overlayAbsent": manifest.get("runtime", {}).get("overlayVisible") is False,
                "frozenFrustum": manifest.get("runtime", {}).get("frozenFrustum") is True,
                "nearFar": manifest.get("runtime", {}).get("near") == .01 and manifest.get("runtime", {}).get("far") == 10,
            }
            rotation_combos.append({"viewer": viewer, "variant": variant,
                                    "runtime": manifest.get("runtime"), "checks": checks,
                                    "pass": all(checks.values())})

    result = {
        "model": root.name,
        "frozenHashChecks": frozen_checks,
        "loads": {"required": 40, "actual": sum(10 for item in load_combos if item["checks"]["loadCount10"]),
                  "uniqueNonces": len(set(all_nonces)), "combos": load_combos},
        "rotation": {"yawFrames": 72 * len(rotation_combos),
                     "pitchCheckerFrames": 32 * len(rotation_combos),
                     "stableFrames": 18 * len(rotation_combos), "combos": rotation_combos},
    }
    errors = []
    if not all(item["match"] for item in frozen_checks.values()): errors.append("frozen hash mismatch")
    if len(all_nonces) != 40 or len(set(all_nonces)) != 40 or not all(item["pass"] for item in load_combos): errors.append("40-load gate failed")
    if not all(item["pass"] for item in rotation_combos): errors.append("rotation gate failed")
    result.update({"errors": errors, "errorCount": len(errors), "status": "PASS" if not errors else "REWORK"})
    output = qa / "final-evidence-summary.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"model": root.name, "status": result["status"], "errorCount": len(errors),
                      "loads": len(all_nonces), "uniqueNonces": len(set(all_nonces)),
                      "yawFrames": result["rotation"]["yawFrames"]}, indent=2))


if __name__ == "__main__":
    main()
