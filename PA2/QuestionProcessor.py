import abc
from abc import ABCMeta

class IQuestionProcessor(metaclass=ABCMeta):
    
    ''' Given a question find out the important keywords in it.
        return a list of keywords
    '''
    @abc.abstractmethod
    def GetQueryKeywords(self, question):
        pass
    
    ''' Given a question find out what answer type it expects (eg. PERSON, CITY ?)
        return a list of answer types (in rank order possibly ??)
    '''
    @abc.abstractmethod
    def GetAnswerType(self, question):
        pass
    