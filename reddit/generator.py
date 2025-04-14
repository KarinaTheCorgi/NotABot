# reddit/generator.py

import random

# Replace this with an actual LLM/OpenAI integration if needed
def get_reddit_style_response(topic: str) -> str:
    # Simulated Reddit-style response generation
    responses = {
        "relationships": [
            "I once dated someone who thought pineapple belonged on every food. Chaos.",
            "Communication is key, but sometimes silence is golden. 😉"
        ],
        "career": [
            "Your first job doesn’t define your career. Keep learning, keep grinding.",
            "Just wait until you get asked for 5 years experience in a junior role. Classic."
        ],
        "lifestyle": [
            "Minimalism saved me from drowning in junk. Highly recommend.",
            "Cold showers are life. Try it once and you'll either hate me or thank me."
        ]
    }
    
    

    default_response = "That's an interesting topic! Here's a quirky take on it: stay curious."
    return random.choice(responses.get(topic.lower(), [default_response]))
