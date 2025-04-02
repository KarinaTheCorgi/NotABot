"""
File: cogs.commands.py
Authors: 
    - Karina Solis

Resources:
    - Commands
        - https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html
"""

import discord
from discord.ext import commands
import cogs.command_handling.settings_db as settings_db

loop = discord.SlashCommandGroup("loop", "Loop related commands")

class Commands(commands.Cog):
    """
    the command cog for the bot to implement the setting changes
    """
    def __init__(self, bot):
        self.bot = bot

    @discord.hybrid_command(description="testing commands")
    async def test(self, ctx):
        await ctx.send('Hello. Cmds were loaded.')

    @loop.command(description="Start the loop with either the pre-established or custom configurations")
    async def start(self, ctx):
        pass