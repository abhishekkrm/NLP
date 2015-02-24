import os
from Parser import Parser
import NGramModel
import Classifier
import Smoother
from RandomSentenceGenerator import RandomSentenceGenerator

this_file_path = os.path.dirname(os.path.realpath( __file__)) 

class Controller(object):
    def __init__(self, training_file, validation_file, test_file, remove_punctuation = True, lowercase = True, use_stemmer = False, use_lemmetizer = False):
        self.__up_train = Parser(training_file, Parser.UP_LABEL, remove_punctuation, lowercase, use_stemmer, use_lemmetizer)
        self.__down_train = Parser(training_file, Parser.DOWN_LABEL, remove_punctuation, lowercase, use_stemmer, use_lemmetizer)
        self.__up_validation = Parser(validation_file, Parser.UP_LABEL, remove_punctuation, lowercase, use_stemmer, use_lemmetizer)
        self.__down_validation = Parser(validation_file, Parser.DOWN_LABEL, remove_punctuation, lowercase, use_stemmer, use_lemmetizer)
        self.__updown_test = Parser(test_file, remove_punctuation=remove_punctuation, lowercase=lowercase, use_stemmer=use_stemmer, use_lemmetizer=use_lemmetizer)
        
    def __generate_train_models(self, smoother):
        up_train_ngram_models = {}
        down_train_ngram_models = {}
        
        for n in range(1,4):
            up_train_ngram_models[n] = NGramModel.NGramModel(self.__up_train.get_parsed_content(), n, smoother())
            down_train_ngram_models[n] = NGramModel.NGramModel(self.__down_train.get_parsed_content(), n, smoother())  
        
        return (up_train_ngram_models, down_train_ngram_models)
    
    def generate_most_frequent_ngrams(self):
        print('Part 2.2 - Unsmoothed n-grams')
        up_train_ngram_models, down_train_ngram_models = self.__generate_train_models(Smoother.UnSmoother)
        for n in range(1,4):
            up_train_model_counts = up_train_ngram_models[n].get_counts()[n]
            up_train_model_counts_sorted = sorted(up_train_model_counts, key=up_train_model_counts.get)
            print('N = %d, UP_TRAIN, Most frequent n-grams: %s' %(n, up_train_model_counts_sorted[0:10]))
            
            down_train_model_counts = down_train_ngram_models[n].get_counts()[n]
            down_train_model_counts_sorted = sorted(down_train_model_counts, key=down_train_model_counts.get)
            print('N = %d, DOWN_TRAIN, Most frequent n-grams: %s' %(n, down_train_model_counts_sorted[0:10]))
    
    def generate_random_sentences(self):
        print('Part 2.3 - Random Sentence Generation')
        up_train_ngram_models, down_train_ngram_models = self.__generate_train_models(Smoother.UnSmoother)
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
        parsed_dataset = dataset.get_parsed_content()
        parsed_dataset_words = parsed_dataset.split()
        
        log_probability = model.calculate_probability(parsed_dataset)
        num_tokens = len(parsed_dataset_words) - parsed_dataset_words.count(NGramModel.NGramModel.START_SENTENCE_TOKEN)
        
        log_perplexity = -1*(1/num_tokens)*log_probability
        perplexity = pow(10,log_perplexity) 
        
        return perplexity
    
    def compute_perplexities(self):
        print('Part 2.5 - Perplexity')
        up_train_ngram_models, down_train_ngram_models = self.__generate_train_models(Smoother.LaplaceSmoother)
        for n in range(1,4):
            up_validation_perplexity = self.compute_perplexity(self.__up_validation, up_train_ngram_models[n])
            down_validation_perplexity = self.compute_perplexity(self.__down_validation, down_train_ngram_models[n])
            
            print('N = %d, UP_TRAIN, Perplexity = %f' %(n, up_validation_perplexity))
            print('N = %d, DOWN_TRAIN, Perplexity = %f' %(n, down_validation_perplexity))
            
    def generate_kaggle_file_for_test_data(self, N, smoother, unknown_threshold, output_file_name = 'kaggle.csv'):
        up_train_model = NGramModel.NGramModel(self.__up_train.get_parsed_content(), N, smoother(), unknown_threshold)
        down_train_model = NGramModel.NGramModel(self.__down_train.get_parsed_content(), N, smoother(), unknown_threshold)
        
        classifier = Classifier.Classifier(up_train_model, down_train_model)
        
        up_predicted = 0
        down_predicted = 0
        
        with open(output_file_name, 'w') as output_file:
            output_file.write('Id,Prediction\n')
            mail_id = 1
            for mail in self.__updown_test.get_parsed_mails():
                predicted_classification = classifier.classify_mail(mail)
                output_file.write( '%d,%d\n' %(mail_id, predicted_classification))
                
                if predicted_classification == Classifier.Classifier.UP_SPEAK:  
                    up_predicted+=1
                if predicted_classification == Classifier.Classifier.DOWN_SPEAK:    
                    down_predicted+=1
                mail_id+=1
        #stats
        print('Total Mails: %d, Up Classified = %d, Down Classified = %d' %(up_predicted + down_predicted, up_predicted, down_predicted))
        
    def count_correct_classification(self, up_model, down_model, dataset, actual_label):
        num_correct_classified = 0
        num_total_mails = len(dataset.get_parsed_mails())
        classifier = Classifier.Classifier(up_model, down_model)
        for mail in dataset.get_parsed_mails():
            if classifier.classify_mail(mail) == actual_label:
                num_correct_classified += 1
        return num_total_mails, num_correct_classified
    
    def validate_classifications(self, N, smoother, unknown_threshold):
        train_up_model = NGramModel.NGramModel(self.__up_train.get_parsed_content(), N, smoother(), unknown_threshold)
        train_down_model = NGramModel.NGramModel(self.__down_train.get_parsed_content(), N, smoother(), unknown_threshold)
        up_total, up_correct = self.count_correct_classification(train_up_model, train_down_model, self.__up_validation, Classifier.Classifier.UP_SPEAK) 
        down_total, down_correct = self.count_correct_classification(train_up_model, train_down_model, self.__down_validation, Classifier.Classifier.DOWN_SPEAK)
        print('UPSPEAK Total = %d, Correct = %d, Percentage = %f' %(up_total, up_correct, (up_correct/up_total)*100))
        print('DOWNSPEAK Total = %d, Correct = %d, Percentage = %f' %(down_total, down_correct, (down_correct/down_total)*100))
        print('COMMULATIVE Total = %d, Correct = %d, Percentage = %f'%(up_total+down_total, up_correct+down_correct, ((up_correct+down_correct)/(up_total+down_total))*100))

        
def validate_bulk(training_file, validation_file, test_file, smoother):
    for remove_punctuation in (True, False):
        for lowercase in (True, False):
            controller = Controller(training_file, validation_file, test_file, remove_punctuation, lowercase)
            for N in range(2, 6):
                for unknown_threshold in range(2, 6):
                    print('---------------------------------------------------------------------------------------')
                    print('Remove Punctuation = %s, Lowewrcase = %s, N = %d, Unknown Threshold = %d, Smoother = %s' %(remove_punctuation, lowercase, N, unknown_threshold, smoother.__name__))
                    controller.validate_classifications(N, smoother, unknown_threshold)
                    print('---------------------------------------------------------------------------------------\n')

def generate_kaggle_file(training_file, validation_file, test_file):
    controller_1 = Controller(training_file, validation_file, test_file, False, False)
    controller_1.generate_kaggle_file_for_test_data(5, Smoother.LaplaceSmoother, 5, 'vote1.csv')
    
    controller_2 = Controller(training_file, validation_file, test_file, True, True, use_lemmetizer=True)
    controller_2.generate_kaggle_file_for_test_data(5, Smoother.LaplaceSmoother, 5, 'vote2.csv')
    
    controller_3 = Controller(training_file, validation_file, test_file, True, False, use_stemmer=True)
    controller_3.generate_kaggle_file_for_test_data(5, Smoother.LaplaceSmoother, 5, 'vote3.csv')
    
    generate_majority_vote_file('vote1.csv', 'vote2.csv', 'vote3.csv')
    
def read_vote_file( file_name ):
    mail_pred_dict = {}
    with open(file_name) as file:
        for line in file.readlines():
            mail_id = line.strip().split(',')[0]
            prediction = line.strip().split(',')[1]
            if mail_id.isdigit():
                mail_pred_dict[mail_id] = prediction
    return mail_pred_dict

def generate_majority_vote_file( vote1_file, vote2_file, vote3_file, output_file = 'majority_vote.csv' ):
    vote1_dict = read_vote_file( vote1_file )
    vote2_dict = read_vote_file( vote2_file )
    vote3_dict = read_vote_file( vote3_file )
    
    final_decision = {}
    for mail_id in vote1_dict:
        votes = [vote1_dict[mail_id], vote2_dict[mail_id], vote3_dict[mail_id]]
        final_decision[mail_id] = max(set(votes), key=votes.count)
        
    sorted_mail_ids = sorted([int(mail_id) for mail_id in final_decision])
    with open(output_file, 'w') as out_file:
        out_file.write('Id,Prediction\n')
        for mail_id in sorted_mail_ids:
            out_file.write('%s,%s\n' %(mail_id, final_decision[str(mail_id)]))

def main():
    training_file = os.path.join(this_file_path, 'training.txt')
    validation_file = os.path.join(this_file_path, 'validation.txt')
    test_file = os.path.join(this_file_path, 'test.txt')
    
    #part 2.1 - Default Controller with remove_punctuation and lowercase set to True
    controller = Controller(training_file, validation_file, test_file, False, False)
    #part2.2
    controller.generate_most_frequent_ngrams()
    #part 2.3
    controller.generate_random_sentences()
    #part 2.4 and 2.5
    controller.compute_perplexities()
    #Generate Kaggle submission file
    generate_kaggle_file(training_file, validation_file, test_file)
    #single validation
    #controller.validate_classifications(5, Smoother.LaplaceSmoother, 3)
    #bulk validation
    #validate_bulk(training_file, validation_file, test_file, Smoother.GTSmoother)
    #validate_bulk(training_file, validation_file, test_file, Smoother.SimpleGTSmoother)


if __name__ == "__main__":
    main()
    
