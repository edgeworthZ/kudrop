import re
import random

class DialogueModule:

    def __init__(self):
        self.patterns = { }
        
        self.badwords = []
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
