import os
import math
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
        
    def __generate_train_models(self, smoother):
        up_train_ngram_models = {}
        down_train_ngram_models = {}
        
        for n in range(1,4):
            up_train_ngram_models[n] = NGramModel.NGramModel(self.__up_train.get_parsed_content(), n, smoother)
            down_train_ngram_models[n] = NGramModel.NGramModel(self.__down_train.get_parsed_content(), n, smoother)  
        
        return (up_train_ngram_models, down_train_ngram_models)
    
    def generate_most_frequent_ngrams(self):
        print('Part 2.2 - Unsmoothed n-grams')
        up_train_ngram_models, down_train_ngram_models = self.__generate_train_models(Smoother.UnSmoother())
        for n in range(1,4):
            up_train_model_counts = up_train_ngram_models[n].get_counts()[n]
            up_train_model_counts_sorted = sorted(up_train_model_counts, key=up_train_model_counts.get)
            print('N = %d, UP_TRAIN, Most frequent n-grams: %s' %(n, up_train_model_counts_sorted[0:10]))
            
            down_train_model_counts = down_train_ngram_models[n].get_counts()[n]
            down_train_model_counts_sorted = sorted(down_train_model_counts, key=down_train_model_counts.get)
            print('N = %d, DOWN_TRAIN, Most frequent n-grams: %s' %(n, down_train_model_counts_sorted[0:10]))
    
    def generate_random_sentences(self):
        print('Part 2.3 - Random Sentence Generation')
        up_train_ngram_models, down_train_ngram_models = self.__generate_train_models(Smoother.UnSmoother())
        for n in range(1,4):
            up_train_random_sentence_generator = RandomSentenceGenerator(up_train_ngram_models[n])
            down_train_random_sentence_generator = RandomSentenceGenerator(down_train_ngram_models[n])
            
            print('N = %d, UP_TRAIN, Random Sentences:' %(n))
            for _ in range(5):
                print(up_train_random_sentence_generator.generate_sentence())
                
            print('N = %d, DOWN_TRAIN, Random Sentences:' %(n))
            for _ in range(5):
                print(down_train_random_sentence_generator.generate_sentence())
                
    def compute_perplexity(self, dataset, model):
        log_probability = model.calculate_probability(dataset.get_parsed_content())
        probability = math.pow(10, log_probability)
        num_tokens = model.get_num_tokens()
        perplexity = pow( (1/probability), (1/num_tokens))
        return perplexity
    
    def compute_perplexities(self):
        print('Part 2.5 - Perplexity')
        up_train_ngram_models, down_train_ngram_models = self.__generate_train_models(Smoother.LaplaceSmoother())
        for n in range(1,4):
            up_validation_perplexity = self.compute_perplexity(self.__up_validation, up_train_ngram_models[n])
            down_validation_perplexity = self.compute_perplexity(self.__down_validation, down_train_ngram_models[n])
            
            print('N = %d, UP_TRAIN, Perplexity = %f' %(n, up_validation_perplexity))
            print('N = %d, DOWN_TRAIN, Perplexity = %f' %(n, down_validation_perplexity))
            
    def calculate_unseen_email_probability(self, output_file_name = 'kaggle.txt'):
        #It is hard-coded to run for trigrams
        up_train_model = NGramModel.NGramModel(self.__up_train.get_parsed_content(), 3)
        down_train_model = NGramModel.NGramModel(self.__down_train.get_parsed_content(), 3)
        
        classifier = Classifier.Classifier(up_train_model, down_train_model)
        
        with open(output_file_name, 'w') as output_file:
            mail_id = 1
            for mail in self.__updown_test.get_parsed_mails():
                output_file.write( '%d,%d\n' %(mail_id, classifier.classify_mail(mail)))
                mail_id+=1
    
    
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
    #controller.compute_perplexities()
    #Calculate UP/DOWN probability of unseen emails
    controller.calculate_unseen_email_probability()
    

if __name__ == "__main__":
    main()
    
