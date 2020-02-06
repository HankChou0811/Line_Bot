from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('75ig+9z5XZBIoVswZOTcVbVsPnPZZHyXTHn9ip01PlsHNqqTtPLN5WYufEhCeRNl/GO2pebKwY6dX0lrHpU5fKW1l587Pq2WUtFgRt5gYwsa2OfQ/8VDoOFUy+C4cqO7W3VAH3laTgD/klOuQm8yAgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('08f188eefc874688a91cec3d5d8bf52c')

#接收訊息的程式碼
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()