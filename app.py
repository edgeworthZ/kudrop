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
logSheet = client.open("KUDrop").worksheet("Log")

dialogues = ['หน้าหี','ประยุทธ์หัวควย','ประยวยหัวคุด']

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
    
    # users' reply log
    profile = line_bot_api.get_profile(event.source.user_id)
    row = [profile.user_id,profile.display_name,text]
    logSheet.append_row(row)

    if all(i.isdigit() for i in text) and len(text) == 10: # Input student id
        cell = sheet.find(event.source.user_id)
        sheet.update_cell(cell.row,cell.col+3, text) # รหัสนิสิตอยู่คอลัมน์ที่ 3 ใน google sheet
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='เชื่อมต่อ Line ของคุณ'+profile.display_name+' กับรหัสนิสิตสำเร็จ นอนรอดรอปได้เลย'))
    elif 'เขียนแบบเป็นไง' in text:
        line_bot_api.broadcast(TextSendMessage(text='เขียนแบบแม่งมึนสัสๆ'))
    elif 'คะแนน' in text:
        cell = sheet.find(event.source.user_id)
        nickname = sheet.cell(cell.row, cell.col+2).value
        displayName = nickname if len(nickname) > 0 else profile.display_name
        score = sheet.cell(cell.row, cell.col+4).value
        regVal = int(sheet.cell(cell.row, cell.col+5).value)
        if regVal != 1:
            line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text='กากสัสไอ้คุณ'+displayName+' เขียนแบบมึงได้'+score+'คะแนนเอง ไปดรอปเหอะ'))
            url = 'https://www.thairath.co.th/media/HCtHFA7ele6Q2dULkStXvrq4Q8ntVDjDlDSWvVNtzOMMr0257UircvOLeoaRlH4IFx.jpg'
            app.logger.info("url=" + url)
            line_bot_api.push_message(event.source.user_id, [ImageSendMessage(url, url),])
        else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='เขียนแบบมึงได้'+score+'คะแนน ก็ใช้ได้อยู่'))
            url = 'https://thestandard.co/wp-content/uploads/2019/03/%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%A2%E0%B8%B8%E0%B8%97%E0%B8%98%E0%B9%8C-%E0%B8%88%E0%B8%B1%E0%B8%99%E0%B8%97%E0%B8%A3%E0%B9%8C%E0%B9%82%E0%B8%AD%E0%B8%8A%E0%B8%B2-.jpg'
            app.logger.info("url=" + url)
            line_bot_api.push_message(event.source.user_id, [ImageSendMessage(url, url),])
    else:
        msg = dialogues[len(text)%len(dialogues)]
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))

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
