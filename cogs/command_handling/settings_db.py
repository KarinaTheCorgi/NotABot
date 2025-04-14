"""
File: cogs.command_handling.settings_db.py
Authors: 
    - Karina Solis

Resources:
    - Connecting to DB:
        - https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
        
    - Using deco as error handling:
        - https://medium.com/swlh/handling-exceptions-in-python-a-cleaner-way-using-decorators-fae22aa0abec
        
    - Inserting Data into DB:
        - https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
        
    - SQL Syntax
        - https://www.w3schools.com/sql/default.asp
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
    result = cursor.fetchall()
    cnx.commit()
    cursor.close()
    cnx.close()
    return result

@exception_handler
def is_in_db(user_id:int)->bool:
    query_str = ("SELECT COUNT(*) FROM Users WHERE user_id = %s")
    result = query(query_str, (user_id,))
    if result and result[0][0] > 0:
        return True  
    return False

@exception_handler
def set_prompt_time(user_id:int, prompt_time:int = 10800):
    if (not is_in_db(user_id)):
        users_query = ("INSERT INTO Users (prompt_time, user_id) VALUES (%s, %s)")
        print(f"{user_id} inserted into Users db")
    else:
        users_query = ("UPDATE Users SET prompt_time = %s WHERE user_id = %s")
        print(f"{user_id} prompt_time updated")
    query(users_query, (prompt_time, user_id))

@exception_handler
def add_topics(user_id:int, topics:list[int] = [1, 2, 3]):
    if (not is_in_db(user_id)):
        set_prompt_time(user_id)

    topics_query = ("INSERT INTO UserTopics (user_id, topic_id) VALUES (%s, %s)")
    print(f"{user_id} topics updated.")
    
    for topic in topics:
        query(topics_query, (user_id, topic))
        
@exception_handler
def remove_topics(user_id:int, topics:list[int]):
    if (not is_in_db(user_id)):
        set_prompt_time(user_id)

    topics_query = ("DELETE FROM UserTopics WHERE user_id = %s AND topic_id = %s")
    print(f"{user_id} topics updated.")
    
    for topic in topics:
        query(topics_query, (user_id, topic))
    
@exception_handler
def get_prompt_time(user_id:int):
    if is_in_db(user_id):
        get_prompt_query = ("SELECT prompt_time From Users WHERE user_id = %s")
        return query(get_prompt_query, (user_id,))[0][0]
    else:
        return None

@exception_handler
def get_topics(user_id:int):
    if is_in_db(user_id):
        get_topics_query = ("SELECT topic_id FROM UserTopics where user_id = %s")
        list_of_lists_of_topics = query(get_topics_query, (user_id,))
        topics = []
        for list in list_of_lists_of_topics:
            topics.append(list[0])
        return topics
    else:
        return None
    
@exception_handler
def get_settings(user_id:int):
    if is_in_db(user_id):
        return get_prompt_time(user_id), get_topics(user_id)
    else:
        return None
    
@exception_handler
def delete_user(user_id:int):
    if is_in_db(user_id):
        delete_topics_query = ("DELETE FROM UserTopics WHERE user_id = %s")
        delete_prompt_time_query = ("DELETE FROM Users WHERE user_id = %s")
        query(delete_topics_query, (user_id,))
        query(delete_prompt_time_query, (user_id,))
    else:
        return None
    
@exception_handler
def get_all_users():
    query_str = "SELECT user_id FROM Users"
    results = query(query_str, ())
    return [user[0] for user in results]