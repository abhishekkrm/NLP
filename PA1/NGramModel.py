

class NGramModel(object):
    def __init__(self, corpus, N, smoother = None):
        self.__ngram_counts = {}
        self.__n = N
        self.__smoother = smoother
        self.__parse_corpus(corpus)
    
    def __parse_corpus(self, corpus):
        """ Parses the corpus and populates the counts table
        """
        pass
    
    def calculate_probability(self, unseen_mail):       
        """ Calculates the probability of this mail according to this model.
            Uses the smoother for smoothing. Note that it can be None for Unsmoothed ngrams
        """
        pass