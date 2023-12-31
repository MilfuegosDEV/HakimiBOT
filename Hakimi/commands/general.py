import discord
from discord.commands import option
from discord.ext import commands
from messages import EmbedConstructor


class GeneralCog(commands.Cog):
    """
    A cog for general commands.
    """

    # TODO: `/help`
    def __init__(self, bot: discord.Bot):
        self.__bot: discord.Bot = bot

    @commands.slash_command(description='Say hello to someone')
    @option(name='name', type=str, description="Someone's name")
    async def hello(self, ctx: discord.context.ApplicationContext, name: str = None):
        """
        Say hello to someone.

        Parameters:
            ctx (discord.context.ApplicationContext): The interaction context.
            name (str): Optional. The name of the person to greet. Defaults to None.
        """
        name: str = name or ctx.author.name
        await ctx.respond('Hello {}!'.format(name))

    @commands.slash_command(name='ping', description="Bot's latency")
    async def ping(self, ctx: discord.context.ApplicationContext):
        """
        Retrieves the bot's latency.

        Parameters:
            ctx (discord.context.ApplicationContext): The interaction context.
        """
        latency_ms = round(self.__bot.latency * 1000, 0)
        description = f"Bot's latency: `{latency_ms}` ms"

        if len(description) <= 4096:
            embedInfo = {
                "title": ":ping_pong: Pong!",
                "description": description,
                "color": discord.Color.gold(),
                "timestamp": "now",
                "footer": {
                    "text": "v1.0.0",
                }
            }
        else:
            embedInfo = {
                "title": ":warning: Ping Warning",
                "description": "The bot's latency is too high to display.",
                "color": discord.Color.red(),
                "timestamp": "now",
                "footer": {
                    "text": "v1.0.0",
                }
            }

        embed = EmbedConstructor(embedInfo)
        await ctx.respond(embed=embed.get_embed())

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Event handler for member join.

        Parameters:
            member (discord.Member): The member who joined.
        """
        await member.send('Welcome to the server!')
