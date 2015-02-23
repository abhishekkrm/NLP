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

class SimpleGTSmoother(ISmoother):
    def __init__(self, k = 5):
        self.__k = k
        self.__freq_populated = False
        self.__freq_count = {} 
        self.__gt_n = 0
        self.__a = 0
        self.__b = 0
        
    def handle_unknown_words(self):
        return True
    
    def __calculate_frequency_count(self,model):
        ngrams_counts = model.get_counts()[model.get_n()]
        for ngram in ngrams_counts:
            self.__freq_count[ngrams_counts[ngram]] = self.__freq_count.get(ngrams_counts[ngram], 0) + 1
            self.__gt_n += ngrams_counts[ngram]
        self.__perform_smoothing()
        self.__freq_populated = True 
        
    def __perform_smoothing(self):
        sorted_freq = sorted(self.__freq_count)
        
        Z = {}
        for r in range(len(sorted_freq)):
            if r == 0:
                q = 0
            else:
                q = sorted_freq[r-1]
                
            if r == len(sorted_freq)-1:
                t = 2*sorted_freq[r] - q
            else:
                t = sorted_freq[r+1]
            
            Z[sorted_freq[r]] = self.__freq_count[sorted_freq[r]] / (0.5 * (t - q))
         
        print(Z)
        x = np.array([math.log10(k) for k in Z.keys()])
        y = np.array([math.log10(v) for v in Z.values()])
        A = np.vstack([x, np.ones(len(x))]).T
        self.__b, self.__a = np.linalg.lstsq(A, y)[0]
    
    def __get_smoothed_freq_count(self, freq):
        freq_count = self.__freq_count.get(freq, 0)
        smoothed_freq_count = pow(10, self.__a + self.__b * math.log10(freq))
        return smoothed_freq_count
#         if freq_count == 0:
#             return smoothed_freq_count
#         
#         #varaiance_turing_freq = pow((freq + 1),2) * (self.__freq_count.get(freq + 1, 0)/pow(self.__freq_count.get(freq, 0), 2)) * ( 1 + (self.__freq_count.get(freq + 1, 0)/self.__freq_count.get(freq, 0)) )
#         
#         if abs(freq_count - smoothed_freq_count)  <= 1.65 * math.sqrt(varaiance_turing_freq):
#             freq_count = smoothed_freq_count
#         
#         return freq_count
#     
    def __get_c_star(self, model, word_sequence):
        freq_word_sequence = model.get_counts()[model.get_n()].get(word_sequence, 0)
        if freq_word_sequence == 0:
            return self.__get_smoothed_freq_count(1)
        elif freq_word_sequence <= self.__k:
            #return (freq_word_sequence + 1) * ( self.__get_smoothed_freq_count(freq_word_sequence+1)/self.__get_smoothed_freq_count(freq_word_sequence) )
            part_1 = (freq_word_sequence + 1) * ( self.__get_smoothed_freq_count(freq_word_sequence+1)/self.__get_smoothed_freq_count(freq_word_sequence) )
            part_2 = (freq_word_sequence) * ( ((self.__k+1)*self.__get_smoothed_freq_count(self.__k+1))/self.__get_smoothed_freq_count(1) )
            part_3 = 1- ( ((self.__k+1)*self.__get_smoothed_freq_count(self.__k+1))/self.__get_smoothed_freq_count(1) )
            return (part_1 - part_2) / part_3
        else:
            return freq_word_sequence
#         if(c < self.__k):
#             
#             return self.__freq_count.get(1,0)/self.__gt_n
#         else:
#             numerator=(c+1)*self.__freq_count.get(c+1,0)
#             denominator = self.__freq_count.get(c,0)
#             if(numerator==0 or denominator==0):
#                 return 0;
#             else:
#                 return numerator/(denominator*self.__gt_n)
#             pass
    
    def calculate_probability(self, model, word_sequence):
        if(self.__freq_populated == False):
            self.__calculate_frequency_count(model)
            
        return (self.__get_c_star(model, word_sequence) / self.__gt_n)
       
        

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
            
    
