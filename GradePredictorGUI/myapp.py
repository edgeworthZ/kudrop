import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot
from mainwindow import Ui_MainWindow
from model import Model
from logisreg import LogisReg
from gspreadmod import GSpreadMod
from linebotcon import LineBotCon
import pandas as pd
import numpy as np

class MainWindowUIClass( Ui_MainWindow ):
    def __init__( self ):
        '''Initialize the super class
        '''
        super().__init__()
        self.model = Model()
        self.logisreg = LogisReg()
        self.gspreadmod = GSpreadMod()
        self.linebotcon = LineBotCon()
        
    def setupUi( self, MW ):
        ''' Setup the UI of the super class, and add here code
        that relates to the way we want our UI to operate.
        '''
        super().setupUi( MW )

        # close the lower part of the splitter to hide the 
        # debug window under normal operations
        #self.splitter.setSizes([300, 0])

    def debugPrint( self, msg ):
        '''Print the message in the text edit at the bottom of the
        horizontal splitter.
        '''
        self.debugTextBrowser.append( msg )

    def refreshAll( self ):
        '''
        Updates the widgets whenever an interaction happens.
        Typically some interaction takes place, the UI responds,
        and informs the model of the change.  Then this method
        is called, pulling from the model information that is
        updated in the GUI.
        '''
        self.lineEdit.setText( self.model.getTrainFileName() )
        self.lineEdit_4.setText( self.model.getTestFileName() )
        #self.textBrowser.setText( self.model.getFileContents() )

    # slot
    def trainReturnPressedSlot( self ):
        ''' Called when the user enters a string in the line edit and
        presses the ENTER key.
        '''
        fileName =  self.lineEdit.text()
        if self.model.isValid( fileName ):
            self.debugPrint( "setting file name: " + fileName )
            self.model.setFileName( self.lineEdit.text() )
            self.refreshAll()
        else:
            m = QtWidgets.QMessageBox()
            m.setText("Invalid file name!\n" + fileName )
            m.setIcon(QtWidgets.QMessageBox.Warning)
            m.setStandardButtons(QtWidgets.QMessageBox.Ok
                                 | QtWidgets.QMessageBox.Cancel)
            m.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            ret = m.exec_()
            self.lineEdit.setText( "" )
            self.refreshAll()
            self.debugPrint( "Invalid file specified: " + fileName  )
        
    # slot
    def trainBrowseSlot( self ):
        ''' Called when the user presses the Browse button
        '''
        #self.debugPrint( "Browse button pressed" )
        options = QtWidgets.QFileDialog.Options()
        #options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                        None,
                        "QFileDialog.getOpenFileName()",
                        "",
                        "Comma-separated values (*.csv);;All Files (*)",
                        options=options)
        if fileName:
            self.debugPrint( "setting train file name: " + fileName )
            self.model.setTrainFileName( fileName )
            self.logisreg.setTrainFile(fileName)
            auc = self.logisreg.analyzeTrainData()
            self.lineEdit_3.setText(str(auc))
            self.pushButton_4.setEnabled(True)
            self.lineEdit_4.setEnabled(True)
            self.refreshAll()

    # slot
    def testBrowseSlot( self ):
        ''' Called when the user presses the Browse button
        '''
        #self.debugPrint( "Browse button pressed" )
        options = QtWidgets.QFileDialog.Options()
        #options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                        None,
                        "QFileDialog.getOpenFileName()",
                        "",
                        "Comma-separated values (*.csv);;All Files (*)",
                        options=options)
        if fileName:
            self.debugPrint( "setting test file name: " + fileName )
            self.model.setTestFileName( fileName )
            self.model.setSubjectName(fileName.split('/')[-1].split('.')[0])
            self.debugPrint( "Found subject: " + self.model.getSubjectName())
            self.logisreg.setTestFile(fileName)
            self.debugPrint( "analyzing: " + fileName )
            self.logisreg.analyzeTestData()
            res = self.logisreg.getTestAnalyzeResult()
            self.textBrowser.setText(res)
            self.pushButton_5.setEnabled(True)
            self.pushButton_6.setEnabled(True)
            self.refreshAll()

    # slot
    def exportCSVSlot( self ):
        ''' Called when the user presses the Export CSV button.'''
        #self.debugPrint( "Browse button pressed" )
        options = QtWidgets.QFileDialog.Options()
        #options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
                        None,
                        "QFileDialog.getSaveFileName()",
                        "",
                        "Comma-separated values (*.csv);;All Files (*)",
                        options=options)
        if fileName:
            self.debugPrint( "exporting analyzed data: " + fileName )
            res = self.logisreg.export2CSV(fileName)
            self.debugPrint( "Successfully exported: " + fileName )
            self.refreshAll()

    # slot
    def exportDatabaseSlot(self):
        self.gspreadmod.updateScore(self.logisreg.getSubmission(), self.model.getSubjectName())
        self.pushButton_7.setEnabled(True)

    # slot
    def broadcastSlot( self ):
        """userIDslist = self.gspreadmod.sheet.col_values(1)
        scoreslist  = self.gspreadmod.sheet.col_values(5)
        gradeslist = self.gspreadmod.sheet.col_values(6)
        for i in range(1,len(userIDslist)):
            #print(userIDslist[i],scoreslist[i],gradeslist[i])
            self.linebotcon.reportScore(userIDslist[i],self.gspreadmod.getUserName(userIDslist[i]),
                                        self.model.getSubjectName(),scoreslist[i],gradeslist[i])"""
        dataFrame = self.logisreg.getSubmission()
        for index, row in dataFrame.iterrows():
            #print(row['Name'], row['Grade'])
            try:
                userID = self.gspreadmod.getUserIDFromStudentID(str(row['Name']))
                userName = self.gspreadmod.getUserName(userID)
                subject = self.model.getSubjectName()
                self.linebotcon.reportScore(userID,userName,subject,str(row['MidTerm']),row['Grade'])
            except:
                continue

def main():
    """
    This is the MAIN ENTRY POINT of our application.  The code at the end
    of the mainwindow.py script will not be executed, since this script is now
    our main program.   We have simply copied the code from mainwindow.py here
    since it was automatically generated by '''pyuic5'''.

    """
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowUIClass()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

main()
