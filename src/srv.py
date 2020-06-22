import os
import socketserver
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime

PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")
now = datetime.now().year


def get_page(self):
    path, qs = self.path.split("?") if '?' in self.path else [self.path, ""]
    switcher = {
        "/hello": get_page_hello,
        "/goodbye": get_page_goodbye,
        #"/pages": get_page_about_me,
       # "/pages/hobby": get_page_hobby,
       # "/pages/job": get_page_hobby,
        #"/pages/education": get_page_education,
    }
    return switcher[path](qs) if path in switcher else "no information"

def get_page_hello(qs):
    if qs != "":
        qs = parse_qs(qs)
    name = get_name(qs)
    year = get_year(qs)
    return f"""
          Hello {name}! 
          You were born in {year}.
        """
    self.respond(msg)


def get_page_goodbye(qs):
    if qs != "":
        qs = parse_qs(qs)
    return msg = f"""
        {time}
            """
    self.respond(msg)

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

#def resume(qs):
    msg = """<html>
    <head>
    <title>Main page</title>
    </head>
    <body>
    <h1>Hi! This is my page.</h1>
    <h2>Links
    """

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
