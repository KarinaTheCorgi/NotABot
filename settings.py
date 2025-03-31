import os
import mysql.connector as sql
from dotenv import load_dotenv
from discord.ext import commands


# why did i think it was a good idea to do this. i dont know what im doing. i dont know what decorators are.
# i think im gonna get rid of this and make it 
def validateArgs(func):
    def wrapper(self, **kwargs):
        prompt_time = 0
        reply_time = 0
        topics = []
        for k, val in kwargs.items():
            if k == "user_id":
                if self.isInDB():
                    raise ValueError("user already in DB")
                else:
                    pass
            if k == "prompt_time":
                self.prompt_time = val
            elif k == "reply_time":
                self.reply_time = val
            elif k == "topics":
                if isinstance(val, list[str]):
                    for topic in val:
                        if topic == "relationship":
                            self.addTopic(1)
                        elif topic == "career":
                            self.addTopic(2)
                        elif topic == "school":
                            self.addTopic(3)
                        elif topic == "lifestyle":
                            self.addTopic(4)
                        else:
                            raise ValueError("Unknown Topic.")
                else:
                    raise ValueError("Topics should be a list. Even if there's only one item in the list.")
                
                
        # literally where is the other positional arh 
        return func(self, **kwargs)
    return wrapper
    
class Settings(commands.Cog):
    def __init__(self, user):
        # Connect to the database
        load_dotenv()

        self.db = sql.connect(
            host = os.getenv('db_host'),
            port = os.getenv('db_port'),
            user = os.getenv('db_user'),
            password = os.getenv('db_pass'),
            database = os.getenv('settings_db')
        )
        self.user = user
        cursor = self.db.cursor()
        self.prompt_time = 0
        self.reply_time = 0
        self.topics = []
        
        if self.isInDB():
            sql1 = ("SELECT user_id, prompt_time, reply_time FROM Users WHERE user_id = %s")
            cursor.execute(sql1, (self.user,))
            userdata = cursor.fetchall()
            self.prompt_time = userdata[0][1]
            self.reply_time = userdata[0][2]
            sql2 = ("SELECT topic_name FROM Topics JOIN UserTopics ON Topics.topic_id = UserTopics.topic_id WHERE user_id = %s")
            cursor.execute(sql2, (userdata[0][0],))
            topicdata = cursor.fetchall()
            for row in topicdata:
                self.topics.append(row[0])
        else:
            #self.addUser(user_id = self.user, prompt_time = 10800, reply_time = 30)
            pass
        
    def __str__(self):
        return(f"user_id: {self.user} prompt_time: {self.prompt_time} reply_time: {self.reply_time} topics: {self.topics}")
    
    def __repr__(self):
        return(f"user_id: {self.user} prompt_time: {self.prompt_time} reply_time: {self.reply_time} topics: {self.topics}")
        
    def isInDB(self)->bool:
        """
        checks if the user is in the database already
        """ 
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM Users WHERE user_id = %s", (self.user,))
        result = cursor.fetchone()
        cursor.close()
        if result and result[0] > 0:
            return True  
        return False
        
    def removeUser(self):
        ...
    
    @validateArgs
    def changePromptTime(self, prompt_time:int):
        ...
    
    @validateArgs   
    def changeReplyTime(self, reply_time:int):
        ...
     
    @validateArgs       
    def addTopics(self, topics:list[str])->None:
        # adds an entry in the UserTopics (user_id, topic_id)
        # read topics as kwargs and handle in validateArgs deco
        cursor = self.db.cursor()
        for topic in topics:
                cursor.execute(f"INSERT INTO UserTopics (user_id, topic_id) VALUES ({self.user}, {topic})")
                cursor.close()
    
    @validateArgs
    def addUser(self, **kwargs)->None:
        # idk what im doing wrong but its saying that it works sometimes but then doesnt add a user. so like then what is it doing...
        cursor = self.db.cursor()
        cursor.execute(f"INSERT INTO Users (user_id, prompt_time, reply_time) VALUES ({self.user}, {self.prompt_time}, {self.reply_time})")
        cursor.close()

class SettingsCmds(commands.Cog):
    """
    the command cog for the bot to implement the setting changes
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="testting slash commands")
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