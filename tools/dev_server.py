#!/usr/bin/env python3
"""
Run the tracker locally for testing:   python3 tools/dev_server.py   then open http://localhost:8000

- Serves tracker.html with its three /_blob/ placeholders pointed at the files in assets/.
- Add ?mock=1 to the URL to inject tools/mock-claude.js, a small stand-in for the claude.ai
  runtime (window.claude.use("db") backed by localStorage, and a "sample" that reports no
  image support), so the database code paths run too. Without it, the app behaves as it does
  when claude.ai's database isn't reachable: data in localStorage, built-in label parser.
- The label reader, USDA search, and storage all work locally. What can't be tested here:
  the real claude.ai database, Claude calls ("Ask Claude", reading label text), and claude.ai's
  content-security policy. Test those on a real install after publishing.
"""
import http.server, os, sys
from urllib.parse import urlparse, parse_qs

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOBS = {
    "/_blob/REPLACE_WITH_OCR_CORE_ID": "assets/ocr-core.js",
    "/_blob/REPLACE_WITH_OCR_DATA_ID": "assets/ocr-eng-data.js",
    "/_blob/REPLACE_WITH_USDA_ID": "assets/usda-foods.js",
}

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def send_body(self, body, ctype):
        self.send_response(200); self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store"); self.send_header("Content-Length", str(len(body)))
        self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        u = urlparse(self.path)
        if u.path in BLOBS:
            return self.send_body(open(os.path.join(ROOT, BLOBS[u.path]), "rb").read(), "text/javascript")
        if u.path in ("/", "/index.html", "/tracker.html"):
            html = open(os.path.join(ROOT, "tracker.html"), encoding="utf-8").read()
            if parse_qs(u.query).get("mock") == ["1"]:
                mock = open(os.path.join(ROOT, "tools", "mock-claude.js"), encoding="utf-8").read()
                html = html.replace("<head>", "<head>\n<script>\n" + mock + "\n</script>", 1)
            return self.send_body(html.encode("utf-8"), "text/html; charset=utf-8")
        return super().do_GET()

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
print(f"Tracker running at http://localhost:{port}   (add ?mock=1 for the claude.ai stand-in)")
http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
