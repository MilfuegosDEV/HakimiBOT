import discord
import json
import commands


class HakimiBot(discord.Bot):

    def __init__(self, description=None, *args, **options):
        super().__init__(description, *args, **options)

        with open("config.json", 'r') as fp:
            self.__config: dict = json.load(fp)
        fp.close()

        self.debug_guilds = self.__config['discord']['debug_guilds']
        # General commands as `/ping` `/hello`
        self.add_cog(commands.GeneralCog(self))

        # Search commands as `/lyrics`
        self.add_cog(commands.SearchCog(
            spotifyApi=self.__config['spotifyApi'], geniusApi=self.__config['geniusAPI']))

    @property
    def token(self):
        return self.__config['discord']['token']

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
        BOT.run(BOT.token)

    except discord.errors.LoginFailure as LoginFailure:
        print(LoginFailure)

    except Exception as e:
        print(e)
