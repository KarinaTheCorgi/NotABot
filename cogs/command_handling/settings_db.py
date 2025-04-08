"""
File: cogs.settings_db.py
Authors: 
    - Karina Solis

Resources:
    - Connecting to DB:
        - https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
        
    - Using deco as error handling:
        - https://medium.com/swlh/handling-exceptions-in-python-a-cleaner-way-using-decorators-fae22aa0abec
        
    - Inserting Data into DB:
        - https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
        
"""

import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode

load_dotenv()
valid_config = {"host" : os.getenv('db_host'),
                "port" : os.getenv('db_port'),
                "user" : os.getenv('db_user'),
                "password" : os.getenv('db_pass'),
                "database" : os.getenv('settings_db')}

def exception_handler(func:callable):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except mysql.connector.Error as err:
            raise ValueError(f"{func.__name__} could not be completed. {err}")
    return inner_function

@exception_handler
def connect(config):
    return mysql.connector.connect(**config)

@exception_handler
def query(query: str, items):
    cnx = connect(valid_config)
    cursor = cnx.cursor()
    cursor.execute(query, items)
    result = cursor.fetchone()
    cnx.commit()
    cursor.close()
    cnx.close()
    return result

@exception_handler
def is_in_db(user_id:int)->bool:
    query_str = ("SELECT COUNT(*) FROM Users WHERE user_id = %s")
    result = query(query_str, (user_id,))
    if result and result[0] > 0:
        return True  
    return False

@exception_handler
def set_prompt_time(user_id:int, prompt_time:int = 10800):
    if (not is_in_db(user_id)):
        users_query = ("INSERT INTO Users (prompt_time, user_id) VALUES (%s, %s)")
        print("user inserted into Users db")
    else:
        users_query = ("UPDATE Users SET prompt_time = %s WHERE user_id = %s")
        print("user updated")
    query(users_query, (prompt_time, user_id))

@exception_handler
def add_topics(user_id:int, topics:list[int] = [1, 2, 3]):
    if (not is_in_db(user_id)):
        set_prompt_time(user_id)

    topics_query = ("INSERT INTO UserTopics (user_id, topic_id) VALUES (%s, %s)")
    
    for topic in topics:
        query(topics_query, (user_id, topic))
        
@exception_handler
def get_settings(user_id:int)->tuple(int, list[int]):
    get_prompt_query = ("SELECT * From Users WHERE user_id = %s")