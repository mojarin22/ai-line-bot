import json
import os
import random

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "compliments.json")

def get_compliment():
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as file:
        compliments = json.load(file)
    return random.choice(compliments)

# 会話に褒め言葉を自然に挿入する
def inject_compliment(message):
    compliment = get_compliment()
    return f"{message}\n\n{compliment}✨"
