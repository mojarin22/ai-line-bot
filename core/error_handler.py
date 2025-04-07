import logging
import os
from datetime import datetime

# エラーログの設定
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, 'error.log')

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.ERROR,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# エラーを記録する関数
def log_error(error_msg, user_id=None):
    user_info = f"ユーザーID: {user_id} - " if user_id else ""
    full_message = f"{user_info}{error_msg}"
    logging.error(full_message)

# ユーザー向けエラーメッセージ生成関数
def friendly_error_message():
    return "ごめんなさい、少し調子が悪いみたいです😥 もう一度試してみてください。"

# エラー処理デコレーター（任意の関数を安全に実行）
def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = f"{func.__name__} でエラー: {e}"
            user_id = kwargs.get('user_id') if 'user_id' in kwargs else None
            log_error(error_msg, user_id)
            return friendly_error_message()
    return wrapper
