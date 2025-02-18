""""

Resources:
    - Setting Up Bot 
        - https://realpython.com/how-to-make-a-discord-bot-python/
    - Commands
        - https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html
"""

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('token')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
polling_int = 6000

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

#Commands, might want to seperate into another file when this list gets bigger
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')
    
@bot.command()
async def changeTime(ctx, time:float):
    polling_int = time
    await ctx.send(f'Changed Polling time to: {time} secs')


bot.run(token)