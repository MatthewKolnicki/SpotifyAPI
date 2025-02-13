# Spotify Now Playing Monitor

A Python application that monitors your currently playing track on Spotify in real-time. This project uses the Spotify Web API to fetch current playback information and can display album artwork.

## Features

- Real-time monitoring of currently playing tracks
- Display of track information including song name, artist, and album
- Automatic download and display of album artwork
- Graceful handling of playback states (playing, paused, stopped)

## Prerequisites

- Python 3.x
- Spotify Premium account
- Spotify Developer account with registered application

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd SpotifyAPI
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your Spotify API credentials:
```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=your_redirect_uri
```

## Usage

Run the application using:
```bash
python main.py
```

The application will:
- Authenticate with Spotify
- Start monitoring your currently playing track
- Display track information in real-time
- Download and save album artwork (as album_cover.jpg)
- Update information every 2 seconds

To stop the application, press `Ctrl+C`.

## Project Structure

```
SpotifyAPI/
├── api/              # API-related modules
├── utils/
│   ├── auth.py      # Authentication handling
│   └── connector.py # Spotify API connection logic
├── main.py          # Main application entry point
├── requirements.txt # Project dependencies
└── .env            # Environment variables (not tracked in git)
```

## Dependencies

- requests: HTTP library for API calls
- python-dotenv: Environment variable management
- Other utilities for code formatting and maintenance

## Error Handling

The application includes robust error handling for:
- Network connectivity issues
- API authentication failures
- Playback state changes
- Resource cleanup

## Contributing

Feel free to submit issues and enhancement requests!

## License

[Your chosen license]

## Acknowledgments

- Spotify Web API
- All contributors to this project 