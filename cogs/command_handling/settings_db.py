"""
File: cogs.settings_db.py
Authors: 
    - Karina Solis

Resources:
    - Connecting to DB:
        - https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
        
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

def connect(config):
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise ValueError("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            raise ValueError("Database does not exist")
        else:
            raise ValueError(err)
    return cnx

def isInDB(user_id:int)->bool:
    try:
        query = ("SELECT COUNT(*) FROM Users WHERE user_id = %s")
        cnx = connect(valid_config)
        cursor = cnx.cursor()
        cursor.execute(query, (user_id))
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        if result and result[0] > 0:
            return True  
        return False
    except mysql.connector.Error as err:
        raise ValueError(f"Something went wrong {err}")

def insert_user(user_id:int, prompt_time:int = 10800):
    try:
        if (not isInDB(user_id)):
            users_query = ("insert into Users (user_id, prompt_time) values (%s, %s)")
            cnx = connect(valid_config)
            cursor = cnx.cursor()
            cursor.execute(users_query, (user_id, prompt_time))
            cursor.close()
            cnx.close()
        elif (isInDB(user_id)):
            users_query = ("insert into Users (user_id, prompt_time) values (%s, %s)")
            cnx = connect(valid_config)
            cursor = cnx.cursor()
            cursor.execute(users_query, (user_id, prompt_time))
            cursor.close()
            cnx.close()
    except mysql.connector.Error as err:
        raise ValueError(f"Something went wrong {err}")
    
def numerate_topics(topics:list[str])->list[int]:
    numbered_topics = []
    for topic in topics:
        if topic.lower() == "relationships":
            if 1 not in numbered_topics:
                numbered_topics.append(1)
        elif topic.lower() == "lifestyle":
            if 2 not in numbered_topics:
                numbered_topics.append(2)
        elif topic.lower() == "career":
            if 3 not in numbered_topics:
                numbered_topics.append(3)
        else:
            raise ValueError("Unclassified Topic")
    return numbered_topics    

def insert_user_topics(user_id:int, topics:list[int] = [1, 2, 3]):
    try:
        # have to make sure that a user with the user_id is in the table first or else you get err 1452
        if isInDB:
            topics_query = ("insert into UserTopics (user_id, topic_id) values (%s, %s)")
            cnx = connect(valid_config)
            cursor = cnx.cursor()
            for topic in topics:
                cursor.execute(topics_query, (user_id, topic))
            cursor.close()
            cnx.close()
        else:
            insert_user(user_id)
            # i  know this code is repetitive but idc
            topics_query = ("insert into UserTopics (user_id, topic_id) values (%s, %s)")
            cnx = connect(valid_config)
            cursor = cnx.cursor()
            for topic in topics:
                cursor.execute(topics_query, (user_id, topic))
            cursor.close()
            cnx.close()
            
    except mysql.connector.Error as err:
        raise ValueError(f"Something went wrong {err}")
