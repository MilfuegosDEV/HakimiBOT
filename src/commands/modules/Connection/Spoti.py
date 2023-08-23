from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


def spoti(spotifyApi: dict) -> Spotify:
    """Connects to spotify api"""
    return Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id=spotifyApi['ClientID'], client_secret=spotifyApi['ClientSecret']))
