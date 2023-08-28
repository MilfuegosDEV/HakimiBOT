import discord
from discord.ext import tasks
import json
import commands

from Connection import SpotiConnect, GeniusConnect, GPTConnect


class HakimiBot(discord.AutoShardedBot):

    def __init__(self, description=None, *args, **options):
        super().__init__(description, *args, **options)

        self.TOKEN: str = self.__config['discord']['token'] # My bot token
        self.intents.all()
        self.__update_activity.start() # Activity Status

        # API'S CONNECTION
        self.__apisConnection()

        # General commands as `/ping` `/hello`
        self.add_cog(commands.GeneralCog(self))

        # GPT commands as
        self.add_cog(commands.GPTCog(gptConnect = self.__gptConnection))

        # Music commands as `/lyrics`
        self.add_cog(commands.MusicCog(self,
            spotiConnect=self.__spotiConnection, geniusConnect=self.__geniusConnection))
        


    @property
    def __config(self) -> dict:
        with open("config.json", 'r') as fp:
            config: dict = json.load(fp)
        fp.close()
        return config

    def __apisConnection(self):
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
        print('Joined as {}!'.format(self.user.name))

    @tasks.loop(minutes=10)
    async def __update_activity(self):
        await self.change_presence(activity=discord.Game('Helping {} guilds!'.format(len(self.guilds))))

    @__update_activity.before_loop
    async def before_update_activity(self):
        await self.wait_until_ready()


if __name__ == "__main__":
    try:
        BOT = HakimiBot()
        BOT.run(BOT.TOKEN)

    except discord.errors.LoginFailure as LoginFailure:
        print(LoginFailure)

    except Exception as e:
        print(e)
