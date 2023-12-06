from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['k2AtHDI4AjqxtsrSWi7XQo8DxyoW1hTouwAT/jbr4V2eLhDfuupdhnLIMquEcRyj7QJmzuhZPn8Mp47ekKrc2xjPu0c/HDcZ1gLifkhUE+KMe1s336766036030503076760303ifkhUE+Kx724x56/202050505050505050000 89/1O/w1cDnyilFU='])
handler = WebhookHandler(os.environ['50a34fb97a7d83a7ff7c2fe8de732c19'])


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
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    app.run()
