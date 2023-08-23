from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


def Connection(clientID: str, clientSecret: str) -> Spotify:
    return SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)