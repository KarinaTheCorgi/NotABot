"""
File: cogs.commands.py
Authors: 
    - Karina Solis

Resources:
   - https://discordpy.readthedocs.io/en/stable/ext/tasks/index.html
"""

import openai

# this will handle the initial prompts (triggered by no reply in [prompt_time] secs)
from discord.ext import tasks, commands

from cogs.command_handling import settings_db as db
from cogs.command_handling.commands import Topic

import random
from reddit.generator import get_reddit_style_response


class Prompts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prompt_users.start()  # Start the loop on load

    @tasks.loop(seconds=60)  # check every minute
    async def prompt_users(self):
        # get users from the DB
        users = db.get_all_users()  
        for user_id in users:
            prompt_time = db.get_prompt_time(user_id)
            topics = db.get_topics(user_id)

            # Implement logic to check last interaction timestamp if needed
            # Assuming time has passed:
            topic = random.choice(topics)
            topic_name = Topic(topic).name # topic is not impemented

            response = await get_reddit_style_response(topic_name) # this function is not implemented yet
            user = await self.bot.fetch_user(user_id)
            await user.send(response)