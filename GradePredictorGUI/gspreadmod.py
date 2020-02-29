# use creds to create a client to interact with the Google Drive API
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
import ast

class GSpreadMod:
    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)
        self.sheet = client.open("KUDrop").sheet1
        self.logSheet = client.open("KUDrop").worksheet("Log")

    def updateScore(self, dataFrame, subjectName):
        Score = {'01204111': {'Score': 0, 'Grade': 'P'},
                 '01355744': {'Score': 4, 'Grade': 'F'},
                 '01444328': {'Score': 0, 'Grade': 'P'} }
        df = pd.DataFrame(Score)
        """df = df.rename(columns={'Student1': 'Good',
                                'Student2': 'Medium',
                                'Student3': 'Bad'})"""
        
        for index, row in dataFrame.iterrows():
            try:
                #print(row['Name'], row['Grade'])
                #cell = self.sheet.find(str(row['Name']))
                cell = self.sheet.find(str(row['Name']))
                if self.sheet.cell(cell.row, cell.col+1).value:
                    rawNewFrame = self.sheet.cell(cell.row, cell.col+1).value
                    newFrame = ast.literal_eval(rawNewFrame)
                    newFrame[subjectName] = {'Score':str(row['MidTerm']),'Grade':row['Grade']}
                    self.sheet.update_cell(cell.row,cell.col+1, str(newFrame))
                else:
                    newFrame = {subjectName:{'Score':str(row['MidTerm']),'Grade':row['Grade']}}
                    self.sheet.update_cell(cell.row,cell.col+1, str(newFrame))
                    
            except:
                continue

    def getUserName(self, userID):
        try:
            cell = self.sheet.find(userID)
            name = self.sheet.cell(cell.row, cell.col+2).value
            return name
        except:
            return None

    def getUserIDFromStudentID(self, studentID):
        try:
            cell = self.sheet.find(studentID)
            userID = self.sheet.cell(cell.row, cell.col-3).value
            return userID
        except:
            return None

    def test(self):
        try:
            cell = self.sheet.find('6210503659')
            self.sheet.update_cell(cell.row,cell.col+2, 'P')
            print('F')
        except:
            print('FFF')
"""
g = GSpreadMod()
Score = {'01204111': {'Score': 0, 'Grade': 'P'},
                 '01355744': {'Score': 4, 'Grade': 'F'},
                 '01444328': {'Score': 0, 'Grade': 'P'} }
df = pd.DataFrame(Score)
g.updateScore(df,'AAA')
"""


