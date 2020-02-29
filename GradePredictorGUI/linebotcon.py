# This code gets results from regression module and broadcast them to line users

from linebot import (LineBotApi, WebhookHandler)
from linebot.models import (
 MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
 SourceUser, SourceGroup, SourceRoom,
 TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
 ButtonsTemplate, URITemplateAction, PostbackTemplateAction,
 CarouselTemplate, CarouselColumn, PostbackEvent,
 StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
 ImageMessage, VideoMessage, AudioMessage,
 UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)
from linebot.models import (
    RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, 
    URIAction, PostbackAction, MessageAction
    )

class LineBotCon:
    def __init__(self):
        self.line_bot_api = LineBotApi('i1sVJnx19N2uqelufDprbHySs8hdPYnDtgP1NeFpd3fwMjmdSPSqzwh86wXPpxUCGiRSucjpnxaOIfV3Otcd662kXscktrKxOg9oJR7StLm+4d91oYVoWJrfHlSsXJtvOkbhiez8Jy5vRALD0QsC8QdB04t89/1O/w1cDnyilFU=') #Your Channel Access Token

    def reportScore(self,userID,userName,subject,score,grade):
        #line_bot_api.push_message(userid, [TextSendMessage(text='หวัดดี อีดอก555'),])
        print(userID+' คะแนนของคุณ '+userName+' วิชา '+subject+' คือ '+score)
        if grade != 'P':
            print('คุณมีแนวโน้มว่าเกรดจะติด F สูง ควรดรอปทันที')
        else:
            print('คุณมีโอกาสผ่านวิชานี้สูง ไม่จำเป็นต้องดรอป')
            
        """
        self.line_bot_api.push_message(userID,
                                  [TextSendMessage(text='คะแนนของคุณ '+userName+' วิชา '+subject+' คือ '+score),])
        if grade != 'P':
            self.line_bot_api.push_message(userID,
                                      [TextSendMessage(text='คุณมีแนวโน้มว่าเกรดจะติด F สูง ควรดรอปทันที'),])
        else:
            self.line_bot_api.push_message(userID,
                                      [TextSendMessage(text='คุณมีโอกาสผ่านวิชานี้สูง ไม่จำเป็นต้องดรอป'),])"""
            
# Send message to all users
#line_bot_api.broadcast(TextSendMessage(text=regression.get_result()))

# Send message to specific user, using user_id
#userid = 'U3a1be706d82cdfdeb5521e2639d8ced1'
#line_bot_api.push_message(userid, [TextSendMessage(text='หวัดดี อีดอก555'),])
# Send image to all users
"""image_message = ImageSendMessage(
    original_content_url='https://avatars2.githubusercontent.com/u/13128444?s=400&v=4',
    preview_image_url='https://avatars2.githubusercontent.com/u/13128444?s=400&v=4'
)
line_bot_api.broadcast(image_message)"""

"""
test = LineBotCon()
test.reportScore('U3a1be706d82cdfdeb5521e2639d8ced1','Art','01111333','30','P')
"""
