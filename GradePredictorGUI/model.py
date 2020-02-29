class Model:
    def __init__( self ):
        '''
        Initializes the two members the class holds:
        the file name and its contents.
        '''
        self.trainFileName = None
        self.testFileName = None
        self.subjectName = None

    def isValid( self, fileName ):
        '''
        returns True if the file exists and can be
        opened.  Returns False otherwise.
        '''
        try: 
            file = open( fileName, 'r' )
            file.close()
            return True
        except:
            return False

    def setTrainFileName( self, fileName ):
        '''
        sets the member fileName to the value of the argument
        if the file exists.  Otherwise resets both the filename
        and file contents members.
        '''
        if self.isValid( fileName ):
            self.trainFileName = fileName

        else:
            self.trainFileName = ""
            
    def getTrainFileName( self ):
        '''
        Returns the name of the file name member.
        '''
        return self.trainFileName

    def setTestFileName( self, fileName ):
        '''
        sets the member fileName to the value of the argument
        if the file exists.  Otherwise resets both the filename
        and file contents members.
        '''
        if self.isValid( fileName ):
            self.testFileName = fileName
        else:
            self.testFileName = ""
            
    def getTestFileName( self ):
        '''
        Returns the name of the file name member.
        '''
        return self.testFileName

    def setSubjectName( self, fileName ):
            self.subjectName = fileName

    def getSubjectName( self ):
        return self.subjectName
