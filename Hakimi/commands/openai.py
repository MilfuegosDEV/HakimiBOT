import discord
from discord.commands import option
from discord.ext import commands

import openai

class GPTCog(commands.Cog):
    __gptCommands = discord.SlashCommandGroup(name='gpt', description='Ask something to Chat GPT')

    def __init__(self, gptConnect: openai) -> None:
        super().__init__()

        self.__gptConnect: openai = gptConnect