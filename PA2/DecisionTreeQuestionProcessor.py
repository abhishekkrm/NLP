import os
import nltk
import Utils
from QuestionProcessor import IQuestionProcessor

this_file_path = os.path.dirname(os.path.realpath(os.path.basename(__file__)))
dt_dump_file = os.path.join(this_file_path, 'dt_qtype_classifications.txt')

class DecisionTreeQuestionProcessor(IQuestionProcessor):
    def __init__(self, training_file, N_Gram = 2):    
        self.__classifier = None
        self.__feature_set = set()
        self.__N_Gram = N_Gram
        self.__training_file = training_file
        self.__question_classifications = {}
        self.__ParseDumpFile()
        
    def __ParseDumpFile(self):
        if os.path.exists(dt_dump_file):
            with open(dt_dump_file) as dump_file:
                for line in dump_file:
                    question_number_and_classification = line.strip().split('~')
                    assert len(question_number_and_classification)==2
                    
                    question_number = int(question_number_and_classification[0])
                    classification = question_number_and_classification[1]
                    self.__question_classifications[question_number] = classification
    
    def __PopulateFeatureSet(self, training_file):
        with open(training_file) as t_file:
            for line in t_file:
                n_grams = Utils.GetNGrams(' '.join(line.strip().split()[1:]), self.__N_Gram)
                for n_gram in n_grams:
                    self.__feature_set.add(n_gram)
    
    def __BuildQuestionVector(self, question_text):
        question_n_grams = Utils.GetNGrams(question_text, self.__N_Gram)
                
        question_vector = {}
        for feature in self.__feature_set:
            question_vector[feature] = feature in question_n_grams
        
        return question_vector
    
    def __TrainClassifier(self):
        #make sure to train only once
        if self.__classifier:
            return
        
        self.__PopulateFeatureSet(self.__training_file)
        
        labeled_featuresets = []
        with open(self.__training_file) as t_file:
            for label_question in t_file:
                label = label_question.strip().split()[0]
                question_text = ' '.join(label_question.strip().split()[1:])
                labeled_featuresets.append((self.__BuildQuestionVector(question_text), label))
        
        self.__classifier = nltk.classify.DecisionTreeClassifier.train(labeled_featuresets, entropy_cutoff=0,support_cutoff=0)
    
    def GetAnswerType(self, question):
        question_number = question.GetQuestionNumber()
        if question_number in self.__question_classifications:
            return self.__question_classifications[question_number] 
        
        #Lazy Training
        self.__TrainClassifier()
        
        question_vector = self.__BuildQuestionVector(question.GetRawQuestion())
        classification = self.__classifier.classify(question_vector)
        
        self.__question_classifications[question.GetQuestionNumber()] = classification
        return classification
    
    def GetQueryKeywords(self, question):
        question_text_without_stop_words =  Utils.RemoveStopwords(question.GetRawQuestion())
        return question_text_without_stop_words.split()
    
    def DumpInfo(self):
        with open(dt_dump_file, 'w') as dump_file:
            for question_number, classification in self.__question_classifications.items():
                dump_file.write(str(question_number) + '~' + classification + '\n')
