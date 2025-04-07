import openai
from core.error_handler import log_error, friendly_error_message
from .prompt_builder import build_prompt
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

# OpenAI API呼び出しラッパー
def get_ai_response(user_message, conversation_history=None, user_id=None):
    try:
        messages = build_prompt(user_message, conversation_history)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        log_error(f"AI APIエラー: {e}", user_id)
        return friendly_error_message()
