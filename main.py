from utils.connector import SpotifyAPI
import time
import json
import os

# Example usage
if __name__ == "__main__":
    spotify = SpotifyAPI()

    try:
        spotify.authenticate()
        while True:
            current_track = spotify.get_currently_playing()
            if isinstance(current_track, dict) and current_track["is_playing"]:
                print(current_track)
                if current_track["album_cover"]:
                    with open("album_cover.jpg", "wb") as f:
                        f.write(current_track["album_cover"].getvalue())
            else:
                print(f"\r{current_track}", end="")
                # Delete album cover if no track playing or paused
                if os.path.exists("album_cover.jpg"):
                    os.remove("album_cover.jpg")
            time.sleep(2)
    except KeyboardInterrupt:
        if os.path.exists("album_cover.jpg"):
            os.remove("album_cover.jpg")
        print("\nStopping playback monitor...")
    except Exception as e:
        if os.path.exists("album_cover.jpg"):
            os.remove("album_cover.jpg")
        print(f"\nError: {str(e)}")
