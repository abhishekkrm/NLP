from abc import ABCMeta

class IPassageRetriever(metaclass=ABCMeta):
    
    ''' From the list of top documents figures out the relevent passages
    '''
    def GetRelatedPassages(self, question):
        pass