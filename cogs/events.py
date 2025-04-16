"""
File: cogs.events.py
Author:
    - Karina Solis
Resources:
    - 
"""
from threading import Thread, Event

# What I want this to do: 
# open a thread for each user (that waits for their specified prompt time)
# handles the reset of the loop with on a reply event
# 



class EventHandler():
    
    def exception_handler(func:callable):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError as e:
                raise ValueError(f"Something went wrong. {e}")
        return inner
    
    def __init__(self, user_id:int, prompt_time:int):
        self.user_id = user_id
        self.prompt_time = prompt_time
        # Events that would influence the state of thread
        self.prompt_event = False
        self.reply_event = False
        self.change_time_event = False
        
    def run(self):
        # Prompt Event waits for a certain amount of time
        self.prompt_event.wait(timeout=self.prompt_time)
        
    @exception_handler
    def reset_timer(self):
        self.prompt_event = Event.set()
        
    @exception_handler
    def change_prompt_time(self, time:int):
        self.prompt_time = time
        
    
        
    