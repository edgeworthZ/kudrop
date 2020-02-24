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
import os

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["i1sVJnx19N2uqelufDprbHySs8hdPYnDtgP1NeFpd3fwMjmdSPSqzwh86wXPpxUCGiRSucjpnxaOIfV3Otcd662kXscktrKxOg9oJR7StLm+4d91oYVoWJrfHlSsXJtvOkbhiez8Jy5vRALD0QsC8QdB04t89/1O/w1cDnyilFU="]
YOUR_CHANNEL_SECRET = os.environ["6d8a30ddb7073299e39424a40037c50d"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="hello this is me"))
#Change the argument for text in TextSendMessage
#to reply to the user.


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
