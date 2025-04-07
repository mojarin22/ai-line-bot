from flask import Flask, request, abort
from linebot.v3.webhook import WebhookHandler, MessageEvent
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import TextMessageContent
import os
from datetime import datetime

from core.db_manager import init_db
from core.user_state import get_user_state, set_user_state
from services.compliment_engine import get_random_compliment
from services.diary_logger import log_diary_entry
from services.mote_trainer import handle_mote_mode
from services.notifier import check_and_send_reminder
from services.topic_provider import get_today_topic
from services.trainer_mode import handle_training_mode
from services.weather_advisor import get_weather_advice
from core.nickname_handler import get_nickname, set_nickname_from_message

app = Flask(__name__)

# 環境変数からLINEのトークンとシークレットを取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

# LINE SDK 設定
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# DB初期化
init_db()

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# リッチメニューによるモード切り替え用キーワード（※リッチメニューのボタンと一致させる）
mode_keywords = {
    "🔍モテ診断": "mote",
    "📘日記を書く": "diary",
    "🔥訓練モード": "train",
    "💬雑談する": "default"
}

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_id = event.source.user_id
    user_message = event.message.text.strip()
    reply_token = event.reply_token

    # ユーザーの状態を取得または初期化
    state = get_user_state(user_id)

    # 呼び名変更メッセージが含まれていたら処理
    if "って呼んで" in user_message:
        reply_text = set_nickname_from_message(user_id, user_message)
    elif user_message in mode_keywords:
        new_mode = mode_keywords[user_message]
        set_user_state(user_id, mode=new_mode)
        reply_text = f"🛠 モードを『{user_message}』に切り替えました！ご希望の内容を入力してね。"
    else:
        nickname, honorific = get_nickname(user_id)
        name_display = f"{nickname}{honorific}" if nickname else "あなた"

        hour = datetime.now().hour
        if hour < 11:
            greeting = "おはよう☀️"
        elif hour < 18:
            greeting = "こんにちは☀️"
        else:
            greeting = "こんばんは🌙"

        if state.get("mode") == "mote":
            reply_text = handle_mote_mode(user_id, user_message)
        elif state.get("mode") == "train":
            reply_text = handle_training_mode(user_id, user_message)
        elif state.get("mode") == "diary":
            log_diary_entry(user_id, user_message)
            reply_text = f"{greeting} {name_display}の日記を記録したよ✍️"
        else:
            compliment = get_random_compliment()
            weather_tip = get_weather_advice(user_id)
            topic = get_today_topic()
            reply_text = f"{greeting} {name_display}、{compliment}\n\n💡今日の話題: {topic}\n☁️天気アドバイス: {weather_tip}\n\nあなたのメッセージ: {user_message}"

        set_user_state(user_id, last_message=user_message)
        check_and_send_reminder(user_id)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=[TextMessage(text=reply_text)]
            )
        )

if __name__ == "__main__":
    app.run(debug=True)
