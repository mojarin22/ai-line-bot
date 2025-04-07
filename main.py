from flask import Flask, request, abort
import os

from linebot.v3.messaging import (
    MessagingApi,
    Configuration,
    ApiClient,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhook import (
    WebhookHandler,
    WebhookParser,
    MessageEvent,
    TextMessageContent
)

from services import (
    diary_logger,
    mote_trainer,
    compliment_engine,
    notifier,
    weather_advisor,
    topic_provider
)

from dotenv import load_dotenv
load_dotenv()

# 環境変数からトークン類を取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

# LINE Bot SDK v3 用の設定
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
api_client = ApiClient(configuration)
line_bot_api = MessagingApi(api_client)
parser = WebhookParser(channel_secret=LINE_CHANNEL_SECRET)

# Flask アプリ作成
app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーとボディの取得
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)

    try:
        # イベントをパース
        events = parser.parse(body, signature)
    except Exception as e:
        print(f"❌ Webhook parsing failed: {e}")
        abort(400)

    for event in events:
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessageContent):
            user_id = event.source.user_id
            message_text = event.message.text

            # 応答メッセージの生成（ここにモード分岐ロジックを追加可能）
            reply_text = f"こんにちは！メッセージありがとうございます😊\n「{message_text}」を受け取りました。"

            # メッセージを返信
            try:
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=reply_text)]
                    )
                )
            except Exception as e:
                print(f"❌ メッセージ送信エラー: {e}")

    return 'OK'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
