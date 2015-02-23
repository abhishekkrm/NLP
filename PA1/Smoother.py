#ref http://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.lstsq.html
#ref http://en.wikipedia.org/wiki/Good%E2%80%93Turing_frequency_estimation
#ref https://github.com/maxbane/simplegoodturing/blob/master/sgt.py
#ref http://www.d.umn.edu/~tpederse/Courses/CS8761-FALL02/Code/sgt-gale.pdf

import abc
import math
import numpy as np

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


class GTSmoother(ISmoother):
    def __init__(self):
        self.__frequency_popluated = False
        self.__frequency_counts = {}
        self.__num_ngrams_in_model = 0
        
    def __populate_frequencies(self, model):
        self.__frequency_popluated = True
        ngrams_counts_dict = model.get_counts()[model.get_n()]
        for _, count in ngrams_counts_dict.items():
            self.__frequency_counts[count] = self.__frequency_counts.get(count, 0) + 1
            self.__num_ngrams_in_model += count
    
    def __get_adjusted_count(self, count):
        if count == 0:
            return self.__frequency_counts.get(1, 0)
        return (count + 1)*(self.__frequency_counts.get(count+1, 0)/self.__frequency_counts.get(count, 1))
    
    def handle_unknown_words(self):
        return True
    
    def calculate_probability(self, model, word_sequence):
        if self.__frequency_popluated == False:
            self.__populate_frequencies(model)
        count_of_word_sequence = model.get_counts()[model.get_n()].get(word_sequence, 0)
        return self.__get_adjusted_count(count_of_word_sequence)/self.__num_ngrams_in_model    
    

class SimpleGTSmoother(ISmoother):
    def __init__(self):
        self.__frequency_popluated = False
        self.__frequency_counts = {}
        self.__num_ngrams_in_model = 0
        self.__smoothed_frequency_counts = {}
        self.__smoothed_total = 0
        
    def __populate_frequencies(self, model):
        self.__frequency_popluated = True
        ngrams_counts_dict = model.get_counts()[model.get_n()]
        for _, count in ngrams_counts_dict.items():
            self.__frequency_counts[count] = self.__frequency_counts.get(count, 0) + 1
            self.__num_ngrams_in_model += count
        
        a, b = self.__fit_log_linear_regression()
        self.__compute_smoothed_counts(a, b)
                
    def __fit_log_linear_regression(self):
        sorted_frequencies = sorted(self.__frequency_counts)
        
        Z = {}
        for r in range(len(sorted_frequencies)):
            if r == 0:
                q = 0
            else:
                q = sorted_frequencies[r-1]
                
            if r == len(sorted_frequencies)-1:
                t = 2*sorted_frequencies[r] - q
            else:
                t = sorted_frequencies[r+1]
            
            Z[sorted_frequencies[r]] = self.__frequency_counts[sorted_frequencies[r]] / (0.5 * (t - q))
         
        x = np.array([math.log10(k) for k in Z.keys()])
        y = np.array([math.log10(v) for v in Z.values()])
        A = np.vstack([x, np.ones(len(x))]).T
        b, a = np.linalg.lstsq(A, y)[0]
        
        return (b, a)
    
    def __compute_smoothed_counts(self, a, b):
        sorted_frequencies = sorted(self.__frequency_counts)
        
        use_smooth_for_remaining = False
        for r in sorted_frequencies:
            smoothed_count = (r+1.0) * math.exp(a + b*math.log(r+1)) / math.exp(a + b*math.log(r))
            
            if r+1 not in self.__frequency_counts:
                use_smooth_for_remaining = True
                
            if use_smooth_for_remaining:
                self.__smoothed_frequency_counts[r] = smoothed_count
                continue
                
            turing_estimate = ((r+1.0) * self.__frequency_counts[r+1]) / self.__frequency_counts[r]
            std_dev_for_turing_estimate = math.sqrt( pow(r+1, 2) * \
                                                     (self.__frequency_counts[r+1] / pow(self.__frequency_counts[r],2) ) * \
                                                     (1.0 + (self.__frequency_counts[r+1] / self.__frequency_counts[r]))
                                                   )
            if abs( smoothed_count - turing_estimate ) <= 1.65 * std_dev_for_turing_estimate:
                self.__smoothed_frequency_counts[r] = smoothed_count
                use_smooth_for_remaining = True
                
            self.__smoothed_frequency_counts[r] = turing_estimate
        
        for frequency, smoothed_count in self.__smoothed_frequency_counts.items():
            self.__smoothed_total += self.__frequency_counts[frequency] * smoothed_count
        
    def handle_unknown_words(self):
        return True
    
    def calculate_probability(self, model, word_sequence):
        if self.__frequency_popluated == False:
            self.__populate_frequencies(model)
            
        prob_zero_frequency = self.__frequency_counts.get(1, 0) / self.__num_ngrams_in_model
        count_of_word_sequence = model.get_counts()[model.get_n()].get(word_sequence, 0)
        
        if count_of_word_sequence == 0:
            return prob_zero_frequency
        else:
            return (1.0 - prob_zero_frequency) * (self.__smoothed_frequency_counts[count_of_word_sequence]/self.__smoothed_total)
        

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
            
    
