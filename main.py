"""
消息队列系统搭建 - 后端服务
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

class APIHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "service": "feature_1567"}).encode())
        else:
            super().do_GET()

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8080), APIHandler)
    print('Server running on http://localhost:8080')
    server.serve_forever()
