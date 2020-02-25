# encoding: utf-8
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

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage)

# use creds to create a client to interact with the Google Drive API
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("KUDrop").sheet1

app = Flask(__name__)

line_bot_api = LineBotApi('i1sVJnx19N2uqelufDprbHySs8hdPYnDtgP1NeFpd3fwMjmdSPSqzwh86wXPpxUCGiRSucjpnxaOIfV3Otcd662kXscktrKxOg9oJR7StLm+4d91oYVoWJrfHlSsXJtvOkbhiez8Jy5vRALD0QsC8QdB04t89/1O/w1cDnyilFU=') #Your Channel Access Token
handler = WebhookHandler('6d8a30ddb7073299e39424a40037c50d') #Your Channel Secret

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
def handle_text_message(event):
    text = event.message.text #message from user

    if all(i.isdigit() for i in text) and len(text) == 10: # Input student id
        profile = line_bot_api.get_profile(event.source.user_id)
        """x = sheet.row_count
        while x > 0:
           row = sheet.row_values(x, value_render_option='UNFORMATTED_VALUE')                    
           if row[0] == event.source.user_id: #replace name by the desired keyword
              row[3] = text
              break
           x = x - 1"""
        
        cell = worksheet.find(event.source.user_id)
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='พบข้อมูลที่'+cell.row+cell.col+'เชื่อมต่อ Line กับ รหัสนิสิตสำเร็จ นอนรอดรอปได้เลย'))
    else:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='พิมพ์ห่าไร กุอ่านลายมือมึงไม่ออก'))

@handler.add(FollowEvent)
def handle_follow(event):
    #app.logger.info("Got Follow event:" + event.source.user_id)
    profile = line_bot_api.get_profile(event.source.user_id)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='ขอบคุณที่แอด กุเก็บข้อมูลทุกอย่างของมึงเข้าเซิร์ฟเรียบร้อย555555'))
    row = [profile.user_id,profile.display_name,profile.picture_url]
    sheet.append_row(row)

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
