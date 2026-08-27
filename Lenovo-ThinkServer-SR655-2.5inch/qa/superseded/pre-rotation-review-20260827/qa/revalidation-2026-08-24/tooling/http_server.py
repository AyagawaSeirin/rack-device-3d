#!/usr/bin/env python3
"""Serve the model directory and preserve every HTTP request for QA."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class RecordingHandler(SimpleHTTPRequestHandler):
    log_path: Path

    def log_message(self, format_string: str, *args: object) -> None:
        record = {
            "timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "client": self.client_address[0],
            "method": self.command,
            "path": self.path,
            "message": format_string % args,
        }
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", required=True)
    parser.add_argument("--log", required=True)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    log_path = Path(args.log).resolve()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("", encoding="utf-8")

    handler = lambda *hargs, **hkwargs: RecordingHandler(
        *hargs, directory=str(Path(args.directory).resolve()), **hkwargs
    )
    RecordingHandler.log_path = log_path
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
