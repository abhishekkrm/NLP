import os
from Parser import Parser
import NGramModel
import Classifier
import Smoother
from RandomSentenceGenerator import RandomSentenceGenerator

this_file_path = os.path.dirname(os.path.realpath( __file__)) 

class Controller(object):
    UP_LABEL = 'UPSPEAK'
    DOWN_LABEL = 'DOWNSPEAK'
    
    def __init__(self, training_file, validation_file, test_file):
        self.__up_train = Parser(training_file, Controller.UP_LABEL)
        self.__down_train = Parser(training_file, Controller.DOWN_LABEL)
        self.__up_validation = Parser(validation_file, Controller.UP_LABEL)
        self.__down_validation = Parser(validation_file, Controller.DOWN_LABEL)
        self.__updown_test = Parser(test_file)
        self.__up_train_ngram_models = {}
        self.__down_train_ngram_models = {}
        self.__generate_train_models()
        
    def __generate_train_models(self):
        for n in range(1,4):
            self.__up_train_ngram_models[n] = NGramModel.NGramModel(self.__up_train.get_parsed_content(), n)
            self.__down_train_ngram_models[n] = NGramModel.NGramModel(self.__down_train.get_parsed_content(), n)  
    
    def generate_most_frequent_ngrams(self):
        print('Part 2.2 - Unsmoothed n-grams')
        for n in range(1,4):
            up_train_model_counts = self.__up_train_ngram_models[n].get_counts()[n]
            up_train_model_counts_sorted = sorted(up_train_model_counts, key=up_train_model_counts.get)
            print('N = %d, UP_TRAIN, Most frequent n-grams: %s' %(n, up_train_model_counts_sorted[0:10]))
            
            down_train_model_counts = self.__down_train_ngram_models[n].get_counts()[n]
            down_train_model_counts_sorted = sorted(down_train_model_counts, key=down_train_model_counts.get)
            print('N = %d, DOWN_TRAIN, Most frequent n-grams: %s' %(n, down_train_model_counts_sorted[0:10]))
    
    def compute_perplexities(self):
        print('Part 2.5 - Perplexity')
        laplace_smoother = Smoother.LaplaceSmoother()
        for n in range(1,4):
            up_train_ngram_model = NGramModel.NGramModel(self.__up_train.get_parsed_content(), n, laplace_smoother)
            down_train_ngram_model = NGramModel.NGramModel(self.__down_train.get_parsed_content(), n, laplace_smoother)
            
            up_validation_probability = up_train_ngram_model.calculate_probability(self.__up_validation.get_parsed_content())
            up_validation_total_tokens = up_train_ngram_model.get_num_tokens()
            up_validation_perplexity = pow( (1/up_validation_probability), (1/up_validation_total_tokens))
            
            down_validation_probability = down_train_ngram_model.calculate_probability(self.__down_validation.get_parsed_content())
            down_validation_total_tokens = down_train_ngram_model.get_num_tokens()
            down_validation_perplexity = pow( (1/down_validation_probability), (1/down_validation_total_tokens))
            
            print('N = %d, UP_TRAIN, Perplexity = %f' %(n, up_validation_perplexity))
            print('N = %d, DOWN_TRAIN, Perplexity = %f' %(n, down_validation_perplexity))
            
    def generate_random_sentences(self):
        print('Part 2.3 - Random Sentence Generation')
        for n in range(1,4):
            up_train_random_sentence_generator = RandomSentenceGenerator(self.__up_train_ngram_models[n])
            down_train_random_sentence_generator = RandomSentenceGenerator(self.__down_train_ngram_models[n])
            
            print('N = %d, UP_TRAIN, Random Sentences:' %(n))
            for _ in range(5):
                print(up_train_random_sentence_generator.generate_sentence())
                
            print('N = %d, DOWN_TRAIN, Random Sentences:' %(n))
            for _ in range(5):
                print(down_train_random_sentence_generator.generate_sentence())
    
    
def main():
    training_file = os.path.join(this_file_path, 'training.txt')
   
    validation_file = os.path.join(this_file_path, 'validation.txt')
    test_file = os.path.join(this_file_path, 'test.txt')
    
    #part 2.1
    controller = Controller(training_file, validation_file, test_file)
    #part2.2
    controller.generate_most_frequent_ngrams()
    #part 2.3
    controller.generate_random_sentences()
    #part 2.4 and 2.5
    controller.compute_perplexities()
    

if __name__ == "__main__":
    main()
    
