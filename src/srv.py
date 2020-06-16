import os
import socketserver
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime

PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")
now = datetime.now().year


def get_page(query):
    path, qs = query.split("?") if '?' in query else [query, ""]
    switcher = {
        "/hello": page_hello,
        "/goodbye": page_goodbye, }
    return switcher[path](qs) if path in switcher else "no information"

def page_hello(qs):
    qs = parse_qs(qs) if qs != "" else ""
    name = get_name(qs)
    year = get_year(qs)
    return f"""
          Hello {name}! 
          You were born in {year}.
        """

def page_goodbye(qs):
    qs = parse_qs(qs)
    time = get_bye(qs)
    return f"""
        {time}
            """

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


def get_bye():
    hour = datetime.now().hour
    if hour < 6:
        return "Good night"
    elif hour < 12:
        return "Good morning"
    elif hour < 18:
        return "Good afternoon"
    elif hour < 23:
        return "Good evening"
    else:
        return "Good night"


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path != "":
            msg = get_page(self.path)

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
