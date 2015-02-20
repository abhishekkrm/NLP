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

class BackoffSmoother(ISmoother):
    def __init__(self, D = 0.5,delta=1):
        self.__D = D
        self.__delta=delta

    def calculate_probability(self, counts, N, word_sequence):

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
            return (counts[N].get(word_sequence)-self.__D)/(counts[N-1].get(history)
        else:
            history2=' '.join(history.split()[1:N-1])
            Wi=word_sequence.split()[N]
            Pkatz=calculate_probability(counts,N-1,history2+' '+Wi)
            # Compute alpha
            numerator=self.__D
            denominator=0

            for unigram in counts[1]:
                s=history+' '+unigram
                if s not in counts[N]:
                	denominator+=calculate_probability(counts,N-1,history2+' '+unigram)
            return numerator/denominator
            
    
