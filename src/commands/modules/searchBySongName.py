from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


#Search song
def searchTrackByName(self, q: str):
        results = self.__spotify.search(q=q, type="track")
        if results['tracks']['items']:
            return results['tracks']['items'][0]
        else:
            return None
        

#Spotify API
def __init__(self, spotifyApi: dict) -> None:
        super().__init__()
        self.__spotify: Spotify = Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id=spotifyApi['ClientID'], client_secret=spotifyApi['ClientSecret']))