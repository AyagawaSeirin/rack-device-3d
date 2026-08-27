#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import threading
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


ROOT = Path(__file__).resolve().parents[3]
LOCK = threading.Lock()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=8890)
parser.add_argument("--log", type=Path, required=True)
args = parser.parse_args()
args.log.parent.mkdir(parents=True, exist_ok=True)


class Handler(SimpleHTTPRequestHandler):
    server_version = "SR655ForcedRevalidationHTTP/1.0"

    def __init__(self, *handler_args, **handler_kwargs):
        self._status = None
        super().__init__(*handler_args, directory=str(ROOT), **handler_kwargs)

    def send_response(self, code, message=None):
        self._status = code
        super().send_response(code, message)

    def log_message(self, format, *values):
        return

    def do_GET(self):
        parsed = urlsplit(self.path)
        is_glb = parsed.path.startswith("/model/") and parsed.path.endswith(".glb")
        file_path = ROOT / parsed.path.lstrip("/") if is_glb else None
        started_at = datetime.now(timezone.utc).isoformat()
        super().do_GET()
        if is_glb:
            exists = file_path.is_file()
            actual_sha = sha256(file_path) if exists else None
            query = {key: values[0] if len(values) == 1 else values for key, values in parse_qs(parsed.query).items()}
            event = {
                "timestamp_utc": started_at,
                "method": "GET",
                "request_path": self.path,
                "path": parsed.path,
                "query": query,
                "status": self._status,
                "bytes": file_path.stat().st_size if exists else None,
                "sha256": actual_sha,
                "expected_sha256": query.get("sha"),
                "sha256_match": exists and actual_sha == query.get("sha"),
                "client": self.client_address[0],
                "user_agent": self.headers.get("User-Agent"),
                "referer": self.headers.get("Referer"),
            }
            with LOCK:
                with args.log.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(event, separators=(",", ":")) + "\n")


server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
print(json.dumps({"ready": True, "root": str(ROOT), "port": args.port, "log": str(args.log)}, separators=(",", ":")), flush=True)
server.serve_forever()
