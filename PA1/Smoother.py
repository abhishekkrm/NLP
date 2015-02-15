import abc

class ISmoother(metacalss=abc.ABCMeta):
    @abc.abstractmethod
    def calculate_probability(self, counts, N, word_sequence):
        pass
    
class LaplaceSmoother(ISmoother):
    def __init__(self, delta = 1):
        self.__delta = delta
        
    def calculate_probability(self, counts, N, word_sequence):
        pass
    