""""
File: bot.py
Authors: 
    - Karina Solis

Resources:
    - Setting Up Bot 
        - https://guide.pycord.dev/
        - https://realpython.com/how-to-make-a-discord-bot-python/
    
    - Setting up automatic git pulling
        - https://stackoverflow.com/questions/11329917/restart-python-script-from-within-itself/33334183#33334183
        - https://www.geeksforgeeks.org/python-subprocess-module/
        - https://www.geeksforgeeks.org/multithreading-python-set-1/
        - https://realpython.com/intro-to-python-threading/#daemon-threads
"""

import os
import sys
import subprocess
from time import sleep
from threading import Thread

import discord
from discord.ext import commands
from dotenv import load_dotenv

import cogs.command_handling.commands as cmds
import cogs.events as events
import cogs.prompts as prompts

def git_pull():
    if "Already up to date." in str(subprocess.run(["git", "pull"], capture_output=True, text=True)):
        return False
    else:
        return True
    
def restart():
    os.execv(sys.executable, ['python'] + sys.argv)
    
def update():
    while True:
        sleep(10)
        if git_pull():
            restart()
            
# Creates a new (background) thread to auto update from git          
Thread(target=update, daemon=True).start()

# Loading Token and Creating Bot Variables
load_dotenv()
token = os.getenv('token')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Event Listeners, might want to seperate into another file when this list gets bigger
@bot.event
async def on_ready():
    bot.add_cog(cmds.Commands(bot))
    bot.add_cog(events.EventsListener(bot))
    bot.add_cog(prompts.Prompts(bot))
    
    print(f'We have logged in as {bot.user}')    

# Test command
@bot.command()
async def ping(ctx):
    await ctx.send('Pong....')
    
bot.run(token)
