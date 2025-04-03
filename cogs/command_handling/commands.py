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

    @commands.hybrid_command(name = "test", description = "Test Description")
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
        
    @update.command()
    async def prompt_time(self, ctx, *args):
        await ctx.send()
        
    async def topics_autocomplete(interaction: discord.Interaction, current: str,):
        topics = ["relationships", "lifestyle", "career"]
        return [
            app_commands.Choice(name=topic, value=topic)
            for topic in topics if current.lower() in topic.lower()
        ]

    @update.command()
    @app_commands.autocomplete(topic=topics_autocomplete)
    async def topics(interaction: discord.Interaction, topic: str):
        await interaction.response.send_message(f'You added: {topic} to your list of topics')
