"""
File: settings.py
Authors: 
    - Karina Solis
Resources:
    - Cogs
        - https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html
"""
#i literally dk what im doing or if any of this makes sense. theres probably a much easier and simpler way to be doing this but im tired and scared
import os
import sys
import subprocess
from time import sleep
from threading import Thread

import discord
from discord.ext import commands
from dotenv import load_dotenv

import mysql.connector



class Settings(commands.Cog):
    def __init__(self, user):
        # Connect to a database
        load_dotenv() #unsure if needed

        self.db = mysql.connector.connect(
            host = os.getenv('db_host'),
            port = os.getenv('db_port'),
            user = os.getenv('db_user'),
            password = os.getenv('db_pass'),
            database = os.getenv('settings_db')
        )
        self.user = user
        
    async def isInDB(self)->bool:
        """
        checks if the user is in the database already
        """ 
        val = (self.user,)
        self.db.cursor().execute("SELECT COUNT(*) FROM Users WHERE author_id = %s", val)
        result = self.db.cursor().fetch()
        
        if result and int(result[0]) > 0:
            return True  
        return False
        
    def areArgsNorm(self, *args)->bool:
        """
        checks if the args are valid 
        """
        ...
        
    async def validateArgs(self, *args):
        if Settings.areArgsNorm(*args):  
            return
        else:
            # make em norm idk
            ...
        
        
class SettingsCmds(commands.Cog):
    """
    the command cog for the bot to implement the setting changes
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def test(self, ctx):
        await ctx.send('Hello. Cmds were loaded.')
    
    @commands.command()
    async def start(self, ctx, *args):
        # Starts polling loop, creates custom settings data
        """
        creates Settings for specified user if there isnt one
        """
        settings = self.bot.get_cog('Settings')
        if settings is not None:
            if settings.isInDB(ctx.author.id):
                await ctx.send("You're already in the database.")
            else:
                await settings.validateArgs(*args)
                await settings.addUser(ctx.author.id, *args)
        
    @commands.command()
    async def stop(self, ctx):
        # exits polling loop
        """
        destroys the entry in db from specified user if there is one
        """
        settings = self.bot.get_cog('Settings')
        if settings is not None:
            if settings.isInDB(ctx.author.id):
                await settings.remove_user(ctx.author.id)
            else:
                await ctx.send("You're not in the database.")
            