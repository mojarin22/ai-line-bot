from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import openai

app = Flask(__name__)

# 環境変数から取得
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return "AIアイbot 動いてるよ！"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    # OpenAI への問い合わせ
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # または gpt-4
            messages=[
                {"role": "system", "content": "あなたは面倒見の良い27歳の女性型AIです。優しく、でも時にズバッとアドバイスします。"},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"エラーが発生しました: {e}"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
