import os
from dotenv import load_dotenv

load_dotenv()

CHANNEL_ID = "2007205792"
EMAIL_ADDRESS = "pretty.moja.orz@gmail.com"
LINE_DISPLAY_NAME = '非モテ専用AI『アイ』'
WEBHOOK_URL = "https://ai-line-bot-e03n.onrender.com/callback"

# 環境変数を取得
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
