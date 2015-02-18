
from nltk.util import ngrams
class NGramModel(object):
    def __init__(self, corpus, N, smoother = None):
        self.__ngram_counts = {}
        self.__nMinusOnegram_counts={}
        self.__n = N
        self.__smoother = smoother
        self.__parse_corpus(corpus)
    
    def __parse_corpus(self, corpus):
        """ Parses the corpus and populates the counts table
        """
        allNgrams = ngrams(corpus.split(), self.__n)

	# Count the ngrams
        for grams in allNgrams:
            if grams in self.__ngram_counts:
                self.__ngram_counts[grams]=self.__ngram_counts[grams]+1
            else:
                self.__ngram_counts[grams]=1
	# Count the (n-1)grams if n>1
        if self.__n>1:
            allNgrams = ngrams(corpus.split(), self.__n-1)
            for grams in allNgrams:
                if grams in self.__nMinusOnegram_counts:
                    self.__nMinusOnegram_counts[grams]=self.__nMinusOnegram_counts[grams]+1
                else:
                    self.__nMinusOnegram_counts[grams]=1
        pass
    
    def calculate_probability(self, unseen_mail):       
        """ Calculates the probability of this mail according to this model.
            Uses the smoother for smoothing. Note that it can be None for Unsmoothed ngrams
        """

        pass
