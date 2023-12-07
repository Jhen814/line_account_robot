from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, MessageEvent, TextMessage
import os

app = Flask(__name__)

# LINE 聊天機器人的 Channel Access Token 和 Channel Secret
channel_access_token = 'kiI+91MdztqCamHqJThQd4wwBed5r9NG8DanO/bgr7Ruq3kjBZ5dOnGGBbOvo8fQ7QJmzuhZPn8Mp47ekKrc2xjPu0c/HDcZPMgLif+KVW47ekKrc2xjPu0c/HDcZPMgLif+K4Q94745700002545452L B04t89/1O/w1cDnyilFU='
channel_secret = '50a34fb97a7d83a7ff7c2fe8de732c19'

# 初始化 LineBotApi 和 WebhookHandler
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    # 取得 LINE 平台傳送的資訊
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    # 記錄傳送的資訊
    app.logger.info("Request body: " + body)

    try:
        # 驗證簽名
        handler.handle(body, signature)
    except InvalidSignatureError:
        # 簽名錯誤，回傳 400 錯誤
        abort(400)

    # 回傳 'OK' 表示成功接收並處理 LINE 平台的事件
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 收到文字訊息時的處理函式
    message_text = event.message.text
    reply_message = f"You said: {message_text}"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

if __name__ == "__main__":
    # 取得 Heroku 上的 PORT 環境變數，若不存在則使用預設值 5000
    port = int(os.environ.get('PORT', 5000))
    # 啟動 Flask 應用程式
    app.run(host='0.0.0.0', port=port)
