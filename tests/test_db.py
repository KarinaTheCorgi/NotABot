import os
from dotenv import load_dotenv
import pytest

import cogs.command_handling.settings_db as db

from cogs.prompts import Prompts
from cogs.command_handling.commands import Topic


# Settings DB Test Fixtures
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

# Bot Test Fixtures



@pytest.fixture
def relationships():
    return Topic("relationships")

@pytest.fixture
def lifestyle():
    return Topic("lifestyle")

@pytest.fixture
def career():
    return Topic("career")

@pytest.fixture
def prompt():
    return Prompts()




# Settings DB Tests

def test_connect(config):
    assert db.connect(config).is_connected()
    assert db.connect(config)
    
def test_faulty_connect(faulty_config):
    with pytest.raises(ValueError):
        db.connect(faulty_config)
        
# Prompt Tests
        
def test_generate_prompts(prompt, relationships, lifestyle, career):
    assert prompt.generate_prompt(relationships)
    assert prompt.generate_prompt(lifestyle)
    assert prompt.generate_prompt(career)