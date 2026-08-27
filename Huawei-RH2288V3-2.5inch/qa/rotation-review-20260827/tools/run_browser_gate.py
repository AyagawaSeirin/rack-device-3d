#!/usr/bin/env python3
"""Capture real-browser WebGL2 orbit and load-gate evidence via Playwright CLI.

This orchestrator intentionally shells out to the installed playwright-cli wrapper;
it does not import Playwright or create a Playwright test suite.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

from PIL import Image, ImageDraw


ROTATION_ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = Path(__file__).resolve().parents[3]
PWCLI = Path("/root/.codex/skills/playwright/scripts/playwright_cli.sh")
ENGINES = ("three", "babylon")
VARIANTS = ("standard", "web")
STATIC_VIEWS = (
    ("front", 0, 0, "light"),
    ("rear", 180, 0, "dark"),
    ("left", 270, 0, "light"),
    ("right", 90, 0, "dark"),
    ("top", 0, 88, "light"),
    ("bottom", 0, -88, "dark"),
    ("front-left", 315, 18, "light"),
    ("front-right", 45, 18, "dark"),
    ("rear-left", 225, 18, "light"),
    ("rear-right", 135, 18, "dark"),
)
PITCH_VIEWS = tuple(
    (f"yaw-{yaw:03d}-pitch-{pitch:+03d}", yaw, pitch)
    for pitch in (30, -30) for yaw in (0, 90, 180, 270)
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run(command: list[str], timeout: int = 180) -> str:
    completed = subprocess.run(
        command,
        cwd=ROTATION_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(command)}\n{completed.stdout}")
    return completed.stdout


def pw(session: str, *args: str, timeout: int = 180) -> str:
    return run([str(PWCLI), f"-s={session}", *args], timeout=timeout)


def parse_result(output: str) -> object:
    match = re.search(r"### Result\n([^\n]+)", output)
    if not match:
        raise RuntimeError(f"playwright-cli result missing:\n{output}")
    raw = match.group(1).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"playwright-cli result is not JSON: {raw}\n{output}") from exc


def model_path(key: str, variant: str) -> Path:
    suffix = "-web" if variant == "web" else ""
    return MODEL_ROOT / "model" / f"{key}{suffix}.glb"


def viewer_url(port: int, key: str, engine: str, variant: str, background: str,
               load_id: str, model_hash: str, yaw: int = 0, pitch: int = 12) -> str:
    query = urlencode({
        "key": key,
        "model": variant,
        "bg": background,
        "load": load_id,
        "sha256": model_hash,
        "yaw": yaw,
        "pitch": pitch,
    })
    return f"http://127.0.0.1:{port}/qa/rotation-review-20260827/viewers/{engine}.html?{query}"


def viewer_provenance() -> dict[str, object]:
    relative = (
        "viewers/three.html",
        "viewers/babylon.html",
        "viewers/vendor/three.module.js",
        "viewers/vendor/GLTFLoader.js",
        "viewers/vendor/babylon.js",
        "viewers/vendor/babylonjs.loaders.min.js",
        "viewers/utils/BufferGeometryUtils.js",
    )
    return {
        item: {"bytes": (ROTATION_ROOT / item).stat().st_size, "sha256": sha256(ROTATION_ROOT / item)}
        for item in relative
    }


def make_contact_sheet(frame_paths: list[Path], output: Path, title: str,
                       columns: int = 12, thumb=(320, 180)) -> None:
    rows = (len(frame_paths) + columns - 1) // columns
    label_h = 24
    canvas = Image.new("RGB", (columns * thumb[0], 42 + rows * (thumb[1] + label_h)), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((10, 12), title, fill="black")
    for index, path in enumerate(frame_paths):
        image = Image.open(path).convert("RGB")
        image.thumbnail(thumb, Image.Resampling.LANCZOS)
        x = (index % columns) * thumb[0] + (thumb[0] - image.width) // 2
        y = 42 + (index // columns) * (thumb[1] + label_h)
        canvas.paste(image, (x, y))
        draw.text((index % columns * thumb[0] + 4, y + thumb[1] + 4), path.stem, fill="black")
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, optimize=True)


def wait_ready(session: str) -> dict[str, object]:
    code = (
        "async page => {"
        "await page.waitForFunction(() => document.body.dataset.ready === '1' || document.body.dataset.error, null, {timeout:30000});"
        "return await page.evaluate(() => ({state:window.qaState?window.qaState():null,error:document.body.dataset.error||null,title:document.title}));"
        "}"
    )
    result = parse_result(pw(session, "run-code", code, timeout=60))
    if result.get("error") or not result.get("state"):
        raise RuntimeError(f"viewer failed: {result}")
    return result


def capture_rotation(stage: str, port: int, key: str, engine: str, variant: str,
                     model_hash: str) -> dict[str, object]:
    combo = f"{engine}-{variant}"
    session = re.sub(r"[^a-z0-9]", "", f"rot{port}{stage}{engine}{variant}")[-42:]
    output_dir = ROTATION_ROOT / stage / "rotation" / engine / variant
    frames_dir = output_dir / "yaw-frames"
    pitch_dir = output_dir / "pitch-frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    pitch_dir.mkdir(parents=True, exist_ok=True)
    url = viewer_url(port, key, engine, variant, "light", f"{stage}-rotation-{combo}", model_hash)
    try:
        pw(session, "open", url, timeout=60)
        pw(session, "resize", "1280", "720", timeout=60)
        pw(session, "snapshot", timeout=60)
        initial = wait_ready(session)
        video_path = output_dir / "continuous-360.webm"
        pw(session, "video-start", str(video_path), timeout=60)
        animation_code = (
            "async page => {const result=await page.evaluate(() => window.qaStartRotation(7200,12));"
            "return {duration_ms:result.duration_ms,animation_frames:result.animation_frames,"
            "first:result.samples[0],last:result.samples[result.samples.length-1],state:await page.evaluate(() => window.qaState())};}"
        )
        animation = parse_result(pw(session, "run-code", animation_code, timeout=90))
        pw(session, "video-stop", timeout=60)

        yaw_paths = [frames_dir / f"frame-{index:03d}-yaw-{index * 5:03d}.jpg" for index in range(72)]
        capture_code = (
            "async page => {const output=" + json.dumps([str(path) for path in yaw_paths]) + ";const records=[];"
            "await page.evaluate(() => window.qaSetBackground('light'));"
            "for(let i=0;i<72;i++){const angle=i*5;const state=await page.evaluate(a=>window.qaSetOrbit(a,12),angle);"
            "await page.waitForTimeout(35);await page.screenshot({path:output[i],type:'jpeg',quality:82});"
            "records.push({index:i,yaw_deg:angle,pitch_deg:12,path:output[i],state});}"
            "return {state:await page.evaluate(() => window.qaState()),frames:records};}"
        )
        yaw_result = parse_result(pw(session, "run-code", capture_code, timeout=240))

        pitch_paths = [pitch_dir / f"{name}.png" for name, _, _ in PITCH_VIEWS]
        pitch_specs = [
            {"name": name, "yaw": yaw_value, "pitch": pitch_value, "path": str(path)}
            for (name, yaw_value, pitch_value), path in zip(PITCH_VIEWS, pitch_paths)
        ]
        pitch_code = (
            "async page => {const specs=" + json.dumps(pitch_specs) + ";const records=[];"
            "await page.evaluate(() => window.qaSetBackground('dark'));"
            "for(const spec of specs){const state=await page.evaluate(s=>window.qaSetOrbit(s.yaw,s.pitch),spec);"
            "await page.waitForTimeout(50);await page.screenshot({path:spec.path,type:'png'});records.push({...spec,state});}"
            "return {state:await page.evaluate(() => window.qaState()),frames:records};}"
        )
        pitch_result = parse_result(pw(session, "run-code", pitch_code, timeout=120))
    finally:
        try:
            pw(session, "close", timeout=30)
        except Exception:
            pass

    yaw_records = []
    for record, path in zip(yaw_result["frames"], yaw_paths):
        yaw_records.append({
            **{key_name: record[key_name] for key_name in ("index", "yaw_deg", "pitch_deg")},
            "path": str(path.relative_to(ROTATION_ROOT)),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    pitch_records = []
    for spec, path in zip(pitch_specs, pitch_paths):
        pitch_records.append({
            "name": spec["name"], "yaw_deg": spec["yaw"], "pitch_deg": spec["pitch"],
            "path": str(path.relative_to(ROTATION_ROOT)), "bytes": path.stat().st_size, "sha256": sha256(path),
        })
    contact_path = output_dir / "yaw-72-contact-sheet.jpg"
    make_contact_sheet(yaw_paths, contact_path, f"{key} · {stage} · {engine} · {variant} · 72 x 5-degree yaw")
    video = {
        "path": str(video_path.relative_to(ROTATION_ROOT)),
        "bytes": video_path.stat().st_size,
        "sha256": sha256(video_path),
        "duration_requested_ms": 7200,
    }
    manifest = {
        "status": "CAPTURED_PENDING_VISUAL_REVIEW",
        "captured_utc": datetime.now(timezone.utc).isoformat(),
        "stage": stage,
        "engine": engine,
        "variant": variant,
        "model_path": str(model_path(key, variant).relative_to(MODEL_ROOT)),
        "model_bytes": model_path(key, variant).stat().st_size,
        "model_sha256": model_hash,
        "viewer_provenance": viewer_provenance(),
        "initial_browser_state": initial,
        "continuous_rotation": {"animation": animation, "video": video},
        "yaw_step_degrees": 5,
        "yaw_frame_count": len(yaw_records),
        "yaw_frames": yaw_records,
        "pitch_frames": pitch_records,
        "contact_sheet": {"path": str(contact_path.relative_to(ROTATION_ROOT)), "bytes": contact_path.stat().st_size, "sha256": sha256(contact_path)},
    }
    manifest_path = output_dir / "rotation-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def capture_static_gate(stage: str, port: int, key: str, engine: str, variant: str,
                        model_hash: str) -> list[dict[str, object]]:
    session = re.sub(r"[^a-z0-9]", "", f"static{port}{stage}{engine}{variant}")[-42:]
    output_dir = ROTATION_ROOT / stage / "static-40-loads" / engine / variant
    output_dir.mkdir(parents=True, exist_ok=True)
    specs = []
    for index, (name, yaw, pitch, background) in enumerate(STATIC_VIEWS, 1):
        load_id = f"{stage}-{engine}-{variant}-{index:02d}-{name}"
        path = output_dir / f"{index:02d}-{name}.png"
        specs.append({
            "index": index, "name": name, "yaw": yaw, "pitch": pitch, "background": background,
            "load_id": load_id, "path": str(path),
            "url": viewer_url(port, key, engine, variant, background, load_id, model_hash, yaw=yaw, pitch=pitch),
        })
    try:
        pw(session, "open", "about:blank", timeout=60)
        pw(session, "resize", "1280", "720", timeout=60)
        pw(session, "snapshot", timeout=60)
        code = (
            "async page => {const specs=" + json.dumps(specs) + ";const errors=[];"
            "page.on('console',message=>{if(message.type()==='error')errors.push({type:'console',text:message.text()});});"
            "page.on('pageerror',error=>errors.push({type:'pageerror',text:String(error)}));const records=[];"
            "for(const spec of specs){await page.goto(spec.url,{waitUntil:'domcontentloaded',timeout:30000});"
            "await page.waitForFunction(()=>document.body.dataset.ready==='1'||document.body.dataset.error,null,{timeout:30000});"
            "const state=await page.evaluate(()=>window.qaState?window.qaState():null);const error=await page.evaluate(()=>document.body.dataset.error||null);"
            "const resource=await page.evaluate(()=>performance.getEntriesByType('resource').filter(item=>item.name.includes('.glb?')).map(item=>({name:item.name,transferSize:item.transferSize,encodedBodySize:item.encodedBodySize,decodedBodySize:item.decodedBodySize,duration:item.duration})).pop()||null);"
            "await page.screenshot({path:spec.path,type:'png'});records.push({...spec,state,error,resource});}return {records,errors};}"
        )
        result = parse_result(pw(session, "run-code", code, timeout=360))
    finally:
        try:
            pw(session, "close", timeout=30)
        except Exception:
            pass
    records = []
    for record in result["records"]:
        path = Path(record["path"])
        records.append({
            **{name: record[name] for name in ("index", "name", "yaw", "pitch", "background", "load_id", "url")},
            "state": record["state"], "error": record["error"], "resource": record["resource"],
            "screenshot_path": str(path.relative_to(ROTATION_ROOT)),
            "screenshot_bytes": path.stat().st_size,
            "screenshot_sha256": sha256(path),
            "status": "PASS" if not record["error"] and record["state"] and record["state"]["webgl_version"] == 2 else "FAIL",
        })
    if result["errors"]:
        for record in records:
            record["browser_errors"] = result["errors"]
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("before", "after"), required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--model-key", required=True)
    parser.add_argument("--rotation", action="store_true")
    parser.add_argument("--static-gate", action="store_true")
    args = parser.parse_args()
    if not args.rotation and not args.static_gate:
        parser.error("select --rotation and/or --static-gate")
    models = {
        variant: {
            "path": str(model_path(args.model_key, variant)),
            "bytes": model_path(args.model_key, variant).stat().st_size,
            "sha256": sha256(model_path(args.model_key, variant)),
        }
        for variant in VARIANTS
    }
    summary: dict[str, object] = {
        "stage": args.stage,
        "model_key": args.model_key,
        "captured_utc": datetime.now(timezone.utc).isoformat(),
        "models": models,
        "viewer_provenance": viewer_provenance(),
        "rotation_manifests": [],
        "static_loads": [],
    }
    if args.rotation:
        for engine in ENGINES:
            for variant in VARIANTS:
                manifest = capture_rotation(args.stage, args.port, args.model_key, engine, variant, models[variant]["sha256"])
                summary["rotation_manifests"].append({
                    "engine": engine, "variant": variant, "status": manifest["status"],
                    "yaw_frame_count": manifest["yaw_frame_count"], "model_sha256": manifest["model_sha256"],
                })
                print(f"rotation {engine}/{variant}: {manifest['yaw_frame_count']} frames", flush=True)
    if args.static_gate:
        for engine in ENGINES:
            for variant in VARIANTS:
                records = capture_static_gate(args.stage, args.port, args.model_key, engine, variant, models[variant]["sha256"])
                summary["static_loads"].extend(records)
                print(f"static {engine}/{variant}: {len(records)} loads", flush=True)
    static_records = summary["static_loads"]
    summary["static_load_count"] = len(static_records)
    summary["static_pass_count"] = sum(record["status"] == "PASS" for record in static_records)
    summary["status"] = "CAPTURED_PENDING_VISUAL_REVIEW"
    output = ROTATION_ROOT / args.stage / "browser-gate-summary.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise
