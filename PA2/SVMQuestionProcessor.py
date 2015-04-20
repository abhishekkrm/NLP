import Utils
from QuestionProcessor import IQuestionProcessor
from sklearn.svm import LinearSVC
from nltk.classify.scikitlearn import SklearnClassifier

class SVMQuestionProcessor(IQuestionProcessor):
    def __init__(self, training_file, N_Gram = 2):
        self.__classifier = SklearnClassifier(LinearSVC())
        self.__feature_set = set()
        self.__TrainClassifier(training_file, N_Gram)
        
    def __PopulateFeatureSet(self, training_file, N_Gram):
        with open(training_file) as t_file:
            for line in t_file:
                n_grams = Utils.GetNGrams(' '.join(line.strip().split()[1:]), N_Gram)
                for n_gram in n_grams:
                    self.__feature_set.add(n_gram)

    def __BuildQuestionVector(self, question_text):
        question_n_grams = Utils.GetNGrams(question_text)
                
        question_vector = {}
        for feature in self.__feature_set:
            question_vector[feature] = feature in question_n_grams
        
        return question_vector
    
    def __TrainClassifier(self, training_file, N_Gram):
        self.__PopulateFeatureSet(training_file, N_Gram)
        
        labeled_featuresets = []
        with open(training_file) as t_file:
            for label_question in t_file:
                label = label_question.strip().split()[0]
                question_text = ' '.join(label_question.strip().split()[1:])
                labeled_featuresets.append((self.__BuildQuestionVector(question_text), label))
        
        self.__classifier.train(labeled_featuresets)
    
    def GetAnswerType(self, question):
        question_vector = self.__BuildQuestionVector(question.GetRawQuestion())
        return self.__classifier.classify(question_vector)
    
    def GetQueryKeywords(self, question):
        question_text_without_stop_words =  Utils.RemoveStopwords(question.GetRawQuestion())
        return question_text_without_stop_words.split()
