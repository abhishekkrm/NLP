# Ref: http://stackoverflow.com/questions/4113307/pythonic-way-to-select-list-elements-with-different-probability
import random
import bisect
import NGramModel

class _WeightedSelector(object):
    def __init__(self, item_weight_dict):
        self.__items = []
        self.__weights = []
        self.__populate_items_weights(item_weight_dict)
        
    def __populate_items_weights(self, item_weight_dict):
        raw_weights = []
        for key, value in item_weight_dict.items():
            self.__items.append(key)
            raw_weights.append(value)
        
        sum_weights = sum(raw_weights)
        cumulative_weight = 0
        
        for raw_weight in raw_weights:
            cumulative_weight += raw_weight
            self.__weights.append(cumulative_weight/sum_weights)
    
    def select_item(self):
        return self.__items[ bisect.bisect(self.__weights, random.random()) ]
    
    
class RandomSentenceGenerator(object):
    def __init__(self, model):
        self.__model = model
        self.__prefix_weighted_selector_dict = {}
        self.__create_weighted_selector_dict(model)
        
    def __create_weighted_selector_dict(self, model):
        n = model.get_n()
        counts = model.get_counts()

        prefix_suffix_dict = {} 
        for n_gram in counts[n]:
            prefix = ' '.join(n_gram.split()[0:n-1])
            suffix = n_gram.split()[n-1]
            if prefix not in prefix_suffix_dict:
                prefix_suffix_dict[prefix] = {}
            prefix_suffix_dict[prefix][suffix] = prefix_suffix_dict[prefix].get(suffix, 0) + counts[n][n_gram]
            
        for prefix in prefix_suffix_dict:
            self.__prefix_weighted_selector_dict[prefix] = _WeightedSelector(prefix_suffix_dict[prefix])
            
    def generate_sentence(self):
        ''' Returns a randomly generated sentence using the model 
        '''
        n = self.__model.get_n()
        generated_sentence = []
        
        for _ in range(0, n):
            generated_sentence.append(NGramModel.NGramModel.START_SENTENCE_TOKEN)
            
        next_selected_word = ''
        while next_selected_word != NGramModel.NGramModel.END_SENTENCE_TOKEN:
            prefix = ''
            if n > 1:
                prefix = ' '.join(generated_sentence[-(n-1):])
            next_selected_word = self.__prefix_weighted_selector_dict[prefix].select_item()
            generated_sentence.append(next_selected_word)
            
        return ' '.join(generated_sentence[n:len(generated_sentence)-1])        
    

def test_cases():
    corpus = '<start> since our evaluation metric is based on test set probability it is important \
             not to let the test sentences into the training set </start> <start> suppose we are trying to \
             compute the probability of a particular test sentence </start> <start> if our test sentence is \
             part of the training corpus we will mistakenly assign it an artificially high probability when \
             it occurs in the test set </start> <start> we call this situation training on the test set \
             </start> <start> training on the test set introduces a bias that makes the probabilities all \
             look too high and causes huge inaccuracies in perplexity </start>'
    
    bigram_model = NGramModel.NGramModel(corpus, 2)
    bigram_sentence_generator = RandomSentenceGenerator(bigram_model)
    
    unigram_model = NGramModel.NGramModel(corpus, 1)
    unigram_sentence_generator = RandomSentenceGenerator(unigram_model)
    
    print(bigram_sentence_generator.generate_sentence())
    print(bigram_sentence_generator.generate_sentence())
    print(unigram_sentence_generator.generate_sentence())
    print(unigram_sentence_generator.generate_sentence())
    
if __name__ == '__main__':
    test_cases()
    
    