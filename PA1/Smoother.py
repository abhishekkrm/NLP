import abc

class ISmoother(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def calculate_probability(self, counts, N, word_sequence):
        pass
    
class LaplaceSmoother(ISmoother):
    def __init__(self, delta = 1):
        self.__delta = delta
        
    def calculate_probability(self, counts, N, word_sequence):
        history = ' '.join(word_sequence.split()[0:N-1])
        size_of_vocab = len(counts[1])
        num_tokens = sum(counts[1].values())
        
        numerator = counts[N].get(word_sequence, 0) + self.__delta
        denominator = counts.get(N-1, {'':num_tokens}).get(history,0) + size_of_vocab * self.__delta
        
        return numerator/denominator
    