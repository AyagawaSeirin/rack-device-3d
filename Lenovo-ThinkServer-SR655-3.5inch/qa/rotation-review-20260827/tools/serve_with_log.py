#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

MODEL_ROOT = Path(__file__).resolve().parents[3]


class Handler(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    log_path: Path

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def log_message(self, fmt: str, *args: object) -> None:
        split = urlsplit(self.path)
        local = MODEL_ROOT / unquote(split.path.lstrip("/"))
        record = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "client": self.client_address[0],
            "method": self.command,
            "path": split.path,
            "query": split.query,
            "status_line": fmt % args,
            "resolved_file": str(local),
            "resolved_bytes": local.stat().st_size if local.is_file() else None,
        }
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--log", type=Path, required=True)
    args = parser.parse_args()
    Handler.log_path = args.log.resolve()
    handler = partial(Handler, directory=str(MODEL_ROOT))
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(json.dumps({"root": str(MODEL_ROOT), "host": args.host, "port": args.port, "log": str(Handler.log_path)}), flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
