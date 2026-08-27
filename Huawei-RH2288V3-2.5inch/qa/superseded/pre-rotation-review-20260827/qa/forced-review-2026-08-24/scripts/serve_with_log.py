#!/usr/bin/env python3
"""Serve the model directory and record every forced-review GLB GET."""

from __future__ import annotations

import argparse
import hashlib
import json
import threading
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse


ROOT = Path(__file__).resolve().parents[3]
REVIEW = ROOT / "qa" / "forced-review-2026-08-24"
LOG = REVIEW / "http-loads.jsonl"
LOCK = threading.Lock()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


MODEL_METADATA = {
    f"/model/{path.name}": {"sha256": sha256(path), "bytes": path.stat().st_size}
    for path in (ROOT / "model").glob("*.glb")
}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        normalized = unquote(parsed.path)
        if normalized in MODEL_METADATA:
            record = {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "method": "GET",
                "path": normalized,
                "query": parse_qs(parsed.query),
                "response": 200,
                **MODEL_METADATA[normalized],
            }
            with LOCK:
                with LOG.open("a", encoding="utf-8") as output:
                    output.write(json.dumps(record, ensure_ascii=False) + "\n")
        super().do_GET()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8877)
    args = parser.parse_args()
    REVIEW.mkdir(parents=True, exist_ok=True)
    start = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "root": str(ROOT),
        "port": args.port,
        "models": MODEL_METADATA,
    }
    (REVIEW / "http-server-start.json").write_text(
        json.dumps(start, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(start, ensure_ascii=False), flush=True)
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
