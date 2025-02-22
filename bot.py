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
        
    - Setting up automatic git pulling
        - https://stackoverflow.com/questions/11329917/restart-python-script-from-within-itself/33334183#33334183
        - https://www.geeksforgeeks.org/python-subprocess-module/
        - https://www.geeksforgeeks.org/multithreading-python-set-1/
        - https://realpython.com/intro-to-python-threading/#daemon-threads
        
    - Setting up a database
        - https://www.w3schools.com/python/python_mysql_getstarted.asp
"""

import os
import sys
import subprocess
from time import sleep
from threading import Thread

import discord
from discord.ext import commands
from dotenv import load_dotenv

import mysql.connector

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


# Connect to a database
db_host = os.getenv('db_host')
db_port = os.getenv('db_port')
db_user = os.getenv('db_user')
db_pass = os.getenv('db_pass')
db_database_name = os.getenv('settings_db')

db = mysql.connector.connect(
  host = db_host,
  port = db_port,
  user = db_user,
  password = db_pass,
  database = db_database_name
)

# each user will need a different setting info, might want to create a class to hold custom info
polling_int = 6000
personality_prompt = ""

# Event Listeners, might want to seperate into another file when this list gets bigger
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')    

# Commands, also might want to seperate into another file when this list gets bigger
@bot.command()
async def ping(ctx):
    await ctx.send('Pong....')
    
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