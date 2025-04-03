"""
File: cogs.commands.py
Authors: 
    - Karina Solis

Resources:
    - Commands
        - https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html
    
    - Hybrid Commands
        - https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.hybrid_command
        - https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html#hybrid-commands
"""

import discord
from discord.ext import commands
import cogs.command_handling.settings_db as settings_db

class Commands(commands.Cog):
    """
    the command cog for the bot to implement the setting changes
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(description="Test Description")
    async def test(self, ctx):
        await ctx.send('Hello. Cmds were loaded.')
        
    @commands.hybrid_group()
    async def loop(ctx, name):
        await ctx.send(f"Showing tag: {name}")

    @loop.command(description="Start the loop with either the pre-established or custom configurations")
    async def start(self, ctx):
        pass
    
    @loop.command(description="End the loop")
    async def stop(self, ctx):
        pass