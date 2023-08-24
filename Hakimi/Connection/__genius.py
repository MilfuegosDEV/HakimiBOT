from lyricsgenius import Genius

def Connection(Credentials: dict) -> Genius:
    """
    Creates a connection to the Genius API.

    Parameters:
        Credentials (dict): Dictionary containing 'token' for authentication.

    Returns:
        Genius: A Genius API connection object.
    """
    # Create a Genius connection using the provided access token
    return Genius(access_token=Credentials['token'], retries=10, remove_section_headers=True)