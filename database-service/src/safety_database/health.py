from http.server import BaseHTTPRequestHandler, HTTPServer


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path != "/health":
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)

        # self.send_header("Content-Type", "json")
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(b'{"status":"ok"}')

    def log_message(self, _format: str, *_args) -> None:
        return


def serve_health(port: int) -> None:
    HTTPServer(("", port), HealthHandler).serve_forever()
