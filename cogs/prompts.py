"""
File: cogs.commands.py
Authors: 
    - Karina Solis

Resources:
   - https://discordpy.readthedocs.io/en/stable/ext/tasks/index.html
"""

import openai

# this will handle the initial prompts (triggered by no reply in [prompt_time] secs)
from discord.ext import commands

from cogs.command_handling import settings_db as db

class Prompts(commands.Cog):
    ...