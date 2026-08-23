#!/usr/bin/env python3
"""Load both GLBs in two independent WebGL engines and capture 40 views."""

from __future__ import annotations

import csv
import functools
import hashlib
import http.server
from pathlib import Path
import subprocess
import threading
import time
from urllib.parse import urlencode

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "qa"
RENDERS = QA / "final" / "webgl-renders"
VIEWS = (
    "front", "rear", "left", "right", "top", "bottom",
    "front-left", "front-right", "rear-left", "rear-right",
)
ENGINES = {
    "threejs": "qa/viewer-threejs/index.html",
    "babylonjs": "qa/viewer-babylonjs/index.html",
}
PROFILES = {
    "standard": "model/Dell-C6420-2.5inch.glb",
    "web": "model/Dell-C6420-2.5inch-web.glb",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class LoggingHandler(http.server.SimpleHTTPRequestHandler):
    records: list[tuple[str, str, str, int | str, int | str]] = []
    lock = threading.Lock()

    def log_request(self, code="-", size="-"):
        with self.lock:
            self.records.append((
                time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                self.command,
                self.path,
                code,
                size,
            ))

    def log_message(self, format, *args):
        return


def main() -> None:
    LoggingHandler.records.clear()
    handler = functools.partial(LoggingHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    rows = []
    try:
        for engine, viewer_path in ENGINES.items():
            for profile, model_path in PROFILES.items():
                model_query = "../../" + model_path
                for view in VIEWS:
                    output = RENDERS / engine / profile / f"{view}.png"
                    output.parent.mkdir(parents=True, exist_ok=True)
                    query = urlencode({"model": model_query, "view": view})
                    url = f"http://127.0.0.1:{port}/{viewer_path}?{query}"
                    cmd = [
                        "npx", "--yes", "playwright", "screenshot",
                        "--channel", "chrome",
                        "--viewport-size", "1600,1200",
                        "--wait-for-selector", 'body[data-ready="true"]',
                        "--timeout", "60000",
                        url, str(output),
                    ]
                    started = time.time()
                    proc = subprocess.run(
                        cmd, cwd=ROOT, capture_output=True, text=True, timeout=90
                    )
                    elapsed = round(time.time() - started, 3)
                    valid = False
                    size = 0
                    digest = ""
                    if proc.returncode == 0 and output.is_file():
                        with Image.open(output) as image:
                            valid = image.size == (1600, 1200) and image.format == "PNG"
                        size = output.stat().st_size
                        digest = sha256(output)
                    status = "PASS" if valid else "FAIL"
                    rows.append({
                        "engine": engine,
                        "profile": profile,
                        "view": view,
                        "model": model_path,
                        "ready_selector": 'body[data-ready="true"]',
                        "browser_exit": proc.returncode,
                        "elapsed_seconds": elapsed,
                        "render": str(output.relative_to(ROOT)),
                        "render_bytes": size,
                        "render_sha256": digest,
                        "status": status,
                        "stderr_tail": proc.stderr[-400:].replace("\n", " "),
                    })
                    print(f"{len(rows):02d}/40 {engine} {profile} {view}: {status}", flush=True)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    log_path = QA / "webgl-http-requests.csv"
    with log_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["timestamp_utc", "method", "path", "status", "bytes"])
        writer.writerows(LoggingHandler.records)

    load_path = QA / "webgl-load-log.csv"
    with load_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    model_requests = [record for record in LoggingHandler.records
                      if record[2].split("?", 1)[0].endswith(".glb") and str(record[3]) == "200"]
    pass_count = sum(row["status"] == "PASS" for row in rows)
    print(f"captures={len(rows)} pass={pass_count} HTTP_200_GLB={len(model_requests)}", flush=True)
    if len(rows) != 40 or pass_count != 40 or len(model_requests) < 40:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
