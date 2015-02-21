import abc

class ISmoother(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def calculate_probability(self, model, word_sequence):
        pass
    
    @abc.abstractmethod
    def handle_unknown_words(self):
        pass
    

class UnSmoother(ISmoother):
    def handle_unknown_words(self):
        return False
    
    def calculate_probability(self, model, word_sequence):
        N = model.get_n()
        history = ' '.join(word_sequence.split()[0:N-1])
        
        numerator = model.get_counts()[N].get(word_sequence, 0)
        denominator = model.get_counts().get(N-1, {'':model.get_num_tokens()}).get(history, 0)
        
        if numerator==0 or denominator ==0:
            return 0
        
        return numerator/denominator


class LaplaceSmoother(ISmoother):
    def __init__(self, delta = 1):
        self.__delta = delta
        
    def handle_unknown_words(self):
        return True
    
    def calculate_probability(self, model, word_sequence):
        N = model.get_n()
        history = ' '.join(word_sequence.split()[0:N-1])
        size_of_vocab = model.get_vocab_size()
        num_tokens = model.get_num_tokens()
        
        numerator = model.get_counts()[N].get(word_sequence, 0) + self.__delta
        denominator = model.get_counts().get(N-1, {'':num_tokens}).get(history,0) + size_of_vocab * self.__delta
        
        return numerator/denominator


class BackoffSmoother(ISmoother):
    def __init__(self, D = 0.5,delta=1):
        self.__D = D
        self.__delta=delta

    def handle_unknown_words(self):
        return True
    
    def calculate_probability(self, model, word_sequence):
        return self.__calculate_probability(model.get_counts(), model.get_n(), word_sequence)
    
    def __calculate_probability(self, counts, N, word_sequence):
        history = ' '.join(word_sequence.split()[0:N-1])
        size_of_vocab = len(counts[1])
        num_tokens = sum(counts[1].values())

        if N==1:
            # Laplace smoothing if N=1	
            numerator = counts[1].get(word_sequence, 0) + self.__delta
            denominator = num_tokens + size_of_vocab * self.__delta
            return numerator/denominator
        elif word_sequence in counts[N]:	
            # Discounted probability
            return (counts[N].get(word_sequence)-self.__D)/(counts[N-1].get(history))
        else:
            history2=' '.join(history.split()[1:N-1])
            Wi=word_sequence.split()[N-1]
            Pkatz = self.__calculate_probability(counts,N-1,history2+' '+Wi)
            # Compute alpha
            numerator=self.__D
            denominator=0

            for unigram in counts[1]:
                s=history+' '+unigram
                if s not in counts[N]:
                    denominator+=self.__calculate_probability(counts,N-1,history2+' '+unigram)
            alpha = numerator/denominator
            return Pkatz*alpha 
            
    
