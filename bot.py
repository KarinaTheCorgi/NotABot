""""
File: bot.py
Authors: 
    - Asher Adighije
    - Taylor Hobbs
    - Kyle Miller
    - Karina Solis

Resources:
    - Setting Up Bot 
        - https://guide.pycord.dev/
        - https://realpython.com/how-to-make-a-discord-bot-python/
    - Commands
        - https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html
"""

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Loading Token and Creating Bot Variables
load_dotenv()
token = os.getenv('token')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# each user will need a different setting info, might want to create a class to hold custom info
polling_int = 6000
personality_prompt = ""

# Event Listeners, might want to seperate into another file when this list gets bigger
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user} (updated)')
    

# Commands, also might want to seperate into another file when this list gets bigger
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')
    
@bot.command()
async def start(ctx):
    # Starts polling loop, creates custom settings data
    """
    creates Settings for specified user, maybe prints out the default values on calling this function
    """
    ...
    
@bot.command()
async def stop(ctx):
    # exits polling loop
    """
    destroys the 
    """
    ...
    
@bot.command()
async def changeTime(ctx, time:float):
    polling_int = time
    await ctx.send(f'Changed Polling time to: {time} secs')
    
@bot.command()
async def changePerson(ctx, personality:str):
    personality_prompt = personality
    await ctx.send(f'Updated the personality of NotABot to: {personality}')


bot.run(token)