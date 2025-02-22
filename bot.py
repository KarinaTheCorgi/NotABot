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


# Event Listeners, might want to seperate into another file when this list gets bigger
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')    

# Commands, also might want to seperate into another file when this list gets bigger
@bot.command()
async def ping(ctx):
    await ctx.send('Pong....')
    print(ctx.message.author.id)
    
    
@bot.command()
async def start(ctx, prompt_time:int = 10800, reply_time:int = 5):
    # Starts polling loop, creates custom settings data
    """
    creates Settings for specified user
    """
    # prompt_time: time between each initial prompt given
    if prompt_time < 30:
        if prompt_time <= 0:
            sleep(3)
            await ctx.reply(f"Nice try. I'll give you 30 seconds between each prompt. I need time to think.")
            prompt_time = 30
        else:
            sleep(3)
            await ctx.reply(f"{prompt_time} seconds is stupid. Best I can get to you is {prompt_time + 30} seconds.")
            prompt_time = prompt_time + 30
    
    # reply_time: how long the bot will give the user to respond
    if reply_time < 5:
        if reply_time <= 0:
            sleep(3)
            await ctx.reply(f"Ok smart guy. I'll give you 10 seconds for an answer. After that, I won't expect anything from you.")
            reply_time = 10
        else:
            sleep(3)
            await ctx.reply(f"{reply_time} seconds is unreasonable. I can wait around for {reply_time + 10} seconds.")
            reply_time = reply_time + 10
    
    check_sql = "SELECT COUNT(*) FROM Users WHERE author_id = %s"
    val = (ctx.author.id)
    db.cursor().execute(check_sql, val)
    
    if db.cursor().fetchone()[0] > 0:
        sleep(3)
        await ctx.reply("You're already on my radar. Please stop before you start again.")   
    else:
        insert_sql = "INSERT INTO Users (author_id, prompt_time, reply_time) VALUES (%s, %s, %s)"
        val = (str(ctx.author.id), str(prompt_time), str(reply_time))
        db.cursor().execute(insert_sql, val)
        db.commit()
        sleep(3)
        await ctx.send(f"Oop you've just added your name to a list of people for me to bug. I'll try to annoy you every {prompt_time} seconds")
    
    

    
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
    

bot.run(token)