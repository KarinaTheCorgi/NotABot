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
    
class TopicConverter(commands.Converter):
    async def convert(self, ctx, arg: str):
        try:
            return Topic[arg.upper()]
        except KeyError:
            raise commands.BadArgument(f"Invalid topic: {arg}. Please choose from the available topics.")
    
class Commands(commands.Cog):
    """
    the command cog for the bot to implement the setting changes
    """
    def __init__(self, bot):
        self.bot = bot

    # Lone Commands

    @commands.hybrid_command(name = "ping", description = "Test Description")
    async def ping(self, ctx: commands.Context):
        await ctx.send('Pong....')
    
    @commands.hybrid_command(description="Start the loop with either the pre-established or custom configurations")
    async def start(self, ctx: commands.Context, propmt_time:int=10800, *topics:Topic):
        if topics == None:
            topics = [1, 2, 3]
        if db.is_in_db(ctx.author):
            await ctx.send("You are already on my list, silly goose.")
        else:
            db.set_prompt_time(ctx.author, propmt_time)
            db.add_topics(topics)
            await ctx.send("You just made the list.")
    
    @commands.hybrid_command(description="Stops the loop")
    async def stop(self, ctx: commands.Context):
        result = db.delete_user(ctx.author)
        if result == None:
            await ctx.send("You weren't on my list to begin with...Try starting before you stop.")
        else:
            await ctx.send(f"User Deleted from DB. Use /start to start again.")
        
    # Command Groups
        
    @commands.hybrid_group()
    async def update(ctx: commands.Context, name):
        await ctx.send(f"Showing tag: {name}")
        
    @commands.hybrid_group()
    async def add(ctx: commands.Context, name):
        await ctx.send(f"Showing tag: {name}")
        
    @commands.hybrid_group()
    async def remove(ctx: commands.Context, name):
        await ctx.send(f"Showing tag: {name}")
        
    @commands.hybrid_group()
    async def show(ctx: commands.Context, name):
        await ctx.send(f"Showing tag: {name}")
        
    # Grouped Commands
        
    @update.command(description="Updates the time between last reply and new prompt.")
    async def time(self, ctx: commands.Context, time: int=10800):
        if db.is_in_db(ctx.author):
            db.set_prompt_time(time)
            await ctx.send(f'You updated the new time between last reply and new prompt to: {time} seconds.')
        else:
            await ctx.send("You aren't on the list...Try starting me before updating your settings.")
    
    @add.command(description="Updates the topics you will be prompted.")
    async def topic(self, ctx: commands.Context, *topics: Topic):
        if db.is_in_db(ctx.author):
            topics_int = []
            topics_str = ""
            for topic in topics:
                topics_int.append(topic.value)
                topics_str += (f"\n- {topic.name}")
            db.set_topics(topics_int)
            await ctx.send(f'You updated your topics to: ' + topics_str)
        else:
            await ctx.send("You aren't on the list...Try starting me before updating your settings.")
        
    @remove.command(description="Updates the topics you will be prompted.")
    async def topic(self, ctx: commands.Context, *topics: Topic):
        if topics != None:
            db.remove_topics(topics)
            updated_topics = db.get_topics(ctx.author)
            topic_str = ""
            for topic in updated_topics:
                topic_str += (f"\n- {topic.name}")
        else:
            await ctx.send(f'You added: {topic} to your list of topics')
        
    @show.command(description="Displays the chosen time between no reply and a new prompt.")
    async def time(self, ctx: commands.Context):
        time = db.get_prompt_time(ctx.author)
        await ctx.send(f"If you don't respond to me in {time} seconds, I'll come up with a new question.")
    
    @show.command(description="Displays the topics you will be prompted.")
    async def topics(self, ctx: commands.Context):
        topics = db.get_topics(ctx.author)
        topics_str = ""
        await ctx.send(f'Your enlisted topics are: ')
        for topic in topics:
                topics_str += (f"\n- {topic.name}")
            
    @show.command(description="Displays both the time and topics")
    async def settings(self, ctx: commands.Context):
        prompt_time = db.get_settings(ctx.author)[0]
        topics = db.get_topics(ctx.author)[0]
        if prompt_time == None:
            await ctx.send("You aren't on the list...Try starting me first.")
        else:
            time_msg = (f"If you don't respond to me in {prompt_time} seconds, I'll come up with a new question.")
            topics_msg = (f'\nYour enlisted topics are: ')
            for topic in topics:
                topics_msg += (f"\n- {topic}")
            await ctx.send(time_msg + topics_msg)
        