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
        
    - Auto Complete
        - https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.app_commands.autocomplete
"""

import discord
from enum import Enum
from discord.ext import commands
from discord import app_commands

import cogs.command_handling.settings_db as db

class Topic(Enum):
    relationships = 1
    lifestyle = 2
    career = 3
    
class Commands(commands.Cog):
    """
    the command cog for the bot to implement the setting changes
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name = "ping", description = "Test Description")
    async def ping(self, ctx: commands.Context):
        await ctx.send('Pong....')
    
    @commands.hybrid_command(description="Start the loop with either the pre-established or custom configurations")
    async def start(self, ctx: commands.Context):
        db.add_topics()
        await ctx.send(f"Doing stuff to start bot...")
    
    @commands.hybrid_command(description="Stops the loop")
    async def stop(self, ctx: commands.Context):
        await ctx.send(f"Doing stuff to stop bot...")
        
    @commands.hybrid_group()
    async def update(ctx: commands.Context, name):
        await ctx.send(f"Showing tag: {name}")
        
    @update.command(description="Updates the time between last reply and new prompt.")
    async def time(self, ctx: commands.Context, time: int):
        await ctx.send(f'You updated the new time between last reply and new prompt to: {time} seconds.')
    
    @update.command(description="Updates the topics you will be prompted.")
    async def topics(self, ctx: commands.Context, topic: Topic):
        await ctx.send(f'You added: {topic} to your list of topics')
        
    @commands.hybrid_group()
    async def show(ctx: commands.Context, name):
        await ctx.send(f"Showing tag: {name}")
        
    @show.command(description="Displays the chosen time between no reply and a new prompt.")
    async def time(self, ctx: commands.Context):
        time = 30
        await ctx.send(f"If you don't respond to me in {time} seconds, I'll come up with a new question.")
    
    @show.command(description="Displays the topics you will be prompted.")
    async def topics(self, ctx: commands.Context):
        topics = [1, 2, 3]
        await ctx.send(f'Your enlisted topics are: ')
        for topic in topics:
            await ctx.send(f'- {topic}')
            
    @show.command(description="Displays both the time and topics")
    async def settings(self, ctx: commands.Context):
        time = 30
        topics = [1, 2, 3]
        await ctx.send(f"If you don't respond to me in {time} seconds, I'll come up with a new question.")
        await ctx.send(f'Your enlisted topics are: ')
        for topic in topics:
            await ctx.send(f'- {topic}')