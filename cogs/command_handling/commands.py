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
from discord.ext import commands
from discord import app_commands

import cogs.command_handling.settings_db as settings_db

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
    async def start(self, ctx):
        await ctx.send(f"Doing stuff to start bot...")
    
    @commands.hybrid_command(description="Stops the loop")
    async def stop(self, ctx):
        await ctx.send(f"Doing stuff to stop bot...")
        
    @commands.hybrid_group()
    async def update(ctx: commands.Context, name):
        await ctx.send(f"Showing tag: {name}")
        
    @update.command(description="Updates the time between last reply and new prompt.")
    async def time(self, ctx: commands.Context, time: int):
        await ctx.send(f'You updated the new time between last reply and new prompt to: {time} seconds.')
        
    async def topics_autocomplete(current: str,):
        topics = ["relationships", "lifestyle", "career"]
        return [
            app_commands.Choice(name=topic, value=topic)
            for topic in topics if current.lower() in topic.lower()
        ]

    @update.command(description="Updates the topics you will be prompted.")
    @app_commands.autocomplete(topic=topics_autocomplete)
    async def topics(self, ctx: commands.Context, topic: str):
        await ctx.send(f'You added: {topic} to your list of topics')
