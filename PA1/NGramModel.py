# Ref: http://stackoverflow.com/questions/12488722/counting-bigrams-pair-of-two-words-in-a-file-using-python
from itertools import tee, islice
from collections import Counter

class NGramModel(object):
    START_SENTENCE_TOKEN = '<start>'
    END_SENTENCE_TOKEN = '</start>'

    def __init__(self, corpus, N, smoother = None):
        self.__ngram_counts = {}
        self.__n = N
        self.__smoother = smoother
        self.__parse_corpus(corpus)
    
    def __parse_corpus(self, corpus):
        """ Parses the corpus and populates the counts table
        """
        for n in range(1, self.__n+1):
            start_token = ' '.join([NGramModel.START_SENTENCE_TOKEN]*n)
            word_list = corpus.replace(NGramModel.START_SENTENCE_TOKEN, start_token).split()
            
            self.__ngram_counts[n] = {}
            for ngram, count in Counter(self.__generate_n_grams(word_list, n)).items():
                self.__ngram_counts[n][' '.join(ngram)] = count
            
            self.__ngram_counts[n].pop(start_token, None)
    
    def __generate_n_grams(self, word_list, n):
        local_word_list = word_list
        while True:
            iter1, iter2 = tee(local_word_list)
            ngram = tuple(islice(iter1, n))
            if len(ngram) == n:
                yield ngram
                next(iter2)
                local_word_list = iter2
            else:
                break
    
    def calculate_probability(self, unseen_mail):       
        """ Calculates the probability of this mail according to this model.
            Uses the smoother for smoothing. Note that it can be None for Unsmoothed ngrams
        """
        pass
    
    def get_n(self):
        return self.__n
    
    def get_counts(self):
        return self.__ngram_counts
    
    def get_num_tokens(self):
        return sum(self.__ngram_counts[1].values())
    
    def get_vocab_size(self):
        return len(self.__ngram_counts[1]) + 1 #for <start>
    
    