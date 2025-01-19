import os
import requests
import base64
from datetime import datetime, timedelta
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import threading
from utils.auth import OAuthHandler
from io import BytesIO


class SpotifyAPI:
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.redirect_uri = "http://localhost:8080/callback"
        self.access_token = None
        self.refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")
        self.token_expiry = None
        self.base_url = "https://api.spotify.com/v1"

    def get_auth_url(self):
        """Generate the authorization URL"""
        scope = "user-read-currently-playing user-read-playback-state"
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": scope,
        }
        return (
            f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(params)}"
        )

    def start_auth_server(self):
        """Start local server to receive the authorization code"""
        server = HTTPServer(("localhost", 8080), OAuthHandler)
        server.auth_code = None
        server_thread = threading.Thread(target=server.handle_request)
        server_thread.start()
        return server

    def authenticate(self):
        """Perform the full OAuth flow"""
        if self.refresh_token:
            # If we have a refresh token, just use it
            self.refresh_access_token()
            return

        # Only open browser and start server if we don't have a refresh token
        print("No refresh token found. Starting new OAuth flow...")
        auth_url = self.get_auth_url()
        server = self.start_auth_server()
        webbrowser.open(auth_url)

        while server.auth_code is None:
            pass

        self.get_tokens(server.auth_code)

    def get_tokens(self, auth_code):
        """Exchange authorization code for access and refresh tokens"""
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_base64 = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": self.redirect_uri,
        }

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data["access_token"]
            self.refresh_token = token_data["refresh_token"]
            self.token_expiry = datetime.now() + timedelta(
                seconds=token_data["expires_in"]
            )

            # Save refresh token to .env file
            self.update_env_file()
        else:
            raise Exception(f"Failed to get tokens: {response.status_code}")

    def refresh_access_token(self):
        """Refresh the access token using the refresh token"""
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_base64 = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {"grant_type": "refresh_token", "refresh_token": self.refresh_token}

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data["access_token"]
            self.token_expiry = datetime.now() + timedelta(
                seconds=token_data["expires_in"]
            )
            if "refresh_token" in token_data:
                self.refresh_token = token_data["refresh_token"]
                self.update_env_file()
        else:
            raise Exception(f"Failed to refresh token: {response.status_code}")

    def update_env_file(self):
        """Update the .env file with the new refresh token"""
        env_path = ".env"
        env_vars = {}

        # Read existing variables
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        env_vars[key] = value

        # Update refresh token
        env_vars["SPOTIFY_REFRESH_TOKEN"] = self.refresh_token

        # Write back to file
        with open(env_path, "w") as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")

    def _download_image(self, url):
        """Download image from URL and return as bytes"""
        response = requests.get(url)
        if response.status_code == 200:
            return BytesIO(response.content)
        return None

    def get_currently_playing(self):
        """Get the user's currently playing track"""
        if not self.access_token or (
            self.token_expiry and datetime.now() >= self.token_expiry
        ):
            self.refresh_access_token()

        headers = {"Authorization": f"Bearer {self.access_token}"}

        url = f"{self.base_url}/me/player/currently-playing"
        response = requests.get(url, headers=headers)

        if response.status_code == 204:
            return "No track currently playing"
        elif response.status_code == 200:
            data = response.json()
            if data is None or not data:
                return "No track currently playing"

            track = data["item"]
            artists = ", ".join([artist["name"] for artist in track["artists"]])
            album_cover_url = track["album"]["images"][0]["url"]
            album_cover_data = self._download_image(album_cover_url)
            is_playing = data.get(
                "is_playing", True
            )  # Default to True if not specified

            return {
                "name": track["name"],
                "artists": artists,
                "album_cover": album_cover_data,
                "is_playing": is_playing,
            }
        else:
            raise Exception(
                f"Failed to get currently playing track: {response.status_code}"
            )
