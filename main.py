import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from config import LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN
from core import nickname_handler, user_state, error_handler
from ai.ai_client import get_ai_response
from services import diary_logger, mote_trainer, compliment_engine, notifier, weather_advisor, topic_provider

app = Flask(__name__)

# LINE API設定
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_message = event.message.text

    mode = user_state.get_mode(user_id)

    # モードに応じた処理
    if user_message.endswith("って呼んで") or user_message.startswith("名前教えて"):
        response = nickname_handler.handle_nickname_command(user_id, user_message)
    elif mode == 'diary':
        response = diary_logger.log_diary(user_id, user_message)
    elif mode == 'mote_check':
        answers = {"1": user_message}  # 実際は回答形式に合わせる必要あり
        response = mote_trainer.perform_mote_check(user_id, answers)
    elif mode == 'training':
        points = 80  # 実際のスコア計算を実装
        response = f"訓練結果: {points}点獲得！🎯"
        user_state.set_mode(user_id, 'normal')
    elif mode == 'consult':
        response = get_ai_response(user_message, user_id=user_id)
    elif user_message == "天気教えて":
        response = weather_advisor.get_weather_advice()
    elif user_message == "今日は何の日":
        response = topic_provider.get_today_topic()
    else:
        # 通常モード（AIと自然な会話）
        ai_reply = get_ai_response(user_message, user_id=user_id)
        response = compliment_engine.inject_compliment(ai_reply)

    # 応答を送信
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
