import os
import socketserver
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime
from pathlib import Path

PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")
now = datetime.now().year

PAGES_DIR = Path(__file__).parent.parent.resolve()
print(f"PAGES_DIR = {PAGES_DIR}")

HOBBY_DIR = PAGES_DIR / "templates"
print(f"HOBBY_DIR = {HOBBY_DIR}")


class NotFound(Exception):
    pass

def get_page_hello(qs):
    if qs != "":
        qs = parse_qs(qs)
    name = get_name(qs)
    year = get_year(qs)
    return f"""
          Hello {name}! 
          You were born in {year}.
        """
    self.response(msg)


def get_page_goodbye(qs):
    hour = datetime.now().hour
    if hour < 6:
        return f"Good night"
    elif hour < 12:
        return f"Good morning"
    elif hour < 18:
        return f"Good afternoon"
    elif hour < 23:
        return f"Good evening"
    else:
        return f"Good night"
    self.response(msg)


def get_name(qs):
    if qs == "":
        return "anonymous"
    else:
        qs = parse_qs(qs)
        if "name" not in qs:
            return "anonymous"
        else:
            return qs["name"][0]


def get_year(qs):
    if qs == "":
        return "no information"
    else:
        qs = parse_qs(qs)
        if "age" not in qs:
            return "no information"
        else:
            today = datetime.today().year
            return str(today - int(qs["age"][0]))


def get_page_about_me(self):
    html = PAGES_DIR / "pages" / "index.html"
    contents = self.get_file_contents(html)
    self.response(contents, "text/html")


def get_page_hobby(self):
    html = PAGES_DIR / "pages" / "hobby" / "index.html"
    contents = self.get_file_contents(html)
    self.response(contents, "text/html")


def get_file_contents(self, fp: Path):
    if not fp.is_file():
        raise NotFound()

    with fp.open("r") as src:
        ct = src.read()

    return ct


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path, qs = self.path.split("?") if '?' in self.path else [self.path, ""]
        switcher = {
            "/hello": get_page_hello,
            "/goodbye": get_page_goodbye,
            "/pages": get_page_about_me,
            "/pages/hobby": get_page_hobby,
        }
        if path in switcher:
            msg = switcher[path](qs)

            self.send_response(200)
            self.send_header("content-type", "text/plain")
            self.send_header("content-length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg.encode())
        else:
            return SimpleHTTPRequestHandler.do_GET(self)


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("it" + " works")
    httpd.serve_forever()
