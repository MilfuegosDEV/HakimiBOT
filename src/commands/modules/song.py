#Search and play songs

import json
import spotipy

# Read the JSON data from config.json
with open('config.json', 'r') as json_file:
    data = json.load(json_file)

# Get Spotify API credentials
spotify_client_id = data['spotifyApi']['ClientID']
spotify_client_secret = data['spotifyApi']['ClientSecret']

# Establish a connection to the Spotify API
sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id=spotify_client_id, client_secret=spotify_client_secret, redirect_uri='http://localhost:8888/callback', scope='user-library-read user-read-playback-state user-modify-playback-state'))

# Test connection to Spotify
try:
    user_info = sp.current_user()
    print("Connected to Spotify. User Display Name:", user_info['display_name'])
except Exception as e:
    print("Error connecting to Spotify:", e)


