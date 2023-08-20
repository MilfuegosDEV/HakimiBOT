import discord
import json
import commands


class HakimiBot(discord.Bot):

    def __init__(self, description=None, *args, **options):
        super().__init__(description, *args, **options)

        # General commands as `/ping` `/hello`
        self.add_cog(commands.GeneralCog(self))

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
        # Getting config information:
        with open("config.json", 'r') as fp:
            config: dict = json.load(fp)
        fp.close()

        BOT.debug_guilds = config['debug_guilds']

        # RUNNING BOT
        BOT.run(config["token"])

    except discord.errors.LoginFailure as LoginFailure:
        print(LoginFailure)

    except Exception as e:
        print(e)
