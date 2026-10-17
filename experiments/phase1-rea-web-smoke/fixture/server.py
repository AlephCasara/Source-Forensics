from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
from pathlib import Path

ROOT = Path(__file__).parent

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/':
            data = (ROOT / 'index.html').read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers(); self.wfile.write(data); return
        if parsed.path == '/app.js':
            data = (ROOT / 'app.js').read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript; charset=utf-8')
            self.send_header('SourceMap', '/app.js.map')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers(); self.wfile.write(data); return
        if parsed.path == '/app.js.map':
            data = (ROOT / 'app.js.map').read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers(); self.wfile.write(data); return
        if parsed.path == '/api/search':
            q = parse_qs(parsed.query)
            region = q.get('region', ['UNKNOWN'])[0]
            sort = q.get('sort', ['UNKNOWN'])[0]
            payload = {
                'request': {'region': region, 'sort': sort},
                'items': [
                    {'product_id': 'p-001', 'name': 'Alpha', 'gmv_7d': 1200, 'sold_7d': 40},
                    {'product_id': 'p-002', 'name': 'Beta', 'gmv_7d': 900, 'sold_7d': 30}
                ],
                'next_cursor': 'cursor-002'
            }
            data = json.dumps(payload).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers(); self.wfile.write(data); return
        self.send_response(404); self.end_headers()

    def log_message(self, fmt, *args):
        print('%s - %s' % (self.address_string(), fmt % args), flush=True)

if __name__ == '__main__':
    HTTPServer(('127.0.0.1', 8765), Handler).serve_forever()
