import http.server
import socketserver
import os

PORT = 8000
# Corrected the directory path to be absolute
DIRECTORY = "/home/runner/workspace/workspace/project_site"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Change the current working directory to the target directory
        os.chdir(DIRECTORY)
        super().__init__(*args, **kwargs)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
