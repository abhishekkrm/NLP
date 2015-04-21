import abc
from abc import ABCMeta

class IAnswerProcessor(metaclass=ABCMeta):
    ''' Given a list of relevent passages, returns a list of N possible answers in ranked order.
    '''
    @abc.abstractmethod
    def GetAnswers(self, question, relevent_passages, num_answers=10):
        pass
    