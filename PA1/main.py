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
        laplace_smoother = Smoother.LaplaceSmoother()
        for n in range(1,4):
            self.__up_train_ngram_models[n] = NGramModel.NGramModel(self.__up_train.get_parsed_content(), n, laplace_smoother)
            self.__down_train_ngram_models[n] = NGramModel.NGramModel(self.__down_train.get_parsed_content(), n, laplace_smoother)  
    
    def compute_perplexities(self):
        print('Part 2.5 - Perplexity')
        for n in range(1,4):
            up_validation_probability = self.__up_train_ngram_models[n].calculate_probability(self.__up_validation.get_parsed_content())
            up_validation_total_tokens = sum(self.__up_train_ngram_models[n].get_counts()[1].values())
            up_validation_perplexity = pow( (1/up_validation_probability), (1/up_validation_total_tokens))
            
            down_validation_probability = self.__down_train_ngram_models[n].calculate_probability(self.__down_validation.get_parsed_content())
            down_validation_total_tokens = sum(self.__down_train_ngram_models[n].get_counts()[1].values())
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
    
    controller = Controller(training_file, validation_file, test_file)
    #part 2.3
    controller.generate_random_sentences()
    #part 2.5
    controller.compute_perplexities()
    

if __name__ == "__main__":
    main()
    
