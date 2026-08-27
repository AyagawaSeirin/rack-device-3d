#!/usr/bin/env python3
"""Run the two required WebGL loaders against both current GLBs at ten views."""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path


MODEL_ROOT = Path(__file__).resolve().parents[3]
VALIDATION_LABEL = os.environ.get("SR655_REVALIDATION_LABEL", "revalidation-2026-08-24")
OUT = MODEL_ROOT / "qa" / VALIDATION_LABEL
PWCLI = Path("/root/.codex/skills/playwright/scripts/playwright_cli.sh")
SESSION = os.environ.get("SR655_PLAYWRIGHT_SESSION", "sr655reval")
BASE_URL = "http://127.0.0.1:8765"
VIEWS = (
    "front",
    "rear",
    "right",
    "left",
    "top",
    "bottom",
    "frontLeft",
    "frontRight",
    "rearLeft",
    "rearRight",
)
MODELS = {
    "standard": MODEL_ROOT / "model" / "Lenovo-ThinkServer-SR655-2.5inch.glb",
    "web": MODEL_ROOT / "model" / "Lenovo-ThinkServer-SR655-2.5inch-web.glb",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run_cli(*args: str) -> str:
    process = subprocess.run(
        [str(PWCLI), f"-s={SESSION}", *args],
        cwd=MODEL_ROOT,
        text=True,
        capture_output=True,
        timeout=90,
    )
    output = process.stdout + process.stderr
    if process.returncode:
        raise RuntimeError(f"playwright-cli failed ({process.returncode}): {' '.join(args)}\n{output}")
    return output


def parse_result(output: str) -> dict:
    match = re.search(r"### Result\n(\{.*?\})\n### Ran Playwright code", output, re.DOTALL)
    if not match:
        raise RuntimeError(f"could not parse Playwright result:\n{output}")
    return json.loads(match.group(1))


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pre = {
        key: {"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path)}
        for key, path in MODELS.items()
    }
    records: list[dict] = []
    run_cli("open", "about:blank")
    run_cli("resize", "1280", "720")

    index = 0
    for loader in ("three", "babylon"):
        for variant in ("standard", "web"):
            for view in VIEWS:
                index += 1
                run_id = f"R{index:03d}-{loader}-{variant}-{view}"
                query = urllib.parse.urlencode(
                    {
                        "model": variant,
                        "view": view,
                        "run": run_id,
                        "sha256": pre[variant]["sha256"],
                    }
                )
                url = f"{BASE_URL}/qa/{VALIDATION_LABEL}/viewers/{loader}.html?{query}"
                started = utc_now()
                goto_output = run_cli("goto", url)
                result_output = run_cli(
                    "run-code",
                    "async (page) => { await page.waitForFunction(() => document.body.dataset.ready === '1' || document.body.dataset.error, null, {timeout: 30000}); return await page.evaluate(() => ({title: document.title, dataset: Object.fromEntries(Object.entries(document.body.dataset)), glbResources: performance.getEntriesByType('resource').filter((entry) => entry.name.includes('.glb')).map((entry) => ({name: entry.name, transferSize: entry.transferSize, encodedBodySize: entry.encodedBodySize, decodedBodySize: entry.decodedBodySize, duration: entry.duration}))})); }",
                )
                page_result = parse_result(result_output)
                dataset = page_result.get("dataset", {})
                if dataset.get("ready") != "1" or dataset.get("error"):
                    raise RuntimeError(f"viewer did not reach ready state for {run_id}: {page_result}")
                for field, expected in {
                    "loader": loader,
                    "variant": variant,
                    "view": view,
                    "run": run_id,
                    "sha256": pre[variant]["sha256"],
                }.items():
                    if dataset.get(field) != expected:
                        raise RuntimeError(f"dataset mismatch {field} for {run_id}: {dataset.get(field)!r} != {expected!r}")
                resources = page_result.get("glbResources", [])
                if len(resources) != 1 or f"load={run_id}" not in resources[0].get("name", ""):
                    raise RuntimeError(f"missing unique GLB resource load for {run_id}: {resources}")

                screenshot = OUT / "renders" / loader / variant / f"{view}.png"
                screenshot.parent.mkdir(parents=True, exist_ok=True)
                screenshot_output = run_cli("screenshot", f"--filename={screenshot.relative_to(MODEL_ROOT)}")
                if not screenshot.exists() or screenshot.stat().st_size == 0:
                    raise RuntimeError(f"screenshot missing for {run_id}: {screenshot_output}")

                console_match = re.search(r"Console: (\d+) errors?, (\d+) warnings?", goto_output)
                console_errors = int(console_match.group(1)) if console_match else None
                console_warnings = int(console_match.group(2)) if console_match else None
                records.append(
                    {
                        "index": index,
                        "run_id": run_id,
                        "loader": loader,
                        "model_variant": variant,
                        "view": view,
                        "model_path": str(MODELS[variant]),
                        "model_bytes": pre[variant]["bytes"],
                        "model_sha256": pre[variant]["sha256"],
                        "page_url": url,
                        "page_title": page_result.get("title"),
                        "dataset_ready": dataset.get("ready"),
                        "dataset_model_url": dataset.get("modelUrl"),
                        "glb_resource_url": resources[0].get("name"),
                        "glb_transfer_size": resources[0].get("transferSize"),
                        "glb_encoded_body_size": resources[0].get("encodedBodySize"),
                        "glb_decoded_body_size": resources[0].get("decodedBodySize"),
                        "glb_duration_ms": resources[0].get("duration"),
                        "console_errors_at_navigation": console_errors,
                        "console_warnings_at_navigation": console_warnings,
                        "screenshot_path": str(screenshot),
                        "screenshot_bytes": screenshot.stat().st_size,
                        "screenshot_sha256": sha256(screenshot),
                        "started_utc": started,
                        "completed_utc": utc_now(),
                        "status": "PASS",
                    }
                )
                print(f"{index:02d}/40 PASS {loader} {variant} {view}", flush=True)

    post = {
        key: {"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path)}
        for key, path in MODELS.items()
    }
    if pre != post:
        raise RuntimeError(f"model files changed during validation: pre={pre} post={post}")

    http_log = OUT / "http-requests.jsonl"
    http_records = [json.loads(line) for line in http_log.read_text(encoding="utf-8").splitlines() if line]
    required_run_ids = {record["run_id"] for record in records}
    glb_http = [
        record
        for record in http_records
        if ".glb?" in record.get("path", "")
        and any(f"load={urllib.parse.quote(run_id)}" in record.get("path", "") for run_id in required_run_ids)
    ]
    if len(glb_http) != 40:
        raise RuntimeError(f"expected 40 uniquely identified GLB HTTP requests, found {len(glb_http)}")

    manifest = {
        "status": "PASS",
        "requirement": "Two independent WebGL loaders x two current GLBs x ten required views = 40 real loads",
        "loaders": ["Three.js GLTFLoader", "Babylon.js SceneLoader"],
        "views": list(VIEWS),
        "model_preflight": pre,
        "model_postflight": post,
        "load_count": len(records),
        "unique_run_id_count": len({record["run_id"] for record in records}),
        "unique_glb_http_request_count": len(glb_http),
        "http_request_log": str(http_log),
        "records": records,
    }
    (OUT / "load-manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with (OUT / "load-manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)

    run_cli("close")
    print(json.dumps({"status": "PASS", "load_count": 40, "manifest": str(OUT / 'load-manifest.json')}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
