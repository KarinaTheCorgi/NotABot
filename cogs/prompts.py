"""
File: cogs.commands.py
Authors: 
    - Karina Solis
    - Asher Adighije
     
Resources:
   - Tasks
        - https://discordpy.readthedocs.io/en/stable/ext/tasks/index.html
   - Prompt Templates
        - ChatGPT
"""

# this will handle the initial prompts (triggered by no reply in [prompt_time] secs)
from discord.ext import tasks, commands

from cogs.command_handling import settings_db as db
from cogs.command_handling.commands import Topic

import random



class Prompts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prompt_users.start()

def generate_prompt(topic: Topic) -> str:
    templates = {
        Topic.relationships: [
            "How should I deal with a {relationship_issue} in my {relationship_type}?",
            "What are some tips for maintaining a healthy {relationship_type}?",
            "How do I know if my {relationship_type} is {relationship_status}?"
        ],
        Topic.lifestyle: [
            "What are some good habits for improving my {lifestyle_aspect}?",
            "How can I balance my {lifestyle_element} with my daily responsibilities?",
            "Is it important to include {lifestyle_habit} in my routine?"
        ],
        Topic.career: [
            "What’s the best way to handle {career_situation} at work?",
            "How do I transition from {career_stage_1} to {career_stage_2}?",
            "What are some underrated skills for succeeding in a {career_field} career?"
        ]
    }

    # Word banks
    word_bank = {
        "relationship_issue": ["lack of communication", "jealousy", "long-distance challenges"],
        "relationship_type": ["friendship", "romantic relationship", "family dynamic"],
        "relationship_status": ["toxic", "healthy", "worth continuing"],

        "lifestyle_aspect": ["mental health", "physical fitness", "daily energy"],
        "lifestyle_element": ["work-life balance", "social life", "me time"],
        "lifestyle_habit": ["journaling", "daily walks", "meal prepping"],

        "career_situation": ["a difficult boss", "burnout", "being overlooked for promotion"],
        "career_stage_1": ["entry-level job", "freelancer", "internship"],
        "career_stage_2": ["management role", "full-time position", "remote career"],
        "career_field": ["tech", "creative", "corporate"]
    }

    template = random.choice(templates[topic])
    prompt = template.format(**{key: random.choice(val) for key, val in word_bank.items()})
    return prompt
        
    @tasks.loop(seconds=60)  # unsure how to change to individual prompt times
    async def prompt_users(self):
        # get users from the DB
        users = db.get_all_users()  
        for user_id in users:
            topics = db.get_topics(user_id)
            
            topic = random.choice(topics)

            prompt = generate_prompt(topic)
            user = await self.bot.fetch_user(user_id)
            await user.send(prompt)
            
    @prompt_users.before_loop
    async def before_prompting(self):
        await self.bot.wait_until_ready()