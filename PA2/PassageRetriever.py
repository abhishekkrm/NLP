import abc
from abc import ABCMeta

class IPassageRetriever(metaclass=ABCMeta):
    
    ''' From the list of top documents figures out the the n most relevent passages
    '''
    @abc.abstractmethod
    def GetRelatedPassages(self, question, n = 10):
        
        pass
