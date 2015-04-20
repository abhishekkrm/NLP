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
    
    ''' Give a chane to the questions processor to write it's answer type classifications/query keywords to a file
        Implementations using slow classifiers may want to use this opportunity to write their classifications once
        and may reuse them for subsequent runs.
        It is not an abstract method and hence its implementation is optional
    '''
    def DumpInfo(self):
        pass
    