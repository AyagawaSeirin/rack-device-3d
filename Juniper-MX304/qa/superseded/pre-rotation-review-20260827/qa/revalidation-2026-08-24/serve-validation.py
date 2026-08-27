#!/usr/bin/env python3
"""Serve the project and log every actual GLB response used by revalidation."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

PROJECT_ROOT = Path("/root/Project/rack-device-3d")
LOG_PATH = PROJECT_ROOT / "Juniper-MX304/revalidation-2026-08-24/logs/server-loads.jsonl"
HOST = "127.0.0.1"
PORT = 8767


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PROJECT_ROOT), **kwargs)

    def send_response(self, code, message=None):  # noqa: ANN001
        self._response_code = code
        super().send_response(code, message)

    def do_GET(self):  # noqa: N802
        parsed = urlparse(self.path)
        is_glb = parsed.path.lower().endswith(".glb")
        is_ready_proof = parsed.path.endswith("/web-proof/ready.txt")
        local_path = None
        before = None
        if is_glb or is_ready_proof:
            local_path = PROJECT_ROOT / unquote(parsed.path).lstrip("/")
            if local_path.is_file():
                data = local_path.read_bytes()
                before = {
                    "served_file": str(local_path),
                    "byte_size": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                }
        self._response_code = None
        try:
            super().do_GET()
        finally:
            if is_glb or is_ready_proof:
                query = {key: values[-1] for key, values in parse_qs(parsed.query).items()}
                record = {
                    "record_type": "glb_response" if is_glb else "viewer_ready_proof",
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "request_path": parsed.path,
                    "query": query,
                    "response_status": self._response_code,
                    **(before or {"served_file": str(local_path), "byte_size": None, "sha256": None}),
                }
                LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
                with LOG_PATH.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(record, sort_keys=True) + "\n")

    def log_message(self, format, *args):  # noqa: A002, ANN001
        return


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Serving {PROJECT_ROOT} at http://{HOST}:{PORT}", flush=True)
    server.serve_forever()
