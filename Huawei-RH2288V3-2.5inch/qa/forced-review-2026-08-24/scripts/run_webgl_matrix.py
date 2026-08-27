#!/usr/bin/env python3
"""Drive two independent Playwright CLI sessions through the 40-load matrix."""

from __future__ import annotations

import json
import argparse
import subprocess
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode


ROOT = Path(__file__).resolve().parents[3]
REVIEW = ROOT / "qa" / "forced-review-2026-08-24"
PWCLI = Path("/root/.codex/skills/playwright/scripts/playwright_cli.sh")
BASE = "http://127.0.0.1:8877/qa/forced-review-2026-08-24/viewers"
VIEWS = ("front", "rear", "left", "right", "top", "bottom", "frontLeft", "frontRight", "rearLeft", "rearRight")
MODELS = {
    "standard": {
        "sha256": "daa3ff261e7f7e40b9e3566ebff5430c8dafe78054bec673487cf9828a6e34ee",
        "bytes": 26207588,
    },
    "web": {
        "sha256": "10e11be59a635642e8f3ec289e12766b1a028384ab73edc0060792ff2ae9d570",
        "bytes": 10089824,
    },
}
SESSIONS = {"three": "rh2288forcedthree", "babylon": "rh2288forcedbabylon"}
EVAL = "JSON.stringify({...document.body.dataset,title:document.title})"


def command(*args: str, timeout: int = 90) -> str:
    completed = subprocess.run(
        [str(PWCLI), *args], cwd=ROOT.parent, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout,
    )
    if completed.returncode:
        raise RuntimeError(f"command failed: {' '.join(args)}\n{completed.stdout}")
    return completed.stdout


def read_dataset(session: str) -> dict:
    raw = command("--session", session, "--raw", "eval", EVAL)
    return json.loads(json.loads(raw.strip()))


def run_engine(engine: str) -> list[dict]:
    session = SESSIONS[engine]
    records: list[dict] = []
    for variant, expected in MODELS.items():
        for view in VIEWS:
            nonce = f"20260824-{engine}-{variant}-{view}-{uuid.uuid4().hex}"
            query = urlencode({
                "model": variant,
                "view": view,
                "sha256": expected["sha256"],
                "nonce": nonce,
            })
            url = f"{BASE}/{engine}.html?{query}"
            command("--session", session, "goto", url)
            data = {}
            for _ in range(6):
                data = read_dataset(session)
                if data.get("ready") == "1" or data.get("error"):
                    break
                time.sleep(1)
            if data.get("ready") != "1":
                raise RuntimeError(f"{engine}/{variant}/{view} did not become ready: {data}")
            if data.get("loadedSha256") != expected["sha256"]:
                raise RuntimeError(f"{engine}/{variant}/{view} hash mismatch: {data}")
            if int(data.get("loadedBytes", "0")) != expected["bytes"]:
                raise RuntimeError(f"{engine}/{variant}/{view} byte-size mismatch: {data}")
            screenshot = REVIEW / "renders" / engine / variant / f"{view}.png"
            screenshot.parent.mkdir(parents=True, exist_ok=True)
            screenshot_error = None
            for _ in range(3):
                try:
                    command("--session", session, "screenshot", "--filename", str(screenshot))
                    screenshot_error = None
                    break
                except RuntimeError as error:
                    screenshot_error = error
                    time.sleep(2)
            if screenshot_error is not None:
                raise screenshot_error
            if not screenshot.is_file() or screenshot.stat().st_size < 100_000:
                raise RuntimeError(f"invalid screenshot {screenshot}")
            record = {
                "sequence": len(records) + 1,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "engine": engine,
                "variant": variant,
                "view": view,
                "expected_sha256": expected["sha256"],
                "loaded_sha256": data["loadedSha256"],
                "loaded_bytes": int(data["loadedBytes"]),
                "nonce": nonce,
                "title": data["title"],
                "screenshot": str(screenshot.relative_to(ROOT)),
                "status": "PASS",
            }
            records.append(record)
            partial = {
                "status": "IN_PROGRESS",
                "engine": engine,
                "completed": len(records),
                "records": records,
            }
            (REVIEW / f"load-matrix-{engine}-partial.json").write_text(
                json.dumps(partial, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            print(f"PASS {engine} {variant} {view} {data['loadedSha256'][:12]}", flush=True)
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--babylon-only", action="store_true")
    args = parser.parse_args()
    if args.babylon_only:
        three_partial = json.loads((REVIEW / "load-matrix-three-partial.json").read_text(encoding="utf-8"))
        if three_partial.get("completed") != 20:
            raise RuntimeError("Three.js partial matrix is not complete")
        records = list(three_partial["records"])
        records.extend(run_engine("babylon"))
    else:
        for path in (REVIEW / "http-loads.jsonl", REVIEW / "load-matrix.json"):
            if path.exists():
                path.unlink()
        records = []
        for engine in SESSIONS:
            records.extend(run_engine(engine))
    expected_keys = {
        (engine, variant, view)
        for engine in SESSIONS for variant in MODELS for view in VIEWS
    }
    actual_keys = {(record["engine"], record["variant"], record["view"]) for record in records}
    if len(records) != 40 or actual_keys != expected_keys:
        raise RuntimeError(f"incomplete matrix: {len(records)} records")
    result = {
        "status": "PASS",
        "load_count": len(records),
        "engines": list(SESSIONS),
        "variants": MODELS,
        "views": list(VIEWS),
        "records": records,
    }
    (REVIEW / "load-matrix.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("MATRIX PASS 40", flush=True)


if __name__ == "__main__":
    main()
