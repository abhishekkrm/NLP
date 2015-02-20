import abc

class ISmoother(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def calculate_probability(self, model, word_sequence):
        pass
    
class LaplaceSmoother(ISmoother):
    def __init__(self, delta = 1):
        self.__delta = delta
        
    def calculate_probability(self, model, word_sequence):
        N = model.get_n()
        history = ' '.join(word_sequence.split()[0:N-1])
        size_of_vocab = model.get_vocab_size()
        num_tokens = model.get_num_tokens()
        
        numerator = model.get_counts()[N].get(word_sequence, 0) + self.__delta
        denominator = model.get_counts().get(N-1, {'':num_tokens}).get(history,0) + size_of_vocab * self.__delta
        
        return numerator/denominator
    