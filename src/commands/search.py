import discord
from discord.commands import option

from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from lyricsgenius import Genius

from embedBuider import EmbedConstructor


class SearchCog(discord.Cog):

    __searchCommands: discord.SlashCommandGroup = discord.SlashCommandGroup(
        "search", "Commands related search something")

    def __init__(self, spotifyApi: dict, geniusApi) -> None:
        super().__init__()
        self.__spotify: Spotify = Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id=spotifyApi['ClientID'], client_secret=spotifyApi['ClientSecret']))

        self.__genius: Genius = Genius(access_token=geniusApi["APIKey"])

    def __searchTrackByName(self, q: str):
        results = self.__spotify.search(q=q, type="track")
        if results['tracks']['items']:
            return results['tracks']['items'][0]
        else:
            return None

    def __get_lyrics(self, artist, track_name):
        song = self.__genius.search_song(track_name, artist)
        if song:
            return song.lyrics
        else:
            return "Lyrics doesn't found"

    @__searchCommands.command(description="Search the song's lyrics")
    @option(name="query", type=str, description="Song's name or URL")
    async def lyrics(self, ctx: discord.context.ApplicationContext, query: str):
        embedInfo = {
            "title": 'Song doesn\'t found',
            "description": '{} doesn\'t found'.format(query),
            "color": discord.Color.red(),
            "timestamp": 'now',
            "footer": {
                "text": "v1.0.0",
            },

        }

        if not self.__searchTrackByName(query):
            search_result = self.__spotify.track(query)
            if not search_result:
                embed = EmbedConstructor(embedInfo)
                await ctx.respond(embed=embed.get_embed())
            else:
                embedInfo['fields'] = [{
                    "name": "Author",
                    "value": search_result['artists'][0]['name'],
                    "inline": True
                }]

                embedInfo['color'] = discord.Color.gold()

                artist = search_result['artists'][0]['name']
                track_name = search_result['name']

                embedInfo['title'] = track_name

                embedInfo['description'] = self.__get_lyrics(
                    artist, track_name)
                embed = EmbedConstructor(embedInfo)
                await ctx.respond(embed=embed.get_embed())
        else:
            embedInfo['fields'] = [{
                "name": "Author",
                "value": search_result['artists'][0]['name'],
                "inline": True
            }]

            embedInfo['color'] = discord.Color.gold()

            artist = search_result['artists'][0]['name']
            track_name = search_result['name']

            embedInfo['title'] = track_name

            embedInfo['description'] = self.__get_lyrics(artist, track_name)
            embed = EmbedConstructor(embedInfo)
            await ctx.respond(embed=embed.get_embed())
