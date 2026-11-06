#!/usr/bin/env python3
"""Serve the capability board with cross-origin isolation headers.

A plain static server (python -m http.server, file://) can't set COOP/COEP,
so the SharedArrayBuffer / Atomics / threads probes report a false negative.
This tiny stdlib server adds the two headers that make those probes honest.

    python3 serve.py [port]        # default 8000

Then open  http://localhost:<port>/capability-board.html
"""
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"capability board: http://localhost:{port}/capability-board.html")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
