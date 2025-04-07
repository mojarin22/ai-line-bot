import json
import os
from datetime import datetime

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "topics.json")

def get_today_topic():
    today = datetime.now().strftime("%m-%d")
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as file:
        topics = json.load(file)

    for item in topics:
        if item['date'] == today:
            return f"📅 {item['topic']}"

    return "今日は特に記念日はないようです。でも毎日が特別な日ですね！✨"
