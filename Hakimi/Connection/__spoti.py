
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

def Connection(ClientCredentials) -> Spotify:
    """
    Creates a connection to the Spotify API.

    Parameters:
        ClientCredentials (dict): Dictionary containing 'ClientID' and 'ClientSecret'.

    Returns:
        Spotify: A Spotify API connection object.
    """
    # Create a Spotify connection using the provided client credentials
    return Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id=ClientCredentials['ClientID'],
        client_secret=ClientCredentials['ClientSecret']))
