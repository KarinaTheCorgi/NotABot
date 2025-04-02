import os
from dotenv import load_dotenv
import pytest

import cogs.command_handling.settings_db as db

@pytest.fixture
def config():
    load_dotenv()
    return {"host" : os.getenv('db_host'),
            "port" : os.getenv('db_port'),
            "user" : os.getenv('db_user'),
            "password" : os.getenv('db_pass'),
            "database" : os.getenv('settings_db')}
    
@pytest.fixture
def faulty_config():
    return {"host" : "faulty_host",
            "port" : "12345",
            "user" : "faulty_user",
            "password" : "faulty_pass",
            "database" : "faulty_db"}

def test_connect(config):
    assert db.connect(config).is_connected()
    assert db.connect(config)
    
def test_faulty_connect(faulty_config):
    with pytest.raises(ValueError):
        db.connect(faulty_config)
        
@pytest.fixture
def topics():
    return ["relationships", "lifestyle", "career"]
        
@pytest.fixture
def faulty_topics():
    return ["hello", "world"]

def test_numerate_topics(topics):
    assert db.numerate_topics(topics) == [1, 2, 3]
    
def test_faulty_numerate_topics(faulty_topics):
    with pytest.raises(ValueError):
        db.numerate_topics(faulty_topics)
        
def test_insert_user_prompt_time():
    user_id = 12345
    prompt_time = 10000
    db.insert_user(user_id, prompt_time)
    
def test_insert_faulty_user_prompt_time():
    with pytest.raises(ValueError):
        db.insert_user("user")
        
def test_insert_user_topics():
    user_id = 12345
    topics = ["relationships", "career", "lifestyle"]
    topics = db.numerate_topics(topics)
    db.insert_user_topics(user_id, topics)
    
def test_insert_faulty_user_topics():
    with pytest.raises(ValueError):
        db.insert_user_topics("user")