import re
import random

class DialogueModule:

    def __init__(self):
        self.patterns = {
            r"(.*)โง่":["กุว่าไม่โง่อ่ะ ควายเลยแหละ",
                        "เห็นด้วย โง่สัสๆ"],
            r"(ประยุทธ์|ตู่|ลุง)":["{bw}มาก",
                      "{bw} {bw}และ{bw}ที่สุดในโลกต้องยกให้ลุง",
                      "เอาจริงๆนะ ใครมันจะทั้ง{bw}และ{bw}เท่าลุงวะ ถามจริง",
                      "อยากได้คนดีมาคุยกับฉัน อยากได้คน{bw}ไปคุยกับลุง",
                      "จะบอกว่า{bw}ก็ดูสุภาพไป ใช้คำว่าชั่วช้าดีกว่า",
                      "เมื่อวานเดินเจอเด็กประถมนั่งท่องลุง{bw}ราวๆ10ครั้ง",
                      "กุเคารพลุงมาก เคารพในความ{bw}ของมัน",
                      "เดินเจอลุงฝากตบด้วย",
                      "{bw}",
                      "สงสัยทานอสไม่นับญาติ เลยต้องมาบริหารประเทศ"],
            r"(รัฐบาล)":["พวกลุงทั้งนั้น"],
            r"(สลิ่ม)":["เดี๋ยวก็ตายกันหมด"]
            }
        
        self.badwords = ['เหี้ย','ส้นตีน','ทุเรศ','ไร้ยางอาย','โง่','ปญอ','ควาย',
                         'หน้าด้าน','ขยะ','กระจอก','หน้าเหลี่ยม','โกง','ชั่ว','เลว','ทราม',
                         'บัฟฟาโล่','งี่เง่า','กะลา','สลิ่ม','เฮงซวย']
        pass

    def converse(self,txt):
        for pattern,replyList in self.patterns.items():
            objs = re.search(pattern,txt)
            if objs is not None:
                reply = random.choice(replyList)
                while('bw' in reply):
                    reply = reply.replace('{bw}',random.choice(self.badwords),1)
                return reply
            else:
                continue

"""
dm = DialogueModule()
while True:
    print('CodeK:', dm.converse(input('Text: ')))
"""
