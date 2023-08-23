import discord
from discord.commands import option
from Connection import GeniusConnect, SpotiConnect
from messages import EmbedConstructor


class MusicCog(discord.Cog):

    __MusicCommands: discord.SlashCommandGroup = discord.SlashCommandGroup(
        "music", "music commands")

    def __init__(self, spotifyApi: dict, geniusApi: dict) -> None:
        super().__init__()
        self.__spotify = SpotiConnect(ClientCredentials=spotifyApi)
        self.__genius = GeniusConnect(Credentials=geniusApi)

    def searchTrackByName(self, q: str):
        results = self.__spotify.search(q=q, type="track")
        if results['tracks']['items']:
            return results['tracks']['items'][0]
        else:
            return None

    def __get_lyrics(self, artist, track_name):
        song = self.__genius.search_song(track_name, artist)

        lyrics = song.lyrics.splitlines()
        lyrics.pop(0)

        if song:
            return "\n".join(lyrics)
        else:
            return "Lyrics not found"

    @__MusicCommands.command(description="Search the song's lyrics")
    @option(name="query", type=str, description="Song's name or URL")
    async def lyrics(self, ctx: discord.context.ApplicationContext, query: str):
        embedInfo = {
            "title": 'Song not found',
            "description": '{} not found'.format(query),
            "color": discord.Color.red(),
            "timestamp": 'now',
            "footer": {
                "text": "v1.0.0",
            },
        }

        search_result = self.searchTrackByName(query)

        if not search_result:
            search_result = self.__spotify.track(query)
            if not search_result:
                embed = EmbedConstructor(embedInfo)
                await ctx.respond(embed=embed.get_embed())
            else:
                embedInfo['fields'] = [{
                    "name": "Album",
                    "value": search_result['album']['name'],
                    "inline": True
                }, {
                    "name": "Release Date",
                    "value": search_result['album']['release_date'],
                    "inline": True
                }, {
                    "name": "Song's url",
                    "value": search_result['external_urls']['spotify'],
                    "inline": False
                }]

                embedInfo['color'] = discord.Color.gold()

                artist = search_result['artists'][0]['name']
                track_name = search_result['name']
                # Obtener la URL de la imagen del álbum
                album_image = search_result['album']['images'][0]['url']

                embedInfo['title'] = track_name + ' by ' + artist
                embedInfo['description'] = self.__get_lyrics(
                    artist, track_name)

                # Añadir imagen del álbum al embebido
                embedInfo['thumbnail'] = {"url": album_image}

                embed = EmbedConstructor(embedInfo)
                await ctx.respond(embed=embed.get_embed())
        else:
            embedInfo['fields'] = [{
                "name": "Album",
                "value": search_result['album']['name'],
                "inline": True
            }, {
                "name": "Release Date",
                "value": search_result['album']['release_date'],
                "inline": True
            },
                {
                "name": "Song's url",
                    "value": search_result['external_urls']['spotify'],
                    "inline": False
            }]

            embedInfo['color'] = discord.Color.gold()

            artist = search_result['artists'][0]['name']
            track_name = search_result['name']
            # Obtener la URL de la imagen del álbum
            album_image = search_result['album']['images'][0]['url']

            embedInfo['title'] = track_name + ' by ' + artist
            embedInfo['description'] = self.__get_lyrics(artist, track_name)

            # Añadir imagen del álbum al embebido
            embedInfo['thumbnail'] = {"url": album_image}

            embed = EmbedConstructor(embedInfo)
            await ctx.respond(embed=embed.get_embed())
