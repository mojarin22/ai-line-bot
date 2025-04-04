from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from openai import OpenAI
import os

app = Flask(__name__)

# 環境変数から各種キーを取得
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
openai_api_key = os.getenv("OPENAI_API_KEY")

# OpenAIクライアント（v1.0.0以降対応）
client = OpenAI(api_key=openai_api_key)

# 動作確認用エンドポイント（Renderのトップページが 404 にならないように）
@app.route("/")
def index():
    return "AIアイは元気に動いています😊"

# LINEからのWebhookを受け取るエンドポイント
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

# メッセージイベントに反応
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    try:
        # OpenAIに問い合わせ（v1.0.0対応）
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは27歳の優しくて小悪魔的な女性型AI『アイ』です。質問者が非モテ男子であることを前提に、親しみやすく寄り添いながら返答してください。"},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content.strip()

    except Exception as e:
        reply = f"エラーが発生しました: {str(e)}"

    # LINEに返信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

# Renderで動かすためにホストとポートを指定
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
