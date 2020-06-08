import os
import socketserver
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs
PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/hello"):
            path, qs = self.path.split("?")
            qs = parse_qs(qs)
            name = qs["name"][0]
            msg = f"""
                Hello {name}!
                Your path:  {path}
            """
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg.encode())
        else:
            return SimpleHTTPRequestHandler.do_GET(self)


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("it" + " works")
    httpd.serve_forever()
