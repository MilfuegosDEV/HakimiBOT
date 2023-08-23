import discord
import json
import commands


class HakimiBot(discord.Bot):

    def __init__(self, description=None, *args, **options):
        super().__init__(description, *args, **options)

        self.TOKEN: str = self.__config['discord']['token'] # My bot token
        self.debug_guilds:list = self.__config['discord']['debug_guilds'] # My server's ids
        
        # General commands as `/ping` `/hello`
        self.add_cog(commands.GeneralCog(self))
        
        # Music commands as `/lyrics` 
        self.add_cog(commands.MusicCog(self.__config["spotifyApi"], self.__config['GeniusAPI']))        

    @property
    def __config(self) -> dict:
        with open("config.json", 'r') as fp:
            config: dict = json.load(fp)
        fp.close()
        return config
    

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
