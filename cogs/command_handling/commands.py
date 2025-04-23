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

    # Lone Commands

    @commands.hybrid_command(name = "ping", description = "Test Description")
    async def ping(self, ctx: commands.Context):
        await ctx.send('Pong....')
    
    @commands.hybrid_command(description="Start the loop with either the pre-established or custom configurations")
    async def start(self, ctx: commands.Context, propmt_time:int=10800, topic1:Topic=None, topic2:Topic=None, topic3:Topic=None):
        await ctx.defer()
        topics = [topic1, topic2, topic3]
        if topics == [None, None, None]:
            topics = [1,2,3]
        if db.is_in_db(ctx.author.id):
            await ctx.send("You are already on my list, silly goose.")
        else:
            db.set_prompt_time(ctx.author.id, propmt_time)
            db.add_topics(ctx.author.id, topics)
            await ctx.send("You just made the list.")
    
    @commands.hybrid_command(description="Stops the loop")
    async def stop(self, ctx: commands.Context):
        await ctx.defer()
        result = db.delete_user(ctx.author.id)
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
        
    # Update Settings
        
    @update.command(description="Updates the time between last reply and new prompt.")
    async def time(self, ctx: commands.Context, time: int=10800):
        if db.is_in_db(ctx.author.id):
            db.set_prompt_time(ctx.author.id, time)
            await ctx.send(f'You updated the new time between last reply and new prompt to: {time} seconds.')
        else:
            await ctx.send("You aren't on the list...Try starting me before updating your settings.")
    
    @add.command(description="Updates the topics you will be prompted.")
    async def topic(self, ctx: commands.Context, topic1:Topic, topic2:Topic=None, topic3:Topic=None):
        await ctx.defer()
        topics_to_add = (topic1.value, topic2.value if topic2 != None else None, topic3.value if topic3 != None else None)
        if db.is_in_db(ctx.author.id):
            topics_in_db = db.get_topics(ctx.author.id)
            for topic_int in topics_to_add:
                if topic_int not in topics_in_db and topic_int != None: 
                    db.add_topics(ctx.author.id, (topic_int,))
            ctx.command =self.bot.get_command("show topics")
            await self.bot.invoke(ctx)
        else:
            await ctx.send("You aren't on the list...Try starting me before updating your settings.")
        
    @remove.command(description="Updates the topics you will be prompted.")
    async def topic(self, ctx: commands.Context, topic1:Topic, topic2:Topic=None, topic3:Topic=None):
        await ctx.defer()
        topics = [topic1, topic2, topic3]
        if topics != None:
            db.remove_topics(ctx.author.id, topics)
            updated_topics = db.get_topics(ctx.author.id)
            topic_str = ""
            for topic in updated_topics:
                topic_str += (f"\n- {topic.name}")
        else:
            await ctx.send(f'You added: {topic} to your list of topics')
        
    # Show Settings
        
    @show.command(description="Displays the chosen time between no reply and a new prompt.")
    async def time(self, ctx: commands.Context):
        await ctx.defer()
        time = db.get_prompt_time(ctx.author.id)
        await ctx.send(f"If you don't respond to me in {time} seconds, I'll come up with a new question.")
    
    @show.command(description="Displays the topics you will be prompted.")
    async def topics(self, ctx: commands.Context):
        await ctx.defer()
        topics = db.get_topics(ctx.author.id)
        topics_str = ""
        topics_str += (f'Your enlisted topics are: ')
        for topic_int in topics:
                topics_str += (f"\n- {Topic(topic_int).name}")
        await ctx.send(topics_str)
            
    @show.command(description="Displays both the time and topics")
    async def settings(self, ctx: commands.Context):
        await ctx.defer()
        prompt_time = db.get_settings(ctx.author.id)[0]
        topics = db.get_topics(ctx.author.id)
       
        if prompt_time == None:
            await ctx.send("You aren't on the list...Try starting me first.")
        else:
            time_msg = (f"If you don't respond to me in {prompt_time} seconds, I'll come up with a new question.")
            topics_msg = (f'\nYour enlisted topics are: ')
            for topic_int in topics:
                topics_msg += (f"\n- {Topic(topic_int).name}")
            await ctx.send(time_msg + topics_msg)
        