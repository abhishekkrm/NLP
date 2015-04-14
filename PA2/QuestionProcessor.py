from abc import ABCMeta

class IQuestionProcessor(metaclass=ABCMeta):
    
    ''' Given a question find out the important keywords in it.
        return a list of keywords
    '''
    def GetQueryKeywords(self, raw_question_text):
        pass
    
    ''' Given a question find out what answer type it expects (eg. PERSON, CITY ?)
        return a list of answer types (in rank order possibly ??)
    '''
    def GetAnswerType(self, raw_question_text):
        pass
    