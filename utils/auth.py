import urllib.parse
from http.server import BaseHTTPRequestHandler


class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Parse the query string
        query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        # Get the authorization code
        if "code" in query_components:
            self.server.auth_code = query_components["code"][0]
            self.wfile.write(b"Authorization successful! You can close this window.")
        else:
            self.wfile.write(b"Authorization failed! Please try again.")

    def log_message(self, format, *args):
        # Suppress logging
        return
