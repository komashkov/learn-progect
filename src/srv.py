import socketserver
import os
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs
import datetime

PORT = int(os.getenv("PORT", 8000))
print(f"port = {PORT}")
now = datetime.datetime.now()

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/hello":
            msg = """
                     Hello, Anonymouse!
                     I don't know your age :(
                     """
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-Length", len(msg))
            self.end_headers()
            self.wfile.write(msg.encode())

        elif self.path.startswith("/hello"):
            path, qs = self.path.split("?")
            qs = parse_qs(qs)
            name = qs["name"][0]
            age = qs["age"][0]
            year = str(now - int(age))
            born = 'You were born in the ' + year + ' year'
            msg = """ Hello {name}
                        {born}
                        """

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-Length", len(msg))
            self.end_headers()

            self.wfile.write(msg.encode())
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("it works")
    httpd.serve_forever()
