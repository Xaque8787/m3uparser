import http.server
import socketserver
import threading
import os

PORT = 2112
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Directory of the current script
FILE_TO_SERVE = os.path.join(SCRIPT_DIR, "ezpztv-androidtv-v2.11.2-release.apk")
TIMEOUT = 3600  # Timeout in seconds

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve the file with the correct filename in Content-Disposition header
        self.send_response(200)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Disposition", f"attachment; filename={os.path.basename(FILE_TO_SERVE)}")
        self.end_headers()

        # Serve the file content
        with open(FILE_TO_SERVE, "rb") as file:
            self.wfile.write(file.read())

        # Shutdown the server after handling the request
        threading.Thread(target=self.server.shutdown).start()

def start_server():
    handler = MyHandler
    httpd = socketserver.TCPServer(("", PORT), handler)

    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.start()

    print(f"Serving {os.path.basename(FILE_TO_SERVE)} on port {PORT}")

    # Automatically stop the server after TIMEOUT seconds if no request is made
    server_thread.join(timeout=TIMEOUT)
    httpd.shutdown()
    httpd.server_close()

    print("Server stopped")

if __name__ == "__main__":
    start_server()
