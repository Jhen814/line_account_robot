from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os

app = Flask(__name__)
line_bot_api = LineBotApi('rjv3sSjGeNdc/cN4zLt7QWtSP8X8Ppvcv2lgHrJPY0Donyas6EzSJWA9j4NBEPqpbjUWDNE4peUB+SdA1LbP/6VnXGKoWjwlOGrZEkMLGsH&nwC1LbP/6VnXGKoWjwlOGrZEkMLGsHZawfVzA dB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('434ec9714a51ddb8f18572370c77de99')

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = event.message.text
    reply_message = f"You said: {message_text}"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
