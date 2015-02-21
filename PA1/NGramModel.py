# Ref: http://stackoverflow.com/questions/12488722/counting-bigrams-pair-of-two-words-in-a-file-using-python
from itertools import tee, islice
from collections import Counter
import math
import re
import Smoother

class NGramModel(object):
    START_SENTENCE_TOKEN = '<start>'
    END_SENTENCE_TOKEN = '</start>'
    UNKNOWN_WORD_TOKEN = '<unk>'
    UNKNOWN_THRESHOLD = 5
    
    def __init__(self, corpus, N, smoother = Smoother.UnSmoother()):
        self.__ngram_counts = {}
        self.__n = N
        self.__smoother = smoother
        self.__parse_corpus(corpus)
    
    def __parse_corpus(self, corpus):
        """ Parses the corpus and populates the counts table
        """
        corpus = self.__handle_corpus_unkwon_words(corpus)
        start_token = ' '.join([NGramModel.START_SENTENCE_TOKEN]*(self.__n-1))
        word_list = corpus.replace(NGramModel.START_SENTENCE_TOKEN, start_token).split()
            
        for n in range(1, self.__n+1):    
            self.__ngram_counts[n] = {}
            for ngram, count in Counter(self.__generate_n_grams(word_list, n)).items():
                self.__ngram_counts[n][' '.join(ngram)] = count
    
    def __handle_corpus_unkwon_words(self, corpus):
        if self.__smoother.handle_unknown_words():
            for word, count in Counter(corpus.split()).items():
                if count < NGramModel.UNKNOWN_THRESHOLD:
                    corpus = re.sub(r'\b' + word + r'\b', NGramModel.UNKNOWN_WORD_TOKEN, corpus)
        return corpus
    
    def __handle_unseen_mail_unknown_words(self, unseen_mail):
        if self.__smoother.handle_unknown_words():
            for word in unseen_mail.split():
                if word not in self.__ngram_counts[1]:
                    unseen_mail = re.sub(r'\b' + word + r'\b', NGramModel.UNKNOWN_WORD_TOKEN, unseen_mail)
        return unseen_mail
    
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
        unseen_mail = self.__handle_unseen_mail_unknown_words(unseen_mail)
        
        start_token = ' '.join([NGramModel.START_SENTENCE_TOKEN]*(self.__n-1));
        sentences = unseen_mail.replace(NGramModel.START_SENTENCE_TOKEN, start_token).split(NGramModel.END_SENTENCE_TOKEN)
        
        log_probability = 0;
        for sentence in sentences:
            word_list = sentence.split()
            word_list.append(NGramModel.END_SENTENCE_TOKEN)
            
            for ngram in self.__generate_n_grams(word_list, self.__n):
                probability = self.__smoother.calculate_probability(self, ' '.join(ngram))
                if probability == 0:
                    return 0
                log_probability += math.log10(probability)
        
        return log_probability
    
    def get_n(self):
        return self.__n
    
    def get_counts(self):
        return self.__ngram_counts
    
    def get_num_tokens(self):
        return sum(self.__ngram_counts[1].values()) - self.__ngram_counts[1].get(NGramModel.START_SENTENCE_TOKEN, 0)
    
    def get_vocab_size(self):
        return len(self.__ngram_counts[1])
    
    