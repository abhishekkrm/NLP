import abc
from abc import ABCMeta

class IAnswerProcessor(metaclass=ABCMeta):
    ''' Given a list of relevent passages and their corresponding scores, returns a list of N possible answers in ranked order.
    '''
    @abc.abstractmethod
    def GetAnswers(self, question, relevent_passages_and_scores, num_answers=10):
        pass
    