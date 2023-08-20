import discord
from discord.commands import option
from discord.ext import commands
from embedBuider import EmbedConstructor


class GeneralCog(commands.Cog):
    """
    A cog for general commands.
    """

    # TODO: `/help`
    def __init__(self, bot: discord.Bot):
        self.bot: discord.Bot = bot

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
        embedInfo: dict = {
            "title": ":ping_pong: Pong!",
            "description": "Bot's latency: `{}` :mailbox_with_mail:".format(round(self.bot.latency * 1000, 0)),
            "color": discord.Color.gold(),
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