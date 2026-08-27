#!/usr/bin/env python3
"""Static no-cache QA server that records successful WebGL GLB loads."""

from __future__ import annotations

import argparse
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "qa" / "viewer-load-evidence.json"
LOCK = threading.Lock()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        super().end_headers()

    def do_POST(self) -> None:
        if self.path != "/qa-result":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        record = json.loads(self.rfile.read(length))
        model = record.get("model")
        model_path = ROOT / "model" / (
            "Dell-R7515-3.5inch-web.glb" if model == "web" else "Dell-R7515-3.5inch.glb"
        )
        record["serverReceivedAt"] = datetime.now(timezone.utc).isoformat()
        record["serverModelBytes"] = model_path.stat().st_size
        record["serverModelSha256"] = digest(model_path)
        with LOCK:
            payload = json.loads(EVIDENCE.read_text(encoding="utf-8"))
            existing = {item.get("qaId") for item in payload["loads"]}
            if record.get("qaId") not in existing:
                payload["loads"].append(record)
            payload["count"] = len(payload["loads"])
            EVIDENCE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            count = payload["count"]
        body = json.dumps({"ok": True, "count": count}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        if self.path == "/qa-result" or self.path.endswith(".glb"):
            super().log_message(format, *args)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8791)
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args()
    if args.reset or not EVIDENCE.exists():
        EVIDENCE.write_text(
            json.dumps(
                {
                    "modelKey": "Dell-R7515-3.5inch",
                    "requiredMatrix": "2 viewers x 2 GLBs x (6 orthographic + 4 oblique) = 40; plus close-ups",
                    "startedAt": datetime.now(timezone.utc).isoformat(),
                    "count": 0,
                    "loads": [],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"QA_SERVER http://127.0.0.1:{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
