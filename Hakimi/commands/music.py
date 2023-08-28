import discord
from discord.commands import option
from discord.ext import tasks
from messages import EmbedConstructor

from spotipy import Spotify
from lyricsgenius import Genius

import asyncio

import re


class MusicCog(discord.Cog):
    """
    Cog class for music-related commands in a Discord bot.
    """

    __MusicCommands: discord.SlashCommandGroup = discord.SlashCommandGroup(
        "music", "music commands")

    def __init__(self, bot: discord.AutoShardedBot, spotiConnect: Spotify, geniusConnect: Genius) -> None:
        """
        Initialize the MusicCog.
        :param bot: discord.Bot instance
        :param spotifyApi: Dictionary containing Spotify API credentials.
        :param geniusApi: Dictionary containing Genius API credentials.
        """
        super().__init__()

        # Getting spotify's connection
        self.__spotify: Spotify = spotiConnect
        # Getting Genius's connection
        self.__genius: Genius = geniusConnect
        # MyBot
        self.__bot = bot

        # Voice cache.
        self.__connections = {}

        # Voice auto disconnection
        self.disconnect_countdown.start()

    def __searchTrackByName(self, q: str) -> dict:
        """
        Search for a track by its name using Spotify API.

        :param q: Query string for track search.
        :return: Track information if found, else None.
        """
        results: dict = self.__spotify.search(q=q, type="track")
        if results['tracks']['items']:
            return results['tracks']['items'][0]
        else:
            return None

    def __get_lyrics(self, artist, track_name) -> str:
        """
        Get lyrics of a song using Genius API.

        :param artist: Artist's name.
        :param track_name: Track's name.
        :return: Lyrics of the song, or "Lyrics not found" if not available.
        """
        song = self.__genius.search_song(track_name, artist)
        if song:
            lyrics: list = song.lyrics.splitlines()
            lyrics[-1] = re.sub(r'\d+Embed', '.', lyrics[-1])
            lyrics.pop(0)
            return "\n".join(lyrics)
        else:
            return "Lyrics not found"

    @__MusicCommands.command(description="Search the song's lyrics")
    @option(name="query", type=str, description="Song's name or URL")
    async def lyrics(self, ctx: discord.context.ApplicationContext, query: str):
        """
        Command to search and display lyrics of a song.

        :param ctx: Context of the command.
        :param query: Song's name or URL.
        """
        embedInfo = {
            "title": 'Song not found',
            "description": '{} not found'.format(query),
            "color": discord.Color.red(),
            "timestamp": 'now',
            "footer": {
                "text": "v1.0.1",
            },
        }

        search_result = self.__searchTrackByName(query)

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

    @tasks.loop(minutes=1)
    async def disconnect_countdown(self):
        for guild_id, vc in self.__connections.copy().items():
            if len(vc.channel.members) == 1 and vc.is_connected():
                await vc.disconnect()
                del self.__connections[guild_id]
            if guild_id == self.__ctx.guild.id:
                await self.__ctx.respond(f"Logged out of {vc.channel.mention}")

    @disconnect_countdown.before_loop
    async def before_disconnect_countdown(self):
        await self.__bot.wait_until_ready()

    @disconnect_countdown.after_loop
    async def after_disconnect_countdown(self):
        self.disconnect_countdown.cancel()

    @__MusicCommands.command(description="Play music into a voice channel")
    async def play(self, ctx: discord.context.ApplicationContext):
        self.__ctx = ctx
        voice = ctx.author.voice
        if not voice:
            await ctx.respond("You must be in a voice channel!")
        else:
            try:
                vc = await voice.channel.connect()
                self.__connections[ctx.guild.id] = vc
                await ctx.respond("Joined into {}".format(voice.channel.mention))
            except Exception as e:
                if "Task is already launched and is not completed." in str(e):
                    await asyncio.sleep(2)
                    self.disconnect_countdown.restart()
                else:
                    await ctx.respond(str(e))

    @__MusicCommands.command(description="Stop and disconnect the bot from the voice channel")
    async def stop(self, ctx: discord.context.ApplicationContext):
        vc = self.__connections.get(ctx.guild.id)
        if vc:
            await vc.disconnect()
            del self.__connections[ctx.guild.id]
            await ctx.respond("Disconnected from the voice channel.")
        else:
            await ctx.respond("I'm not connected to any voice channel.")
