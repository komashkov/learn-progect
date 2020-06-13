import socketserver
import os
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime

PORT = int(os.getenv("PORT", 8000))
print(f"port = {PORT}")

def get_page(query):
    path, qs = query.split("?") if '?' in query else [query, ""]
    paths = {
        '/hello': hello,
        '/goodbye': goodbye,
        }
    return paths[path](qs)

def hello(qs):
    print(qs)

    qs = parse_qs(qs)
    print("get_name: ")
    print(qs)
    return f"""
                    Hello {get_name(qs)}!
                    You were born in {get_year(qs)} year
                    Your path: /hello
                     """

def goodbye(qs):
    print(qs)
    hour = datetime.now().hour
    if hour < 6:
        return f"Good night!"
    elif hour < 12:
        return f"Good morning!"
    elif hour < 18:
        return f"Good afternoon!"
    elif hour < 23:
        return f"Good evening!"
    else:
        return f"Good night!"

def get_name(qs):
    if 'name' in qs:
        print("get_name: ")
        print(qs)
        return qs["name"][0]
    else:
        return "Anonymous"

def get_year(qs):
    if 'age' in qs:
        print("get age: ")
        print(qs)
        return str(datetime.now().year - int(qs['age'][0]))
    else:
        return "I don't know your age:("


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        msg = get_page(self.path)

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("it works")
    httpd.serve_forever()
