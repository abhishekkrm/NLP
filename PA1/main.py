import os
import Parser
import NGramModel
import Classifier
import RandomSentenceGenerator
import Smoother

this_file_path = os.path.dirname(os.path.realpath( __file__)) 

class Controller(object):
    UP_LABEL = 'UPSPEAK'
    DOWN_LABEL = 'DOWNSPEAK'
    
    def __init__(self, training_file, validation_file, test_file):
        self.__up_train = Parser(training_file, Controller.UP_LABEL).get_parsed_content()
        self.__down_train = Parser(training_file, Controller.DOWN_LABEL).get_parsed_content()
        self.__up_validation = Parser(validation_file, Controller.UP_LABEL).get_parsed_content()
        self.__down_validation = Parser(validation_file, Controller.DOWN_LABEL).get_parsed_content()
        self.__updown_test = Parser(test_file).get_parsed_mails()
        
    def generate_ngrams(self, N, ISmoother=None):
        up_ngram_model = NGramModel.NGramModel(self.__up_train, N, ISmoother)
        down_ngram_model = NGramModel.NGramModel(self.__down_train, N, ISmoother)
        return (up_ngram_model, down_ngram_model)
    
    
def main():
    training_file = os.path.join(this_file_path, 'training.txt')
    validation_file = os.path.join(this_file_path, 'validation.txt')
    test_file = os.path.join(this_file_path, 'test.txt')
    
    controller = Controller(training_file, validation_file, test_file)
    up_unigram_unsmoothed_model, down_unigram_unsmoothed_model = controller.generate_ngrams(1)
    ''' Enhance Controller as per the requirements ''' 


if __name__ == "__main__":
    main()
    