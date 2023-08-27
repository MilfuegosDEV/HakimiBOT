import discord
import json
import commands

from Connection import SpotiConnect, GeniusConnect, GPTConnect


class HakimiBot(discord.Bot):

    def __init__(self, description=None, *args, **options):
        super().__init__(description, *args, **options)

        # My bot token
        self.TOKEN: str = self.__config['discord']['token']
        # My server's ids
        self.debug_guilds: list = self.__config['discord']['debug_guilds']

        # API'S CONNECTION
        self.__apisConnection()

        # General commands as `/ping` `/hello`
        self.add_cog(commands.GeneralCog(self))

        # GPT commands as
        self.add_cog(commands.GPTCog(gptConnect = self.__gptConnection))

        # Music commands as `/lyrics`
        self.add_cog(commands.MusicCog(
            spotiConnect=self.__spotiConnection, geniusConnect=self.__geniusConnection))
        

    @property
    def __config(self) -> dict:
        with open("config.json", 'r') as fp:
            config: dict = json.load(fp)
        fp.close()
        return config

    def __apisConnection(self):
        """All apis connection
        """
        self.__spotiConnection = SpotiConnect(
            ClientCredentials=self.__config["spotifyApi"])

        # Genius's connection
        self.__geniusConnection = GeniusConnect(
            Credentials=self.__config['GeniusAPI'])
        
        #OpenAI Connection
        self.__gptConnection = GPTConnect(
            GPTCredentials=self.__config['OpenAIAPI']
        )

    async def on_ready(self):
        """
        Event handler for bot being ready.

        Called when the bot has successfully connected to Discord.
        """
        await self.change_presence(activity=discord.Game('/help'))
        print(f'Joined as {self.user.name}!')


if __name__ == "__main__":
    try:
        BOT = HakimiBot()
        BOT.run(BOT.TOKEN)

    except discord.errors.LoginFailure as LoginFailure:
        print(LoginFailure)

    except Exception as e:
        print(e)
