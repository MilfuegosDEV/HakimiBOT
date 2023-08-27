import discord
import openai
from discord.commands import option
from discord.ext import commands
from messages import EmbedConstructor

class GPTCog(commands.Cog):

    def __init__(self, gptConnect: openai) -> None:
        
        super().__init__()

        self.__chatgpt: openai = gptConnect
        